from snap import sn_unit
from .common import common_parts
from . import closet_props
from .data import data_closet_carcass
from .data import data_closet_carcass_island
from .data import data_single_parts
from .data import data_rods_and_shelves
from .data import data_countertop
from .data import data_drawers
from .data import data_closet_doors
from .data import data_hampers
from .data import data_closet_carcass_corner
from .data import data_base_assembly
# from .data import data_shoe_cubbies
from .data import data_closet_hooks_and_pins
from .data import data_closet_top
from .data import data_closet_splitters
from .data import data_closet_flat_molding
from .data import data_closet_wall_cleat
from .data import data_closet_bottom_capping
from .data import data_garage_leg
import bpy


# from . import data_closet_carcass_hutch
# from . import data_ironing_boards
# from . import data_deco_fillers
# from . import data_applied_panel
# from . import data_tie_drawer
# from . import data_closet_peninsula
# from . import data_closet_bench
# from . import data_hanging_rod
# from . import data_fixed_shelf_and_rod
# from . import data_classy_closets_hanging_rods

LIBRARY_NAME = "Closets"

# CLOSET_PRODUCTS_FLOOR = "Closet Products - Floor Panels"
CLOSET_PRODUCTS_PARTIONS = "Closet Products – Partitions"
CLOSET_PRODUCTS_BASIC = "Closet Products - Basic"
CLOSET_PRODUCTS_DRAWERS = "Closet Products - Drawers"
CLOSET_PRODUCTS_SHELVES = "Closet Products - Shelves"
CLOSET_PRODUCTS_HUTCH = "Closet Products - Hutch"
CLOSET_PRODUCTS_ISLANDS = "Closet Products - Islands"
CLOSET_PRODUCTS_STACKED = "Closet Products - Uppers"
CLOSET_PARTS_ACCESSORIES = "Parts - Closet Accessories"
SECTION_INSERTS_DIVIDERS = "Section Inserts - Dividers"
CLOSET_PRODUCTS_GARAGE = "Closet Prodcuts - Garage"


# --------CLOSET PRODUCTS HANGING
class PRODUCT_1_Section(data_closet_carcass.Closet_Carcass):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_PARTIONS
        self.opening_qty = 1
        self.is_hanging = True
        super().__init__()


class PRODUCT_2_Sections(data_closet_carcass.Closet_Carcass):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_PARTIONS
        self.opening_qty = 2
        self.is_hanging = True
        super().__init__()


class PRODUCT_3_Sections(data_closet_carcass.Closet_Carcass):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_PARTIONS
        self.opening_qty = 3
        self.is_hanging = True
        super().__init__()


class PRODUCT_4_Sections(data_closet_carcass.Closet_Carcass):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_PARTIONS
        self.opening_qty = 4
        self.is_hanging = True
        super().__init__()


class PRODUCT_5_Sections(data_closet_carcass.Closet_Carcass):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_PARTIONS
        self.opening_qty = 5
        self.is_hanging = True
        super().__init__()


class PRODUCT_6_Sections(data_closet_carcass.Closet_Carcass):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_PARTIONS
        self.opening_qty = 6
        self.is_hanging = True
        super().__init__()


class PRODUCT_7_Sections(data_closet_carcass.Closet_Carcass):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_PARTIONS
        self.opening_qty = 7
        self.is_hanging = True
        super().__init__()


class PRODUCT_8_Sections(data_closet_carcass.Closet_Carcass):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_PARTIONS
        self.opening_qty = 8
        self.is_hanging = True
        super().__init__()


class PRODUCT_9_Sections(data_closet_carcass.Closet_Carcass):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_PARTIONS
        self.opening_qty = 9
        self.is_hanging = True
        super().__init__()


# --------CLOSET PRODUCTS BASIC

class PRODUCT_Toe_Kick(data_base_assembly.Base_Assembly):

    def __init__(self):
        props = bpy.context.scene.sn_closets
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = sn_unit.inch(18)
        self.height = props.closet_defaults.toe_kick_height
        self.depth = sn_unit.inch(12)


