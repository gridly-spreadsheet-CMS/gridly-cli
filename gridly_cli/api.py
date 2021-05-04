import requests
import json
import os
import time
from typing import Dict

api_key = str(os.environ["GRIDLY_API_KEY"])

MAX_RETRY = 3
HTTP_STATUS = {
    'OK': 200,
    'NOT_FOUND': 404
}

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

def patch(url, data):
    headers = {'Authorization': f'ApiKey {api_key}', 'Content-Type': 'application/json'}
    response = requests.patch(url, headers=headers, data=json.dumps(data))

def delete(url, data):
    headers = {'Authorization': f'ApiKey {api_key}', 'Content-Type': 'application/json'}
    response = requests.delete(url, headers=headers, data=json.dumps(data))

def get_projects():
    url = 'https://api.gridly.com/v1/projects'
    response = get(url)
    return response.json()

def get_databases(project_id):
    url = f'https://api.gridly.com/v1/databases?projectId={project_id}'
    response = get(url)
    return response.json()

def get_grids(db_id):
    url = f'https://api.gridly.com/v1/grids?dbId={db_id}'
    response = get(url)
    return response.json()

def get_grid(grid_id):
    url = f'https://api.gridly.com/v1/grids/{grid_id}'
    response = get(url)
    return response.json()

def update_grid(grid_id, data):
    url = f'https://api.gridly.com/v1/grids/{grid_id}'
    response = patch(url, data)
    return response.json()

def get_views(grid_id):
    url = f'https://api.gridly.com/v1/views?gridId={grid_id}'
    response = get(url)
    return response.json()

def get_view(view_id):
    url = f'https://api.gridly.com/v1/views/{view_id}'
    response = get(url)
    return response.json()

def export_view(view_id):
    url =f'https://api.gridly.com/v1/views/{view_id}/export'
    response = get(url)
    return response

def get_records(view_id):
    url = f'https://api.gridly.com/v1/views/{view_id}/records'
    records = []
    while len(url) > 0:
        response = get(url)
        if response is not None:
            records = records + response.json()
            if 'Link' in response.headers and 'next' in response.links:
              url = response.links['next']['url']
            else:
              url = ''
        else:
          url = ''
    return records

def delete_records(view_id, data):
    url = f'https://api.gridly.com/v1/views/{view_id}/records'
    response = delete(url, data)
    return response
