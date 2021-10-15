
from snap.project_manager import pm_ops
from snap.project_manager import pm_props
from snap.project_manager import pm_ui
from snap.project_manager import pm_handlers

classes = (
    pm_handlers,
    pm_props,
    pm_ops,
    pm_ui,
)


def register():
    for cls in classes:
        cls.register()


def unregister():
    for cls in reversed(classes):
        cls.unregister()