class PRODUCT_Counter_Top(data_countertop.Countertop_Insert):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.drop_id = "sn_closets.place_countertop"
        # self.assembly_type = "PRODUCT"
        self.width = sn_unit.inch(18)
        self.depth = sn_unit.inch(23)


class INSERT_Doors(data_closet_doors.Doors):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = sn_unit.inch(25)
        self.height = sn_unit.inch(50)
        self.depth = sn_unit.inch(14)
        self.prompts = {"Door Type": 2}
        # DOOR TYPE ONLY USED TO DETERMINE DOOR HEIGHT FOR PLANT ON TOP
        self.door_type = "Upper"


class INSERT_Hamper(data_hampers.Hamper):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = sn_unit.inch(20)
        self.height = sn_unit.inch(34)
        self.depth = sn_unit.inch(16)


class PRODUCT_Double_Hang(data_rods_and_shelves.Hanging_Rods_with_Shelves):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = sn_unit.inch(18)
        self.height = sn_unit.inch(50)
        self.depth = sn_unit.inch(14)
        self.prompts = {"Add Top Rod": True,
                        "Add Middle Rod": False,
                        "Add Bottom Rod": True,
                        "Add Top Shelf": False,
                        "Add Bottom Shelf": True,
                        "Top Rod Location": sn_unit.millimeter(172.95),
                        "Bottom Rod Location": sn_unit.millimeter(1164.95),
                        "Bottom Shelves Location": sn_unit.millimeter(1164.95),
                        "Add Shelves In Top Section": False,
                        "Add Shelves In Middle Section": False,
                        "Add Shelves In Bottom Section": False,
                        "Top Shelf Quantity": 1,
                        "Middle Shelf Quantity": 1,
                        "Bottom Shelf Quantity": 1,
                        "Is Hang Single": False,
                        "Is Hang Double": True}


class PRODUCT_Double_Hang_Tall(data_rods_and_shelves.Hanging_Rods_with_Shelves):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = sn_unit.inch(18)
        self.height = sn_unit.inch(50)
        self.depth = sn_unit.inch(14)
        self.prompts = {"Add Top Rod": False,
                        "Add Middle Rod": True,
                        "Add Bottom Rod": True,
                        "Add Top Shelf": True,
                        "Add Bottom Shelf": True,
                        "Top Rod Location": sn_unit.millimeter(300.95),
                        "Bottom Rod Location": sn_unit.millimeter(1388.95),
                        "Bottom Shelves Location": sn_unit.millimeter(1388.95),
                        "Add Shelves In Top Section": False,
                        "Add Shelves In Middle Section": False,
                        "Add Shelves In Bottom Section": False,
                        "Top Shelf Quantity": 1,
                        "Middle Shelf Quantity": 1,
                        "Bottom Shelf Quantity": 1,
                        "Is Hang Single": False,
                        "Is Hang Double": True}


class PRODUCT_Medium_Hang(data_rods_and_shelves.Hanging_Rods_with_Shelves):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = sn_unit.inch(18)
        self.height = sn_unit.inch(50)
        self.depth = sn_unit.inch(14)
        self.prompts = {"Add Top Rod": False,
                        "Add Middle Rod": True,
                        "Add Bottom Rod": False,
                        "Add Top Shelf": True,
                        "Add Bottom Shelf": False,
                        "Top Rod Location": sn_unit.millimeter(748.95),
                        "Bottom Rod Location": sn_unit.millimeter(1164.95),
                        "Bottom Shelves Location": sn_unit.millimeter(1164.95),
                        "Add Shelves In Top Section": True,
                        "Add Shelves In Middle Section": False,
                        "Add Shelves In Bottom Section": False,
                        "Top Shelf Quantity": 2,
                        "Middle Shelf Quantity": 1,
                        "Bottom Shelf Quantity": 1,
                        "Is Hang Single": False,
                        "Is Hang Double": False}


