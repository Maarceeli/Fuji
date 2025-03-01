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

def get_recent_grades(days=7, db_path="grades.db"):
    """
    Retrieve grades from the database from the last specified number of days.
    
    Args:
        days (int): Number of days to look back
        db_path (str): Path to the SQLite database file
    
    Returns:
        list: List of dictionaries containing the grade records
    """
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    
    # Configure connection to return datetime objects for timestamp fields
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Calculate the date from which to retrieve grades
    cutoff_date = datetime.datetime.now() - timedelta(days=days)
    
    # Query recent grades
    cursor.execute('''
    SELECT * FROM grades
    WHERE created_at >= ?
    ORDER BY created_at DESC
    ''', (cutoff_date,))
    
    # Fetch all results
    results = cursor.fetchall()
    
    # Convert results to a list of dictionaries for easier access
    grades = []
    for row in results:
        grade_dict = dict(row)
        grades.append(grade_dict)
    
    # Close connection
    conn.close()
    
    return grades

def get_grades_by_subject(subject, db_path="grades.db"):
    """
    Retrieve grades for a specific subject from the database.
    
    Args:
        subject (str): The subject name to filter by
        db_path (str): Path to the SQLite database file
    
    Returns:
        list: List of dictionaries containing the grade records
    """
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    
    # Configure connection to return dictionary-like objects
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Query grades by subject
    cursor.execute('''
    SELECT * FROM grades
    WHERE subject = ?
    ORDER BY created_at DESC
    ''', (subject,))
    
    # Fetch all results
    results = cursor.fetchall()
    
    # Convert results to a list of dictionaries for easier access
    grades = []
    for row in results:
        grade_dict = dict(row)
        grades.append(grade_dict)
    
    # Close connection
    conn.close()
    
    return grades

def display_grades(grades):
    """
    Helper function to display grades in a readable format.
    
    Args:
        grades (list): List of grade dictionaries
    """
    if not grades:
        print("No grades found.")
        return
    
    for grade in grades:
        created_at = grade['created_at']
        if isinstance(created_at, str):
            created_at = datetime.datetime.fromisoformat(created_at)
        
        print(f"Subject: {grade['subject']}")
        print(f"Value: {grade['value']} (Weight: {grade['weight']})")
        print(f"Name: {grade['name']}")
        print(f"Created at: {created_at}")
        print(f"Creator: {grade['creator']}")
        print("-" * 50)