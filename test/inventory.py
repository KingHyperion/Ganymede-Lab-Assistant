import json
import os

data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")

available_tags = ["rp2040", "rp2350", "wireless", "soldered", "pla", "bambu", "jumper-wires", "cleaning"]
available_units = ["count", "spools", "bottles"]

inventory = []
projects = []

def load_data(path=data_file):
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    inventory.clear()
    inventory.extend(data.get("inventory", []))
    projects.clear()
    projects.extend(data.get("projects", []))

def save_data(path=data_file):
    data = {"inventory": inventory, "projects": projects}
    temp_path = path + ".tmp"
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(temp_path, path)

load_data()