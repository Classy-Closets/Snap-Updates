import bpy
from bpy.types import Operator, Menu
from bpy.props import (
    StringProperty,
    BoolProperty,
    EnumProperty)
from snap import sn_utils, sn_types
import math


class SN_GEN_OT_change_file_browser_path(Operator):
    bl_idname = "sn_general.change_file_browser_path"
    bl_label = "Change File Browser Path"
    bl_description = "Changes the file browser path"
    bl_options = {'UNDO'}

    file_path: StringProperty(name='File Path')

    def execute(self, context):
        sn_utils.update_file_browser_path(context, self.file_path)
        return {'FINISHED'}


class SN_GEN_OT_update_library_xml(Operator):
    """ This will load all of the products from the products module.
    """
    bl_idname = "sn_general.update_library_xml"
    bl_label = "Update Library XML"
    bl_description = "This will Update the Library XML file that stores the library paths"
    bl_options = {'UNDO'}

    def execute(self, context):
        xml = sn_types.MV_XML()
        root = xml.create_tree()
        paths = xml.add_element(root, 'LibraryPaths')

        wm = context.window_manager
        packages = xml.add_element(paths, 'Packages')
        for package in wm.snap.library_packages:
            if os.path.exists(package.lib_path):
                lib_package = xml.add_element(packages, 'Package', package.lib_path)
                xml.add_element_with_text(lib_package, 'Enabled', str(package.enabled))

        if os.path.exists(wm.snap.library_module_path):
            xml.add_element_with_text(paths, 'Modules', wm.snap.library_module_path)
        else:
            xml.add_element_with_text(paths, 'Modules', "")

        if os.path.exists(wm.snap.assembly_library_path):
            xml.add_element_with_text(paths, 'Assemblies', wm.snap.assembly_library_path)
        else:
            xml.add_element_with_text(paths, 'Assemblies', "")

        if os.path.exists(wm.snap.object_library_path):
            xml.add_element_with_text(paths, 'Objects', wm.snap.object_library_path)
        else:
            xml.add_element_with_text(paths, 'Objects', "")

        if os.path.exists(wm.snap.material_library_path):
            xml.add_element_with_text(paths, 'Materials', wm.snap.material_library_path)
        else:
            xml.add_element_with_text(paths, 'Materials', "")

        if os.path.exists(wm.snap.world_library_path):
            xml.add_element_with_text(paths, 'Worlds', wm.snap.world_library_path)
        else:
            xml.add_element_with_text(paths, 'Worlds', "")

        xml.write(sn_utils.get_library_path_file())

        return {'FINISHED'}


class SN_GEN_OT_open_new_window(Operator):
    bl_idname = "sn_general.open_new_window"
    bl_label = "Open New Window"

    space_type: bpy.props.StringProperty(name="Space Type")

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
        for window in context.window_manager.windows:
            if len(window.screen.areas) == 1 and window.screen.areas[0].type == 'PREFERENCES':
                window.screen.areas[0].type = self.space_type
        return {'FINISHED'}


class SN_GEN_OT_select_all_elevation_scenes(Operator):
    bl_idname = "sn_general.select_all_elevation_scenes"
    bl_label = "Select All Elevation Scenes"
    bl_description = "This will select all of the scenes in the elevation scenes list"

    select_all: BoolProperty(name="Select All", default=True)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        for scene in bpy.data.scenes:
            if scene.snap.elevation_scene or scene.snap.plan_view_scene:
                scene.snap.elevation_selected = self.select_all

        return{'FINISHED'}


class SN_GEN_OT_project_info(Operator):
    bl_idname = "sn_general.project_info"
    bl_label = "Project Info (Fill In All Fields)"

    def check(self, context):
        active_props = context.scene.snap
        for scene in bpy.data.scenes:
            props = scene.snap
            props.job_name = active_props.job_name
            props.job_number = active_props.job_number
            props.install_date = active_props.install_date
            props.designer_name = active_props.designer_name
            props.designer_phone = active_props.designer_phone
            props.client_name = active_props.client_name
            props.client_phone = active_props.client_phone
            props.client_email = active_props.client_email
            props.client_number = active_props.client_number
            props.job_comments = active_props.job_comments
            props.tear_out = active_props.tear_out
            props.touch_up = active_props.touch_up
            props.block_wall = active_props.block_wall
            props.new_construction = active_props.new_construction
            props.elevator = active_props.elevator
            props.stairs = active_props.stairs
            props.floor = active_props.floor
            props.door = active_props.door
            props.base_height = active_props.base_height
            props.parking = active_props.parking

        return True

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=sn_utils.get_prop_dialog_width(350))

    def draw(self, context):
        props = context.scene.snap
        layout = self.layout
        layout.prop(props, "job_name")
        layout.prop(props, "job_number")
        layout.prop(props, "install_date")
        layout.prop(props, "designer_name")
        layout.prop(props, "designer_phone")
        layout.prop(props, "client_name")
        layout.prop(props, "client_number")
        layout.prop(props, "client_phone")
        layout.prop(props, "client_email")
        layout.prop(props, "job_comments")
        layout.prop(props, "tear_out")
        layout.prop(props, "touch_up")
        layout.prop(props, "block_wall")
        layout.prop(props, "new_construction")
        layout.prop(props, "elevator")
        layout.prop(props, "stairs")
        layout.prop(props, "floor")
        layout.prop(props, "door")
        layout.prop(props, "base_height")
        layout.prop(props, "parking")


class SNAP_GEN_OT_viewport_shade_mode(Operator):
    bl_idname = "sn_general.change_shade_mode"
    bl_label = "Change Viewport Shading Mode"

    mode: EnumProperty(
        name="Shade Mode",
        items=(
            ('WIREFRAME', "Wire Frame", "WIREFRAME", 'SHADING_WIRE', 1),
            ('SOLID', "Solid", "SOLID", 'SHADING_SOLID', 2),
            ('MATERIAL', "Material", "MATERIAL", 'MATERIAL', 3),
            ('RENDERED', "Rendered", "RENDERED", 'SHADING_RENDERED', 4)))

    def hide_ceiling(self, context, hide):
        for obj in bpy.data.objects:
            if obj.sn_roombuilder.is_ceiling:
                obj.hide_viewport = hide

    def execute(self, context):
        context.area.spaces.active.shading.type = self.mode
        if self.mode == 'RENDERED':
            context.space_data.overlay.show_overlays = False
            context.space_data.show_gizmo = False
            self.hide_ceiling(context, False)
        else:
            context.space_data.overlay.show_overlays = True
            context.space_data.show_gizmo = True
            self.hide_ceiling(context, True)

        return {'FINISHED'}


class SNAP_MT_viewport_shade_mode(Menu):
    bl_label = "Viewport Shade Mode"

    def draw(self, context):
        layout = self.layout
        layout.operator("sn_general.change_shade_mode", text="")


classes = (
    SN_GEN_OT_change_file_browser_path,
    SN_GEN_OT_update_library_xml,
    SN_GEN_OT_open_new_window,
    SN_GEN_OT_select_all_elevation_scenes,
    SN_GEN_OT_project_info,
    SNAP_GEN_OT_viewport_shade_mode,
    SNAP_MT_viewport_shade_mode
)

register, unregister = bpy.utils.register_classes_factory(classes)
