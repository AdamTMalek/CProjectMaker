import errno
import fileinput
import os
from shutil import copyfile

from submanager import Submanager
from verbose import *


class Project(Submanager):
    def __init__(self, verbose_obj, project_name):
        super().__init__(verbose_obj)
        self.project_name = project_name
        self.project_directory = os.path.join(os.getcwd(), self.project_name)

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
        if args.rename:
            Project.rename(args.rename, args.name)
        else:
            project = Project(verbose, args.name)
            project.create_project()

    def create_folders(self):
        """
        Creates folders for the project
        :return: True if creating folders finished successfully, False otherwise
        """
        try:
            os.makedirs(self.project_directory)
        except OSError as error:
            if error.errno == errno.EEXIST:
                Verbose.print_any_level(MessageType.ERROR, "project with the same name already exists")
                return False
            if error.errno == errno.EACCES:
                Verbose.print_any_level(MessageType.ERROR, "permission denied")
                return False
            else:
                raise error

        os.makedirs(os.path.join(self.project_directory, "src"))
        os.makedirs(os.path.join(self.project_directory, "build"))

        return True

    def create_main_file(self):
        """
        Create the main.c file
        """
        template = os.path.join(os.path.dirname(__file__), "../templates/main.c.txt")
        main_file = os.path.join(self.project_directory, "src/main.c")
        copyfile(template, main_file)

    def create_makefile(self):
        """
        Create the makefile
        """
        template_path = os.path.join(os.path.dirname(__file__), "../templates/makefile.txt")
        makefile_path = os.path.join(self.project_directory, "makefile")

        with open(template_path, mode='r') as template:
            with open(makefile_path, mode='w') as makefile:
                for line in template.readlines():
                    line = line.replace("[PROJECT_NAME]", self.project_name)
                    makefile.write(line)

    def create_project(self):
        """
        Create project folders (main folder with src and build in it), main.c and the makefile
        """
        if self.create_folders():
            self.create_main_file()
            self.create_makefile()

    @staticmethod
    def rename(old, new):
        """
        Rename the project
        :param old: old (existing) name
        :param new: new name
        """
        if not os.path.isdir(os.path.join(os.getcwd(), old)):
            Verbose.print_any_level(MessageType.ERROR, "project {} does not exist".format(old), stream=sys.stderr)
            return

        os.rename(old, new)
        makefile_path = (os.path.join(os.getcwd(), new, "makefile"))
        for line in fileinput.input(makefile_path, inplace=True):
            print(line.replace(old, new), end='')  # Change the end to an empty string, otherwise it will put another \n
