from . import sn_space_toolsystem_toolbar
from . import sn_space_topbar
from . import sn_filebrowser_ui
from . import sn_properties_workspace
from . import sn_space_view3d_toolbar
from . import sn_space_view3d
from . import sn_view3d_ui_sidebar_assemblies
from . import sn_view3d_ui_sidebar_object
from . import sn_view3d_ui_menu
from . import sn_lists
from . import sn_log_window

modules = (
    sn_space_toolsystem_toolbar,
    sn_space_topbar,
    sn_filebrowser_ui,
    sn_properties_workspace,
    sn_space_view3d_toolbar,
    sn_space_view3d,
    sn_view3d_ui_sidebar_assemblies,
    sn_view3d_ui_sidebar_object,
    sn_view3d_ui_menu,
    sn_log_window,
    sn_lists
)


def register():

    for mod in modules:
        mod.register()


def unregister():

    for mod in reversed(modules):
        mod.unregister()
