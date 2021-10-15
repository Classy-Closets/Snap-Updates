import inspect

import bpy
from bpy.types import Operator
from bpy.props import StringProperty

from snap import sn_utils


class SN_MAT_OT_add_material_slot(Operator):
    bl_idname = "sn_material.add_material_slot"
    bl_label = "Add Material Slot"
    bl_description = "This adds a material slot and a material pointer"
    bl_options = {'UNDO'}

    object_name: StringProperty(name="Object Name")

    def execute(self, context):
        obj = bpy.data.objects[self.object_name]
        obj.snap.material_slots.add()
        override = {'active_object': obj, 'object': obj}
        bpy.ops.object.material_slot_add(override)
        return{'FINISHED'}


class SN_MAT_OT_add_material_pointer(Operator):
    bl_idname = "sn_material.add_material_pointers"
    bl_label = "Add Material Pointers"
    bl_description = "This add a material pointer"
    bl_options = {'UNDO'}

    object_name: StringProperty(name="Object Name")

    def execute(self, context):
        obj = bpy.data.objects[self.object_name]
        for index, mat_slot in enumerate(obj.material_slots):
            if len(obj.snap.material_slots) < index + 1:
                obj.snap.material_slots.add()
        return{'FINISHED'}


class SN_MAT_OT_assign_material_dialog(Operator):
    bl_idname = "sn_material.assign_material_dialog"
    bl_label = "Assign Material Dialog"
    bl_description = "This is a dialog to assign materials to material slots"
    bl_options = {'UNDO'}

    # READONLY
    material_name: bpy.props.StringProperty(name="Material Name")
    object_name: bpy.props.StringProperty(name="Object Name")

    obj = None
    material = None

    def check(self, context):
        return True

    def invoke(self, context, event):
        self.material = bpy.data.materials[self.material_name]
        self.obj = bpy.data.objects[self.object_name]
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=500)

    def draw(self, context):
        layout = self.layout
        layout.label(text=self.obj.name, icon='OBJECT_DATA')
        for index, mat_slot in enumerate(self.obj.material_slots):
            row = layout.split(factor=.55)
            if mat_slot.name == "":
                row.label(text='No Material')
            else:
                row.prop(mat_slot, "name", text="", icon='MATERIAL')

            props = row.operator('sn_material.assign_material_to_slot', text="Assign", icon='BACK')
            props.object_name = self.obj.name
            props.material_name = self.material.name
            props.index = index

            props = row.operator('sn_material.replace_all_materials', text="Replace All", icon='FILE_REFRESH')
            props.object_name = self.obj.name
            props.material_name = self.material.name
            props.index = index

    def execute(self, context):
        return {'FINISHED'}


class SN_MAT_OT_assign_material_to_slot(Operator):
    bl_idname = "sn_material.assign_material_to_slot"
    bl_label = "Assign Material to Slot"
    bl_description = "This will assign a material to a material slot"
    bl_options = {'UNDO'}

    # READONLY
    material_name: bpy.props.StringProperty(name="Material Name")
    object_name: bpy.props.StringProperty(name="Object Name")

    index: bpy.props.IntProperty(name="Index")

    def execute(self, context):
        obj = bpy.data.objects[self.object_name]
        mat = bpy.data.materials[self.material_name]
        obj.material_slots[self.index].material = mat
        return {'FINISHED'}


class SN_MAT_OT_replace_all_materials(Operator):
    bl_idname = "sn_material.replace_all_materials"
    bl_label = "Assign Material to Slot"
    bl_description = "This will replace all materials in the file with a new material"
    bl_options = {'UNDO'}

    # READONLY
    material_name: bpy.props.StringProperty(name="Material Name")
    object_name: bpy.props.StringProperty(name="Object Name")

    index: bpy.props.IntProperty(name="Index")

    def execute(self, context):
        obj = bpy.data.objects[self.object_name]
        mat = bpy.data.materials[self.material_name]
        mat_to_replace = obj.material_slots[self.index].material
        obj.material_slots[self.index].material = mat
        for obj in bpy.data.objects:
            for slot in obj.material_slots:
                if slot.material == mat_to_replace:
                    slot.material = mat
        return {'FINISHED'}


