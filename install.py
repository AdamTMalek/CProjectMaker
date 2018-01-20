import sys
import os
import errno


link = "/usr/local/bin/cpm"


def has_remove_arg(args):
    """
    Checks if remove argument exists
    :param args: Argument list
    :return: True if remove argument is found, False otherwise
    """

    if "remove" in args:
        return True

    return False


def main(args):
    if has_remove_arg(args):
        remove()
        return

    install()


def print_permission_denied():
    print("Permission denied. Make sure you run the install script as root")


def remove():
    """
    Removes symbolic link to the script
    """
    print("Removing...")
    try:
        os.remove(link)
    except OSError as error:

        if error.errno == errno.ENOENT:  # No such file or directory
            print("Symlink not found.")
        elif error.errno == errno.EACCES:
            print_permission_denied()
        else:
            raise error

    print("Finished.")


def create_symlink():
    target = os.path.join(os.path.abspath(os.path.dirname(__file__)), "project/cpm")
    try:
        os.symlink(target, link)
    except OSError as error:
        if error.errno == errno.EEXIST:
            os.remove(link)
            create_symlink()
        elif error.errno == errno.EACCES:
            print_permission_denied()
        else:
            raise error


def install():
    """
    Creates a symbolic link to the script
    """

    print("Installing...")
    create_symlink()
    print("Finished")


if __name__ == "__main__":
    main(sys.argv)
