#! /usr/bin/env python3

import tkinter as tk
from tkinter import messagebox

# -- [21] remove_driver_role()
# -- -----------------------------------------------------------------------------
# /* This stored procedure removes a driver from the system.  The removal can
# occur if, and only if, the driver is not controlling any vans.  
# The driver's information must be completely removed from the system. */
# -- -----------------------------------------------------------------------------
# drop procedure if exists remove_driver_role;
# delimiter //
# create procedure remove_driver_role (in ip_username varchar(40))
# sp_main: begin
# 	-- ensure that the driver exists
#     -- ensure that the driver is not controlling any vans
#     -- remove all remaining information
#     if ip_username not in (select username from drivers) then leave sp_main; end if;
#     if ip_username in (select driven_by from vans) then leave sp_main; end if;
#     delete from drivers where username like ip_username;
#     delete from users where username like ip_username;
# end //
# delimiter ;

def remove_driver_role(cursor, connection, username):
    if not username:
        return ValueError("Error", "Username must be filled out.")
    
    cursor.execute("SELECT COUNT(*) FROM drivers WHERE username = %s", (username,))
    if cursor.fetchone()[0] == 0:
        return ValueError("Driver does not exist.")
    
    cursor.execute("SELECT COUNT(*) FROM vans WHERE driven_by = %s", (username,))
    if cursor.fetchone()[0] > 0:
        return ValueError("Driver is controlling one or more vans.")
    
    cursor.callproc('remove_driver_role', [username])
    connection.commit()
    return "Driver removed successfully."