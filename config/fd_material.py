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

import bpy
import os
import re
import inspect
from mv import utils, unit
from bpy.types import Header, Menu, Operator

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       BoolVectorProperty,
                       PointerProperty,
                       EnumProperty)

class OPS_clear_unused_materials_from_file(Operator):
    bl_idname = "fd_material.clear_unused_materials_from_file"
    bl_label = "Clear Unused Materials From File"
    bl_options = {'UNDO'}
    
    def execute(self,context):
        for mat in bpy.data.materials:
            if mat.users == 0:
                bpy.data.materials.remove(mat)
        return{'FINISHED'}

#THIS IS BEING USED BY frameless library addon
class OPS_apply_materials_from_pointers(Operator):
    bl_idname = "fd_material.apply_materials_from_pointers"
    bl_label = "Apply Materials From Pointers"
    bl_options = {'UNDO'}
    
    def execute(self,context):
        for obj in bpy.data.objects:
            utils.assign_materials_from_pointers(obj)
        return{'FINISHED'}

class OPS_add_material_slot(Operator):
    bl_idname = "fd_material.add_material_slot"
    bl_label = "Add Material Slot"
    bl_options = {'UNDO'}
    
    object_name = StringProperty(name="Object Name")
    
    def execute(self,context):
        obj = bpy.data.objects[self.object_name]
        obj.mv.material_slot_col.add()
        override = {'active_object':obj,'object':obj}
        bpy.ops.object.material_slot_add(override)
#         for obj in bpy.data.objects:
#             obj.mv.assign_materials_from_pointers(obj.name)
        return{'FINISHED'}

class OPS_fix_texture_paths(Operator):
    bl_idname = "fd_material.fix_texture_paths"
    bl_label = "Fix Texture Paths"
    bl_options = {'UNDO'}
    bl_description = "This will set all of the image filepaths to c:\\fluidtextures"
    
    def execute(self,context):
        for image in bpy.data.images:
            image.filepath = "C:\\fluidtextures\\" + image.name
        return{'FINISHED'}

class OPS_material_properties(Operator):
    bl_idname = "fd_material.material_properties"
    bl_label = "Material Properties"
    bl_options = {'UNDO'}

    material_name = StringProperty(name="Material Name")

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(400))

    def draw(self, context):
        material = bpy.data.materials[self.material_name]
        layout = self.layout
        layout.label(material.name)
        for node in material.node_tree.nodes:
            if node.type == 'MAPPING':
                box = layout.box()
                col = box.column()
                col.label(node.name)
                col.prop(node,'scale')
                col = box.column()
                col.prop(node,'rotation',index=2)
                
class OPS_clear_material_copies(Operator):
    bl_idname = "fd_material.clear_material_copies"
    bl_label = "Clear Duplicate Materials"
    bl_options = {'UNDO'}
    
    def execute(self, context):         
        import re
        
        materials = bpy.data.materials    
             
        for obj in bpy.context.scene.objects:
            for mat_slot in obj.material_slots:
                if mat_slot.material:
                    if re.search('[.][0-9][0-9][0-9]', mat_slot.material.name):
                        
                        try: 
                            mat_slot.material = materials[mat_slot.material.name.split(sep=".")[0]]
                        
                        except:
                            mat_slot.material.name = mat_slot.material.name.split(sep=".")[0]
        
        for mat in materials:
            if mat.users < 1:
                materials.remove(mat)
                    
        return {'FINISHED'}                
  
