# CProjectMaker
CProjectMaker (or cpm for short) lets you create base of any C project with just one simple command.
What exactly does it do? It creates:
* src and build folders
* main.c file with the following content:
* ```c
  #include <stdlib.h>
    
  int main(int argc, char *argv[])
  {
      return 0;
  }
  ```
* A simple makefile to compile the whole project

## Getting Started
**Please note that the script was developed only for the Linux operating system**
### Installing the script
In order to install the cpm you must download the script and run `install.py` by doing the following:
```
sudo python3 install.py
```
This will create a symbolic link in `/usr/local/bin`.

### Usage
Go to a directory where you want a new project to be created, then call the script like in the following example:
```
cpm [Project_Name]
```
Where the [Project_Name] is obviously your project name.
Now you should see a new folder named [Project_Name]. Inside it you will find
* Makefile
* src directory with main.c
* build directory where all the compiled files will go

## Uninstalling
If for some reason you want to uninstall the cpm you can do this using the `install.py` script. This is done by adding `remove` argument:
```
sudo python3 install.py remove
```
You can also go to `/usr/local/bin` and delete `cpm`, after doing so delete the whole cpm package wherever it was downloaded.