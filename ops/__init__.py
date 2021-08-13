from . import sn_assembly
from . import sn_driver
from . import sn_export
from . import sn_library
from . import sn_material
from . import sn_object
from . import sn_prompt
from . import sn_window_manager
from . import sn_general
from . import sn_scene


modules = (
    sn_assembly,
    sn_driver,
    sn_export,
    sn_library,
    sn_material,
    sn_object,
    sn_prompt,
    sn_window_manager,
    sn_general,
    sn_scene
)


def register():

    for mod in modules:
        mod.register()


def unregister():

    for mod in reversed(modules):
        mod.unregister()
