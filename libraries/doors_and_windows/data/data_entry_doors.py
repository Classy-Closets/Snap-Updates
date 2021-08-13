import bpy
import math
import os
from snap import sn_types, sn_unit, sn_utils, sn_paths
from snap.libraries.closets import closet_paths
from math import radians, degrees
from bpy.types import Operator
from bpy.props import FloatProperty, EnumProperty, StringProperty

DOOR_DIR = os.path.join(sn_paths.DOORS_AND_WINDOWS_ROOT, 'assets', 'Entry Door')
DOOR_FRAME_PATH = os.path.join(DOOR_DIR, "Door Frames")
DOOR_PANEL = os.path.join(DOOR_DIR, "Door Panels")
DOOR_HANDLE = os.path.join(DOOR_DIR, "Door Handles", "Door_Handle.blend")
HINGE = os.path.join(DOOR_DIR, "Door Hardware", "Hinge.blend")
LATCH = os.path.join(DOOR_DIR, "Door Hardware", "Latch.blend")
MATERIAL_FILE = os.path.join(DOOR_DIR, "materials", "materials.blend")

SINGLE_PANEL_WIDTH = sn_unit.inch(42)
DOUBLE_PANEL_WIDTH = sn_unit.inch(84)
DOOR_HEIGHT = sn_unit.inch(83)
DOOR_DEPTH = sn_unit.inch(6)
HANDLE_HEIGHT = sn_unit.inch(37)


