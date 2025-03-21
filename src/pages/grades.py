import flet as ft
from sqlitehandlernr import fetch_all_grades
from i18n import _

def parse_grade_value(value):
    """
    Parse grade value with optional + or - suffix.
    Args:
        value (str): Grade value as a string

    Returns:
        float: Parsed grade value, or None if unrecognized
    """
    try:
        base_value = float(value.rstrip('+-'))  # Remove +/- suffix and convert to float
        if value.endswith('+'):
            return base_value + 0.25  # Add 0.25 for "+" suffix
        elif value.endswith('-'):
            return base_value - 0.25  # Subtract 0.25 for "-" suffix
        return base_value
    except ValueError:
        return None  # Ignore unrecognized values

def GradesPage(page):
    """
    Generate grades page with subject-based panels and expandable content

    Args:
        page (flet.Page): Flet page instance
    """

    # Retrieve all grades from SQLite database
    grades = fetch_all_grades()

    # Create modal dialog for displaying grade details
    modal = ft.AlertDialog(
        modal=True,
        title=ft.Text(_("Test modal")),  # Set modal title with translated text
        content=ft.Text(""),  # Placeholder text that will be updated dynamically
        actions=[
            ft.TextButton("OK", on_click=lambda e: page.close(modal)),  # Close modal when OK button clicked
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Initialize subject-based panels and data storage
    panels = []
    subjects = {}

    # Group grades by subject
    for grade in grades:
        subject = grade.subject
        if subject not in subjects:  # Create new subject entry if not already present
            subjects[subject] = []
        subjects[subject].append(grade)  # Add grade to corresponding subject list
    
    def format_date(dt):
        """Format a datetime object to YYYY-MM-DD string"""
        return dt.strftime("%Y-%m-%d")
    
    def open_grade_modal(grade):
        """
        Open modal dialog with detailed grade information

        Args:
            grade (dict): Grade dictionary containing details
        """
        modal.title = ft.Text(_("Grade Details"))  # Update modal title
        parsed_value = parse_grade_value(grade.value)  # Parse grade value for display
        
        # Fixed line - don't use replace with None
        grade_text = f"{_('Grade')}: {grade.value}"
        if parsed_value is None:
            grade_text = f"{_('Grade')}: {_('Grade not recognized')}"
            
        modal.content = ft.Column([
            ft.Text(f"{_('Subject')}: {grade.subject}", size=14),  # Display subject and translated text
            ft.Text(grade_text, size=14),
            ft.Text(f"{_('Date')}: {format_date(grade.created_at)}", size=14),  # Format datetime object
            ft.Text(f"{_('Weight')}: {getattr(grade, 'weight', 1.0)}", size=14),
            ft.Text(f"{_('Description')}: {grade.name}", size=14),
            ft.Text(f"{_('Creator')}: {grade.creator}", size=14)
        ], expand=False)
        page.open(modal)  # Open modal dialog

    # Generate subject-based panels with expandable content
    for subject, grades_list in subjects.items():
        header = ft.Container(
            content=ft.Column(
                [
                    ft.Text(subject, size=15),  # Display subject name
                    ft.Row([
                        ft.Text(f"{len(grades_list)} "+_("grades"), size=14),  # Display number of grades and translated text
                        ft.Text((_("Average"))+": {:.2f}".format(
                            sum(parse_grade_value(g.value) for g in grades_list if parse_grade_value(g.value) is not None) / max(len([g for g in grades_list if parse_grade_value(g.value) is not None]), 1)
                        ), size=14),  # Calculate and display average grade
                    ])
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                expand=True,
            ),
            padding=ft.padding.all(10),
            expand=True,
        )

        grade_rows = []
        for grade in grades_list:
            grade_rows.append(
                ft.Container(
                    content=ft.Row([
                                ft.Container(
                                    content=ft.Text(grade.value, text_align=ft.TextAlign.CENTER),  # Display grade value
                                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                                    border_radius=5,
                                    margin=ft.margin.all(5),
                                    width=None,  # Allow the container to size based on content
                                    on_click=lambda e, grade=grade: open_grade_modal(grade),  # Open modal dialog when row clicked
                                    ),
                                ft.Column(
                                    [
                                        ft.Text(grade.name),  # Display grade name
                                        ft.Row([
                                            ft.Text(format_date(grade.created_at)),  # Format datetime object
                                            ft.Text((_("Weight"))+": {:.1f}".format(getattr(grade, 'weight', 1.0)))
                                        ])
                                    ],
                                    spacing=1
                                ),
                                ], expand=True),  # Allow Row to expand and avoid tight squeezing
                        on_click=lambda e, grade=grade: open_grade_modal(grade),
                        )
            )

        panel = ft.ExpansionPanel(
            header=header,
            content=ft.Column(grade_rows),
            expand=False,
            #bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            #can_tap_header=True,
        )
        panels.append(panel)

    return ft.Column([
        ft.Text((_("Grades")), size=30, weight="bold"),
        ft.ExpansionPanelList(panels)  # Display subject-based panels with expandable content
    ],
    scroll=True
    )