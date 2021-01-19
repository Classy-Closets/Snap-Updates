'''
Created on Dec 18, 2017

@author: Montes
'''

import bpy
from bpy.types import Operator

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       BoolVectorProperty,
                       PointerProperty,
                       EnumProperty,
                       CollectionProperty)

import math
# import os
from mv import utils, fd_types, unit
# import inspect
# import subprocess
# import sys


class OPS_add_annotation(bpy.types.Operator):
    bl_idname = "fd_2d_views.add_annotation"
    bl_label = "Add Annotation"

    annotation_text = bpy.props.StringProperty(name="Annotation Text",
                                          description="Enter in the name of the annoation")    

    header_text = "Place Annotation"
    
    annotation = None
    drawing_plane = None
    
    def place_annotation(self,context,event):
        selected_point, selected_obj = utils.get_selection_point(context,event,floor=self.drawing_plane)
        self.annotation.anchor.location = selected_point
        if event.type == 'LEFTMOUSE':
            return self.finish_drop(context, event)
        
        return {'RUNNING_MODAL'}
    
    def create_drawing_plane(self,context):
        bpy.ops.mesh.primitive_plane_add()
        self.drawing_plane = context.active_object
        self.drawing_plane.location = (0,0,0)
        self.drawing_plane.draw_type = 'WIRE'
        self.drawing_plane.dimensions = (100,100,1)   

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(550))

    def draw(self,context):
        layout = self.layout
        layout.prop(self,'annotation_text')

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        self.create_drawing_plane(context)
        
        self.annotation = fd_types.Dimension()
        self.annotation.end_x(value = unit.inch(0))
        self.annotation.anchor.select = True
        self.annotation.set_label(self.annotation_text)
        
        context.scene.objects.active = self.annotation.anchor
        bpy.ops.fd_general.toggle_dimension_handles(turn_on=True)
        context.window_manager.mv.use_opengl_dimensions = True
        
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
        
    def modal(self, context, event):
        context.area.tag_redraw()
        context.area.header_text_set(text=self.header_text)
        
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}
        
        if event.type in {'ESC'}:
            self.cancel_drop(context,event)
            return {'FINISHED'}
        
        return self.place_annotation(context,event)    
        
    def cancel_drop(self,context,event):
        utils.delete_object_and_children(self.annotation.anchor)
        utils.delete_object_and_children(self.drawing_plane)
        bpy.context.window.cursor_set('DEFAULT')
        return {'CANCELLED'}
        
    def finish_drop(self,context,event):
        utils.delete_object_and_children(self.drawing_plane)
        bpy.context.window.cursor_set('DEFAULT')
        context.area.header_text_set()
        return {'FINISHED'}


