import io
import json
from typing import Dict

def records_data_to_json(records, selected_column_ids = []):
    formatted_records = []
    for record in records:
        formatted = {
            "id": record["id"]
        }
        cells = record["cells"]
        for cell in cells:
            if cell["columnId"] in selected_column_ids or len(selected_column_ids) == 0:
                value = ''
                if "value" in cell:
                    value = cell["value"]
                formatted[cell["columnId"]] = value
        formatted_records.append(formatted)
    return formatted_records
    
def save_file(text, file_path):
    with io.open(file_path, 'w', encoding='utf8') as f:
        f.write(text)

def dump_to_json_file(file_path, obj: Dict):
    text = json.dumps(obj, indent=4, ensure_ascii=False)
    save_file(text, file_path)

def dump_to_csv_file(file_path, records: Dict):
    DELIMITER = ','
    lines = []
    cols = []

    if len(records) > 0:
        for col in records[0]:
            cols.append(f'{col}')
        lines.append(DELIMITER.join(cols))
        for record in records:
            values = []
            for col in record:
                values.append(f'{record[col]}')
            lines.append(DELIMITER.join(values))
        
    text = '\n'.join(lines)
    save_file(text, file_path)
