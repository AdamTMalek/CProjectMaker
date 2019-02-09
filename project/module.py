import os

directory = ""


def create_source(name):
    template_path = os.path.join(os.path.dirname(__file__), "../templates/module.c.txt")
    source_path = os.path.join(directory, name + ".c")

    with open(template_path, mode='r') as template:
        with open(source_path, mode='w') as source:
            for line in template.readlines():
                line = line.replace("[NAME]", name)
                source.write(line)


def create_header(name):
    template_path = os.path.join(os.path.dirname(__file__), "../templates/module.h.txt")
    header_path = os.path.join(directory, name + ".h")

    header_name = name.upper()

    with open(template_path, mode='r') as template:
        with open(header_path, mode='w') as header:
            for line in template.readlines():
                line = line.replace("[NAME]", header_name)
                header.write(line)


def create_module(name, create_directory):
    global directory

    if already_exists(name):
        print("Module with that name already exists.")
        return

    if create_directory:
        os.mkdir(name)
        directory = os.path.join(os.getcwd(), name + '/')
    else:
        directory = os.getcwd()

    create_source(name)
    create_header(name)


def already_exists(name):
    return os.path.exists(os.path.join(os.getcwd(), name + '.c')) or \
           os.path.exists(os.path.join(os.getcwd(), name + '.h')) or \
           os.path.exists(os.path.join(os.getcwd(), name))
