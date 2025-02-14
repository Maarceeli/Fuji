import flet as ft
import json
import keyring
import pickle
import base64
from pages.home import *
from sdk.src.interfaces.prometheus.context import *
from sdk.src.interfaces.prometheus.interface import *

def loadauth(service, username):
    try:
        count = int(keyring.get_password(service, f"{username}_count"))
        return "".join(keyring.get_password(service, f"{username}_{i}") or "" for i in range(count))
    except (TypeError, ValueError):
        return None

def main(page: ft.Page):
    page.title = "Fuji"
    page.theme = ft.Theme(
    color_scheme_seed=ft.Colors.RED,
    font_family="Roboto",
    page_transitions=ft.PageTransitionsTheme(
        android=ft.PageTransitionTheme.PREDICTIVE,
        ios=ft.PageTransitionTheme.PREDICTIVE,
        macos=ft.PageTransitionTheme.PREDICTIVE,
        linux=ft.PageTransitionTheme.PREDICTIVE,
        windows=ft.PageTransitionTheme.PREDICTIVE
        )
    )
    def changePage(index):
        pages = [
            # Home page
            HomePage(),
            
            # Grades page
            ft.Column([
                ft.Text("  Grades", size=30, weight="bold"),
                ft.Placeholder()
            ]),

            # Timetable page
            ft.Column([
                ft.Text("  Timetable", size=30, weight="bold"),
                ft.Placeholder()
            ]),

            # Homework page
            ft.Column([
                ft.Text("  Homework", size=30, weight="bold"),
                ft.Placeholder()
            ]),

            # Exams page
            ft.Column([
                ft.Text("  Exams", size=30, weight="bold"),
                ft.Placeholder()
            ]),

            # Attendance page
            ft.Column([
                ft.Text("  Attendance", size=30, weight="bold"),
                ft.Placeholder()
            ]),

            # Behaviour page
            ft.Column([
                ft.Text("  Behaviour Notes", size=30, weight="bold"),
                ft.Placeholder()
            ]),

            # Settings page
            ft.Column([
                ft.Text("  Settings", size=30, weight="bold"),
                ft.Placeholder()
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
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.RED,
        font_family="Roboto",
        page_transitions=ft.PageTransitionsTheme(
            android=ft.PageTransitionTheme.PREDICTIVE,
            ios=ft.PageTransitionTheme.PREDICTIVE,
            macos=ft.PageTransitionTheme.PREDICTIVE,
            linux=ft.PageTransitionTheme.PREDICTIVE,
            windows=ft.PageTransitionTheme.PREDICTIVE
        )
    )

    interface = None
    data = {"usr": None, "passwd": None}
    
    def changeusr(e):
        global usr
        
        data["usr"] = e.control.value
        #print(usr)

    def changepasswd(e):
        global passwd
        
        data["passwd"] = e.control.value
        #print(passwd)
    
    def loginev(e):   
        global interface
        
        login = data["usr"]
        password = data["passwd"]
        
        if login and password:
            interface = PrometheusInterface(auth_context=PrometheusAuthContext(prometheus_web_credentials=PrometheusWebCredentials(username=login, password=password)))
            interface.login()
            page.go("/students")
        else:
            print("No credentials!")
    
    def students():
        global interface
        
        students = interface.get_students()
        
        def saveauth(service, username, data, chunk_size=1000):
            chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
            keyring.set_password(service, f"{username}_count", str(len(chunks)))
            
            for i, chunk in enumerate(chunks):
                keyring.set_password(service, f"{username}_{i}", chunk)



        def on_change(e):
            selected_index = next((i for i, student in enumerate(students) if student.full_name == e.control.value), -1)
            interface.select_student(students[selected_index].context)
            
            auth_context = interface.get_auth_context()
            jsoncontext = auth_context.model_dump_json()
            
            saveauth("Fuji", "Auth Context", jsoncontext)
            
            config = {"isLoggedIn": True}
            with open("config.json", "w") as file:
                json.dump(config, file)
            
            page.go("/start")
                
            
        
        dropdown = ft.Dropdown(
            label="Select a Student",
            options=[
                ft.dropdown.Option(student.full_name) for student in students
            ],
            on_change=on_change,
            width=300
        )
        
        return dropdown
                
            
    
    def route_change(route):
        page.views.clear()
        
        # Welcome view
        if page.route == "/login":
            welcome_view = ft.View(
                route="/login",
                controls=[
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Image(
                                    src="src/assets/logo.png",
                                    width=256,
                                    height=256,
                                    fit=ft.ImageFit.CONTAIN,
                                    border_radius=ft.border_radius.all(100000)
                                ),
                                ft.Text(value="Welcome to Fuji!", size=64),
                                ft.Button(
                                    "Get Started", 
                                    scale=2.0, 
                                    width=230, 
                                    on_click=lambda e: page.go("/login/eduvulcan")
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=30
                        ),
                        alignment=ft.alignment.center,
                        expand=True,
                        padding=ft.padding.all(20)
                    )
                ]
            )
            page.views.append(welcome_view)
        
        # Login form view
        elif page.route == "/login/eduvulcan":
            login_view = ft.View(
                route="/login/eduvulcan",
                controls=[
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(value="Log in", size=32, weight="bold", 
                                       text_align=ft.TextAlign.CENTER),
                                
                                ft.TextField(
                                    label="Username",
                                    autofill_hints=[ft.AutofillHint.USERNAME],
                                    width=300,
                                    on_change=changeusr
                                ),
                                
                                ft.TextField(
                                    label="Password",
                                    password=True,
                                    can_reveal_password=True,
                                    autofill_hints=[ft.AutofillHint.PASSWORD],
                                    width=300,
                                    on_change=changepasswd
                                ),
                                
                                ft.Button("Log in", scale=1.25, width=250, on_click=loginev),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=30
                        ),
                        alignment=ft.alignment.center,
                        expand=True,
                        padding=ft.padding.all(20)
                    )
                ]
            )
            page.views.append(login_view)
        
        # Students view
        elif page.route == "/students":
            students_view = ft.View(
                route="/students",
                controls=[
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(value="Select a student", size=32, weight="bold", 
                                       text_align=ft.TextAlign.CENTER),
                                students(),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=30
                        ),
                        alignment=ft.alignment.center,
                        expand=True,
                        padding=ft.padding.all(20)
                    )
                ]
            )
            page.views.append(students_view)
        
        elif page.route == "/start":
            start_view = ft.View(
                route="/start",
                controls=[
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(value="Logged in!", size=32, weight="bold", 
                                       text_align=ft.TextAlign.CENTER),
                                
                                ft.Text(value="Please restart the app to use it.", size=16, weight="normal", 
                                       text_align=ft.TextAlign.CENTER),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=30
                        ),
                        alignment=ft.alignment.center,
                        expand=True,
                        padding=ft.padding.all(20)
                    )
                ]
            )
            page.views.append(start_view)
            
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/login")

    
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