class OPS_create_material_library(Operator):
    bl_idname = "fd_material.create_mat_lib"
    bl_label = "Create Material Library"
    bl_options = {'UNDO'}
    
    def clear(self):
        self.clear_imgs()
        self.clear_mats()    
    
    def clear_imgs(self):
        for img in self.images:
            img.user_clear()
            self.images.remove(img)
            
    def clear_mats(self):
        for mat in self.materials:
            if mat.name == self.original_mat_name:
                pass
            else:
                mat.user_clear()
                self.materials.remove(mat)                                     

    def execute(self, context):
        scene = context.scene.materiallib
        images = bpy.data.images
        materials = bpy.data.materials 
        diffuse_textures = []
        spec_textures = []
        gloss_textures = []
        normal_textures = []
        displace_textures = []
        
        #get material to  copy
        base_material = bpy.data.materials[scene.active_material_index]
        
        #load diffuse images
        if scene.diffuse_path:
            for file in os.listdir(bpy.path.abspath(scene.diffuse_path)):
                diffuse_textures.append(file)
            
        #load spec images
        if scene.spec_path:
            for file in os.listdir(bpy.path.abspath(scene.spec_path)):
                spec_textures.append(file)
                                            
        #load gloss images
        if scene.gloss_path:        
            for file in os.listdir(bpy.path.abspath(scene.gloss_path)):
                gloss_textures.append(file)
                                            
        #load normal images
        if scene.normal_path:        
            for file in os.listdir(bpy.path.abspath(scene.normal_path)):
                normal_textures.append(file)
                                            
        #load displace images
        if scene.displace_path:        
            for file in os.listdir(bpy.path.abspath(scene.displace_path)):
                displace_textures.append(file)      
            
        for tex in diffuse_textures:    
            if tex not in images:
                images.load(bpy.path.abspath(scene.diffuse_path) + "/" + tex)
            
            #Create material    
            if tex.split(".")[0] not in materials:
                material = base_material.copy()
                material.use_fake_user = True
                material.name = tex.split(".")[0]             
                       
                #add cycles textures
                for node in material.node_tree.nodes:
                    if node.label == 'Diffuse Map':
                        node.image = images[tex]   
                    elif node.select == True:
                        node.image = images[tex]
                
                #Add BI textures
                if scene.use_internal_render_material:
                    for node in material.node_tree.nodes:
                        if node.type == 'MATERIAL':
                            node.material = material
                    
                    for t_slot in material.texture_slots:
                        if t_slot: 
                            new_tex = t_slot.texture.copy()
                            new_tex.name = str(material.name) + " Diffuse"
                            new_tex.image = images[tex]
                            t_slot.texture = new_tex
                            
        base_material.user_clear()
        base_material.use_fake_user = True     
                    
        return {'FINISHED'}                    
                
