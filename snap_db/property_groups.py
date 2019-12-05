import bpy
import operator
import os
from mv import utils

def render_material_exists(material_name):
    materials_dir = utils.get_library_dir("materials")
    search_directory = os.path.join(materials_dir, "Cabinet Materials", "Classy Closets")

    if os.path.isdir(search_directory):
        files = os.listdir(search_directory)
        possible_files = []

        if material_name + ".blend" in files:
            return True
        else:
            return False


class ColorMixIn:
    has_render_mat = bpy.props.BoolProperty(name="Has Rendering Material")

    def render_material_exists(self, material_name):
        materials_dir = utils.get_library_dir("materials")
        cls_type =  self.bl_rna.name

        if cls_type in ("EdgeColor", "MaterialColor"):
            search_directory = os.path.join(materials_dir, "Cabinet Materials", "Classy Closets")

        elif cls_type == "CountertopColor":
            search_directory = os.path.join(materials_dir, "Cabinet Materials", "Classy Closets CT")

        if os.path.isdir(search_directory):
            files = os.listdir(search_directory)
            possible_files = []

            if material_name + ".blend" in files:
                return True
            else:
                return False

    def check_render_material(self):
        if self.render_material_exists(self.name):
            self.has_render_mat = True
        else:
            self.has_render_mat = False

    def get_icon(self):
        if self.has_render_mat:
            return 'LINK'
        else:
            return 'ERROR'


class EdgeColor(bpy.types.PropertyGroup, ColorMixIn):
    color_code = bpy.props.IntProperty()
    description = bpy.props.StringProperty()

    def draw(layout):
        pass

bpy.utils.register_class(EdgeColor)


class EdgeType(bpy.types.PropertyGroup):   
    description = bpy.props.StringProperty()
    type_code = bpy.props.IntProperty()
    colors = bpy.props.CollectionProperty(type=EdgeColor)

    def set_color_index(self, index):
        scene_props = bpy.context.scene.db_materials
        scene_props.edge_color_index = index

    def get_edge_color(self):
        scene_props = bpy.context.scene.db_materials
        return self.colors[scene_props.edge_color_index]          

    def get_inventory_edge_name(self):
        return "EB {} {}".format(self.name, self.type_code)    

    def draw(self, layout):
        color = self.get_edge_color()

        row = layout.row()
        split = row.split(percentage=0.25)
        split.label("Color:")            
        split.menu("MENU_Edge_Colors", text=color.name, icon='SOLO_ON' if color.has_render_mat else 'ERROR')

        if not color.has_render_mat:
            row = layout.row()
            split = row.split(percentage=0.25)
            split.label("")             
            box = split.box()
            row = box.row()
            row.label("Missing render material.", icon='ERROR')   

bpy.utils.register_class(EdgeType)


class Edges(bpy.types.PropertyGroup):
    edge_types = bpy.props.CollectionProperty(type=EdgeType)

    def set_type_index(self, index):
        scene_props = bpy.context.scene.db_materials
        scene_props.edge_type_index = index
        scene_props.edge_color_index = 0

    def get_edge_type(self):
        scene_props = bpy.context.scene.db_materials
        return self.edge_types[scene_props.edge_type_index]

    def get_edge_color(self):
        return self.get_edge_type().get_edge_color()        

    def draw(self, layout):
        box = layout.box()
        box.label("Edge Selection:")

        if len(self.edge_types) > 0:
            row = box.row()
            split = row.split(percentage=0.25)
            split.label("Type:")
            split.menu('MENU_Edge_Types', text=self.get_edge_type().name, icon='SOLO_ON')
            self.get_edge_type().draw(box)

        else:
            row = box.row()
            row.label("None", icon='ERROR')

bpy.utils.register_class(Edges)


class SecondaryEdgeType(bpy.types.PropertyGroup):   
    description = bpy.props.StringProperty()
    type_code = bpy.props.IntProperty()
    colors = bpy.props.CollectionProperty(type=EdgeColor)

    def set_color_index(self, index):
        scene_props = bpy.context.scene.db_materials
        scene_props.secondary_edge_color_index = index

    def get_edge_color(self):
        scene_props = bpy.context.scene.db_materials
        return self.colors[scene_props.secondary_edge_color_index]         

    def get_inventory_edge_name(self):
        return "EB {} {}".format(self.name, self.type_code)          

    def draw(self, layout):
        color = self.get_edge_color()

        row = layout.row()
        split = row.split(percentage=0.25)
        split.label("Color:")            
        split.menu("MENU_Secondary_Edge_Colors", text=color.name, icon='SOLO_ON' if color.has_render_mat else 'ERROR')

        if not color.has_render_mat:
            row = layout.row()
            split = row.split(percentage=0.25)
            split.label("")             
            box = split.box()
            row = box.row()
            row.label("Missing render material.", icon='ERROR') 

bpy.utils.register_class(SecondaryEdgeType)


