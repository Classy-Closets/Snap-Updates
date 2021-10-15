import os
from snap import sn_types, sn_unit
from . import cabinet_countertops

LIBRARY_FOLDER_NAME = "Appliance - Sample"

from .appliance_paths import MATERIAL_FILE


def get_file_name(path):
    file_name = os.path.basename(path)
    return os.path.splitext(file_name)[0]


class Parametric_Wall_Appliance(sn_types.Assembly):
    category_name = "Appliances"
    show_in_library = True
    library_name = LIBRARY_FOLDER_NAME
    type_assembly = "PRODUCT"
    drop_id = "sn_appliances.place_appliance_object"

    """ Path to blend file that contains a group of the appliance """
    appliance_path = ""

    """ Set to True if you want to add a countertop to this appliance """
    add_countertop = False

    def draw(self):
        self.create_assembly()
        dim_x = self.obj_x.snap.get_var('location.x', 'dim_x')
        dim_z = self.obj_z.snap.get_var('location.z', 'dim_z')
        dim_y = self.obj_y.snap.get_var('location.y', 'dim_y')
        obj = self.add_assembly_from_file(self.appliance_path)
        part = sn_types.Part(obj_bp=obj)
        self.obj_x = part.obj_x
        self.obj_y = part.obj_y
        self.obj_z = part.obj_z
        self.obj_prompts = part.obj_prompts
        part.set_name(get_file_name(self.appliance_path))
        part.assign_material("Chrome", MATERIAL_FILE, "Chrome")
        part.assign_material("Stainless Steel", MATERIAL_FILE, "Stainless Steel")
        part.assign_material("Black Anodized Metal", MATERIAL_FILE, "Black Anodized Metal")

        if self.add_countertop:
            # self.add_tab(name="Counter Top Options", tab_type='VISIBLE')
            self.add_prompt("Countertop Overhang Front", 'DISTANCE', sn_unit.inch(1))
            self.add_prompt("Countertop Overhang Back", 'DISTANCE', sn_unit.inch(0))
            self.add_prompt("Countertop Overhang Left", 'DISTANCE', sn_unit.inch(0))
            self.add_prompt("Countertop Overhang Right", 'DISTANCE', sn_unit.inch(0))
            Countertop_Overhang_Front = self.get_prompt('Countertop Overhang Front').get_var()
            Countertop_Overhang_Left = self.get_prompt('Countertop Overhang Left').get_var()
            Countertop_Overhang_Right = self.get_prompt('Countertop Overhang Right').get_var()
            Countertop_Overhang_Back = self.get_prompt('Countertop Overhang Back').get_var()

            ctop = cabinet_countertops.Straight_Countertop()
            ctop.draw()
            ctop.obj_bp.snap.type_group = 'INSERT'
            ctop.obj_bp.parent = self.obj_bp
            ctop.loc_x('-Countertop_Overhang_Left', [Countertop_Overhang_Left])
            ctop.loc_y('Countertop_Overhang_Back', [Countertop_Overhang_Back])
            ctop.loc_z('dim_z', [dim_z])
            ctop.rot_x(value=0)
            ctop.rot_y(value=0)
            ctop.rot_z(value=0)
            ctop.dim_x('dim_x+Countertop_Overhang_Left+Countertop_Overhang_Right',
                       [dim_x, Countertop_Overhang_Left, Countertop_Overhang_Right])
            ctop.dim_y('dim_y-Countertop_Overhang_Front-Countertop_Overhang_Back',
                       [dim_y, Countertop_Overhang_Front, Countertop_Overhang_Back])
            ctop.dim_z(value=sn_unit.inch(4))