class OPS_create_material_template(Operator):
    bl_idname = "fd_material.create_mat_template"
    bl_label = "Create Material Template"
    bl_options = {'UNDO'}       
    
    material_name = StringProperty(name="Template Material Name")
    
    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(400))

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "material_name", text="Material Name")    
    
    def execute(self, context):         
        mat_temp = bpy.data.materials.new(self.material_name)
        #Cycles
        mat_temp.use_nodes = True
        nodes = mat_temp.node_tree.nodes
        
        cycles_frame = nodes.new("NodeFrame")
        cycles_frame.name = "Cycles"
        cycles_frame.label = "Cycles"
        
        node_material_output = nodes.new("ShaderNodeOutputMaterial")
        node_material_output.parent = cycles_frame
        node_material_output.location.x = 600 
        node_material_output.location.y = -500  
        
        node_glossy_shader = nodes.new("ShaderNodeBsdfGlossy")
        node_glossy_shader.parent = cycles_frame
        node_glossy_shader.location.x = 400 
        node_glossy_shader.location.y = -250        
        
        node_diffuse_shader = nodes.new("ShaderNodeBsdfDiffuse")
        node_diffuse_shader.parent = cycles_frame
        node_diffuse_shader.location.x = 400 
        node_diffuse_shader.location.y = -500                         
        
        node_layer_weight = nodes.new("ShaderNodeLayerWeight")
        node_layer_weight.parent = cycles_frame
        node_layer_weight.location.x = 200       
        
        node_mapping = nodes.new("ShaderNodeMapping")
        node_mapping.parent = cycles_frame
        node_mapping.location.x = -400 
        node_mapping.location.y = -500         
        
        node_tex_coord = nodes.new("ShaderNodeTexCoord")
        node_tex_coord.parent = cycles_frame
        node_tex_coord.location.x = -600 
        node_tex_coord.location.y = -500         
        
        node_gloss = nodes.new("ShaderNodeTexImage")
        node_gloss.name = "Gloss Map"
        node_gloss.label = "Gloss Map"
        node_gloss.parent = cycles_frame
        mat_temp.node_tree.links.new(node_mapping.outputs["Vector"], node_gloss.inputs["Vector"])
        
        node_spec = nodes.new("ShaderNodeTexImage")
        node_spec.name = "Spec Map"
        node_spec.label = "Spec Map"
        node_spec.parent = cycles_frame
        node_spec.location.y = -250
        mat_temp.node_tree.links.new(node_mapping.outputs["Vector"], node_spec.inputs["Vector"])
        
        node_diffuse = nodes.new("ShaderNodeTexImage")
        node_diffuse.name = "Diffuse Map"
        node_diffuse.label = "Diffuse Map"
        node_diffuse.parent = cycles_frame 
        node_diffuse.location.y = -500
        mat_temp.node_tree.links.new(node_mapping.outputs["Vector"], node_diffuse.inputs["Vector"])
        
        node_normal = nodes.new("ShaderNodeTexImage")
        node_normal.name = "Normal Map"
        node_normal.label = "Normal Map"
        node_normal.parent = cycles_frame
        node_normal.location.y = -750      
        mat_temp.node_tree.links.new(node_mapping.outputs["Vector"], node_normal.inputs["Vector"])
        
        node_normal_map = nodes.new("ShaderNodeNormalMap")
        node_normal_map.parent = cycles_frame   
        node_normal_map.location.x = 200    
        node_normal_map.location.y = -750
        mat_temp.node_tree.links.new(node_normal.outputs["Color"], node_normal_map.inputs["Color"])       
        
        node_displace = nodes.new("ShaderNodeTexImage")
        node_displace.name = "Displace Map"
        node_displace.label = "Displace Map"
        node_displace.parent = cycles_frame
        node_displace.location.y = -1000
        mat_temp.node_tree.links.new(node_mapping.outputs["Vector"], node_displace.inputs["Vector"])
        
        #Blender Internal
        BI_frame = nodes.new("NodeFrame")
        BI_frame.name = "Blender Internal"
        BI_frame.label = "Blender Internal" 
        
        for node in nodes:
            if node.type == 'MATERIAL':
                node.parent = BI_frame
                node.material = mat_temp
            if node.type == 'OUTPUT':    
                node.parent = BI_frame
        
            #need to attach alpha node inputs/outputs between BI mat_node and output_node
        
        BI_frame.location.y = 200  
                 
        return{'FINISHED'}
                
class OPS_change_product_spec_group(Operator):
    """ This change the products spec group.
    """
    bl_idname = "fd_material.change_product_spec_group"
    bl_label = "Change Product Specification Group"
    bl_description = "This changes the products specification group"
    bl_options = {'UNDO'}

    object_name = StringProperty(name="Object Name")
    spec_group_name = StringProperty(name="Spec Group Name")

    def change_spec_group_for_children(self,obj_bp,spec_group_name):
        for index, spec_group in enumerate(bpy.context.scene.mv.spec_groups):
            if spec_group.name == spec_group_name:
                spec_group_index = index
        
        obj_bp.cabinetlib.spec_group_name = spec_group_name
        obj_bp.cabinetlib.spec_group_index = spec_group_index
        for child in obj_bp.children:
            child.cabinetlib.spec_group_name = spec_group_name
            child.cabinetlib.spec_group_index = spec_group_index

            try:
                from snap_db import utils as sn_utils
                sn_utils.assign_materials_from_pointers(child)
            except ImportError:
                utils.assign_materials_from_pointers(child)
            
            if len(child.children) > 0:
                self.change_spec_group_for_children(child,spec_group_name)

    def execute(self, context):
        product_bp = bpy.data.objects[self.object_name]
        self.change_spec_group_for_children(product_bp,self.spec_group_name)
        return {'FINISHED'}