class OPS_add_dimension(Operator):
    bl_description = "Add Dimension to Selected Assembly"
    bl_idname = "fd_2d_views.add_dimension"
    bl_label = "Add Dimension" 
    bl_options = {'UNDO'}

    label = StringProperty(name="Dimension Label",
                           default="")
    
    offset = FloatProperty(name="Offset", subtype='DISTANCE')
    
    above_assembly_draw_to = EnumProperty(name="Draw to Above Assembly Top or Bottom",
                                          items=[('Top',"Top","Top"),
                                                 ('BOTTOM',"Bottom","Bottom")],
                                          default='BOTTOM')

    configuration = EnumProperty(name="configuration",
                                 items=[('WIDTH',"Width",'Width of Assembly'),
                                        ('HEIGHT',"Height",'Height of Assembly'),
                                        ('DEPTH',"Depth",'Depth of Assembly'),
                                        ('WALL_TOP',"Wall Top",'Top of Wall'),
                                        ('WALL_BOTTOM',"Wall Bottom",'Bottom of Wall'),
                                        ('WALL_LEFT',"Wall Left",'Left Wall End'),
                                        ('WALL_RIGHT',"Wall Right",'Right Wall End'),
                                        ('AVAILABLE_SPACE_ABOVE',"Available Space Above",'Available Space Above'),
                                        ('AVAILABLE_SPACE_BELOW',"Available Space Below",'Available Space Below'),
                                        ('AVAILABLE_SPACE_LEFT',"Available Space Left",'Available Space Left'),
                                        ('AVAILABLE_SPACE_RIGHT',"Available Space Right",'Available Space Right')],                                      
                                 default = 'WIDTH')
    
    dimension = None
    assembly = None
    wall = None
    del_dim = True
    neg_z_dim = False
    
    @classmethod
    def poll(cls, context):
        if utils.get_bp(context.object, 'PRODUCT'):
            return True   
        else:
            return False 
    
    def check(self, context):
        self.dimension.anchor.location = (0,0,0)
        self.dimension.end_point.location = (0,0,0)  
        
        self.dimension.set_label(self.label)
        
        if self.configuration in ['HEIGHT','WALL_TOP','WALL_BOTTOM','AVAILABLE_SPACE_ABOVE','AVAILABLE_SPACE_BELOW']:
            self.dimension.anchor.location.x += self.offset
        else:         
            self.dimension.anchor.location.z += self.offset
        
        if self.configuration == 'WIDTH':
            self.dimension.end_point.location.x =self.assembly.obj_x.location.x
            
        if self.configuration == 'HEIGHT':
            self.dimension.end_point.location.z = self.assembly.obj_z.location.z
            
        if self.configuration == 'DEPTH':
            self.dimension.end_point.location.y = self.assembly.obj_y.location.y            
            
        if self.configuration == 'WALL_TOP':
            if self.neg_z_dim == False:
                self.dimension.anchor.location.z = self.assembly.obj_z.location.z
                self.dimension.end_point.location.z = self.wall.obj_z.location.z -\
                                                      self.assembly.obj_bp.location.z -\
                                                      self.assembly.obj_z.location.z         
            else:
                self.dimension.end_point.location.z = self.wall.obj_z.location.z -\
                                                      self.assembly.obj_bp.location.z               
            
        if self.configuration == 'WALL_BOTTOM':
            if self.neg_z_dim == False:
                self.dimension.end_point.location.z = -self.assembly.obj_bp.location.z
            else:
                self.dimension.anchor.location.z = self.assembly.obj_z.location.z
                self.dimension.end_point.location.z = -self.assembly.obj_bp.location.z -\
                                                      self.assembly.obj_z.location.z
            
        if self.configuration == 'WALL_LEFT':
            self.dimension.end_point.location.x = -self.assembly.obj_bp.location.x
            
        if self.configuration == 'WALL_RIGHT': 
            self.dimension.anchor.location.x = self.assembly.obj_x.location.x
            self.dimension.end_point.location.x = self.wall.obj_x.location.x -\
                                                  self.assembly.obj_bp.location.x -\
                                                  self.assembly.obj_x.location.x
            
        if self.configuration == 'AVAILABLE_SPACE_ABOVE':
            if self.neg_z_dim == False:
                self.dimension.anchor.location.z = self.assembly.obj_z.location.z 
                assembly_dim_z = self.assembly.obj_z.location.z
            else:
                assembly_dim_z = 0.0                
            
            assembly_a = self.assembly.get_adjacent_assembly(direction='ABOVE')
            
            if assembly_a:
                above_assembly_loc_z = assembly_a.obj_bp.location.z
                
                if self.above_assembly_draw_to == 'BOTTOM':                                                           
                    above_assembly_dim_z = assembly_a.obj_z.location.z
                    self.dimension.end_point.location.z = above_assembly_loc_z +\
                                                          above_assembly_dim_z -\
                                                          self.assembly.obj_bp.location.z -\
                                                          assembly_dim_z 
                                                                                                                        
                else:
                    self.dimension.end_point.location.z = above_assembly_loc_z -\
                                                          self.assembly.obj_bp.location.z -\
                                                          assembly_dim_z                    
               
            else:
                self.dimension.end_point.location.z = self.wall.obj_z.location.z -\
                                                      self.assembly.obj_bp.location.z -\
                                                      assembly_dim_z
         
        if self.configuration == 'AVAILABLE_SPACE_BELOW':
            if self.assembly.obj_z.location.z < 0:
                self.dimension.anchor.location.z = self.assembly.obj_z.location.z
            
            assembly_b = self.assembly.get_adjacent_assembly(direction='BELOW')
            if assembly_b:
                if self.neg_z_dim == False:
                    self.dimension.end_point.location.z = -self.assembly.obj_bp.location.z +\
                                                          assembly_b.obj_bp.location.z +\
                                                          assembly_b.obj_z.location.z
                else:
                    self.dimension.end_point.location.z = -self.assembly.obj_bp.location.z -\
                                                          self.assembly.obj_z.location.z +\
                                                          assembly_b.obj_bp.location.z +\
                                                          assembly_b.obj_z.location.z
            else:
                self.dimension.end_point.location.z = -self.assembly.obj_bp.location.z
        
        if self.configuration == 'AVAILABLE_SPACE_LEFT':
            if self.assembly.get_adjacent_assembly(direction='LEFT'):
                self.dimension.end_point.location.x = -self.assembly.obj_bp.location.x +\
                                                      self.assembly.get_adjacent_assembly(direction='LEFT').obj_bp.location.x +\
                                                      self.assembly.get_adjacent_assembly(direction='LEFT').obj_x.location.x
            else:
                self.dimension.end_point.location.x = -self.assembly.obj_bp.location.x
            
        if self.configuration == 'AVAILABLE_SPACE_RIGHT':
            self.dimension.anchor.location.x = self.assembly.obj_x.location.x
            if self.assembly.get_adjacent_assembly(direction='RIGHT'):
                self.dimension.end_point.location.x = self.assembly.get_adjacent_assembly(direction='RIGHT').obj_bp.location.x -\
                                                      self.assembly.obj_bp.location.x -\
                                                      self.assembly.obj_x.location.x           
            else:
                self.dimension.end_point.location.x = self.wall.obj_x.location.x -\
                                                      self.assembly.obj_bp.location.x -\
                                                      self.assembly.obj_x.location.x
                                                            
        return True
    
    def __del__(self):
        if self.del_dim == True:
            obj_del = []
            obj_del.append(self.dimension.anchor)
            obj_del.append(self.dimension.end_point)
            utils.delete_obj_list(obj_del)
    
    def invoke(self, context, event):
        wm = context.window_manager
        
        if wm.mv.use_opengl_dimensions == False:
            wm.mv.use_opengl_dimensions = True
        
        if context.object:
            obj_wall_bp = utils.get_wall_bp(context.object)
            if obj_wall_bp:
                self.wall = fd_types.Wall(obj_wall_bp)
                
