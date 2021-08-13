import bpy
from bpy.types import Menu

from snap import sn_utils, sn_types


def draw_assembly_properties(self, context):
    layout = self.layout
    layout.operator_context = 'INVOKE_AREA'
    obj = context.object
    id_prompt = ""
    menu_id = ""
    if obj and "ID_PROMPT" in obj and obj["ID_PROMPT"] != "":
        id_prompt = obj["ID_PROMPT"]
    if obj and "MENU_ID" in obj and obj["MENU_ID"] != "":
        menu_id = obj["MENU_ID"]

    if id_prompt:

        layout.operator(id_prompt, icon='WINDOW')
        if not menu_id:
            layout.separator()
    if menu_id:
        layout.menu(menu_id)
        layout.separator()


def draw_mesh_context(self, context):
    layout = self.layout
    layout.menu("SN_VIEW3D_MT_assembly_vertex_groups", icon='GROUP_VERTEX')
    layout.separator()


class SN_OT_object_properties(sn_types.Prompts_Interface):
    bl_idname = "wm.popup_props"
    bl_label = "Object Prompts"
    bl_options = {'UNDO'}

    plane: bpy.props.StringProperty(name="Plane", default="")  # noqa F722

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        obj = bpy.context.selected_objects[0]
        self.product = sn_types.Assembly(obj_bp=obj)
        split_name = obj.name.split(".")
        category = split_name[0]

        if category == "Outlets and Switches":
            self.plane = "XZ"
        else:
            self.plane = ""

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        self.draw_product_position(box, self.plane)
        row = box.row(align=True)
        self.draw_product_dimensions(row)
        self.draw_product_rotation(row, self.plane)


class SN_VIEW3D_MT_assembly_vertex_groups(Menu):
    bl_label = "Assembly Vertex Groups"

    def draw(self, context):
        layout = self.layout
        for vgroup in context.active_object.vertex_groups:
            count = 0
            for vert in context.active_object.data.vertices:
                for group in vert.groups:
                    if group.group == vgroup.index:
                        count += 1
            layout.operator(
                'sn_object.assign_verties_to_vertex_group',
                text="Assign to - " + vgroup.name + " (" + str(count) + ")").vertex_group_name = vgroup.name
        layout.separator()
        layout.operator(
            'sn_assembly.connect_meshes_to_hooks_in_assembly',
            text='Connect Hooks',
            icon='HOOK').obj_name = context.active_object.name
        layout.operator(
            'sn_object.clear_vertex_groups',
            text='Clear All Vertex Group Assignments',
            icon='X').obj_name = context.active_object.name


