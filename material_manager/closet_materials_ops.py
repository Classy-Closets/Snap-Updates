import os
import subprocess

import bpy
from bpy.types import Operator
from bpy.props import BoolProperty

from snap import sn_unit
from snap import sn_paths
from snap import sn_utils
from snap import sn_types


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
    only_update_pointers: BoolProperty(name="Only Update Pointers", default=False)

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

    def set_door_material(self, part):
        for obj in part.obj_bp.children:
            if obj.snap.type_mesh == 'CUTPART':
                cab_mat_props = self.props_closet_materials
                mat_type = cab_mat_props.door_drawer_materials.get_mat_type()
                edge_type = cab_mat_props.door_drawer_edges.get_edge_type()

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

            # Construction Defaults
            if default_props.box_type == 'MEL':
                drawer_surface.category_name = "Closet Materials"
                drawer_surface.item_name = "Oxford White"
            else:
                drawer_surface.category_name = "Closet Materials"
                drawer_surface.item_name = "Birch"

            surface_pointer.category_name = "Closet Materials"
            surface_pointer.item_name = mat_props.materials.get_mat_color().name

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
            moderno_door_pointer.item_name = mat_props.moderno_colors[mat_props.moderno_color_index].name

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

    def execute(self, context):
        self.closet_props = context.scene.sn_closets
        self.props_closet_materials = context.scene.closet_materials

        if self.only_update_pointers:
            self.update_material_pointers(context)
            self.update_drawer_materials()
        else:
            self.update_drawer_materials()

            for assembly in self.scene_assemblies(context):
                props = assembly.obj_bp.sn_closets

                if props.is_panel_bp:
                    if assembly.obj_x.location.x > sn_unit.inch(46.11):  # 36H or lower have to be edgebanded, but 46.10 doesn't work, so I made it 46.11 and now it does
                        exposed_bottom = assembly.get_prompt("Exposed Bottom")
                        if exposed_bottom:
                            if exposed_bottom.get_value():
                                for child in assembly.obj_bp.children:
                                    if child.snap.type_mesh == 'CUTPART':
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
                                child.snap.edge_w1 = 'Edge_2'
                                child.snap.edge_w2 = 'Edge_2'
                                for mat_slot in child.snap.material_slots:
                                    if mat_slot.name == 'TopBottomEdge':
                                        mat_slot.pointer_name = "Closet_Part_Edges_Secondary"

                if props.is_countertop_bp:
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

                # Metal Garage Leg
                if "IS_BP_METAL_LEG" in assembly.obj_bp:
                    metal_color = sn_types.Assembly(assembly.obj_bp.parent).get_prompt("Metal Color")
                    if metal_color:
                        for child in assembly.obj_bp.children:
                            for mat_slot in child.snap.material_slots:
                                if mat_slot.name == 'Metal':
                                    if metal_color.get_value() == 0:
                                        mat_slot.pointer_name = "Nickel"
                                    elif metal_color.get_value() == 1:
                                        mat_slot.pointer_name = "Chrome"
                                    elif metal_color.get_value() == 2:
                                        mat_slot.pointer_name = "Black"
                                    elif metal_color.get_value() == 3:
                                        mat_slot.pointer_name = "Aluminum"

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
                        assembly.obj_bp.snap.comment_2 = str(int(catnum.get_value()))

                if props.is_door_bp:
                    self.set_door_material(assembly)

                elif props.is_drawer_bottom_bp:
                    self.set_drawer_bottom_material(assembly)

                elif props.is_drawer_back_bp or props.is_drawer_side_bp or props.is_drawer_sub_front_bp:
                    self.set_drawer_part_material(assembly)
                else:
                    self.set_material(assembly)

            self.update_material_pointers(context)

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

    def execute(self, context):
        materials_dir = sn_paths.CLOSET_MATERIAL_DIR

        for f in os.listdir(materials_dir):
            if ".blend" in f:
                mat_file_path = os.path.abspath(
                    os.path.join(materials_dir, f))

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
        template_file = os.path.join(materials_dir, "template_material", "template_material.blend")

        for image_name in os.listdir(tex_directory):
            tex_file_path = os.path.abspath(os.path.join(tex_directory, image_name))

            script = os.path.join(bpy.app.tempdir, 'create_material_library.py')
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
            subprocess.call(bpy.app.binary_path + ' "' + template_file + '"' + ' -b --python ' + '"' + script + '"')

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
