from nicegui import ui
from inventory import projects, project_statuses, project_categories
from helpers import get_item_name, get_all_tags, get_supply_options, get_project_categories, add_new_project

def render_projects_tab(on_projects_changed=None):
    ui.label('Project Hub & hackatime Stats').classes('text-2xl font-bold mb-4')

    ui.button('Add Project', icon='add', on_click=lambda: open_add_dialog()).classes('bg-purple-600 text-white mb-4')