from .data import data_entry_doors
from snap import sn_unit
from .data.data_windows import (Window,
                                HEIGHT_ABOVE_FLOOR,
                                DEFAULT_DEPTH,
                                DEFAULT_HEIGHT,
                                DEFAULT_WIDTH)


class PRODUCT_Entry_Door_Frame(data_entry_doors.Entry_Door):

    def __init__(self):
        self.category_name = "Open Entry Ways"
        self.assembly_name = "Entry Door Frame"
        self.width = data_entry_doors.SINGLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"


class PRODUCT_Entry_Door_Flat_Panel(data_entry_doors.Entry_Door):

    def __init__(self):
        self.category_name = "Single Doors"
        self.assembly_name = "Entry Door Flat Panel"
        self.width = data_entry_doors.SINGLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Flat.blend"


class PRODUCT_Entry_Door_Double_Panel(data_entry_doors.Entry_Door):

    def __init__(self):
        self.category_name = "Single Doors"
        self.assembly_name = "Entry Door Double Panel"
        self.width = data_entry_doors.SINGLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Double.blend"


class PRODUCT_Entry_Door_Inset_Panel(data_entry_doors.Entry_Door):

    def __init__(self):
        self.category_name = "Single Doors"
        self.assembly_name = "Entry Door Inset Panel"
        self.width = data_entry_doors.SINGLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Inset.blend"


class PRODUCT_Entry_Door_Glass_Panel(data_entry_doors.Entry_Door):

    def __init__(self):
        self.category_name = "Single Doors"
        self.assembly_name = "Entry Door Glass Panel"
        self.width = data_entry_doors.SINGLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass.blend"


class PRODUCT_Entry_Door_Glass_Georgian_Panel(data_entry_doors.Entry_Door):

    def __init__(self):
        self.category_name = "Single Doors"
        self.assembly_name = "Entry Door Glass Georgian Panel"
        self.width = data_entry_doors.SINGLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass_Georgian.blend"


class PRODUCT_Entry_Door_Glass_Border_Panel(data_entry_doors.Entry_Door):

    def __init__(self):
        self.category_name = "Single Doors"
        self.assembly_name = "Entry Door Glass Border Panel"
        self.width = data_entry_doors.SINGLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass_Marginal_Border.blend"


class PRODUCT_Entry_Double_Door_Double_Panel(data_entry_doors.Entry_Door):

    def __init__(self):
        self.category_name = "Double Doors"
        self.assembly_name = "Entry Double Door Double Panel"
        self.width = data_entry_doors.DOUBLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Double.blend"


class PRODUCT_Entry_Double_Door_Flat_Panel(data_entry_doors.Entry_Door):

    def __init__(self):
        self.category_name = "Double Doors"
        self.assembly_name = "Entry Double Door Flat Panel"
        self.width = data_entry_doors.DOUBLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Flat.blend"


class PRODUCT_Entry_Double_Door_Inset_Panel(data_entry_doors.Entry_Door):

    def __init__(self):
        self.category_name = "Double Doors"
        self.assembly_name = "Entry Double Door Inset Panel"
        self.width = data_entry_doors.DOUBLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Inset.blend"


class PRODUCT_Entry_Double_Door_Glass_Panel(data_entry_doors.Entry_Door):

    def __init__(self):
        self.category_name = "Double Doors"
        self.assembly_name = "Entry Double Door Glass Panel"
        self.width = data_entry_doors.DOUBLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass.blend"


class PRODUCT_Entry_Double_Door_Glass_Georgian_Panel(data_entry_doors.Entry_Door):

    def __init__(self):
        self.category_name = "Double Doors"
        self.assembly_name = "Entry Double Door Glass Georgian Panel"
        self.width = data_entry_doors.DOUBLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass_Georgian.blend"


class PRODUCT_Entry_Double_Door_Glass_Border_Panel(data_entry_doors.Entry_Door):

    def __init__(self):
        self.category_name = "Double Doors"
        self.assembly_name = "Entry Double Door Glass Border Panel"
        self.width = data_entry_doors.DOUBLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass_Marginal_Border.blend"


