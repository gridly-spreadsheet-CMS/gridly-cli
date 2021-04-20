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

Before using the Grdily CLI, you need to configure your API key. You can add the API key to Environment variables in this way:

- With MacOS and Linux:

```
EXPORT API-KEY=<your-api-key>
```

- With Windows:

```
SET API-KEY=<your-api-key>
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
grid         Retrieve the grid information.
ls-database  List all databases.
ls-grid      List all grids.
ls-project   List all projects.
ls-view      List all views.
records      List all records of a view    
view         Retrieve the view information.
```

For example, to list project, the command would be:

```
$ gridly ls-project
```