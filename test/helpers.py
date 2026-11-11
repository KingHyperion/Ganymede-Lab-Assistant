import uuid
from inventory import inventory, projects, available_tags, save_data

def new_id():
    return uuid.uuid4().hex[:8]

def format_quantity(item):
    u = item.get("unit")
    stock = item.get("stock", [])
    if u == "count":
        return f"{sum(stock)} units"
    elif u == "spools":
        return f"{sum(stock)}g total ({len(stock)} spools)"
    elif u == "containers":
        return f"{sum(stock)}mL total ({len(stock)} bottles)"
    return "Unknown"

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