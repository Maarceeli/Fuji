import flet as ft

class GradeBottomSheet(ft.BottomSheet):
        def __init__(self, GradeName, GradeDesc, GradeValue, GradeWeight, GradeDate, Teacher) -> None:
            icon = ft.Icons.FILTER_5
            if isinstance(GradeValue, (str, list)) and len(GradeValue) > 0:
                grade_value = GradeValue[0]
                
                if grade_value.isdigit():
                    grade = int(grade_value)
                    match grade:
                        case 1:
                            icon = ft.Icons.FILTER_1
                        case 2:
                            icon = ft.Icons.FILTER_2
                        case 3:
                            icon = ft.Icons.FILTER_3
                        case 4:
                            icon = ft.Icons.FILTER_4
                        case 5:
                            icon = ft.Icons.FILTER_5
                        case 6:
                            icon = ft.Icons.FILTER_6

            super().__init__(
                content=ft.Column([
                ft.Row([
                    # Subject details
                    ft.Container(
                        content=ft.Column([
                            ft.Text(GradeName, size=30, weight=ft.FontWeight.BOLD),
                            ft.Text(GradeDesc, size=18, color=ft.Colors.WHITE70),
                        ], spacing=3, tight=True),
                        padding=ft.padding.only(left=20, top=-20, bottom=5, right=20),
                        expand=True,
                    ),
                    
                    # Grade display
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Text(GradeValue, size=48, weight=ft.FontWeight.BOLD),
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
                                    ft.Text(GradeWeight, size=16),
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
                            content=ft.Icon(name=icon, size=20),
                            width=40,
                            height=40,
                            border_radius=8,
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(left=10),
                        ),
                        ft.Column([
                            ft.Text("Grade", size=14, color=ft.Colors.WHITE70),
                            ft.Text(GradeValue, size=20)
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
                            ft.Text(GradeWeight, size=20),
                        ], spacing=2, alignment=ft.MainAxisAlignment.CENTER, expand=True),  # Align and expand
                    ], spacing=15, alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    height=75,
                    color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    margin=ft.margin.only(left=15, right=15, top=5, bottom=5),
                ),

                # Teacher details
                ft.Card(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Icon(name=ft.Icons.PERSON_ROUNDED, size=20),
                            width=40,
                            height=40,
                            border_radius=8,
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(left=10),
                        ),
                        ft.Column([
                            ft.Text("Teacher", size=14, color=ft.Colors.WHITE70),
                            ft.Text(Teacher, size=20),
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
                            ft.Text(GradeDate, size=20),
                        ], spacing=2, alignment=ft.MainAxisAlignment.CENTER, expand=True),  # Align and expand
                    ], spacing=15, alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    height=75,
                    color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    margin=ft.margin.only(left=15, right=15, bottom=5, top=5),
                ),
 
                    
            ], spacing=5),
            enable_drag=True,
            open=False,
            )