class OPS_change_active_spec_group(Operator):
    """ This change the products spec group.
    """
    bl_idname = "fd_material.change_active_spec_group"
    bl_label = "Change Product Specification Group"
    bl_description = "This changes the active specification group"
    bl_options = {'UNDO'}

    spec_group_name = StringProperty(name="Spec Group Name")

    def execute(self, context):
        spec_groups = context.scene.mv.spec_groups
        for index, spec_group in enumerate(spec_groups):
            if spec_group.name == self.spec_group_name:
                context.scene.cabinetlib.spec_group_index = index
        return {'FINISHED'}

class OPS_clear_spec_group(Operator):
    """ This will clear all the spec groups to save on file size.
    """
    bl_idname = "fd_material.clear_spec_group"
    bl_label = "Clear Specification Groups"
    bl_description = "This will clear all the spec group information from this file"
    bl_options = {'UNDO'}

    def execute(self, context):
        spec_groups = context.scene.mv.spec_groups
        for i in spec_groups:
            spec_groups.remove(0)
        return {'FINISHED'}

    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(400))

    def draw(self, context):
        layout = self.layout
        layout.label('Do you want to clear all specification group information?')

class OPS_copy_selected_spec_group(Operator):
    """ This will copy the selected specification group.
    """
    bl_idname = "fd_material.copy_selected_spec_group"
    bl_label = "Copy Selected Spec Group"
    bl_description = "This will copy the selected specification group"
    bl_options = {'UNDO'}

    new_name = StringProperty(name="New Name",
                              default="New Specification Group")

    def execute(self, context):
        spec_groups = context.scene.mv.spec_groups
        selected_spec_group = spec_groups[context.scene.mv.spec_group_index]
        if self.new_name not in spec_groups:
            new_spec_group = spec_groups.add()
            new_spec_group.name = self.new_name
            
            for mat_pointer in selected_spec_group.materials:
                new_mat_pointer = new_spec_group.materials.add()
                new_mat_pointer.name = mat_pointer.name
                new_mat_pointer.library_name = mat_pointer.library_name
                new_mat_pointer.category_name = mat_pointer.category_name
                new_mat_pointer.item_name = mat_pointer.item_name
            
            for cutpart_pointer in selected_spec_group.cutparts:
                new_cutpart_pointer = new_spec_group.cutparts.add()
                new_cutpart_pointer.name = cutpart_pointer.name
                new_cutpart_pointer.mv_pointer_name = cutpart_pointer.mv_pointer_name
                new_cutpart_pointer.thickness = cutpart_pointer.thickness
                new_cutpart_pointer.core = cutpart_pointer.core
                new_cutpart_pointer.top = cutpart_pointer.top
                new_cutpart_pointer.bottom = cutpart_pointer.bottom

            for edgepart_pointer in selected_spec_group.edgeparts:
                new_edgepart_pointer = new_spec_group.edgeparts.add()
                new_edgepart_pointer.name = edgepart_pointer.name
                new_edgepart_pointer.mv_pointer_name = edgepart_pointer.mv_pointer_name
                new_edgepart_pointer.thickness = edgepart_pointer.thickness
                new_edgepart_pointer.material = edgepart_pointer.material

        else:
            pass # RETURN ERROR
        return {'FINISHED'}

    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(400))

    def draw(self, context):
        layout = self.layout
        layout.prop(self,'new_name')


