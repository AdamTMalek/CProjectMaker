from importlib.machinery import SourceFileLoader
from importlib.util import spec_from_loader, module_from_spec


def load(module):
    if not isinstance(module, str):
        raise TypeError("Argument must be of type str, not: " + type(module))

    if len(module) == 0:
        raise ValueError("Module name cannot be empty")

    spec = spec_from_loader(module, SourceFileLoader(module, "../scripts/" + module))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
