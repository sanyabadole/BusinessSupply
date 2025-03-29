import tkinter as tk
from tkinter import messagebox

def add_driver_role(cursor, connection, username, licenseID, license_type, driver_experience):
    # Check if all fields are filled out
    if not all([username, licenseID, license_type, driver_experience]):
        messagebox.showerror("Input Error", "All fields must be filled out.")

    # Validate driver experience
    try:
        driver_experience = int(driver_experience)
        if driver_experience < 0:
            raise ValueError("Driver experience cannot be negative.")
    except ValueError as e:
        raise ValueError("Input Error", str(e))
    
    # Check if username exists in employees and not in workers
    cursor.execute("SELECT COUNT(*) FROM employees WHERE username = %s", (username,))
    if cursor.fetchone()[0] == 0:
        raise ValueError("Input Error", "User is not a valid employee")

    cursor.execute("SELECT COUNT(*) FROM workers WHERE username = %s", (username,))
    if cursor.fetchone()[0] > 0:
        raise ValueError("Input Error", "User is already a worker. Cannot be a worker and a driver.")

    # Check if licenseID is unique
    cursor.execute("SELECT COUNT(*) FROM drivers WHERE licenseID = %s", (licenseID,))
    if cursor.fetchone()[0] > 0:
        raise ValueError("Input Error", "License ID already exists.")

    # Call stored procedure
    cursor.callproc('add_driver_role', (username, licenseID, license_type, driver_experience))
    connection.commit()
    return "Driver role added successfully!"