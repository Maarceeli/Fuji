import flet as ft
from i18n import _
from sqlitehandlernr import fetch_all_notes


def BehaviourPage():
    notes = fetch_all_notes()
    
    if not notes:
        return ft.Container(
                content=ft.Row([ft.Text(_("No notes yet"), size=20, color=ft.Colors.WHITE)]),
                expand=True, 
                alignment=ft.alignment.center,  # Correct alignment
            )

    
    notes_cards = []
    
    for note in notes:
        notes_cards.append(
            ft.Card(
                content=ft.Container(
                    content=
                        ft.Column([
                            ft.Row([             
                                ft.Text(note.name, size=20, color=ft.Colors.WHITE),
                                ft.Chip(label=ft.Text(note.points))
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Row([
                                ft.Text(note.content, size=14, color=ft.Colors.WHITE70, overflow=ft.TextOverflow.FADE, width=800),
                            ], expand=True),
                            ft.Row([
                                ft.Text(note.created_at.strftime("%Y/%m/%d"), size=14, color=ft.Colors.WHITE70),
                                ft.Text(note.creator, size=14, color=ft.Colors.WHITE70),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        ]),
                    padding=10,
                    expand=True,
                ),
            )
        )
    
    return ft.Column([
                ft.Text((_("Behaviour")), size=30, weight="bold"),
                ft.ListView(
                            controls=[
                                ft.Column(
                                    notes_cards[::-1]
                                )
                            ],
                            expand=True,
                            spacing=10,
                            padding=10,
                            auto_scroll=False
                        ),
            ])
        
        