class OPS_delete_spec_group(Operator):
    """ This will delete the a specification group.
    """
    bl_idname = "fd_material.delete_spec_group"
    bl_label = "Delete Specification Group"
    bl_description = "This will delete the selected specification group. You must have at least one specification group"
    bl_options = {'UNDO'}

    spec_group_name = StringProperty(name="New Name",
                                     default="New Specification Group")

    @classmethod
    def poll(cls, context):
        spec_groups = context.scene.mv.spec_groups
        if len(spec_groups) > 1:
            return True
        else:
            return False

    def execute(self, context):
        spec_groups = context.scene.mv.spec_groups
        if self.spec_group_name in spec_groups:
            for index, spec_group in enumerate(spec_groups):
                if spec_group.name == self.spec_group_name:
                    spec_groups.remove(index)

        else:
            pass # RETURN ERROR
        return {'FINISHED'}

    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(400))

    def draw(self, context):
        layout = self.layout
        layout.label('Do you want to delete ' + self.spec_group_name)

class OPS_rename_spec_group(Operator):
    """ This will delete the a specification group.
    """
    bl_idname = "fd_material.rename_spec_group"
    bl_label = "Rename Specification Group"
    bl_description = "This will allow you to rename the selected specification group."
    bl_options = {'UNDO'}

    new_spec_group_name = StringProperty(name="New Name",
                                         default="New Specification Group")

    old_spec_group_name = ""
    
    def execute(self, context):
        spec_group = context.scene.mv.spec_groups[context.scene.mv.spec_group_index]
        spec_group.name = self.new_spec_group_name
        for obj in bpy.data.objects:
            if obj.cabinetlib.spec_group_name == self.old_spec_group_name:
                obj.cabinetlib.spec_group_name = self.new_spec_group_name
                
        return {'FINISHED'}

    def invoke(self,context,event):
        spec_group = context.scene.mv.spec_groups[context.scene.mv.spec_group_index]
        self.new_spec_group_name = spec_group.name
        self.old_spec_group_name = spec_group.name
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(400))

    def draw(self, context):
        layout = self.layout
        layout.prop(self,'new_spec_group_name')

class OPS_reload_spec_group_from_library_modules(Operator):
    bl_idname = "fd_material.reload_spec_group_from_library_modules"
    bl_label = "Reload Specification Group From Library Modules"
    bl_description = "This will clear all of the specification group information and reload from the template"
    bl_options = {'UNDO'}

    def execute(self, context):
        from importlib import import_module
        for specgroup in context.scene.mv.spec_groups:
            context.scene.mv.spec_groups.remove(0)
            
        spec_group = context.scene.mv.spec_groups.add()
        spec_group.name = "Default Specification Group"
        
        packages = utils.get_library_packages(context)
        
        for package in packages:
            pkg = import_module(package)            
            for mod_name, mod in inspect.getmembers(pkg):
                for name, obj in inspect.getmembers(mod):        
                    if hasattr(mod, 'Material_Pointers'):
                        materials = mod.Material_Pointers
                        for name, obj in inspect.getmembers(materials):
                            if "__" not in name: # Ignore built-in attributes 
                                if name not in spec_group.materials:
                                    mat_pointer = spec_group.materials.add()
                                    mat_pointer.name = name
                                    mat_pointer.library_name = obj.library_name
                                    mat_pointer.category_name = obj.category_name
                                    mat_pointer.item_name = obj.item_name
                                    
                    if hasattr(mod, 'Cutpart_Pointers'):
                        cutparts = mod.Cutpart_Pointers
                        for name, obj in inspect.getmembers(cutparts):
                            if "__" not in name: # Ignore built-in attributes
                                if name not in spec_group.cutparts:
                                    cut_pointer = spec_group.cutparts.add()
                                    cut_pointer.name = name
                                    cut_pointer.thickness = obj.thickness
                                    cut_pointer.core = obj.core
                                    cut_pointer.top = obj.top
                                    cut_pointer.bottom = obj.bottom
                                    cut_pointer.mv_pointer_name = obj.mv_pointer_name
                    
                    if hasattr(mod, 'Edgepart_Pointers'):
                        edgeparts = mod.Edgepart_Pointers
                        for name, obj in inspect.getmembers(edgeparts):
                            if "__" not in name: # Ignore built-in attributes
                                if name not in spec_group.edgeparts:
                                    edge_pointer = spec_group.edgeparts.add()
                                    edge_pointer.name = name
                                    edge_pointer.thickness = obj.thickness
                                    edge_pointer.material = obj.material
                                    edge_pointer.mv_pointer_name = obj.mv_pointer_name

        return {'FINISHED'}