class Entry_Door(sn_types.Assembly):
    library_name = "Entry Doors"
    category_name = "Entry Doors"
    assembly_name = ""
    show_in_library = True
    id_prompt = "sn_entry_doors.entry_door_prompts"
    plan_draw_id = "sn_entry_doors.draw_plan"
    type_assembly = "PRODUCT"
    mirror_z = False
    mirror_y = False
    width = 0
    height = 0
    depth = 0

    door_frame = ""
    door_panel = ""
    double_door = False

    def add_hardware(self, panel_assembly, no_latch=False):
        Width = panel_assembly.obj_x.snap.get_var("location.x", "Width")
        Height = panel_assembly.obj_z.snap.get_var("location.z", "Height")
        Depth = panel_assembly.obj_y.snap.get_var("location.y", "Depth")
        Hinge_Offset = self.get_prompt("Hinge Placement").get_var("Hinge_Offset")

        hinge_bottom = self.add_object_from_file(HINGE)
        hinge_bottom = sn_types.Part(obj_bp=hinge_bottom)
        hinge_bottom.obj_bp.parent = panel_assembly.obj_bp
        hinge_bottom.set_name("Bottom Hinge")
        hinge_bottom.loc_z("Hinge_Offset", [Hinge_Offset])
        hinge_bottom.rot_y(value=radians(-90))
        hinge_bottom.material("Aluminum")

        hinge_top = self.add_object_from_file(HINGE)
        hinge_top = sn_types.Part(obj_bp=hinge_top)
        hinge_top.obj_bp.parent = panel_assembly.obj_bp
        hinge_top.set_name("Top Hinge")
        hinge_top.loc_z("Height-Hinge_Offset", [Hinge_Offset, Height])
        hinge_top.rot_y(value=radians(-90))
        hinge_top.material("Aluminum")

        if not no_latch:
            latch = self.add_object_from_file(LATCH)
            latch = sn_types.Part(obj_bp=latch)
            latch.obj_bp.parent = panel_assembly.obj_bp
            latch.set_name("Latch")
            latch.loc_x("Width", [Width])
            latch.loc_y("Depth*0.5", [Depth])
            latch.loc_z(value=HANDLE_HEIGHT)
            latch.rot_y(value=radians(90))
            latch.material("Aluminum")

    def draw(self):
        self.create_assembly()
        self.obj_x.location.x = self.width
        if self.obj_bp.get('mirror_y'):
            self.obj_y.location.y = -self.depth
        else:
            self.obj_y.location.y = self.depth

        if self.obj_bp.get('mirror_z'):
            self.obj_z.location.z = -self.height
        else:
            self.obj_z.location.z = self.height

        if self.door_panel != "":
            self.add_prompt("Reverse Swing", "CHECKBOX", False)
            self.add_prompt("Door Rotation", "ANGLE", 0.0)
            self.add_prompt("Hinge Placement", "DISTANCE", sn_unit.inch(18.0))

            if not self.double_door:
                self.add_prompt("Door Swing", 'COMBOBOX',
                                0, combobox_items=["Left Swing", "Right Swing"])

        Width = self.obj_x.snap.get_var("location.x", "Width")
        Height = self.obj_z.snap.get_var("location.z", "Height")
        Depth = self.obj_y.snap.get_var("location.y", "Depth")
        Door_Rotation = self.get_prompt("Door Rotation").get_var()
        Reverse_Swing = self.get_prompt("Reverse Swing").get_var()

        if not self.double_door:
            Swing = self.get_prompt("Door Swing").get_var()
        door_frame = self.add_assembly_from_file(os.path.join(DOOR_FRAME_PATH, self.door_frame))
        door_frame = sn_types.Part(obj_bp=door_frame)
        door_frame.set_name("Door Frame")
        door_frame.dim_x('Width', [Width])
        door_frame.dim_y('Depth', [Depth])
        door_frame.dim_z('Height', [Height])
        door_frame.material("Entry_Door_Surface")
        door_frame.draw_as_hidden_line()

        if self.door_panel != "":
            door_panel = self.add_assembly_from_file(os.path.join(DOOR_PANEL, self.door_panel))
            door_panel = sn_types.Part(obj_bp=door_panel)
            door_panel.set_name("Door Panel")

            if not self.double_door:
                door_panel.loc_x('IF(Door_Swing==1,Width-INCH(3),INCH(3))', [Width, Swing])
                door_panel.loc_y('IF(Reverse_Swing,IF(Door_Swing==0,INCH(1.75),0),\
                                  IF(Door_Swing==0,Depth,Depth-INCH(1.75)))',
                                 [Swing, Reverse_Swing, Depth])
                door_panel.rot_z('IF(Door_Swing==1,radians(180)+IF(Reverse_Swing,Door_Rotation,-Door_Rotation),\
                                  IF(Reverse_Swing,-Door_Rotation,Door_Rotation))',
                                 [Door_Rotation, Swing, Reverse_Swing])

            else:
                door_panel.loc_x(value=sn_unit.inch(3))
                door_panel.loc_y('Depth-IF(Reverse_Swing,INCH(4.25),INCH(0))', [Reverse_Swing, Depth])
                door_panel.rot_z('IF(Reverse_Swing,-Door_Rotation,Door_Rotation)', [Door_Rotation, Reverse_Swing])

            door_panel.dim_x('Width-INCH(6)', [Width])
            door_panel.dim_z('Height-INCH(3.25)', [Height])
            door_panel.material("Entry_Door_Surface")
            self.add_hardware(door_panel)

            door_handle = self.add_object_from_file(DOOR_HANDLE)
            door_handle = sn_types.Part(obj_bp=door_handle)
            door_handle.obj_bp.parent = door_panel.obj_bp
            door_handle.set_name("Door Handle")
            door_handle.loc_x('Width-INCH(9)', [Width])
            door_handle.loc_y(value=sn_unit.inch(-0.875))
            door_handle.loc_z(value=HANDLE_HEIGHT)
            door_handle.material("Aluminum")

        if self.double_door:
            door_panel.dim_x('(Width-INCH(6))*0.5', [Width])
            door_handle.loc_x('(Width*0.5)-INCH(6)', [Width])

            door_panel_right = self.add_assembly_from_file(os.path.join(DOOR_PANEL, self.door_panel))
            door_panel_right = sn_types.Part(obj_bp=door_panel_right)
            door_panel_right.set_name("Door Panel Right")
            door_panel_right.loc_x('Width-INCH(3)', [Width])
            door_panel_right.loc_y('Depth-INCH(1.75)-IF(Reverse_Swing,INCH(4.25),INCH(0))', [Reverse_Swing, Depth])
            door_panel_right.rot_z('radians(180)+IF(Reverse_Swing,Door_Rotation,-Door_Rotation)',
                                   [Door_Rotation, Reverse_Swing])
            door_panel_right.dim_x('(Width-INCH(6))*0.5', [Width])
            door_panel_right.dim_z('Height-INCH(3.25)', [Height])
            door_panel_right.material("Entry_Door_Surface")

            self.add_hardware(door_panel_right, no_latch=True)

            Dpr_Width = door_panel_right.obj_x.snap.get_var("location.x", "Dpr_Width")

            door_handle_right = self.add_object_from_file(DOOR_HANDLE)
            door_handle_right = sn_types.Part(obj_bp=door_handle_right)
            door_handle_right.set_name("Door Handle Right")
            door_handle_right.obj_bp.parent = door_panel_right.obj_bp
            door_handle_right.loc_x('Dpr_Width-INCH(3)', [Dpr_Width])
            door_handle_right.loc_y(value=sn_unit.inch(-0.875))
            door_handle_right.loc_z(value=HANDLE_HEIGHT)
            door_handle_right.material("Aluminum")
        self.update()

    def update(self):
        super().update()
        self.obj_bp["IS_BP_ENTRY_DOOR"] = True
        self.obj_bp.snap.dont_export = True
   
        if hasattr(self, 'assembly_name'):
            self.set_name(self.assembly_name)
        self.obj_x.location.x = self.width
        if self.obj_bp.get('mirror_y'):
            self.obj_y.location.y = -self.depth
        else:
            self.obj_y.location.y = self.depth

        if self.obj_bp.get('mirror_z'):
            self.obj_z.location.z = -self.height
        else:
            self.obj_z.location.z = self.height


