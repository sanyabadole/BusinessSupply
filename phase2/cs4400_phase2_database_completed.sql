-- CS4400: Introduction to Database Systems (Fall 2024)
-- Phase II: Create Table & Insert Statements [v0] Monday, September 15, 2024 @ 17:00 EST

-- Team __
-- Elizabeth Kalemera (ekalemera3)
-- Yashas Appaji (yappaji3)
-- Sanya Badole (sbadole6)
-- Jacob Smith (jsmith975)

-- Directions:
-- Please follow all instructions for Phase II as listed on Canvas.
-- Fill in the team number and names and GT usernames for all members above.
-- Create Table statements must be manually written, not taken from an SQL Dump file.
-- This file must run without error for credit.

/* This is a standard preamble for most of our scripts.  The intent is to establish
a consistent environment for the database behavior. */
set global transaction isolation level serializable;
set global SQL_MODE = 'ANSI,TRADITIONAL';
set names utf8mb4;
set SQL_SAFE_UPDATES = 0;

set @thisDatabase = 'business_supply';
drop database if exists business_supply;
create database if not exists business_supply;
use business_supply;

-- Define the database structures
/* You must enter your tables definitions, along with your primary, unique and foreign key
declarations, and data insertion statements here.  You may sequence them in any order that
works for you.  When executed, your statements must create a functional database that contains
all of the data, and supports as many of the constraints as reasonably possible. */

drop table if exists database_user;
create table database_user (
username varchar(40),
first_name varchar(100) not null,
last_name varchar(100) not null,
address varchar(500) not null,
birthdate date not null,
primary key(username)
) ENGINE = InnoDB;

drop table if exists employee;
create table employee (
username varchar(40),
taxID char(11) unique not null, #XXX-XX-XXXX
experience int not null,
hired date not null,
salary int not null,
foreign key(username) references database_user(username),
primary key(taxID)
) ENGINE = InnoDB;

drop table if exists business_owner; #owner is a keyword so changed to business_owner
create table business_owner (
username varchar(40),
foreign key(username) references database_user(username),
primary key(username)
) ENGINE = InnoDB;

drop table if exists driver;
create table driver (
license_type varchar(100) not null,
successful_trips int not null,
license_id varchar(40) not null,
taxID char(11) unique not null,
foreign key(taxID) references employee(taxID),
primary key(license_id)
) ENGINE = InnoDB;

drop table if exists location;
create table location (
label varchar(40),
x_coord int not null,
y_coord int not null,
location_space int, #space is a keyword so changed to location_space
primary key(label)
) ENGINE = InnoDB;

drop table if exists service;
create table service (
ID varchar(40),
service_name varchar(100) not null, #name is a keyword so changed to service_name
label varchar(100) not null,
foreign key(label) references location(label),
primary key(ID)
) ENGINE = InnoDB;

drop table if exists worker;
create table worker (
taxID char(11) unique not null,
manageID varchar(40),
foreign key(taxID) references employee(taxID),
foreign key(manageID) references service(ID),
primary key(taxID)
) ENGINE = InnoDB;

drop table if exists van;
create table van (
ID varchar(40),
tag varchar(40),
fuel int not null,
capacity int not null,
sales int not null,
controlDriver varchar(40),
parkLocation varchar(40),
foreign key(ID) references service(ID),
foreign key(controlDriver) references driver(license_id),
foreign key(parkLocation) references location(label),
primary key(ID, tag)
) ENGINE = InnoDB;

drop table if exists business;
create table business (
business_name varchar(40),
rating int not null,
spent int not null,
label varchar(40) not null, 
foreign key(label) references location(label),
primary key(business_name)
) ENGINE = InnoDB;

drop table if exists product;
create table product (
barcode varchar(40), #primary key idc
iname varchar(100) not null,
weight int not null,
primary key(barcode)
) ENGINE = InnoDB;

drop table if exists OwnerFundsBusiness;
create table OwnerFundsBusiness (
username varchar(40),
business_name varchar(40),
invested int,
dt_invested date, 
foreign key(business_name) references business(business_name),
foreign key(username) references business_owner(username),
primary key(username, business_name)
) ENGINE = InnoDB;

drop table if exists VanContainProduct;
create table VanContainProduct (
ID varchar(40),
tag varchar(40),
barcode varchar(40),
price int,
quantity int,
foreign key(ID, tag) references van(ID, tag),
foreign key(barcode) references product(barcode),
primary key(ID, tag, barcode)
) ENGINE = InnoDB;