class Static_Wall_Appliance(sn_types.Assembly):
    category_name = "Appliances"
    show_in_library = True
    library_name = LIBRARY_FOLDER_NAME
    type_assembly = "PRODUCT"
    drop_id = "sn_appliances.place_appliance_object"

    """ Path to blend file that contains a group of the appliance """
    appliance_path = ""

    """ Set to True if you want to add a countertop to this appliance """
    add_countertop = False

    def draw(self):
        self.create_assembly()
        obj = self.add_assembly_from_file(self.appliance_path)
        part = sn_types.Part(obj)
        part.set_name(get_file_name(self.appliance_path))
        self.width = part.obj_x.location.x
        self.height = part.obj_z.location.z
        self.depth = part.obj_y.location.y
        part.assign_material("Chrome", MATERIAL_FILE, "Chrome")
        part.assign_material("Stainless Steel", MATERIAL_FILE, "Stainless Steel")
        part.assign_material("Black Anodized Metal", MATERIAL_FILE, "Black Anodized Metal")

        dim_x = self.obj_x.snap.get_var('location.x', 'dim_x')
        dim_y = self.obj_y.snap.get_var('location.y', 'dim_y')
        dim_z = self.obj_z.snap.get_var('location.z', 'dim_z')

        if self.add_countertop:
            # self.add_tab(name="Counter Top Options", tab_type='VISIBLE')
            self.add_prompt("Countertop Overhang Front", 'DISTANCE', sn_unit.inch(1))
            self.add_prompt("Countertop Overhang Back", 'DISTANCE', sn_unit.inch(0))
            self.add_prompt("Countertop Overhang Left", 'DISTANCE', sn_unit.inch(0))
            self.add_prompt("Countertop Overhang Right", 'DISTANCE', sn_unit.inch(0))
            Countertop_Overhang_Front = self.get_prompt('Countertop Overhang Front').get_var()
            Countertop_Overhang_Left = self.get_prompt('Countertop Overhang Left').get_var()
            Countertop_Overhang_Right = self.get_prompt('Countertop Overhang Right').get_var()
            Countertop_Overhang_Back = self.get_prompt('Countertop Overhang Back').get_var()

            ctop = cabinet_countertops.PRODUCT_Straight_Countertop()
            ctop.draw()
            ctop.obj_bp.snap.type_group = 'INSERT'
            ctop.obj_bp.parent = self.obj_bp
            ctop.loc_x('-Countertop_Overhang_Left', [Countertop_Overhang_Left])
            ctop.loc_y('Countertop_Overhang_Back', [Countertop_Overhang_Back])
            ctop.loc_z('dim_z', [dim_z])
            ctop.rot_x(value=0)
            ctop.rot_y(value=0)
            ctop.rot_z(value=0)
            ctop.dim_x('dim_x+Countertop_Overhang_Left+Countertop_Overhang_Right',
                       [dim_x, Countertop_Overhang_Left, Countertop_Overhang_Right])
            ctop.dim_y('dim_y-Countertop_Overhang_Front-Countertop_Overhang_Back',
                       [dim_y, Countertop_Overhang_Front, Countertop_Overhang_Back])
            ctop.dim_z(value=sn_unit.inch(4))


class Countertop_Appliance(sn_types.Assembly):
    category_name = "Appliances"
    show_in_library = True
    library_name = LIBRARY_FOLDER_NAME
    type_assembly = "NONE"

    """ Path to blend file that contains a group of the appliance """
    appliance_path = ""
    drop_id = "sn_appliances.place_countertop_appliance"

    def draw(self):
        self.create_assembly()
        obj= self.add_assembly_from_file(self.appliance_path)
        part = sn_types.Part(obj_bp=obj)
        part.set_name(get_file_name(self.appliance_path))
        self.obj_x = part.obj_x
        self.obj_y = part.obj_y
        self.obj_z = part.obj_z
        self.obj_prompts = part.obj_prompts
        self.width = part.obj_x.location.x
        self.height = part.obj_z.location.z
        self.depth = part.obj_y.location.y
        part.assign_material("Chrome", MATERIAL_FILE, "Chrome")
        part.assign_material("Stainless Steel", MATERIAL_FILE, "Stainless Steel")
        part.assign_material("Black Anodized Metal", MATERIAL_FILE, "Black Anodized Metal")


class Object_Appliance(sn_types.Assembly):
    category_name = "Appliances"
    show_in_library = True
    library_name = LIBRARY_FOLDER_NAME
    type_assembly = "NONE"
    drop_id = "sn_appliances.place_appliance_object"

    """ Path to blend file that contains a group of the appliance """
    appliance_path = ""

    def draw(self):
        self.create_assembly()
        ass_obj = self.add_object_from_file(self.appliance_path)
        self.set_name(get_file_name(self.appliance_path))
        self.obj_x.empty_display_size = sn_unit.inch(1)
        self.obj_y.empty_display_size = sn_unit.inch(1)
        self.obj_z.empty_display_size = sn_unit.inch(1)
