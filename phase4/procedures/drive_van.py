#! /usr/bin/env python3

## drive_van
import tkinter as tk
from tkinter import messagebox

def drive_van(cursor, connection, id, tag, destination):
    if not all([id, tag, destination]):
        raise ValueError("Error", "All fields must be filled out.")
    
    cursor.execute("SELECT count(*) FROM locations WHERE label = %s", (destination,))
    if not cursor.fetchone():
        return ValueError("Please enter a valid location.")
    
    cursor.execute("SELECT driven_by FROM vans WHERE id = %s AND tag = %s", (id, tag))
    if not cursor.fetchone()[0]:
        return ValueError("Van does not have a driver.")

    cursor.execute("SELECT located_at FROM vans WHERE id = %s AND tag = %s", (id, tag))
    current_location = str(cursor.fetchone()[0])
    if current_location == destination:
        return ValueError("Van is already at the destination.")
    
    cursor.callproc('drive_van', (id, tag, destination))
    connection.commit()
    return "Van drove to destination."
    
