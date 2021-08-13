import os

import bpy
from bpy.types import PropertyGroup
from bpy.props import (
    StringProperty,
    BoolProperty,
    IntProperty,
    CollectionProperty,
    PointerProperty,
    FloatProperty,
)

from snap import sn_paths


def render_material_exists(material_name):
    materials_dir = sn_paths.CLOSET_MATERIAL_DIR
    search_directory = os.path.join(materials_dir, "Closet Materials")

    if os.path.isdir(search_directory):
        files = os.listdir(search_directory)

        if material_name + ".blend" in files:
            return True
        else:
            return False


class ColorMixIn:
    has_render_mat: BoolProperty(name="Has Rendering Material")
    oversize_max_len: IntProperty(name="Oversize Material Max Length", default=0)

    def render_material_exists(self, material_name):
        cls_type = self.bl_rna.name

        if cls_type in ("EdgeColor", "MaterialColor"):
            snap_db_mat_dir = sn_paths.CLOSET_MATERIAL_DIR
            search_directory = snap_db_mat_dir

        elif cls_type == "CountertopColor":
            countertop_mat_dir = sn_paths.COUNTERTOP_MATERIAL_DIR
            search_directory = countertop_mat_dir

        mat_exists = False

        if os.path.isdir(search_directory):
            files = os.listdir(search_directory)

            if material_name + ".blend" in files:
                mat_exists = True

        return mat_exists

    def check_render_material(self):
        if self.render_material_exists(self.name):
            self.has_render_mat = True
        else:
            self.has_render_mat = False

    def get_icon(self):
        if self.has_render_mat:
            return 'RADIOBUT_OFF'
        else:
            return 'ERROR'


class EdgeColor(PropertyGroup, ColorMixIn):
    color_code: IntProperty()
    description: StringProperty()

    def draw(self, layout):
        pass


class EdgeType(PropertyGroup):
    description: StringProperty()
    type_code: IntProperty()
    colors: CollectionProperty(type=EdgeColor)

    def set_color_index(self, index):
        scene_props = bpy.context.scene.closet_materials
        scene_props.edge_color_index = index

    def get_edge_color(self):
        scene_props = bpy.context.scene.closet_materials
        return self.colors[scene_props.edge_color_index]          

    def get_inventory_edge_name(self):
        return "EB {} {}".format(self.name, self.type_code)    

    def draw(self, layout):
        color = self.get_edge_color()

        row = layout.row()
        split = row.split(factor=0.25)
        split.label(text="Color:")
        split.menu(
            "SNAP_MATERIAL_MT_Edge_Colors",
            text=color.name,
            icon='RADIOBUT_ON' if color.has_render_mat else 'ERROR')

        if not color.has_render_mat:
            row = layout.row()
            split = row.split(factor=0.25)
            split.label(text="")
            box = split.box()
            row = box.row()
            row.label(text="Missing render material.", icon='ERROR')   


class Edges(PropertyGroup):
    edge_types: CollectionProperty(type=EdgeType)

    def set_type_index(self, index):
        scene_props = bpy.context.scene.closet_materials
        scene_props.edge_type_index = index
        scene_props.edge_color_index = 0

    def get_edge_type(self):
        scene_props = bpy.context.scene.closet_materials
        return self.edge_types[scene_props.edge_type_index]

    def get_edge_color(self):
        return self.get_edge_type().get_edge_color()        

    def draw(self, layout):
        box = layout.box()
        box.label(text="Edge Selection:")

        if len(self.edge_types) > 0:
            row = box.row()
            split = row.split(factor=0.25)
            split.label(text="Type:")
            split.menu('SNAP_MATERIAL_MT_Edge_Types', text=self.get_edge_type().name, icon='RADIOBUT_ON')
            self.get_edge_type().draw(box)

        else:
            row = box.row()
            row.label(text="None", icon='ERROR')