class OPS_set_pointer(Operator):
    bl_idname = "fd_material.set_pointer"
    bl_label = "Set Pointer"
    bl_description = "This will set the selected item in the file browser to this pointer."
    
    pointer_name = StringProperty(name="Pointer Name")
    pointer_type = StringProperty(name="Pointer Type")
    
    @classmethod
    def poll(cls, context):
        filepath = utils.get_selected_file_from_file_browser(context)
        if filepath:
            return True
        else:
            return False

    def execute(self, context):
        library = context.scene.mv
        active_specgroup = library.spec_groups[library.spec_group_index]
        filepath = utils.get_selected_file_from_file_browser(context)
        path, file_name = os.path.split(filepath)
        file, ext = os.path.splitext(file_name)
        category_name = os.path.basename(path)

        if category_name and file:
            
            if self.pointer_type == 'MATERIAL':
                pointer = active_specgroup.materials[self.pointer_name]
                pointer.category_name = category_name
                pointer.item_name = file
                
            if self.pointer_type == 'PART':
                pointer = active_specgroup.parts[self.pointer_name]
                pointer.category_name = category_name
                pointer.item_name = file

        return {'FINISHED'}
    
class OPS_assign_materials_from_pointers(Operator):
    bl_idname = "fd_material.assign_materials_from_pointers"
    bl_label = "Assign Materials From Pointers"
    bl_description = "This will assign the materials based on the pointers assigned to the object."

    object_name = StringProperty(name="Object Name")

    def execute(self, context):
        utils.assign_materials_from_pointers(context.object)
        return {'FINISHED'}
    
#TODO: Update operator to remove cabinetlib. Many libraries use this as a way to update all materials
class OPS_update_scene_from_pointers(Operator):
    bl_idname = "cabinetlib.update_scene_from_pointers"
    bl_label = "Update Scene From Pointers"
    bl_description = "This will update the scene with the updated pointer information."

    def execute(self, context):
        for obj in context.visible_objects:
            obj.location = obj.location

        for obj in bpy.data.objects:
            if obj.type in {'MESH','CURVE'}:
                utils.assign_materials_from_pointers(obj)

        return {'FINISHED'}
    
class OPS_get_materials(Operator):
    bl_idname = "fd_material.get_materials"
    bl_label = "Get Materials"
    
    def execute(self, context):
        sheets = context.scene.cabinetlib.sheets
        edgebanding = context.scene.cabinetlib.edgebanding
#         products = context.scene.cabinetlib.products
        
        for sheet in sheets:
            sheets.remove(0)
        
        for edgeband in edgebanding:
            edgebanding.remove(0)
            
#         for product in products:
#             products.remove(0)
        
        for obj in context.visible_objects:
            if obj.cabinetlib.type_mesh == 'CUTPART':
                mat_name = utils.get_material_name(obj)
                if mat_name not in sheets:
                    mat = sheets.add()
                    mat.thickness = utils.get_part_thickness(obj)
                    mat.name = mat_name
                    sheet = mat.sizes.add() 
                    sheet.width = unit.inch(48) #TODO: Make a way set defaults
                    sheet.length = unit.inch(98) #TODO: Make a way set defaults
                    
            if obj.cabinetlib.type_mesh == 'EDGEBANDING':
                pass
            #TODO: Setup edgebanding materials
