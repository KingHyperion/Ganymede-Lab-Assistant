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

def get_projects_using_item(item_name): # Helper, finds which projects use an inventory item
    using_projects = [p['name'] for p in projects if item_name in p.get('supplies', [])]
    return ", ".join(using_projects) if using_projects else "None"

def handle_ollama_chat(user_message, chat_container, input_field): # Handles Ollama chat
    if not user_message.value.strip():
        return
    prompt = user_message.value
    input_field.value = ""
    with chat_container:
        ui.chat_message(prompt, name='You', sent=True)
        loading_msg = ui.chat_message("Thinking...", name='Qwen 3.5 (9B)', sent=False)
    try:
        response = ollama.chat(model='qwen3.5:9b', messages=[{'role': 'user', 'content': prompt}])
        loading_msg.delete()
        with chat_container:
            ui.chat_message(response['message']['content'], name='Qwen 3.5 (9B)', sent=False)
    except Exception as e:
        loading_msg.delete()
        with chat_container:
            ui.chat_message(f"Error connecting to Ollama: {e}. Is ollama running?", name='System', sent=False)