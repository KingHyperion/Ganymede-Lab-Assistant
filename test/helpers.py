import uuid
from inventory import inventory, projects, units, available_tags, save_data

def new_id():
    return uuid.uuid4().hex[:8]

def get_unit(unit_name):
    for u in units:
        if u['name'].lower() == (unit_name or '').lower():
            return u
    return None

def format_quantity(item):
    stock = item.get("stock", [])
    unit = get_unit(item.get("unit", ""))
    if unit is None:
        text = ", ".join(str(n) for n in stock) or "0"
        if len(stock) > 1:
            text += f" ({len(stock)} units)"
        return text
    total = sum(stock)
    if unit['individual']:
        return f"{total}{unit['measure']} total ({len(stock)} {unit['name']})"
    return f"{total} {unit['measure']}".strip()

def get_projects_using_item(item_id):
    using_projects = [p['name'] for p in projects if item_id in p.get('supplies', [])]
    return ", ".join(using_projects) if using_projects else "None"

def get_item_name(item_id):
    for item in inventory:
        if item['id'] == item_id:
            return item['name']
    return "Unownk item"

def get_all_tags():
    tags = set(available_tags)
    for item in inventory:
        tags.update(item.get('tags', []))
    return sorted(tags)

def add_new_unit(name, measure, individual):
    new_unit = {
        "name": name,
        "measure": (measure or '').strip(),
        "individual": bool(individual)
    }
    units.append(new_unit)
    save_data()
    return new_unit

def add_new_inventory_item(name, category, qty, unit, bin_loc, tags):
    qty = qty or 0
    if float(qty).is_integer():
        qty = int(qty)
    new_item = {
        "id": new_id(),
        "name": name,
        "category": category,
        "unit": unit,
        "stock": [qty],
        "tags": list(tags),
        "bin": bin_loc
    }
    inventory.append(new_item)
    save_data()
    return new_item