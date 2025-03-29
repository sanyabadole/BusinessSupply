#! /usr/bin/env python3

import tkinter as tk
from tkinter import messagebox, ttk

def add_service(cursor, connector, id, long_name, home_base, manager):
    if not all([id, long_name, home_base, manager]):
        raise ValueError("Input Error", "All fields must be filled out.")
    
    cursor.execute("SELECT COUNT(*) FROM delivery_services WHERE id = %s", (id,))
    if cursor.fetchone()[0] > 0:
        raise ValueError("Service ID already exists.")
    
    cursor.execute("SELECT COUNT(*) FROM locations WHERE label = %s", (home_base,))
    if cursor.fetchone()[0] == 0:
        raise ValueError("Home base location does not exist.")
    
    cursor.execute("SELECT COUNT(*) FROM delivery_services WHERE home_base = %s", (home_base,))
    if cursor.fetchone()[0] > 0:
        raise ValueError("Home base location is already assigned to a service.")
    
    cursor.execute("SELECT COUNT(*) FROM workers WHERE username = %s", (manager,))
    if cursor.fetchone()[0] == 0:
        raise ValueError("Manager does not exist.")
    
    cursor.execute("SELECT COUNT(*) FROM work_for WHERE username = %s AND id = %s", (manager, id))
    if cursor.fetchone()[0] > 0:
        raise ValueError("Manager is already assigned to a service.")
    
    cursor.callproc('add_service', (id, long_name, home_base, manager))
    connector.commit()
    return "Service added successfully!"