class SN_MAT_OT_reload_spec_group_from_library_modules(Operator):
    bl_idname = "sn_material.reload_spec_group_from_library_modules"
    bl_label = "Reload Specification Group From Library Modules"
    bl_description = "This will clear all of the specification group information and reload from the template"
    bl_options = {'UNDO'}

    def execute(self, context):
        from importlib import import_module

        for specgroup in context.scene.snap.spec_groups:
            context.scene.snap.spec_groups.remove(0)

        spec_group = context.scene.snap.spec_groups.add()
        spec_group.name = "Default Specification Group"
        packages = sn_utils.get_library_packages(context)

        for package in packages:
            pkg = import_module(package)
            for mod_name, mod in inspect.getmembers(pkg):
                if 'spec_group' in mod_name:
                    for name, obj in inspect.getmembers(mod):
                        if hasattr(mod, 'Material_Pointers'):
                            materials = mod.Material_Pointers
                            for name, obj in inspect.getmembers(materials):
                                if "__" not in name:  # Ignore built-in attributes
                                    if name not in spec_group.materials:
                                        mat_pointer = spec_group.materials.add()
                                        mat_pointer.name = name
                                        mat_pointer.category_name = obj.category_name
                                        mat_pointer.item_name = obj.item_name

                        if hasattr(mod, 'Cutpart_Pointers'):
                            cutparts = mod.Cutpart_Pointers
                            for name, obj in inspect.getmembers(cutparts):
                                if "__" not in name:  # Ignore built-in attributes
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
                                if "__" not in name:  # Ignore built-in attributes
                                    if name not in spec_group.edgeparts:
                                        edge_pointer = spec_group.edgeparts.add()
                                        edge_pointer.name = name
                                        edge_pointer.thickness = obj.thickness
                                        edge_pointer.material = obj.material
                                        edge_pointer.mv_pointer_name = obj.mv_pointer_name

        return {'FINISHED'}


class SN_MAT_OT_sync_material_slots(Operator):
    bl_idname = "sn_material.sync_material_slots"
    bl_label = "Sync Material Slots"
    bl_options = {'UNDO'}
    
    object_name : StringProperty(name="Object Name")
    
    def execute(self, context):
        obj = bpy.data.objects[self.object_name]
        scene = context.scene
        spec_group = scene.snap.spec_groups[obj.snap.spec_group_index]
        
        for slot in obj.snap.material_slots:
            obj.snap.material_slots.remove(0)
            
        if obj.snap.type_mesh == 'CUTPART':
            part_pointer = None
            edge_pointer = None
            if obj.snap.cutpart_name in spec_group.cutparts:
                part_pointer = spec_group.cutparts[obj.snap.cutpart_name]
                if obj.snap.edgepart_name in spec_group.edgeparts:
                    edge_pointer = spec_group.edgeparts[obj.snap.edgepart_name]
                
            for index, mat_slot in enumerate(obj.material_slots):
                slot = obj.snap.material_slots.add()

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
                    
        elif obj.snap.type_mesh == 'EDGEBANDING':
            pointer = None
            if obj.snap.edgepart_name in spec_group.edgeparts:
                pointer = spec_group.edgeparts[obj.snap.edgepart_name]
                
            for index, mat_slot in enumerate(obj.material_slots):
                slot = obj.snap.material_slots.add()
                slot.name = 'Edgebanding'
                if pointer:
                    slot.pointer_name = pointer.material
                    
        else:
            for index, mat_slot in enumerate(obj.material_slots):
                slot = obj.snap.material_slots.add()
                
        sn_utils.assign_materials_from_pointers(obj)
        return {'FINISHED'}


classes = (
    SN_MAT_OT_add_material_slot,
    SN_MAT_OT_add_material_pointer,
    SN_MAT_OT_assign_material_dialog,
    SN_MAT_OT_assign_material_to_slot,
    SN_MAT_OT_replace_all_materials,
    SN_MAT_OT_reload_spec_group_from_library_modules,
    SN_MAT_OT_sync_material_slots
)

register, unregister = bpy.utils.register_classes_factory(classes)
