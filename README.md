# Business Supply & Delivery Service System

A comprehensive database management system for a business supply and delivery service, featuring a modern GUI interface for managing operations, deliveries, and business relationships.

## Project Overview

This system manages a business supply and delivery service that:
- Handles product inventory and deliveries
- Manages delivery vans and their operations
- Tracks business owners, employees, and their roles
- Monitors service locations and delivery routes
- Handles product purchases and deliveries
- Manages employee roles (drivers, workers)

## Project Structure

The project is divided into four phases:

- **Phase 1**: Schema Design
- **Phase 2**: Database Schema Creation
  - Creates the core database structure
  - Defines tables for users, products, vans, locations, and services
  - Sets up initial data relationships
- **Phase 3**: Stored Procedures and Views
  - Implements business logic through stored procedures
  - Creates views for data visualization
  - Handles complex operations like van management and product tracking
- **Phase 4**: GUI Interface
  - Modern, user-friendly interface for system management
  - Features for viewing and managing all aspects of the business
  - Organized into logical sections for different operations

## Features

### User Management
- Add/Manage business owners
- Handle employee records
- Manage driver and worker roles
- Track employee assignments

### Product Management
- Track product inventory
- Monitor product locations
- Handle product purchases
- Manage product pricing

### Van Operations
- Track delivery vans
- Monitor van locations
- Handle van loading/unloading
- Manage fuel levels
- Track van assignments

### Business Operations
- Manage service locations
- Track business funding
- Handle employee hiring/firing
- Monitor service performance

## Setup Instructions

### Prerequisites
- MySQL Server
- Python 3.x
- Virtual Environment (recommended)

### Database Setup
1. Navigate to the `phase2` directory
2. Run the database creation script:
   ```bash
   mysql -u your_username -p < cs4400_phase2_database_completed.sql
   ```

### Stored Procedures Setup
1. Navigate to the `phase3` directory
2. Run the stored procedures script:
   ```bash
   mysql -u your_username -p < attemptphase3.sql
   ```

### GUI Setup
1. Navigate to the `phase4` directory
2. Create and activate the virtual environment:
   ```bash
   ./make_venv.sh
   source phase4_env/bin/activate  # On Unix/macOS
   # or
   .\phase4_env\Scripts\activate  # On Windows
   ```
3. Install required packages:
   ```bash
   pip install -r packages.txt
   ```
4. Run the GUI application:
   ```bash
   python phase4_gui.py
   ```

## System Architecture

### Database Design
- Relational database structure
- Optimized for delivery service operations
- Supports complex queries and operations
- Maintains data integrity and relationships

### GUI Features
- Modern, intuitive interface
- Organized by business function
- Real-time data updates
- User-friendly forms and displays
- Responsive design

### Business Logic
- Stored procedures for complex operations
- Views for data visualization
- Automated business rules
- Data validation and error handling

## Contributing
This is a course project repository. Please refer to the course guidelines for contribution rules.

## License
This project is part of a course assignment and should be used in accordance with the course policies. 
