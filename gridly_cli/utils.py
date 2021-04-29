import io
import json
from typing import Dict

def save_file(text, file_path):
    with io.open(file_path, 'w', encoding='utf8') as f:
        f.write(text)

def dump_to_json_file(file_path, obj: Dict):
    text = json.dumps(obj, indent=4)
    save_file(text, file_path)