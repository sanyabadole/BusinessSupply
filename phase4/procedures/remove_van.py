#! /usr/bin/env python3

##remove_van
import tkinter as tk
from tkinter import messagebox

# -- [20] remove_van()
# -- -----------------------------------------------------------------------------
# /* This stored procedure removes a van from the system.  The removal can
# occur if, and only if, the van is not carrying any products.*/
# -- -----------------------------------------------------------------------------
# drop procedure if exists remove_van;
# delimiter //
# create procedure remove_van (in ip_id varchar(40), in ip_tag integer)
# sp_main: BEGIN
#     DECLARE van_exists INT DEFAULT 0;
#     DECLARE in_payload INT DEFAULT 0;

#     -- Ensure that the van exists
#     SELECT COUNT(*) INTO van_exists FROM vans WHERE id = ip_id AND tag = ip_tag;

#     -- Ensure that the van is not carrying any products
#     SELECT COUNT(*) INTO in_payload FROM contain WHERE id = ip_id AND tag = ip_tag;

#     -- Delete the van if it exists and is not carrying any products
#     IF van_exists = 1 AND in_payload = 0 THEN
#         DELETE FROM vans WHERE id = ip_id AND tag = ip_tag;
#     END IF;
# end //
# delimiter ;

def remove_van(cursor, connection, id, tag):
    if not all([id, tag]):
        return ValueError("Error", "All fields must be filled out.")
    
    cursor.execute("SELECT COUNT(*) FROM vans WHERE id = %s AND tag = %s", (id, tag))
    if cursor.fetchone()[0] == 0:
        return ValueError("Van does not exist.")
    
    cursor.execute("SELECT COUNT(*) FROM contain WHERE id = %s AND tag = %s", (id, tag))
    if cursor.fetchone()[0] > 0:
        return ValueError("Van is carrying one or more products.")
    
    cursor.callproc('remove_van', [id, tag])
    connection.commit()
    return "Van removed successfully."