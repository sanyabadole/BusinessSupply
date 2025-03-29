# -- [18] purchase_product()
# -- -----------------------------------------------------------------------------
# /* This stored procedure allows a business to purchase products from a van
# at its current location.  The van must have the desired quantity of the product
# being purchased.  And the business must have enough money to purchase the
# products.  If the transaction is otherwise valid, then the van and business
# information must be changed appropriately.  Finally, we need to ensure that all
# quantities in the payload table (post transaction) are greater than zero. */
# -- -----------------------------------------------------------------------------
# drop procedure if exists purchase_product;
# delimiter //
# create procedure purchase_product (in ip_long_name varchar(40), in ip_id varchar(40),
# 	in ip_tag integer, in ip_barcode varchar(40), in ip_quantity integer)
# sp_main: begin
# 	IF ip_quantity is NULL THEN LEAVE sp_main; END IF;
#     -- Ensure the business exists
#     IF ip_long_name NOT IN (SELECT long_name FROM businesses) THEN LEAVE sp_main; END IF;

#     -- Ensure the van exists (id, tag pair) in vans table
#     IF NOT EXISTS (SELECT 1 FROM vans WHERE id = ip_id AND tag = ip_tag) THEN LEAVE sp_main;END IF;

#     -- Ensure the van is at the same location as the business
#     IF (SELECT location FROM businesses WHERE long_name = ip_long_name) != (SELECT located_at FROM vans WHERE id = ip_id AND tag = ip_tag) THEN LEAVE sp_main; END IF;

#     -- Ensure there is enough product in the van and product exists 
# 	if ip_barcode not in (select barcode from contain where id=ip_id and tag=ip_tag) then leave sp_main; end if;
#     IF ip_quantity > (SELECT quantity FROM contain WHERE id = ip_id AND tag = ip_tag AND barcode = ip_barcode) THEN LEAVE sp_main; END IF;

#     -- Update the quantity in the 'contain' table (reduce the available quantity)
#     UPDATE contain SET quantity = (quantity - ip_quantity) WHERE id = ip_id AND tag = ip_tag AND barcode = ip_barcode;

#     -- Update the 'spent' value in the 'businesses' table (increment the spent value)
#     UPDATE businesses SET spent = spent + ip_quantity * (SELECT price FROM contain WHERE id = ip_id AND tag = ip_tag AND barcode = ip_barcode) WHERE long_name = ip_long_name;
  
# 	UPDATE vans SET sales = sales + ip_quantity * (SELECT price FROM contain WHERE id = ip_id AND tag = ip_tag AND barcode = ip_barcode) WHERE id = ip_id AND tag = ip_tag;

# 	-- Additional logic: Ensure no quantities are less than zero in the 'contain' table after update
#     IF (SELECT quantity FROM contain WHERE id = ip_id AND tag = ip_tag AND barcode = ip_barcode) = 0 THEN 
#     delete from contain where id = ip_id AND tag = ip_tag AND barcode = ip_barcode;
#     END IF;
# end //
# delimiter ;

import tkinter as tk
from tkinter import messagebox

def purchase_product(cursor, connection, long_name, id, tag, barcode, quantity):
    if not all([long_name, id, tag, barcode, quantity]):
        return ValueError("Error", "All fields must be filled out.")
    
    cursor.execute("SELECT COUNT(*) FROM businesses WHERE long_name = %s", (long_name,))
    if not cursor.fetchone()[0]:
        return ValueError("Business does not exist.")
    
    cursor.execute("SELECT COUNT(*) FROM vans WHERE id = %s AND tag = %s", (id, tag))
    if not cursor.fetchone()[0]:
        return ValueError("Van does not exist.")
    
    cursor.execute("SELECT located_at FROM vans WHERE id = %s AND tag = %s", (id, tag))
    if cursor.fetchone()[0] != long_name:
        return ValueError("Van is not at the same location as the business.")
    
    cursor.execute("SELECT COUNT(*) FROM contain WHERE id = %s AND tag = %s AND barcode = %s", (id, tag, barcode))
    if not cursor.fetchone()[0]:
        return ValueError("Product does not exist in the van.")
    
    cursor.execute("SELECT quantity FROM contain WHERE id = %s AND tag = %s AND barcode = %s", (id, tag, barcode))
    if cursor.fetchone()[0] < quantity:
        return ValueError("Van does not have enough of the product.")
    
    cursor.callproc('purchase_product', (long_name, id, tag, barcode, quantity))
    connection.commit()
    return "Product purchased successfully."