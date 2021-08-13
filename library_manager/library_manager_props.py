import bpy
from bpy.types import PropertyGroup

from bpy.props import (
    StringProperty,
    BoolProperty,
    IntProperty,
    CollectionProperty
)


class List_Library_Item(PropertyGroup):
    """ Class to put products, inserts, and parts in a list view
        Used to show all library items
    """
    bp_name: StringProperty(name='BP Name')
    class_name: StringProperty(name='Class Name')
    library_name: StringProperty(name='Library Name')
    category_name: StringProperty(name='Category Name')
    selected: BoolProperty(name="Selected")
    has_thumbnail: BoolProperty(name="Has Thumbnail")
    has_file: BoolProperty(name="Has File")


class List_Library(PropertyGroup):
    package_name: StringProperty(name="Package Name")
    module_name: StringProperty(name="Module Name")
    lib_path: StringProperty(name="Library Path")
    items: CollectionProperty(name="Items",type=List_Library_Item)
    index: IntProperty(name="Index")


def register():
    bpy.utils.register_class(List_Library_Item)
    bpy.utils.register_class(List_Library)


def unregister():
    bpy.utils.unregister_class(List_Library)
    bpy.utils.unregister_class(List_Library_Item)