class SecondaryEdges(bpy.types.PropertyGroup):
    edge_types = bpy.props.CollectionProperty(type=SecondaryEdgeType)

    def set_type_index(self, index):
        scene_props = bpy.context.scene.db_materials
        scene_props.secondary_edge_type_index = index
        scene_props.secondary_edge_color_index = 0

    def get_edge_type(self):
        scene_props = bpy.context.scene.db_materials
        return self.edge_types[scene_props.secondary_edge_type_index]

    def get_edge_color(self):
        return self.get_edge_type().get_edge_color()         

    def has_render_mat(self):
        return self.get_edge_type().has_render_mat

    def draw(self, layout):
        box = layout.box()
        box.label("Secondary Edge Selection:")

        if len(self.edge_types) > 0:
            row = box.row()
            split = row.split(percentage=0.25)
            split.label("Type:")
            split.menu('MENU_Secondary_Edge_Types', text=self.get_edge_type().name, icon='SOLO_ON')
            self.get_edge_type().draw(box)

        else:
            row = box.row()
            row.label("None", icon='ERROR')        

bpy.utils.register_class(SecondaryEdges)


class MaterialColor(bpy.types.PropertyGroup, ColorMixIn):
    description = bpy.props.StringProperty()
    color_code = bpy.props.IntProperty()

    def draw(self, layout):
        pass

bpy.utils.register_class(MaterialColor)


class MaterialType(bpy.types.PropertyGroup):
    description = bpy.props.StringProperty()
    type_code = bpy.props.IntProperty()
    colors = bpy.props.CollectionProperty(type=MaterialColor)

    def set_color_index(self, index):
        scene_props = bpy.context.scene.db_materials
        scene_props.mat_color_index = index

    def get_mat_color(self):
        scene_props = bpy.context.scene.db_materials
        return self.colors[scene_props.mat_color_index] 

    def get_inventory_material_name(self):
        return "{} {}".format(self.name, self.type_code)

    def draw(self, layout):
        color = self.get_mat_color()

        row = layout.row()
        split = row.split(percentage=0.25)
        split.label("Color:")            
        split.menu("MENU_Mat_Colors", text=color.name, icon='SOLO_ON' if color.has_render_mat else 'ERROR')

        if not color.has_render_mat:
            row = layout.row()
            split = row.split(percentage=0.25)
            split.label("")             
            box = split.box()
            row = box.row()
            row.label("Missing render material.", icon='ERROR') 

bpy.utils.register_class(MaterialType)


class Materials(bpy.types.PropertyGroup):
    mat_types = bpy.props.CollectionProperty(type=MaterialType)
    textured_mel_color_list = []
    mel_color_list = []

    def create_color_lists(self):
        self.textured_mel_color_list.clear()
        self.mel_color_list.clear()

        for mat_type in self.mat_types:
            if mat_type.name == 'Textured Melamine':
                for color in mat_type.colors:
                    self.textured_mel_color_list.append((color.name, color.name, color.name))
            if mat_type.name == 'Melamine':
                for color in mat_type.colors:
                    self.mel_color_list.append((color.name, color.name, color.name))

    def set_type_index(self, index):
        scene_props = bpy.context.scene.db_materials
        scene_props.mat_type_index = index
        scene_props.mat_color_index = 0

    def get_mat_type(self):
        scene_props = bpy.context.scene.db_materials
        return self.mat_types[scene_props.mat_type_index]

    def get_mat_color(self):
        return self.get_mat_type().get_mat_color()

    def has_render_mat(self):
        return self.get_mat_type().has_render_mat

    def draw(self, layout):
        box = layout.box()
        box.label("Material Selection:")

        if len(self.mat_types) > 0:
            row = box.row()
            split = row.split(percentage=0.25)
            split.label("Type:")
            split.menu('MENU_Mat_Types', text=self.get_mat_type().name, icon='SOLO_ON')
            self.get_mat_type().draw(box) 

        else:
            row = box.row()
            row.label("None", icon='ERROR')               

bpy.utils.register_class(Materials)


class CountertopColor(bpy.types.PropertyGroup, ColorMixIn):
    chip_code = bpy.props.StringProperty()
    vendor = bpy.props.StringProperty()

    def draw(layout):
        pass

bpy.utils.register_class(CountertopColor)


class CountertopManufactuer(bpy.types.PropertyGroup):
    description = bpy.props.StringProperty()
    color_code = bpy.props.IntProperty()
    colors = bpy.props.CollectionProperty(type=CountertopColor)

    def set_color_index(self, index):
        scene_props = bpy.context.scene.db_materials
        scene_props.ct_color_index = index

    def get_color(self):
        scene_props = bpy.context.scene.db_materials
        return self.colors[scene_props.ct_color_index]
        
    def draw(layout):
        pass

bpy.utils.register_class(CountertopManufactuer)


