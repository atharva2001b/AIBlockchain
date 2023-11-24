import hashlib
import time
import csv
import os  # Import the os module for file checking


class Transaction:
    def __init__(self, transaction_id, sender, receiver, amount):
        self.transaction_id = transaction_id
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # A simple hash function (for illustration purposes)
        transaction_data = ""
        for transaction in self.transactions:
            transaction_data += (
                transaction.sender
                + transaction.receiver
                + str(transaction.amount)
            )
        return hashlib.sha256(
            (
                str(self.index)
                + str(self.timestamp)
                + transaction_data
                + str(self.previous_hash)
                + str(self.nonce)
            ).encode()
        ).hexdigest()

    def mine_block(self, difficulty):
        print("Mining block...")
        time.sleep(1)  # Simulate mining time
        start_time = time.time()
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        end_time = time.time()
        mining_time = end_time - start_time
        print(f"Block mined in {mining_time:.4f} seconds. Hash: {self.hash}")
        return mining_time

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2  # Adjust the difficulty level as needed

    def create_genesis_block(self):
        return Block(0, time.time(), [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, transactions):
        print("Initiating transaction...")
        time.sleep(1)  # Simulate transaction initiation time
        start_time = time.time()
        index = len(self.chain)
        timestamp = time.time()
        previous_hash = self.get_latest_block().hash
        new_block = Block(index, timestamp, transactions, previous_hash)
        mining_time = new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Transaction completed in {total_time:.4f} seconds.")

        # Save transaction details to CSV
        self.save_transaction_details(index, mining_time, total_time)

    def save_transaction_details(self, block_index, mining_time, total_time):
        file_exists = os.path.isfile("transaction_details.csv")

        with open("transaction_details.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:  # Write header only if the file is newly created
                writer.writerow(["Transaction ID", "Mining Time", "Total Transaction Time"])

            # Determine the last index in the CSV file
            last_index = 0
            if file_exists:
                with open("transaction_details.csv", mode="r") as read_file:
                    reader = csv.reader(read_file)
                    next(reader)  # Skip the header row

                    for row in reader:
                        last_index = int(row[0])

            # Write new transactions starting from the next index
            writer.writerow([last_index + 1, mining_time, total_time])

# Example usage:
my_blockchain = Blockchain()

# Adding blocks to the blockchain with real-world transactions
transactions1 = [Transaction(1, "Alice", "Bob", 10), Transaction(2, "Bob",
"Charlie", 5)]
my_blockchain.add_block(transactions1)

transactions2 = [Transaction(3, "Charlie", "Alice", 7), Transaction(4,
"Bob", "Alice", 3)]
my_blockchain.add_block(transactions2)