class PRODUCT_Sliding_Door_Flat_Panel(data_entry_doors.Sliding_Doors):

    def __init__(self):
        self.category_name = "Sliding Doors"
        self.assembly_name = "Sliding Door Flat Panel"
        self.width = data_entry_doors.DOUBLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Flat.blend"


class PRODUCT_Sliding_Door_Inset_Panel(data_entry_doors.Sliding_Doors):

    def __init__(self):
        self.category_name = "Sliding Doors"
        self.assembly_name = "Sliding Door Inset Panel"
        self.width = data_entry_doors.DOUBLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Inset.blend"


class PRODUCT_Sliding_Door_Double_Panel(data_entry_doors.Sliding_Doors):

    def __init__(self):
        self.category_name = "Sliding Doors"
        self.assembly_name = "Sliding Door Double Panel"
        self.width = data_entry_doors.DOUBLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Double.blend"


class PRODUCT_Sliding_Door_Glass_Panel(data_entry_doors.Sliding_Doors):

    def __init__(self):
        self.category_name = "Sliding Doors"
        self.assembly_name = "Sliding Door Glass Panel"
        self.width = data_entry_doors.DOUBLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass.blend"


class PRODUCT_Sliding_Door_Glass_Georgian_Panel(data_entry_doors.Sliding_Doors):

    def __init__(self):
        self.category_name = "Sliding Doors"
        self.assembly_name = "Sliding Door Georgian Panel"
        self.width = data_entry_doors.DOUBLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass_Georgian.blend"


class PRODUCT_Sliding_Door_Glass_Border_Panel(data_entry_doors.Sliding_Doors):

    def __init__(self):
        self.category_name = "Sliding Doors"
        self.assembly_name = "Sliding Door Glass Border Panel"
        self.width = data_entry_doors.DOUBLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass_Marginal_Border.blend"


class PRODUCT_Pocket_Door_Flat_Panel(data_entry_doors.Pocket_Doors):

    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Door Flat Panel"
        self.width = data_entry_doors.SINGLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.door_frame = "Pocket_Door_Frame.blend"
        self.door_panel = "Door_Panel_Flat.blend"


class PRODUCT_Pocket_Door_Inset_Panel(data_entry_doors.Pocket_Doors):

    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Door Inset Panel"
        self.width = data_entry_doors.SINGLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.door_frame = "Pocket_Door_Frame.blend"
        self.door_panel = "Door_Panel_Inset.blend"


class PRODUCT_Pocket_Door_Double_Panel(data_entry_doors.Pocket_Doors):

    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Door Double Panel"
        self.width = data_entry_doors.SINGLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.door_frame = "Pocket_Door_Frame.blend"
        self.door_panel = "Door_Panel_Double.blend"


class PRODUCT_Pocket_Door_Glass_Panel(data_entry_doors.Pocket_Doors):

    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Door Glass Panel"
        self.width = data_entry_doors.SINGLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.door_frame = "Pocket_Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass.blend"


class PRODUCT_Pocket_Door_Glass_Georgian_Panel(data_entry_doors.Pocket_Doors):

    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Door Glass Georgian Panel"
        self.width = data_entry_doors.SINGLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.door_frame = "Pocket_Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass_Georgian.blend"


class PRODUCT_Pocket_Door_Glass_Border_Panel(data_entry_doors.Pocket_Doors):

    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Door Glass Border Panel"
        self.width = data_entry_doors.SINGLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.door_frame = "Pocket_Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass_Marginal_Border.blend"


class PRODUCT_Pocket_Double_Door_Flat_Panel(data_entry_doors.Pocket_Doors):

    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Double Door Flat Panel"
        self.width = data_entry_doors.SINGLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Pocket_Door_Frame_Double.blend"
        self.door_panel = "Door_Panel_Flat.blend"


class PRODUCT_Pocket_Double_Door_Inset_Panel(data_entry_doors.Pocket_Doors):

    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Double Door Inset Panel"
        self.width = data_entry_doors.SINGLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Pocket_Door_Frame_Double.blend"
        self.door_panel = "Door_Panel_Inset.blend"


class PRODUCT_Pocket_Double_Door_Double_Panel(data_entry_doors.Pocket_Doors):

    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Double Door Double Panel"
        self.width = data_entry_doors.SINGLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Pocket_Door_Frame_Double.blend"
        self.door_panel = "Door_Panel_Double.blend"