drop table if exists WorkerWork_forService;
create table WorkerWork_forService (
taxID char(11) unique not null,
ID varchar(40),
foreign key(taxID) references employee(taxID),
foreign key(ID) references service(ID),
primary key(taxID, ID)
) ENGINE = InnoDB;

#INSERT statements below
insert into database_user
	(username, first_name, last_name, address, birthdate)
values
('agarcia7', 'Alejandro', 'Garcia', '710 Living Water Drive', '1966-10-29'),
('awilson5', 'Aaron', 'Wilson','220 Peachtree Street', '1963-11-11'),
('bsummers4', 'Brie', 'Summers', '5105 Dragon Star Circle',	'1976-02-09'),
('cjordan5', 'Clark', 'Jordan',	'77 Infinite Stars Road', '1966-06-05'),
('ckann5', 'Carrot', 'Kann', '64 Knights Square Trail',	'1972-09-01'),
('csoares8', 'Claire', 'Soares', '706 Living Stone Way', '1965-09-03'),
('echarles19', 'Ella', 'Charles', '22 Peachtree Street', '1974-05-06'),
('eross10',	'Erica', 'Ross', '22 Peachtree Street', '1975-04-02'),
('fprefontaine6', 'Ford', 'Prefontaine', '10 Hitch Hikers Lane', '1961-01-28'),
('hstark16', 'Harmon', 'Stark', '53 Tanker Top Lane', '1971-10-27'),
('jstone5',	'Jared', 'Stone', '101 Five Finger Way', '1961-01-06'),
('lrodriguez5',	'Lina', 'Rodriguez', '360 Corkscrew Circle', '1975-04-02'),
('mrobot1',	'Mister', 'Robot',	'10 Autonomy Trace', '1988-11-02'),
('mrobot2',	'Mister', 'Robot', '10 Clone Me Circle', '1988-11-02'),
('rlopez6',	'Radish', 'Lopez', '8 Queens Route', '1999-09-03'),
('sprince6', 'Sarah', 'Prince',	'22 Peachtree Street', '1968-06-15'),
('tmccall5', 'Trey', 'McCall', '360 Corkscrew Circle', '1973-03-19');

insert into employee
	(username, taxID, experience, hired, salary)
values
('agarcia7', '999-99-9999',	'24', '2019-03-17',	'41000'),
('awilson5', '111-11-1111',	'9', '2020-03-15', '46000'),
('bsummers4', '000-00-0000', '17', '2018-12-06', '35000'),
('ckann5', '640-81-2357', '27', '2019-08-03', '46000'),
('csoares8', '888-88-8888',	'26', '2019-02-25',	'57000'),
('echarles19', '777-77-7777', '3',	'2021-01-02', '27000'),
('eross10',	'444-44-4444', '10', '2020-04-17',	'61000'),
('fprefontaine6', '121-21-2121', '5', '2020-04-19',	'20000'),
('hstark16', '555-55-5555',	'20', '2018-07-23',	'59000'),
('lrodriguez5',	'222-22-2222', '20', '2019-04-15', '58000'),
('mrobot1',	'101-01-0101',	'8', '2015-05-27', '38000'),
('mrobot2',	'010-10-1010', '8',	'2015-05-27', '38000'),
('rlopez6',	'123-58-1321', '51', '2017-02-05', '64000'),
('tmccall5', '333-33-3333',	'29', '2018-10-17',	'33000');

insert into business_owner
	(username)
values
('cjordan5'),
('jstone5'),
('sprince6');

insert into driver
	(license_type, successful_trips, license_id, taxID)
values
('CDL',	'38', '610623', '999-99-9999'),
('commercial', '41', '314159', '111-11-1111'),
('private',	'35', '411911',	'000-00-0000'),
('commercial', '7',	'343563', '888-88-8888'),
('private', '2', '657483', '121-21-2121'),
('CDL',	'67', '287182',	'222-22-2222'),
('CDL',	'18', '101010', '101-01-0101'),
('private', '58', '235711', '123-58-1321');

insert into location
	(label, x_coord, y_coord, location_space)
