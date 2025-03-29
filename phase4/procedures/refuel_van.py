#! /usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox

def refuel_van(cursor, connector, id, tag, more_fuel):
    if not all([id, tag, more_fuel]):
        raise ValueError("Input Error", "All fields must be filled out.")
    
    cursor.execute("SELECT COUNT(*) FROM vans WHERE id = %s AND tag = %s", (id, tag))
    if cursor.fetchone()[0] == 0:
        raise ValueError("Van does not exist.")
    
    cursor.execute("SELECT located_at FROM vans WHERE id = %s AND tag = %s", (id, tag))
    located_at = str(cursor.fetchone()[0])
    cursor.execute("SELECT home_base FROM delivery_services WHERE id = %s", (id,))
    home_base = str(cursor.fetchone()[0])
    if located_at != home_base:
        raise ValueError("Van is not located at its delivery service's home base.")
    
    cursor.callproc('refuel_van', (id, tag, more_fuel))
    connector.commit()
    return "Van refueled successfully!"