class PRODUCT_Pocket_Double_Door_Glass_Panel(data_entry_doors.Pocket_Doors):

    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Double Door Glass Panel"
        self.width = data_entry_doors.SINGLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Pocket_Door_Frame_Double.blend"
        self.door_panel = "Door_Panel_Glass.blend"


class PRODUCT_Pocket_Double_Door_Glass_Georgian_Panel(data_entry_doors.Pocket_Doors):

    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Double Door Glass Georgian Panel"
        self.width = data_entry_doors.SINGLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Pocket_Door_Frame_Double.blend"
        self.door_panel = "Door_Panel_Glass_Georgian.blend"


class PRODUCT_Pocket_Double_Door_Glass_Border_Panel(data_entry_doors.Pocket_Doors):

    def __init__(self):
        self.category_name = "Pocket Doors"
        self.assembly_name = "Pocket Double Door Glass Border Panel"
        self.width = data_entry_doors.SINGLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Pocket_Door_Frame_Double.blend"
        self.door_panel = "Door_Panel_Glass_Marginal_Border.blend"


class PRODUCT_Bi_Fold_Door_Flat_Panel(data_entry_doors.Bi_Fold_Doors):

    def __init__(self):
        self.category_name = "Bi-Fold Doors"
        self.assembly_name = "Bi-Fold Door Flat Panel"
        self.width = data_entry_doors.SINGLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Flat.blend"


class PRODUCT_Bi_Fold_Door_Inset_Panel(data_entry_doors.Bi_Fold_Doors):

    def __init__(self):
        self.category_name = "Bi-Fold Doors"
        self.assembly_name = "Bi-Fold Door Inset Panel"
        self.width = data_entry_doors.SINGLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Inset.blend"


class PRODUCT_Bi_Fold_Door_Double_Panel(data_entry_doors.Bi_Fold_Doors):

    def __init__(self):
        self.category_name = "Bi-Fold Doors"
        self.assembly_name = "Bi-Fold Door Double Panel"
        self.width = data_entry_doors.SINGLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Double.blend"


class PRODUCT_Bi_Fold_Door_Glass_Panel(data_entry_doors.Bi_Fold_Doors):

    def __init__(self):
        self.category_name = "Bi-Fold Doors"
        self.assembly_name = "Bi-Fold Door Glass Panel"
        self.width = data_entry_doors.SINGLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass.blend"


class PRODUCT_Bi_Fold_Double_Door_Flat_Panel(data_entry_doors.Bi_Fold_Doors):

    def __init__(self):
        self.category_name = "Bi-Fold Doors"
        self.assembly_name = "Bi-Fold Double Door Flat Panel"
        self.width = data_entry_doors.DOUBLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Flat.blend"


class PRODUCT_Bi_Fold_Double_Door_Inset_Panel(data_entry_doors.Bi_Fold_Doors):

    def __init__(self):
        self.category_name = "Bi-Fold Doors"
        self.assembly_name = "Bi-Fold Double Door Inset Panel"
        self.width = data_entry_doors.DOUBLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Inset.blend"


class PRODUCT_Bi_Fold_Double_Door_Double_Panel(data_entry_doors.Bi_Fold_Doors):

    def __init__(self):
        self.category_name = "Bi-Fold Doors"
        self.assembly_name = "Bi-Fold Double Door Double Panel"
        self.width = data_entry_doors.DOUBLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Double.blend"


class PRODUCT_Bi_Fold_Double_Door_Glass_Panel(data_entry_doors.Bi_Fold_Doors):

    def __init__(self):
        self.category_name = "Bi-Fold Doors"
        self.assembly_name = "Bi-Fold Double Door Glass Panel"
        self.width = data_entry_doors.DOUBLE_PANEL_WIDTH
        self.height = data_entry_doors.DOOR_HEIGHT
        self.depth = data_entry_doors.DOOR_DEPTH
        self.double_door = True
        self.door_frame = "Door_Frame.blend"
        self.door_panel = "Door_Panel_Glass.blend"


