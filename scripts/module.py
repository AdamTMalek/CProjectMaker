import os
import re
import fileinput
from verbose import *

directory = ""
verbose = None


def set_verbose(verbose_obj):
    if not isinstance(verbose_obj, Verbose):
        raise TypeError("verbose_obj must be of type {expected}, not {actual}"
                        .format(expected=Verbose, actual=type(verbose_obj)))
    global verbose
    verbose = verbose_obj


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
        verbose.print(MessageType.ERROR, "Module with the name {0} already exists.".format(name), min_level=0)
        return

    if create_directory:
        os.mkdir(name)
        directory = os.path.join(os.getcwd(), name + '/')
    else:
        directory = os.getcwd()

    create_source(name)
    create_header(name)


def directory_exists(name):
    dir_path = os.path.join(os.getcwd(), name)
    return os.path.exists(dir_path)


def source_exists(name, file_dir=os.getcwd()):
    """
    Checks if the source file [name].c exists in the current working directory, or, if specified, given directory
    :param name: Filename without the extension
    :param file_dir: Directory where the source file could exist
    :return: True if source file exists
    """
    return os.path.exists(os.path.join(file_dir, name + '.c'))


def header_exists(name, file_dir=os.getcwd()):
    """
    Check if the source file [name].h exists in the current working directory, or, if specified, given directory
    :param name: Filename without the extension
    :param file_dir: Directory where the header file could exist
    :return: True if source file exists
    """
    return os.path.exists(os.path.join(file_dir, name + '.h'))


def rename_directory(old_name, name):
    """
    Rename directory with old_name that exists in the current working directory to name
    :param old_name: Old (existing) directory name
    :param name: New name
    """
    old_dir = os.path.join(os.getcwd(), old_name)
    new_dir = os.path.join(os.getcwd(), name)
    os.rename(old_dir, new_dir)


def rename_in_include(line, old_name, new_name):
    """
    Matches #include with the old_name as the header file and replaces the name to the new name
    :param line: line of a file
    :param old_name: old name of the module (header file)
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
    dir_replaced = re.sub(r'(#include "[./a-zA-Z_\d]*)({0})(/{0}\.h*")'.format(old_name), r"\1%s\3" % new_name, line)

    """
    The second regex is responsible for renaming the actual header file.
    Again, it has 3 capture groups where 1st and 3rd are there to keep the parts of the line that do not change.
    It works pretty much the same as the first regex.
    The 2nd captured group is the filename without extension which the name is replaced with the [new_name] 
    """
    line, replacements = re.subn(r'(#include "[./a-zA-Z]*)({0})(\.h*")'.format(old_name), r"\1%s\3" % new_name,
                                 dir_replaced)

    return line, replacements > 0


def rename_in_source(source_file, old_name, new_name):
    """
    Rename the module include header inside the source file
    :param source_file: file to be scanned/updated
    :param old_name: old module name
    :param new_name: new name
    :return: true if the file contents have changed
    """
    changed = False  # Indicates whether the file contents have changed or not
    for line in fileinput.input(source_file, inplace=True):
        renamed = rename_in_include(line, old_name, new_name)
        # rename_in_include returns a tuple
        # renamed[0] is the modified line
        # renamed[1] is a boolean flag
        print(renamed[0], end='')
        if not changed and renamed[1]:
            changed = True
    return changed


def rename_source(dir, old_name, name):
    """
    Rename the source file and its included header file inside
    :param dir: Directory in which the source file is located
    :param old_name: Old (existing) name of the file without .c extension
    :param name: New name
    """
    old_path = os.path.join(dir, old_name + '.c')
    new_path = os.path.join(dir, name + '.c')
    os.rename(old_path, new_path)
    rename_in_source(new_path, old_name, name)


def rename_header_constant(line, old_name, new_name):
    """
    Renames file include-guard-constant
    :param line: line of a file
    :param old_name: old name of the module
    :param new_name: new name
    :return: modified line
    """
    old_name = old_name.upper()
    new_name = new_name.upper()

    # Looks for [OLD_NAME]_H and substitutes it with [NEW_NAME]_H. Replacing will also affect the comments
    return re.sub(r'([/*#a-zA-Z ]*)({0})(_H)([/*#a-zA-Z _]+)*'.format(old_name), r"\1%s\3\4" % new_name, line)


def rename_header_constants(file, old_name, new_name):
    """
    Rename the header
    :param file: header file
    :param old_name: old (existing) module name
    :param new_name: new name
    """
    for line in fileinput.input(file, inplace=True):
        print(rename_header_constant(line, old_name, new_name), end='')


def rename_header(module_dir, old_name, name):
    """
    Rename the header file and the constants inside it
    :param module_dir: directory of the header file
    :param old_name: old name of the module
    :param name: new name
    """
    old_path = os.path.join(module_dir, old_name + '.h')
    new_path = os.path.join(module_dir, name + '.h')
    os.rename(old_path, new_path)

    rename_header_constants(new_path, old_name, name)


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


def update_usages(old_name, name):
    """
    Look for the module include directive in every source file inside src directory (if such can be found in
    the current working directory path
    :param old_name: old name of the module
    :param name: new name
    """
    # Try to find src directory in the current working directory path
    try:
        src_dir = re.match(r'([\S\\ ]+src)', os.getcwd()).group(0)
    except AttributeError:
        # src directory not found
        verbose.print(MessageType.WARNING, "src directory was not found in the current path. "
                                           "Files that use the module will not be updated")
        return

    # Get all source files inside src and its subdirectories
    source_files = get_all_source_files(src_dir)
    # In each file, look for the module usage and update the name if such usage exists
    updated_count = 0  # Number of files that were updated
    files_updated = []
    for file in source_files:
        if rename_in_source(file, old_name, name) is True:
            updated_count += 1
            files_updated.append(os.path.relpath(file, src_dir))

    if files_updated:
        verbose.print(MessageType.INFO,
                      "Updated {} files: {}".format(len(files_updated), ", ".join(files_updated)))


def rename(old_name, name):
    """
    Rename the module
    :param old_name: old (existing) name
    :param name: new name
    """
    working_directory = os.getcwd()

    if not already_exists(os.path.join(working_directory, old_name)):
        verbose.print(MessageType.ERROR,
                      "cannot rename the module. Module with the name {0} does not exist.".format(old_name),
                      min_level=0)
        return

    if already_exists(os.path.join(working_directory, name)):
        verbose.print(MessageType.ERROR,
                      "cannot rename the module. Module with the name {0} already exists.".format(name),
                      min_level=0)
        return

    # If the module is created inside a directory, rename it and go inside it
    if directory_exists(old_name):
        rename_directory(old_name, name)
        working_directory = os.path.join(working_directory, name)

    # Rename source and header files
    if source_exists(old_name, file_dir=working_directory):
        rename_source(working_directory, old_name, name)
    if header_exists(old_name, file_dir=working_directory):
        rename_header(working_directory, old_name, name)

    verbose.print(MessageType.INFO, "Successfully renamed the module", min_level=0)

    update_usages(old_name, name)


def already_exists(name):
    """
    Check if the module already exists
    :param name: name of a module
    :return: True if either source, header or directory with the given name exists
    """
    return source_exists(name) or header_exists(name) or directory_exists(name)