#             obj_assembly_bp = utils.get_parent_assembly_bp(context.object)
            obj_assembly_bp = utils.get_bp(context.object, 'PRODUCT')
            if obj_assembly_bp:
                self.assembly = fd_types.Assembly(obj_assembly_bp)
                wall_bp = utils.get_wall_bp(obj_assembly_bp)
                self.wall = fd_types.Wall(wall_bp)
        
        self.dimension = fd_types.Dimension()
        self.dimension.set_color(value=7)
        self.dimension.parent(obj_assembly_bp)
        self.dimension.end_point.location.x = self.assembly.obj_x.location.x
        
        if self.assembly.obj_z.location.z < 0:
            self.neg_z_dim = True
        else:
            self.neg_z_dim = False
            
        self.configuration = 'WIDTH'
        self.label = ""
        
        
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(550))
    
    def execute(self, context):
        self.del_dim = False
        self.dimension.set_color(value=0)
        self.dimension.anchor.hide = False
        self.dimension.end_point.hide = False
        
        if self.label != "":
            self.dimension.set_label(self.label)
        
        wall_dim_x = self.wall.get_var("dim_x", "wall_dim_x")
        wall_dim_z = self.wall.get_var("dim_z", "wall_dim_z")
        
        assembly_loc_x = self.assembly.get_var("loc_x", "assembly_loc_x")
        assembly_loc_z = self.assembly.get_var("loc_z", "assembly_loc_z")
        assembly_dim_x = self.assembly.get_var("dim_x", "assembly_dim_x")
        assembly_dim_z = self.assembly.get_var("dim_z", "assembly_dim_z")        
        
        assembly_l = self.assembly.get_adjacent_assembly(direction='LEFT')
        if assembly_l:
            assembly_l_loc_x = assembly_l.get_var("loc_x", "assembly_l_loc_x")
            assembly_l_dim_x = assembly_l.get_var("dim_x", "assembly_l_dim_x")               
        
        assembly_r = self.assembly.get_adjacent_assembly(direction='RIGHT')
        if assembly_r:
            assembly_r_loc_x = assembly_r.get_var("loc_x", "assembly_r_loc_x")
            
        assembly_a = self.assembly.get_adjacent_assembly(direction='ABOVE')
        if assembly_a:
            assembly_a_loc_z = assembly_a.get_var("loc_z", "assembly_a_loc_z")
            assembly_a_dim_z = assembly_a.get_var("dim_z", "assembly_a_dim_z")
        
        assembly_b = self.assembly.get_adjacent_assembly(direction="BELOW")
        if assembly_b:
            assembly_b_loc_z = assembly_b.get_var("loc_z", "assembly_b_loc_z")
            assembly_b_dim_z = assembly_b.get_var("dim_z", "assembly_b_dim_z")
        
        if self.configuration == 'WIDTH':
            self.dimension.end_x(expression="dim_x",driver_vars=[self.assembly.get_var("dim_x")])
            
        if self.configuration == 'HEIGHT':
            self.dimension.end_z(expression="dim_z",driver_vars=[self.assembly.get_var("dim_z")])
            
        if self.configuration == 'DEPTH':
            self.dimension.end_y(expression="dim_y",driver_vars=[self.assembly.get_var("dim_y")])            
            
        if self.configuration == 'WALL_TOP':
            if self.neg_z_dim == False: 
                self.dimension.start_z(expression="assembly_dim_z", 
                                       driver_vars=[assembly_dim_z])
                
                self.dimension.end_z(expression="wall_dim_z-assembly_loc_z-assembly_dim_z",
                                     driver_vars=[wall_dim_z, assembly_loc_z, assembly_dim_z])
            else:
                self.dimension.end_z(expression="wall_dim_z-assembly_loc_z", 
                                     driver_vars=[wall_dim_z,assembly_loc_z])
            
        if self.configuration == 'WALL_BOTTOM':
            if self.neg_z_dim == False:
                self.dimension.end_z(expression="-assembly_loc_z",driver_vars=[assembly_loc_z])
            else:
                self.dimension.start_z(expression="assembly_dim_z", driver_vars=[assembly_dim_z])
                self.dimension.end_z(expression="-assembly_loc_z-assembly_dim_z",
                                     driver_vars=[assembly_loc_z, assembly_dim_z])
            
        if self.configuration == 'WALL_LEFT':
            self.dimension.end_x(expression="-assembly_loc_x",driver_vars=[assembly_loc_x])
            
        if self.configuration == 'WALL_RIGHT': 
            self.dimension.start_x(expression="dim_x", driver_vars=[self.assembly.get_var("dim_x")])
            self.dimension.end_x(expression="wall_dim_x-assembly_dim_x-assembly_loc_x", 
                                 driver_vars=[wall_dim_x, assembly_dim_x, assembly_loc_x])
            
        if self.configuration == 'AVAILABLE_SPACE_ABOVE':
            if assembly_a:
                self.dimension.start_z(expression="dim_z", driver_vars=[self.assembly.get_var("dim_z")])
                
                if self.above_assembly_draw_to == 'BOTTOM':
                    self.dimension.end_z(expression="assembly_a_loc_z+assembly_a_dim_z-assembly_loc_z-assembly_dim_z", 
                                         driver_vars=[assembly_a_loc_z,
                                                      assembly_a_dim_z,
                                                      assembly_loc_z,
                                                      assembly_dim_z])                     
                else:
                    self.dimension.end_z(expression="assembly_a_loc_z-assembly_loc_z-assembly_dim_z", 
                                         driver_vars=[assembly_a_loc_z,
                                                      assembly_loc_z,
                                                      assembly_dim_z])                   
            else:
                if self.neg_z_dim == False:
                    self.dimension.end_z(expression="wall_dim_z-assembly_loc_z-assembly_dim_z", 
                                         driver_vars=[wall_dim_z,
                                                      assembly_loc_z,
                                                      assembly_dim_z])
                else:
                    self.dimension.end_z(expression="wall_dim_z-assembly_loc_z", 
                                         driver_vars=[wall_dim_z,
                                                      assembly_loc_z])
         
        if self.configuration == 'AVAILABLE_SPACE_BELOW':
            if assembly_b:
                if self.neg_z_dim == False:
                    self.dimension.end_z(expression="-assembly_loc_z+assembly_b_loc_z+assembly_b_dim_z", 
                                         driver_vars=[assembly_loc_z,
                                                      assembly_b_loc_z,
                                                      assembly_b_dim_z])
                else:
                    self.dimension.start_z(expression="assembly_dim_z",driver_vars=[assembly_dim_z])
                    self.dimension.end_z(expression="-assembly_loc_z-assembly_dim_z+assembly_b_loc_z+assembly_b_dim_z",
                                         driver_vars=[assembly_loc_z,
                                                      assembly_dim_z,
                                                      assembly_b_loc_z,
                                                      assembly_b_dim_z])
            else:
                self.dimension.end_z(expression="-loc_z", 
                                     driver_vars=[self.assembly.get_var("loc_z")])
        
        if self.configuration == 'AVAILABLE_SPACE_LEFT':
            if assembly_l:
                self.dimension.end_x(expression="-assembly_loc_x+assembly_l_loc_x+assembly_l_dim_x", 
                                     driver_vars=[assembly_l_loc_x,
                                                  assembly_loc_x,
                                                  assembly_l_dim_x])
            else:
                self.dimension.end_x(expression="-assembly_loc_x", driver_vars=[assembly_loc_x])
            
        if self.configuration == 'AVAILABLE_SPACE_RIGHT':
            self.dimension.start_x(expression="dim_x", driver_vars=[self.assembly.get_var("dim_x")])
            if assembly_r:
                self.dimension.end_x(expression="assembly_r_loc_x-assembly_loc_x-assembly_dim_x", 
                                     driver_vars=[assembly_r_loc_x,
                                                  assembly_loc_x,
                                                  assembly_dim_x])    
                
            else:
                self.dimension.end_x(expression="wall_dim_x-assembly_loc_x-assembly_dim_x", 
                                     driver_vars=[wall_dim_x,
                                                  assembly_loc_x,
                                                  assembly_dim_x])
        
        return {'FINISHED'}    
    
    def draw(self,context):
        layout = self.layout
        config_box = layout.box()  
        config_box.label("Configuration")
        
        row = config_box.row()
        split1 = row.split(align=True)
        split1.label("Assembly Dimension: ")
        split1.prop_enum(self, "configuration", 'WIDTH')
        split1.prop_enum(self, "configuration", 'HEIGHT')
        split1.prop_enum(self, "configuration", 'DEPTH')
        
        row = config_box.row()
        split2 = row.split(align=True)
        split2.label("To Wall: ")
        split2.prop_enum(self, "configuration", 'WALL_LEFT', text="Left")
        split2.prop_enum(self, "configuration", 'WALL_RIGHT', text="Right")
        split2.prop_enum(self, "configuration", 'WALL_TOP', text="Top")
        split2.prop_enum(self, "configuration", 'WALL_BOTTOM', text="Bottom")
        
        row = config_box.row()
        split3 = row.split(align=True)
        split3.label("Available Space: ")
        split3.prop_enum(self, "configuration", 'AVAILABLE_SPACE_LEFT', text="Left")
        split3.prop_enum(self, "configuration", 'AVAILABLE_SPACE_RIGHT', text="Right")
        split3.prop_enum(self, "configuration", 'AVAILABLE_SPACE_ABOVE', text="Above")
        split3.prop_enum(self, "configuration", 'AVAILABLE_SPACE_BELOW', text="Below")
            
        if self.configuration == 'AVAILABLE_SPACE_ABOVE' and self.assembly.get_adjacent_assembly(direction='ABOVE'):
            row = config_box.row()
            row.prop(self, "above_assembly_draw_to", text="Draw to Above Assembly")                            
        
        box2 = layout.box()
        col = box2.column()
        col.prop(self, "label", text="Label")
        col.prop(self, "offset", text="Offset")


