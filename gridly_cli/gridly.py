import click
import requests
import os
import json
import questionary
from questionary import Separator, Choice, prompt
from tabulate import tabulate

import api
from utils import records_data_to_json, dump_to_json_file, dump_to_csv_file

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'ApiKey ' + str(os.environ["GRIDLY_API_KEY"])
}

@click.group()
def gridly():
    """A CLI wrapper for the API of Gridly."""
    pass

def choose_project():
    projects = api.get_projects()

    projectname = []
    projectid = ""
    for project in projects:
        projectname.append(project["name"])

    chosen_projectname = questionary.select(
    "Choose your Project:",
    choices=projectname).ask()

    for project in projects:
        if chosen_projectname == str(project["name"]):
            projectid = str(project["id"])
        else:
            continue
    return projectid

def choose_database():
    project_id = choose_project()
    databases = api.get_databases(project_id)

    databasename = []
    databaseid = ""
    for database in databases:
        databasename.append(database["name"])

    chosen_databasename = questionary.select(
    "Choose your Database:",
    choices=databasename).ask()

    for database in databases:
        if chosen_databasename == str(database["name"]):
            databaseid = str(database["id"])
        else:
            continue
    return databaseid

def choose_grid():
    db_id = choose_database()
    grids = api.get_grids(db_id)

    gridname = []
    gridid = ""
    for grid in grids:
        gridname.append(grid["name"])

    chosen_gridname = questionary.select(
    "Choose your Grid:",
    choices=gridname).ask()

    for grid in grids:
        if chosen_gridname == str(grid["name"]):
            gridid = str(grid["id"])
        else:
            continue
    return gridid

def choose_view():
    grid_id = choose_grid()
    views = api.get_views(grid_id)

    viewname = []
    viewid = ""
    for view in views:
        viewname.append(view["name"])

    chosen_viewname = questionary.select(
    "Choose your view:",
    choices=viewname).ask()

    for view in views:
        if chosen_viewname == str(view["name"]):
            viewid = str(view["id"])
        else:
            continue
    return viewid

def choose_columns(view_id):
    view = api.get_view(view_id)
    options = ['All']
    columns = view["columns"]
    for column in columns:
        options.append(column["id"])
    
    ls_chosen_columns = questionary.checkbox('Select columns to export', choices=options).ask()
    if 'All' in ls_chosen_columns:
        return options
    else:
        return ls_chosen_columns

####### Grid #######
@gridly.command()
@click.option('-ls', 'action', flag_value='ls', default=True, help='To list all Grids')
@click.option('-u', 'action', flag_value='u', help='To update Grid name')
def grid(action):
    """
        List all Grids / Update Grid name
    """
    if action == 'ls':
        db_id = choose_database()
        response = api.get_grids(db_id)
        for grid in response:
            click.echo(grid["name"])
    elif action == 'u':
        grid_id = choose_grid()

        grid_name = questionary.text("New Grid name:").ask()
        data = {
            "name": grid_name
        }
        api.update_grid(grid_id, data)

        click.echo("Your Grid has been changed")
    else: 
        gridly()

@gridly.command()
@click.option('-ls', 'action', flag_value='ls', default=True)
def project(action):
    """
        List all Projects
    """
    if action == 'ls':
        response = api.get_projects()
        for project in response:
            click.echo(project["name"])
    else: 
        gridly()

@gridly.command()
@click.option('-ls', 'action', flag_value='ls', default=True)
def database(action):
    """
        List all Databases
    """
    if action == 'ls':
        project_id = choose_project()
        response = api.get_databases(project_id)
        for database in response:
            click.echo(database["name"])
    else: 
        gridly()

@gridly.command()
@click.option('-ls', 'action', flag_value='ls', help='To list all views')
@click.option('-ex', 'action', flag_value='ex', help='To export a view to CSV file')
@click.argument('view_id', required=False)
def view(action, view_id):
    """
        List all views / Export a view to CSV file
    """
    if action == 'ls':
        grid_id = choose_grid()
        response = api.get_views(grid_id)
        for view in response:
            click.echo(view["name"])
    elif action == 'ex':
        view_id = choose_view()
        api.export_view(view_id)
    elif view_id is not None:
        view = api.get_view(view_id)
        click.echo(json.dumps(view, indent=4))
    else: 
        gridly()

