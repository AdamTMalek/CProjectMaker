import os
from abc import ABC, abstractmethod

from scripts.verbose import Verbose


class Submanager(ABC):
    @abstractmethod
    def __init__(self, verbose_obj):
        """
        Constructor of any submanager (project/module etc.)
        :param verbose_obj: Verbose object
        """
        if not isinstance(verbose_obj, Verbose):
            raise TypeError("verbose object should be of type {}, not {}".format(Verbose, type(verbose_obj)))
        self.verbose = verbose_obj
        self.working_dir = os.getcwd()

    @staticmethod
    @abstractmethod
    def add_subparser(subparsers):
        """
        All submanagers must implement the add_subparser method that takes a subparsers class created from argparse
        and adds a subparser with arguments and options supported by the submanager.
        """
        raise NotImplementedError("add_subparsers is not implemented")

    @staticmethod
    @abstractmethod
    def handle_args(args, verbose):
        """
        This function will be called when the program arguments supported by the submanager need to be handled.
        All submanagers must implement this function.
        """
        raise NotImplementedError("handle_args is not implemented")
