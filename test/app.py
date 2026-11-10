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

with ui.tab_panels(tabs, value=inv_tab).classes('w-full p-6 bg-gray-900 text-white min-h-[80vh]'):

    with ui.tab_panel(inv_tab): # Tab 1: Inventory
        ui.label('Workshop Inventory & Resources').classes('text-2xl font-bold mb-4')

        search_query = ui.input(placeholder='Search by name, category, or tags...').classes('bg-gray-800 text-white w-full mb-4')

        table_rows = []
        for item in inventory:
            r = item.copy()
            r['formatted_qty'] = format_quantity(item)
            r['tags_str'] = ", ".join(item.get('tags', []))
            r['used_in_str'] = get_projects_using_item(item['name'])
            table_rows.append(r)

        table_columns = [
            {'name': 'name', 'label': 'Item Description', 'field': 'name', 'align': 'left'},
            {'name': 'category', 'label': 'Category', 'field': 'category'},
            {'name': 'qty', 'label': 'Quantity / Status', 'field': 'formatted_qty'},
            {'name': 'tags', 'label': 'Tags', 'field': 'tags_str'},
            {'name': 'used_in', 'label': 'Used In Projects', 'field': 'used_in_str'},
            {'name': 'bin', 'label': 'Storage Bin', 'field': 'bin'},
        ]

        inv_table = ui.table(columns=table_columns, rows=table_rows).classes('bg-gray-800 text-white w-full')

        def filter_table():
            query = search_query.value.lower()
            filtered = [
                item for item in table_rows
                if query in item['name'].lower() or 
                   query in item['category'].lower() or 
                   query in item['bin'].lower() or
                   query in item['used_in_str'].lower() or
                   any(query in tag.lower() for tag in item.get('tags', []))
            ]
            inv_table.rows = filtered
            inv_table.update()

        search_query.on('update:model-value', filter_table)

    with ui.tab_panel(proj_tab): # Tab 2: Project Hub
        ui.label('Project Hub & Hackatime Stats').classes('text-2xl font-bold mb-4')
        with ui.row().classes('gap-4'):
            for p in projects:
                with ui.card().classes('bg-gray-800 p-5 w-96 text-white'):
                    ui.label(p['name']).classes('text-xl font-bold text-purple-400')
                    ui.separator().classes('my-2')
                    ui.label(f"Category: {p['category']}").classes('text-sm text-gray-300')
                    ui.label(f"Status: {p['status']}").classes('text-sm text-gray-300')

                    ui.label("Required Supplies:").classes('text-sm font-bold text-purple-300 mt-3')
                    with ui.column().classes('pl-2 gap-1'):
                        for supply in p.get('supplies', []):
                            ui.label(f"- {supply}").classes('text-xs text-gray-300')

                    with ui.row().classes('mt-4 bg-gray-900 p-2 rounded items-center gap-2'):
                        ui.icon('code', color='purple')
                        ui.label(p['hackatime_stats']).classes('text-xs text-purple-300 font-mono')


ui.run(port=8080, reload=True)