class PRODUCT_Long_Hang(data_rods_and_shelves.Hanging_Rods_with_Shelves):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = sn_unit.inch(18)
        self.height = sn_unit.inch(50)
        self.depth = sn_unit.inch(14)
        self.prompts = {"Add Top Rod": False,
                        "Add Middle Rod": True,
                        "Add Bottom Rod": False,
                        "Add Top Shelf": True,
                        "Add Bottom Shelf": False,
                        "Top Rod Location": sn_unit.millimeter(300.95),
                        "Bottom Rod Location": sn_unit.millimeter(1164.95),
                        "Bottom Shelves Location": sn_unit.millimeter(1164.95),
                        "Add Shelves In Top Section": False,
                        "Add Shelves In Middle Section": False,
                        "Add Shelves In Bottom Section": False,
                        "Top Shelf Quantity": 1,
                        "Middle Shelf Quantity": 1,
                        "Bottom Shelf Quantity": 1,
                        "Is Hang Single": False,
                        "Is Hang Double": False}


class PRODUCT_Short_Hang(data_rods_and_shelves.Hanging_Rods_with_Shelves):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = sn_unit.inch(18)
        self.height = sn_unit.inch(50)
        self.depth = sn_unit.inch(14)
        self.prompts = {"Add Top Rod": False,
                        "Add Middle Rod": False,
                        "Add Bottom Rod": True,
                        "Add Top Shelf": False,
                        "Add Bottom Shelf": True,
                        "Top Rod Location": sn_unit.millimeter(172.95),
                        "Bottom Rod Location": sn_unit.millimeter(1164.95),
                        "Bottom Shelves Location": sn_unit.millimeter(1164.95),
                        "Add Shelves In Top Section": False,
                        "Add Shelves In Middle Section": True,
                        "Add Shelves In Bottom Section": False,
                        "Top Shelf Quantity": 1,
                        "Middle Shelf Quantity": 4,
                        "Bottom Shelf Quantity": 1,
                        "Is Hang Single": True,
                        "Is Hang Double": False}


class PRODUCT_Short_Hang_Tall(data_rods_and_shelves.Hanging_Rods_with_Shelves):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = sn_unit.inch(18)
        self.height = sn_unit.inch(50)
        self.depth = sn_unit.inch(14)
        self.prompts = {"Add Top Rod": False,
                        "Add Middle Rod": False,
                        "Add Bottom Rod": True,
                        "Add Top Shelf": False,
                        "Add Bottom Shelf": True,
                        "Top Rod Location": sn_unit.millimeter(172.95),
                        "Bottom Rod Location": sn_unit.millimeter(1388.95),
                        "Bottom Shelves Location": sn_unit.millimeter(1388.95),
                        "Add Shelves In Top Section": False,
                        "Add Shelves In Middle Section": True,
                        "Add Shelves In Bottom Section": False,
                        "Top Shelf Quantity": 1,
                        "Middle Shelf Quantity": 6,
                        "Bottom Shelf Quantity": 1,
                        "Is Hang Single": True,
                        "Is Hang Double": False}


class PRODUCT_Corner_Shelves(data_closet_carcass_corner.Corner_Shelves):

    def __init__(self):
        props = bpy.context.scene.sn_closets
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        # self.drop_id = "sn_closets.place_corner_l_shelves"
        self.width = sn_unit.inch(24.75)
        self.height = sn_unit.millimeter(2003)
        self.depth = sn_unit.inch(24.75)
        self.prompts = {"Is Hanging": False}
        super().__init__()


class PRODUCT_L_Shelves(data_closet_carcass_corner.L_Shelves):

    def __init__(self):
        props = bpy.context.scene.sn_closets
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        # self.drop_id = "sn_closets.place_corner_l_shelves"
        self.width = sn_unit.inch(24.75)
        self.height = sn_unit.millimeter(2003)
        self.depth = sn_unit.inch(24.75)
        self.prompts = {"Is Hanging": False}
        super().__init__()


# class PRODUCT_Triangle_Shelves(data_closet_carcass_corner.Corner_Triangle_Shelves):

#     def __init__(self):
#         props = bpy.context.scene.sn_closets
#         self.library_name = LIBRARY_NAME
#         self.category_name = CLOSET_PRODUCTS_BASIC
#         self.width = props.closet_defaults.panel_depth
#         self.height = sn_unit.millimeter(
#             float(props.closet_defaults.panel_height))
#         self.depth = props.closet_defaults.panel_depth


