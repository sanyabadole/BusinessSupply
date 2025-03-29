import tkinter as tk
from tkinter import messagebox

def add_worker_role(cursor, connection, username):
    if not username:
        messagebox.showerror("Input Error", "Username must be filled out.")

    # Check if username exists in employees and not in drivers
    cursor.execute("SELECT COUNT(*) FROM employees WHERE username = %s", (username,))
    if cursor.fetchone()[0] == 0:
        raise ValueError("Input Error", "User is not a valid employee.")

    cursor.execute("SELECT COUNT(*) FROM drivers WHERE username = %s", (username,))
    if cursor.fetchone()[0] > 0:
        raise ValueError("Input Error", "User is already a driver. Cannot be both a driver and a worker.")

    # Call stored procedure
    cursor.callproc('add_worker_role', (username,))
    connection.commit()
    return "Worker role added successfully!"