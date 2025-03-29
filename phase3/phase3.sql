-- CS4400: Introduction to Database Systems (Fall 2024)
-- Project Phase III: Stored Procedures SHELL [v3] Thursday, Nov 7, 2024
set global transaction isolation level serializable;
set global SQL_MODE = 'ANSI,TRADITIONAL';
set names utf8mb4;
set SQL_SAFE_UPDATES = 0;

use business_supply;
-- -----------------------------------------------------------------------------
-- stored procedures and views
-- -----------------------------------------------------------------------------
/* Standard Procedure: If one or more of the necessary conditions for a procedure to
be executed is false, then simply have the procedure halt execution without changing
the database state. Do NOT display any error messages, etc. */

-- [1] add_owner()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new owner.  A new owner must have a unique
username. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_owner;
delimiter //
create procedure add_owner (in ip_username varchar(40), in ip_first_name varchar(100),
	in ip_last_name varchar(100), in ip_address varchar(500), in ip_birthdate date)
sp_main: begin

    declare username_exists int;
    select count(*) into username_exists from users where username = ip_username;

    if username_exists > 0 then
        leave sp_main;
    end if;

    insert into users (username, first_name, last_name, address, birthdate)
    values (ip_username, ip_first_name, ip_last_name, ip_address, ip_birthdate);

    insert into business_owners (username)
    values (ip_username);
    
end //
delimiter ;

-- [2] add_employee()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new employee without any designated driver or
worker roles.  A new employee must have a unique username and a unique tax identifier. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_employee;
delimiter //
create procedure add_employee (in ip_username varchar(40), in ip_first_name varchar(100),
	in ip_last_name varchar(100), in ip_address varchar(500), in ip_birthdate date,
    in ip_taxID varchar(40), in ip_hired date, in ip_employee_experience integer,
    in ip_salary integer)
sp_main: begin

	declare username_exists int;
    declare taxID_exists int;

    select count(*) into username_exists from users where username = ip_username;
    select count(*) into taxID_exists from employees where taxID = ip_taxID;

    if username_exists > 0 or taxID_exists > 0 then
        leave sp_main;
    end if;

    insert into users (username, first_name, last_name, address, birthdate)
    values (ip_username, ip_first_name, ip_last_name, ip_address, ip_birthdate);

    insert into employees (username, taxID, hired, experience, salary)
    values (ip_username, ip_taxID, ip_hired, ip_employee_experience, ip_salary);
    
end //
delimiter ;

