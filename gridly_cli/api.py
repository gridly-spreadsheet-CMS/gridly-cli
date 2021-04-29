import requests
import os
import time
from typing import Dict

api_key = str(os.environ["GRIDLY_API_KEY"])

MAX_RETRY = 3
HTTP_STATUS = {
    'OK': 200,
    'NOT_FOUND': 404
}

def _records_data_to_json(records, selected_column_ids):
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

def split_column(records: Dict, column_id):
    list = []
    for record in records:
        if column_id in record:
            list.append({
                "id": record["id"],
                column_id: record[column_id]
            })
    return list

def get(url, retry_times = 0):
    headers = {'Authorization': f'ApiKey {api_key}', 'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    if response.status_code == HTTP_STATUS['OK']:
      return response
    elif retry_times < MAX_RETRY:
      time.sleep(1)
      return get(url, retry_times + 1)
    else:
      print(f'!!! FAILED to request {url}. Details: {response.status_code} - {response.text}')
      return None

def get_records(view_id, selected_column_ids = []):
    url = f'https://api.gridly.com/v1/views/{view_id}/records'
    records = []
    while len(url) > 0:
        response = get(url)
        if response is not None:
            records = records + _records_data_to_json(response.json(), selected_column_ids)

            if 'Link' in response.headers and 'next' in response.links:
              url = response.links['next']['url']
            else:
              url = ''
        else:
          url = ''
    return records

def get_view(view_id):
    url = f'https://api.gridly.com/v1/views/{view_id}'
    response = get(url)
    return response.json()
