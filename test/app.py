from nicegui import ui

from inventory import inventory, projects, available_tags, available_units
from helpers import format_quantity, get_projects_using_item, handle_ollama_chat

ui.colors(primary='#a78bfa')

with ui.header().classes('bg-gray-900 text-white items-center justify-between px-6'):
    ui.label('Maker Lab Hub & Assistant').classes('text-xl font-bold')
    ui.label('Model: qwen3.5:9b | Engine: NiceGUI').classes('text-xs text-purple-300 bg-gray-800 px-3 py-1 rounded-full')

with ui.tabs().classes('w-full bg-gray-800 text-white') as tabs:
    inv_tab = ui.tab('Inventory', icon='inventory')
    proj_tab = ui.tab('Project Hub', icon='build')
    ai_tab = ui.tab('Ollama Chat', icon='smart_toy')
