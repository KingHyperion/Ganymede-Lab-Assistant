from nicegui import ui
from inventory import inventory, units
from helpers import format_quantity, get_projects_using_item, add_new_inventory_item, get_all_tags, get_unit, add_new_unit

def render_inventory_tab():
    ui.label('Workshop Inventory & Resources').classes('text-2xl font-bold mb-4')

    with ui.row().classes('w-full items-center justify-between mb-4 gap-4'):
        search_query = ui.input(placeholder='Search by name, category, bin, project, or tags...').props('dark input-class="text-white"')
        ui.button('Add Item', icon='add', on_click=lambda: add_dialog.open()).classes('bg-purple-600 text-white')

    table_columns = [
        {'name': 'name', 'label': 'Item Description', 'field': 'name', 'align': 'left'},
        {'name': 'category', 'label': 'Category', 'field': 'category'},
        {'name': 'qty', 'label': 'Quantity / Status', 'field': 'formatted_qty'},
        {'name': 'tags', 'label': 'Tags', 'field': 'tags_str'},
        {'name': 'used_in', 'label': 'Used In Projects', 'field': 'used_in_str'},
        {'name': 'bin', 'label': 'Storage Bin', 'field': 'bin'},
    ]

    inv_table = ui.table(columns=table_columns, rows=[], row_key='id').classes('bg-gray-800 text-white w-full')

    def refresh_table():
        query = search_query.value.lower() if (search_query and search_query.value) else ''

        table_rows = []
        for item in inventory:
            r = item.copy()
            r['formatted_qty'] = format_quantity(item)
            r['tags_str'] = ", ".join(item.get('tags', []))
            r['used_in_str'] = get_projects_using_item(item['id'])
            table_rows.append(r)

        if not query:
            filtered = table_rows
        else:
            filtered = []
            for item in table_rows:
                tags_list = item.get('tags', [])
                tag_match = any(query in tag.lower() for tag in tags_list)

                if (
                    query in item.get('name', '').lower() or
                    query in item.get('category', '').lower() or
                    query in item.get('bin', '').lower() or
                    query in item['used_in_str'].lower() or
                    tag_match
                ):
                    filtered.append(item)

        inv_table.rows = filtered
        inv_table.update()

    search_query.on('update:model-value', refresh_table)

    with ui.dialog() as add_dialog, ui.card().classes('bg-gray-800 text-white p-6 w-[450px]'):
        ui.label('Add New Inventory Item').classes('text-xl font-bold text-purple-300 mb-4')

        name_input = ui.input(label='Item Description / Name').props('dark').classes('w-full mb-2')
        cat_input = ui.input(label='Category').props('dark').classes('w-full mb-2')

        with ui.row().classes('w-full items-center gap-2 mb-2'):
            qty_input = ui.number(label='Quantity', value=1).props('dark').classes('flex-grow')
            unit_input = ui.select(label='Unit (optional)', options=[u['name'] for u in units], value=None).props('dark clearable').classes('w-40')
            ui.button(icon='add', on_click=lambda: unit_dialog.open()).props('flat dense').classes('text-purple-300')

        def update_qty_label():
            unit = get_unit(unit_input.value)
            label = f'Quantity ({unit["measure"]})' if (unit and unit['measure']) else 'Quantity'
            qty_input.props(f'label="{label}"')

        unit_input.on_value_change(update_qty_label)
        update_qty_label()

        bin_input = ui.input(label='Storage Bin').props('dark').classes('w-full mb-2')
        tags_input = ui.select(
            label='Tags (type a new one and press Enter)',
            options=get_all_tags(),
            multiple=True,
            new_value_mode='add-unique',
            with_input=True,
            value=[]
        ).props('dark use-chips').classes('w-full mb-4')

        def save_new_item():
            if not name_input.value:
                ui.notify('Item name is required!', color='negative')
                return
            add_new_inventory_item(
                name=name_input.value,
                category=cat_input.value,
                qty=qty_input.value,
                unit=unit_input.value,
                bin_loc=bin_input.value,
                tags=tags_input.value
            )
            ui.notify(f"Added {name_input.value}!", color='positive')
            refresh_table()
            add_dialog.close()

            name_input.value = ''
            cat_input.value =''
            qty_input.value = 1
            bin_input.value = ''
            tags_input.set_options(get_all_tags(), value=[])

        with ui.row().classes('w-full justify-end gap-2 mt-4'):
            ui.button('Cancel', on_click=add_dialog.close).props('flat').classes('text-gray-400')
            ui.button('Save Item', on_click=save_new_item).classes('bg-purple-600 text-white')

    with ui.dialog() as unit_dialog, ui.card().classes('bg-gray-800 text-white p-6 w-[400px]'):
        ui.label('New Unit').classes('text-xl font-bold text-purple-300 mb-4')

        new_unit_name = ui.input(label='Unit name (e.g. spools, meters)').props('dark').classes('w-full mb-2')
        new_unit_measure = ui.input(label='Measure (e.g. g, mL, m) - optional').props('dark').classes('w-full mb-2')
        new_unit_individual = ui.checkbox('Track each entry separately (like spools or bottles)').classes('mb-4')

        def save_new_unit():
            name = (new_unit_name.vlaue or '').strip()
            if not name:
                ui.notify('Unit name is required!', color='negative')
                return
            if get_unit(name):
                ui.notify('That unit already exists!', color='negative')
                return
            add_new_unit(name, new_unit_measure.value, new_unit_individual.value)
            unit_input.set_options([u['name'] for u in units], value=name)
            ui.notify(f'Added unit {name}!', color='positive')
            unit_dialog.close()

            new_unit_name.value = ''
            new_unit_measure.value = ''
            new_unit_individual.value = False

        with ui.row().classes('w-full justify-end gap-2 mt-4'):
            ui.button('Cancel', on_click=unit_dialog.close).props('flat').classes('text-gray-400')
            ui.button('Save Unit', on_click=save_new_unit).classes('bg-purple-600 text-white')

    refresh_table()

    return refresh_table