values
('airport', '5', '-6', '15'),
('downtown', '-4', '-3', '10'),
('springs',	'7', '10', '8'),
('buckhead', '7', '10',	'8'),
('avalon', '2',	'15', '12'),
('mercedes', '-8', '5',	NULL),
('highlands', '2', '1',	'7'),
('southside', '1', '-16', '5'),
('midtown',	'2', '1', '7'),
('plaza', '-4',	'-3', '10');

insert into service
	(ID, service_name, label)
values
('mbm', 'Metro Business Movers', 'southside'),
('lcc', 'Local Commerce Couriers', 'plaza'),
('pbl',	'Pro Business Logistics', 'avalon');

insert into worker
	(taxID, manageID)
values
('640-81-2357', NULL),
('777-77-7777',	'pbl'),
('444-44-4444',	'lcc'),
('555-55-5555',	'mbm'),
('333-33-3333',	NULL),
('010-10-1010', NULL);

insert into van
	(ID, tag, fuel, capacity, sales, controlDriver, parkLocation)
values
('mbm',	'1', '100', '6', '0', '657483', 'southside'),
('mbm',	'5', '27', '7', '100', '657483', 'buckhead'),
('mbm',	'8', '100',	'8', '0', '411911', 'southside'),
('mbm',	'11', '25',	'10', '0', NULL, 'southside'),
('mbm',	'16', '17',	'5', '40', '657483', 'southside'),
('lcc',	'1', '100',	'9', '0', '314159', 'airport'),
('lcc',	'2', '75', '7',	'0', NULL, 'plaza'),
('pbl',	'3', '100',	'5', '50', '610623', 'avalon'),
('pbl',	'7', '53', '5',	'100', '610623', 'avalon'),
('pbl',	'8', '100',	'6', '0', '610623', 'highlands'),
('pbl',	'11', '90',	'6', '0', NULL,	'avalon');

insert into business
	(business_name, rating, spent, label)
values
('Aircraft Electrical Svc', '5', '10', 'airport'),
('Homestead Insurance',	'5', '30', 'downtown'),
('Jones and Associates', '3', '0', 'springs'),
('Prime Solutions', '4', '30', 'buckhead'),
('Innovative Ventures',	'4', '0', 'avalon'),
('Blue Horizon Enterprises', '4', '10', 'mercedes'),
('Peak Performance Group', '5',	'20', 'highlands'),
('Summit Strategies', '2', '0',	'southside'),
('Elevate Consulting', '5',	'30', 'midtown'),
('Pinnacle Partners', '4', '10', 'plaza');

insert into product
	(barcode, iname, weight)
values
('gc_4C6B9R', 'glass cleaner', '4'),
('pn_2D7Z6C', 'pens', '5'),
('sd_6J5S8H', 'screwdrivers', '4'),
('pt_16WEF6', 'paper towels', '6'),
('st_2D4E6L',' shipping tape', '3'),
('hm_5E7L23M', 'hammer', '3');

insert into OwnerFundsBusiness
	(username, business_name, invested, dt_invested)
values
('jstone5', 'Jones and Associates',	'20', '2022-10-25'),
('sprince6', 'Blue Horizon Enterprises', '10', '2022-03-06'),
('jstone5',	'Peak Performance Group', '30',	'2022-09-08'),
('jstone5',	'Elevate Consulting', '5', '2022-07-25');

insert into VanContainProduct
	(ID, tag, barcode, price, quantity)
values
('pbl',	'3', 'pn_2D7Z6C', '28',	'2'),
('mbm',	'5', 'pn_2D7Z6C', '30',	'1'),
('lcc',	'1', 'pt_16WEF6', '20',	'5'),
('mbm',	'8', 'pt_16WEF6', '18',	'4'),
('lcc',	'1', 'st_2D4E6L', '23',	'3'),
('mbm',	'11', 'st_2D4E6L', '19', '3'),
('mbm',	'1', 'st_2D4E6L', '27', '6'),
('lcc',	'2', 'hm_5E7L23M', '14', '7'),
('pbl',	'3', 'hm_5E7L23M', '15', '2'),
('mbm',	'5', 'hm_5E7L23M', '17', '4');

insert into WorkerWork_forService
	(taxID, ID)
values
('640-81-2357',	'lcc'),
('777-77-7777',	'pbl'),
('444-44-4444',	'lcc'),
('555-55-5555',	'mbm'),
('333-33-3333',	'mbm'),
('010-10-1010',	'pbl');



