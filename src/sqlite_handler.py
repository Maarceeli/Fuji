import sqlite3
import datetime
import re
from datetime import timedelta

def create_grades_database(grades_list, db_path="grades.db"):
    """
    Create a SQLite database from a list of Grade objects.
    
    Args:
        grades_list (list or str): List of Grade objects or string representation of the list
        db_path (str): Path to the SQLite database file
    
    Returns:
        bool: True if database was created successfully
    """
    # Connect to SQLite database (will create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create grades table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        value TEXT NOT NULL,
        is_point BOOLEAN NOT NULL,
        point_numerator INTEGER,
        point_denominator INTEGER,
        weight REAL NOT NULL,
        name TEXT NOT NULL,
        created_at TIMESTAMP NOT NULL,
        subject TEXT NOT NULL,
        creator TEXT NOT NULL
    )
    ''')
    
    # Clear existing data if table exists
    cursor.execute('DELETE FROM grades')
    
    # Define regex pattern to extract grade information
    pattern = r"Grade\(value='(.*?)', is_point=(.*?), point_numerator=(.*?), point_denominator=(.*?), weight=(.*?), name='(.*?)', created_at=datetime\.datetime\((.*?)\), subject='(.*?)', creator='(.*?)'\)"
    
    # Convert to string if it's not already
    grades_str = str(grades_list)
    
    # Find all grades in the input string
    matches = re.finditer(pattern, grades_str)
    
    for match in matches:
        value = match.group(1)
        is_point = match.group(2).lower() == 'true'
        point_numerator = None if match.group(3) == 'None' else int(match.group(3))
        point_denominator = None if match.group(4) == 'None' else int(match.group(4))
        weight = float(match.group(5))
        name = match.group(6)
        
        # Parse datetime components
        datetime_parts = match.group(7).split(', ')
        year = int(datetime_parts[0])
        month = int(datetime_parts[1])
        day = int(datetime_parts[2])
        hour = int(datetime_parts[3])
        minute = int(datetime_parts[4])
        second = int(datetime_parts[5])
        microsecond = int(datetime_parts[6]) if len(datetime_parts) > 6 else 0
        
        created_at = datetime.datetime(year, month, day, hour, minute, second, microsecond)
        subject = match.group(8)
        creator = match.group(9)
        
        # Insert data into the database
        cursor.execute('''
        INSERT INTO grades (value, is_point, point_numerator, point_denominator, weight, name, created_at, subject, creator)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (value, is_point, point_numerator, point_denominator, weight, name, created_at, subject, creator))
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"Database created successfully with data from {len(list(re.finditer(pattern, grades_str)))} grades")
    return True

def get_current_week_grades(db_path="grades.db"):
    """
    Get all grades from the current week (Monday to Sunday).
    """
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    
    # Configure connection to return dictionary-like objects
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Calculate the start and end of the current week
    today = datetime.datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)
    
    # Query to get grades from the current week
    cursor.execute('''
    SELECT id, subject, name, value, is_point, point_numerator, point_denominator, created_at 
    FROM grades
    WHERE created_at BETWEEN ? AND ?
    ORDER BY subject, created_at
    ''', (start_of_week, end_of_week))
    
    # Convert cursor results to dictionaries
    grades = [dict(row) for row in cursor.fetchall()]
    
    # Close the connection
    conn.close()
    
    return grades