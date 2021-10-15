from snap import sn_types, sn_unit
from .appliance_paths import (
    BACKSPLASH_PART,
    CTOP
)

LIBRARY_NAME_SPACE = "sn_appliances"

# ---------PRODUCT: COUNTERTOPS


class Straight_Countertop(sn_types.Assembly):

    def __init__(self):
        self.library_name = "Countertops"
        self.category_name = "Countertops"
        self.assembly_name = "Straight Countertop"
        self.type_assembly = "PRODUCT"
        self.width = sn_unit.inch(30)
        self.height = sn_unit.inch(5.5)
        self.depth = sn_unit.inch(24)
        self.height_above_floor = sn_unit.inch(34.1)

    def draw(self):
        self.create_assembly()
        self.obj_bp['ID_PROMPT'] = "sn_closets.counter_top"

        # self.add_tab(name='Countertop Options', tab_type='VISIBLE')
        # self.add_tab(name='Material Thickness', tab_type='HIDDEN')
        self.add_prompt("Add Backsplash", 'CHECKBOX', True)
        self.add_prompt("Add Left Backsplash", 'CHECKBOX', False)
        self.add_prompt("Add Right Backsplash", 'CHECKBOX', False)
        self.add_prompt("Side Splash Setback", 'DISTANCE', sn_unit.inch(2.75))
        self.add_prompt("Deck Thickness", 'DISTANCE', sn_unit.inch(1.5))
        self.add_prompt("Splash Thickness", 'DISTANCE', sn_unit.inch(.75))

        # VARS
        Product_Width = self.obj_x.snap.get_var('location.x', 'Product_Width')
        Product_Height = self.obj_z.snap.get_var('location.z', 'Product_Height')
        Product_Depth = self.obj_y.snap.get_var('location.y', 'Product_Depth')
        Add_Backsplash = self.get_prompt('Add Backsplash').get_var()
        Add_Left_Backsplash = self.get_prompt('Add Left Backsplash').get_var()
        Add_Right_Backsplash = self.get_prompt('Add Right Backsplash').get_var()
        Side_Splash_Setback = self.get_prompt('Side Splash Setback').get_var()
        Deck_Thickness = self.get_prompt('Deck Thickness').get_var()
        Splash_Thickness = self.get_prompt('Splash Thickness').get_var()

        deck = sn_types.Part(self.add_assembly_from_file(CTOP))
        deck.set_name("Countertop Deck")
        deck.loc_x(value=0)
        deck.loc_y(value=0)
        deck.loc_z(value=0)
        deck.rot_x(value=0)
        deck.rot_y(value=0)
        deck.rot_z(value=0)
        deck.dim_x("Product_Width", [Product_Width])
        deck.dim_y("Product_Depth", [Product_Depth])
        deck.dim_z("Deck_Thickness", [Deck_Thickness])
        deck.material("Countertop_Surface")

        splash = sn_types.Part(self.add_assembly_from_file(BACKSPLASH_PART))
        splash.set_name("Backsplash")
        splash.loc_x(value=0)
        splash.loc_y(value=0)
        splash.loc_z('Deck_Thickness', [Deck_Thickness])
        splash.rot_x(value=90)
        splash.rot_y(value=0)
        splash.rot_z(value=0)
        splash.dim_x("Product_Width", [Product_Width])
        splash.dim_y("Product_Height-Deck_Thickness", [Product_Height, Deck_Thickness])
        splash.dim_z("Splash_Thickness", [Splash_Thickness])
        splash.add_prompt('Hide','CHECKBOX',False)
        splash_prompt = splash.get_prompt("Hide")
        splash_prompt.set_formula("IF(Add_Backsplash, False, True)", [Add_Backsplash])
        splash.material("Countertop_Surface")

        left_splash = sn_types.Part(self.add_assembly_from_file(BACKSPLASH_PART))

        left_splash.set_name("Left Backsplash")
        left_splash.loc_x(value=0)
        left_splash.loc_y("IF(Add_Backsplash, -Splash_Thickness, 0)", [Splash_Thickness, Add_Backsplash])
        left_splash.loc_z('Deck_Thickness', [Deck_Thickness])
        left_splash.rot_x(value=90)
        left_splash.rot_y(value=0)
        left_splash.rot_z(value=-90)
        left_splash.dim_x("fabs(Product_Depth)-Side_Splash_Setback-Splash_Thickness",
                          [Product_Depth, Side_Splash_Setback, Splash_Thickness])
        left_splash.dim_y("Product_Height-Deck_Thickness", [Product_Height, Deck_Thickness])
        left_splash.dim_z("-Splash_Thickness", [Splash_Thickness])
        left_splash.add_prompt('Hide','CHECKBOX',False)
        left_splash_prompt = left_splash.get_prompt("Hide")
        left_splash_prompt.set_formula("IF(Add_Left_Backsplash, False, True)", [Add_Left_Backsplash])
        left_splash.material("Countertop_Surface")

        right_splash = sn_types.Part(self.add_assembly_from_file(BACKSPLASH_PART))

        right_splash.set_name("Rear Backsplash")
        right_splash.loc_x("Product_Width", [Product_Width])
        right_splash.loc_y("IF(Add_Backsplash, -Splash_Thickness, 0)", [Splash_Thickness, Add_Backsplash])
        right_splash.loc_z('Deck_Thickness', [Deck_Thickness])
        right_splash.rot_x(value=90)
        right_splash.rot_z(value=0)
        right_splash.rot_z(value=-90)
        right_splash.dim_x("fabs(Product_Depth)-Side_Splash_Setback-Splash_Thickness",
                           [Product_Depth, Side_Splash_Setback, Splash_Thickness])
        right_splash.dim_y("Product_Height-Deck_Thickness", [Product_Height, Deck_Thickness])
        right_splash.dim_z("Splash_Thickness", [Splash_Thickness])
        right_splash.add_prompt('Hide','CHECKBOX',False)
        right_splash_prompt = right_splash.get_prompt("Hide")
        right_splash_prompt.set_formula("IF(Add_Right_Backsplash, False, True)", [Add_Right_Backsplash])
        right_splash.material("Countertop_Surface")

        self.update()
