import bpy,os

from bpy.types import (Header, 
                       Menu, 
                       Panel, 
                       Operator,
                       PropertyGroup)

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       PointerProperty,
                       EnumProperty,
                       CollectionProperty)

from snap import sn_unit, sn_types, sn_utils
import math


enum_machine_tokens = [('NONE', "None", "None", 'SCULPTMODE_HLT', 0),
                       ('CONST', "CONST", "CONST", 'SCULPTMODE_HLT', 1),
                       ('HOLES', "HOLES", "HOLES", 'SCULPTMODE_HLT', 2),
                       ('SHLF', "SHLF", "SHLF", 'SCULPTMODE_HLT', 3),
                       ('SHELF', "SHELF", "SHELF", 'SCULPTMODE_HLT', 4),
                       ('SHELFSTD', "SHELFSTD", "SHELFSTD", 'SCULPTMODE_HLT', 5),
                       ('DADO', "DADO", "DADO", 'SCULPTMODE_HLT', 6),
                       ('SAW', "SAW", "SAW", 'SCULPTMODE_HLT', 7),
                       ('SLIDE', "SLIDE", "SLIDE", 'SCULPTMODE_HLT', 8),
                       ('CAMLOCK', "CAMLOCK", "CAMLOCK", 'SCULPTMODE_HLT', 9),
                       ('MITER', "MITER", "MITER", 'SCULPTMODE_HLT', 10),
                       ('3SIDEDNOTCH', "3SIDEDNOTCH", "3SIDEDNOTCH", 'SCULPTMODE_HLT', 12),
                       ('PLINE', "PLINE", "PLINE", 'SCULPTMODE_HLT', 11),
                       ('BORE', "BORE", "BORE", 'SCULPTMODE_HLT', 13)]


class SN_OBJ_override_object_context_menu(Operator):
    bl_idname = "sn_object.override_object_context_menu"
    bl_label = "Override object context menu"

    def execute(self, context):
        obj = context.object
        has_id_ppt = obj and "ID_PROMPT" in obj and obj["ID_PROMPT"] != ""
        assy_obj_bp = sn_utils.get_assembly_bp(obj)

        if not assy_obj_bp:
            if has_id_ppt:
                eval("bpy.ops.{}('INVOKE_DEFAULT')".format(obj["ID_PROMPT"]))
            elif obj.type == "MESH" and not context.scene.snap.ui.use_default_blender_interface:
                bpy.ops.wm.popup_props('INVOKE_DEFAULT')
        else:
            bpy.ops.wm.call_menu(name="VIEW3D_MT_object_context_menu")

        return {'FINISHED'}


class SN_OBJ_delete(Operator):
    bl_idname = "sn_object.delete"
    bl_label = "Delete Operator that honors delete protected objects"

    use_global: BoolProperty(name='Use Global', default=False)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        contains_protected = False
        delete_protected_objects = []
        for obj in context.selected_objects:
            if obj.snap.delete_protected:
                obj.select_set(False)
                contains_protected = True
                delete_protected_objects.append(obj.name)

        bpy.ops.object.delete(use_global=self.use_global)
        if contains_protected:
            bpy.ops.snap.message_box(
                'INVOKE_DEFAULT',
                message="Unable to delete wall. Proceed building room and then \nadd door or open entry way to reflect open space.")


        return {'FINISHED'}


class SN_OBJ_delete(Operator):
    bl_idname = "sn_object.delete"
    bl_label = "Delete Object(s)"

    use_global: BoolProperty(name='Use Global', default=False)
    del_obj_protected: BoolProperty(name='Delete Protected Object', default=False)
    del_obj = None
    del_obj_bp = None
    delete_protected_objects = []


    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def invoke(self, context, event):
        wm = context.window_manager

        for obj in context.selected_objects:
            # Ensure delete_protected is set for older library data
            obj_bp = sn_utils.get_assembly_bp(obj)
            if obj_bp:
                if "IS_BP_PANEL" in obj_bp:
                    obj.snap.delete_protected = True

            if obj.snap.delete_protected:
                self.del_obj = obj
                obj.select_set(False)
                self.del_obj_protected = True
                self.delete_protected_objects.append(obj.name)

        self.del_obj_bp = sn_utils.get_assembly_bp(self.del_obj)

        if self.del_obj_bp:
            if "IS_BP_PANEL" in self.del_obj_bp:
                return wm.invoke_props_dialog(self, width=350)
            else:
                return self.execute(context)
        return self.execute(context)

    def draw(self, context):
        layout = self.layout

        if "IS_BP_PANEL" in self.del_obj_bp:
            layout.label(text="Warning!")
            layout.label(text="Deleting this partition is unsupported and may lead to plans with")
            layout.label(text="insufficient/incorrect information and/or inability to create 2D views")

    def execute(self, context):
        bpy.ops.object.delete(use_global=self.use_global)

        if self.del_obj_protected and self.del_obj:
            message = ""
            if self.del_obj.snap:
                props = self.del_obj.snap
                if props.is_wall_mesh:
                    message = "Unable to delete wall. Proceed building room and then \nadd door or open entry way to reflect open space."
            if message:
                bpy.ops.snap.message_box('INVOKE_DEFAULT', message=message)

            if self.del_obj_bp:
                if "IS_BP_PANEL" in self.del_obj_bp:
                    sn_utils.delete_object_and_children(self.del_obj_bp)

        return {'FINISHED'}


