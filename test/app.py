from nicegui import ui
from tab_inventory import render_inventory_tab
from tab_projects import render_projects_tab

ui.colors(primary='#a78bfa')

with ui.header().classes('bg-gray-900 text-white items-center justify-between px-6'):
    ui.label('Maker Lab Hub & Assistant').classes('text-xl font-bold')

with ui.tabs().classes('w-full bg-gray-800 text-white') as tabs:
    inv_tab = ui.tab('Inventory', icon='inventory')
    proj_tab = ui.tab('Project Hub', icon='build')

with ui.tab_panels(tabs, value=inv_tab).classes('w-full p-6 bg-gray-900 text-white min-h-[80vh]'):
    with ui.tab_panel(inv_tab):
        refresh_inventory = render_inventory_tab()

    with ui.tab_panel(proj_tab):
        render_projects_tab(refresh_inventory)

ui.run(port=8080, reload=True)