class DoorDrawerEdgeType(PropertyGroup):   
    description: StringProperty()
    type_code: IntProperty()
    colors: CollectionProperty(type=EdgeColor)

    def set_color_index(self, index):
        scene_props = bpy.context.scene.closet_materials
        scene_props.door_drawer_edge_color_index = index

    def get_edge_color(self):
        scene_props = bpy.context.scene.closet_materials
        return self.colors[scene_props.door_drawer_edge_color_index]          

    def get_inventory_edge_name(self):
        return "EB {} {}".format(self.name, self.type_code)    

    def draw(self, layout):
        color = self.get_edge_color()

        row = layout.row()
        split = row.split(factor=0.25)
        split.label(text="Color:")            
        split.menu(
            "SNAP_MATERIAL_MT_Door_Drawer_Edge_Colors",
            text=color.name,
            icon='RADIOBUT_ON' if color.has_render_mat else 'ERROR')

        if not color.has_render_mat:
            row = layout.row()
            split = row.split(factor=0.25)
            split.label(text="")             
            box = split.box()
            row = box.row()
            row.label(text="Missing render material.", icon='ERROR')   


class DoorDrawerEdges(PropertyGroup):
    edge_types: CollectionProperty(type=DoorDrawerEdgeType)

    def set_type_index(self, index):
        scene_props = bpy.context.scene.closet_materials
        scene_props.door_drawer_edge_type_index = index
        scene_props.door_drawer_edge_color_index = 0

    def get_edge_type(self):
        scene_props = bpy.context.scene.closet_materials
        return self.edge_types[scene_props.door_drawer_edge_type_index]

    def get_edge_color(self):
        return self.get_edge_type().get_edge_color()        

    def draw(self, layout):
        box = layout.box()
        box.label(text="Edge Selection:")

        if len(self.edge_types) > 0:
            row = box.row()
            split = row.split(factor=0.25)
            split.label(text="Type:")
            split.menu('SNAP_MATERIAL_MT_Door_Drawer_Edge_Types', text=self.get_edge_type().name, icon='RADIOBUT_ON')
            self.get_edge_type().draw(box)

        else:
            row = box.row()
            row.label(text="None", icon='ERROR')


class SecondaryEdgeType(PropertyGroup):   
    description: StringProperty()
    type_code: IntProperty()
    colors: CollectionProperty(type=EdgeColor)

    def set_color_index(self, index):
        scene_props = bpy.context.scene.closet_materials
        scene_props.secondary_edge_color_index = index

    def get_edge_color(self):
        scene_props = bpy.context.scene.closet_materials
        return self.colors[scene_props.secondary_edge_color_index]         

    def get_inventory_edge_name(self):
        return "EB {} {}".format(self.name, self.type_code)          

    def draw(self, layout):
        color = self.get_edge_color()

        row = layout.row()
        split = row.split(factor=0.25)
        split.label(text="Color:")            
        split.menu(
            "SNAP_MATERIAL_MT_Secondary_Edge_Colors",
            text=color.name,
            icon='RADIOBUT_ON' if color.has_render_mat else 'ERROR')

        if not color.has_render_mat:
            row = layout.row()
            split = row.split(factor=0.25)
            split.label(text="")             
            box = split.box()
            row = box.row()
            row.label(text="Missing render material.", icon='ERROR') 


class SecondaryEdges(PropertyGroup):
    edge_types: CollectionProperty(type=SecondaryEdgeType)

    def set_type_index(self, index):
        scene_props = bpy.context.scene.closet_materials
        scene_props.secondary_edge_type_index = index
        scene_props.secondary_edge_color_index = 0

    def get_edge_type(self):
        scene_props = bpy.context.scene.closet_materials
        return self.edge_types[scene_props.secondary_edge_type_index]

    def get_edge_color(self):
        return self.get_edge_type().get_edge_color()         

    def has_render_mat(self):
        return self.get_edge_type().has_render_mat

    def draw(self, layout):
        box = layout.box()
        box.label(text="Secondary Edge Selection:")

        if len(self.edge_types) > 0:
            row = box.row()
            split = row.split(factor=0.25)
            split.label(text="Type:")
            split.menu('SNAP_MATERIAL_MT_Secondary_Edge_Types', text=self.get_edge_type().name, icon='RADIOBUT_ON')
            self.get_edge_type().draw(box)

        else:
            row = box.row()
            row.label(text="None", icon='ERROR')        


class MaterialColor(PropertyGroup, ColorMixIn):
    description: StringProperty()
    color_code: IntProperty()

    def draw(self, layout):
        pass