class PRODUCT_Fixed_Window(Window):

    def __init__(self):
        self.category_name = "Windows"
        self.assembly_name = "Fixed Window"
        self.width = DEFAULT_WIDTH
        self.height = DEFAULT_HEIGHT
        self.depth = DEFAULT_DEPTH
        self.height_above_floor = HEIGHT_ABOVE_FLOOR

        self.window_frame = "Window_Frame_Fixed.blend"
        self.window_divider = ""
        self.window_blinds = ""


class PRODUCT_Fixed_Window_4_Lites(Window):
    def __init__(self):
        self.category_name = "Windows"
        self.assembly_name = "Fixed Window 4 Lites"
        self.width = DEFAULT_WIDTH
        self.height = DEFAULT_HEIGHT
        self.depth = DEFAULT_DEPTH
        self.height_above_floor = HEIGHT_ABOVE_FLOOR

        self.window_frame = "Window_Frame_Fixed.blend"
        self.window_divider = "Window_Divider_4_Lites.blend"
        self.window_blinds = ""


class PRODUCT_Fixed_Window_Marginal_Borders(Window):
    def __init__(self):
        self.category_name = "Windows"
        self.assembly_name = "Fixed Window Marginal Borders"
        self.width = DEFAULT_WIDTH
        self.height = DEFAULT_HEIGHT
        self.depth = DEFAULT_DEPTH
        self.height_above_floor = HEIGHT_ABOVE_FLOOR

        self.window_frame = "Window_Frame_Fixed.blend"
        self.window_divider = "Window_Divider_Border.blend"
        self.window_blinds = ""


class PRODUCT_Fixed_Window_Georgian(Window):

    def __init__(self):
        self.category_name = "Windows"
        self.assembly_name = "Fixed Window Georgian"
        self.width = DEFAULT_WIDTH
        self.height = DEFAULT_HEIGHT
        self.depth = DEFAULT_DEPTH
        self.height_above_floor = HEIGHT_ABOVE_FLOOR

        self.window_frame = "Window_Frame_Fixed.blend"
        self.window_divider = "Window_Divider_Georgian.blend"
        self.window_blinds = ""


class PRODUCT_Hung_Window(Window):

    def __init__(self):
        self.category_name = "Windows"
        self.assembly_name = "Hung Window"
        self.width = DEFAULT_WIDTH
        self.height = sn_unit.inch(48)
        self.depth = DEFAULT_DEPTH
        self.height_above_floor = HEIGHT_ABOVE_FLOOR

        self.window_frame = "Window_Frame_Hung.blend"
        self.window_divider = ""
        self.window_blinds = ""


class PRODUCT_Hung_Window_4_Lites(Window):
    def __init__(self):
        self.category_name = "Windows"
        self.assembly_name = "Hung Window 4 Lites"
        self.width = DEFAULT_WIDTH
        self.height = sn_unit.inch(48)
        self.depth = DEFAULT_DEPTH
        self.height_above_floor = HEIGHT_ABOVE_FLOOR

        self.window_frame = "Window_Frame_Hung.blend"
        self.window_divider = "Window_Divider_4_Lites.blend"
        self.window_blinds = ""


class PRODUCT_Hung_Window_Marginal_Borders(Window):
    def __init__(self):
        self.category_name = "Windows"
        self.assembly_name = "Hung Window Marginal Borders"
        self.width = DEFAULT_WIDTH
        self.height = sn_unit.inch(48)
        self.depth = DEFAULT_DEPTH
        self.height_above_floor = HEIGHT_ABOVE_FLOOR

        self.window_frame = "Window_Frame_Hung.blend"
        self.window_divider = "Window_Divider_Border.blend"
        self.window_blinds = ""


class PRODUCT_Hung_Window_Georgian(Window):
    def __init__(self):
        self.category_name = "Windows"
        self.assembly_name = "Hung Window Georgian"
        self.width = DEFAULT_WIDTH
        self.height = sn_unit.inch(48)
        self.depth = DEFAULT_DEPTH
        self.height_above_floor = HEIGHT_ABOVE_FLOOR

        self.window_frame = "Window_Frame_Hung.blend"
        self.window_divider = "Window_Divider_Georgian.blend"
        self.window_blinds = ""


