import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

class FraudDetectionAI:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.data = pd.read_csv(csv_file_path)

    def train_random_forest(self, test_size=0.2, random_state=42):
        # Assuming 'Mining Time' and 'Total Transaction Time' are features, and 'FraudLabel' is the target variable
        X = self.data[['Mining Time', 'Total Transaction Time']]
        y = self.data['FraudLabel']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

        # Train Random Forest classifier
        rf_classifier = RandomForestClassifier(n_estimators=100, random_state=random_state)
        rf_classifier.fit(X_train, y_train)

        # Evaluate Random Forest on the test set
        y_pred_rf = rf_classifier.predict(X_test)
        print("Random Forest Classification Report:")
        print(classification_report(y_test, y_pred_rf))

        # Return the trained classifier
        return rf_classifier

    def detect_fraud(self, classifier, deviation_percentage):
        avg_mining_time, avg_transaction_time = self.calculate_averages()

        # Generate a sample to predict
        sample_data = pd.DataFrame({'Mining Time': [avg_mining_time], 'Total Transaction Time': [avg_transaction_time]})

        # Predict the label using the trained Random Forest classifier
        predicted_label = classifier.predict(sample_data)[0]

        # Print the result
        print("\nFraud Detection Result:")
        if predicted_label == 1:
            print("The transaction is predicted as FRAUDULENT.")
        else:
            print("The transaction is predicted as NON-FRAUDULENT.")

        mining_time_threshold, transaction_time_threshold = self.calculate_thresholds(deviation_percentage)
        print(f"\nThresholds (+- {deviation_percentage}%):")
        print(f"Mining Time: {mining_time_threshold[0]:.4f} to {mining_time_threshold[1]:.4f} seconds")
        print(f"Transaction Time: {transaction_time_threshold[0]:.4f} to {transaction_time_threshold[1]:.4f} seconds")

    def calculate_averages(self):
        avg_mining_time = self.data["Mining Time"].mean()
        avg_transaction_time = self.data["Total Transaction Time"].mean()
        return avg_mining_time, avg_transaction_time

    def calculate_thresholds(self, deviation_percentage):
        avg_mining_time, avg_transaction_time = self.calculate_averages()

        mining_time_threshold = (
            avg_mining_time * (1 - deviation_percentage / 100),
            avg_mining_time * (1 + deviation_percentage / 100)
        )

        transaction_time_threshold = (
            avg_transaction_time * (1 - deviation_percentage / 100),
            avg_transaction_time * (1 + deviation_percentage / 100)
        )

        return mining_time_threshold, transaction_time_threshold

# Example usage:
if __name__ == "__main__":
    ai = FraudDetectionAI("transaction_details.csv")

    # Train Random Forest classifier
    rf_classifier = ai.train_random_forest()

    deviation_percentage = 10  # Adjust the deviation percentage as needed

    # Detect fraud using the trained Random Forest classifier
    ai.detect_fraud(rf_classifier, deviation_percentage)
