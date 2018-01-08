import os


def create_folders(project_name):
    cwd = os.getcwd()
    os.makedirs(os.path.join(cwd, project_name))
    os.makedirs(os.path.join(cwd, project_name, "src"))
    os.makedirs(os.path.join(cwd, project_name, "build"))