class SN_OBJ_select_object(Operator):
    bl_idname = "sn_object.select_object"
    bl_label = "Select Object"
    bl_description = "This selects an object and sets it as an active object"
    bl_options = {'UNDO'}

    obj_name: StringProperty(name='Object Name')

    def execute(self, context):
        if self.obj_name in context.scene.objects:
            bpy.ops.object.select_all(action = 'DESELECT')
            obj = context.scene.objects[self.obj_name]
            obj.select_set(True)
            context.view_layer.objects.active = obj
        return {'FINISHED'}


class SNAP_OT_delete_object(Operator):
    bl_idname = "sn_object.delete_object"
    bl_label = "Delete Object"
    bl_description = "This deletes an object"
    bl_options = {'UNDO'}

    obj_name: StringProperty(name='Object Name')

    def execute(self, context):
        obj = bpy.data.objects[self.obj_name]
        bpy.data.objects.remove(obj, do_unlink=True)
        return {'FINISHED'}


class SN_OBJ_draw_floor_plane(Operator):
    bl_idname = "sn_object.draw_floor_plane"
    bl_label = "Draw Floor Plane"
    bl_options = {'UNDO'}
    
    def execute(self, context):
        largest_x = 0
        largest_y = 0
        smallest_x = 0
        smallest_y = 0
        wall_groups = []
        for obj in bpy.data.objects:
            if obj.get('IS_BP_WALL') is not None:
                wall_groups.append(sn_types.Wall(obj_bp=obj))
            
        for group in wall_groups:
            start_point = (group.obj_bp.matrix_world[0][3],group.obj_bp.matrix_world[1][3],0)
            end_point = (group.obj_x.matrix_world[0][3],group.obj_x.matrix_world[1][3],0)

            if start_point[0] > largest_x:

                largest_x = start_point[0]
            if start_point[1] > largest_y:
                largest_y = start_point[1]
            if start_point[0] < smallest_x:
                smallest_x = start_point[0]
            if start_point[1] < smallest_y:
                smallest_y = start_point[1]
            if end_point[0] > largest_x:
                largest_x = end_point[0]
            if end_point[1] > largest_y:
                largest_y = end_point[1]
            if end_point[0] < smallest_x:
                smallest_x = end_point[0]
            if end_point[1] < smallest_y:
                smallest_y = end_point[1]

        loc = (smallest_x , smallest_y,0)
        width = math.fabs(smallest_y) + math.fabs(largest_y)
        length = math.fabs(largest_x) + math.fabs(smallest_x)
        if width == 0:
            width = sn_unit.inch(-48)
        if length == 0:
            length = sn_unit.inch(-48)

        obj_plane = sn_utils.create_floor_mesh('Floor',(length,width,0.0))
        obj_plane.location = loc
        obj_plane["ID_PROMPT"] = "wm.popup_props"

        # SET CONTEXT
        context.view_layer.objects.active = obj_plane

        return {'FINISHED'}


class SN_OBJ_toggle_edit_mode(Operator):
    bl_idname = "sn_object.toggle_edit_mode"
    bl_label = "Toggle Edit Mode"
    bl_description = "This will toggle between object and edit mode"
    
    obj_name: StringProperty(name="Object Name")

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        obj = bpy.data.objects[self.obj_name]
        obj.hide_set(False)
        obj.hide_select = False
        obj.select_set(True)
        context.view_layer.objects.active = obj
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class SN_OBJ_clear_vertex_groups(Operator):
    bl_idname = "sn_object.clear_vertex_groups"
    bl_label = "Clear Vertex Groups"
    bl_description = "This clears all of the vertex group assignments"
    bl_options = {'UNDO'}
    
    obj_name: StringProperty(name="Object Name")
    
    def execute(self,context):

        obj = bpy.data.objects[self.obj_name]
        
        if obj.mode == 'EDIT':
            bpy.ops.object.editmode_toggle()
            
        for vgroup in obj.vertex_groups:
            for vert in obj.data.vertices:
                vgroup.remove((vert.index,))

        if obj.mode == 'OBJECT':
            bpy.ops.object.editmode_toggle()

        return{'FINISHED'}