#                 edge_name = utils.get_edgebanding_name(obj)
#                 if edge_name not in edgebanding:
#                     mat = edgebanding.add()
#                     mat.thickness = utils.get_part_thickness(obj)
#                     mat.name= edge_name
                    
#             if obj.mv.type == 'BPASSEMBLY' and obj.mv.type_group == 'PRODUCT':
#                 product = products.add()
#                 product.name = obj.mv.name_object
#                 product.bp_name = obj.name
        
        return {'FINISHED'}
    
#TODO: Update operator to remove cabinetlib. Many libraries use this as a way to update all materials
class OPS_sync_material_slots(Operator):
    bl_idname = "cabinetlib.sync_material_slots"
    bl_label = "Sync Material Slots"
    bl_options = {'UNDO'}
    
    object_name = StringProperty(name="Object Name")
    
    def execute(self, context):
        obj = bpy.data.objects[self.object_name]
        scene = context.scene
        spec_group = scene.mv.spec_groups[obj.cabinetlib.spec_group_index]
        
        for slot in obj.cabinetlib.material_slots:
            obj.cabinetlib.material_slots.remove(0)
            
        if obj.cabinetlib.type_mesh == 'CUTPART':
            part_pointer = None
            edge_pointer = None
            if obj.cabinetlib.cutpart_name in spec_group.cutparts:
                part_pointer = spec_group.cutparts[obj.cabinetlib.cutpart_name]
                if obj.cabinetlib.edgepart_name in spec_group.edgeparts:
                    edge_pointer = spec_group.edgeparts[obj.cabinetlib.edgepart_name]
                
            for index, mat_slot in enumerate(obj.material_slots):
                slot = obj.cabinetlib.material_slots.add()

                if index == 0:
                    slot.name = 'Core'
                    if part_pointer:
                        slot.pointer_name = part_pointer.core
                if index == 1:
                    slot.name = 'Interior'
                    if part_pointer:
                        slot.pointer_name = part_pointer.top
                if index == 2:
                    slot.name = 'Exterior'
                    if part_pointer:
                        slot.pointer_name = part_pointer.bottom
                
                if index > 2:
                    slot.name = "Edgebanding"
                    if edge_pointer:
                        slot.pointer_name = edge_pointer.material
                    
        elif obj.cabinetlib.type_mesh == 'EDGEBANDING':
            pointer = None
            if obj.cabinetlib.edgepart_name in spec_group.edgeparts:
                pointer = spec_group.edgeparts[obj.cabinetlib.edgepart_name]
                
            for index, mat_slot in enumerate(obj.material_slots):
                slot = obj.cabinetlib.material_slots.add()
                slot.name = 'Edgebanding'
                if pointer:
                    slot.pointer_name = pointer.material
                    
        else:
            for index, mat_slot in enumerate(obj.material_slots):
                slot = obj.cabinetlib.material_slots.add()
                
        utils.assign_materials_from_pointers(obj)
        return {'FINISHED'}
    
