import sys
import os
import re

sys.path.append(os.path.join(os.path.dirname(__file__)))
from make import create_folders


def main(argv):
    if len(argv) == 1:
        print(os.path.join(os.path.dirname(__file__)))
        return

    project_name = argv[1]

    if not valid_name(project_name):
        print("The project name is invalid. Make sure it's only consisted of alphabetic characters")
        return

    create_folders(project_name)


def valid_name(name):
    return not re.search(r"[^a-zA-Z]+", name)


if __name__ == "__main__":
    main(sys.argv)
