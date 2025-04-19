import flet as ft
from collections import defaultdict
from sqlitehandlernr import fetch_grades_this_week
from utils import format_grade
from i18n import _

def RecentGradesColumn():
    """
    Create a column containing the recent grades content styled like the image.
    
    Args:
        db_path (str): Path to the SQLite database file
        
    Returns:
        ft.Column: A column widget containing the recent grades UI
    """
    # Create a function to load grades
    def load_grades(e=None):
        try:
            # Get grades from the current week
            grades_list = fetch_grades_this_week()
            
            # Group by subject
            grades_by_subject = defaultdict(list)
            for grade in grades_list:
                subject = grade.subject
                grades_by_subject[subject].append(grade)
            
            # Prepare the list of controls
            grade_controls = []
            
            if not grades_list:
                # No grades found
                grade_controls.append(
                    ft.Text(_("No grades found for this week."), 
                           color="#AAAAAA")
                )
            else:
                # Add each subject with its grades
                for subject, grades in grades_by_subject.items():
                    # Format grades as a space-separated string  
                    formatted_grades = [format_grade(grade) for grade in grades]
                    
                    # Create a row for each subject 
                    subject_row = ft.Row([
                        ft.Text(
                            subject,
                            color="#FFFFFF",
                            size=16,
                            expand=True,
                            no_wrap=False
                        ),
                        *[
                            ft.Container(
                                content=ft.Text(grade_val, color="#FFFFFF", size=16, text_align=ft.TextAlign.CENTER, width=30),
                                expand=False,
                                bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                                width=30,
                                height=30,
                                border_radius=1000,
                                alignment=ft.alignment.center,
                            )
                            for grade_val in formatted_grades
                        ]
                    ])
                    grade_controls.append(subject_row)
            
            return grade_controls
            
        except Exception as e:
            # Return an error message
            return [
                ft.Text(f"Error loading grades: {str(e)}", 
                       color="#FF0000")
            ]
    
    # Load the initial grades
    initial_grades = load_grades()
    
    # Create the grades ListView
    grades_listview = ft.ListView(
        controls=initial_grades,
        expand=True,
        spacing=8,
        padding=ft.padding.only(left=10, right=10, top=10, bottom=16)
    )
    
    
    # Create the header section like in the image
    header = ft.Row([
        ft.Icon(ft.Icons.FILTER_6, size=32, color="#FFFFFF"),
        ft.Text((_("Recent Grades")), size=24, font_family="Roboto", weight="bold", color="#FFFFFF")
    ], spacing=12, alignment=ft.MainAxisAlignment.START)
    
    # Create the column with header and content
    return ft.Container(
        content=ft.Column([
            header,
            grades_listview
        ], spacing=5),
        padding=ft.padding.only(left=5, right=5, top=5),
        expand=True
    )