class SN_OBJ_apply_hook_modifiers(Operator):
    bl_idname = "sn_object.apply_hook_modifiers"
    bl_label = "Apply Hook Modifiers"
    bl_options = {'UNDO'}

    object_name : StringProperty(name="Object Name")

    def execute(self, context):
        obj = bpy.data.objects[self.object_name]
        context.view_layer.objects.active = obj
        list_mod = []
        if obj:
            for mod in obj.modifiers:
                if mod.type in {'HOOK','MIRROR'}:
                    list_mod.append(mod.name)

        for mod in list_mod:
            bpy.ops.object.modifier_apply(modifier=mod)
            
        obj.lock_location = (False,False,False)
        obj.lock_scale = (False,False,False)
        obj.lock_rotation = (False,False,False)
        
        return {'FINISHED'}


class SN_OBJ_assign_verties_to_vertex_group(Operator):
    bl_idname = "sn_object.assign_verties_to_vertex_group"
    bl_label = "Assign Verties to Vertex Group"
    bl_description = "This assigns selected verties to the group that is passed in"
    bl_options = {'UNDO'}
    
    vertex_group_name: StringProperty(name="Vertex Group Name")
    
    def execute(self,context):

        obj = context.active_object
        
        if obj.mode == 'EDIT':
            bpy.ops.object.editmode_toggle()
            
        vgroup = obj.vertex_groups[self.vertex_group_name]
        
        for vert in obj.data.vertices:
            if vert.select == True:
                vgroup.add((vert.index,),1,'ADD')

        if obj.mode == 'OBJECT':
            bpy.ops.object.editmode_toggle()

        return{'FINISHED'}


class SNAP_OT_add_camera(Operator):
    bl_idname = "sn_object.add_camera"
    bl_label = "Camera"
    bl_options = {'UNDO'}

    def execute(self, context):
        space_data = context.space_data
        bpy.ops.object.camera_add(align='VIEW')
        camera = context.active_object
        camera["ID_PROMPT"] = "sn_object.camera_properties"
        bpy.ops.view3d.camera_to_view()
        camera.data.clip_start = space_data.clip_start
        camera.data.clip_end = space_data.clip_end
        camera.data.ortho_scale = 200.0
        space_data.region_3d.view_camera_offset = [0, 0]
        return {'FINISHED'}


class SNAP_OT_camera_properties(Operator):
    bl_idname = "sn_object.camera_properties"
    bl_label = "Camera Properties"

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, event):
        self.lock_camera = context.space_data.lock_camera
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)

    def draw(self, context):
        camera = context.active_object
        sn_utils.draw_object_info(self.layout, camera)
        sn_utils.draw_object_data(self.layout, camera)


class SNAP_OT_light_properties(Operator):
    bl_idname = "sn_object.light_properties"
    bl_label = "Light Properties"

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)

    def draw(self, context):
        light = context.active_object
        sn_utils.draw_object_info(self.layout, light)
        sn_utils.draw_object_data(self.layout, light)


