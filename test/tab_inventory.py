from nicegui import ui
from inventory import inventory, available_units
from helpers import format_quantity, get_projects_using_item, add_new_inventory_item, get_all_tags

def render_inventory_tab():
    ui.label('Workshop Inventory & Resources').classes('text-2xl font-bold mb-4')