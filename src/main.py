import json
import pickle
import base64
import gettext
import keyring
import threading
import flet as ft
from i18n import *
from utils import *
from pages.home import *
from pathlib import Path
from pages.exams import *
from pages.grades import *
from pages.homework import *
from pages.settings import *
from pages.timetable import *
from pages.behaviour import *
from pages.attendance import *
from sdk.src.interfaces.prometheus.context import *
from sdk.src.interfaces.prometheus.interface import *

def sync():
    auth_context_raw = loadauth("Fuji", "Auth Context")
    auth_context = PrometheusAuthContext.model_validate_json(auth_context_raw)
    
    interface = PrometheusInterface(
            auth_context=auth_context,
            student_context=None,
        )
    
    try:
        interface.login()
    
    except NoLoggedInException:
        print("NoLoggedInException, or in other words, vulcan shitted itself.")
        
    
    students = interface.get_students()
    
    student = int(keyring.get_password("Fuji", "Student_Index"))
    interface.select_student(students[student].context)
    
    auth_context = interface.get_auth_context()
    jsoncontext = auth_context.model_dump_json()
    saveauth("Fuji", "Auth Context", jsoncontext)

def main(page: ft.Page):
    # Page settings
    page.title = "Fuji"
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.RED,
        font_family="Roboto",
        page_transitions=ft.PageTransitionsTheme(
            macos=ft.PageTransitionTheme.NONE,
            linux=ft.PageTransitionTheme.NONE,
            windows=ft.PageTransitionTheme.NONE
        )
    )
    
    # Sync 
    s = threading.Thread(target=sync)
    s.start()
    
    # Page routing
    def change_page(route):
        routes = {
            "/": HomePage(),
            "/grades": GradesPage(),
            "/timetable": TimetablePage(),
            "/homework": HomeworkPage(),
            "/exams": ExamsPage(),
            "/attendance": AttendancePage(),
            "/behaviour": BehaviourPage(),
            "/settings": SettingsPage()
        }
        page.views.clear()
        page.views.append(ft.View(route, [
            ft.Row([
                bar,
                ft.Container(content=routes.get(route, HomePage()), expand=True)
            ], expand=True)
        ]))
        page.update()
    
    def on_route_change(e):
        change_page(e.route)

    # Navigation bar
    bar = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        extended=False,
        min_width=50,
        min_extended_width=400,
        group_alignment=0,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label=(_("Home"))),
            ft.NavigationRailDestination(icon=ft.Icons.LOOKS_6_OUTLINED, selected_icon=ft.Icons.LOOKS_6, label=(_("Grades"))),
            ft.NavigationRailDestination(icon=ft.Icons.BACKPACK_OUTLINED, selected_icon=ft.Icons.BACKPACK, label=(_("Timetable"))),
            ft.NavigationRailDestination(icon=ft.Icons.BOOK_OUTLINED, selected_icon=ft.Icons.BOOK, label=(_("Homework"))),
            ft.NavigationRailDestination(icon=ft.Icons.CALENDAR_TODAY_OUTLINED, selected_icon=ft.Icons.CALENDAR_TODAY, label=(_("Exams"))),
            ft.NavigationRailDestination(icon=ft.Icons.EVENT_NOTE_OUTLINED, selected_icon=ft.Icons.EVENT_NOTE, label=(_("Attendance"))),
            ft.NavigationRailDestination(icon=ft.Icons.STICKY_NOTE_2_OUTLINED, selected_icon=ft.Icons.STICKY_NOTE_2, label=(_("Behaviour"))),
            ft.NavigationRailDestination(icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icons.SETTINGS_ROUNDED, label=(_("Settings"))),
        ],
        on_change=lambda e: page.go([
            "/",
            "/grades",
            "/timetable",
            "/homework",
            "/exams",
            "/attendance",
            "/behaviour",
            "/settings"
        ][e.control.selected_index])
    )

    page.on_route_change = on_route_change
    page.go("/")


def login(page: ft.Page):
    # Page settings
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
    
    # Saving credentials
    def changeusr(e):
        global usr
        
        data["usr"] = e.control.value
        #print(usr)

    def changepasswd(e):
        global passwd
        
        data["passwd"] = e.control.value
        #print(passwd)
    
    # Login event
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
    
    # Students fetching, dropdown and selection
    def students():
        global interface
        
        students = interface.get_students()
        
        def on_change(e):
            selected_index = next((i for i, student in enumerate(students) if student.full_name == e.control.value), -1)
            
            interface.select_student(students[selected_index].context)
            keyring.set_password("Fuji", "Student_Index", str(selected_index))
            
            
            auth_context = interface.get_auth_context()
            jsoncontext = auth_context.model_dump_json()
            
            saveauth("Fuji", "Auth Context", jsoncontext)
            
            config = {"isLoggedIn": True, "lang": "pl"}
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
                
            
    # Page routing
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
                                ft.Text(value=(_("Welcome to Fuji!")), size=64),
                                ft.Button(
                                    (_("Get Started")), 
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
                                ft.Text(value=(_("Log in")), size=32, weight="bold", 
                                       text_align=ft.TextAlign.CENTER),
                                
                                ft.TextField(
                                    label=(_("Username")),
                                    autofill_hints=[ft.AutofillHint.USERNAME],
                                    width=300,
                                    on_change=changeusr
                                ),
                                
                                ft.TextField(
                                    label=(_("Password")),
                                    password=True,
                                    can_reveal_password=True,
                                    autofill_hints=[ft.AutofillHint.PASSWORD],
                                    width=300,
                                    on_change=changepasswd
                                ),
                                
                                ft.Button((_("Log in")), scale=1.25, width=250, on_click=loginev),
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
                                ft.Text(value=(_("Select a student")), size=32, weight="bold", 
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
        
        # Start view
        elif page.route == "/start":
            start_view = ft.View(
                route="/start",
                controls=[
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(value=(_("Logged in!")), size=32, weight="bold", 
                                       text_align=ft.TextAlign.CENTER),
                                
                                ft.Text(value=(_("Please restart the app to use it.")), size=16, weight="normal", 
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


# App configuration
if __name__ == "__main__":
    try:
        with open("config.json", "r") as file:
            data = json.load(file)
        if data.get("isLoggedIn", False):
            ft.app(target=main)
        else:
            ft.app(target=login)
    except FileNotFoundError:
        config = {"isLoggedIn": False, "lang": "pl"}
        with open("config.json", "w") as file:
            json.dump(config, file)
        ft.app(target=login)