class PRODUCT_Slanted_Shoe_Shelf(data_single_parts.Slanted_Shoe_Shelves):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.assembly_type = "PRODUCT"
        self.width = sn_unit.inch(18)
        self.depth = sn_unit.inch(23)


class PRODUCT_Top_Shelf(data_closet_top.Top):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = sn_unit.inch(34)
        self.height = sn_unit.inch(34)
        self.depth = sn_unit.inch(12)


class PRODUCT_Capping_Bottom(data_closet_bottom_capping.Bottom_Capping):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = sn_unit.inch(34)
        self.height = sn_unit.inch(34)
        self.depth = sn_unit.inch(12)


class PRODUCT_Flat_Crown(data_closet_flat_molding.Flat_Crown):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = sn_unit.inch(34)
        self.height = sn_unit.inch(4)
        self.depth = sn_unit.inch(.75)
        self.prompts = {"Extend To Left Panel": True,
                        "Extend To Right Panel": True,
                        "Exposed Left": False,
                        "Exposed Right": False,
                        "Exposed Back": False,
                        "Return Left": False,
                        "Return Right": False,
                        "Extend Left Amount": 0,
                        "Extend Right Amount": 0,
                        "Front Overhang": 0,
                        "Molding Height": sn_unit.inch(3),
                        "Molding Location": 0}        


class PRODUCT_Light_Rail(data_closet_flat_molding.Flat_Molding):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = sn_unit.inch(34)
        self.height = sn_unit.inch(4)
        self.depth = sn_unit.inch(.75)
        self.prompts = {"Extend To Left Panel": True,
                        "Extend To Right Panel": True,
                        "Exposed Left": True,
                        "Exposed Right": True,
                        "Exposed Back": True,
                        "Return Left": False,
                        "Return Right": False,
                        "Extend Left Amount": 0,
                        "Extend Right Amount": 0,
                        "Front Overhang": sn_unit.inch(0.75),
                        "Molding Height": sn_unit.inch(3),
                        "Molding Location": sn_unit.inch(-24)}


class PRODUCT_Valance(data_closet_flat_molding.Flat_Molding):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = sn_unit.inch(34)
        self.height = sn_unit.inch(4)
        self.depth = sn_unit.inch(.75)
        self.prompts = {"Extend To Left Panel": True,
                        "Extend To Right Panel": True,
                        "Exposed Left": False,
                        "Exposed Right": False,
                        "Exposed Back": True,
                        "Return Left": False,
                        "Return Right": False,
                        "Extend Left Amount": sn_unit.inch(-0.75),
                        "Extend Right Amount": sn_unit.inch(-0.75),
                        "Front Overhang": 0,
                        "Molding Height": sn_unit.inch(3),
                        "Molding Location": sn_unit.inch(-24)}       


class PRODUCT_Wall_Cleat(data_closet_wall_cleat.Wall_Cleat):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_BASIC
        self.width = sn_unit.inch(18)
        self.height = sn_unit.inch(0.75)
        self.depth = sn_unit.inch(3.64)


# --------CLOSET PRODUCTS DRAWERS


class INSERT_1_Drawer(data_drawers.Drawer_Stack):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_DRAWERS
        self.width = sn_unit.inch(18)
        self.height = sn_unit.inch(50)
        self.depth = sn_unit.inch(14)
        self.number_of_drawers = 2


class INSERT_2_Drawers(data_drawers.Drawer_Stack):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_DRAWERS
        self.width = sn_unit.inch(18)
        self.height = sn_unit.inch(50)
        self.depth = sn_unit.inch(14)
        self.number_of_drawers = 3


class INSERT_3_Drawers(data_drawers.Drawer_Stack):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_DRAWERS
        self.width = sn_unit.inch(18)
        self.height = sn_unit.inch(50)
        self.depth = sn_unit.inch(14)
        self.number_of_drawers = 4


class INSERT_4_Drawers(data_drawers.Drawer_Stack):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_DRAWERS
        self.width = sn_unit.inch(18)
        self.height = sn_unit.inch(50)
        self.depth = sn_unit.inch(14)
        self.number_of_drawers = 5