-- [3] add_driver_role()
-- -----------------------------------------------------------------------------
/* This stored procedure adds the driver role to an existing employee.  The
employee/new driver must have a unique license identifier. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_driver_role;
delimiter //
create procedure add_driver_role (in ip_username varchar(40), in ip_licenseID varchar(40),
	in ip_license_type varchar(40), in ip_driver_experience integer)
sp_main: begin

	declare employee_exists int;
    declare is_worker int;
    declare license_exists int;

    select count(*) into employee_exists from employees where username = ip_username;
    select count(*) into is_worker from workers where username = ip_username;
    select count(*) into license_exists from drivers where licenseID = ip_licenseID;
    
	if ip_username is NULL or ip_license is NULL or ip_license_type is NULL or ip_driver_experience is NULL then
		leave sp_main;
	end if;
    if employee_exists = 0 or is_worker > 0 or license_exists > 0 then
        leave sp_main;
    end if;

    insert into drivers (username, licenseID, license_type, successful_trips)
    values (ip_username, ip_licenseID, ip_license_type, ip_driver_experience);
    
end //
delimiter ;

-- [4] add_worker_role()
-- -----------------------------------------------------------------------------
/* This stored procedure adds the worker role to an existing employee. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_worker_role;
delimiter //
create procedure add_worker_role (in ip_username varchar(40))
sp_main: begin

    declare employee_exists int;
    declare is_driver int;
    declare already_worker int;

    select count(*) into employee_exists from employees where username = ip_username;
    select count(*) into is_driver from drivers where username = ip_username;
    select count(*) into already_worker from workers where username = ip_username;

	if ip_username is null then leave sp_main;
    end if;
    if employee_exists = 0 or is_driver > 0 or already_worker > 0 then
        leave sp_main;
    end if;

    insert into workers (username)
    values (ip_username);
    
end //
delimiter ;

-- [5] add_product()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new product.  A new product must have a
unique barcode. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_product;
delimiter //
create procedure add_product (in ip_barcode varchar(40), in ip_name varchar(100),
	in ip_weight integer)
sp_main: begin

    declare product_exists int;

    select count(*) into product_exists from products where barcode = ip_barcode;

    if product_exists > 0 then
        leave sp_main;
    end if;

    insert into products (barcode, iname, weight)
    values (ip_barcode, ip_name, ip_weight);
    
end //
delimiter ;


-- [6] add_van()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new van.  A new van must be assigned 
to a valid delivery service and must have a unique tag.  Also, it must be driven
by a valid driver initially (i.e., driver works for the same service). And the van's starting
location will always be the delivery service's home base by default. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_van;
delimiter //
create procedure add_van (in ip_id varchar(40), in ip_tag integer, in ip_fuel int,
	in ip_capacity int, in ip_sales integer, in ip_driven_by varchar(40))
sp_main: begin
    declare home_base_location varchar(40);
    if exists (select * from vans where id = ip_id and tag = ip_tag) then
        leave sp_main;
    end if;
    if not exists (select * from delivery_services where id = ip_id) then
        leave sp_main;
    end if;
    if not exists (select d.username, v.id from drivers d
					join vans v on d.username = v.driven_by
					where d.username = ip_driven_by and v.id = ip_id
					group by d.username) then
        leave sp_main;
    end if;
    select home_base into home_base_location
    from delivery_services
    where id = ip_id;
    insert into vans (id, tag, fuel, capacity, sales, driven_by, located_at)
    values (ip_id, ip_tag, ip_fuel, ip_capacity, ip_sales, ip_driven_by, home_base_location);
end //
delimiter ;

-- [7] add_business()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new business.  A new business must have a
unique (long) name and must exist at a valid location, and have a valid rating.
And a resturant is initially "independent" (i.e., no owner), but will be assigned
an owner later for funding purposes. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_business;
delimiter //
create procedure add_business (in ip_long_name varchar(40), in ip_rating int,
	in ip_spent integer, in ip_location varchar(40))
sp_main: begin
    DECLARE business_exists INT;
    DECLARE location_valid INT;
    
    SELECT COUNT(*) INTO business_exists
    FROM businesses
    WHERE long_name = ip_long_name;
    
    SELECT COUNT(*) INTO location_valid
    FROM locations
    WHERE label = ip_location;
    
    IF business_exists > 0 OR location_valid = 0 OR ip_rating < 1 OR ip_rating > 5 THEN
        LEAVE sp_main;
    END IF;
    
    INSERT INTO businesses (long_name, rating, spent, location)
    VALUES (ip_long_name, ip_rating, ip_spent, ip_location);
end //
delimiter ;

-- [8] add_service()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new delivery service.  A new service must have
a unique identifier, along with a valid home base and manager. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_service;
delimiter //
create procedure add_service (in ip_id varchar(40), in ip_long_name varchar(100),
	in ip_home_base varchar(40), in ip_manager varchar(40))
sp_main: begin
    DECLARE service_exists INT;
    DECLARE location_valid INT;
    DECLARE manager_valid INT;
    declare location_not_used int;
    declare already_manager int;
    declare already_working_for int;
    
    SELECT COUNT(*) INTO service_exists
    FROM delivery_services
    WHERE id = ip_id;
    
    SELECT COUNT(*) INTO location_valid
    FROM locations
    WHERE label = ip_home_base;
    
    SELECT COUNT(*) INTO manager_valid
    FROM workers
    WHERE username = ip_manager;
    
    select count(*) into already_manager
    from delivery_services
    where manager = ip_manager;
    
    select count(*) into already_working_for
    from work_for
    where username = ip_manager;
    
    select count(*) into location_not_used
    from delivery_services
    where home_base = ip_home_base;
    
    IF service_exists > 0 OR location_valid = 0 OR manager_valid = 0 or location_not_used > 0 or already_manager > 0 or already_working_for > 0 THEN
        LEAVE sp_main;
    END IF;
    
    INSERT INTO delivery_services (id, long_name, home_base, manager)
    VALUES (ip_id, ip_long_name, ip_home_base, ip_manager);
    insert into work_for (username, id)
    values (ip_manager, ip_id);
    
end //
delimiter ;

-- [9] add_location()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new location that becomes a new valid van
destination.  A new location must have a unique combination of coordinates. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_location;
delimiter //
create procedure add_location (in ip_label varchar(40), in ip_x_coord int,
	in ip_y_coord int, in ip_space int)
sp_main: begin
    DECLARE location_exists INT;
    DECLARE coord_exists INT;
    
    SELECT COUNT(*) INTO location_exists
    FROM locations
    WHERE label = ip_label;
    
    SELECT COUNT(*) INTO coord_exists
    FROM locations
    WHERE x_coord = ip_x_coord AND y_coord = ip_y_coord;
    
    IF location_exists > 0 OR coord_exists > 0 THEN
        LEAVE sp_main;
    END IF;
    
    INSERT INTO locations (label, x_coord, y_coord, space)
    VALUES (ip_label, ip_x_coord, ip_y_coord, ip_space);
end //
delimiter ;

-- [10] start_funding()
-- -----------------------------------------------------------------------------
/* This stored procedure opens a channel for a business owner to provide funds
to a business. The owner and business must be valid. */
-- -----------------------------------------------------------------------------
drop procedure if exists start_funding;
delimiter //
create procedure start_funding (in ip_owner varchar(40), in ip_amount int, in ip_long_name varchar(40), in ip_fund_date date)
sp_main: begin
    if not exists (select * from business_owners where username = ip_owner) then
        leave sp_main;
    end if;
    if not exists (select * from businesses where long_name = ip_long_name) then
        leave sp_main;
    end if;
    if exists (select * from fund where username = ip_owner and business = ip_long_name) then
        update fund
        set invested = ip_amount,
            invested_date = ip_fund_date
        where username = ip_owner and business = ip_long_name;
    else
        insert into fund (username, invested, invested_date, business)
        values (ip_owner, ip_amount, ip_fund_date, ip_long_name);
    end if;
