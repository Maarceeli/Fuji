import flet as ft
import json
from pages.home import *

def main(page: ft.Page):
    page.title = "Fuji"
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.RED, font_family="Roboto")
    
    def changePage(index):
        pages = [
            # Home page
            HomePage(),
            
            # Grades page
            ft.Column([
                ft.Text("  Grades", size=30, weight="bold"),
            ]),

            # Timetable page
            ft.Column([
                ft.Text("  Timetable", size=30, weight="bold"),
            ]),

            # Homework page
            ft.Column([
                ft.Text("  Homework", size=30, weight="bold"),
            ]),

            # Exams page
            ft.Column([
                ft.Text("  Exams", size=30, weight="bold"),
            ]),

            # Attendance page
            ft.Column([
                ft.Text("  Attendance", size=30, weight="bold"),
            ]),

            # Behaviour page
            ft.Column([
                ft.Text("  Behaviour Notes", size=30, weight="bold"),
            ]),

            # Settings page
            ft.Column([
                ft.Text("  Settings", size=30, weight="bold"),
            ]),
        ]
        return pages[index]

    # Function to switch content
    def update_content(index):
        main_container.content = changePage(index)
        page.update()

    # Initial content display container
    main_container = ft.Container(
        content=changePage(0),
        expand=True,
    )

    # Navigation Rail
    bar = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        extended=False,
        min_width=50,
        min_extended_width=400,
        group_alignment=0,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Home"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.LOOKS_6_OUTLINED, selected_icon=ft.Icons.LOOKS_6, label="Grades"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.BACKPACK_OUTLINED, selected_icon=ft.Icons.BACKPACK, label="Timetable"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.BOOK_OUTLINED, selected_icon=ft.Icons.BOOK, label="Homework"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.CALENDAR_TODAY_OUTLINED, selected_icon=ft.Icons.CALENDAR_TODAY, label="Exams"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.EVENT_NOTE_OUTLINED, selected_icon=ft.Icons.EVENT_NOTE, label="Attendance"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.STICKY_NOTE_2_OUTLINED, selected_icon=ft.Icons.STICKY_NOTE_2, label="Behaviour"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icons.SETTINGS_ROUNDED, label="Settings"
            ),
        ],
        on_change=lambda e: update_content(e.control.selected_index),
    )

    page.add(
        ft.Row(
            [
                bar,
                main_container,
            ],
            expand=True,
        )
    )

def login(page: ft.Page):
    page.title = "Log in"
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.RED, font_family="Roboto")

    loginpage = ft.Container(
        content=ft.Column(
            [
                ft.Image(
                src="https://i.imgur.com/t49tb4d.png",
                width=200,
                height=200,
                fit=ft.ImageFit.NONE,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(100)),

                ft.Text(value="Welcome to Fuji!", size=48)
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Center text vertically in Column
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Center text horizontally
        ),
        alignment=ft.alignment.center,  # Center the entire container on the page
        expand=True,  # Allow the container to take full page size
    )
    
    page.add(loginpage)
    page.update()

    
if __name__ == "__main__":
    try:
        with open("config.json", "r") as file:
            data = json.load(file)
        if data.get("isLoggedIn", False):
            ft.app(target=main)
        else:
            ft.app(target=login)
    except FileNotFoundError:
        config = {"isLoggedIn": False}
        with open("config.json", "w") as file:
            json.dump(config, file)
        ft.app(target=login)