class INSERT_5_Drawers(data_drawers.Drawer_Stack):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_DRAWERS
        self.width = sn_unit.inch(18)
        self.height = sn_unit.inch(50)
        self.depth = sn_unit.inch(14)
        self.number_of_drawers = 6


class INSERT_6_Drawers(data_drawers.Drawer_Stack):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_DRAWERS
        self.width = sn_unit.inch(18)
        self.height = sn_unit.inch(50)
        self.depth = sn_unit.inch(14)
        self.number_of_drawers = 7


class INSERT_7_Drawers(data_drawers.Drawer_Stack):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_DRAWERS
        self.width = sn_unit.inch(18)
        self.height = sn_unit.inch(50)
        self.depth = sn_unit.inch(14)
        self.number_of_drawers = 8


class INSERT_8_Drawers(data_drawers.Drawer_Stack):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_DRAWERS
        self.width = sn_unit.inch(18)
        self.height = sn_unit.inch(50)
        self.depth = sn_unit.inch(14)
        self.number_of_drawers = 9


# --------CLOSET INSERTS SHELVES

class PRODUCT_Shelves_Glass(data_rods_and_shelves.Glass_Shelves):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_SHELVES
        self.width = sn_unit.inch(18)
        self.height = sn_unit.inch(50)
        self.depth = sn_unit.inch(14)
        self.drop_id = "sn_closets.drop_insert"


class PRODUCT_Shelf_Stack(data_closet_splitters.Vertical_Splitters):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_SHELVES
        self.width = sn_unit.inch(34)
        self.height = sn_unit.inch(34)
        self.depth = sn_unit.inch(12)
        #self.drop_id = "sn_closets.insert_vertical_splitters_drop"


# class PRODUCT_Shelf_2(data_closet_splitters.Vertical_Splitters):

#     def __init__(self):
#         self.library_name = LIBRARY_NAME
#         self.category_name = CLOSET_PRODUCTS_SHELVES
#         self.width = sn_unit.inch(34)
#         self.height = sn_unit.inch(34)
#         self.depth = sn_unit.inch(12)
#         self.vertical_openings = 3
#         self.drop_id = "sn_closets.drop_insert"


# class PRODUCT_Shelf_3(data_closet_splitters.Vertical_Splitters):

#     def __init__(self):
#         self.library_name = LIBRARY_NAME
#         self.category_name = CLOSET_PRODUCTS_SHELVES
#         self.width = sn_unit.inch(34)
#         self.height = sn_unit.inch(34)
#         self.depth = sn_unit.inch(12)
#         self.vertical_openings = 4
#         self.drop_id = "sn_closets.drop_insert"


# class PRODUCT_Shelf_4(data_closet_splitters.Vertical_Splitters):

#     def __init__(self):
#         self.library_name = LIBRARY_NAME
#         self.category_name = CLOSET_PRODUCTS_SHELVES
#         self.width = sn_unit.inch(34)
#         self.height = sn_unit.inch(34)
#         self.depth = sn_unit.inch(12)
#         self.vertical_openings = 5
#         self.drop_id = "sn_closets.drop_insert"


# class PRODUCT_Shelf_5(data_closet_splitters.Vertical_Splitters):

#     def __init__(self):
#         self.library_name = LIBRARY_NAME
#         self.category_name = CLOSET_PRODUCTS_SHELVES
#         self.width = sn_unit.inch(34)
#         self.height = sn_unit.inch(34)
#         self.depth = sn_unit.inch(12)
#         self.vertical_openings = 6
#         self.drop_id = "sn_closets.drop_insert"


# class PRODUCT_Shelf_6(data_closet_splitters.Vertical_Splitters):

#     def __init__(self):
#         self.library_name = LIBRARY_NAME
#         self.category_name = CLOSET_PRODUCTS_SHELVES
#         self.width = sn_unit.inch(34)
#         self.height = sn_unit.inch(34)
#         self.depth = sn_unit.inch(12)
#         self.vertical_openings = 7
#         self.drop_id = "sn_closets.drop_insert"


# class PRODUCT_Shelf_7(data_closet_splitters.Vertical_Splitters):