@gridly.command()
@click.option('-ls', 'action', flag_value='ls', default=True)
def column(action):
    """
        List all columns of a Grid
    """
    if action == 'ls':
        grid_id = choose_grid()
        response = api.get_grid(grid_id)
        
        columns = response.get("columns")
        ls_column = []

        for column in columns:
            ls_column.append([column["id"], column["name"], column["type"]])

        click.echo("Grid name: " + response.get("name"))
        click.echo(tabulate(ls_column, headers=["Column ID", "Column Name", "Column Type"], tablefmt="grid"))

    else: 
        gridly()

@gridly.command()
@click.option('-ls', 'action', flag_value='ls', default=True, help='To list all records of a view')
@click.option('-d', 'action', flag_value='d', help='To delete records')
def record(action):
    """
        List all records of a view / Delete records
    """
    if action == 'ls':
        view_id = choose_view()

        response_columns = api.get_view(view_id)
        
        columns = response_columns.get("columns")

        response_records = api.get_records(view_id)

        # Set up column keys before add value to each column
        ls_cell = {} # ls_cell is a dictionary
        for cell in response_records:
            unique_cell = cell["cells"]
            for value in unique_cell:
                ls_cell.setdefault(value["columnId"], [])

        # Map value to column
        for cell in response_records:
            unique_cell = cell["cells"]
            for value in unique_cell:
                if value["columnId"] in ls_cell and "value" in value:
                    ls_cell[value["columnId"]].append(value["value"])
                elif value["columnId"] in ls_cell and "value" not in value:
                    ls_cell[value["columnId"]].append("")
                else: 
                    continue
        
        for column in columns:
            if column["id"] in ls_cell:
                ls_cell[column["name"]] = ls_cell.pop(column["id"]) 
            else:
                continue

        click.echo(tabulate(ls_cell, headers="keys", tablefmt="grid"))
    elif action == 'd':
        view_id = choose_view()
        response_records = api.get_records(view_id)

        ls_record_id = []
        for record in response_records:
            ls_record_id.append(record["id"])

        ls_chosen_record = questionary.checkbox(
            'Select records which you want delete',
            choices=ls_record_id).ask()

        data = {
            "ids": ls_chosen_record
        }

        api.delete_records(view_id, data)
    else:
        gridly()

@gridly.command()
@click.option('-json', 'type_json', flag_value='json', default=True, help="To export to JSON file type")
@click.option('-csv', 'type_csv', flag_value='csv', default=False, help="To export to CSV file type")
@click.option('-lang', 'target', flag_value='lang', default=False, help="To export to separate language files")
@click.argument('view_id')
@click.argument('dest', type=click.Path(exists=True), default='./', required=False)
def export(type_json, type_csv , target, view_id, dest):
    """
        Export all records of a view to files
    """

    rs_records = api.get_records(view_id)
    records = records_data_to_json(rs_records)
    lang_columns = []
    lang_records = {}

    if target == 'lang':
        view = api.get_view(view_id)
        for column in view["columns"]:
            if 'languageCode' in column:
                lang_columns.append(column["languageCode"])
        for lang in lang_columns:
            lang_records[lang] = api.split_column(records, lang)
    else:
        lang_records["all"] = records

    if type_json == 'json':
        for lang in lang_records:
            file_path = f'{dest}grid_{view_id}_{lang}.json'
            dump_to_json_file(file_path, lang_records[lang])
            click.echo(f'!!!SUCCESS exported to: {file_path}')

    if type_csv == 'csv':
        for lang in lang_records:
            file_path = f'{dest}grid_{view_id}_{lang}.csv'
            dump_to_csv_file(file_path, lang_records[lang])
            click.echo(f'!!!SUCCESS exported to: {file_path}')

if __name__ == '__main__':
    gridly()