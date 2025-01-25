import flet as ft

# vars
grade1 = "#F44336"
grade2 = "#FF9800"
grade3 = "#eebd00"
grade4 = "#4CAF50"
grade5 = "#2196F3"
grade6 = "#9C27B0"
gradeother = "#5D5D5D"

def main(page: ft.Page):
    page.title = "Fuji"
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.RED)
    
    def changePage(index):
        pages = [
            # Home page
            ft.Column([
                ft.Text("  Home", size=30, weight="bold"),
                ft.Text("\n", size=30, weight="bold"),
                ft.Row([
                    ft.Container( # Timetable Card
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.BACKPACK_OUTLINED, size=32, color="#FFFFFF"),
                                ft.Text("Timetable", size=24, font_family="Roboto", weight="bold")
                            ]),
                            ft.ListView(
                                controls=[
                                    ft.Text("1. Lorem ipsum\n2. Lorem ipsum\n3. Lorem ipsum\n4. Im curious what happens if i ran out of space\n5. It just creates a new line\n6. No idea why i tested that\n7. I also want to test what happens if there is too much lines\n8. Lorem ipsum\n9. Yay now you can scroll\n10. Looks like dogshit but it works\n11. Simi simi jej simi jaj", size=16, weight="normal")
                                ],
                                expand=True,
                                spacing=10,
                                padding=10,
                                auto_scroll=False
                            )
                        ]), 
                        margin=20,
                        padding=10,
                        alignment=ft.alignment.top_left,
                        bgcolor='#271D1C',
                        width=420,
                        height=270,
                        border_radius=10,
                    ),
                    
                    ft.Container( # Recent Grades Card
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.LOOKS_6_OUTLINED, size=32, color="#FFFFFF"),
                                ft.Text("Recent Grades", size=24, font_family="Roboto", weight="bold")
                            ]),
                            ft.ListView(
                                controls=[
                                    ft.Row([
                                        ft.Text("Matematyka", size=16, weight="normal"),
                                        ft.Container(
                                            content=ft.Text("6"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade6,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("5"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade5,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("4"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade4,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("3"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade3,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("2"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade2,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("1"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade1,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                    ]),
                                    ft.Row([
                                        ft.Text("Język polski", size=16, weight="normal"),
                                        ft.Container(
                                            content=ft.Text("6"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade6,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("5"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade5,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("4"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade4,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("3"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade3,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("2"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade2,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("1"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade1,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                    ]),
                                    ft.Row([
                                        ft.Text("Język Angielski", size=16, weight="normal"),
                                        ft.Container(
                                            content=ft.Text("6"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade6,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("5"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade5,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("4"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade4,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("3"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade3,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("2"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade2,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("1"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade1,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                    ]),
                                    ft.Row([
                                        ft.Text("Informatyka", size=16, weight="normal"),
                                        ft.Container(
                                            content=ft.Text("6"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade6,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("5"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade5,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("4"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade4,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("3"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade3,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("2"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade2,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("1"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade1,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                    ]),
                                    ft.Row([
                                        ft.Text("Język Niemiecki", size=16, weight="normal"),
                                        ft.Container(
                                            content=ft.Text("6"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade6,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("5"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade5,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("4"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade4,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("3"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade3,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("2"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade2,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("1"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade1,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                    ]),
                                    ft.Row([
                                        ft.Text("Chemia", size=16, weight="normal"),
                                        ft.Container(
                                            content=ft.Text("6"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade6,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("5"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade5,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("4"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade4,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("3"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade3,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("2"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade2,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                        ft.Container(
                                            content=ft.Text("1"),
                                            margin=0,
                                            padding=0,
                                            alignment=ft.alignment.center,
                                            bgcolor=grade1,
                                            width=20,
                                            height=20,
                                            border_radius=5,
                                        ),
                                    ]),
                                ],
                                expand=False,
                                spacing=10,
                                padding=10,
                                auto_scroll=False
                            )
                        ]), 
                        margin=20,
                        padding=10,
                        alignment=ft.alignment.top_left,
                        bgcolor='#271D1C',
                        width=420,
                        height=270,
                        border_radius=10,
                    ),
                ]),
                
            ]),
            
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

ft.app(main)