#     def __init__(self):
#         self.library_name = LIBRARY_NAME
#         self.category_name = CLOSET_PRODUCTS_SHELVES
#         self.width = sn_unit.inch(34)
#         self.height = sn_unit.inch(34)
#         self.depth = sn_unit.inch(12)
#         self.vertical_openings = 8
#         self.drop_id = "sn_closets.drop_insert"


# class PRODUCT_Shelf_8(data_closet_splitters.Vertical_Splitters):

#     def __init__(self):
#         self.library_name = LIBRARY_NAME
#         self.category_name = CLOSET_PRODUCTS_SHELVES
#         self.width = sn_unit.inch(34)
#         self.height = sn_unit.inch(34)
#         self.depth = sn_unit.inch(12)
#         self.vertical_openings = 9
#         self.drop_id = "sn_closets.drop_insert"


# class PRODUCT_Shelf_9(data_closet_splitters.Vertical_Splitters):

#     def __init__(self):
#         self.library_name = LIBRARY_NAME
#         self.category_name = CLOSET_PRODUCTS_SHELVES
#         self.width = sn_unit.inch(34)
#         self.height = sn_unit.inch(34)
#         self.depth = sn_unit.inch(12)
#         self.vertical_openings = 10
#         self.drop_id = "sn_closets.drop_insert"

# --------CLOSET PRODUCTS HUTCH

# class PRODUCT_1_Hutch_Opening(data_closet_carcass_hutch.Hutch):

    # def __init__(self):
    #     self.library_name = LIBRARY_NAME
    #     self.category_name = CLOSET_PRODUCTS_HUTCH
    #     self.opening_qty = 1
    #     super().__init__()


# class PRODUCT_2_Hutch_Opening(data_closet_carcass_hutch.Hutch):

    # def __init__(self):
    #     self.library_name = LIBRARY_NAME
    #     self.category_name = CLOSET_PRODUCTS_HUTCH
    #     self.opening_qty = 2
    #     super().__init__()


# class PRODUCT_3_Hutch_Opening(data_closet_carcass_hutch.Hutch):

    # def __init__(self):
    #     self.library_name = LIBRARY_NAME
    #     self.category_name = CLOSET_PRODUCTS_HUTCH
    #     self.opening_qty = 3
    #     super().__init__()


# class PRODUCT_4_Hutch_Opening(data_closet_carcass_hutch.Hutch):

    # def __init__(self):
    #     self.library_name = LIBRARY_NAME
    #     self.category_name = CLOSET_PRODUCTS_HUTCH
    #     self.opening_qty = 4
    #     super().__init__()


# class PRODUCT_5_Hutch_Opening(data_closet_carcass_hutch.Hutch):

    # def __init__(self):
    #     self.library_name = LIBRARY_NAME
    #     self.category_name = CLOSET_PRODUCTS_HUTCH
    #     self.opening_qty = 5
    #     super().__init__()


# class PRODUCT_6_Hutch_Opening(data_closet_carcass_hutch.Hutch):

    # def __init__(self):
    #     self.library_name = LIBRARY_NAME
    #     self.category_name = CLOSET_PRODUCTS_HUTCH
    #     self.opening_qty = 6
    #     super().__init__()


# ---------PARTS - CLOSET ACCESSORIES

class PRODUCT_Belt_Rack(data_closet_hooks_and_pins.Belt_Accessories):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES
        self.width = sn_unit.inch(12)
        self.depth = sn_unit.inch(1)
        self.height = sn_unit.inch(3)


class PRODUCT_Tie_Rack(data_closet_hooks_and_pins.Tie_Accessories):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES
        self.width = sn_unit.inch(12)
        self.depth = sn_unit.inch(1)
        self.height = sn_unit.inch(3)


class PRODUCT_Robe_Hooks(data_closet_hooks_and_pins.Robe_Hook_Accessories):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES
        self.width = sn_unit.inch(4)
        self.depth = sn_unit.inch(1)
        self.height = sn_unit.inch(3)


