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
        raise NotImplementedError("add_subparsers is not implemented")

    @staticmethod
    @abstractmethod
    def handle_args(args, verbose):
        raise NotImplementedError("handle_args is not implemented")
