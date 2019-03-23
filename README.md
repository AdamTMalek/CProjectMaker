# CProjectManager
CProjectManager (or cpm for short) makes it much easier to:
* Create a base for a new project (see usage for more information)
* Create a module (header with include guard + source file)

## Getting Started
**Please note that the script was developed only for the Linux operating system**
### Installing the script
In order to install the cpm you must download the script and run `install.py` by doing the following:
```
sudo python3 install.py
```
This will create a symbolic link in `/usr/local/bin`.

### Usage
The cpm has two options - `project` and `module`. The general usage syntax looks like this:
```
cpm [-h] {project,module} ...
```
#### Project
The `project` option is responsible for managing a C project. This includes:
* Creating a project with:
    * makefile
    * build directory
    * src directory
    * main.c inside src
    
    In this case the program only expects one positional argument `name`.
* Renaming a project. To do this, `-r`/`--rename` argument must be used. The argument expects an existing module name to be given.

The created makefile will have the following content:
```makefile
# Compiler:
CC = gcc

# C flags:
CFLAGS = -g -Wall -pedantic

# Directory with all the source files:
SRC = src
# Find all subdirectories inside the SRC directory. Remove ./ with subst.
VPATH = $(shell find $(SRC) -type d)

# Directory with where the compiled files go:
OBJ = build

# Find all .c files
SOURCES = $(subst ./,,$(shell find . -name "*.c"))
# Use $(notdir ...) to get only the filenames (ignore the directories)
# Delete file extensions with $(basename ...)
FILENAMES = $(basename $(notdir $(SOURCES)))
# All objects will be stored inside OBJ directory, without any sub-directories
# so, once we have the filenames we just simply add the .o suffix to them
# then, add the $(OBJ)/ prefix to put them inside the directory
OBJECTS = $(addprefix $(OBJ)/, $(addsuffix .o, $(FILENAMES)))

.PHONY: all
all: $(OBJECTS)
	$(CC) -o $(OBJ)/[PROJECT_NAME] $(OBJECTS)

$(OBJ)/%.o: %.c
	$(CC) -c $< $(CFLAGS) -o $@

.PHONY: clean
clean:
	@echo "Deleting all compiled files..."
	rm -f $(OBJ)/*
	@echo "Done."
```
**main.c** will have:
```c
#include <stdlib.h>

int main(int argc, char *argv[])
{
    return 0;
}
```
The usage syntax for `project` option is:
```
cpm project [-h] [-r old_name] name
```
#### Module
The `module` option is responsible for managing a C module - source and header files and optionally, a directory. 

The usage syntax for the `module` option is:
```
cpm module [-h] [-r old_name | -d] name
```
This option has three functions:
* Create source and header files with the given name in the current working directory
* (With `-d`/`--directory`) Create directory with the given name, then create source and header files inside that directory.
* (With `-r`/`--rename`) Rename module. Scan all source files inside **src** directory and update includes where applicable

The source file created will have the following content:
```c
#include "[NAME].h"

```
The header file will be:
```c
#ifndef [NAME]_H
#define [NAME]_H



#endif
```
Where in both cases `[NAME]` is the name passed as an argument.
## Uninstalling
If for some reason you want to uninstall the cpm you can do this using the `install.py` script. 
This is done by adding `remove` argument:
```
sudo python3 install.py remove
```
You can also go to `/usr/local/bin` and delete `cpm`, after doing so delete the whole cpm package wherever it was 
downloaded.