class PRODUCT_Wire_Basket(data_single_parts.Wire_Basket):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES
        self.assembly_type = "PRODUCT"
        self.width = sn_unit.inch(18)
        self.depth = sn_unit.inch(23)


class PRODUCT_Valet_Rod(data_single_parts.Valet_Rod):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES
        self.assembly_type = "PRODUCT"
        self.object_path = common_parts.VALET_ROD
        self.accessory_name = "Valet Rod"
        # self.id_prompt = ""


# class PRODUCT_Valet_Rod_2(data_single_parts.Accessory):

#     def __init__(self):
#         self.library_name = LIBRARY_NAME
#         self.category_name = CLOSET_PARTS_ACCESSORIES
#         self.assembly_type = "PRODUCT"
#         self.object_path = common_parts.VALET_ROD_2
#         self.accessory_name = "Valet Rod 2"
#         self.id_prompt = ""


# class PRODUCT_Tie_and_Belt_Rack(data_closet_hooks_and_pins.Tie_and_Belt_Accessories):

#     def __init__(self):
#         self.library_name = LIBRARY_NAME
#         self.category_name = CLOSET_PARTS_ACCESSORIES
#         self.width = sn_unit.inch(12)
#         self.depth = sn_unit.inch(1)
#         self.height = sn_unit.inch(3)


class PRODUCT_Double_Robe_Hooks(data_closet_hooks_and_pins.Double_Robe_Hook_Accessories):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES
        self.width = sn_unit.inch(4)
        self.depth = sn_unit.inch(1)
        self.height = sn_unit.inch(3)


class PRODUCT_DORB_Hooks(data_closet_hooks_and_pins.DORB_Hook_Accessories):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES
        self.width = sn_unit.inch(4)
        self.depth = sn_unit.inch(1)
        self.height = sn_unit.inch(3)


class PRODUCT_Coat_and_Hat_Hooks(data_closet_hooks_and_pins.Coat_and_Hat_Hook_Accessories):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES
        self.width = sn_unit.inch(4)
        self.depth = sn_unit.inch(1)
        self.height = sn_unit.inch(3)


class PRODUCT_Hanging_Rod(data_single_parts.Hanging_Rod):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES
        self.assembly_type = "PRODUCT"
        self.width = sn_unit.inch(18)
        self.depth = sn_unit.inch(23)


class PRODUCT_Pants_Rack(data_single_parts.Pants_Rack):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES
        self.assembly_type = "INSERT"
        self.width = sn_unit.inch(18)
        self.depth = sn_unit.inch(23)


class PRODUCT_Hamper_Single_Pullout_Canvas(data_single_parts.Single_Pull_Out_Hamper):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES
        self.assembly_type = "INSERT"
        self.width = sn_unit.inch(18)
        self.depth = sn_unit.inch(23)


class PRODUCT_Hamper_Double_Pullout_Canvas(data_single_parts.Double_Pull_Out_Hamper):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PARTS_ACCESSORIES
        self.assembly_type = "INSERT"
        self.width = sn_unit.inch(24)
        self.depth = sn_unit.inch(23)


# class PRODUCT_Metal_Tie_and_Belt_Rack(data_single_parts.Accessory):

#     def __init__(self):
#         self.library_name = LIBRARY_NAME
#         self.category_name = CLOSET_PARTS_ACCESSORIES
#         self.assembly_type = "PRODUCT"
#         self.id_prompt = ""
#         self.object_path = common_parts.TIE_AND_BELT_RACK
#         self.accessory_name = "Metal Tie and Belt Rack"


# --------ISLAND CLOSETS

class PRODUCT_1_Island_Opening(data_closet_carcass_island.Closet_Island_Carcass):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ISLANDS
        self.opening_qty = 1
        self.is_double_sided = False
        super().__init__()


class PRODUCT_2_Island_Opening(data_closet_carcass_island.Closet_Island_Carcass):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ISLANDS
        self.opening_qty = 2
        self.is_double_sided = False
        super().__init__()


class PRODUCT_3_Island_Opening(data_closet_carcass_island.Closet_Island_Carcass):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ISLANDS
        self.opening_qty = 3
        self.is_double_sided = False
        super().__init__()


