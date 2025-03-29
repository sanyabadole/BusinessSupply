#! /usr/bin/env python3

## takeover_van #####still have to finish

import tkinter as tk
from tkinter import messagebox, ttk

def takeover_van(cursor, connector, username, van_id, van_tag):
    if not all([username, van_id, van_tag]):
        raise ValueError("Input Error", "All fields must be filled out.")
    
    cursor.execute("SELECT COUNT(*) FROM drivers WHERE username = %s", (username,))
    if cursor.fetchone()[0] == 0:
        raise ValueError("Driver does not exist.")
    
    cursor.execute("SELECT COUNT(*) FROM vans WHERE id = %s AND tag = %s", (van_id, van_tag))
    if cursor.fetchone()[0] == 0:
        raise ValueError("Van does not exist.")
    
    cursor.execute("SELECT COUNT(*) FROM vans WHERE driven_by = %s AND id != %s", (username, van_id))
    if cursor.fetchone()[0] > 0:
        raise ValueError("Driver is already driving another van.")
    
    cursor.callproc('takeover_van', (username, van_id, van_tag))
    connector.commit()
    return "Van taken over successfully!"