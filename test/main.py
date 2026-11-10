from nicegui import ui
import ollama

from inventory import inventory, projects, available_tags, available_units

def format_quantity(item): # Helper, grammatically formats inventory item as per unit
    u = item.get("unit")
    if u == "count":
        return f"{item.get('qty', 0)} units"
    elif u == "spools":
        spools = item.get("spools", [])
        return f"{sum(spools)}g total, ({len(spools)} spools)"
    elif u == "bottles":
        bottles = item.get("bottles", [])
        return f"{sum(bottles)}mL total, ({len(bottles)} bottles)"
    return "Unknown"