class MaterialType(PropertyGroup):
    description: StringProperty()
    type_code: IntProperty()
    colors: CollectionProperty(type=MaterialColor)

    def set_color_index(self, index):
        scene_props = bpy.context.scene.closet_materials
        scene_props.mat_color_index = index

    def get_mat_color(self):
        scene_props = bpy.context.scene.closet_materials
        return self.colors[scene_props.mat_color_index] 

    def get_inventory_material_name(self):
        return "{} {}".format(self.name, self.type_code)

    def draw(self, layout):
        color = self.get_mat_color()

        row = layout.row()
        split = row.split(factor=0.25)
        split.label(text="Color:")            
        split.menu(
            "SNAP_MATERIAL_MT_Mat_Colors",
            text=color.name,
            icon='RADIOBUT_ON' if color.has_render_mat else 'ERROR')

        if color.oversize_max_len > 0:
            row = layout.row()
            split = row.split(factor=0.25)
            split.label(text="")

            max_len_inch = round(color.oversize_max_len / 25.4, 2)
            max_len_str = 'Max Length: {}"'.format(max_len_inch)
            split.label(text=max_len_str, icon='INFO')      

        if not color.has_render_mat:
            row = layout.row()
            split = row.split(factor=0.25)
            split.label(text="")             
            box = split.box()
            row = box.row()
            row.label(text="Missing render material.", icon='ERROR') 


class Materials(PropertyGroup):
    mat_types: CollectionProperty(type=MaterialType)
    textured_mel_color_list = []
    mel_color_list = []
    veneer_backing_color_list = []

    def create_color_lists(self):
        self.textured_mel_color_list.clear()
        self.mel_color_list.clear()
        self.veneer_backing_color_list.clear()

        for mat_type in self.mat_types:
            if mat_type.name == 'Textured Melamine':
                for color in mat_type.colors:
                    self.textured_mel_color_list.append((color.name, color.name, color.name))
            if mat_type.name == 'Melamine':
                for color in mat_type.colors:
                    self.mel_color_list.append((color.name, color.name, color.name))
            if mat_type.name == 'Veneer':
                # Add 1/4" backing veneer
                for color in mat_type.colors:
                    if (color.name, color.name, color.name) not in self.veneer_backing_color_list:
                        self.veneer_backing_color_list.append((color.name, color.name, color.name))

    def set_type_index(self, index):
        scene_props = bpy.context.scene.closet_materials
        scene_props.mat_type_index = index
        scene_props.mat_color_index = 0

    def get_mat_type(self):
        scene_props = bpy.context.scene.closet_materials
        return self.mat_types[scene_props.mat_type_index]

    def get_mat_color(self):
        return self.get_mat_type().get_mat_color()

    def has_render_mat(self):
        return self.get_mat_type().has_render_mat

    def draw(self, layout):
        box = layout.box()
        box.label(text="Material Selection:")

        if len(self.mat_types) > 0:
            row = box.row()
            split = row.split(factor=0.25)
            split.label(text="Type:")
            split.menu('SNAP_MATERIAL_MT_Mat_Types', text=self.get_mat_type().name, icon='RADIOBUT_ON')
            self.get_mat_type().draw(box) 

        else:
            row = box.row()
            row.label(text="None", icon='ERROR')               


class DoorDrawerMaterialType(PropertyGroup):
    description: StringProperty()
    type_code: IntProperty()
    colors: CollectionProperty(type=MaterialColor)

    def set_color_index(self, index):
        scene_props = bpy.context.scene.closet_materials
        scene_props.door_drawer_mat_color_index = index

    def get_mat_color(self):
        scene_props = bpy.context.scene.closet_materials
        return self.colors[scene_props.door_drawer_mat_color_index] 

    def get_inventory_material_name(self):
        return "{} {}".format(self.name, self.type_code)

    def draw(self, layout):
        color = self.get_mat_color()

        row = layout.row()
        split = row.split(factor=0.25)
        split.label(text="Color:")            
        split.menu(
            "SNAP_MATERIAL_MT_Door_Drawer_Mat_Colors",
            text=color.name,
            icon='RADIOBUT_ON' if color.has_render_mat else 'ERROR')

        if not color.has_render_mat:
            row = layout.row()
            split = row.split(factor=0.25)
            split.label(text="")             
            box = split.box()
            row = box.row()
            row.label(text="Missing render material.", icon='ERROR') 