end //
delimiter ;

-- [11] hire_employee()
-- -----------------------------------------------------------------------------
/* This stored procedure hires a worker to work for a delivery service.
If a worker is actively serving as manager for a different service, then they are
not eligible to be hired.  Otherwise, the hiring is permitted. */
-- -----------------------------------------------------------------------------
drop procedure if exists hire_employee;
delimiter //
create procedure hire_employee (in ip_username varchar(40), in ip_id varchar(40))
sp_main: begin
    DECLARE employee_exists INT;
    DECLARE service_exists INT;
    DECLARE already_hired INT;
    DECLARE is_manager INT;


	if ip_username is null or ip_id is null then
    leave sp_main;
    end if;
    
    SELECT COUNT(*) INTO employee_exists
    FROM employees
    WHERE username = ip_username;

    SELECT COUNT(*) INTO service_exists
    FROM delivery_services
    WHERE id = ip_id;

    SELECT COUNT(*) INTO already_hired
    FROM work_for
    WHERE username = ip_username;

    SELECT COUNT(*) INTO is_manager
    FROM delivery_services
    WHERE manager = ip_username AND id != ip_id;

    IF employee_exists = 0 OR service_exists = 0 OR is_manager > 0 THEN
        LEAVE sp_main;
    END IF;
    
    if already_hired > 0 then
        update work_for
        set id = ip_id where username = ip_username;
    else
		INSERT INTO work_for (username, id)
		VALUES (ip_username, ip_id);
    end if;
end //

delimiter ;

-- [12] fire_employee()
-- -----------------------------------------------------------------------------
/* This stored procedure fires a worker who is currently working for a delivery
service.  The only restriction is that the employee must not be serving as a manager 
for the service. Otherwise, the firing is permitted. */
-- -----------------------------------------------------------------------------
drop procedure if exists fire_employee;
delimiter //
create procedure fire_employee (in ip_username varchar(40), in ip_id varchar(40))
sp_main: begin
	declare last_worker int;

	if ip_username is null or ip_id is null then leave sp_main; end if;
    if not exists (select * from work_for where username = ip_username and id = ip_id) then
        leave sp_main;
    end if;

    select count(*) into last_worker
    from work_for
    where id = ip_id;
    
    if last_worker = 1 then
		leave sp_main;
	end if;

    if exists (select * from delivery_services where manager = ip_username) then
        leave sp_main;
    end if;

    delete from work_for where username = ip_username and id = ip_id;
    # update vans set driven_by = NULL where driven_by = ip_username and id = ip_id;

