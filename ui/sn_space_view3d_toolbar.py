# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>
import bpy
from bpy.types import (
    Header,
    Menu,
    Panel,
)


class View3DPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


class VIEW3D_PT_tools_object_options(View3DPanel, Panel):
    bl_category = "Tool"
    bl_context = ".objectmode"  # dot on purpose (access from topbar)
    bl_label = "Options"

    @classmethod
    def poll(cls, context):
        return context.scene.snap.ui.use_default_blender_interface

    def draw(self, context):
        # layout = self.layout
        pass


class VIEW3D_PT_tools_object_options_transform(View3DPanel, Panel):
    bl_category = "Tool"
    bl_context = ".objectmode"  # dot on purpose (access from topbar)
    bl_label = "Transform"
    bl_parent_id = "VIEW3D_PT_tools_object_options"

    @classmethod
    def poll(cls, context):
        return context.scene.snap.ui.use_default_blender_interface

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False

        tool_settings = context.tool_settings

        col = layout.column(heading="Affect Only", align=True)
        col.prop(tool_settings, "use_transform_data_origin", text="Origins")
        col.prop(tool_settings, "use_transform_pivot_point_align", text="Locations")
        col.prop(tool_settings, "use_transform_skip_children", text="Parents")    


classes = (
    VIEW3D_PT_tools_object_options,
    VIEW3D_PT_tools_object_options_transform,
)


def register():
    for cls in classes:
        if hasattr(bpy.types, str(cls)):
            bpy.utils.unregister_class(cls)
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
