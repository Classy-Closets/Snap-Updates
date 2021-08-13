from . import ops
from .data import data_entry_doors
from .data import data_windows

modules = (
    ops,
    data_entry_doors,
    data_windows
)


def register():
    for mod in modules:
        mod.register()


def unregister():
    for mod in reversed(modules):
        mod.unregister()