end //
delimiter ;

-- [13] manage_service()
-- -----------------------------------------------------------------------------
/* This stored procedure appoints a worker who is currently hired by a delivery
service as the new manager for that service.  The only restrictions is that
the worker must not be working for any other delivery service. Otherwise, the appointment 
to manager is permitted.  The current manager is simply replaced. */
-- -----------------------------------------------------------------------------
drop procedure if exists manage_service;
delimiter //
create procedure manage_service (in ip_username varchar(40), in ip_id varchar(40))
sp_main: begin
    DECLARE must_work_for INT;
    DECLARE other_services INT;

	if ip_username is null or ip_id is null then leave sp_main; end if;
    SELECT COUNT(*) INTO must_work_for
    FROM work_for
    WHERE username = ip_username AND id = ip_id;

    SELECT COUNT(*) INTO other_services
    FROM work_for
    WHERE username = ip_username AND id != ip_id;

    IF must_work_for = 0 OR other_services > 0 THEN
        LEAVE sp_main;
    END IF;

    UPDATE delivery_services
    SET manager = ip_username
    WHERE id = ip_id;
end //
delimiter ;

-- [14] takeover_van()
-- -----------------------------------------------------------------------------
/* This stored procedure allows a valid driver to take control of a van owned by 
the same delivery service. The current controller of the van is simply relieved 
of those duties. */
-- -----------------------------------------------------------------------------
drop procedure if exists takeover_van;
delimiter //
create procedure takeover_van (in ip_username varchar(40), in ip_id varchar(40),
	in ip_tag integer)
sp_main: begin

	if ip_username is null or ip_id is null or ip_tag is null then leave sp_main; end if;
    if not exists (select * from drivers where username = ip_username) then
        leave sp_main;
    end if;

    if exists (select * from work_for where username = ip_username and id != ip_id) then
        leave sp_main;
    end if;

    if not exists (select * from vans where id = ip_id and tag = ip_tag) then
        leave sp_main;
    end if;

    update vans
    set driven_by = ip_username
    where id = ip_id and tag = ip_tag;

end //
delimiter ;

-- [15] load_van()
-- -----------------------------------------------------------------------------
/* This stored procedure allows us to add some quantity of fixed-size packages of
a specific product to a van's payload so that we can sell them for some
specific price to other businesses.  The van can only be loaded if it's located
at its delivery service's home base, and the van must have enough capacity to
carry the increased number of items.

The change/delta quantity value must be positive, and must be added to the quantity
of the product already loaded onto the van as applicable.  And if the product
already exists on the van, then the existing price must not be changed. */
-- -----------------------------------------------------------------------------
drop procedure if exists load_van;
delimiter //
create procedure load_van (in ip_id varchar(40), in ip_tag integer, in ip_barcode varchar(40),
	in ip_more_packages integer, in ip_price integer)
sp_main: begin
    declare van_capacity integer;
    declare current_load integer;
    declare product_weight integer;
    declare home_base varchar(40);
    declare van_location varchar(40);

    select home_base into home_base from delivery_services where id = ip_id;
    select located_at into van_location from vans where id = ip_id and tag = ip_tag;

    if van_location != home_base then
        leave sp_main;
    end if;

    if ip_more_packages <= 0 then
        leave sp_main;
    end if;

    select capacity into van_capacity from vans where id = ip_id and tag = ip_tag;
    
    if ip_more_packages > van_capacity then
		leave sp_main;
	end if;

    if exists (select * from contain where id = ip_id and tag = ip_tag and barcode = ip_barcode) then
        update contain
        set quantity = quantity + ip_more_packages
        where id = ip_id and tag = ip_tag and barcode = ip_barcode;
    else
        insert into contain (id, tag, barcode, quantity, price)
        values (ip_id, ip_tag, ip_barcode, ip_more_packages, ip_price);
    end if;

end //
delimiter ;

