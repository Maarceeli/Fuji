import flet as ft

# Grade colors
GRADE_COLORS = {
    1: "#F44336",
    2: "#FF9800",
    3: "#eebd00",
    4: "#4CAF50",
    5: "#2196F3",
    6: "#9C27B0",
    "other": "#5D5D5D"
}

SUBJECTS = [
    "Matematyka", "Język polski", "Język Angielski",
    "Informatyka", "Język Niemiecki", "Chemia"
]

NAV_ITEMS = [
    (ft.Icons.HOME, "Home"),
    (ft.Icons.LOOKS_6, "Grades"),
    (ft.Icons.BACKPACK, "Timetable"),
    (ft.Icons.BOOK, "Homework"),
    (ft.Icons.CALENDAR_TODAY, "Exams"),
    (ft.Icons.EVENT_NOTE, "Attendance"),
    (ft.Icons.STICKY_NOTE_2, "Behaviour"),
    (ft.Icons.SETTINGS, "Settings")
]

def main(page: ft.Page):
    page.title = "Fuji"
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.RED)

    def create_grade_container(grade: int):
        return ft.Container(
            content=ft.Text(str(grade)),
            margin=0,
            padding=0,
            alignment=ft.alignment.center,
            bgcolor=GRADE_COLORS.get(grade, GRADE_COLORS["other"]),
            width=20,
            height=20,
            border_radius=5,
        )

    def create_subject_row(subject: str):
        return ft.Row([
            ft.Text(subject, size=16, weight="normal"),
            *[create_grade_container(grade) for grade in range(6, 0, -1)]
        ])

    def create_card(title: str, icon, content):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(icon, size=32, color="#FFFFFF"),
                    ft.Text(title, size=24, font_family="Roboto", weight="bold")
                ]),
                ft.ListView(
                    controls=[content],
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
        )

    def change_page(index):
        if index == 0:  # Home Page
            timetable_content = ft.Text("1. Lorem ipsum\n"*10, size=16, weight="normal")
            grades_content = ft.Column([create_subject_row(subject) for subject in SUBJECTS])
            
            return ft.Column([
                ft.Text("  Home", size=30, weight="bold"),
                ft.Text("\n", size=30, weight="bold"),
                ft.Row([
                    create_card("Timetable", ft.Icons.BACKPACK_OUTLINED, timetable_content),
                    create_card("Recent Grades", ft.Icons.LOOKS_6_OUTLINED, grades_content)
                ])
            ])
        
        # Other pages
        return ft.Column([
            ft.Text(f"  {NAV_ITEMS[index][1]}", size=30, weight="bold"),
        ])

    def update_content(e):
        main_container.content = change_page(e.control.selected_index)
        page.update()

    # Navigation Rail
    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        extended=False,
        min_width=50,
        min_extended_width=400,
        group_alignment=0,
        destinations=[
            ft.NavigationRailDestination(
                icon=item[0]+"_OUTLINED",
                selected_icon=item[0],
                label=item[1]
            ) for item in NAV_ITEMS
        ],
        on_change=update_content
    )

    main_container = ft.Container(content=change_page(0), expand=True)
    page.add(ft.Row([nav_rail, main_container], expand=True))

ft.app(main)