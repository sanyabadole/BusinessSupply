#! /usr/bin/env python3

## Manage service

import tkinter as tk
from tkinter import messagebox, ttk

def manage_service(cursor, connector, username, service_id):
    if not all([username, service_id]):
        raise ValueError("Input Error", "All fields must be filled out.")
    
    cursor.execute("SELECT COUNT(*) FROM workers WHERE username = %s", (username,))
    if cursor.fetchone()[0] == 0:
        raise ValueError("Worker does not exist.")
    
    cursor.execute("SELECT COUNT(*) FROM work_for WHERE username = %s AND id = %s", (username, service_id))
    if cursor.fetchone()[0] == 0:
        raise ValueError("Worker does not work for this service.")
    
    cursor.execute("SELECT COUNT(*) FROM drivers WHERE username = %s", (username,))
    if cursor.fetchone()[0] > 0:
        raise ValueError("Drivers cannot manage services.")
    
    cursor.execute("SELECT COUNT(*) FROM delivery_services WHERE id = %s", (service_id,))
    if cursor.fetchone()[0] == 0:
        raise ValueError("Service does not exist.")
    
    cursor.execute("SELECT COUNT(*) FROM work_for WHERE username = %s AND id != %s", (username, service_id))
    if cursor.fetchone()[0] > 0:
        raise ValueError("Worker works for another service.")
    
    cursor.callproc('fire_employee', (username, service_id))
    connector.commit()
    return "Service managed successfully!"