-- [16] refuel_van()
-- -----------------------------------------------------------------------------
/* This stored procedure allows us to add more fuel to a van. The van can only
be refueled if it's located at the delivery service's home base. */
-- -----------------------------------------------------------------------------
drop procedure if exists refuel_van;
delimiter //
create procedure refuel_van (in ip_id varchar(40), in ip_tag integer, in ip_more_fuel integer)
sp_main: begin
    DECLARE van_exists INT;
    DECLARE van_location VARCHAR(40);
    DECLARE home_base VARCHAR(40);

    SELECT COUNT(*) INTO van_exists
    FROM vans
    WHERE id = ip_id AND tag = ip_tag;

    IF van_exists = 0 THEN
        LEAVE sp_main;
    END IF;

    SELECT v.located_at, ds.home_base 
    INTO van_location, home_base
    FROM vans v
    JOIN delivery_services ds ON v.id = ds.id
    WHERE v.id = ip_id AND v.tag = ip_tag;

    IF van_location != home_base THEN
        LEAVE sp_main;
    END IF;

    UPDATE vans
    SET fuel = fuel + ip_more_fuel
    WHERE id = ip_id AND tag = ip_tag;
end //
delimiter ;


-- [17] drive_van()
-- -----------------------------------------------------------------------------
/* This stored procedure allows us to move a single van to a new
location (i.e., destination). This will also update the respective driver's 
experience and van's fuel. The main constraints on the van(s) being able to 
move to a new  location are fuel and space.  A van can only move to a destination
if it has enough fuel to reach the destination and still move from the destination
back to home base.  And a van can only move to a destination if there's enough
space remaining at the destination. */
-- -----------------------------------------------------------------------------
drop function if exists fuel_required;
delimiter //
create function fuel_required (ip_departure varchar(40), ip_arrival varchar(40))
	returns integer reads sql data
begin
	if (ip_departure = ip_arrival) then return 0;
    else return (select 1 + truncate(sqrt(power(arrival.x_coord - departure.x_coord, 2) + power(arrival.y_coord - departure.y_coord, 2)), 0) as fuel
		from (select x_coord, y_coord from locations where label = ip_departure) as departure,
        (select x_coord, y_coord from locations where label = ip_arrival) as arrival);
	end if;
end //
delimiter ;


-- [drive_van]
drop procedure if exists drive_van;
delimiter //
create procedure drive_van (in ip_id varchar(40), in ip_tag int, in ip_destination varchar(40))
sp_main: begin
    declare current_location varchar(40);
    declare home_base varchar(40);
    declare van_fuel int;
    declare fuel_to_destination int;
    declare fuel_to_home int;
    declare destination_space int;
    declare driver_username varchar(40);

    if not exists (select * from locations where label = ip_destination) then
        leave sp_main;
    end if;
    
    select located_at, fuel, driven_by into current_location, van_fuel, driver_username
    from vans
    where id = ip_id and tag = ip_tag;
    
    if current_location = ip_destination then
        leave sp_main;
    end if;
    
    select home_base into home_base
    from delivery_services
    where id = ip_id;
    set fuel_to_destination = fuel_required(current_location, ip_destination);
    set fuel_to_home = fuel_required(ip_destination, home_base);
    if van_fuel < (fuel_to_destination + fuel_to_home) then
        leave sp_main;
    end if;
    select space into destination_space
    from locations
    where label = ip_destination;
    if destination_space <= 0 then
        leave sp_main;
    end if;
    update vans
    set located_at = ip_destination,
        fuel = fuel - fuel_to_destination
    where id = ip_id and tag = ip_tag;
    if driver_username is not null then
        update drivers
        set successful_trips = successful_trips + 1
        where username = driver_username;
    end if;
end //
delimiter ;

-- [18] purchase_product()
-- -----------------------------------------------------------------------------
/* This stored procedure allows a business to purchase products from a van
at its current location.  The van must have the desired quantity of the product
being purchased.  And the business must have enough money to purchase the
products.  If the transaction is otherwise valid, then the van and business
information must be changed appropriately.  Finally, we need to ensure that all
quantities in the payload table (post transaction) are greater than zero. */
-- -----------------------------------------------------------------------------
drop procedure if exists purchase_product;
delimiter //
create procedure purchase_product (in ip_long_name varchar(40), in ip_id varchar(40),
	in ip_tag int, in ip_barcode varchar(40), in ip_quantity int)