class OPS_assign_material_interface(bpy.types.Operator):
    bl_idname = "fd_material.assign_material_interface"
    bl_label = "Assign Materials"
    bl_options = {'UNDO'}
    
    #READONLY
    filepath = StringProperty(name="Material Name")

    materials = None 

    def check(self,context):
        return True

    def invoke(self, context, event):
        library = context.scene.mv
        active_spec_group = library.spec_groups[library.spec_group_index]
        for material in active_spec_group.materials:
            material.assign_material = False
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(600))
    
    def execute(self,context):
        path, filename = os.path.split(self.filepath)
        file, ext = os.path.splitext(filename)
        file_dir = os.path.basename(path)
        material = utils.get_material(file_dir,file)

        library = context.scene.mv
        active_spec_group = library.spec_groups[library.spec_group_index]
        for material in active_spec_group.materials:
            if material.assign_material:
                material.library_name = "Cabinet Materials"
                material.category_name = file_dir
                material.item_name = file
            material.assign_material = False # Reset back to false
        
        bpy.ops.cabinetlib.update_scene_from_pointers()
        return {'FINISHED'}
    
    def draw(self, context):
        library = context.scene.mv
        layout = self.layout
        active_spec_group = library.spec_groups[library.spec_group_index]
        layout.menu('MENU_Available_Spec_Groups',text=active_spec_group.name,icon='SOLO_ON')
        row = layout.row()
        box1 = row.box()
        box1.label('Surface Materials:')
        col1 = box1.column(align=True)
        box2 = row.box()
        box2.label('Edge Materials:')
        col2 = box2.column(align=True)
        box3 = row.box()
        box3.label('Hardware and Buyout Materials:')
        col3 = box3.column(align=True)
        active_spec_group = library.spec_groups[library.spec_group_index]
        for material in active_spec_group.materials:
            if 'Surface' in material.name:
                row = col1.row()
            elif 'Edge' in material.name:
                row = col2.row()
            else:
                row = col3.row()
            row.label(material.name.replace("_"," "))
            row.prop(material,'assign_material',text="")
    
class OPS_assign_material(Operator):
    bl_idname = "fd_material.assign_material"
    bl_label = "Assign Material"
    bl_options = {'UNDO'}
    
    #READONLY
    material_name = StringProperty(name="Material Name")
    object_name = StringProperty(name="Object Name")
    
    obj = None
    material = None
    
    def check(self, context):
        return True
    
    def invoke(self, context, event):
        self.material = bpy.data.materials[self.material_name]
        self.obj = bpy.data.objects[self.object_name]
#         if self.material.name not in context.scene.materiallib.scene_materials:
#             material = context.scene.materiallib.scene_materials.add()
#             material.name = self.material.name
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(400))
        
    def draw(self,context):
        layout = self.layout
        layout.label(self.obj.name,icon='OBJECT_DATA')
        for index, mat_slot in enumerate(self.obj.material_slots):
            row = layout.split(percentage=.8)
            if mat_slot.name == "":
                row.label('No Material')
            else:
                row.prop(mat_slot,"name",text=self.obj.cabinetlib.material_slots[index].name if len(self.obj.cabinetlib.material_slots) >= index+1 else "")
            props = row.operator('fd_material.assign_material_to_slot',text="Assign",icon='BACK')
            props.object_name = self.obj.name
            props.material_name = self.material.name
            props.index = index
        
    def execute(self,context):
        return {'FINISHED'}
        
class OPS_assign_material_to_slot(Operator):
    bl_idname = "fd_material.assign_material_to_slot"
    bl_label = "Assign Material to Slot"
    bl_options = {'UNDO'}
    
    #READONLY
    material_name = StringProperty(name="Material Name")
    object_name = StringProperty(name="Object Name")
    
    index = IntProperty(name="Index")
    
    obj = None
    material = None
    
    def execute(self,context):
        obj = bpy.data.objects[self.object_name]
        mat = bpy.data.materials[self.material_name]
        obj.material_slots[self.index].material = mat
        return {'FINISHED'}
    
#------REGISTER
classes = [
           OPS_clear_unused_materials_from_file,
           OPS_apply_materials_from_pointers,
           OPS_add_material_slot,
           OPS_fix_texture_paths,
           OPS_material_properties,
           OPS_clear_material_copies,
           OPS_create_material_library,
           OPS_create_material_template,
           OPS_change_product_spec_group,
           OPS_change_active_spec_group,
           OPS_clear_spec_group,
           OPS_copy_selected_spec_group,
           OPS_delete_spec_group,
           OPS_rename_spec_group,
           OPS_reload_spec_group_from_library_modules,
           OPS_set_pointer,
           OPS_assign_materials_from_pointers,
           OPS_update_scene_from_pointers,
           OPS_get_materials,
           OPS_sync_material_slots,
           OPS_assign_material_interface,
           OPS_assign_material,
           OPS_assign_material_to_slot
           ]

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()