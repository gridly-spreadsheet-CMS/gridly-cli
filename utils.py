import io
import json
from tkinter import filedialog
from tkinter import *
from typing import Dict

def select_file(default_file_name):
    root = Tk()
    root.filename = filedialog.asksaveasfilename(initialdir = "/", initialfile = default_file_name,title = "Save file",filetypes = (("json files","*.json"),("all files","*.*")))
    return root.filename

def save_file(text, file_path):
    with io.open(file_path, 'w', encoding='utf8') as f:
        f.write(text)

def dump_to_json_file(file_path, obj: Dict):
    text = json.dumps(obj, indent=4)
    save_file(text, file_path)