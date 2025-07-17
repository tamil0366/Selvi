import tkinter as tk
from tkinter import messagebox
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Define correct password
CORRECT_PASSWORD = "secure123"

# Track wrong attempts
attempts = 0
MAX_ATTEMPTS = 3

# Sample training data for fraud detection (features: amount, transaction_type, location_code)
# For simplicity, transaction_type and location_code are encoded as integers
X_train = np.array([
    [100, 0, 1],
    [2000, 1, 2],
    [50, 0, 1],
    [5000, 1, 3],
    [20, 0, 1],
    [3000, 1, 2],
    [10, 0, 1],
    [7000, 1, 3]
])
y_train = np.array([0, 1, 0, 1, 0, 1, 0, 1])  # 0 = legitimate, 1 = fraud

# Train a simple RandomForest model
model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X_train, y_train)

def predict_fraud(amount, transaction_type, location_code):
    features = np.array([[amount, transaction_type, location_code]])
    prediction = model.predict(features)
    return prediction[0]

# Function to check password
def check_password():
    global attempts
    entered_password = password_entry.get()
    
    if entered_password == CORRECT_PASSWORD:
        messagebox.showinfo("Access Granted", "Welcome! Transaction access granted.")
        attempts = 0  # Reset after success
        root.withdraw()  # Hide login window
        open_fraud_detection_window()
    else:
        attempts += 1
        messagebox.showwarning("Access Denied", f"Wrong password! Attempt {attempts} of {MAX_ATTEMPTS}.")
        
        if attempts >= MAX_ATTEMPTS:
            messagebox.showerror("ALERT 🚨", "Multiple failed attempts detected!\nThis attempt has been flagged as suspicious.")
            # Optionally: Log the event, send email alert, block access, etc.

def open_fraud_detection_window():
    fraud_window = tk.Toplevel()
    fraud_window.title("Fraud Detection")
    fraud_window.geometry("400x300")

    tk.Label(fraud_window, text="Enter Transaction Amount:").pack(pady=5)
    amount_entry = tk.Entry(fraud_window)
    amount_entry.pack()

    tk.Label(fraud_window, text="Transaction Type (0=debit, 1=credit):").pack(pady=5)
    type_entry = tk.Entry(fraud_window)
    type_entry.pack()

    tk.Label(fraud_window, text="Location Code (1, 2, or 3):").pack(pady=5)
    location_entry = tk.Entry(fraud_window)
    location_entry.pack()

    def on_predict():
        try:
            amount = float(amount_entry.get())
            transaction_type = int(type_entry.get())
            location_code = int(location_entry.get())
            if transaction_type not in [0, 1] or location_code not in [1, 2, 3]:
                messagebox.showerror("Input Error", "Transaction type must be 0 or 1, location code must be 1, 2, or 3.")
                return
            result = predict_fraud(amount, transaction_type, location_code)
            if result == 1:
                messagebox.showwarning("Fraud Detection Result", "Warning: This transaction is likely FRAUDULENT!")
            else:
                messagebox.showinfo("Fraud Detection Result", "This transaction appears LEGITIMATE.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")

    predict_btn = tk.Button(fraud_window, text="Check Fraud", command=on_predict)
    predict_btn.pack(pady=20)

# Create GUI for login
root = tk.Tk()
root.title("Fraud Protection - Secure Login")
root.geometry("300x180")

# GUI components for login
label = tk.Label(root, text="Enter your password:")
label.pack(pady=10)

password_entry = tk.Entry(root, show="*", width=25)
password_entry.pack()

submit_btn = tk.Button(root, text="Submit", command=check_password)
submit_btn.pack(pady=15)
root.mainloop()