class OPS_dimension_options(Operator):
    bl_idname = "fd_2d_views.dimension_options"
    bl_label = "Dimension Global Options"

    info = {}

    @classmethod
    def poll(cls, context):
        return True

    def check(self, context):
        return True

    def execute(self, context):
        pass
        return {'FINISHED'}
        
    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(320))
        
    def draw(self, context):
        wm = context.window_manager.mv
        scene = context.scene
        dim_props = scene.mv.opengl_dim
        sys_units = scene.unit_settings.system
        layout = self.layout
        box = layout.box()
        
        row = box.row()
        
        if dim_props.gl_dim_units == 'AUTO':
            row.label("Units:" +
                      "                    (" +
                      sys_units.title() +
                      ")")
        else:
            row.label("Units:")
        
        row.prop(dim_props, 'gl_dim_units', text="")
        
        row = box.row()
        row.label("Arrow Type:")
        row.prop(dim_props, 'gl_arrow_type', text="")
        row = box.row()
        row.label("Color:")        
        row.prop(dim_props, 'gl_default_color', text="")        
        row = box.row()
        
        if dim_props.gl_dim_units in ('INCH', 'FEET') or dim_props.gl_dim_units == 'AUTO' and sys_units == 'IMPERIAL':
            row.label("Round to the nearest:")
            row.prop(dim_props, 'gl_imperial_rd_factor', text="")
            row = box.row()
            row.label("Number format:")
            row.prop(dim_props, 'gl_number_format', text="")
            
        else:         
            row.label("Precision:")
            row.prop(dim_props, 'gl_precision',text="")
        
        row = box.row()
        row.label("Text Size:")
        row.prop(dim_props, 'gl_font_size',text="")
        row = box.row()
        row.label("Arrow Size:")        
        row.prop(dim_props, 'gl_arrow_size', text="")


