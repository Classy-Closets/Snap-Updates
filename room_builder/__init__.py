from snap.room_builder import props
from snap.room_builder import room_builder_ui
from snap.room_builder import ops

# This was going to be used to add the background image functionality.
# from snap.room_builder import image_class

modules = (
    props,
    ops,
    room_builder_ui,
)


def register():
    for mod in modules:
        mod.register()


def unregister():
    for mod in reversed(modules):
        mod.unregister()