sp_main: begin
    declare business_location varchar(40);
    declare van_location varchar(40);
    declare product_price int;
    declare product_quantity int;
    declare total_cost int;
    declare business_spent int;

    select location, spent into business_location, business_spent
    from businesses
    where long_name = ip_long_name;
    if business_location is null then
        leave sp_main;
    end if;

    select located_at into van_location
    from vans
    where id = ip_id and tag = ip_tag;
    
    if van_location is null or van_location != business_location then
        leave sp_main;
    end if;

    select price, quantity into product_price, product_quantity
    from contain
    where id = ip_id and tag = ip_tag and barcode = ip_barcode;
    
    if product_quantity is null or product_quantity < ip_quantity then
        leave sp_main;
    end if;

    set total_cost = product_price * ip_quantity;

    if business_spent + total_cost > (select rating * 100 from businesses where long_name = ip_long_name) then
        leave sp_main;
    end if;

    update contain
    set quantity = quantity - ip_quantity
    where id = ip_id and tag = ip_tag and barcode = ip_barcode;

    update vans
    set sales = sales + total_cost
    where id = ip_id and tag = ip_tag;

    update businesses
    set spent = spent + total_cost
    where long_name = ip_long_name;

    delete from contain
    where id = ip_id and tag = ip_tag and quantity <= 0;
end //
delimiter ;

-- [19] remove_product()
-- -----------------------------------------------------------------------------
/* This stored procedure removes a product from the system.  The removal can
occur if, and only if, the product is not being carried by any vans. */
-- -----------------------------------------------------------------------------
drop procedure if exists remove_product;
delimiter //
create procedure remove_product (in ip_barcode varchar(40))
sp_main: begin
    declare product_exists int;
    declare vans_carrying int;

	if ip_barcode is null then leave sp_main; end if;

    select count(*) into product_exists
    from products
    where barcode = ip_barcode;

    if product_exists > 0 then
        select count(*) into vans_carrying
        from contain
        where barcode = ip_barcode;

        if vans_carrying = 0 then
            delete from products
            where barcode = ip_barcode;
        end if;
    end if;
end //
delimiter ;

-- [20] remove_van()
-- -----------------------------------------------------------------------------
/* This stored procedure removes a van from the system.  The removal can
occur if, and only if, the van is not carrying any products.*/
-- -----------------------------------------------------------------------------
drop procedure if exists remove_van;
delimiter //
create procedure remove_van (in ip_id varchar(40), in ip_tag int)
sp_main: begin
    declare van_exists int;
    declare products_count int;

	if ip_if is null or ip_tag is null then leave sp_main; end if;
    
    select count(*) into van_exists
    from vans
    where id = ip_id and tag = ip_tag;

    if van_exists > 0 then
        select count(*) into products_count
        from contain
        where id = ip_id and tag = ip_tag;

        if products_count = 0 then
            delete from vans
            where id = ip_id and tag = ip_tag;
        end if;
    END IF;
end //
delimiter ;

-- [21] remove_driver_role()
-- -----------------------------------------------------------------------------
/* This stored procedure removes a driver from the system.  The removal can
occur if, and only if, the driver is not controlling any vans.  
The driver's information must be completely removed from the system. */
-- -----------------------------------------------------------------------------
drop procedure if exists remove_driver_role;
delimiter //
create procedure remove_driver_role (in ip_username varchar(40))
sp_main: begin
    declare driver_count int;
    declare van_count int;

	if ip_username is null then leave sp_main; end if;

    select count(*) into driver_count
    from drivers
    where username = ip_username;

    if driver_count = 0 then
        leave sp_main;
    end if;

    select count(*) into van_count
    from vans
    where driven_by = ip_username;

    if van_count > 0 then
        leave sp_main;
    end if;

    delete from drivers where username = ip_username;
    delete from employees where username = ip_username;
    delete from work_for where username = ip_username;
    delete from users where username = ip_username;
end //
delimiter ;

