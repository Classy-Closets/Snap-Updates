import os
import subprocess

import bpy
from bpy.types import Operator
from bpy.props import BoolProperty, StringProperty

from snap import sn_unit
from snap import sn_paths
from snap import sn_utils
from snap import sn_types
from snap.ops.sn_prompt import SN_PPT_OT_update_all_prompts_in_scene


class SN_MAT_OT_Poll_Assign_Materials(Operator):
    bl_idname = "closet_materials.poll_assign_materials"
    bl_label = ""
    bl_description = ""
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene.closet_materials.check_render_mats()

    def execute(self, context):
        bpy.ops.closet_materials.assign_materials()

        return {'FINISHED'}


class SN_MAT_OT_Assign_Materials(Operator):
    bl_idname = "closet_materials.assign_materials"
    bl_label = "Assign Materials"
    bl_description = "This will assign the material names"
    bl_options = {'UNDO'}

    update_countertops: BoolProperty(name="Update Countertops", default=False)
    only_update_pointers: BoolProperty(
        name="Only Update Pointers", default=False)

    closet_props = None
    props_closet_materials = None

    @classmethod
    def poll(cls, context):
        return context.scene.closet_materials.check_render_mats()

    def scene_assemblies(self, context):
        for obj in bpy.context.scene.objects:
            if 'IS_BP_ASSEMBLY' in obj:
                assembly = sn_types.Assembly(obj_bp=obj)
                yield assembly

    def set_manufacturing_material(self, obj):
        """ Sets the cutpart_material_name property so the materials
            get exported as the correct names.
        """
        props = bpy.context.scene.closet_materials
        mat_type = props.materials.get_mat_type()
        edge_type = props.edges.get_edge_type()
        door_drawer_edge_type = props.door_drawer_edges.get_edge_type()
        edge2_type = props.secondary_edges.get_edge_type()

        obj.snap.cutpart_material_name = mat_type.get_inventory_material_name()

        if obj.snap.edge_w1 != "":
            if obj.snap.edge_w1 == 'Edge':
                obj.snap.edgeband_material_name_w1 = edge_type.get_inventory_edge_name()
            elif obj.snap.edge_w1 == 'Door_Edges':
                obj.snap.edgeband_material_name_w1 = door_drawer_edge_type.get_inventory_edge_name()
            else:
                obj.snap.edgeband_material_name_w1 = edge2_type.get_inventory_edge_name()
        if obj.snap.edge_w2 != "":
            if obj.snap.edge_w2 == 'Edge':
                obj.snap.edgeband_material_name_w2 = edge_type.get_inventory_edge_name()
            elif obj.snap.edge_w2 == 'Door_Edges':
                obj.snap.edgeband_material_name_w2 = door_drawer_edge_type.get_inventory_edge_name()
            else:
                obj.snap.edgeband_material_name_w2 = edge2_type.get_inventory_edge_name()
        if obj.snap.edge_l1 != "":
            if obj.snap.edge_l1 == 'Edge':
                obj.snap.edgeband_material_name_l1 = edge_type.get_inventory_edge_name()
            elif obj.snap.edge_l1 == 'Door_Edges':
                obj.snap.edgeband_material_name_l1 = door_drawer_edge_type.get_inventory_edge_name()
            else:
                obj.snap.edgeband_material_name_l1 = edge2_type.get_inventory_edge_name()
        if obj.snap.edge_l2 != "":
            if obj.snap.edge_l2 == 'Edge':
                obj.snap.edgeband_material_name_l2 = edge_type.get_inventory_edge_name()
            elif obj.snap.edge_l2 == 'Door_Edges':
                obj.snap.edgeband_material_name_l2 = door_drawer_edge_type.get_inventory_edge_name()
            else:
                obj.snap.edgeband_material_name_l2 = edge2_type.get_inventory_edge_name()

    def set_material(self, part):
        for child in part.obj_bp.children:
            if child.snap.type_mesh == 'CUTPART':
                self.set_manufacturing_material(child)

    def set_door_material(self, assembly):
        for obj in assembly.obj_bp.children:
            if obj.snap.type_mesh == 'CUTPART':
                cab_mat_props = self.props_closet_materials
                mat_type = cab_mat_props.door_drawer_materials.get_mat_type()
                mat_color_name = cab_mat_props.materials.get_mat_color().name
                edge_type = cab_mat_props.door_drawer_edges.get_edge_type()
                door_part = sn_types.Part(assembly.obj_bp)

                if mat_type.name == "Garage Material":
                    door_part.cutpart("Garage_Slab_Door")
                    if mat_color_name == "Graphite Spectrum":
                        door_part.edgebanding("Black_Edge", l1=True, w1=True, l2=True, w2=True)
                        door_part.set_material_pointers("Black", "TopBottomEdge")
                        door_part.set_material_pointers("Black", "LeftRightEdge")
                    else:
                        door_part.edgebanding("Exterior_Edge", l1=True, w1=True, l2=True, w2=True)
                        door_part.set_material_pointers("Garage_Exterior_Edges", "TopBottomEdge")
                        door_part.set_material_pointers("Garage_Exterior_Edges", "LeftRightEdge")
                
                else:
                    door_part.cutpart("Slab_Door")
                    door_part.edgebanding('Door_Edges', l1=True, w1=True, l2=True, w2=True)
                    door_part.set_material_pointers("Door_Edge", "TopBottomEdge")
                    door_part.set_material_pointers("Door_Edge", "LeftRightEdge")

                obj.snap.cutpart_material_name = mat_type.get_inventory_material_name()
                obj.snap.edgeband_material_name_w1 = edge_type.get_inventory_edge_name()
                obj.snap.edgeband_material_name_w2 = edge_type.get_inventory_edge_name()
                obj.snap.edgeband_material_name_l1 = edge_type.get_inventory_edge_name()
                obj.snap.edgeband_material_name_l2 = edge_type.get_inventory_edge_name()

    def set_drawer_bottom_material(self, part):
        for obj in part.obj_bp.children:
            if obj.snap.type_mesh == 'CUTPART':
                props = self.props_closet_materials
                box_type = self.closet_props.closet_options.box_type

                if box_type == 'MEL':
                    obj.snap.cutpart_material_name = "White Paper 11300"
                else:
                    obj.snap.cutpart_material_name = "Baltic Birch 30250"

    def set_drawer_part_material(self, part):
        for obj in part.obj_bp.children:
            if obj.snap.type_mesh == 'CUTPART':
                props = self.props_closet_materials
                box_type = self.closet_props.closet_options.box_type

                if box_type == 'MEL':
                    obj.snap.cutpart_material_name = "Oxford White 12200"
                else:
                    obj.snap.cutpart_material_name = "Baltic Birch 32200"

                obj.snap.edgeband_material_name_l1 = "Oxford White 1030"
                obj.snap.edgeband_material_name_l2 = ""
                obj.snap.edgeband_material_name_w1 = ""
                obj.snap.edgeband_material_name_w2 = ""

    def update_material_pointers(self, context):
        mat_props = self.props_closet_materials
        default_props = self.closet_props.closet_options

        for spec_group in context.scene.snap.spec_groups:
            surface_pointer = spec_group.materials["Closet_Part_Surfaces"]
            garage_interior_pointer = spec_group.materials["Garage_Interior_Surface"]
            edge_pointer = spec_group.materials["Closet_Part_Edges"]
            edge_pointer_2 = spec_group.materials["Closet_Part_Edges_Secondary"]
            door_pointer = spec_group.materials["Door_Surface"]
            door_edge_pointer = spec_group.materials["Door_Edge"]
            molding_pointer = spec_group.materials["Molding"]
            drawer_surface = spec_group.materials["Drawer_Box_Surface"]
            wood_door_pointer = spec_group.materials["Wood_Door_Surface"]
            moderno_door_pointer = spec_group.materials["Moderno_Door"]
            glass_panel_pointer = spec_group.materials["Glass"]
            countertop_pointer = spec_group.materials["Countertop_Surface"]
            garage_exterior_surface_pointer = spec_group.materials["Garage_Exterior_Surface"]
            garage_panel_edge_pointer = spec_group.materials["Garage_Panel_Edges"]
            garage_interior_edge_pointer = spec_group.materials["Garage_Interior_Edges"]

            # Set garage pointers
            garage_exterior_surface_pointer.category_name = "Closet Materials"
            garage_exterior_surface_pointer.item_name = mat_props.materials.get_mat_color().name

            garage_panel_edge_pointer.category_name = "Closet Materials"
            garage_panel_edge_pointer.item_name = mat_props.materials.get_mat_color().name

            garage_interior_edge_pointer.category_name = "Closet Materials"
            garage_interior_edge_pointer.item_name = "Oxford White"


            # Construction Defaults
            if default_props.box_type == 'MEL':
                drawer_surface.category_name = "Closet Materials"
                drawer_surface.item_name = "Oxford White"
            else:
                drawer_surface.category_name = "Closet Materials"
                drawer_surface.item_name = "Birch"

            surface_pointer.category_name = "Closet Materials"
            surface_pointer.item_name = mat_props.materials.get_mat_color().name

            garage_interior_pointer.category_name = "Closet Materials"
            if mat_props.materials.get_mat_type().name == "Garage Material":
                garage_interior_pointer.item_name = "Oxford White"
            else:
                garage_interior_pointer.item_name = mat_props.materials.get_mat_color().name

            molding_pointer.category_name = "Closet Materials"
            molding_pointer.item_name = mat_props.stain_colors[mat_props.stain_color_index].name

            edge_pointer.category_name = "Closet Materials"
            edge_pointer.item_name = mat_props.edges.get_edge_color().name

            edge_pointer_2.category_name = "Closet Materials"
            edge_pointer_2.item_name = mat_props.secondary_edges.get_edge_color().name

            door_pointer.category_name = "Closet Materials"
            door_pointer.item_name = mat_props.door_drawer_materials.get_mat_color().name

            door_edge_pointer.category_name = "Closet Materials"
            door_edge_pointer.item_name = mat_props.door_drawer_edges.get_edge_color().name

            wood_door_pointer.category_name = "Closet Materials"
            wood_door_pointer.item_name = mat_props.stain_colors[mat_props.stain_color_index].name

            moderno_door_pointer.category_name = "Closet Materials"
            moderno_door_pointer.item_name = mat_props.moderno_colors[
                mat_props.moderno_color_index].name

            glass_panel_pointer.category_name = "Glass"
            glass_panel_pointer.item_name = "Glass"

            if "Melamine" in mat_props.countertops.get_type().name:
                countertop_pointer.category_name = "Closet Materials"
            else:
                countertop_pointer.category_name = "Countertop Materials"

            countertop_pointer.item_name = mat_props.countertops.get_color_name()

    def update_drawer_materials(self):
        props = self.closet_props
        box_type = props.closet_options.box_type
        for spec_group in bpy.context.scene.snap.spec_groups:
            drawer_part = spec_group.cutparts['Drawer_Part']
            drawer_back = spec_group.cutparts['Drawer_Back']
            drawer_bottom = spec_group.cutparts['Drawer_Bottom']
            if box_type == 'MEL':
                drawer_part.thickness = sn_unit.inch(.5)
                drawer_back.thickness = sn_unit.inch(.5)
                drawer_bottom.thickness = sn_unit.inch(.375)
            else:
                drawer_part.thickness = sn_unit.inch(.5)
                drawer_back.thickness = sn_unit.inch(.5)
                drawer_bottom.thickness = sn_unit.inch(.25)

    def set_panel_material(self, assembly):
        cab_mat_props = self.props_closet_materials
        mat_type = cab_mat_props.materials.get_mat_type()
        mat_color_name = cab_mat_props.materials.get_mat_color().name
        panel_part = sn_types.Part(assembly.obj_bp)
        section_product = sn_types.Assembly(
            sn_utils.get_closet_bp(assembly.obj_bp))
        opening_qty = 0
        left_end_condition = 'WP'
        right_end_condition = 'WP'

        if section_product and section_product.get_prompt("Opening Quantity"):
            opening_qty = section_product.get_prompt(
                "Opening Quantity").get_value()
            left_end_condition = section_product.get_prompt(
                "Left End Condition").get_value()
            right_end_condition = section_product.get_prompt(
                "Right End Condition").get_value()

        if mat_type.name == "Garage Material":
            # Check left end panel condition
            if panel_part.obj_bp.get('PARTITION_NUMBER') == 0:
                if left_end_condition == 0:  # 0='EP'
                    panel_part.cutpart("Garage_End_Panel")
                else:
                    panel_part.cutpart("Garage_Mid_Panel")
            # Check right end panel condition
            elif panel_part.obj_bp.get('PARTITION_NUMBER') == opening_qty:
                if right_end_condition == 0:  # 0='EP'
                    panel_part.cutpart("Garage_End_Panel")
                else:
                    panel_part.cutpart("Garage_Mid_Panel")
            else:
                panel_part.cutpart("Garage_Mid_Panel")

            if mat_color_name == "Graphite Spectrum":
                panel_part.set_material_pointers(
                "Black", "FrontBackEdge")
                panel_part.set_material_pointers(
                "Black", "TopBottomEdge")
            else:
                panel_part.set_material_pointers(
                "Garage_Panel_Edges", "FrontBackEdge")
                panel_part.set_material_pointers(
                "Garage_Panel_Edges", "TopBottomEdge")

        else:
            # Set back to closet material pointers, same as common_parts.add_panel
            panel_part.cutpart("Panel")
            panel_part.edgebanding("Edge", l2=True)
            panel_part.edgebanding("Edge_2", w2=True, w1=True)
            panel_part.set_material_pointers("Closet_Part_Edges", "FrontBackEdge")
            panel_part.set_material_pointers("Closet_Part_Edges_Secondary", "TopBottomEdge")

        # 36H or lower have to be edgebanded, but 46.10 doesn't work, so I made it 46.11 and now it does
        if assembly.obj_x.location.x > sn_unit.inch(46.11):
            exposed_bottom = assembly.get_prompt("Exposed Bottom")
            if exposed_bottom:
                if exposed_bottom.get_value():
                    for child in assembly.obj_bp.children:
                        if child.snap.type_mesh == 'CUTPART':
                            if mat_type.name == "Garage Material":
                                if mat_color_name == "Graphite Spectrum":
                                    child.snap.edge_w1 = 'Black_Edge'
                                    child.snap.edge_w2 = 'Black_Edge'
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'TopBottomEdge':
                                            mat_slot.pointer_name = "Black"
                                else:
                                    child.snap.edge_w1 = 'Exterior_Edge'
                                    child.snap.edge_w2 = 'Exterior_Edge'
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'TopBottomEdge':
                                            mat_slot.pointer_name = "Garage_Panel_Edges"
                            else:
                                child.snap.edge_w1 = 'Edge_2'
                                child.snap.edge_w2 = 'Edge_2'
                                for mat_slot in child.snap.material_slots:
                                    if mat_slot.name == 'TopBottomEdge':
                                        mat_slot.pointer_name = "Closet_Part_Edges_Secondary"
                else:
                    for child in assembly.obj_bp.children:
                        if child.snap.type_mesh == 'CUTPART':
                            child.snap.edge_w1 = ''
                            child.snap.edge_w2 = ''
                            for mat_slot in child.snap.material_slots:
                                if mat_slot.name == 'TopBottomEdge':
                                    mat_slot.pointer_name = "Core"
            else:
                for child in assembly.obj_bp.children:
                    if child.snap.type_mesh == 'CUTPART':
                        child.snap.edge_w1 = ''
                        child.snap.edge_w2 = ''
                        for mat_slot in child.snap.material_slots:
                            if mat_slot.name == 'TopBottomEdge':
                                mat_slot.pointer_name = "Core"
        else:
            for child in assembly.obj_bp.children:
                if child.snap.type_mesh == 'CUTPART':
                    if mat_type.name == "Garage Material":
                        if mat_color_name == "Graphite Spectrum":
                            child.snap.edge_w1 = 'Black_Edge'
                            child.snap.edge_w2 = 'Black_Edge'
                            for mat_slot in child.snap.material_slots:
                                if mat_slot.name == 'TopBottomEdge':
                                    mat_slot.pointer_name = "Black"
                        else:
                            child.snap.edge_w1 = 'Exterior_Edge'
                            child.snap.edge_w2 = 'Exterior_Edge'
                            for mat_slot in child.snap.material_slots:
                                if mat_slot.name == 'TopBottomEdge':
                                    mat_slot.pointer_name = "Garage_Panel_Edges"
                    else:
                        child.snap.edge_w1 = 'Edge_2'
                        child.snap.edge_w2 = 'Edge_2'
                        for mat_slot in child.snap.material_slots:
                            if mat_slot.name == 'TopBottomEdge':
                                mat_slot.pointer_name = "Closet_Part_Edges_Secondary"

    def set_shelf_material(self, assembly):
        cab_mat_props = self.props_closet_materials
        mat_type = cab_mat_props.materials.get_mat_type()
        mat_color_name = cab_mat_props.materials.get_mat_color().name
        shelf_part = sn_types.Part(assembly.obj_bp)
        is_raised_bottom_KD = False
        parent_obj = assembly.obj_bp.parent
        parent_assembly = sn_types.Assembly(parent_obj)

        is_KD = False
        is_locked_shelf = assembly.get_prompt("Is Locked Shelf")
        if is_locked_shelf:
            if is_locked_shelf.get_value():
                is_KD = True
        
        is_exposed = False
        is_bottom_exposed_kd = assembly.get_prompt("Is Bottom Exposed KD")
        if is_bottom_exposed_kd:
            if is_bottom_exposed_kd.get_value():
                is_exposed = True
        
        if mat_type.name == "Garage Material":
            if is_KD:
                if is_exposed:
                    # If the z dimension is negative, I need to flip the cutpart sides.
                    if assembly.obj_z.location.z > 0:
                        shelf_part.cutpart("Garage_Bottom_KD")
                    else:
                        shelf_part.cutpart("Garage_Top_KD")
                else:
                    shelf_part.cutpart("Garage_Interior_KD")
                if abs(sn_unit.meter_to_inch(assembly.obj_z.location.z)) > 0.76:
                    shelf_part.cutpart("Garage_Interior_Shelf")
                    shelf_part.edgebanding("Interior_Edge", l2=True)
                    shelf_part.set_material_pointers("Garage_Interior_Edges", "Edgebanding")
                elif mat_color_name == "Graphite Spectrum":
                    shelf_part.edgebanding("Black_Edge", l2=True)
                    shelf_part.set_material_pointers("Black", "Edgebanding")
                else:
                    shelf_part.edgebanding("Exterior_Edge", l2=True)
                    shelf_part.set_material_pointers("Garage_Panel_Edges", "Edgebanding")
            else:
                shelf_part.cutpart("Garage_Interior_Shelf")
                shelf_part.edgebanding("Interior_Edge", l2=True)
                shelf_part.set_material_pointers("Garage_Interior_Edges", "Edgebanding")
        else:
            shelf_part.cutpart("Shelf")
            shelf_part.edgebanding("Edge", l2=True)
            shelf_part.set_material_pointers("Closet_Part_Edges", "Edgebanding")

    def set_cleat_material(self, assembly):
        cab_mat_props = self.props_closet_materials
        mat_type = cab_mat_props.materials.get_mat_type()
        cleat_part = sn_types.Part(assembly.obj_bp)
        if mat_type.name == "Garage Material":
            if assembly.obj_bp.get("IS_COVER_CLEAT"):
                cleat_part.cutpart("Garage_Cover_Cleat")
                cleat_part.edgebanding("Interior_Edge", l1=True)
                cleat_part.set_material_pointers("Garage_Interior_Edges", "Edgebanding")
            else:
                cleat_part.cutpart("Garage_Cleat")
                cleat_part.edgebanding("Interior_Edge", l1=True)
                cleat_part.set_material_pointers("Garage_Interior_Edges", "Edgebanding")
                
        else:
            if assembly.obj_bp.get("IS_COVER_CLEAT"):
                cleat_part.cutpart("Cover_Cleat")
                cleat_part.edgebanding("Edge_2", l1=True)
                cleat_part.set_material_pointers("Closet_Part_Edges_Secondary", "Edgebanding")
            else:
                cleat_part.cutpart("Cleat")
                cleat_part.edgebanding("Edge_2", l1=True)
                cleat_part.set_material_pointers("Closet_Part_Edges_Secondary", "Edgebanding")
    
    def set_back_material(self, assembly):
        cab_mat_props = self.props_closet_materials
        mat_type = cab_mat_props.materials.get_mat_type()
        back_part = sn_types.Part(assembly.obj_bp)

        if not assembly.obj_bp.sn_closets.use_unique_material:
            if mat_type.name == "Garage Material":
                for child in assembly.obj_bp.children:
                    if child.snap.type_mesh == 'CUTPART':
                        for mat_slot in child.snap.material_slots:
                            if mat_slot.name == "Full Back Color":
                                mat_slot.pointer_name = "Garage_Interior_Surface"
                back_part.cutpart("Garage_Back")
            else:
                for child in assembly.obj_bp.children:
                    if child.snap.type_mesh == 'CUTPART':
                        for mat_slot in child.snap.material_slots:
                            if mat_slot.name == "Full Back Color":
                                mat_slot.pointer_name = "Closet_Part_Surfaces"
                back_part.cutpart("Back")
    
    def set_drawer_front_material(self, assembly):
        cab_mat_props = self.props_closet_materials
        mat_type = cab_mat_props.materials.get_mat_type()
        mat_color_name = cab_mat_props.materials.get_mat_color().name
        drawer_front_part = sn_types.Part(assembly.obj_bp)
        
        if mat_type.name == "Garage Material":
            drawer_front_part.cutpart("Garage_Slab_Drawer_Front")
            if mat_color_name == "Graphite Spectrum":
                drawer_front_part.edgebanding("Black_Edge", l1=True, w1=True, l2=True, w2=True)
                drawer_front_part.set_material_pointers("Black", "TopBottomEdge")
                drawer_front_part.set_material_pointers("Black", "LeftRightEdge")
            else:
                drawer_front_part.edgebanding("Exterior_Edge", l1=True, w1=True, l2=True, w2=True)
                drawer_front_part.set_material_pointers("Garage_Exterior_Edges", "TopBottomEdge")
                drawer_front_part.set_material_pointers("Garage_Exterior_Edges", "LeftRightEdge")
        else:
            drawer_front_part.cutpart("Slab_Drawer_Front")
            drawer_front_part.edgebanding('Door_Edges',l1=True, w1=True, l2=True, w2=True)
            drawer_front_part.set_material_pointers("Door_Edge", "TopBottomEdge")
            drawer_front_part.set_material_pointers("Door_Edge", "LeftRightEdge")

    def set_countertop_material(self, assembly):
        cab_mat_props = self.props_closet_materials
        mat_type = cab_mat_props.materials.get_mat_type()
        mat_color_name = cab_mat_props.materials.get_mat_color().name
        countertop_part = sn_types.Part(assembly.obj_bp)

        if mat_type.name == "Garage Material":
            if mat_color_name == "Graphite Spectrum":
                countertop_part.edgebanding('Black_Edge', l1=True, l2=True, w1=True, w2=True)
                countertop_part.set_material_pointers("Black", "Edgebanding")
            else:
                countertop_part.edgebanding('Exterior_Edge', l1=True, l2=True, w1=True, w2=True)
                countertop_part.set_material_pointers("Garage_Panel_Edges", "Edgebanding")
        else:
            countertop_part.edgebanding('Edge', l1=True, l2=True, w1=True, w2=True)
            countertop_part.set_material_pointers("Closet_Part_Edges", "Edgebanding")

        exposed_left = assembly.get_prompt("Exposed Left")
        exposed_right = assembly.get_prompt("Exposed Right")
        exposed_back = assembly.get_prompt("Exposed Back")
        if exposed_left:
            if exposed_left.get_value():
                for child in assembly.obj_bp.children:
                    if child.snap.type_mesh == 'CUTPART':
                        if mat_type.name == "Garage Material":
                            if mat_color_name == "Graphite Spectrum":
                                child.snap.edge_w1 = 'Black_Edge'
                                for mat_slot in child.snap.material_slots:
                                    if mat_slot.name == 'LeftEdge':
                                        mat_slot.pointer_name = "Black"
                            else:
                                child.snap.edge_w1 = 'Exterior_Edge'
                                for mat_slot in child.snap.material_slots:
                                    if mat_slot.name == 'LeftEdge':
                                        mat_slot.pointer_name = "Garage_Panel_Edges"
                        else:
                            child.snap.edge_w1 = 'Edge'
                            for mat_slot in child.snap.material_slots:
                                if mat_slot.name == 'LeftEdge':
                                    mat_slot.pointer_name = "Closet_Part_Edges"
            else:
                for child in assembly.obj_bp.children:
                    if child.snap.type_mesh == 'CUTPART':
                        child.snap.edge_w1 = ''
                        for mat_slot in child.snap.material_slots:
                            if mat_slot.name == 'LeftEdge':
                                mat_slot.pointer_name = "Core"
        if exposed_right:
            if exposed_right.get_value():
                for child in assembly.obj_bp.children:
                    if child.snap.type_mesh == 'CUTPART':
                        if mat_type.name == "Garage Material":
                            if mat_color_name == "Graphite Spectrum":
                                child.snap.edge_w2 = 'Black_Edge'
                                for mat_slot in child.snap.material_slots:
                                    if mat_slot.name == 'RightEdge':
                                        mat_slot.pointer_name = "Black"
                            else:
                                child.snap.edge_w2 = 'Exterior_Edge'
                                for mat_slot in child.snap.material_slots:
                                    if mat_slot.name == 'RightEdge':
                                        mat_slot.pointer_name = "Garage_Panel_Edges"
                        else:
                            child.snap.edge_w2 = 'Edge'
                            for mat_slot in child.snap.material_slots:
                                if mat_slot.name == 'RightEdge':
                                    mat_slot.pointer_name = "Closet_Part_Edges"
            else:
                for child in assembly.obj_bp.children:
                    if child.snap.type_mesh == 'CUTPART':
                        child.snap.edge_w2 = ''
                        for mat_slot in child.snap.material_slots:
                            if mat_slot.name == 'RightEdge':
                                mat_slot.pointer_name = "Core"

        if exposed_back:
            if exposed_back.get_value():
                for child in assembly.obj_bp.children:
                    if child.snap.type_mesh == 'CUTPART':
                        if mat_type.name == "Garage Material":
                            if mat_color_name == "Graphite Spectrum":
                                child.snap.edge_l2 = 'Black_Edge'
                                for mat_slot in child.snap.material_slots:
                                    if mat_slot.name == 'BackEdge':
                                        mat_slot.pointer_name = "Black"
                            else:
                                child.snap.edge_l2 = 'Exterior_Edge'
                                for mat_slot in child.snap.material_slots:
                                    if mat_slot.name == 'BackEdge':
                                        mat_slot.pointer_name = "Garage_Panel_Edges"
                        else:
                            child.snap.edge_l2 = 'Edge'
                            for mat_slot in child.snap.material_slots:
                                if mat_slot.name == 'BackEdge':
                                    mat_slot.pointer_name = "Closet_Part_Edges"
            else:
                for child in assembly.obj_bp.children:
                    if child.snap.type_mesh == 'CUTPART':
                        child.snap.edge_l2 = ''
                        for mat_slot in child.snap.material_slots:
                            if mat_slot.name == 'BackEdge':
                                mat_slot.pointer_name = "Core"

    def update_closet_defaults(self, context):
        """
        Currently this function will just update the 1" thick adjustable shelves option when
        Garage Material was just selected, but we can use this to hopefully change closet defaults whenever necessary.
        """
        closet_defaults = context.scene.sn_closets.closet_defaults
        cab_mat_props = self.props_closet_materials
        mat_type = cab_mat_props.materials.get_mat_type()
        if closet_defaults.temp_mat_type_name != mat_type.name:
            if mat_type.name == "Garage Material":
                closet_defaults.thick_adjustable_shelves = True
                exec("bpy.ops.sn_prompt.update_all_prompts_in_scene(prompt_name='Thick Adjustable Shelves', prompt_type='CHECKBOX', bool_value=True)")
            else:
                closet_defaults.thick_adjustable_shelves = False
                exec("bpy.ops.sn_prompt.update_all_prompts_in_scene(prompt_name='Thick Adjustable Shelves', prompt_type='CHECKBOX', bool_value=False)")

            closet_defaults.temp_mat_type_name = mat_type.name


    def execute(self, context):
        self.closet_props = context.scene.sn_closets
        self.props_closet_materials = context.scene.closet_materials
        material_color = bpy.context.scene.closet_materials.materials.get_mat_color()

        if self.only_update_pointers:
            self.update_material_pointers(context)
            self.update_drawer_materials()
        else:
            self.update_drawer_materials()

            for assembly in self.scene_assemblies(context):
                props = assembly.obj_bp.sn_closets

                if props.is_panel_bp:
                    self.set_panel_material(assembly)

                if props.is_countertop_bp:
                    self.set_countertop_material(assembly)

                # Topshelf
                if props.is_plant_on_top_bp:
                    exposed_left = assembly.get_prompt("Exposed Left")
                    exposed_right = assembly.get_prompt("Exposed Right")
                    exposed_back = assembly.get_prompt("Exposed Back")

                    if exposed_left:
                        if exposed_left.get_value():
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_w1 = 'Edge'
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'LeftEdge':
                                            mat_slot.pointer_name = "Closet_Part_Edges"
                        else:
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_w1 = ''
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'LeftEdge':
                                            mat_slot.pointer_name = "Core"
                    if exposed_right:
                        if exposed_right.get_value():
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_w2 = 'Edge'
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'RightEdge':
                                            mat_slot.pointer_name = "Closet_Part_Edges"
                        else:
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_w2 = ''
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'RightEdge':
                                            mat_slot.pointer_name = "Core"

                    if exposed_back:
                        if exposed_back.get_value():
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_l2 = 'Edge'
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'BackEdge':
                                            mat_slot.pointer_name = "Closet_Part_Edges"
                        else:
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_l2 = ''
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'BackEdge':
                                            mat_slot.pointer_name = "Core"

                # Crown
                if props.is_crown_molding:
                    exposed_left = assembly.get_prompt("Exposed Left")
                    exposed_right = assembly.get_prompt("Exposed Right")
                    exposed_back = assembly.get_prompt("Exposed Back")
                    exposed_front = assembly.get_prompt("Exposed Front")

                    if exposed_left:
                        if exposed_left.get_value():
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_w1 = 'Edge'
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'LeftEdge':
                                            mat_slot.pointer_name = "Closet_Part_Edges_Secondary"
                        else:
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_w1 = ''
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'LeftEdge':
                                            mat_slot.pointer_name = "Core"
                    if exposed_right:
                        if exposed_right.get_value():
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_w2 = 'Edge'
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'RightEdge':
                                            mat_slot.pointer_name = "Closet_Part_Edges_Secondary"
                        else:
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_w2 = ''
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'RightEdge':
                                            mat_slot.pointer_name = "Core"

                    if exposed_back:
                        if exposed_back.get_value():
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_l2 = 'Edge'
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'BackEdge':
                                            mat_slot.pointer_name = "Closet_Part_Edges_Secondary"
                        else:
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_l2 = ''
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'BackEdge':
                                            mat_slot.pointer_name = "Core"

                    if exposed_front:
                        if exposed_front.get_value():
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_l1 = 'Edge'
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'Edgebanding':
                                            mat_slot.pointer_name = "Closet_Part_Edges_Secondary"
                        else:
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_l1 = ''
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'Edgebanding':
                                            mat_slot.pointer_name = "Core"

                # Metal Garage Leg
                if "IS_BP_METAL_LEG" in assembly.obj_bp:
                    metal_color = sn_types.Assembly(
                        assembly.obj_bp.parent).get_prompt("Metal Color")
                    if metal_color:
                        for child in assembly.obj_bp.children:
                            for mat_slot in child.snap.material_slots:
                                if mat_slot.name == 'Metal':
                                    if metal_color.get_value() == 0:
                                        mat_slot.pointer_name = "Steel"
                                    elif metal_color.get_value() == 1:
                                        mat_slot.pointer_name = "Black"
                                    elif metal_color.get_value() == 2:
                                        mat_slot.pointer_name = "Chrome"

                if "IS_BP_VALET_ROD" in assembly.obj_bp:
                    metal_color = assembly.get_prompt("Metal Color")
                    if metal_color:
                        for child in assembly.obj_bp.children:
                            for cchild in child.children:
                                for mat_slot in cchild.snap.material_slots:
                                    if mat_slot.name == 'Chrome':
                                        if metal_color.get_value() == 0:
                                            mat_slot.pointer_name = "Chrome"
                                        elif metal_color.get_value() == 1:
                                            mat_slot.pointer_name = "Aluminum"
                                        elif metal_color.get_value() == 2:
                                            mat_slot.pointer_name = "Nickel"
                                        elif metal_color.get_value() == 3:
                                            mat_slot.pointer_name = "Gold"
                                        elif metal_color.get_value() == 4:
                                            mat_slot.pointer_name = "Black"
                                        elif metal_color.get_value() == 5:
                                            mat_slot.pointer_name = "Slate"

                if "IS_BP_BELT_RACK" in assembly.obj_bp:
                    metal_color = assembly.get_prompt("Metal Color")
                    if metal_color:
                        for child in assembly.obj_bp.children:
                            for mat_slot in child.snap.material_slots:
                                if mat_slot.name == 'Chrome':
                                    if metal_color.get_value() == 0:
                                        mat_slot.pointer_name = "Chrome"
                                    elif metal_color.get_value() == 1:
                                        mat_slot.pointer_name = "Aluminum"
                                    elif metal_color.get_value() == 2:
                                        mat_slot.pointer_name = "Nickel"
                                    elif metal_color.get_value() == 3:
                                        mat_slot.pointer_name = "Gold"
                                    elif metal_color.get_value() == 4:
                                        mat_slot.pointer_name = "Black"
                                    elif metal_color.get_value() == 5:
                                        mat_slot.pointer_name = "Slate"

                if "IS_BP_TIE_RACK" in assembly.obj_bp:
                    metal_color = assembly.get_prompt("Metal Color")
                    if metal_color:
                        for child in assembly.obj_bp.children:
                            for mat_slot in child.snap.material_slots:
                                if mat_slot.name == 'Chrome':
                                    if metal_color.get_value() == 0:
                                        mat_slot.pointer_name = "Chrome"
                                    elif metal_color.get_value() == 1:
                                        mat_slot.pointer_name = "Aluminum"
                                    elif metal_color.get_value() == 2:
                                        mat_slot.pointer_name = "Nickel"
                                    elif metal_color.get_value() == 3:
                                        mat_slot.pointer_name = "Gold"
                                    elif metal_color.get_value() == 4:
                                        mat_slot.pointer_name = "Black"
                                    elif metal_color.get_value() == 5:
                                        mat_slot.pointer_name = "Slate"

                if "IS_FILLER" in assembly.obj_bp:
                    exposed_left = assembly.get_prompt("Exposed Left")
                    exposed_right = assembly.get_prompt("Exposed Right")
                    exposed_back = assembly.get_prompt("Exposed Back")
                    if exposed_left:
                        if exposed_left.get_value():
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_w1 = 'Edge'
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'LeftEdge':
                                            mat_slot.pointer_name = "Closet_Part_Edges"
                        else:
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_w1 = ''
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'LeftEdge':
                                            mat_slot.pointer_name = "Core"
                    if exposed_right:
                        if exposed_right.get_value():
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_w2 = 'Edge'
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'RightEdge':
                                            mat_slot.pointer_name = "Closet_Part_Edges"
                        else:
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_w2 = ''
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'RightEdge':
                                            mat_slot.pointer_name = "Core"

                    if exposed_back:
                        if exposed_back.get_value():
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_l2 = 'Edge'
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'BackEdge':
                                            mat_slot.pointer_name = "Closet_Part_Edges"
                        else:
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_l2 = ''
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'BackEdge':
                                            mat_slot.pointer_name = "Core"

                # Wall_Cleat
                if "IS_WALL_CLEAT" in assembly.obj_bp:

                    exposed_left = assembly.get_prompt("Exposed Left")
                    exposed_right = assembly.get_prompt("Exposed Right")
                    exposed_top = assembly.get_prompt("Exposed Top")
                    exposed_bottom = assembly.get_prompt("Exposed Bottom")

                    if exposed_left:
                        if exposed_left.get_value():
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_w1 = 'Edge'
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'LeftEdge':
                                            mat_slot.pointer_name = "Closet_Part_Edges"
                        else:
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_w1 = ''
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'LeftEdge':
                                            mat_slot.pointer_name = "Core"
                    if exposed_right:
                        if exposed_right.get_value():
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_w2 = 'Edge'
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'RightEdge':
                                            mat_slot.pointer_name = "Closet_Part_Edges"
                        else:
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_w2 = ''
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'RightEdge':
                                            mat_slot.pointer_name = "Core"

                    if exposed_top:
                        if exposed_top.get_value():
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_l2 = 'Edge'
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'Edgebanding':
                                            mat_slot.pointer_name = "Closet_Part_Edges"
                        else:
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_l2 = ''
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'Edgebanding':
                                            mat_slot.pointer_name = "Core"

                    if exposed_bottom:
                        if exposed_bottom.get_value():
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_l2 = 'Edge'
                                for mat_slot in child.snap.material_slots:
                                    if mat_slot.name == 'BackEdge':
                                        mat_slot.pointer_name = "Closet_Part_Edges"
                        else:
                            for child in assembly.obj_bp.children:
                                if child.snap.type_mesh == 'CUTPART':
                                    child.snap.edge_l2 = ''
                                    for mat_slot in child.snap.material_slots:
                                        if mat_slot.name == 'BackEdge':
                                            mat_slot.pointer_name = "Core"
                if assembly.obj_prompts:
                    catnum = assembly.get_prompt("CatNum")
                    if catnum:
                        assembly.obj_bp.snap.comment_2 = str(
                            int(catnum.get_value()))

                if props.is_door_bp:
                    self.set_door_material(assembly)

                elif props.is_shelf_bp or assembly.obj_bp.get("IS_SHELF"):
                    self.set_shelf_material(assembly)

                elif assembly.obj_bp.get("IS_CLEAT"):
                    self.set_cleat_material(assembly)

                elif assembly.obj_bp.get("IS_BACK"):
                    self.set_back_material(assembly)

                elif props.is_drawer_bottom_bp:
                    self.set_drawer_bottom_material(assembly)

                elif props.is_drawer_back_bp or props.is_drawer_side_bp or props.is_drawer_sub_front_bp:
                    self.set_drawer_part_material(assembly)
                
                elif assembly.obj_bp.get("IS_BP_DRAWER_FRONT"):
                    self.set_drawer_front_material(assembly)
                
                elif assembly.obj_bp.get("IS_BP_COUNTERTOP"):
                    self.set_countertop_material(assembly)

                else:
                    self.set_material(assembly)

            self.update_material_pointers(context)

            self.update_closet_defaults(context)

            bpy.ops.snap.update_scene_from_pointers()

        return {'FINISHED'}


