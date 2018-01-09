import os
from shutil import copyfile


project_directory = ""


def create_folders(project_name):
    global project_directory
    project_directory = os.path.join(os.getcwd(), project_name)
    os.makedirs(project_directory)
    os.makedirs(os.path.join(project_directory, "src"))
    os.makedirs(os.path.join(project_directory, "build"))


def create_main_file():
    if len(project_directory) == 0:
        print("Project directory doesn't exist")
        return

    template = os.path.join(os.path.dirname(__file__), "../templates/main.c.txt")
    main_file = os.path.join(project_directory, "src/main.c")
    copyfile(template, main_file)


def create_project(project_name):
    create_folders(project_name)
    create_main_file()

