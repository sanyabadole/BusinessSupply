#! /usr/bin/env python3

## fire_employee

import tkinter as tk
from tkinter import messagebox, ttk

def fire_employee(cursor, connector, username, id):
    if not all([username, id]):
        raise ValueError("Input Error", "All fields must be filled out.")
    
    cursor.execute("SELECT COUNT(*) FROM work_for WHERE username = %s AND id = %s", (username, id))
    if cursor.fetchone()[0] == 0:
        raise ValueError("Employee does not work for this service.")
    
    cursor.execute("SELECT COUNT(*) FROM delivery_services WHERE id = %s", (id,))
    if cursor.fetchone()[0] == 0:
        raise ValueError("Delivery Service does not exist.")
    
    cursor.execute("SELECT COUNT(*) FROM delivery_services WHERE manager = %s", (username,))
    if cursor.fetchone()[0] > 0:
        raise ValueError("Employee is a manager for this service.")
    
    cursor.execute("SELECT COUNT(*) FROM work_for WHERE id = %s", (id,))
    if cursor.fetchone()[0] <= 1:
        raise ValueError("At least one employee must work for this service.")
    
    cursor.callproc('fire_employee', (username, id))
    connector.commit()
    return "Employee fired successfully!"