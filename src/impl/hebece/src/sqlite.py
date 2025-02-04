import sqlite3
import json

def ImportGradesToSQLite(content):
    data = json.loads(content)

    conn = sqlite3.connect('grades.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY,
        pupil_id INTEGER,
        content_raw TEXT,
        content TEXT,
        value INTEGER,
        description TEXT,
        date_created TEXT,
        date_modified TEXT,
        creator_name TEXT,
        creator_surname TEXT,
        lesson_name TEXT,
        lesson_code TEXT,
        category_name TEXT,
        category_code TEXT
    )
    ''')

    for entry in data['Envelope']:
        column = entry.get('Column') or {} 
        subject = column.get('Subject') or {}
        category = column.get('Category') or {}
        creator = entry.get('Creator') or {}
        
        cursor.execute('''
        INSERT or IGNORE INTO grades (
            id, pupil_id, content_raw, content, value, description,
            date_created, date_modified, creator_name, creator_surname,
            lesson_name, lesson_code, category_name, category_code
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            entry.get('Id'),
            entry.get('PupilId'),
            entry.get('ContentRaw'),
            entry.get('Content'),
            entry.get('Value'),
            entry.get('Comment'),
            entry.get('DateCreated', {}).get('DateDisplay'),
            entry.get('DateModify', {}).get('DateDisplay'),
            creator.get('Name'),
            creator.get('Surname'),
            subject.get('Name'),
            subject.get('Kod'),
            category.get('Name'),
            category.get('Code')
        ))

    conn.commit()
    conn.close()
    
def ImportTimetableToSQLite(content):
    data = json.loads(content)

    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS timetable (
        id INTEGER PRIMARY KEY,
        date TEXT,
        start_time TEXT,
        end_time TEXT,
        subject_name TEXT,
        teacher_name TEXT,
        teacher_surname TEXT,
        room_code TEXT,
        class_display TEXT,
        position INTEGER
    )
    ''')

    for entry in data['Envelope']:
        cursor.execute('''
        INSERT OR IGNORE INTO timetable (
            id, date, start_time, end_time, subject_name, teacher_name, 
            teacher_surname, room_code, class_display, position
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            entry.get('Id'),
            entry.get('Date', {}).get('DateDisplay'),
            entry.get('TimeSlot', {}).get('Start'),
            entry.get('TimeSlot', {}).get('End'),
            entry.get('Subject', {}).get('Name'),
            entry.get('TeacherPrimary', {}).get('Name'),
            entry.get('TeacherPrimary', {}).get('Surname'),
            entry.get('Room', {}).get('Code'),
            entry.get('Clazz', {}).get('DisplayName'),
            entry.get('TimeSlot', {}).get('Position') or 0
        ))

    conn.commit()
    conn.close()
    
def getTimetableForDay(day):
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    def get_lessons_for_day_sorted(date):
        cursor.execute('SELECT * FROM timetable WHERE date = ? ORDER BY position ASC', (date,))
        lessons = cursor.fetchall()
        return lessons


    day_to_check = day
    lessons_for_day_sorted = get_lessons_for_day_sorted(day_to_check)
    conn.close()

    return lessons_for_day_sorted

def ImportExamsToSQLite(content):
    data = json.loads(content)
    
    conn = sqlite3.connect("exams.db")
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS exams (
        id INTEGER PRIMARY KEY,
        type TEXT,
        content TEXT,
        date_created TEXT,
        date_modified TEXT,
        deadline TEXT,
        creator_name TEXT,
        creator_surname TEXT,
        subject_name TEXT,
        pupil_id INTEGER
    )
    ''')

    for entry in data['Envelope']:
        cursor.execute('''
        INSERT OR IGNORE INTO exams (
            id, type, content, date_created, date_modified, deadline, 
            creator_name, creator_surname, subject_name, pupil_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            entry.get('Id'),
            entry.get('Type'),
            entry.get('Content'),
            entry.get('DateCreated', {}).get('DateDisplay'),
            entry.get('DateModify', {}).get('DateDisplay'),
            entry.get('Deadline', {}).get('DateDisplay'),
            entry.get('Creator', {}).get('Name'),
            entry.get('Creator', {}).get('Surname'),
            entry.get('Subject', {}).get('Name'),
            entry.get('PupilId')
        ))
    
    conn.commit()
    conn.close()

def getExamsForWeek(start_date, end_date):
    conn = sqlite3.connect("exams.db")
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM exams 
    WHERE deadline BETWEEN ? AND ?
    ORDER BY deadline ASC
    ''', (start_date, end_date))
    exams = cursor.fetchall()
    conn.close()
    return exams