class DoorDrawerMaterials(PropertyGroup):
    mat_types: CollectionProperty(type=DoorDrawerMaterialType)
    textured_mel_color_list = []
    mel_color_list = []
    veneer_backing_color_list = []

    def create_color_lists(self):
        self.textured_mel_color_list.clear()
        self.mel_color_list.clear()
        self.veneer_backing_color_list.clear()

        for mat_type in self.mat_types:
            if mat_type.name == 'Textured Melamine':
                for color in mat_type.colors:
                    self.textured_mel_color_list.append((color.name, color.name, color.name))
            if mat_type.name == 'Melamine':
                for color in mat_type.colors:
                    self.mel_color_list.append((color.name, color.name, color.name))
            if mat_type.name == 'Veneer':
                # Add 1/4" backing veneer
                for color in mat_type.colors:
                    if (color.name, color.name, color.name) not in self.veneer_backing_color_list:
                        self.veneer_backing_color_list.append((color.name, color.name, color.name))

    def set_type_index(self, index):
        scene_props = bpy.context.scene.closet_materials
        scene_props.door_drawer_mat_type_index = index
        scene_props.door_drawer_mat_color_index = 0

    def get_mat_type(self):
        scene_props = bpy.context.scene.closet_materials
        return self.mat_types[scene_props.door_drawer_mat_type_index]

    def get_mat_color(self):
        return self.get_mat_type().get_mat_color()

    def has_render_mat(self):
        return self.get_mat_type().has_render_mat

    def draw(self, layout):
        box = layout.box()
        box.label(text="Material Selection:")

        if len(self.mat_types) > 0:
            row = box.row()
            split = row.split(factor=0.25)
            split.label(text="Type:")
            split.menu('SNAP_MATERIAL_MT_Door_Drawer_Mat_Types', text=self.get_mat_type().name, icon='RADIOBUT_ON')
            self.get_mat_type().draw(box) 

        else:
            row = box.row()
            row.label(text="None", icon='ERROR')               


class CountertopColor(PropertyGroup, ColorMixIn):
    chip_code: StringProperty()
    vendor: StringProperty()


class CountertopManufactuer(PropertyGroup):
    description: StringProperty()
    color_code: IntProperty()
    colors: CollectionProperty(type=CountertopColor)

    def set_color_index(self, index):
        scene_props = bpy.context.scene.closet_materials
        scene_props.ct_color_index = index

    def get_color(self):
        scene_props = bpy.context.scene.closet_materials
        return self.colors[scene_props.ct_color_index]


class CountertopType(PropertyGroup):
    type_code: IntProperty()
    description: StringProperty()
    manufactuers: CollectionProperty(type=CountertopManufactuer)
    colors: CollectionProperty(type=CountertopColor)

    def set_color_index(self, index):
        scene_props = bpy.context.scene.closet_materials
        scene_props.ct_color_index = index

    def set_mfg_index(self, index):
        scene_props = bpy.context.scene.closet_materials
        scene_props.ct_mfg_index = index
        scene_props.ct_color_index = 0     

    def get_mfg(self):
        scene_props = bpy.context.scene.closet_materials
        return self.manufactuers[scene_props.ct_mfg_index]

    def get_color(self):
        scene_props = bpy.context.scene.closet_materials

        if len(self.colors) > 0:
            return self.colors[scene_props.ct_color_index] 

        elif len(self.manufactuers) > 0:
            return self.get_mfg().get_color()

    def draw(self, layout):
        if len(self.colors) > 0:
            color = self.get_color()

            row = layout.row()
            split = row.split(factor=0.25)
            split.label(text="Color:")            
            split.menu(
                "SNAP_MATERIAL_MT_Countertop_Colors",
                text=color.name,
                icon='RADIOBUT_ON' if color.has_render_mat else 'ERROR')

            if not color.has_render_mat:
                row = layout.row()
                split = row.split(factor=0.25)
                split.label(text="")             
                box = split.box()
                row = box.row()
                row.label(text="Missing render material.", icon='ERROR')         

        elif len(self.manufactuers) > 0:
            mfg = self.get_mfg()
            color = mfg.get_color()

            row = layout.row()
            split = row.split(factor=0.25)
            split.label(text="Manufactuer:")             
            split.menu("SNAP_MATERIAL_MT_Countertop_Mfgs", text=mfg.name, icon='RADIOBUT_ON')

            row = layout.row()
            split = row.split(factor=0.25)
            split.label(text="Color:")   
            split.menu(
                "SNAP_MATERIAL_MT_Countertop_Colors",
                text=mfg.get_color().name,
                icon='RADIOBUT_ON' if color.has_render_mat else 'ERROR')

            if not color.has_render_mat:
                row = layout.row()
                split = row.split(factor=0.25)
                split.label(text="")             
                box = split.box()
                row = box.row()
                row.label(text="Missing render material.", icon='ERROR') 


