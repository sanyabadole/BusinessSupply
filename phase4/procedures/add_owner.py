from datetime import datetime

def add_owner(cursor, connection, username, first_name, last_name, address, birthdate):
    if not all([username, first_name, last_name, address, birthdate]):
        raise ValueError("All fields must be filled out.")

    # Validate birthdate format
    try:
        datetime.strptime(birthdate, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Birthdate must be in YYYY-MM-DD format.")

    # Check if username exists
    cursor.execute("SELECT COUNT(*) FROM business_owners WHERE username = %s", (username,))
    if cursor.fetchone()[0] > 0:
        raise ValueError("Username already exists.")

    # Call the stored procedure
    cursor.callproc('add_owner', (username, first_name, last_name, address, birthdate))
    connection.commit()
    return "Owner added successfully!"