class PRODUCT_Sliding_Window(Window):
    def __init__(self):
        self.category_name = "Windows"
        self.assembly_name = "Sliding Window"
        self.width = sn_unit.inch(64)
        self.height = DEFAULT_HEIGHT
        self.depth = DEFAULT_DEPTH
        self.height_above_floor = HEIGHT_ABOVE_FLOOR

        self.window_frame = "Window_Frame_Sliding.blend"
        self.window_divider = ""
        self.window_blinds = ""


class PRODUCT_Sliding_Window_4_Lites(Window):
    def __init__(self):
        self.category_name = "Windows"
        self.assembly_name = "Sliding Window 4 Lites"
        self.width = sn_unit.inch(64)
        self.height = DEFAULT_HEIGHT
        self.depth = DEFAULT_DEPTH
        self.height_above_floor = HEIGHT_ABOVE_FLOOR

        self.window_frame = "Window_Frame_Sliding.blend"
        self.window_divider = "Window_Divider_4_Lites.blend"
        self.window_blinds = ""


class PRODUCT_Sliding_Window_Marginal_Borders(Window):
    def __init__(self):
        self.category_name = "Windows"
        self.assembly_name = "Sliding Window Marginal Borders"
        self.width = sn_unit.inch(64)
        self.height = DEFAULT_HEIGHT
        self.depth = DEFAULT_DEPTH
        self.height_above_floor = HEIGHT_ABOVE_FLOOR

        self.window_frame = "Window_Frame_Sliding.blend"
        self.window_divider = "Window_Divider_Border.blend"
        self.window_blinds = ""


class PRODUCT_Sliding_Window_Georgian(Window):
    def __init__(self):
        self.category_name = "Windows"
        self.assembly_name = "Sliding Window Georgian"
        self.width = sn_unit.inch(64)
        self.height = DEFAULT_HEIGHT
        self.depth = DEFAULT_DEPTH
        self.height_above_floor = HEIGHT_ABOVE_FLOOR

        self.window_frame = "Window_Frame_Sliding.blend"
        self.window_divider = "Window_Divider_Georgian.blend"
        self.window_blinds = ""


class PRODUCT_Triple_Window(Window):

    def __init__(self):
        self.category_name = "Windows"
        self.assembly_name = "Triple Window"
        self.width = sn_unit.inch(64)
        self.height = sn_unit.inch(48)
        self.depth = DEFAULT_DEPTH
        self.height_above_floor = HEIGHT_ABOVE_FLOOR

        self.window_frame = "Window_Frame_Triple.blend"
        self.window_divider = ""
        self.window_blinds = ""


class PRODUCT_Triple_Window_4_Lites(Window):
    def __init__(self):
        self.category_name = "Windows"
        self.assembly_name = "Triple Window 4 Lites"
        self.width = sn_unit.inch(64)
        self.height = sn_unit.inch(48)
        self.depth = DEFAULT_DEPTH
        self.height_above_floor = HEIGHT_ABOVE_FLOOR

        self.window_frame = "Window_Frame_Triple.blend"
        self.window_divider = "Window_Divider_4_Lites.blend"
        self.window_blinds = ""


class PRODUCT_Triple_Window_Marginal_Borders(Window):
    def __init__(self):
        self.category_name = "Windows"
        self.assembly_name = "Triple Window Marginal Borders"
        self.width = sn_unit.inch(64)
        self.height = sn_unit.inch(48)
        self.depth = DEFAULT_DEPTH
        self.height_above_floor = HEIGHT_ABOVE_FLOOR

        self.window_frame = "Window_Frame_Triple.blend"
        self.window_divider = "Window_Divider_Border.blend"
        self.window_blinds = ""


class PRODUCT_Triple_Window_Georgian(Window):
    def __init__(self):
        self.category_name = "Windows"
        self.assembly_name = "Triple Window Georgian"
        self.width = sn_unit.inch(64)
        self.height = sn_unit.inch(48)
        self.depth = DEFAULT_DEPTH
        self.height_above_floor = HEIGHT_ABOVE_FLOOR

        self.window_frame = "Window_Frame_Triple.blend"
        self.window_divider = "Window_Divider_Georgian.blend"
        self.window_blinds = ""
