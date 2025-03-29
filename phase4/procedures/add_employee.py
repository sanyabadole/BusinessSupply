import re
from datetime import datetime

def validate_taxID(taxID):
    pattern = r'^\d{3}-\d{2}-\d{4}$'
    return bool(re.match(pattern, taxID))

def add_employee(cursor, connection, username, first_name, last_name, address, birthdate, taxID, hired, experience, salary):
    if not all([username, first_name, last_name, address, birthdate, taxID, hired, experience, salary]):
        raise ValueError("All fields must be filled out.")

    # Validate date formats
    try:
        datetime.strptime(birthdate, '%Y-%m-%d')
        datetime.strptime(hired, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Dates must be in YYYY-MM-DD format.")

    # Validate Tax ID format
    if not validate_taxID(taxID):
        raise ValueError("Tax ID must be in the format XXX-XX-XXXX.")

    # Validate salary and experience
    try:
        salary = int(salary)
        experience = int(experience)
        if salary < 0 or experience < 0:
            raise ValueError("Salary and experience cannot be negative.")
    except ValueError:
        raise ValueError("Invalid salary or experience value.")

    # Check for unique fields
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username,))
    if cursor.fetchone()[0] > 0:
        raise ValueError("Username already exists in users.")

    cursor.execute("SELECT COUNT(*) FROM employees WHERE username = %s", (username,))
    if cursor.fetchone()[0] > 0:
        raise ValueError("Username already exists in employees.")

    cursor.execute("SELECT COUNT(*) FROM employees WHERE taxID = %s", (taxID,))
    if cursor.fetchone()[0] > 0:
        raise ValueError("Tax ID already exists.")

    # Call the stored procedure
    cursor.callproc('add_employee', (username, first_name, last_name, address, birthdate,
                                     taxID, hired, experience, salary))
    connection.commit()
    return "Employee added successfully!"