class SN_MAT_OT_update_scene_from_pointers(Operator):
    bl_idname = "snap.update_scene_from_pointers"
    bl_label = "Update Scene From Pointers"
    bl_description = "This will update the scene with the updated pointer information."

    def execute(self, context):
        for obj in context.visible_objects:
            obj.location = obj.location

        for obj in bpy.data.objects:
            if obj.type in {'MESH', 'CURVE'}:
                sn_utils.assign_materials_from_pointers(obj)

        return {'FINISHED'}


class SN_MAT_OT_Unpack_Material_Images(Operator):
    bl_idname = "closet_materials.unpack_material_images"
    bl_label = "Unpack Closet Material Images"
    bl_description = ""
    bl_options = {'UNDO'}

    material_files = []
    materials_dir: StringProperty(
        name="Materials Path",
        description="Material directory to unpack",
        subtype='FILE_PATH')

    _timer = None

    item_list = []

    def invoke(self, context, event):
        wm = context.window_manager
        props = context.window_manager.snap
        self.materials_dir = sn_paths.CLOSET_MATERIAL_DIR
        textures_dir = os.path.join(self.materials_dir, "textures")

        if not os.path.exists(textures_dir):
            os.makedirs(textures_dir)

        bpy.ops.sn_library.open_browser_window(
            path=os.path.join(self.materials_dir, "textures"))

        self.item_list = []

        for f in os.listdir(self.materials_dir):
            if ".blend" in f:
                self.item_list.append(f)

        props.total_items = len(self.item_list)
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)

        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        progress = context.window_manager.snap

        if event.type == 'ESC':
            return {'FINISHED'}

        if event.type == 'TIMER':
            if progress.current_item + 1 <= len(self.item_list):
                b_file = self.item_list[progress.current_item]
                mat_file_path = os.path.abspath(
                    os.path.join(self.materials_dir, b_file))
                script = os.path.join(
                    bpy.app.tempdir, 'unpack_material_images.py')
                script_file = open(script, 'w')
                script_file.write("import bpy\n")
                script_file.write(
                    "bpy.ops.file.unpack_all(method='WRITE_LOCAL')\n")
                script_file.close()
                print(bpy.app.binary_path)
                print(mat_file_path)
                print(bpy.app.binary_path + ' "' + mat_file_path +
                      '"' + ' -b --python ' + '"' + script + '"')
                subprocess.call(bpy.app.binary_path + ' "' + mat_file_path +
                                '"' + ' -b --python ' + '"' + script + '"')
                progress.current_item += 1
                if progress.current_item + 1 <= len(self.item_list):
                    header_text = "Processing Item " + \
                        str(progress.current_item + 1) + \
                        " of " + str(progress.total_items)
                    context.area.header_text_set(text=header_text)
            else:
                return self.cancel(context)
        return {'PASS_THROUGH'}

    def cancel(self, context):
        progress = context.window_manager.snap
        progress.current_item = 0
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        context.window.cursor_set('DEFAULT')
        context.area.header_text_set(None)
        return {'FINISHED'}