class CustomCountertops(PropertyGroup):
    name: StringProperty(name="Name")
    vendor: StringProperty(name="Vendor")
    color_code: StringProperty(name="Color Code")
    price: FloatProperty(name="Price")

    def get_color(self):
        pass

    def draw(self, layout):
        layout.prop(self, 'name')
        layout.prop(self, 'vendor')
        layout.prop(self, 'color_code')
        layout.prop(self, 'price')


class Countertops(PropertyGroup):
    countertop_types: CollectionProperty(type=CountertopType) 
    custom_countertop: PointerProperty(type=CustomCountertops)

    def set_ct_type_index(self, index):
        scene_props = bpy.context.scene.closet_materials
        scene_props.ct_type_index = index
        scene_props.ct_mfg_index = 0
        scene_props.ct_color_index = 0

    def get_type(self):
        scene_props = bpy.context.scene.closet_materials
        return self.countertop_types[scene_props.ct_type_index]

    def get_color(self):
        return self.get_type().get_color()

    def get_color_name(self):
        if "Melamine" in self.get_type().name:
            materials = bpy.context.scene.closet_materials.materials
            return materials.get_mat_color().name
        
        else:
            color = self.get_color()
            return color.name

    def color_has_render_mat(self):
        color = self.get_color()

        if color:
            if color.has_render_mat:
                return True
            else:
                return False
        else:
            return True

    def get_ct_inventory_name(self):
        ct_type = self.get_type()
        ct_color = self.get_color()
        ct_mfg = ct_type.get_mfg()
        
        if len(ct_type.colors) > 0:
            return "{} {}".format(ct_type.name, ct_color.name)
        
        elif len(ct_type.manufactuers) > 0:
            return "{} {} {}".format(ct_type.name, ct_mfg.name, ct_color.name)

    def draw(self, layout):
        box = layout.box()
        box.label(text="Countertop Selection:")

        if len(self.countertop_types) > 0:
            row = box.row()
            split = row.split(factor=0.25)
            split.label(text="Type:")
            split.menu('SNAP_MATERIAL_MT_Countertop_Types', text=self.get_type().name, icon='RADIOBUT_ON')
            self.get_type().draw(box)

            if self.get_type().name == "Custom":
                self.custom_countertop.draw(box)

        else:
            row = box.row()
            row.label(text="None", icon='ERROR')            


class StainColor(PropertyGroup):
    description: StringProperty()
    sku: StringProperty()


class GlazeColor(PropertyGroup):
    description: StringProperty()
    sku: StringProperty()


class GlazeStyle(PropertyGroup):
    description: StringProperty()
    sku: StringProperty()


class DoorColor(PropertyGroup):
    description: StringProperty()
    sku: StringProperty()


class GlassColor(PropertyGroup):
    description: StringProperty()
    sku: StringProperty()


class BackingVeneerColor(PropertyGroup):
    description: StringProperty()
    sku: StringProperty()


class DrawerSlideSize(PropertyGroup):
    slide_length_inch: FloatProperty()
    front_hole_dim_mm: IntProperty()
    back_hole_dim_mm: IntProperty()


class DrawerSlide(PropertyGroup):
    db_name: StringProperty()
    sizes: CollectionProperty(type=DrawerSlideSize)


classes = (
    EdgeColor,
    EdgeType,
    Edges,
    DoorDrawerEdgeType,
    DoorDrawerEdges,
    SecondaryEdgeType,
    SecondaryEdges,
    MaterialColor,
    MaterialType,
    Materials,
    DoorDrawerMaterialType,
    DoorDrawerMaterials,
    CountertopColor,
    CountertopManufactuer,
    CountertopType,
    CustomCountertops,
    Countertops,
    StainColor,
    GlazeColor,
    GlazeStyle,
    DoorColor,
    GlassColor,
    BackingVeneerColor,
    DrawerSlideSize,
    DrawerSlide
)

register, unregister = bpy.utils.register_classes_factory(classes)