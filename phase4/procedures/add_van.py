#! /usr/bin/env python3

import tkinter as tk
from tkinter import messagebox, ttk

def add_van(cursor, connector, id, tag, fuel, capacity, sales, driven_by):
    if not all([id, tag, fuel, capacity, sales]):
        raise ValueError("Input Error", "ID, tag, fuel, capacity, and sales fields must be filled out.")

    cursor.execute("SELECT COUNT(*) FROM delivery_services WHERE id = %s", (id,))
    if cursor.fetchone()[0] == 0:
        raise ValueError("Delivery Service ID does not exist.")
    
    cursor.execute("SELECT COUNT(*) FROM vans WHERE id = %s AND tag = %s", (id, tag))
    if cursor.fetchone()[0] > 0:
        raise ValueError("Van already exists.")
    
    if str(driven_by).lower() != "null":
        cursor.execute("SELECT COUNT(*) FROM drivers WHERE username = %s", (driven_by,))
        if cursor.fetchone()[0] == 0:
            raise ValueError("Driver does not exist.")
        cursor.callproc('add_van', (id, tag, fuel, capacity, sales, driven_by))
    else:
        cursor.callproc('add_van', (id, tag, fuel, capacity, sales, None))

    connector.commit()
    return "Van added successfully!"