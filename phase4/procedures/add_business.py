#! /usr/bin/env python3

import tkinter as tk
from tkinter import messagebox

def add_business(cursor, connection, long_name, rating, spent, location):

    if not all([long_name, rating, spent, location]):
        raise ValueError("Input Error", "All fields must be filled out.")

    cursor.execute("SELECT COUNT(*) FROM businesses WHERE long_name = %s", (long_name,))
    (business_exists,) = cursor.fetchone()
    if business_exists > 0:
        raise ValueError("Business name already exists. Please choose a different name.")

    cursor.execute("SELECT COUNT(*) FROM locations WHERE label = %s", (location,))
    (location_exists,) = cursor.fetchone()
    if location_exists == 0:
        raise ValueError("Location is not valid. Please choose an existing location.")
    
    cursor.execute("SELECT COUNT(*) FROM businesses WHERE location = %s", (location,))
    (location_used,) = cursor.fetchone()
    if location_used > 0:
        raise ValueError("Location already in use. Please choose a different location.")
    
    if int(rating) < 1 or int(rating) > 5:
        raise ValueError("Rating must be between 1 and 5.")

    # Call stored procedure if the long name is unique
    cursor.callproc('add_business', [long_name, rating, spent, location])
    connection.commit()
    return "Business added successfully!"