import click
import requests
import os
import json
import questionary
from questionary import Separator, Choice, prompt
from tabulate import tabulate


headers = {
    'Content-Type': 'application/json',
    'Authorization': 'ApiKey ' + str(os.environ["GRIDLY-API-KEY"])
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

@gridly.command()
@click.option('--ls', 'action', flag_value='ls', default=True)
@click.option('--u', 'action', flag_value='u')
def grid(action):
    """List all grids."""
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

if __name__ == '__main__':
    gridly()