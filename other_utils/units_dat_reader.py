import json
import argparse
from pathlib import Path
from typing import Dict, Any, List

UNITS_DAT_MAPPING = {
    # === Vanilla fields ===
    0: "Flingy",
    1: "Subunit",
    2: "Subunit 2",
    3: "Infestation",
    4: "Construction image",
    5: "Direction",
    6: "Has shields",
    7: "Shields",
    8: "Hitpoints",
    9: "Elevation level",
    10: "Floating",
    11: "Rank",
    12: "Ai idle order",
    13: "Human idle order",
    14: "Return to idle order",
    15: "Attack unit order",
    16: "Attack move order",
    17: "Ground weapon",
    18: "Ground weapon hits",
    19: "Air weapon",
    20: "Air weapon hits",
    21: "AI flags",
    22: "Flags",
    23: "Target acquisition range",
    24: "Sight range",
    25: "Armor upgrade",
    26: "Armor type",
    27: "Armor",
    28: "Rclick action",
    29: "Ready sound",
    30: "First what sound",
    31: "Last what sound",
    32: "First annoyed sound",
    33: "Last annoyed sound",
    34: "First yes sound",
    35: "Last yes sound",
    36: "Placement box",
    37: "Addon position",
    38: "Dimension box",
    39: "Portrait",
    40: "Mineral cost",
    41: "Gas cost",
    42: "Build time",
    43: "Datreq offset",
    44: "Group flags",
    45: "Supply provided",
    46: "Supply cost",
    47: "Space required",
    48: "Space provided",
    49: "Build score",
    50: "Kill score",
    51: "Map label",
    52: "???",
    53: "Misc flags",
    # === Extended fields ===
    64: "Dat requirement buffer",
    65: "Wireframe mode",
    66: "Wireframe ID",
    67: "Icon ID",
    68: "Buttons",
    69: "Linked Buttons Unit",
    70: "Speed multiplier",
    71: "Ext flags",
    72: "Turret max angle",
    73: "Bunker range bonus",
    74: "Death timer",
    75: "Alternate rank string",
    76: "Max energy",
    77: "Infestation HP percentage",
    78: "AI Building guards",
    83: "Cloak tech",
    84: "Cloak energy regen (usually degen so negative)",
    85: "Ext flags 2 (AI-related)",
}

def translate_data(data: List[Dict[str, Any]], mapping: Dict[int, str]) -> List[Dict[str, Any]]:
    translated_list = []
    for entry in data:
        original_data = entry.get("data", {})
        translated_data = {}
        for key, value in original_data.items():
            if key.startswith("field_"):
                try:
                    field_id = int(key.split('_')[1])
                    new_key = mapping.get(field_id, key)
                    translated_data[new_key] = value
                except (ValueError, IndexError):
                    translated_data[key] = value
            else:
                translated_data[key] = value
        
        translated_list.append({
            "index": entry.get("index"),
            "data": translated_data
        })
        
    return translated_list

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dat", type=Path, help="Path to text file with copied unit DAT values", default="./input.txt")
    
    args = parser.parse_args()

    if not args.input_dat.is_file(): #TODO test on Linux
        print(f"File does not exist: {args.input_dat}")
        

    try:
        with open(args.input_dat, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
        
        translated_output = translate_data(input_data, UNITS_DAT_MAPPING)
        
        print(json.dumps(translated_output, indent=2, ensure_ascii=False))

    except json.JSONDecodeError as json_e:
        print(json_e)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()