class VIEW3D_MT_object_context_menu(Menu):
    bl_label = "Object Context Menu"

    def draw(self, context):
        layout = self.layout
        view = context.space_data

        obj = context.object

        use_bl_ui = context.scene.snap.ui.use_default_blender_interface
        if not use_bl_ui and obj.type == 'CAMERA':
            return

        selected_objects_len = len(context.selected_objects)

        # If nothing is selected
        # (disabled for now until it can be made more useful).
        '''
        if selected_objects_len == 0:

            layout.menu("VIEW3D_MT_add", text="Add", text_ctxt=i18n_contexts.operator_default)
            layout.operator("view3d.pastebuffer", text="Paste Objects", icon='PASTEDOWN')

            return
        '''

        # TODO: Part context menu
        # obj_bp = sn_utils.get_assembly_bp(obj)
        assembly_bp = sn_utils.get_assembly_bp(obj)
        closet_bp = sn_utils.get_closet_bp(obj)
        insert_bp = sn_utils.get_bp(context.object, 'INSERT')
        entry_door_bp = sn_utils.get_entry_door_bp(context.object)
        window_bp = sn_utils.get_window_bp(context.object)
        assemblies = (assembly_bp, closet_bp, insert_bp, entry_door_bp, window_bp)
        # Adding walls to this
        pos_wall = sn_utils.get_wall_bp(context.object)
        layout.operator_context = 'INVOKE_DEFAULT'

        if any(assemblies):
            if closet_bp:
                layout.operator(
                    'sn_closets.move_closet',
                    text="Move - " + closet_bp.snap.name_object,
                    icon='OBJECT_ORIGIN').obj_bp_name = closet_bp.name

                layout.operator(
                    'sn_closets.copy_product',
                    text="Copy - " + closet_bp.snap.name_object,
                    icon='DUPLICATE').obj_bp_name = closet_bp.name

                layout.operator(
                    'sn_closets.delete_closet',
                    text="Delete - {}".format(closet_bp.snap.name_object),
                    icon='X')

                layout.separator()

            if entry_door_bp or window_bp:
                # TODO: Delete door/window operator here
                layout.operator(
                    'sn_closets.delete_closet',
                    text="Delete - {}".format(entry_door_bp.snap.name_object),
                    icon='X')

            if insert_bp:
                layout.operator(
                    'sn_closets.copy_insert',
                    text="Copy - {}".format(insert_bp.snap.name_object),
                    icon='DUPLICATE')

                layout.operator(
                    'sn_closets.delete_closet_insert',
                    text="Delete - {}".format(insert_bp.snap.name_object),
                    icon='X')

            if assembly_bp:
                if assembly_bp.get("ALLOW_PART_DELETE"):
                    layout.operator(
                        'sn_closets.delete_part',
                        text="Delete - {}".format(assembly_bp.snap.name_object),
                        icon='X')

                # TODO: Part context menu
                # layout.operator(
                #     'sn_closets.part_prompts',
                #     text="Part Prompts - " + obj_bp.name,
                #     icon='WINDOW')

        else:
            # If something is selected
            if obj is not None and obj.type in {'MESH', 'CURVE', 'SURFACE'} and pos_wall is None:
                layout.operator(
                    SN_OT_object_properties.bl_idname, icon='WINDOW')
                layout.separator()
                layout.operator("object.shade_smooth", text="Shade Smooth")
                layout.operator("object.shade_flat", text="Shade Flat")

                layout.separator()

            if obj is None:
                pass
            elif obj.type == 'MESH':
                layout.operator_context = 'INVOKE_REGION_WIN'
                layout.operator_menu_enum("object.origin_set", text="Set Origin", property="type")

                layout.operator_context = 'INVOKE_DEFAULT'
                # If more than one object is selected
                if selected_objects_len > 1:
                    layout.operator("object.join")

                layout.separator()

            elif obj.type == 'CAMERA':
                layout.operator_context = 'INVOKE_REGION_WIN'

                if obj.data.type == 'PERSP':
                    props = layout.operator("wm.context_modal_mouse", text="Camera Lens Angle")
                    props.data_path_iter = "selected_editable_objects"
                    props.data_path_item = "data.lens"
                    props.input_scale = 0.1
                    if obj.data.lens_unit == 'MILLIMETERS':
                        props.header_text = "Camera Lens Angle: %.1fmm"
                    else:
                        props.header_text = "Camera Lens Angle: %.1f\u00B0"

                else:
                    props = layout.operator("wm.context_modal_mouse", text="Camera Lens Scale")
                    props.data_path_iter = "selected_editable_objects"
                    props.data_path_item = "data.ortho_scale"
                    props.input_scale = 0.01
                    props.header_text = "Camera Lens Scale: %.3f"

                if not obj.data.dof.focus_object:
                    if view and view.camera == obj and view.region_3d.view_perspective == 'CAMERA':
                        props = layout.operator("ui.eyedropper_depth", text="DOF Distance (Pick)")
                    else:
                        props = layout.operator("wm.context_modal_mouse", text="DOF Distance")
                        props.data_path_iter = "selected_editable_objects"
                        props.data_path_item = "data.dof.focus_distance"
                        props.input_scale = 0.02
                        props.header_text = "DOF Distance: %.3f"

                layout.separator()

            elif obj.type in {'CURVE', 'FONT'}:
                layout.operator_context = 'INVOKE_REGION_WIN'

                props = layout.operator("wm.context_modal_mouse", text="Extrude Size")
                props.data_path_iter = "selected_editable_objects"
                props.data_path_item = "data.extrude"
                props.input_scale = 0.01
                props.header_text = "Extrude Size: %.3f"

                props = layout.operator("wm.context_modal_mouse", text="Width Size")
                props.data_path_iter = "selected_editable_objects"
                props.data_path_item = "data.offset"
                props.input_scale = 0.01
                props.header_text = "Width Size: %.3f"

                layout.separator()

                layout.operator("object.convert", text="Convert to Mesh").target = 'MESH'
                layout.operator("object.convert", text="Convert to Grease Pencil").target = 'GPENCIL'
                layout.operator_menu_enum("object.origin_set", text="Set Origin", property="type")

                layout.separator()

            elif obj.type == 'GPENCIL':
                layout.operator("gpencil.convert", text="Convert to Path").type = 'PATH'
                layout.operator("gpencil.convert", text="Convert to Bezier Curve").type = 'CURVE'
                layout.operator("gpencil.convert", text="Convert to Polygon Curve").type = 'POLY'

                layout.operator_menu_enum("object.origin_set", text="Set Origin", property="type")

                layout.separator()

            elif obj.type == 'EMPTY':
                layout.operator_context = 'INVOKE_REGION_WIN'

                props = layout.operator("wm.context_modal_mouse", text="Empty Draw Size")
                props.data_path_iter = "selected_editable_objects"
                props.data_path_item = "empty_display_size"
                props.input_scale = 0.01
                props.header_text = "Empty Draw Size: %.3f"

                layout.separator()

            elif obj.type == 'LIGHT':
                light = obj.data

                layout.operator_context = 'INVOKE_REGION_WIN'

                props = layout.operator("wm.context_modal_mouse", text="Power")
                props.data_path_iter = "selected_editable_objects"
                props.data_path_item = "data.energy"
                props.header_text = "Light Power: %.3f"

                if light.type == 'AREA':
                    props = layout.operator("wm.context_modal_mouse", text="Size X")
                    props.data_path_iter = "selected_editable_objects"
                    props.data_path_item = "data.size"
                    props.header_text = "Light Size X: %.3f"

                    if light.shape in {'RECTANGLE', 'ELLIPSE'}:
                        props = layout.operator("wm.context_modal_mouse", text="Size Y")
                        props.data_path_iter = "selected_editable_objects"
                        props.data_path_item = "data.size_y"
                        props.header_text = "Light Size Y: %.3f"

                elif light.type in {'SPOT', 'POINT'}:
                    props = layout.operator("wm.context_modal_mouse", text="Radius")
                    props.data_path_iter = "selected_editable_objects"
                    props.data_path_item = "data.shadow_soft_size"
                    props.header_text = "Light Radius: %.3f"

                elif light.type == 'SUN':
                    props = layout.operator("wm.context_modal_mouse", text="Angle")
                    props.data_path_iter = "selected_editable_objects"
                    props.data_path_item = "data.angle"
                    props.header_text = "Light Angle: %.3f"

                if light.type == 'SPOT':
                    layout.separator()

                    props = layout.operator("wm.context_modal_mouse", text="Spot Size")
                    props.data_path_iter = "selected_editable_objects"
                    props.data_path_item = "data.spot_size"
                    props.input_scale = 0.01
                    props.header_text = "Spot Size: %.2f"

                    props = layout.operator("wm.context_modal_mouse", text="Spot Blend")
                    props.data_path_iter = "selected_editable_objects"
                    props.data_path_item = "data.spot_blend"
                    props.input_scale = -0.01
                    props.header_text = "Spot Blend: %.2f"

                layout.separator()

            layout.operator("view3d.copybuffer", text="Copy Objects", icon='COPYDOWN')
            layout.operator("view3d.pastebuffer", text="Paste Objects", icon='PASTEDOWN')

            layout.separator()

            layout.operator("object.duplicate_move", icon='DUPLICATE')
            layout.operator("object.duplicate_move_linked")

            layout.separator()

            props = layout.operator("wm.call_panel", text="Rename Active Object...")
            props.name = "TOPBAR_PT_name"
            props.keep_open = False

            layout.separator()

            layout.menu("VIEW3D_MT_mirror")
            layout.menu("VIEW3D_MT_snap")
            layout.menu("VIEW3D_MT_object_parent")
            layout.operator_context = 'INVOKE_REGION_WIN'

            if view and view.local_view:
                layout.operator("view3d.localview_remove_from")
            else:
                layout.operator("object.move_to_collection")

            layout.separator()

            layout.operator("anim.keyframe_insert_menu", text="Insert Keyframe...")

            layout.separator()

            layout.operator_context = 'EXEC_DEFAULT'
            layout.operator("object.delete", text="Delete").use_global = False


def draw_add_object(self, context):
    layout = self.layout
    layout.operator_context = 'INVOKE_AREA'
    layout.operator('sn_assembly.create_new_assembly', text="Add Assembly", icon='FILE_3D')


def register():
    bpy.utils.register_class(VIEW3D_MT_object_context_menu)
    bpy.utils.register_class(SN_OT_object_properties)
    bpy.utils.register_class(SN_VIEW3D_MT_assembly_vertex_groups)
    bpy.types.VIEW3D_MT_edit_mesh.prepend(draw_mesh_context)
    bpy.types.VIEW3D_MT_object_context_menu.prepend(draw_assembly_properties)
    bpy.types.VIEW3D_MT_add.prepend(draw_add_object)


def unregister():
    bpy.utils.unregister_class(SN_VIEW3D_MT_assembly_vertex_groups)
    bpy.utils.unregister_class(SN_OT_object_properties)
    bpy.types.VIEW3D_MT_edit_mesh.remove(draw_mesh_context)
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_assembly_properties)
    bpy.types.VIEW3D_MT_add.remove(draw_add_object)
    bpy.utils.unregister_class(VIEW3D_MT_object_context_menu)
