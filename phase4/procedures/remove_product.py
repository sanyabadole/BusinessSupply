import tkinter as tk
from tkinter import messagebox

# -- [19] remove_product()
# -- -----------------------------------------------------------------------------
# /* This stored procedure removes a product from the system.  The removal can
# occur if, and only if, the product is not being carried by any vans. */
# -- -----------------------------------------------------------------------------
# drop procedure if exists remove_product;
# delimiter //
# create procedure remove_product (in ip_barcode varchar(40))
# sp_main: BEGIN
#     DECLARE product_exists INT DEFAULT 0;
#     DECLARE in_payload INT DEFAULT 0;

#     -- Ensure that the product exists
#     SELECT COUNT(*) INTO product_exists FROM products WHERE barcode = ip_barcode;

#     -- Ensure that the product is not being carried by any vans
#     SELECT COUNT(*) INTO in_payload FROM contain WHERE barcode = ip_barcode;

#     -- Delete the product if it exists and is not in any payloads
#     IF product_exists = 1 AND in_payload = 0 THEN
# 		DELETE FROM products WHERE barcode = ip_barcode;
#     END IF;
# end //
# delimiter ;

def remove_product(cursor, connection, barcode):
    if not barcode:
        return ValueError("Error", "Barcode must be filled out.")
    
    cursor.execute("SELECT COUNT(*) FROM products WHERE barcode = %s", (barcode,))
    if cursor.fetchone()[0] == 0:
        return ValueError("Product does not exist.")
    
    cursor.execute("SELECT COUNT(*) FROM contain WHERE barcode = %s", (barcode,))
    if cursor.fetchone()[0] > 0:
        return ValueError("Product is being carried by one or more vans.")
    
    cursor.callproc('remove_product', [barcode])
    connection.commit()
    return "Product removed successfully."