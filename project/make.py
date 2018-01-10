import os
from shutil import copyfile


directory = ""
name = ""


def create_folders(project_name):
    global directory
    directory = os.path.join(os.getcwd(), project_name)
    os.makedirs(directory)
    os.makedirs(os.path.join(directory, "src"))
    os.makedirs(os.path.join(directory, "build"))


def create_main_file():
    if len(directory) == 0:
        print("Project directory doesn't exist")
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
    create_folders(project_name)
    create_main_file()
    create_makefile()
