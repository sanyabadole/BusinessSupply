#! /usr/bin/env python3

## add_location

import tkinter as tk
from tkinter import messagebox

def add_location(cursor, connection, label, x_coord, y_coord, space):
    if not all([label, x_coord, y_coord, space]):
        raise ValueError("Input Error", "All fields must be filled out.")

    cursor.execute("SELECT COUNT(*) FROM locations WHERE label = %s", (label,))
    if cursor.fetchone()[0] > 0:
        raise ValueError("Input Error", "Location already exists.")
    
    cursor.execute("SELECT COUNT(*) FROM locations WHERE x_coord = %s AND y_coord = %s", (x_coord, y_coord))
    if cursor.fetchone()[0] > 0:
        raise ValueError("Input Error", "Location already exists.")
    
    cursor.callproc('add_location', (label, x_coord, y_coord, space))
    connection.commit()
    return "Location added successfully!"