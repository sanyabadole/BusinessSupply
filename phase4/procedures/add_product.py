import tkinter as tk
from tkinter import messagebox

def add_product(cursor, connection, barcode, name, weight):
    if not all([barcode, name, weight]):
        raise ValueError("Input Error", "All fields must be filled out.")

    # Check if barcode is unique
    cursor.execute("SELECT COUNT(*) FROM employees WHERE username = %s", (barcode,))
    if cursor.fetchone()[0] > 0:
        raise ValueError("Input Error", "Product already exists.")
    
    cursor.callproc('add_product', (barcode, name, weight))
    connection.commit()
    return "Product added successfully!"
    
    # try:
    #     weight = int(weight)
    #     if weight <= 0:
    #         raise ValueError("Weight must be a positive integer.")
    # except ValueError as e:
    #     raise ValueError("Input Error", str(e))