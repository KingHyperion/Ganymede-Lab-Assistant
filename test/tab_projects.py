from nicegui import ui
from inventory import projects, project_statuses, project_categories
from helpers import get_item_name, get_all_tags, get_supply_options, get_project_categories, add_new_project

def render_projects_tab(on_projects_changed=None):
    ui.label('Project Hub & hackatime Stats').classes('text-2xl font-bold mb-4')

    ui.button('Add Project', icon='add', on_click=lambda: open_add_dialog()).classes('bg-purple-600 text-white mb-4')

    cards_container = ui.row().classes('gap-4')

    def refresh_cards():
        cards_container.clear()
        with cards_container:
            for p in projects:
                with ui.card().classes('bg-gray-800 p-5 w-96 text-white'):
                    ui.label(p['name']).classes('text-xl font-bold text-purple-400')
                    ui.separator().classes('my-2')
                    ui.label(f"Category: {p.get('category', "")}").classes('text-sm text-gray-300')
                    ui.label(f"Status: {p.get('status', '')}").classes('test-sm text-gray-300')

                    if p.get('tags'):
                        ui.label(f"Tags: {', '.join(p['tags'])}").classes('text-sm text-gray-300')
                    
                    ui.label("Required Suplies:").classes('text-sm font-bold text-purple-300 mt-3')
                    with ui.column().classes('pl-2 gap-1'):
                        for supply_id in p.get('supplies', []):
                            ui.label(f"- {get_item_name(supply_id)}").classes('text-xs text-gray-300')

                    with ui.row().classes('mt-4 bg-gray-900 p-2 rounded itemscenter gap-2'):
                        ui.icon('code', color='purple')
                        ui.label('Hackatime: not connected yet').classes('text-xs text-purple-300 fonto-mono')

    with ui.dialog() as add_dialog, ui.card().classes('bg-gray-800 text-white p-6 w-[450pc]'):
        ui.label('Add New Project').classes('text-xl font-bold text-purple-300 mb-4')

        name_input = ui.input(label='Project Name').props('dark').classes('w-full mb-2')

        with ui.row().classes('w-full gap-2 mb-2'):
            category_input = ui.select(
                label='Category (type a new one and press Enter)',
                options=get_project_categories(),
                new_value_mode='add-unique',
                with_input=True,
                value=project_categories[0]
            ).props('dark').classes('flex-grow')
            status_input = ui.select(label='Status', options=project_statuses, value=project_statuses[0]).props('dark').classes('w-40')

        supplies_input = ui.select(
            label='Supplies (from inventory)',
            options=get_supply_options(),
            multiple=True,
            with_input=True,
            value=[]
        ).props('dark use-chips').classes('w-full mb-2')

        tags_input = ui.select(
            label='Tags (type a new one and press Enter)',
            options=get_all_tags(),
            multiple=True,
            new_value_mode='add-unique',
            with_input=True,
            value=[]
        ).props('dark use-chips').classes('w-full mb-4')

        def save_new_project():
            if not name_input.value:
                ui.notify('Project name is required!', color='negative')
                return
            add_new_project(
                name=name_input.value,
                category=category_input.value,
                status=status_input.value,
                supplies=supplies_input.value,
                tags=tags_input.value
            )
            ui.notify(f"Added {name_input.value}!", color='positive')
            refresh_cards()
            if on_projects_changed:
                on_projects_changed()
            add_dialog.close()

            name_input.value = ''
            category_input.value = project_categories[0]
            status_input.value = project_statuses[0]
            supplies_input.value = []
            tags_input.value = []

        with ui.row().classes('w-full justify-end gap-2 mt-4'):
            ui.button('Cancel', on_click=add_dialog.close).props('flat').classes('text-gray-400')
            ui.button('Save Project', on_click=save_new_project).classes('bg-purple-600 text-white')

    def open_add_dialog():
        category_input.set_options(get_project_categories())
        supplies_input.set_options(get_supply_options())
        tags_input.set_options(get_all_tags())
        add_dialog.open()

    refresh_cards()