"""
Microvellum 
Cabinet & Closet Designer
Stores the UI, Properties, and Operators for the cabinet and closet designer panel
the Panel definition is stored in an add-on.
"""

import bpy
import math
from os import path
from mv import fd_types, unit, utils
from bpy.app.handlers import persistent
from . import appliance_properties

class OPERATOR_Place_Countertop_Appliance(bpy.types.Operator):
    bl_idname = appliance_properties.LIBRARY_NAME_SPACE + ".place_countertop_appliance"
    bl_label = "Place Sink"
    bl_description = "This allows you to place a countertop appliance. The object that you select will automatically have a cutout for the appliance."
    bl_options = {'UNDO'}
    
    #READONLY
    object_name = bpy.props.StringProperty(name="Object Name")
    
    assembly = None

    def invoke(self, context, event):
        bp = bpy.data.objects[self.object_name]
        self.assembly = fd_types.Assembly(bp)
        utils.set_wireframe(self.assembly.obj_bp,True)
        context.window.cursor_set('PAINT_BRUSH')
        context.scene.update() # THE SCENE MUST BE UPDATED FOR RAY CAST TO WORK
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel_drop(self,context,event):
        if self.assembly:
            utils.delete_object_and_children(self.assembly.obj_bp)
        bpy.context.window.cursor_set('DEFAULT')
        return {'FINISHED'}

    def assign_boolean(self,obj):
        if obj:
            objs = utils.get_child_objects(self.assembly.obj_bp)
            for obj_bool in objs:
                if obj_bool.mv.use_as_bool_obj:
                    obj_bool.hide = True
                    mod = obj.modifiers.new(obj_bool.name,'BOOLEAN')
                    mod.object = obj_bool
                    mod.operation = 'DIFFERENCE'

    def sink_drop(self,context,event):
        selected_point, selected_obj = utils.get_selection_point(context,event)
        bpy.ops.object.select_all(action='DESELECT')
        sel_product_bp = utils.get_bp(selected_obj,'PRODUCT')
        sel_assembly_bp = utils.get_assembly_bp(selected_obj)

        if sel_product_bp and sel_assembly_bp:
            product = fd_types.Assembly(sel_product_bp)
            if product:
                product_depth = math.fabs(product.obj_y.location.y)
                assembly_depth = math.fabs(self.assembly.obj_y.location.y)
                self.assembly.obj_bp.parent = product.obj_bp
                self.assembly.obj_bp.location.z = product.obj_z.location.z + unit.inch(1.5)
                self.assembly.obj_bp.location.y = -math.fabs(product_depth-assembly_depth)/2
                self.assembly.obj_bp.location.x = product.obj_x.location.x/2 - self.assembly.obj_x.location.x/2

            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                self.assign_boolean(selected_obj)
                utils.set_wireframe(self.assembly.obj_bp,False)
                bpy.context.window.cursor_set('DEFAULT')
                bpy.ops.object.select_all(action='DESELECT')
                context.scene.objects.active = self.assembly.obj_bp
                self.assembly.obj_bp.select = True
                return {'FINISHED'}
        
        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        context.area.tag_redraw()
        
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}
        
        if event.type in {'ESC'}:
            self.cancel_drop(context,event)
            return {'FINISHED'}
        
        return self.sink_drop(context,event)

class OPERATOR_Place_Appliance_Object(bpy.types.Operator):
    bl_idname = appliance_properties.LIBRARY_NAME_SPACE + ".place_appliance_object"
    bl_label = "Place Appliance Object"
    bl_description = "This allows you to place an appliance object into the scene."
    bl_options = {'UNDO'}
    
    #READONLY
    object_name = bpy.props.StringProperty(name="Object Name")
    
    object = None
    
    def invoke(self, context, event):
        self.object = bpy.data.objects[self.object_name]
        context.window.cursor_set('PAINT_BRUSH')
        context.scene.update() # THE SCENE MUST BE UPDATED FOR RAY CAST TO WORK
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel_drop(self,context,event):
        if self.object:
            utils.delete_object_and_children(self.object)
        bpy.context.window.cursor_set('DEFAULT')
        return {'FINISHED'}

    def faucet_drop(self,context,event):
        selected_point, selected_obj = utils.get_selection_point(context,event)
        bpy.ops.object.select_all(action='DESELECT')
        
        if selected_obj:
            wall_bp = utils.get_wall_bp(selected_obj)
            if wall_bp:
                self.object.rotation_euler.z = wall_bp.rotation_euler.z
                
        self.object.location = selected_point
        
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            self.object.draw_type = 'TEXTURED'
            bpy.context.window.cursor_set('DEFAULT')
            bpy.ops.object.select_all(action='DESELECT')
            utils.set_wireframe(self.object,False)
            context.scene.objects.active = self.object
            self.object.select = True
            return {'FINISHED'}
        
        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        context.area.tag_redraw()
        
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}
        
        if event.type in {'ESC'}:
            self.cancel_drop(context,event)
            return {'FINISHED'}    
        
        return self.faucet_drop(context,event)

bpy.utils.register_class(OPERATOR_Place_Countertop_Appliance)
bpy.utils.register_class(OPERATOR_Place_Appliance_Object)