import flet as ft

def main(page: ft.Page):
    page.theme = ft.Theme(
    color_scheme_seed=ft.Colors.PINK,
    font_family="Roboto",
    page_transitions=ft.PageTransitionsTheme(
        macos=ft.PageTransitionTheme.NONE,
        linux=ft.PageTransitionTheme.NONE,
        windows=ft.PageTransitionTheme.NONE
    ),
    )
    page.theme_mode = ft.ThemeMode.DARK
    
    modal = ft.BottomSheet(
            content=ft.Column([
                ft.Row([
                    # Subject details
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Wychowanie fizyczne", size=30, weight=ft.FontWeight.BOLD),
                            ft.Text("rozgrzewka", size=18, color=ft.Colors.WHITE70),
                        ], spacing=3, tight=True),
                        padding=ft.padding.only(left=20, top=-20, bottom=5, right=20),
                        expand=True,
                    ),
                    
                    # Grade display
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Text("5", size=48, weight=ft.FontWeight.BOLD),
                                width=80,
                                height=80,
                                bgcolor=ft.Colors.GREEN_700,
                                border_radius=ft.border_radius.only(top_left=8, top_right=8),
                                alignment=ft.alignment.center,
                                margin=ft.margin.only(bottom=5, top=40)
                            ),
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(name=ft.Icons.SCALE, size=16),
                                    ft.Text("1.00", size=16),
                                ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                                width=80,
                                height=30,
                                bgcolor=ft.Colors.GREEN_700,
                                border_radius=ft.border_radius.only(bottom_left=8, bottom_right=8),
                                alignment=ft.alignment.center,
                            ),
                        ], spacing=0, alignment=ft.MainAxisAlignment.CENTER),
                        padding=ft.padding.only(right=20, top=-5, bottom=10),
                    ),   
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        
                
                # Grade details
                ft.Card(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Icon(name=ft.Icons.SCALE, size=20),
                            width=40,
                            height=40,
                            border_radius=8,
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(left=10),
                        ),
                        ft.Column([
                            ft.Text("Grade", size=14, color=ft.Colors.WHITE70),
                            ft.Text("5", size=20)
                        ], spacing=2, alignment=ft.MainAxisAlignment.CENTER, expand=True)
                    ], spacing=15, alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),  
                    height=75,
                    color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    margin=ft.margin.only(left=15, right=15, bottom=5),                    
                ),

                    
                # Weight details
                ft.Card(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Icon(name=ft.Icons.SCALE, size=20),
                            width=40,
                            height=40,
                            border_radius=8,
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(left=10),
                        ),
                        ft.Column([
                            ft.Text("Weight", size=14, color=ft.Colors.WHITE70),
                            ft.Text("1.00", size=20),
                        ], spacing=2, alignment=ft.MainAxisAlignment.CENTER, expand=True),  # Align and expand
                    ], spacing=15, alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    height=75,
                    color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    margin=ft.margin.only(left=15, right=15, top=5, bottom=5),
                ),

                # Date details
                ft.Card(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Icon(name=ft.Icons.CALENDAR_TODAY, size=20),
                            width=40,
                            height=40,
                            border_radius=8,
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(left=10),
                        ),
                        ft.Column([
                            ft.Text("Date", size=14, color=ft.Colors.WHITE70),
                            ft.Text("2/10/25", size=20),
                        ], spacing=2, alignment=ft.MainAxisAlignment.CENTER, expand=True),  # Align and expand
                    ], spacing=15, alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    height=75,
                    color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    margin=ft.margin.only(left=15, right=15, bottom=5, top=5),
                ),
 
                    
            ], spacing=5),
            enable_drag=True,
            open=True,
    )   
    
    # Add the modal directly to the page
    page.add(ft.ElevatedButton("Open Grade Details", on_click=lambda _: page.open(modal)))

ft.app(target=main)