-- [22] display_owner_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of an owner.
For each owner, it includes the owner's information, along with the number of
businesses for which they provide funds and the number of different places where
those businesses are located.  It also includes the highest and lowest ratings
for each of those businesses, as well as the total amount of debt based on the
monies spent purchasing products by all of those businesses. And if an owner
doesn't fund any businesses then display zeros for the highs, lows and debt. */
-- -----------------------------------------------------------------------------
create or replace view display_owner_view as
select b.username, u.first_name, u.last_name, u.address, count(f.invested) as num_businesses,
count(distinct(bus.location)) as num_places, coalesce(max(bus.rating), 0) as highs, coalesce(min(bus.rating), 0) as lows, 
coalesce(sum(bus.spent), 0) as debt
from business_owners b
left join fund f on b.username = f.username
join users u on b.username = u.username
left join businesses bus on f.business = bus.long_name
group by b.username;

-- [23] display_employee_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of an employee.
For each employee, it includes the username, tax identifier, salary, hiring date and
experience level, along with license identifer and driving experience (if applicable,
'n/a' if not), and a 'yes' or 'no' depending on the manager status of the employee. */
-- -----------------------------------------------------------------------------
create or replace view display_employee_view as
select e.username, taxID, salary, hired, experience AS employee_experience, 
    case
        when licenseID is null then 'N/A' 
        else licenseID 
    end as licenseID,
    case
        when successful_trips is null then 'N/A' 
        else successful_trips 
    end as driving_experience,
    case
        when e.username in (select manager from delivery_services) then 'Yes'
        else 'No'
    end as manager_status
from employees e left join drivers d on e.username = d.username;

-- [24] display_driver_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of a driver.
For each driver, it includes the username, licenseID and drivering experience, along
with the number of vans that they are controlling. */
-- -----------------------------------------------------------------------------
create or replace view display_driver_view as
select username, licenseID, successful_trips, count(distinct concat(id, '-', tag)) as num_vans
from drivers d left join vans v on d.username=v.driven_by
group by username;

-- [25] display_location_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of a location.
For each location, it includes the label, x- and y- coordinates, along with the
name of the business or service at that location, the number of vans as well as 
the identifiers of the vans at the location (sorted by the tag), and both the 
total and remaining capacity at the location. */
-- -----------------------------------------------------------------------------
create or replace view display_location_view as
select locations.label, 
    case
        when businesses.long_name is null then delivery_services.long_name
        else businesses.long_name
    end as long_name,
    x_coord, y_coord, space, 
    count(distinct concat(vans.id, vans.tag)) as num_vans,
    GROUP_CONCAT(concat(vans.id, vans.tag) order by vans.tag separator ',') as van_ids,
    space-count(distinct (concat(vans.id, vans.tag))) as remaining_capacity
from locations left join delivery_services on locations.label = delivery_services.home_base
left join businesses on locations.label = businesses.location
join vans on locations.label = vans.located_at
group by locations.label, x_coord, y_coord, space, 
         case
             when businesses.long_name is null then delivery_services.long_name
             else businesses.long_name
         end;

-- [26] display_product_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of the products.
For each product that is being carried by at least one van, it includes a list of
the various locations where it can be purchased, along with the total number of packages
that can be purchased and the lowest and highest prices at which the product is being
sold at that location. */
-- -----------------------------------------------------------------------------
create or replace view display_product_view as
select p.iname as product_name, v.located_at as location, SUM(c.quantity) as amount_available, MIN(c.price) as min_price, MAX(c.price) as max_price
from products p join contain c on p.barcode = c.barcode
natural join vans v
group by p.iname, v.located_at
order by p.iname;

-- [27] display_service_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of a delivery
service.  It includes the identifier, name, home base location and manager for the
service, along with the total sales from the vans.  It must also include the number
of unique products along with the total cost and weight of those products being
carried by the vans. */
-- -----------------------------------------------------------------------------
create or replace view display_service_view as
select table1.id, table1.long_name, table1.home_base, table1.manager, table1.revenue, table2.products_carried, table2.cost_carried, table2.weight_carried from
(select d.id, d.long_name, d.home_base, d.manager, sum(v.sales) as revenue from delivery_services d
join vans v on d.id = v.id
group by d.id) table1
join 
(select c.id, count(distinct(c.barcode)) as products_carried, sum(c.quantity * c.price) as cost_carried, sum(c.quantity * p.weight) as weight_carried from contain c
join products p on c.barcode = p.barcode
group by c.id) table2
on table1.id = table2.id;