class Sliding_Doors(sn_types.Assembly):
    library_name = "Entry Doors"
    category_name = "Entry Doors"
    assembly_name = ""
    show_in_library = True
    id_prompt = "sn_entry_doors.entry_door_prompts"
    plan_draw_id = "sn_entry_doors.draw_plan"
    type_assembly = "PRODUCT"
    mirror_z = False
    mirror_y = False
    width = 0
    height = 0
    depth = 0

    door_frame = ""
    door_panel = ""

    def draw(self):
        self.create_assembly()
        self.obj_bp.snap.dont_export = True

        self.obj_x.location.x = self.width
        if self.obj_bp.get('mirror_y'):
            self.obj_y.location.y = -self.depth
        else:
            self.obj_y.location.y = self.depth

        if self.obj_bp.get('mirror_z'):
            self.obj_z.location.z = -self.height
        else:
            self.obj_z.location.z = self.height

        self.add_prompt("Open Left Door", "PERCENTAGE", 0)
        self.add_prompt("Open Right Door", "PERCENTAGE", 0)
        self.add_prompt("Frame Width", "DISTANCE", sn_unit.inch(3.0))
        self.add_prompt("Panel Depth", "DISTANCE", sn_unit.inch(1.75))
        self.add_prompt("Door to Door Gap", "DISTANCE", sn_unit.inch(0.125))
        self.add_prompt("Door Panel Overlap", "DISTANCE", sn_unit.inch(1.5))

        Width = self.obj_x.snap.get_var("location.x", "Width")
        Height = self.obj_z.snap.get_var("location.z", "Height")
        Depth = self.obj_y.snap.get_var("location.y", "Depth")
        Frame_Width = self.get_prompt("Frame Width").get_var()
        Panel_Depth = self.get_prompt("Panel Depth").get_var()
        Dtd_Gap = self.get_prompt("Door to Door Gap").get_var("Dtd_Gap")
        Panel_Overlap = self.get_prompt("Door Panel Overlap").get_var("Panel_Overlap")
        Open_L_Door = self.get_prompt("Open Left Door").get_var("Open_L_Door")
        Open_R_Door = self.get_prompt("Open Right Door").get_var("Open_R_Door")

        door_frame = self.add_assembly_from_file(os.path.join(DOOR_FRAME_PATH, self.door_frame))
        door_frame = sn_types.Part(obj_bp=door_frame)
        door_frame.set_name("Door Frame")
        door_frame.dim_x('Width', [Width])
        door_frame.dim_y('Depth', [Depth])
        door_frame.dim_z('Height', [Height])
        door_frame.material("Entry_Door_Surface")

        door_panel = self.add_assembly_from_file(os.path.join(DOOR_PANEL, self.door_panel))
        door_panel = sn_types.Part(obj_bp=door_panel)
        door_panel.set_name("Door Panel")
        door_panel.loc_x('Frame_Width+Open_L_Door*((Width-Frame_Width*2)*0.5-Panel_Overlap*0.5)',
                         [Width, Frame_Width, Panel_Overlap, Open_L_Door])
        door_panel.loc_y('(Depth*0.5)-(Dtd_Gap*0.5)', [Depth, Dtd_Gap])
        door_panel.dim_x('(Width-Frame_Width*2)/2+Panel_Overlap*0.5', [Width, Frame_Width, Panel_Overlap])
        door_panel.dim_z('Height-INCH(3.25)', [Height])
        door_panel.add_prompt("No Hardware", "CHECKBOX", True)
        door_panel.material("Entry_Door_Surface")

        door_panel_right = self.add_assembly_from_file(os.path.join(DOOR_PANEL, self.door_panel))
        door_panel_right = sn_types.Part(obj_bp=door_panel_right)
        door_panel_right.set_name("Door Panel Right")
        door_panel_right.loc_x('(Frame_Width+(Width-Frame_Width*2)/2-Panel_Overlap*0.5)-\
                                Open_R_Door*((Width-Frame_Width*2)*0.5-Panel_Overlap*0.5)',
                               [Width, Frame_Width, Open_R_Door, Panel_Overlap])
        door_panel_right.loc_y('(Depth*0.5)+Panel_Depth+(Dtd_Gap*0.5)', [Depth, Dtd_Gap, Panel_Depth])
        door_panel_right.dim_x('(Width-Frame_Width*2)/2+Panel_Overlap*0.5', [Width, Frame_Width, Panel_Overlap])
        door_panel_right.dim_z('Height-INCH(3.25)', [Height])
        door_panel_right.add_prompt("No Hardware", "CHECKBOX", True)
        door_panel_right.material("Entry_Door_Surface")

        self.update()

    def update(self):
        super().update()
        self.obj_bp["IS_BP_ENTRY_DOOR"] = True
        self.obj_bp.snap.dont_export = True
        
        if hasattr(self, 'assembly_name'):
            self.set_name(self.assembly_name)
        self.obj_x.location.x = self.width
        if self.obj_bp.get('mirror_y'):
            self.obj_y.location.y = -self.depth
        else:
            self.obj_y.location.y = self.depth

        if self.obj_bp.get('mirror_z'):
            self.obj_z.location.z = -self.height
        else:
            self.obj_z.location.z = self.height