class OPS_create_single_dimension(Operator):
    bl_idname = "fd_2d_views.create_single_dimension"
    bl_label = "Create Single Dimension"
 
    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        dim = fd_types.Dimension()
        dim.end_x(value = unit.inch(0))
        dim.anchor.select = True
        context.scene.objects.active = dim.anchor
        bpy.ops.fd_2d_views.toggle_dimension_handles(turn_on=True)
        context.window_manager.mv.use_opengl_dimensions = True
        return {'FINISHED'}

    
class OPS_toggle_dimension_handles(Operator):
    bl_idname = "fd_2d_views.toggle_dimension_handles"
    bl_label = "Toggle Dimension Handles"

    turn_on = BoolProperty(name="Turn On",default=False)

    def execute(self, context):
        for obj in context.scene.objects:
            if obj.mv.type == 'VISDIM_A':
                obj.empty_draw_type = 'SPHERE'
                obj.empty_draw_size = unit.inch(1)
                obj.hide = False if self.turn_on else True
            elif obj.mv.type == 'VISDIM_B':
                obj.rotation_euler.z = math.radians(-90)
                obj.empty_draw_type = 'PLAIN_AXES'
                obj.empty_draw_size = unit.inch(2)
                obj.hide = False if self.turn_on else True
        return {'FINISHED'}


