import click
import requests
import os
import json
import questionary
from questionary import Separator, Choice, prompt
from tabulate import tabulate


headers = {
    'Content-Type': 'application/json',
    'Authorization': 'ApiKey ' + str(os.environ["GRIDLY_API_KEY"])
}

@click.group()
def gridly():
    """A CLI wrapper for the API of Gridly."""
    pass

def choose_project():
    projects = requests.get(
    'https://gateway.staging.gridly.com/v1/projects', headers=headers).json()

    projectname = []
    projectid = ""
    for project in projects:
        projectname.append(project["name"])

    chosen_projectname = questionary.select(
    "Choose your project:",
    choices=projectname).ask()

    for project in projects:
        if chosen_projectname == str(project["name"]):
            projectid = str(project["id"])
        else:
            continue
    return projectid

def choose_database():
    projectid = choose_project()
    databases = requests.get(
    'https://gateway.staging.gridly.com/v1/databases?projectId=' + projectid, headers=headers).json()

    databasename = []
    databaseid = ""
    for database in databases:
        databasename.append(database["name"])

    chosen_databasename = questionary.select(
    "Choose your database:",
    choices=databasename).ask()

    for database in databases:
        if chosen_databasename == str(database["name"]):
            databaseid = str(database["id"])
        else:
            continue
    return databaseid

def choose_grid():
    dbid = choose_database()
    grids = requests.get(
    'https://gateway.staging.gridly.com/v1/grids?dbId=' + dbid, headers=headers).json()

    gridname = []
    gridid = ""
    for grid in grids:
        gridname.append(grid["name"])

    chosen_gridname = questionary.select(
    "Choose your grid:",
    choices=gridname).ask()

    for grid in grids:
        if chosen_gridname == str(grid["name"]):
            gridid = str(grid["id"])
        else:
            continue
    return gridid

def choose_view():
    gridid = choose_grid()
    views = requests.get(
    'https://gateway.staging.gridly.com/v1/views?gridId=' + gridid, headers=headers).json()

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

####### Grid #######
@gridly.command()
@click.option('-ls', 'action', flag_value='ls', default=True)
@click.option('-u', 'action', flag_value='u')
def grid(action):
    """
        -ls [List all grids] / -u [Update grid name].
    """
    if action == 'ls':
        dbid = choose_database()
        response = requests.get(
        'https://gateway.staging.gridly.com/v1/grids?dbId=' + dbid, headers=headers).json()
        for grid in response:
            click.echo(grid["name"])
    elif action == 'u':
        gridid = choose_grid()

        grid_name = questionary.text("New grid name:").ask()

        data = {
            "name": grid_name
        }

        requests.patch(
            'https://gateway.staging.gridly.com/v1/grids/' + gridid, headers=headers, data=json.dumps(data))

        click.echo("Your grid name is changed")
    else: 
        gridly()

@gridly.command()
@click.option('-ls', 'action', flag_value='ls', default=True)
def project(action):
    """
        -ls [List all projects].
    """
    if action == 'ls':
        response = requests.get(
        'https://gateway.staging.gridly.com/v1/projects', headers=headers).json()

        for project in response:
            click.echo(project["name"])
    else: 
        gridly()

@gridly.command()
@click.option('-ls', 'action', flag_value='ls', default=True)
def database(action):
    """
        -ls [List all databases].
    """
    if action == 'ls':
        projectid = choose_project()
        response = requests.get(
        'https://gateway.staging.gridly.com/v1/databases?projectId=' + projectid, headers=headers).json()
        for database in response:
            click.echo(database["name"])
    else: 
        gridly()

@gridly.command()
@click.option('-ls', 'action', flag_value='ls', default=True)
@click.option('-ex', 'action', flag_value='ex')
def view(action):
    """
        -ls [List all views] / -ex [Export a view to CSV file].
    """
    if action == 'ls':
        gridid = choose_grid()
        response = requests.get(
        'https://gateway.staging.gridly.com/v1/views?gridId=' + gridid, headers=headers).json()
        for view in response:
            click.echo(view["name"])
    elif action == 'ex':
        viewid = choose_view()

        requests.get(
            'https://gateway.staging.gridly.com/v1/views/' + viewid + '/export', headers=headers)
    else: 
        gridly()

@gridly.command()
@click.option('-ls', 'action', flag_value='ls', default=True)
def column(action):
    """
        -ls [List all columns of a grid].
    """
    if action == 'ls':
        gridid = choose_grid()
        response = requests.get(
        'https://gateway.staging.gridly.com/v1/grids/' + gridid, headers=headers).json()
        
        columns = response.get("columns")
        ls_column = []

        for column in columns:
            ls_column.append([column["id"], column["name"], column["type"]])

        click.echo("Grid name: " + response.get("name"))
        click.echo(tabulate(ls_column, headers=["Column ID", "Column Name", "Column Type"], tablefmt="grid"))

    else: 
        gridly()

@gridly.command()
@click.option('-ls', 'action', flag_value='ls', default=True)
@click.option('-d', 'action', flag_value='d')
def records(action):
    """
        -ls [List all records of a view] / -d [Delete records].
    """
    if action == 'ls':
        viewid = choose_view()

        response_columns = requests.get(
        'https://gateway.staging.gridly.com/v1/views/' + viewid, headers=headers).json()
        
        columns = response_columns.get("columns")

        response_records = requests.get(
        'https://gateway.staging.gridly.com/v1/views/' + viewid + "/records", headers=headers).json()

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
        viewid = choose_view()

        response_records = requests.get(
        'https://gateway.staging.gridly.com/v1/views/' + viewid + "/records", headers=headers).json()

        ls_record_id = []
        for record in response_records:
            ls_record_id.append(record["id"])

        ls_chosen_record = questionary.checkbox(
            'Select columns which you want delete',
            choices=ls_record_id).ask()

        data = {
            "ids": ls_chosen_record
        }

        requests.delete(
            'https://gateway.staging.gridly.com/v1/views/' + viewid + '/records', headers=headers, data=json.dumps(data)
        )
    else:
        gridly()

if __name__ == '__main__':
    gridly()