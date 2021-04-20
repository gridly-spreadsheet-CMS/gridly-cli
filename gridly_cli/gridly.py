import click
import requests
import os
import questionary

# class QuestionaryOption(click.Option):

#     def __init__(self, param_decls=None, **attrs):
#         click.Option.__init__(self, param_decls, **attrs)
#         if not isinstance(self.type, click.Choice):
#             raise Exception('ChoiceOption type arg must be click.Choice')

#     def prompt_for_value(self, ctx):
#         val = questionary.select(self.prompt, choices=self.type.choices).unsafe_ask()
#         return val

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
def project():
    """List all projects."""
    response = requests.get(
    'https://gateway.staging.gridly.com/v1/projects', headers=headers).json()

    for project in response:
        print(project["name"])

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
def database():
    """List all databases."""
    projectid = choose_project()
    response = requests.get(
    'https://gateway.staging.gridly.com/v1/databases?projectId=' + projectid, headers=headers).json()
    for database in response:
        print(database["name"])

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
def grid():
    """List all grids."""
    dbid = choose_database()
    response = requests.get(
    'https://gateway.staging.gridly.com/v1/grids?dbId=' + dbid, headers=headers).json()
    for grid in response:
        print(grid["name"])

########################
###### List views ######
########################

def choose_grids():
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
def view():
    """List all views."""
    gridid = choose_grids()
    response = requests.get(
    'https://gateway.staging.gridly.com/v1/views?gridId=' + gridid, headers=headers).json()
    for view in response:
        print(view["name"])

if __name__ == '__main__':
    gridly()