# gridly-cli

This package provides a unified command line interface to Gridly

# Requirement

The gridly-cli package works on Python version: 

- 3.6.x and greater
- 3.7.x and greater
- 3.8.x and greater

# Installation

Installation of the Gridly CLI and its dependencies use a range of packaging features provided by pip and setuptools. To ensure smooth installation, it's recommended to use:

- pip: 9.0.2 or greater
- setuptools: 36.2.0 or greater

The safest way to install the Gridly CLI is to use pip in a virtualenv:

```
$ python -m pip install gridly-cli
```

# Configuration

Before using the Gridly CLI, you need to configure your API key. You can add the API key to Environment variables in this way:

- With MacOS and Linux:

```
$ EXPORT GRIDLY_API_KEY=<your-api-key>
```

- With Windows:

```
$ SET GRIDLY_API_KEY=<your-api-key>
```

# Basic Commands

An Gridly CLI command has the following structure:

```
gridly [OPTIONS] COMMAND [ARGS]...    
```   

Options:

```
--help  Show this message and exit.    
```    

Commands:

```
column    List all columns of a Grid

database  List all Databases

grid      List all Grids / Update Grid name
            -ls To list all Grids
            -u  To update Grid name

project   List all Projects

record    List all records of a view / Delete records
            -ls To list all records of a view
            -d To delete records

view      List all views / Export a view to CSV file
            -ls To list all views
            -ex To export a view to CSV file

export [OPTIONS] VIEW_ID [DEST]
          Export all records of a view to files
            -json To export to JSON file type
            -csv  To export to CSV file type
            -lang To export to separate language files
            [DEST] Optional. Path of folder where exporter will save files to. Default is current path.
```

For example, to list project, the command would be:

```
$ gridly project -ls
```