class PRODUCT_4_Island_Opening(data_closet_carcass_island.Closet_Island_Carcass):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ISLANDS
        self.opening_qty = 4
        self.is_double_sided = False
        super().__init__()


class PRODUCT_1_Dbl_Island_Opening(data_closet_carcass_island.Closet_Island_Carcass):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ISLANDS
        self.opening_qty = 1
        self.is_double_sided = True
        super().__init__()


class PRODUCT_2_Dbl_Island_Opening(data_closet_carcass_island.Closet_Island_Carcass):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ISLANDS
        self.opening_qty = 2
        self.is_double_sided = True
        super().__init__()


class PRODUCT_3_Dbl_Island_Opening(data_closet_carcass_island.Closet_Island_Carcass):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ISLANDS
        self.opening_qty = 3
        self.is_double_sided = True
        super().__init__()


class PRODUCT_4_Dbl_Island_Opening(data_closet_carcass_island.Closet_Island_Carcass):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_ISLANDS
        self.opening_qty = 4
        self.is_double_sided = True
        super().__init__()

# --------Section Inserts - Dividers


class PRODUCT_Division_1(data_closet_splitters.Horizontal_Splitters):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = SECTION_INSERTS_DIVIDERS
        self.width = sn_unit.inch(50)
        self.height = sn_unit.inch(34)
        self.depth = sn_unit.inch(12)
        self.horizontal_openings = 2
        self.drop_id = "sn_closets.drop_insert"


class PRODUCT_Division_2(data_closet_splitters.Horizontal_Splitters):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = SECTION_INSERTS_DIVIDERS
        self.width = sn_unit.inch(50)
        self.height = sn_unit.inch(34)
        self.depth = sn_unit.inch(12)
        self.horizontal_openings = 3
        self.drop_id = "sn_closets.drop_insert"


class PRODUCT_Division_3(data_closet_splitters.Horizontal_Splitters):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = SECTION_INSERTS_DIVIDERS
        self.width = sn_unit.inch(50)
        self.height = sn_unit.inch(34)
        self.depth = sn_unit.inch(12)
        self.horizontal_openings = 4
        self.drop_id = "sn_closets.drop_insert"


class PRODUCT_Division_4(data_closet_splitters.Horizontal_Splitters):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = SECTION_INSERTS_DIVIDERS
        self.width = sn_unit.inch(50)
        self.height = sn_unit.inch(34)
        self.depth = sn_unit.inch(12)
        self.horizontal_openings = 5
        self.drop_id = "sn_closets.drop_insert"


class PRODUCT_Division_5(data_closet_splitters.Horizontal_Splitters):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = SECTION_INSERTS_DIVIDERS
        self.width = sn_unit.inch(50)
        self.height = sn_unit.inch(34)
        self.depth = sn_unit.inch(12)
        self.horizontal_openings = 6
        self.drop_id = "sn_closets.drop_insert"


class PRODUCT_Division_6(data_closet_splitters.Horizontal_Splitters):

    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = SECTION_INSERTS_DIVIDERS
        self.width = sn_unit.inch(50)
        self.height = sn_unit.inch(34)
        self.depth = sn_unit.inch(12)
        self.horizontal_openings = 7
        self.drop_id = "sn_closets.drop_insert"


# class PRODUCT_Shoe_Cubbies_Divisions(data_shoe_cubbies.Shoe_Cubbies):

#     def __init__(self):
#         self.library_name = LIBRARY_NAME
#         self.category_name = SECTION_INSERTS_DIVIDERS
#         self.width = sn_unit.inch(34)
#         self.height = sn_unit.inch(34)
#         self.depth = sn_unit.inch(12)
#         self.drop_id = "sn_closets.drop_insert"
#         self.prompts = {"Divider Thickness": sn_unit.inch(.75)}

class PRODUCT_Garage_Leg(data_garage_leg.Garage_Leg):
    
    def __init__(self):
        self.library_name = LIBRARY_NAME
        self.category_name = CLOSET_PRODUCTS_GARAGE
        self.width = sn_unit.inch(24)
        self.height = sn_unit.inch(4)
        self.depth = sn_unit.inch(.5)
