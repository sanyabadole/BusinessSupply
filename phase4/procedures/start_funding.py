#! /usr/bin/env python3

import tkinter as tk
from tkinter import messagebox

def start_funding(cursor, connection, owner, amount, long_name, fund_date):
    if not all([owner, amount, long_name, fund_date]):
        raise ValueError("Input Error", "All fields must be filled out.")
    
    cursor.execute("SELECT COUNT(*) FROM business_owners WHERE username = %s", (owner,))
    if cursor.fetchone()[0] == 0:
        raise ValueError("Owner does not exist.")
    
    cursor.execute("SELECT COUNT(*) FROM businesses WHERE long_name = %s", (long_name,))
    if cursor.fetchone()[0] == 0:
        raise ValueError("Business does not exist.")
    
    cursor.callproc('start_funding', (owner, amount, long_name, fund_date))
    connection.commit()
    return "Funding started successfully!"