class OPS_dimension_interface(Operator):
    bl_idname = "fd_2d_views.dimension_interface"
    bl_label = "Dimension Global Options"
 
    info = {}
 
    @classmethod
    def poll(cls, context):
        return True
 
    def check(self, context):
        return True
 
    def execute(self, context):
        pass
        return {'FINISHED'}
         
    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(320))
         
    def draw(self, context):
        wm = context.window_manager.mv
        scene = context.scene
        dim_props = scene.mv.opengl_dim
        sys_units = scene.unit_settings.system
        layout = self.layout
        box = layout.box()
         
        row = box.row()
         
        if dim_props.gl_dim_units == 'AUTO':
            row.label("Units:" +
                      "                    (" +
                      sys_units.title() +
                      ")")
        else:
            row.label("Units:")
         
        row.prop(dim_props, 'gl_dim_units', text="")
         
        row = box.row()
        row.label("Arrow Type:")
        row.prop(dim_props, 'gl_arrow_type', text="")
        row = box.row()
        row.label("Color:")        
        row.prop(dim_props, 'gl_default_color', text="")        
        row = box.row()
         
        if dim_props.gl_dim_units == 'FEET' or dim_props.gl_dim_units == 'AUTO' and sys_units == 'IMPERIAL':
            row.label("Round to the nearest:")
            row.prop(dim_props, 'gl_imperial_rd_factor', text="")
            row = box.row()
            row.label("Number format:")
            row.prop(dim_props, 'gl_number_format', text="")
        elif dim_props.gl_dim_units == 'INCH' and sys_units == 'IMPERIAL':
            row.label("Precision:")
            row.prop(dim_props, 'gl_precision',text="")
            row = box.row()
            row.label("Number format:")
            row.prop(dim_props, 'gl_number_format', text="")
        else:         
            row.label("Precision:")
            row.prop(dim_props, 'gl_precision',text="")
         
        row = box.row()
        row.label("Text Size:")
        row.prop(dim_props, 'gl_font_size',text="")
        row = box.row()
        row.label("Arrow Size:")        
        row.prop(dim_props, 'gl_arrow_size', text="")

#------REGISTER
classes = [
           OPS_dimension_options,
           OPS_toggle_dimension_handles,
           OPS_add_annotation,
           OPS_create_single_dimension,
           OPS_add_dimension,
           OPS_dimension_interface
           ]

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

# if __name__ == "__main__":
#     register()