class CountertopType(bpy.types.PropertyGroup):
    type_code = bpy.props.IntProperty()
    description = bpy.props.StringProperty()
    manufactuers = bpy.props.CollectionProperty(type=CountertopManufactuer)
    colors = bpy.props.CollectionProperty(type=CountertopColor)

    def set_color_index(self, index):
        scene_props = bpy.context.scene.db_materials
        scene_props.ct_color_index = index

    def set_mfg_index(self, index):
        scene_props = bpy.context.scene.db_materials
        scene_props.ct_mfg_index = index
        scene_props.ct_color_index = 0     

    def get_mfg(self):
        scene_props = bpy.context.scene.db_materials
        return self.manufactuers[scene_props.ct_mfg_index]

    def get_color(self):
        scene_props = bpy.context.scene.db_materials

        if len(self.colors) > 0:
            return self.colors[scene_props.ct_color_index] 

        elif len(self.manufactuers) > 0:
            return self.get_mfg().get_color()

    def draw(self, layout):
        if len(self.colors) > 0:
            color = self.get_color()

            row = layout.row()
            split = row.split(percentage=0.25)
            split.label("Color:")            
            split.menu("MENU_Countertop_Colors", text=color.name, icon='SOLO_ON' if color.has_render_mat else 'ERROR')

            if not color.has_render_mat:
                row = layout.row()
                split = row.split(percentage=0.25)
                split.label("")             
                box = split.box()
                row = box.row()
                row.label("Missing render material.", icon='ERROR')         

        elif len(self.manufactuers) > 0:
            mfg = self.get_mfg()
            color = mfg.get_color()

            row = layout.row()
            split = row.split(percentage=0.25)
            split.label("Manufactuer:")             
            split.menu("MENU_Countertop_Mfgs", text=mfg.name, icon='SOLO_ON')

            row = layout.row()
            split = row.split(percentage=0.25)
            split.label("Color:")   
            split.menu("MENU_Countertop_Colors", text=mfg.get_color().name, icon='SOLO_ON' if color.has_render_mat else 'ERROR')

            if not color.has_render_mat:
                row = layout.row()
                split = row.split(percentage=0.25)
                split.label("")             
                box = split.box()
                row = box.row()
                row.label("Missing render material.", icon='ERROR') 

bpy.utils.register_class(CountertopType)


class CustomCountertops(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name="Name")
    vendor = bpy.props.StringProperty(name="Vendor")
    color_code = bpy.props.StringProperty(name="Color Code")
    price = bpy.props.FloatProperty(name="Price")

    def get_color(self):
        pass

    def draw(self, layout):
        layout.prop(self, 'name')
        layout.prop(self, 'vendor')
        layout.prop(self, 'color_code')
        layout.prop(self, 'price')

bpy.utils.register_class(CustomCountertops)


class Countertops(bpy.types.PropertyGroup):
    countertop_types = bpy.props.CollectionProperty(type=CountertopType) 
    custom_countertop = bpy.props.PointerProperty(type=CustomCountertops)

    def set_ct_type_index(self, index):
        scene_props = bpy.context.scene.db_materials
        scene_props.ct_type_index = index
        scene_props.ct_mfg_index = 0
        scene_props.ct_color_index = 0

    def get_type(self):
        scene_props = bpy.context.scene.db_materials
        return self.countertop_types[scene_props.ct_type_index]

    def get_color(self):
        return self.get_type().get_color()

    def get_color_name(self):
        if "Melamine" in self.get_type().name:
            materials = bpy.context.scene.db_materials.materials
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
        box.label("Countertop Selection:")

        if len(self.countertop_types) > 0:
            row = box.row()
            split = row.split(percentage=0.25)
            split.label("Type:")
            split.menu('MENU_Countertop_Types', text=self.get_type().name, icon='SOLO_ON')
            self.get_type().draw(box)

            if self.get_type().name == "Custom":
                self.custom_countertop.draw(box)

        else:
            row = box.row()
            row.label("None", icon='ERROR')            

bpy.utils.register_class(Countertops)


class StainColor(bpy.types.PropertyGroup):
    description = bpy.props.StringProperty()
    sku = bpy.props.StringProperty()

    def draw(layout):
        pass

bpy.utils.register_class(StainColor)

class GlazeColor(bpy.types.PropertyGroup):
    description = bpy.props.StringProperty()
    sku = bpy.props.StringProperty()

    def draw(layout):
        pass

bpy.utils.register_class(GlazeColor)

class GlazeStyle(bpy.types.PropertyGroup):
    description = bpy.props.StringProperty()
    sku = bpy.props.StringProperty()

    def draw(layout):
        pass

bpy.utils.register_class(GlazeStyle)


class DoorColor(bpy.types.PropertyGroup):
    description = bpy.props.StringProperty()
    sku = bpy.props.StringProperty()

    def draw(layout):
        pass

bpy.utils.register_class(DoorColor)


class GlassColor(bpy.types.PropertyGroup):
    description = bpy.props.StringProperty()
    sku = bpy.props.StringProperty()

    def draw(layout):
        pass

bpy.utils.register_class(GlassColor)


class DrawerSlideSize(bpy.types.PropertyGroup):
    slide_length_inch = bpy.props.FloatProperty()
    front_hole_dim_mm = bpy.props.IntProperty()
    back_hole_dim_mm = bpy.props.IntProperty()

bpy.utils.register_class(DrawerSlideSize)


class DrawerSlide(bpy.types.PropertyGroup):
    db_name = bpy.props.StringProperty()
    sizes = bpy.props.CollectionProperty(type=DrawerSlideSize)

bpy.utils.register_class(DrawerSlide)
