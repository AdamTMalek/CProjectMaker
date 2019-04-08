import fileinput
import os
import re

from scripts.verbose import Verbose, MessageType
from submanager import Submanager


class Module(Submanager):
    def __init__(self, verbose_obj, name):
        """
        Create a Module object to manage (create/rename) a module.
        When creating a module, the name parameter should be set to the wanted name.
        However, when renaming, that parameter should be a name of an existing project that is to be renamed.
        :param verbose_obj: A Verbose object
        :param name: Target name when creating, or name of an existing module when renaming
        """
        super().__init__(verbose_obj)
        self.working_dir = os.getcwd()
        self.name = name

    @staticmethod
    def add_subparser(subparsers):
        """
         Set up the module option and all its arguments
         :param subparsers: subparsers of the argument parser
         """
        parser = subparsers.add_parser('module', help='creates/renames a module (source + header files)')

        # Because it does not make sense to have rename and directory arguments present at the same time
        # (it wouldn't be clear what the user wants to achieve)
        # mutually exclusive group will tell the parser that only one option from that group can be used at a time.
        mutually_exclusive = parser.add_mutually_exclusive_group()
        mutually_exclusive.add_argument('-r', '--rename', help='renfame module with [old_name] to [name]',
                                        metavar='old_name')
        mutually_exclusive.add_argument('-d', '--directory', action='store_true',
                                        help='create directory for the module')

        parser.add_argument('-v', '--verbose', action='count')
        parser.add_argument('name', help='target module name')
        # Set a function that will be called to handle the arguments
        parser.set_defaults(function=Module.handle_args)

    @staticmethod
    def handle_args(args, verbose):
        """
        Handle the program arguments
        :param args: Program arguments
        :param verbose: Verbose object
        """
        # If args.rename option is present the existing name is actually args.rename and the new name is args.name
        # For example, if the program will be executed like this: cpm module -r foo bar
        # The existing name will be set to foo and args.name will be bar (the new name)
        existing_name = args.name if not args.rename else args.rename
        module = Module(verbose, existing_name)

        if args.rename:
            module.rename(args.name)
        else:
            module.create_module(args.directory)

    def create_source(self):
        """
        Create a source file with the header file included
        """
        template_path = os.path.join(os.path.dirname(__file__), "../templates/module.c.txt")
        source_path = os.path.join(self.working_dir, self.name + ".c")

        with open(template_path, mode='r') as template:
            with open(source_path, mode='w') as source:
                for line in template.readlines():
                    line = line.replace("[NAME]", self.name)
                    source.write(line)

    def create_header(self):
        """
        Create a header file with an include-guard
        """
        template_path = os.path.join(os.path.dirname(__file__), "../templates/module.h.txt")
        header_path = os.path.join(self.working_dir, self.name + ".h")

        header_name = self.name.upper()

        with open(template_path, mode='r') as template:
            with open(header_path, mode='w') as header:
                for line in template.readlines():
                    line = line.replace("[NAME]", header_name)
                    header.write(line)

    def create_module(self, create_directory):
        """
        Create a module (source and header files), and a directory if create_directory is True
        :param create_directory: If True a directory for the module will be created
        """
        if self.already_exists(self.name):
            Verbose.print_any_level(MessageType.ERROR, "Module with the name {0} already exists.".format(self.name))
            return

        if create_directory:
            os.mkdir(self.name)
            self.working_dir = os.path.join(os.getcwd(), self.name + '/')

        self.create_source()
        self.create_header()

    def rename_directory(self, new_name):
        """
        Rename directory to the new name
        :param new_name: New name
        """
        old_dir = os.path.join(os.getcwd(), self.name)
        new_dir = os.path.join(os.getcwd(), new_name)
        os.rename(old_dir, new_dir)

    def rename_in_include(self, line, new_name):
        """
        Matches #include with the old_name as the header file and replaces the name to the new name
        :param line: line of a file
        :param new_name: new name to be substituted in
        :return: updated line and true/false depending if the line was modified
        """

        """
        There are two regular expressions and substitutions taking place.
        The first one is responsible for renaming the directory (if it exists) of the module.
        The regexp will capture everything to reuse after replacement
        The first capture group is the #include "[../[directories]/]" part.
        The second group captures the name of the module directory which contains the header file named [old_name].h
        Finally, the last group captures the rest of the line (i.e. /[old_name].h" part)
        """
        dir_replaced = re.sub(r'(#include "[./a-zA-Z_\d]*)({0})(/{0}\.h*")'.format(self.name),
                              r"\1%s\3" % new_name, line)

        """
        The second regex is responsible for renaming the actual header file.
        Again, it has 3 capture groups where 1st and 3rd are there to keep the parts of the line that do not change.
        It works pretty much the same as the first regex.
        The 2nd captured group is the filename without extension which the name is replaced with the [new_name] 
        """
        line, replacements = re.subn(r'(#include "[./a-zA-Z]*)({0})(\.h*")'.format(self.name), r"\1%s\3" % new_name,
                                     dir_replaced)

        return line, replacements > 0

    def rename_in_source(self, source_file, new_name):
        """
        Rename the module include header inside the source file
        :param source_file: file to be scanned/updated
        :param new_name: new name
        :return: true if the file contents have changed
        """
        changed = False  # Indicates whether the file contents have changed or not
        for line in fileinput.input(source_file, inplace=True):
            renamed = self.rename_in_include(line, new_name)
            # rename_in_include returns a tuple
            # renamed[0] is the modified line
            # renamed[1] is a boolean flag
            print(renamed[0], end='')
            if not changed and renamed[1]:
                changed = True
        return changed

    def rename_source(self, new_name):
        """
        Rename the source file and its included header file inside
        :param new_name: New name
        """
        old_path = os.path.join(self.working_dir, self.name + '.c')
        new_path = os.path.join(self.working_dir, new_name + '.c')
        os.rename(old_path, new_path)
        self.rename_in_source(new_path, new_name)

    def rename_header_constant(self, line, new_name):
        """
        Renames file include-guard-constant
        :param line: line of a file
        :param new_name: new name
        :return: modified line
        """
        old_name = self.name.upper()
        new_name = new_name.upper()

        # Looks for [OLD_NAME]_H and substitutes it with [NEW_NAME]_H. Replacing will also affect the comments
        return re.sub(r'([/*#a-zA-Z ]*)({0})(_H)([/*#a-zA-Z _]+)*'.format(old_name), r"\1%s\3\4" % new_name, line)

    def rename_header_constants(self, file, new_name):
        """
        Rename the header
        :param file: header file
        :param new_name: new name
        """
        for line in fileinput.input(file, inplace=True):
            print(self.rename_header_constant(line, new_name), end='')

    def rename_header(self, new_name):
        """
        Rename the header file and the constants inside it
        :param new_name: new name
        """
        old_path = os.path.join(self.working_dir, self.name + '.h')
        new_path = os.path.join(self.working_dir, new_name + '.h')
        os.rename(old_path, new_path)

        self.rename_header_constants(new_path, new_name)

    @staticmethod
    def get_all_source_files(src_dir):
        """
        Get all .c files inside the given directory
        :param src_dir: directory with source files
        :return: list of .c files inside the directory
        """
        files_list = []
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                if file.endswith('.c'):
                    files_list.append(os.path.join(root, file))
        return files_list

    def update_usages(self, new_name):
        """
        Look for the module include directive in every source file inside src directory (if such can be found in
        the current working directory path
        :param new_name: new name
        """
        # Try to find src directory in the current working directory path
        try:
            src_dir = re.match(r'([\S\\ ]+src)', os.getcwd()).group(0)
        except AttributeError:
            # src directory not found
            self.verbose.print(MessageType.WARNING, "src directory was not found in the current path. "
                                                    "Files that use the module will not be updated")
            return

        # Get all source files inside src and its subdirectories
        source_files = self.get_all_source_files(src_dir)
        # In each file, look for the module usage and update the name if such usage exists
        updated_count = 0  # Number of files that were updated
        files_updated = []
        for file in source_files:
            if self.rename_in_source(file, new_name) is True:
                updated_count += 1
                files_updated.append(os.path.relpath(file, src_dir))

        if files_updated:
            self.verbose.print(MessageType.INFO,
                               "Updated {} files: {}".format(len(files_updated), ", ".join(files_updated)))

    def rename(self, new_name):
        """
        Rename the module
        :param new_name: new name
        """
        if not self.already_exists(self.name):
            Verbose.print_any_level(MessageType.ERROR,
                                    "cannot rename the module. "
                                    "Module with the name {0} does not exist.".format(self.name))
            return

        if self.already_exists(new_name):
            Verbose.print_any_level(MessageType.ERROR,
                                    "cannot rename the module. "
                                    "Module with the name {0} already exists.".format(new_name))
            return

        # If the module is created inside a directory, rename it and go inside it
        if self.directory_exists(self.name):
            self.rename_directory(new_name)
            # Update the module directory
            self.working_dir = os.path.join(self.working_dir, new_name)

        # Rename source and header files
        if self.source_exists(self.working_dir, self.name):
            self.rename_source(new_name)
        if self.header_exists(self.working_dir, self.name):
            self.rename_header(new_name)

        Verbose.print_any_level(MessageType.INFO, "Successfully renamed the module")

        self.update_usages(new_name)
        self.name = new_name

    @staticmethod
    def directory_exists(name):
        """
        Check if the directory with the given name exists in the current working directory
        :param name: Directory name
        :return: True if it exists
        """
        dir_path = os.path.join(os.getcwd(), name)
        return os.path.exists(dir_path)

    @staticmethod
    def source_exists(directory, name):
        """
        Checks if the source file [name].c exists in the given directory
        :param directory: Directory to check
        :param name: Filename without the extension
        :return: True if the source file exists
        """
        return os.path.exists(os.path.join(directory, name + '.c'))

    @staticmethod
    def header_exists(directory, name):
        """
        Check if the source file [name].h exists in the given directory
        :param directory: Directory to check
        :param name: Filename without the extension
        :return: True if the header file exists
        """
        return os.path.exists(os.path.join(directory, name + '.h'))

    @staticmethod
    def already_exists(name):
        """
        Check if the module already exists
        :param name: name of a module
        :return: True if either source, header or directory with the given name exists
        """

        if Module.directory_exists(name):
            return True

        directory = os.path.join(os.getcwd(), name + '/')
        return Module.header_exists(directory, name) or Module.source_exists(directory, name)
