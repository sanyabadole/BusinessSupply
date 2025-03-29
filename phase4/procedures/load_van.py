import tkinter as tk
from tkinter import messagebox, ttk

def load_van(cursor, connector, id, tag, barcode, more_packages, price):
    if not all([id, tag, barcode, more_packages, price]):
        raise ValueError("Input Error", "All fields must be filled out.")
    
    cursor.execute("SELECT COUNT(*) FROM vans WHERE id = %s AND tag = %s", (id, tag))
    if cursor.fetchone()[0] == 0:
        raise ValueError("Van does not exist.")
    
    cursor.execute("SELECT COUNT(*) FROM products WHERE barcode = %s", (barcode,))
    if cursor.fetchone()[0] == 0:
        raise ValueError("Product does not exist.")
    
    cursor.execute("SELECT located_at FROM vans WHERE id = %s AND tag = %s", (id, tag))
    located_at = str(cursor.fetchone()[0])
    cursor.execute("SELECT home_base FROM delivery_services WHERE id = (SELECT id FROM vans WHERE id = %s AND tag = %s)", (id, tag))
    home_base = str(cursor.fetchone()[0])
    if located_at != home_base:
        raise ValueError("Van is not located at its delivery service's home base.")
    
    
    cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM contain WHERE id = %s AND tag = %s", (id, tag))
    current = int(cursor.fetchone()[0])
    cursor.execute("SELECT capacity FROM vans WHERE id = %s AND tag = %s", (id, tag))
    capacity = int(cursor.fetchone()[0])
    if current + int(more_packages) > capacity:
        raise ValueError("Van does not have enough capacity to carry the new packages.")
    
    cursor.callproc('load_van', (id, tag, barcode, more_packages, price))
    connector.commit()
    return "Van loaded successfully!"