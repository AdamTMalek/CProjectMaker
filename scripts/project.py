import errno
import os
import fileinput
from shutil import copyfile
from verbose import *

directory = ""
name = ""
verbose = None


def set_verbose(verbose_obj):
    if not isinstance(verbose_obj, Verbose):
        raise TypeError("verbose_obj must be of type {expected}, not {actual}"
                        .format(expected=Verbose, actual=type(verbose_obj)))
    global verbose
    verbose = verbose_obj


def create_folders(project_name):
    """
    Creates folders for the project
    :param project_name: Project name will be used as the name of the main directory
    :return: True if creating folders finished successfully, False otherwise
    """

    global directory
    directory = os.path.join(os.getcwd(), project_name)

    try:
        os.makedirs(directory)
    except OSError as error:
        if error.errno == errno.EEXIST:
            verbose.print(MessageType.ERROR, "project with the same name already exists", min_level=0)
            return False
        if error.errno == errno.EACCES:
            verbose.print(MessageType.ERROR, "permission denied", min_level=0)
            return False
        else:
            raise error

    os.makedirs(os.path.join(directory, "src"))
    os.makedirs(os.path.join(directory, "build"))

    return True


def create_main_file():
    if len(directory) == 0:
        verbose.print(MessageType.ERROR, "project directory doesn't exist", min_level=0)
        return

    template = os.path.join(os.path.dirname(__file__), "../templates/main.c.txt")
    main_file = os.path.join(directory, "src/main.c")
    copyfile(template, main_file)


def create_makefile():
    template_path = os.path.join(os.path.dirname(__file__), "../templates/makefile.txt")
    makefile_path = os.path.join(directory, "makefile")

    with open(template_path, mode='r') as template:
        with open(makefile_path, mode='w') as makefile:
            for line in template.readlines():
                line = line.replace("[PROJECT_NAME]", name)
                makefile.write(line)


def create_project(project_name):
    global name
    name = project_name
    if create_folders(project_name):
        create_main_file()
        create_makefile()


def rename(old, new):
    if not os.path.isdir(os.path.join(os.getcwd(), old)):
        verbose.print(MessageType.ERROR, "project {} does not exist".format(old), min_level=0)
        return

    os.rename(old, new)
    makefile_path = (os.path.join(os.getcwd(), new, "makefile"))
    for line in fileinput.input(makefile_path, inplace=True):
        print(line.replace(old, new), end='')  # Change the end to an empty string, otherwise it will put another \n.
