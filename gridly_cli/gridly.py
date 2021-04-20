import click
import requests
import os
import questionary
from tabulate import tabulate


headers = {
    'Content-Type': 'application/json',
    'Authorization': 'ApiKey ' + str(os.environ["API-KEY"])
}

@click.group()
def gridly():
    """A CLI wrapper for the API of Gridly."""
    pass


###########################
###### List projects ######
###########################
@gridly.command()
def ls_project():
    """List all projects."""
    response = requests.get(
    'https://gateway.staging.gridly.com/v1/projects', headers=headers).json()

    for project in response:
        click.echo(project["name"])

############################
###### List databases ######
############################
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

@gridly.command()
def ls_database():
    """List all databases."""
    projectid = choose_project()
    response = requests.get(
    'https://gateway.staging.gridly.com/v1/databases?projectId=' + projectid, headers=headers).json()
    for database in response:
        click.echo(database["name"])

########################
###### List grids ######
########################

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

@gridly.command()
def ls_grid():
    """List all grids."""
    dbid = choose_database()
    response = requests.get(
    'https://gateway.staging.gridly.com/v1/grids?dbId=' + dbid, headers=headers).json()
    for grid in response:
        click.echo(grid["name"])

########################
###### List views ######
########################

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

@gridly.command()
def ls_view():
    """List all views."""
    gridid = choose_grid()
    response = requests.get(
    'https://gateway.staging.gridly.com/v1/views?gridId=' + gridid, headers=headers).json()
    for view in response:
        click.echo(view["name"])

#############################
###### Retrieve a grid ######
#############################

@gridly.command()
def grid():
    """Retrieve the grid information."""
    gridid = choose_grid()
    response = requests.get(
    'https://gateway.staging.gridly.com/v1/grids/' + gridid, headers=headers).json()
    
    columns = response.get("columns")
    ls_column = []

    for column in columns:
        ls_column.append([column["id"], column["name"], column["type"]])

    click.echo("Grid name: " + response.get("name"))
    click.echo(tabulate(ls_column, headers=["Column ID", "Column Name", "Column Type"]))
    

#############################
###### Retrieve a view ######
#############################

def choose_view():
    gridid = choose_grid()
    views = requests.get(
    'https://gateway.staging.gridly.com/v1/views?gridId=' + gridid, headers=headers).json()

    viewname = []
    viewid = ""
    for view in views:
        viewname.append(view["name"])

    chosen_viewname = questionary.select(
    "Choose your grid:",
    choices=viewname).ask()

    for view in views:
        if chosen_viewname == str(view["name"]):
            viewid = str(view["id"])
        else:
            continue
    return viewid

@gridly.command()
def view():
    """Retrieve the view information."""
    viewid = choose_view()
    response = requests.get(
    'https://gateway.staging.gridly.com/v1/views/' + viewid, headers=headers).json()
    
    columns = response.get("columns")
    ls_column = []

    for column in columns:
        ls_column.append([column["id"], column["name"], column["type"]])

    click.echo("View name: " + response.get("name"))
    click.echo(tabulate(ls_column, headers=["Column ID", "Column Name", "Column Type"]))

def Convert(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct

@gridly.command()
def records():
    """List all records of a view"""
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

    click.echo(tabulate(ls_cell, headers="keys"))



if __name__ == '__main__':
    gridly()