class SNAP_OT_add_room_light(Operator):
    bl_idname = "sn_object.add_room_light"
    bl_label = "Add Room Lamp"
    bl_options = {'UNDO'}

    def invoke(self, context, event):
        view = context.space_data
        view.overlay.show_extras = True
        return self.execute(context)

    def execute(self, context):
        largest_x = 0
        largest_y = 0
        smallest_x = 0
        smallest_y = 0
        wall_assemblies = []
        wall_bps = []
        height = 0

        for obj in context.view_layer.objects:
            if obj.get('IS_BP_WALL'):
                wall_bps.append(obj.parent)
                wall_assemblies.append(sn_types.Wall(obj_bp=obj))

        for assembly in wall_assemblies:
            start_point = (
                assembly.obj_bp.matrix_world[0][3], assembly.obj_bp.matrix_world[1][3], 0)
            end_point = (
                assembly.obj_x.matrix_world[0][3], assembly.obj_x.matrix_world[1][3], 0)
            height = assembly.obj_z.location.z

            if start_point[0] > largest_x:
                largest_x = start_point[0]
            if start_point[1] > largest_y:
                largest_y = start_point[1]
            if start_point[0] < smallest_x:
                smallest_x = start_point[0]
            if start_point[1] < smallest_y:
                smallest_y = start_point[1]
            if end_point[0] > largest_x:
                largest_x = end_point[0]
            if end_point[1] > largest_y:
                largest_y = end_point[1]
            if end_point[0] < smallest_x:
                smallest_x = end_point[0]
            if end_point[1] < smallest_y:
                smallest_y = end_point[1]

        x = (math.fabs(largest_x) - math.fabs(smallest_x)) / 2
        y = (math.fabs(largest_y) - math.fabs(smallest_y)) / 2
        z = height

        width = math.fabs(smallest_y) + math.fabs(largest_y)
        length = math.fabs(largest_x) + math.fabs(smallest_x)
        if width == 0:
            width = sn_unit.inch(-48)
        if length == 0:
            length = sn_unit.inch(-48)

        bpy.ops.object.light_add(type='AREA')
        obj_lamp = context.active_object
        obj_lamp.location.x = x
        obj_lamp.location.y = y
        obj_lamp.location.z = z - sn_unit.inch(.01)
        obj_lamp.data.shape = 'RECTANGLE'
        obj_lamp.data.size = length
        obj_lamp.data.size_y = math.fabs(width)
        obj_lamp.data.energy = 120
        obj_lamp.data.use_shadow = False

        return {'FINISHED'}


class SN_OBJ_unwrap_mesh(Operator):
    bl_idname = "sn_object.unwrap_mesh"
    bl_label = "Unwrap Mesh"
    bl_options = {'UNDO'}
    
    object_name : StringProperty(name="Object Name")
    
    def execute(self, context):
        if self.object_name in bpy.data.objects:
            obj = bpy.data.objects[self.object_name]
            context.view_layer.objects.active = obj
        obj = context.active_object
        mode = obj.mode
        if obj.mode == 'OBJECT':
            bpy.ops.object.editmode_toggle()
            
        bpy.ops.mesh.select_all(action='SELECT')

        bpy.ops.uv.smart_project(angle_limit=1.15192)
        if mode == 'OBJECT':
            bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class SN_OBJ_add_material_slot(Operator):
    bl_idname = "sn_object.add_material_slot"
    bl_label = "Add Material Slot"
    bl_options = {'UNDO'}
    
    object_name : StringProperty(name="Object Name")
    
    def execute(self,context):
        obj = bpy.data.objects[self.object_name]
        override = {'active_object':obj,
                    'object':obj,
                    'window':context.window,
                    'region':context.region}
        bpy.ops.object.material_slot_add(override)
        return{'FINISHED'}


class OPS_add_machine_token(Operator):
    bl_idname = "snap.add_machine_token"
    bl_label = "Add Machine Token"

    token_name: StringProperty(name="Token Name", default="New Machine Token")
    token_type: EnumProperty(items=enum_machine_tokens, name="Machine Token Type")

    @classmethod
    def poll(cls, context):
        if context.object:
            if context.object.snap.type_mesh == 'CUTPART':
                return True
        return False

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=sn_utils.get_prop_dialog_width(400))

    def execute(self, context):
        token = context.object.snap.mp.machine_tokens.add()
        token.name = self.token_name
        token.type_token = self.token_type
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'token_name')


class OPS_delete_machine_token(Operator):
    bl_idname = "snap.delete_machine_token"
    bl_label = "Delete Machine Token"

    token_name: StringProperty(name="Token Name")

    @classmethod
    def poll(cls, context):
        if context.object:
            if context.object.snap.type_mesh == 'CUTPART':
                return True
        return False

    def execute(self, context):
        tokens = context.object.snap.mp.machine_tokens
        if self.token_name in tokens:
            for index, token in enumerate(tokens):
                if token.name == self.token_name:
                    tokens.remove(index)
                    break
        return {'FINISHED'}


classes = (
    SN_OBJ_override_object_context_menu,
    SN_OBJ_select_object,
    SNAP_OT_delete_object,
    SN_OBJ_toggle_edit_mode,
    SN_OBJ_clear_vertex_groups,
    SN_OBJ_assign_verties_to_vertex_group,
    SN_OBJ_draw_floor_plane,
    SNAP_OT_add_camera,
    SNAP_OT_camera_properties,
    SNAP_OT_light_properties,
    SNAP_OT_add_room_light,
    SN_OBJ_unwrap_mesh,
    SN_OBJ_add_material_slot,
    SN_OBJ_apply_hook_modifiers,
    OPS_add_machine_token,
    OPS_delete_machine_token,
    SN_OBJ_delete
)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