class Pocket_Doors(sn_types.Assembly):
    library_name = "Entry Doors"
    category_name = "Entry Doors"
    assembly_name = ""
    id_prompt = "sn_entry_doors.entry_door_prompts"
    plan_draw_id = "sn_entry_doors.draw_plan"
    type_assembly = "PRODUCT"
    show_in_library = True
    mirror_z = False
    mirror_y = False
    width = 0
    height = 0
    depth = 0

    door_frame = ""
    door_panel = ""

    double_door = False

    def draw(self):
        self.create_assembly()
        self.obj_bp.snap.dont_export = True

        self.add_prompt("Open Door", "PERCENTAGE", 0)
        self.add_prompt("Frame Width", "DISTANCE", sn_unit.inch(3.25))
        self.add_prompt("Panel Depth", "DISTANCE", sn_unit.inch(1.75))

        Width = self.obj_x.snap.get_var("location.x", "Width")
        Height = self.obj_z.snap.get_var("location.z", "Height")
        Depth = self.obj_y.snap.get_var("location.y", "Depth")
        Open_Door = self.get_prompt("Open Door").get_var()
        Frame_Width = self.get_prompt("Frame Width").get_var()
        Panel_Depth = self.get_prompt("Panel Depth").get_var()

        door_frame = self.add_assembly_from_file(os.path.join(DOOR_FRAME_PATH, self.door_frame))
        door_frame = sn_types.Part(obj_bp=door_frame)
        door_frame.set_name("Door Frame")
        door_frame.dim_x('Width', [Width])
        door_frame.dim_y('Depth', [Depth])
        door_frame.dim_z('Height', [Height])
        door_frame.material("Entry_Door_Surface")

        door_panel = self.add_assembly_from_file(os.path.join(DOOR_PANEL, self.door_panel))
        door_panel = sn_types.Part(obj_bp=door_panel)
        door_panel.set_name("Door Panel")
        door_panel.loc_y('Depth*0.5+Panel_Depth*0.5', [Depth, Panel_Depth])
        door_panel.dim_z('Height-INCH(3.25)', [Height])
        door_panel.add_prompt("No Hardware", "CHECKBOX", True)

        if not self.double_door:
            door_panel.loc_x('Frame_Width-Open_Door*(Width-Frame_Width*2)', [Width, Frame_Width, Open_Door])
            door_panel.dim_x('(Width-Frame_Width*2)', [Width, Frame_Width])
        else:
            door_panel.loc_x('Frame_Width-Open_Door*((Width-Frame_Width*2)*0.5)', [Width, Frame_Width, Open_Door])
            door_panel.dim_x('(Width-Frame_Width*2)*0.5', [Width, Frame_Width])

        door_panel.material("Entry_Door_Surface")

        if self.double_door:
            door_panel_right = self.add_assembly_from_file(os.path.join(DOOR_PANEL, self.door_panel))
            door_panel_right = sn_types.Part(obj_bp=door_panel_right)
            door_panel_right.set_name("Door Panel Right")
            door_panel_right.loc_x('Width*0.5+(Open_Door*(Width*0.5-Frame_Width))',
                                   [Width, Frame_Width, Open_Door])
            door_panel_right.loc_y('Depth*0.5+Panel_Depth*0.5', [Depth, Panel_Depth])
            door_panel_right.dim_x('(Width-Frame_Width*2)*0.5', [Width, Frame_Width])
            door_panel_right.dim_z('Height-INCH(3.25)', [Height])
            door_panel_right.add_prompt("No Hardware", "CHECKBOX", True)
            door_panel_right.material("Entry_Door_Surface")

        self.update()

    def update(self):
        super().update()
        self.obj_bp["IS_BP_ENTRY_DOOR"] = True
        self.obj_bp.snap.dont_export = True   
        
        if hasattr(self, 'assembly_name'):
            self.set_name(self.assembly_name)
        self.obj_x.location.x = self.width
        if self.obj_bp.get('mirror_y'):
            self.obj_y.location.y = -self.depth
        else:
            self.obj_y.location.y = self.depth

        if self.obj_bp.get('mirror_z'):
            self.obj_z.location.z = -self.height
        else:
            self.obj_z.location.z = self.height


