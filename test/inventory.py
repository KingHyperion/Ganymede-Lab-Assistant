available_tags = ["rp2040", "rp2350", "wireless", "soldered", "pla", "bambu", "jumper-wires", "cleaning"]
available_units = ["count", "spools", "bottles"]

inventory = [
    {
        "name": "Pi Pico 2 (RP2350) - Wireless - Pre-soldered",
        "category": "Microcontrollers",
        "unit": "count",
        "qty": 4,
        "tags": ["rp2350", "wireless", "soldered"],
        "bin": "Pico Kit"
    },
    {
        "name": "PLA Filament - Bambu Labs - Matte Blue",
        "category": "Filament",
        "unit": "spools",
        "spools": [1000, 243],  
        "tags": ["pla", "bambu"],
        "bin": "Filament Box"
    },
    {
        "name": "Isopropyl Alcohol 99% (500ml bottle)",
        "category": "Chemicals & Liquids",
        "unit": "bottles",
        "bottles": [500, 250],  
        "tags": ["cleaning"],
        "bin": "Chemical Shelf"
    },
    {
        "name": "22awg Breadboard Jumper Wires",
        "category": "Wires",
        "unit": "count",
        "qty": 6,
        "tags": ["jumper-wires"],
        "bin": "Wire Box"
    },
]

projects = [
    {
        "name": "AI Spotlight", 
        "category": "Hardware", 
        "status": "In Progress", 
        "supplies": [
            "Pi Pico 2 (RP2350) - Wireless - Pre-soldered",
            "22awg Breadboard Jumper Wires"
        ],
        "hackatime_stats": "4h 15m coded today (MicroPython)"
    }
]