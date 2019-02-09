# CProjectMaker
CProjectMaker (or cpm for short) makes it much easier to:
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
```
cpm [-h] [-m] [-d] name
```
Arguments can be combined. These two lines will have exactly the same result:
```
cpm -m -d gpio
cpm -md gpio
```


If there are no optional arguments present then the script will create a base for the project with the following content:
* src and build folders
* makefile
* main.c file with the following content
    ```c
    #include <stdlib.h>
    
    int main(int argc, char *argv[])
    {
        return 0;
    }
    ```
By using the -m or --module argument the script will instead create a module with the given name in the current working
directory. For example the following:
```
cpm -m gpio
```
will create two files, **gpio.h** with the following content:
```c
#ifndef GPIO_H
#define GPIO_H



#endif
```
and **gpio.c**:
```c
#include "gpio.h"


```


A special option available only when creating module is the -d or --directory option. This will create a separate 
directory for the module. For example:
```
cpm -md gpio
```
will create a new **gpio** directory with **gpio.c** and **gpio.h** inside.
## Uninstalling
If for some reason you want to uninstall the cpm you can do this using the `install.py` script. 
This is done by adding `remove` argument:
```
sudo python3 install.py remove
```
You can also go to `/usr/local/bin` and delete `cpm`, after doing so delete the whole cpm package wherever it was 
downloaded.