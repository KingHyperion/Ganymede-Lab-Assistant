from nicegui import ui
from inventory import inventory, units
from helpers import format_quantity, get_projects_using_item, add_new_inventory_item, get_all_tags, get_unit, add_new_unit, get_item_categories, get_item_bins, get_item_by_id, update_inventory_item, delete_inventory_item, refresh_all

def render_inventory_tab(refreshers):
    ui.label('Workshop Inventory & Resources').classes('text-2xl font-bold mb-4')

    editing = {'id': None}
    stock_values = []

    with ui.row().classes('w-full items-center justify-between mb-4 gap-4'):
        search_query = ui.input(placeholder='Search by name, category, bin, project, or tags...').props('dark input-class="text-white')
        ui.button('Add item', icon='add', on_click=lambda: open_add_dialog()).classes('bg-purple-600 text-white')

    table_columns = [
        {'name': 'name', 'label': 'Item Description', 'field': 'name', 'align': 'left'},
        {'name': 'category', 'label': 'Category', 'field': 'category'},
        {'name': 'qty', 'label': 'Quantity / Status', 'field': 'formatted_qty'},
        {'name': 'tags', 'label': 'Tags', 'field': 'tags_str'},
        {'name': 'used_in', 'label': 'Used In Projects', 'field': 'used_in_str'},
        {'name': 'bin', 'label': 'Storage Bin', 'field': 'bin'},
        {'name': 'actions', 'label': '', 'field': 'actions'},
    ]

    inv_table = ui.table(columns=table_columns, rows=[], row_key='id').classes('bg-gray-800 text-white w-full')
    inv_table.add_slot('body-cell-actions', r'''
        <q-td :props="props">
            <q-btn flat dense color="purple-3" icon="edit" @click="() => $parent.$emit('edit', props.row.id)" />
        </q-td>
    ''')
    inv_table.on('edit', lambda e: open_edit_dialog(e.args))

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
    refreshers.append(refresh_table)

    with ui.dialog() as add_dialog, ui.card().classes('bg-gray-800 text-white p-6 w-[450px]'):
        dialog_title = ui.input(label='Item Description / Name').props('dark').classes('w-full mb-2')
        cat_input = ui.select(
            label='Category (type a new one and press Enter)',
            options=get_item_categories(),
            new_value_mode='add-unique',
            with_input=True,
            value=None
        ).props('dark').classes('w-full mb-2')

        with ui.row().classes('w-full items-center gap-2 mb-2'):
            unit_input = ui.select(label='Unit (optional)', options=[u['name'] for u in units], value=None).props('dark clearable').classes('flex-grow')
            ui.button(icon='add', on_click=lambda: unit_dialog.open()).props('flat dense').classes('text-purple-300')

        ui.label('Stock').classes('text-sm text-gray-300')
        stock_container = ui.column().classes('w-full gap-1')

        def get_stock_label(index):
            unit = get_unit(unit_input.value)
            base = f'Quantity ({unit["measure"]})' if (unit and unit['measure']) else 'Quantity'
            if len(stock_values) > 1:
                return f'{base} #{index + 1}'
            return base

        def set_stock_value(index, value):
            if index < len(stock_values):
                stock_values[index] = value

        def add_stock_entry():
            stock_values.append(None)
            render_stock_rows()

        def remove_stock_entry(index):
            stock_values.pop(index)
            render_stock_rows()

        def render_stock_rows():
            stock_container.clear()
            with stock_container:
                for index, value in enumerate(stock_values):
                    with ui.row().classes('w-full items-center gap-2'):
                        box = ui.number(label=get_stock_label(index), value=value).props('dark').classes('flex-grow')
                        box.on_value_change(lambda e, i=index: set_stock_value(i, e.value))
                        if len(stock_values) > 1:
                            ui.button(icon='close', on_click=lambda i=index: remove_stock_entry(i)).props('flat dense round').classes('text-red-300')
                    
        ui.button('Add entry', icon='add', on_click=add_stock_entry).props('flat dense').classes('text-purple-300 mb-2')
        unit_input.on_value_change(render_stock_rows)

        bin_input = ui.select(
            label='Storage Bin (type a new one and press Enter)',
            options=get_item_bins(),
            new_value_mode='add-unique',
            with_input=True,
            value=None
        ).props('dark').classes('w-full mb-2')

        tags_input = ui.select(
            label='Tags (type a new one and press Enter)',
            options=get_all_tags(),
            multiple=True,
            new_value_mode='add-unique',
            with_input=True,
            value=[]
        ).props('dark use-chips').classes('w-full mb-4')