class SN_MAT_OT_check_mats(Operator):
    bl_idname = "closet_materials.check_mats"
    bl_label = "check_mats"
    bl_description = ""
    bl_options = {'UNDO'}

    def execute(self, context):
        materials_dir = sn_paths.CLOSET_MATERIAL_DIR
        search_directory = os.path.join(
            materials_dir, "Closet Materials")
        tex_directory = os.path.join(search_directory, "textures")

        mat_file_list = []
        tex_list = []

        for f in os.listdir(search_directory):
            if ".blend" in f:
                mat_file_list.append(f.split(".")[0])

        for f in os.listdir(tex_directory):
            tex_list.append(f.split(".")[0])

        for f in os.listdir(search_directory):
            if f.split(".")[0] in tex_list:
                pass
            else:
                print("Material file not in tex dir:", f)

        for f in os.listdir(tex_directory):
            if f.split(".")[0] in mat_file_list:
                pass
            else:
                print("Texture not in material file dir:", f)

        return {'FINISHED'}


class SN_MAT_OT_Create_Material_Library(Operator):
    bl_idname = "closet_materials.create_material_library"
    bl_label = "Create Closet Material Library"
    bl_description = ""
    bl_options = {'UNDO'}

    def execute(self, context):
        materials_dir = sn_paths.CLOSET_MATERIAL_DIR
        tex_directory = os.path.join(materials_dir, "textures")
        template_dir = os.path.join(materials_dir, "template_material")
        new_materials_dir = os.path.join(template_dir, "Materials")
        template_file = os.path.join(
            materials_dir, "template_material", "template_material.blend")

        for image_name in os.listdir(tex_directory):
            tex_file_path = os.path.abspath(
                os.path.join(tex_directory, image_name))

            script = os.path.join(
                bpy.app.tempdir, 'create_material_library.py')
            script_file = open(script, 'w')
            script_file.write("import bpy\n")
            script_file.write(
                "bpy.ops.image.open(filepath=r'" + tex_file_path + "', files=[{'name':'" + image_name + "', 'name':'" + image_name + "'}], relative_path=False, show_multiview=False)\n")
            script_file.write(
                "bpy.data.materials['template_material'].node_tree.nodes['Image Texture'].image = bpy.data.images['" + image_name + "']\n")
            script_file.write(
                "bpy.data.materials['template_material'].name = '" + image_name.split(".")[0] + "'\n")
            script_file.write("bpy.ops.wm.save_as_mainfile(filepath=r'" + os.path.normpath(
                os.path.join(new_materials_dir, image_name.split(".")[0])) + ".blend')\n")

            script_file.close()
            subprocess.call(bpy.app.binary_path + ' "' + template_file +
                            '"' + ' -b --python ' + '"' + script + '"')

        return {'FINISHED'}


classes = (
    SN_MAT_OT_Poll_Assign_Materials,
    SN_MAT_OT_Assign_Materials,
    SN_MAT_OT_update_scene_from_pointers,
    SN_MAT_OT_Unpack_Material_Images,
    SN_MAT_OT_check_mats,
    SN_MAT_OT_Create_Material_Library
)

register, unregister = bpy.utils.register_classes_factory(classes)

# if __name__ == "__main__":
#     register()