class Bi_Fold_Doors(sn_types.Assembly):
    library_name = "Entry Doors"
    category_name = "Entry Doors"
    assembly_name = ""
    id_prompt = "sn_entry_doors.entry_door_prompts"
    plan_draw_id = "sn_entry_doors.draw_plan"
    type_assembly = "PRODUCT"
    show_in_library = True
    mirror_z = False
    mirror_y = False
    width = 0
    height = 0
    depth = 0

    door_frame = ""
    door_panel = ""

    double_door = False

    def add_single_door_hardware(self, panel_assembly, placement='left'):
        assert placement in ('left', 'right'), "Invalid arg - '{}'".format(placement)

        Width = panel_assembly.obj_x.snap.get_var("location.x", "Width")
        Height = panel_assembly.obj_z.snap.get_var("location.z", "Height")
        Hinge_Offset = self.get_prompt("Hinge Placement").get_var("Hinge_Offset")
        RS = self.get_prompt("Reverse Swing").get_var("RS")
        DS = self.get_prompt("Door Swing").get_var("DS")

        hinge_bottom = self.add_object_from_file(HINGE)
        hinge_bottom = sn_types.Part(obj_bp=hinge_bottom)
        hinge_bottom.obj_bp.parent = panel_assembly.obj_bp
        hinge_bottom.set_name("Bottom Hinge")
        hinge_bottom.loc_z("Hinge_Offset", [Hinge_Offset])
        hinge_bottom.rot_y('IF(OR(AND(DS==0,RS==False),AND(DS==1,RS)),radians(-90),radians(90))', [RS, DS])
        hinge_bottom.rot_z('IF(OR(AND(DS==0,RS==False),AND(DS==1,RS)),radians(0),radians(180))', [RS, DS])
        hinge_bottom.material("Aluminum")

        hinge_top = self.add_object_from_file(HINGE)
        hinge_top = sn_types.Part(obj_bp=hinge_top)
        hinge_top.obj_bp.parent = panel_assembly.obj_bp
        hinge_top.set_name("Top Hinge")
        hinge_top.loc_z("Height-Hinge_Offset", [Hinge_Offset, Height])
        hinge_top.rot_y('IF(OR(AND(DS==0,RS==False),AND(DS==1,RS)),radians(-90),radians(90))', [RS, DS])
        hinge_top.rot_z('IF(OR(AND(DS==0,RS==False),AND(DS==1,RS)),radians(0),radians(180))', [RS, DS])
        hinge_top.material("Aluminum")

        if placement == 'right':
            hinge_bottom.loc_x("Width", [Width])
            hinge_bottom.rot_y('IF(OR(AND(DS==0,RS==False),AND(DS==1,RS)),radians(90),radians(-90))', [RS, DS])
            hinge_bottom.rot_z('IF(OR(AND(DS==0,RS==False),AND(DS==1,RS)),radians(0),radians(180))', [RS, DS])
            hinge_top.loc_x("Width", [Width])
            hinge_top.rot_y('IF(OR(AND(DS==0,RS==False),AND(DS==1,RS)),radians(90),radians(-90))', [RS, DS])
            hinge_top.rot_z('IF(OR(AND(DS==0,RS==False),AND(DS==1,RS)),radians(0),radians(180))', [RS, DS])

    def add_double_door_hardware(self, panel_assembly, placement='left'):
        assert placement in ('left', 'right'), "Invalid arg - '{}'".format(placement)

        Width = panel_assembly.obj_x.snap.get_var("location.x", "Width")
        Height = panel_assembly.obj_z.snap.get_var("location.z", "Height")
        Hinge_Offset = self.get_prompt("Hinge Placement").get_var("Hinge_Offset")

        hinge_bottom = self.add_object_from_file(HINGE)
        hinge_bottom = sn_types.Part(obj_bp=hinge_bottom)
        hinge_bottom.obj_bp.parent = panel_assembly.obj_bp
        hinge_bottom.set_name("Bottom Hinge")
        hinge_bottom.loc_z("Hinge_Offset", [Hinge_Offset])
        hinge_bottom.rot_y(value=radians(-90))
        hinge_bottom.material("Aluminum")

        hinge_top = self.add_object_from_file(HINGE)
        hinge_top = sn_types.Part(obj_bp=hinge_top)
        hinge_top.obj_bp.parent = panel_assembly.obj_bp
        hinge_top.set_name("Top Hinge")
        hinge_top.loc_z("Height-Hinge_Offset", [Hinge_Offset, Height])
        hinge_top.rot_y(value=radians(-90))
        hinge_top.material("Aluminum")

        if placement == 'right':
            hinge_bottom.loc_x("Width", [Width])
            hinge_bottom.rot_y(value=radians(90))
            hinge_top.loc_x("Width", [Width])
            hinge_top.rot_y(value=radians(90))

    def set_mirror_modifier(self, assembly, mod_name, mirror_obj):
        for child in assembly.obj_bp.children:
            if child.type == 'MESH':
                child.modifiers.new(mod_name, 'MIRROR')
                child.modifiers[mod_name].mirror_object = mirror_obj

    def draw(self):
        self.create_assembly()
        self.obj_bp.snap.dont_export = True

        self.add_prompt("Open Door", "PERCENTAGE", 0)
        self.add_prompt("Reverse Swing", "CHECKBOX", True)
        self.add_prompt("Frame Width", "DISTANCE", sn_unit.inch(3.25))
        self.add_prompt("Panel Depth", "DISTANCE", sn_unit.inch(1.75))
        self.add_prompt("Door Gap", "DISTANCE", sn_unit.inch(0.125))
        self.add_prompt("Hinge Placement", "DISTANCE", sn_unit.inch(18.0))

        Width = self.obj_x.snap.get_var("location.x", "Width")
        Height = self.obj_z.snap.get_var("location.z", "Height")
        Depth = self.obj_y.snap.get_var("location.y", "Depth")
        Open = self.get_prompt("Open Door").get_var("Open")
        Frame_Width = self.get_prompt("Frame Width").get_var()
        Panel_Depth = self.get_prompt("Panel Depth").get_var()
        Door_Gap = self.get_prompt("Door Gap").get_var()
        RS = self.get_prompt("Reverse Swing").get_var("RS")

        door_frame = self.add_assembly_from_file(os.path.join(DOOR_FRAME_PATH, self.door_frame))
        door_frame = sn_types.Part(obj_bp=door_frame)
        door_frame.set_name("Door Frame")
        door_frame.dim_x('Width', [Width])
        door_frame.dim_y('Depth', [Depth])
        door_frame.dim_z('Height', [Height])
        door_frame.material("")

        if not self.double_door:
            self.add_prompt("Door Swing", 'COMBOBOX',
                            0, combobox_items=["Left Swing", "Right Swing"])
            DS = self.get_prompt("Door Swing").get_var("DS")

            door_panel_left_1 = self.add_assembly_from_file(os.path.join(DOOR_PANEL, self.door_panel))
            door_panel_left_1 = sn_types.Part(obj_bp=door_panel_left_1)
            door_panel_left_1.set_name("Door Panel Left 1")
            door_panel_left_1.loc_x('IF(DS==0,Frame_Width+Panel_Depth*Open,Width-Frame_Width-Panel_Depth*Open)',
                                    [Frame_Width, Open, Panel_Depth, DS, Width])
            door_panel_left_1.loc_y('Depth*0.5+IF(RS,-Panel_Depth,Panel_Depth)*0.5', [Depth, Panel_Depth, RS])
            door_panel_left_1.dim_x('(Width-Frame_Width*2-Door_Gap*2)*0.5', [Width, Frame_Width, Door_Gap])
            door_panel_left_1.dim_y('IF(OR(AND(DS==0,RS==False),AND(DS==1,RS)),-Panel_Depth, Panel_Depth)',
                                    [RS, Panel_Depth, DS])
            door_panel_left_1.dim_z('Height-INCH(3.25)', [Height])
            door_panel_left_1.rot_z('IF(DS==0,0,radians(180))+radians(-90)*IF(OR(AND\
                                    (RS,DS==0),AND(RS==False,DS==1)),-Open,Open)', [Open, RS, DS])
            door_panel_left_1.add_prompt("Hardware Config", "COMBOBOX", 0, combobox_items=["Right", "Left"])
            door_panel_left_1.material("Entry_Door_Surface")
            self.add_single_door_hardware(door_panel_left_1, placement='right')

            door_panel_left_2 = self.add_assembly_from_file(os.path.join(DOOR_PANEL, self.door_panel))
            door_panel_left_2 = sn_types.Part(obj_bp=door_panel_left_2)
            door_panel_left_2.set_name("Door Panel Left 2")
            door_panel_left_2.obj_bp.parent = door_panel_left_1.obj_bp
            door_panel_left_2.loc_x('(Width-Frame_Width*2)*0.5+Door_Gap*0.5', [Width, Frame_Width, Door_Gap])
            door_panel_left_2.dim_x('(Width-Frame_Width*2-Door_Gap*2)*0.5', [Width, Frame_Width, Door_Gap])
            door_panel_left_2.dim_y('IF(OR(AND(DS==0,RS==False),AND(DS==1,RS)),-Panel_Depth, Panel_Depth)',
                                    [RS, Panel_Depth, DS])
            door_panel_left_2.dim_z('Height-INCH(3.25)', [Height])
            door_panel_left_2.rot_z('radians(180)-(radians(180)-(radians(90)*IF(OR(AND(RS,DS==0),\
                                    AND(RS==False,DS==1)),-Open,Open))*2)', [Open, RS, DS])
            door_panel_left_2.add_prompt("Hardware Config", "COMBOBOX", 1, combobox_items=["Right", "Left"])
            door_panel_left_2.material("Entry_Door_Surface")
            self.add_single_door_hardware(door_panel_left_2)

        else:
            mirror_obj = self.add_empty('Mirror Object')
            mirror_obj = sn_types.Part(obj_bp=mirror_obj)
            mirror_obj.loc_x('Width*0.5', [Width])

            door_panel_left_1 = self.add_assembly_from_file(os.path.join(DOOR_PANEL, self.door_panel))
            door_panel_left_1 = sn_types.Part(obj_bp=door_panel_left_1)
            door_panel_left_1.set_name("Door Panel Left 1")
            door_panel_left_1.loc_x('IF(RS,Width-Frame_Width-Panel_Depth*Open,Frame_Width+Panel_Depth*Open)',
                                    [Frame_Width, Open, Panel_Depth, RS, Width])
            door_panel_left_1.loc_y('Depth*0.5+IF(RS,-Panel_Depth*0.5,Panel_Depth*0.5)', [Depth, Panel_Depth, RS])
            door_panel_left_1.dim_x('(Width-Frame_Width*2-Door_Gap*2)*0.25', [Width, Frame_Width, Door_Gap])
            door_panel_left_1.dim_z('Height-INCH(3.25)', [Height])
            door_panel_left_1.rot_z('IF(RS,radians(180),0)+radians(-90)*Open', [Open, RS])
            door_panel_left_1.add_prompt("Hardware Config", "COMBOBOX", 0, combobox_items=["Right", "Left"])
            
            door_panel_left_1.material("Entry_Door_Surface")
            self.add_double_door_hardware(door_panel_left_1, placement='right')
            self.set_mirror_modifier(door_panel_left_1, "Mirror X", mirror_obj.obj_bp)

            door_panel_left_2 = self.add_assembly_from_file(os.path.join(DOOR_PANEL, self.door_panel))
            door_panel_left_2 = sn_types.Part(obj_bp=door_panel_left_2)
            door_panel_left_2.set_name("Door Panel Left 2")
            door_panel_left_2.obj_bp.parent = door_panel_left_1.obj_bp
            door_panel_left_2.loc_x('(Width-Frame_Width*2)*0.25+Door_Gap*0.5', [Width, Frame_Width, Door_Gap])
            door_panel_left_2.dim_x('(Width-Frame_Width*2-Door_Gap*2)*0.25', [Width, Frame_Width, Door_Gap])
            door_panel_left_2.dim_z('Height-INCH(3.25)', [Height])
            door_panel_left_2.rot_z('radians(180)-(radians(180)-(radians(90)*Open)*2)', [Open])
            door_panel_left_2.add_prompt("Hardware Config", "COMBOBOX", 1, combobox_items=["Right", "Left"])
            door_panel_left_2.material("Entry_Door_Surface")
            self.add_double_door_hardware(door_panel_left_2)
            self.set_mirror_modifier(door_panel_left_2, "Mirror X", mirror_obj.obj_bp)

        self.update()

    def update(self):
        super().update()
        self.obj_bp["IS_BP_ENTRY_DOOR"] = True
        self.obj_bp.snap.dont_export = True
        
        if hasattr(self, 'assembly_name'):
            self.set_name(self.assembly_name)
        self.obj_x.location.x = self.width
        if self.obj_bp.get('mirror_y'):
            self.obj_y.location.y = -self.depth
        else:
            self.obj_y.location.y = self.depth

        if self.obj_bp.get('mirror_z'):
            self.obj_z.location.z = -self.height
        else:
            self.obj_z.location.z = self.height


