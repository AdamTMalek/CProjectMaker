import errno
import fileinput
import os
from shutil import copyfile

from submanager import Submanager
from verbose import *


class Project(Submanager):
    def __init__(self, verbose_obj, name):
        super().__init__(verbose_obj)
        self.name = name
        self.directory = os.path.join(os.getcwd(), self.name)

    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser('project', help='creates/renames project')
        parser.add_argument('-r', '--rename', help='rename project with [old_name] to [name]', metavar='old_name')
        parser.add_argument('-v', '--verbose', action='count')
        parser.add_argument("name", help="target project name")
        # Set a function that will be called to handle the arguments
        parser.set_defaults(function=Project.handle_args)

    @staticmethod
    def handle_args(args, verbose):
        existing_name = args.name if not args.rename else args.rename
        project = Project(verbose, existing_name)

        if args.rename:
            project.rename(args.name)
        else:
            project.create_project()

    def create_folders(self):
        """
        Creates folders for the project
        :return: True if creating folders finished successfully, False otherwise
        """
        try:
            os.makedirs(self.directory)
        except OSError as error:
            if error.errno == errno.EEXIST:
                Verbose.print_any_level(MessageType.ERROR, "project with the same name already exists")
                return False
            if error.errno == errno.EACCES:
                Verbose.print_any_level(MessageType.ERROR, "permission denied")
                return False
            else:
                raise error

        os.makedirs(os.path.join(self.directory, "src"))
        os.makedirs(os.path.join(self.directory, "build"))

        return True

    def create_main_file(self):
        """
        Create the main.c file
        """
        template = os.path.join(os.path.dirname(__file__), "../templates/main.c.txt")
        main_file = os.path.join(self.directory, "src/main.c")
        copyfile(template, main_file)

    def create_makefile(self):
        """
        Create the makefile
        """
        template_path = os.path.join(os.path.dirname(__file__), "../templates/makefile.txt")
        makefile_path = os.path.join(self.directory, "makefile")

        with open(template_path, mode='r') as template:
            with open(makefile_path, mode='w') as makefile:
                for line in template.readlines():
                    line = line.replace("[PROJECT_NAME]", self.name)
                    makefile.write(line)

    def create_project(self):
        """
        Create project folders (main folder with src and build in it), main.c and the makefile
        """
        if self.create_folders():
            self.create_main_file()
            self.create_makefile()

    def rename(self, new_name):
        """
        Rename the project
        :param new_name: new name
        """
        if not os.path.isdir(os.path.join(os.getcwd(), self.name)):
            Verbose.print_any_level(MessageType.ERROR, "project {} does not exist".format(self.name), stream=sys.stderr)
            return

        os.rename(self.name, new_name)
        makefile_path = (os.path.join(os.getcwd(), new_name, "makefile"))
        for line in fileinput.input(makefile_path, inplace=True):
            # Change the end to an empty string, otherwise it will put another \n
            print(line.replace(self.name, new_name), end='')
