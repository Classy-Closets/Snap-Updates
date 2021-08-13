from snap.views import (
    report_2d_drawings,
    view_props,
    view_ui,
    view_ops,
    view_handlers
)

modules = (
    view_props,
    view_ops,
    view_ui,
    report_2d_drawings,
    view_handlers
)


def register():
    for mod in modules:
        mod.register()


def unregister():
    for mod in reversed(modules):
        mod.unregister()
