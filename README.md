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
column    -ls [List all columns of a grid].
database  -ls [List all databases].
grid      -ls [List all grids] / -u [Update grid name].
project   -ls [List all projects].
records   -ls [List all records of a view] / -d [Delete records].
view      -ls [List all views] / -ex [Export a view to CSV file].
```

For example, to list project, the command would be:

```
$ gridly ls-project
```