class SNAP_OT_Entry_Door_Prompts(Operator):
    bl_idname = "sn_entry_doors.entry_door_prompts"
    bl_label = "Entry Door Prompts"
    bl_options = {'UNDO'}

    width: FloatProperty(name="Width", unit='LENGTH', precision=4)
    height: FloatProperty(name="Height", unit='LENGTH', precision=4)
    depth: FloatProperty(name="Depth", unit='LENGTH', precision=4)

    door_rotation: FloatProperty(name="Door Rotation", subtype='ANGLE', min=0, max=math.radians(110))

    door_swing: EnumProperty(name="Door Swing", items=[('0', "Left Swing", "Left Swing"),
                                        ('1', "Right Swing", "Right Swing")])
    product = None

    open_door_prompt = None

    door_swing_prompt = None

    @classmethod
    def poll(cls, context):
        return True

    def check(self, context):
        self.product.obj_x.location.x = self.width

        if self.product.obj_bp.get('mirror_y'):
            self.product.obj_y.location.y = -self.depth
        else:
            self.product.obj_y.location.y = self.depth

        if self.product.obj_bp.get('mirror_z'):
            self.product.obj_z.location.z = -self.height
        else:
            self.product.obj_z.location.z = self.height

        if self.open_door_prompt:
            self.open_door_prompt.set_value(degrees(self.door_rotation))

        if self.door_swing_prompt:
            self.door_swing_prompt.set_value(int(self.door_swing))

        self.product.obj_bp.location = self.product.obj_bp.location
        self.product.obj_bp.location = self.product.obj_bp.location

        return True

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        obj = context.object
        obj_product_bp = sn_utils.get_bp(obj, 'PRODUCT')
        self.product = sn_types.Part(obj_product_bp)
        if self.product.obj_bp:
            self.depth = math.fabs(self.product.obj_y.location.y)
            self.height = math.fabs(self.product.obj_z.location.z)
            self.width = math.fabs(self.product.obj_x.location.x)

            try:
                self.open_door_prompt = self.product.get_prompt("Door Rotation")
                self.door_rotation = self.open_door_prompt.get_value()
            except:
                pass

            try:
                self.door_swing_prompt = self.product.get_prompt("Door Swing")
                self.door_swing = self.door_swing_prompt.get_value()
            except:
                pass

        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=480)

    def draw_product_size(self, layout):
        row = layout.row()
        box = row.box()
        col = box.column(align=True)

        row1 = col.row(align=True)
        if self.object_has_driver(self.product.obj_x):
            row1.label(text='Width: ' + str(sn_unit.inch(math.fabs(self.product.obj_x.location.x))))
        else:
            row1.label(text='Width:')
            row1.prop(self, 'width', text="")
            row1.prop(self.product.obj_x, 'hide_viewport', text="")

        row1 = col.row(align=True)
        if self.object_has_driver(self.product.obj_z):
            row1.label(text='Height: ' + str(sn_unit.inch(math.fabs(self.product.obj_z.location.z))))
        else:
            row1.label(text='Height:')
            row1.prop(self, 'height', text="")
            row1.prop(self.product.obj_z, 'hide_viewport', text="")

        row1 = col.row(align=True)
        if self.object_has_driver(self.product.obj_y):
            row1.label(text='Depth: ' + str(sn_unit.inch(math.fabs(self.product.obj_y.location.y))))
        else:
            row1.label(text='Depth:')
            row1.prop(self, 'depth', text="")
            row1.prop(self.product.obj_y, 'hide_viewport', text="")

    def object_has_driver(self, obj):
        if obj.animation_data:
            if len(obj.animation_data.drivers) > 0:
                return True

    def draw_product_prompts(self, layout):
        # I don't know if we need this.
        # if "Main Options" in self.product.obj_bp.snap.PromptPage.COL_MainTab:
        door_swing = self.product.get_prompt("Door Swing")
        reverse_swing = self.product.get_prompt("Reverse Swing")
        open_door = self.product.get_prompt("Open Door")
        open_left_door = self.product.get_prompt("Open Left Door")
        open_right_door = self.product.get_prompt("Open Right Door")

        box = layout.box()
        col = box.column(align=True)
        col.label(text="Main Options:")
        row = col.row()
        row.label(text="Open Door")

        if open_door:
            row.prop(open_door, "factor_value", text="")
        elif open_left_door:
            row.prop(open_left_door, "factor_value", text="Panel 1")
            row.prop(open_right_door, "factor_value", text="Panel 2")
        else:
            row.prop(self, 'door_rotation', text="", slider=True)

        if door_swing:
            col = box.column()
            row = col.row()
            row.label(text="Door Swing")
            row.prop(self, 'door_swing', expand=True)
        col = box.column()

        if reverse_swing:
            row = col.row()
            row.label(text="Reverse Swing")
            row.prop(reverse_swing, 'checkbox_value', text="")

    def draw_product_placment(self, layout):
        box = layout.box()
        row = box.row()
        row.label(text='Location:')
        row.prop(self.product.obj_bp, 'location', index=0, text="")

    def draw(self, context):
        layout = self.layout
        if self.product.obj_bp:
            if self.product.obj_bp.name in context.scene.objects:
                box = layout.box()

                split = box.split(factor=.8)
                split.label(text=self.product.obj_bp.name, icon='LATTICE_DATA')

                self.draw_product_size(box)
                self.draw_product_prompts(box)
                self.draw_product_placment(box)


def register():
    bpy.utils.register_class(SNAP_OT_Entry_Door_Prompts)


def unregister():
    bpy.utils.unregister_class(SNAP_OT_Entry_Door_Prompts)
