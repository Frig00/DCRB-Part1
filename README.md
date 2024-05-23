# DCRB Project - Part 1

## Introduction

The main goals of this project are building a search facility on a subtree of a local file system and implemeting a tool to retrieve files whose names or contents match with a given string. 

### Key Features
- **Upload Flexibility:** Files and directories are uploaded into the database in chunks to reduce the overload created by a large amount of database calls and to speed up the instertion process.
- **Comprehensive Search:** Search in the database is optimized by using indexes and, optionally, a local cache.
- **Database Management:** Efficiently organize and manage files and directories within a structured database environment.

Below are the main features of the scripts present in the project.


# `db.sql`

This SQL script sets up a database schema named `dcrb` and defines two tables: `directories` and `files`. \
The database on which I test this project was filled with all directories and files present in my laptop but, for semplicity, just the structure of the folder DCRB is reported in the file `DCRB tree.txt`. \
The database contains about 1.1 million files and 250000 directories.

## Script Structure
The script is organized into several sections:

1. **Schema creation**: 
   - Creates the `dcrb` schema if it doesn't exist.

2. **Creating `directories` table**:
   - Creates the `directories` table with columns for ID, name and parent directory ID.
   - Establishes a foreign key constraint on the `parent_dir` column referencing the `id` column of the same table with cascading delete.
   - Creates an index on the `id` column for searching optimization.

3. **Creating `files` table**:
   - Creates the `files` table with columns for ID, name, type, readability status, directory ID and content.
   - Establishes a foreign key constraint on the `dir` column referencing the `id` column of the `directories` table with cascading delete.
   - Creates indexes on the `name` column for searching optimization and a full-text index on the `content` column for efficient text searches.

## Data Consistency

- Foreign keys ensure referential integrity between directories and files.
- On Delete Cascade automates the process of elimination of all files and subdirectories when a directory is deleted.
- When a directory name changes, only the directory name needs to be updated, not the entire path of each file.
- Storing only the parent directory ID instead of the full path for each file ensures saving space.  

# `wiki_download.py`

This script downloads the content of Wikipedia pages within the "Music" category and organizes them into directories based on their categories. \
These files and directories populate the directory DCRB.

## Features

- Downloads Wikipedia pages within the "Music" category.
- Creates directories for categories and saves pages as text files.
- Avoids invalid file name characters in titles.

# `db_fill.py`

This script imports the structure and content of directories and files from a specified root directory into a MySQL database.

## Features

- Scans directories and files from a root directory.
- Inserts directory and file metadata into a MySQL database.
- Supports chunked insertion to handle large volumes of data.

# `db_search.py`

This script retrieves the full path and content details of files stored in a MySQL database based on a search string. It uses a recursive query to construct the full directory path for each file.

## Features

- Retrieves files from a MySQL database based on a search string.
- Constructs full file paths using a recursive query.
- Counts occurrences of the search string in readable file contents.
- Supports case-sensitive search.

# `cache.py`

This script provides a simple implementation of a local cache using an ordered dictionary. It ensures that the cache does not exceed a specified maximum size.

## Features

- Stores key-value pairs in a local cache.
- Limits the cache size to prevent memory overflow.
- Supports retrieval of all items and cache clearing.

# `db_search_cached.py`

This script retrieves the full path and content details of files stored in a MySQL database based on a search string. It utilizes both database queries and a local cache to improve performance and reduce database load.

## Features

- Retrieves files from a MySQL database based on a search string.
- Utilizes a local cache to store recently accessed files and reduce database queries.
- Counts occurrences of the search string in readable file contents.
- Supports case-sensitive search.
