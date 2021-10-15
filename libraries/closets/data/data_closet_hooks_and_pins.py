from os import path
import math

import bpy
from bpy.types import Operator
from bpy.props import (
    StringProperty,
    FloatProperty,
    EnumProperty)

from snap import sn_types, sn_utils, sn_unit
from ..ops.drop_closet import PlaceClosetInsert
from ..common import common_parts
from .. import closet_paths
from .. import closet_props

ASSEMBLY_DIR = closet_paths.get_closet_assemblies_path()
OBJECT_DIR = closet_paths.get_closet_objects_path()
PATH = path.join(common_parts.LIBRARY_DATA_DIR, "Closet Assemblies")
PEG_OBJECT = path.join(OBJECT_DIR, "Peg Object.blend")
ROBE_HOOK = path.join(OBJECT_DIR, "Robe Hook.blend")
DORB_HOOK = path.join(OBJECT_DIR, "DORB Hook.blend")
COAT_AND_HAT_HOOK = path.join(OBJECT_DIR, "Coat and Hat Hook.blend")
DOUBLE_ROBE_HOOK = path.join(OBJECT_DIR, "Double Robe Hook.blend")
DECO_PANEL = path.join(ASSEMBLY_DIR, "Deco Panel.blend")
VALET_ROD = path.join(OBJECT_DIR, "Valet Rod", "Valet Rod.blend")
VALET_ROD2 = path.join(OBJECT_DIR, "Valet Rod2.blend")


class Accessory(sn_types.Assembly):

    type_assembly = "PRODUCT"
    drop_id = "sn_closets.place_closet_accessory"
    show_in_library = True
    library_name = ""
    category_name = ""

    def update(self):
        super().update()
        self.obj_x.location.x = self.width
        self.obj_y.location.y = -self.depth
        self.obj_z.location.z = self.height

        self.obj_bp.sn_closets.is_accessory_bp = True  # TODO: Remove
        self.obj_bp["IS_BP_CLOSET"] = True
        self.obj_bp["IS_BP_ACCESSORY"] = True
        # self.obj_bp["ID_PROMPT"] = self.id_prompt
        self.obj_bp["ID_DROP"] = self.drop_id
        self.obj_bp.snap.type_group = self.type_assembly

    def add_prompts(self):
        self.add_prompt("Custom Rack Style", 'COMBOBOX', 0, ["Classic", "Deco"])
        self.add_prompt("Add Slide", 'CHECKBOX', True)
        self.add_prompt("Hook Type", 'TEXT', "BRK")

    # TODO: add dimensions
    def add_dimension(self):
        World_Z = self.obj_bp.snap.get_var('matrix_world[2][3]', 'World_Z')
        accessory_height_dim = sn_types.Dimension()
        accessory_height_dim.anchor.parent = self.obj_bp
        accessory_height_dim.end_z('-World_Z', [World_Z])


class Belt_Accessories(Accessory):
    id_prompt = "sn_closets.belt_rack"

    def update(self):
        super().update()
        self.obj_bp["IS_BP_BELT_RACK"] = True
        self.obj_bp["ID_PROMPT"] = 'sn_closets.belt_rack'

    def draw(self):
        self.create_assembly()
        # we are adding a master hide for everything
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()

        self.add_prompts()
        self.add_prompt("Pin Qty", 'QUANTITY', 11)

        # SIZES OF STANDARD ACCESSORY PANELS
        self.add_prompt("Pin Length", 'DISTANCE', sn_unit.inch(1.5))
        self.add_prompt("Pin Offset", 'DISTANCE', sn_unit.inch(.75))

        self.add_prompt('Belt Rack Category', 'COMBOBOX', 0, ['Synergy', 'Elite'])
        self.add_prompt('Metal Color', 'COMBOBOX', 0, ['Chrome', 'Matte Aluminum', 'Matte Nickel', 'Matte Gold', 'ORB', 'Slate'])
        self.add_prompt('Synergy Belt Rack Length', 'COMBOBOX', 0, ['12"', '14"'])
        self.add_prompt('Elite Belt Rack Length', 'COMBOBOX', 0, ['12"', '14"', '18"'])

        width = self.obj_x.snap.get_var("location.x", 'width')
        height = self.obj_z.snap.get_var("location.z", 'height')
        depth = self.obj_y.snap.get_var("location.y", 'depth')
        Pin_Offset = self.get_prompt("Pin Offset").get_var()
        Pin_Qty = self.get_prompt("Pin Qty").get_var()
        Custom_Rack_Style = self.get_prompt("Custom Rack Style").get_var()

        SBRL = self.get_prompt('Synergy Belt Rack Length').get_var("SBRL")
        EBRL = self.get_prompt('Elite Belt Rack Length').get_var("EBRL")
        BRC = self.get_prompt('Belt Rack Category').get_var('BRC')

        panel = common_parts.add_accessory_panel(self)
        panel.set_name('Accessory Cleat')
        panel.dim_x('IF(IF(BRC==0,SBRL,EBRL)==0,INCH(12),IF(IF(BRC==0,SBRL,EBRL)==1,INCH(14),INCH(18)))', [SBRL, EBRL, BRC])
        panel.dim_y('depth', [depth])
        panel.dim_z('height', [height])
        panel.get_prompt('Hide').set_formula('IF(BRC==0,False,True) or Hide', [BRC, self.hide_var])
        panel.cutpart("Panel")

        deco_panel = sn_types.Part(self.add_assembly_from_file(DECO_PANEL))
        self.add_assembly(deco_panel)
        deco_panel.set_name('Deco Accessory Cleat')
        deco_panel.dim_x('IF(IF(BRC==0,SBRL,EBRL)==0,INCH(12),IF(IF(BRC==0,SBRL,EBRL)==1,INCH(14),INCH(18)))', [SBRL, EBRL, BRC])
        deco_panel.dim_y('depth', [depth])
        deco_panel.dim_z('height', [height])
        deco_panel.get_prompt('Hide').set_formula('IF(BRC==1,False,True) or Hide', [BRC, self.hide_var])
        deco_panel.cutpart("Panel")

        pin = self.add_object_from_file(PEG_OBJECT)
        pin.snap.name_object = "Belt Rack"
        pin.snap.loc_x('Pin_Offset', [Pin_Offset])
        pin.snap.loc_y('depth/2', [depth])
        pin.snap.loc_z('height/2', [height])
        # pin.material("Chrome")
        array_mod = pin.modifiers.new('Quantity', 'ARRAY')
        array_mod.use_relative_offset = False
        array_mod.use_constant_offset = True

        pin.snap.modifier(
            array_mod, 'constant_offset_displace', 0,
            "(IF(IF(BRC==0,SBRL,EBRL)==0,INCH(12),IF(IF(BRC==0,SBRL,EBRL)==1,INCH(14),INCH(18)))-Pin_Offset)/Pin_Qty", [SBRL, EBRL, BRC, Pin_Qty, Pin_Offset])

        pin.snap.modifier(array_mod, 'count', -1, "Pin_Qty", [Pin_Qty])

        self.update()


class Tie_Accessories(Accessory):
    id_prompt = "sn_closets.tie_rack"
    
    def update(self):
        super().update()
        self.obj_bp["IS_BP_TIE_RACK"] = True
        self.obj_bp["ID_PROMPT"] = self.id_prompt

    def draw(self):
        self.create_assembly()
        # we are adding a master hide for everything
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()

        self.add_prompts()
        self.add_prompt("Top Pin Qty", 'QUANTITY', 12)
        self.add_prompt("Bottom Pin Qty", 'QUANTITY', 11)

        # SIZES OF STANDARD ACCESSORY PANELS
        self.add_prompt("Pin Length", 'DISTANCE', sn_unit.inch(1.5))
        self.add_prompt("Pin Offset", 'DISTANCE', sn_unit.inch(.75))

        self.add_prompt('Tie Rack Category', 'COMBOBOX', 0, ['Synergy', 'Elite'])
        self.add_prompt('Metal Color', 'COMBOBOX', 0, ['Chrome', 'Matte Aluminum', 'Matte Nickel', 'Matte Gold', 'ORB', 'Slate'])
        self.add_prompt('Synergy Tie Rack Length', 'COMBOBOX', 0, ['12"', '14"'])
        self.add_prompt('Elite Tie Rack Length', 'COMBOBOX', 0, ['12"', '14"', '18"'])

        width = self.obj_x.snap.get_var("location.x", 'width')
        height = self.obj_z.snap.get_var("location.z", 'height')
        depth = self.obj_y.snap.get_var("location.y", 'depth')
        Pin_Offset = self.get_prompt("Pin Offset").get_var()
        Top_Pin_Qty = self.get_prompt("Top Pin Qty").get_var()
        Bottom_Pin_Qty = self.get_prompt("Bottom Pin Qty").get_var()
        Custom_Rack_Style = self.get_prompt("Custom Rack Style").get_var()

        STRL = self.get_prompt('Synergy Tie Rack Length').get_var("STRL")
        ETRL = self.get_prompt('Elite Tie Rack Length').get_var("ETRL")
        TRC = self.get_prompt('Tie Rack Category').get_var('TRC')

        panel = common_parts.add_accessory_panel(self)
        panel.set_name('Accessory Cleat')
        panel.dim_x('IF(IF(TRC==0,STRL,ETRL)==0,INCH(12),IF(IF(TRC==0,STRL,ETRL)==1,INCH(14),INCH(18)))', [STRL, ETRL, TRC])
        panel.dim_y('depth', [depth])
        panel.dim_z('height', [height])
        panel.get_prompt('Hide').set_formula('IF(TRC==0,False,True) or Hide', [TRC, self.hide_var])
        panel.cutpart("Panel")

        deco_panel = sn_types.Part(self.add_assembly_from_file(DECO_PANEL))
        self.add_assembly(deco_panel)
        deco_panel.set_name('Deco Accessory Cleat')
        deco_panel.dim_x('IF(IF(TRC==0,STRL,ETRL)==0,INCH(12),IF(IF(TRC==0,STRL,ETRL)==1,INCH(14),INCH(18)))', [STRL, ETRL, TRC])
        deco_panel.dim_y('depth', [depth])
        deco_panel.dim_z('height', [height])
        deco_panel.get_prompt('Hide').set_formula('IF(TRC==1,False,True) or Hide', [TRC, self.hide_var])
        deco_panel.cutpart("Panel")

        top_pin = self.add_object_from_file(PEG_OBJECT)
        top_pin.snap.name_object = "Tie Rack"
        top_pin.snap.loc_x('Pin_Offset', [Pin_Offset])
        top_pin.snap.loc_y('depth/2', [depth])
        top_pin.snap.loc_z('height/1.5', [height])
        # top_pin.material("Chrome")  TODO: Set material
        mod = top_pin.modifiers.new('Quantity', 'ARRAY')
        mod.use_relative_offset = False
        mod.use_constant_offset = True

        top_pin.snap.modifier(
            mod, "constant_offset_displace", 0,
            "(IF(IF(TRC==0,STRL,ETRL)==0,INCH(12),IF(IF(TRC==0,STRL,ETRL)==1,INCH(14),INCH(18)))-Pin_Offset)/Top_Pin_Qty",
            [STRL, ETRL, TRC, Top_Pin_Qty, Pin_Offset])

        top_pin.snap.modifier(mod, 'count', -1, "Top_Pin_Qty", [Top_Pin_Qty])

        bot_pin = self.add_object_from_file(PEG_OBJECT)
        bot_pin.snap.type_mesh = 'NONE'
        bot_pin.snap.name_object = "Accessory Pin"
        bot_pin.snap.loc_x('Pin_Offset*1.5', [Pin_Offset])
        bot_pin.snap.loc_y('depth/2', [depth])
        bot_pin.snap.loc_z('height/3', [height])
        # bot_pin.material("Chrome")
        mod = bot_pin.modifiers.new('Quantity', 'ARRAY')
        mod.use_relative_offset = False
        mod.use_constant_offset = True

        bot_pin.snap.modifier(
            mod, "constant_offset_displace", 0,
            "(IF(IF(TRC==0,STRL,ETRL)==0,INCH(12),IF(IF(TRC==0,STRL,ETRL)==1,INCH(14),INCH(18)))-(Pin_Offset*2))/Bottom_Pin_Qty",
            [STRL, ETRL, TRC, Bottom_Pin_Qty, Pin_Offset])

        bot_pin.snap.modifier(mod, 'count', -1, "Bottom_Pin_Qty", [Bottom_Pin_Qty])

        self.update()


class Tie_and_Belt_Accessories(Accessory):
    id_prompt = "sn_closets.accessories"

    def update(self):
        super().update()
        self.obj_bp["ID_PROMPT"] = self.id_prompt

    def draw(self):
        self.create_assembly()
        # we are adding a master hide for everything
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()

        self.add_prompts()
        self.add_prompt("Top Pin Qty", 'QUANTITY', 5)
        self.add_prompt("Bottom Pin Qty", 'QUANTITY', 11)         

        #SIZES OF STANDARD ACCESSORY PANELS
        self.add_prompt("Pin Length", 'DISTANCE', sn_unit.inch(1.5)) 
        self.add_prompt("Pin Offset",'DISTANCE', sn_unit.inch(.75))                                               

        width = self.obj_x.snap.get_var("location.x",'width')
        height = self.obj_z.snap.get_var("location.z",'height')
        depth = self.obj_y.snap.get_var("location.y",'depth')

        Top_Pin_Qty = self.get_prompt("Top Pin Qty").get_var()
        Bottom_Pin_Qty = self.get_prompt("Bottom Pin Qty").get_var()
        Pin_Offset = self.get_prompt("Pin Offset").get_var()
        Custom_Rack_Style = self.get_prompt("Custom Rack Style").get_var()

        panel = common_parts.add_accessory_panel(self)
        panel.set_name('Accessory Cleat')
        panel.dim_x('width', [width])
        panel.dim_y('depth',[depth])
        panel.dim_z('height',[height])
        panel.get_prompt('Hide').set_formula('IF(Custom_Rack_Style==0,False,True) or Hide', [Custom_Rack_Style,self.hide_var])
        panel.cutpart("Panel")

        deco_panel = sn_types.Part(self.add_assembly_from_file(DECO_PANEL))
        self.add_assembly(deco_panel)
        deco_panel.set_name('Deco Accessory Cleat')
        deco_panel.dim_x('width', [width])
        deco_panel.dim_y('depth',[depth])
        deco_panel.dim_z('height',[height])
        deco_panel.get_prompt('Hide').set_formula('IF(Custom_Rack_Style==1,False,True) or Hide', [Custom_Rack_Style,self.hide_var])        
        deco_panel.cutpart("Panel")

        top_pin = self.add_object_from_file(PEG_OBJECT)
        top_pin.snap.name_object = "Accessory Pin"
        top_pin.snap.loc_x('Pin_Offset',[Pin_Offset])
        top_pin.snap.loc_y('depth/2', [depth])
        top_pin.snap.loc_z('height/1.5', [height])
        # top_pin.material('Chrome')
        mod = top_pin.modifiers.new('Quantity','ARRAY')
        mod.use_relative_offset = False
        mod.use_constant_offset = True

        top_pin.snap.modifier(
            mod, 'constant_offset_displace', 0,
            "((width/2)-Pin_Offset)/Top_Pin_Qty", [width, Top_Pin_Qty, Pin_Offset])
        top_pin.snap.modifier(mod, 'count', -1, "Top_Pin_Qty", [Top_Pin_Qty])

        bot_pin = self.add_object_from_file(PEG_OBJECT)
        bot_pin.snap.name_object = "Accessory Pin"
        bot_pin.snap.loc_x('Pin_Offset*2',[Pin_Offset])
        bot_pin.snap.loc_y('depth/2', [depth])
        bot_pin.snap.loc_z('height/3', [height])
        # bot_pin.material('Chrome')
        mod = bot_pin.modifiers.new('Quantity','ARRAY')
        mod.use_relative_offset = False
        mod.use_constant_offset = True

        bot_pin.snap.modifier(
            mod, 'constant_offset_displace', 0,
            "(width-(Pin_Offset*2.5))/Bottom_Pin_Qty", [width, Bottom_Pin_Qty, Pin_Offset])
        bot_pin.snap.modifier(mod, 'count', -1, "Bottom_Pin_Qty", [Bottom_Pin_Qty])

        self.update()


class Robe_Hook_Accessories(Accessory):
    id_prompt = "sn_closets.accessories"

    def update(self):
        super().update()
        self.obj_bp["ID_PROMPT"] = self.id_prompt

    def draw(self):
        self.create_assembly()
        # we are adding a master hide for everything
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()

        self.add_prompts()
        self.add_prompt("Hook Qty", 'QUANTITY', 1)

        #SIZES OF STANDARD ACCESSORY PANELS
        self.add_prompt("Hook Offset",'DISTANCE', sn_unit.inch(2))

        width = self.obj_x.snap.get_var("location.x",'width')
        height = self.obj_z.snap.get_var("location.z",'height')
        depth = self.obj_y.snap.get_var("location.y",'depth')
        Hook_Qty = self.get_prompt("Hook Qty").get_var()
        Hook_Offset = self.get_prompt("Hook Offset").get_var()
        Custom_Rack_Style = self.get_prompt("Custom Rack Style").get_var()

        panel = common_parts.add_accessory_panel(self)
        panel.set_name('Accessory Cleat')
        panel.dim_x('width', [width])
        panel.dim_y('depth',[depth])
        panel.dim_z('height',[height])
        panel.get_prompt('Hide').set_formula('IF(Custom_Rack_Style==0,False,True) or Hide', [Custom_Rack_Style,self.hide_var])
        panel.cutpart("Panel")

        deco_panel = sn_types.Part(self.add_assembly_from_file(DECO_PANEL))
        self.add_assembly(deco_panel)
        deco_panel.set_name('Deco Accessory Cleat')
        deco_panel.dim_x('width', [width])
        deco_panel.dim_y('depth',[depth])
        deco_panel.dim_z('height',[height])
        deco_panel.get_prompt('Hide').set_formula('IF(Custom_Rack_Style==1,False,True) or Hide', [Custom_Rack_Style,self.hide_var])        
        deco_panel.cutpart("Panel")

        hook = self.add_object_from_file(ROBE_HOOK)
        hook.snap.mesh_type = 'HARDWARE'
        hook.snap.name_object = "Robe Hook"
        hook.snap.loc_x('Hook_Offset',[Hook_Offset])
        hook.snap.loc_y('depth', [depth])
        hook.snap.loc_z('height/2', [height])
        # hook.material("Chrome")
        mod = hook.modifiers.new('Quantity','ARRAY')
        mod.use_relative_offset = False
        mod.use_constant_offset = True

        hook.snap.modifier(
            mod, 'constant_offset_displace', 0,
            "width/Hook_Qty", [width, Hook_Qty])
        hook.snap.modifier(mod, 'count', -1, "Hook_Qty", [Hook_Qty])

        self.update()


class Double_Robe_Hook_Accessories(Accessory):
    id_prompt = "sn_closets.accessories"

    def update(self):
        super().update()
        self.obj_bp["ID_PROMPT"] = self.id_prompt

    def draw(self):
        self.create_assembly()
        # we are adding a master hide for everything
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()

        self.add_prompts()
        self.add_prompt("Hook Qty", 'QUANTITY', 1)

        #SIZES OF STANDARD ACCESSORY PANELS
        self.add_prompt("Hook Offset", 'DISTANCE', sn_unit.inch(2))

        width = self.obj_x.snap.get_var("location.x", 'width')
        height = self.obj_z.snap.get_var("location.z", 'height')
        depth = self.obj_y.snap.get_var("location.y", 'depth')
        Hook_Qty = self.get_prompt("Hook Qty").get_var()
        Hook_Offset = self.get_prompt("Hook Offset").get_var()
        Custom_Rack_Style = self.get_prompt("Custom Rack Style").get_var()

        panel = common_parts.add_accessory_panel(self)
        panel.set_name('Accessory Cleat')
        panel.dim_x('width', [width])
        panel.dim_y('depth', [depth])
        panel.dim_z('height', [height])
        panel.get_prompt('Hide').set_formula('IF(Custom_Rack_Style==0,False,True) or Hide', [Custom_Rack_Style,self.hide_var])
        panel.cutpart("Panel")

        deco_panel = sn_types.Part(self.add_assembly_from_file(DECO_PANEL))
        self.add_assembly(deco_panel)
        deco_panel.set_name('Deco Accessory Cleat')
        deco_panel.dim_x('width', [width])
        deco_panel.dim_y('depth', [depth])
        deco_panel.dim_z('height', [height])
        deco_panel.get_prompt('Hide').set_formula('IF(Custom_Rack_Style==1,False,True) or Hide', [Custom_Rack_Style,self.hide_var])        
        deco_panel.cutpart("Panel")

        hook = self.add_object_from_file(DOUBLE_ROBE_HOOK)
        hook.snap.mesh_type = 'HARDWARE'
        hook.snap.name_object = "Robe Hook"
        hook.snap.loc_x('Hook_Offset',[Hook_Offset])
        hook.snap.loc_y('depth', [depth])
        hook.snap.loc_z('height/2', [height])
        # hook.material("Chrome")
        mod = hook.modifiers.new('Quantity', 'ARRAY')
        mod.use_relative_offset = False
        mod.use_constant_offset = True

        hook.snap.modifier(
            mod, 'constant_offset_displace', 0,
            "width/Hook_Qty", [width, Hook_Qty])
        hook.snap.modifier(mod, 'count', -1, "Hook_Qty", [Hook_Qty])

        self.update()


class DORB_Hook_Accessories(Accessory):
    id_prompt = "sn_closets.accessories"

    def update(self):
        super().update()
        self.obj_bp["ID_PROMPT"] = self.id_prompt

    def draw(self):
        self.create_assembly()
        # we are adding a master hide for everything
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()

        self.add_prompts()
        self.add_prompt("Hook Qty", 'QUANTITY', 1)

        # SIZES OF STANDARD ACCESSORY PANELS
        self.add_prompt("Hook Offset", 'DISTANCE', sn_unit.inch(2))

        width = self.obj_x.snap.get_var("location.x", 'width')
        height = self.obj_z.snap.get_var("location.z", 'height')
        depth = self.obj_y.snap.get_var("location.y", 'depth')
        Hook_Qty = self.get_prompt("Hook Qty").get_var()
        Hook_Offset = self.get_prompt("Hook Offset").get_var()
        Custom_Rack_Style = self.get_prompt("Custom Rack Style").get_var()

        panel = common_parts.add_accessory_panel(self)
        panel.set_name('Accessory Cleat')
        panel.dim_x('width', [width])
        panel.dim_y('depth', [depth])
        panel.dim_z('height', [height])
        panel.get_prompt('Hide').set_formula('IF(Custom_Rack_Style==0,False,True) or Hide', [Custom_Rack_Style,self.hide_var])
        panel.cutpart("Panel")

        deco_panel = sn_types.Part(self.add_assembly_from_file(DECO_PANEL))
        self.add_assembly(deco_panel)
        deco_panel.set_name('Deco Accessory Cleat')
        deco_panel.dim_x('width', [width])
        deco_panel.dim_y('depth', [depth])
        deco_panel.dim_z('height', [height])
        deco_panel.get_prompt('Hide').set_formula('IF(Custom_Rack_Style==1,False,True) or Hide', [Custom_Rack_Style,self.hide_var])        
        deco_panel.cutpart("Panel")

        hook = self.add_object_from_file(DORB_HOOK)
        hook.snap.name_object = "Robe Hook"
        hook.snap.mesh_type = "Hardware"
        hook.snap.loc_x('Hook_Offset',[Hook_Offset])
        hook.snap.loc_y('depth', [depth])
        hook.snap.loc_z('height/2', [height])
        # hook.material("Chrome")
        mod = hook.modifiers.new('Quantity', 'ARRAY')
        mod.use_relative_offset = False
        mod.use_constant_offset = True

        hook.snap.modifier(
            mod, 'constant_offset_displace', 0,
            "width/Hook_Qty", [width, Hook_Qty])
        hook.snap.modifier(mod, 'count', -1, "Hook_Qty", [Hook_Qty])

        self.update()


class Coat_and_Hat_Hook_Accessories(Accessory):
    id_prompt = "sn_closets.accessories"

    def update(self):
        super().update()
        self.obj_bp["ID_PROMPT"] = self.id_prompt

    def draw(self):
        self.create_assembly()
        # we are adding a master hide for everything
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()

        self.add_prompts()
        self.add_prompt("Hook Qty", 'QUANTITY', 1)

        # SIZES OF STANDARD ACCESSORY PANELS
        self.add_prompt("Hook Offset", 'DISTANCE', sn_unit.inch(2))

        width = self.obj_x.snap.get_var("location.x", 'width')
        height = self.obj_z.snap.get_var("location.z", 'height')
        depth = self.obj_y.snap.get_var("location.y", 'depth')
        Hook_Qty = self.get_prompt("Hook Qty").get_var()
        Hook_Offset = self.get_prompt("Hook Offset").get_var()
        Custom_Rack_Style = self.get_prompt("Custom Rack Style").get_var()

        panel = common_parts.add_accessory_panel(self)
        panel.set_name('Accessory Cleat')
        panel.dim_x('width', [width])
        panel.dim_y('depth',[depth])
        panel.dim_z('height',[height])
        panel.get_prompt('Hide').set_formula('IF(Custom_Rack_Style==0,False,True) or Hide', [Custom_Rack_Style,self.hide_var])
        panel.cutpart("Panel")

        deco_panel = sn_types.Part(self.add_assembly_from_file(DECO_PANEL))
        self.add_assembly(deco_panel)
        deco_panel.set_name('Deco Accessory Cleat')
        deco_panel.dim_x('width', [width])
        deco_panel.dim_y('depth', [depth])
        deco_panel.dim_z('height', [height])
        deco_panel.get_prompt('Hide').set_formula('IF(Custom_Rack_Style==1,False,True) or Hide', [Custom_Rack_Style,self.hide_var])        
        deco_panel.cutpart("Panel")

        hook = self.add_object_from_file(COAT_AND_HAT_HOOK)
        hook.snap.mesh_type = 'HARDWARE'
        hook.name = "Robe Hook"
        hook.snap.loc_x('Hook_Offset', [Hook_Offset])
        hook.snap.loc_y('depth', [depth])
        hook.snap.loc_z('height/2', [height])
        # hook.material("Chrome")
        mod = hook.modifiers.new('Quantity', 'ARRAY')
        mod.use_relative_offset = False
        mod.use_constant_offset = True

        hook.snap.modifier(
            mod, 'constant_offset_displace', 0,
            "width/Hook_Qty", [width, Hook_Qty])
        hook.snap.modifier(mod, 'count', -1, "Hook_Qty", [Hook_Qty])

        self.update()


class OPERATOR_Place_Accessory(Operator, PlaceClosetInsert):
    bl_idname = "sn_closets.place_closet_accessory"
    bl_label = "Place Accessory"
    bl_description = "This allows you to place an accessory object into the scene."

    def execute(self, context):
        self.draw_asset()
        self.get_insert(context)

        if self.insert is None:
            bpy.ops.snap.message_box(
                'INVOKE_DEFAULT',
                message="Could Not Find Insert Class: " + self.object_name)
            return {'CANCELLED'}

        self.exclude_objects = sn_utils.get_child_objects(self.insert.obj_bp)
        self.set_wire_and_xray(self.insert.obj_bp, True)
        if self.header_text:
            context.area.header_text_set(text=self.header_text)
        context.view_layer.update()  # THE SCENE MUST BE UPDATED FOR RAY CAST TO WORK
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def accessory_drop(self, context, event):
        selected_point, selected_obj, _ = sn_utils.get_selection_point(
            context, event, exclude_objects=self.exclude_objects)
        bpy.ops.object.select_all(action='DESELECT')
        self.asset.obj_bp.location = selected_point
        self.asset.obj_bp.parent = None

        if selected_obj:
            wall_bp = sn_utils.get_wall_bp(selected_obj)
            selected_assembly_bp = sn_utils.get_assembly_bp(selected_obj)
            selected_assembly = sn_types.Assembly(selected_assembly_bp)

            if wall_bp:
                self.asset.obj_bp.parent = wall_bp
                loc_pos = wall_bp.matrix_world.inverted() @ selected_point
                self.asset.obj_bp.location = loc_pos
                self.asset.obj_bp.rotation_euler.z = 0
                self.asset.obj_bp.rotation_euler.y = 0
                self.asset.obj_bp.rotation_euler.x = 0

            if selected_assembly and selected_assembly.obj_bp:
                if "IS_BP_PANEL" in selected_assembly.obj_bp:
                    assy_world_loc = (
                        selected_assembly.obj_bp.matrix_world[0][3],
                        selected_assembly.obj_bp.matrix_world[1][3],
                        selected_assembly.obj_bp.matrix_world[2][3])

                    assy_z_world_loc = (
                        selected_assembly.obj_z.matrix_world[0][3],
                        selected_assembly.obj_z.matrix_world[1][3],
                        selected_assembly.obj_z.matrix_world[2][3])

                    dist_to_bp = math.fabs(sn_utils.calc_distance(selected_point, assy_world_loc))
                    dist_to_z = math.fabs(sn_utils.calc_distance(selected_point, assy_z_world_loc))
                    loc_pos = selected_assembly.obj_bp.matrix_world.inverted() @ selected_point
                    self.asset.obj_bp.parent = selected_assembly.obj_bp
                    self.asset.obj_bp.location.x = loc_pos[0]
                    self.asset.obj_bp.location.z = 0
                    self.asset.obj_x.location.x = math.fabs(selected_assembly.obj_y.location.y)  # SET DEPTH

                    if selected_assembly.obj_z.location.z < 0:  # LEFT PANEL
                        if dist_to_bp > dist_to_z:  # PLACE ON RIGHT SIDE
                            self.asset.obj_bp.location.y = selected_assembly.obj_y.location.y
                            self.asset.obj_bp.rotation_euler.x = math.radians(90)
                            self.asset.obj_bp.rotation_euler.y = math.radians(0)
                            self.asset.obj_bp.rotation_euler.z = math.radians(90)
                            self.asset.obj_bp.location.z = selected_assembly.obj_z.location.z
                        else:  # PLACE ON LEFT SIDE
                            self.asset.obj_bp.location.y = 0
                            self.asset.obj_bp.rotation_euler.x = math.radians(90)
                            self.asset.obj_bp.rotation_euler.y = math.radians(180)
                            self.asset.obj_bp.rotation_euler.z = math.radians(90)
                            self.asset.obj_bp.location.z = 0
                    else:  # CENTER AND RIGHT PANEL
                        if dist_to_bp > dist_to_z:  # PLACE ON LEFT SIDE
                            self.asset.obj_bp.location.y = 0
                            self.asset.obj_bp.rotation_euler.x = math.radians(90)
                            self.asset.obj_bp.rotation_euler.y = math.radians(180)
                            self.asset.obj_bp.rotation_euler.z = math.radians(90)
                            self.asset.obj_bp.location.z = selected_assembly.obj_z.location.z
                        else:  # PLACE ON RIGHT SIDE
                            self.asset.obj_bp.location.y = selected_assembly.obj_y.location.y
                            self.asset.obj_bp.rotation_euler.x = math.radians(90)
                            self.asset.obj_bp.rotation_euler.y = math.radians(0)
                            self.asset.obj_bp.rotation_euler.z = math.radians(90)
                            self.asset.obj_bp.location.z = 0

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            bpy.context.window.cursor_set('DEFAULT')
            bpy.ops.object.select_all(action='DESELECT')
            sn_utils.set_wireframe(self.asset.obj_bp, False)
            context.view_layer.objects.active = self.asset.obj_bp
            self.asset.obj_bp.select_set(True)
            obj = self.asset.obj_bp

            if obj and "ID_PROMPT" in obj and obj["ID_PROMPT"] != "":
                id_prompt = obj["ID_PROMPT"]
                eval("bpy.ops." + id_prompt + "('INVOKE_DEFAULT')")
            else:
                bpy.ops.sn_closets.accessories('INVOKE_DEFAULT')
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        bpy.ops.object.select_all(action='DESELECT')
        context.area.tag_redraw()
        context.area.header_text_set(text=self.header_text)
        self.reset_selection()

        if self.event_is_cancel_command(event):
            context.area.header_text_set(None)
            return self.cancel_drop(context)

        if self.event_is_pass_through(event):
            return {'PASS_THROUGH'}

        return self.accessory_drop(context, event)


class PROMPTS_Accessories(sn_types.Prompts_Interface):
    bl_idname = "sn_closets.accessories"
    bl_label = "Accessories"
    bl_options = {'UNDO'}

    object_name: StringProperty(name="Object Name",
                                description="Stores the Base Point Object Name"
                                            "so the object can be retrieved from the database.")

    width: FloatProperty(name="Width", unit='LENGTH', precision=4)
    height: FloatProperty(name="Height", unit='LENGTH', precision=4)
    depth: FloatProperty(name="Depth", unit='LENGTH', precision=4)

    plane: bpy.props.StringProperty(name="Plane", default="")  # noqa F722

    custom_rack_style: EnumProperty(
        name="Custom Rack Style",
        items=[
            ('0', 'Classic', 'Classic'),
            ('1', 'Deco', 'Deco')],
        default='0')

    product = None
    style_prompt = None

    def check(self, context):
        """ This is called everytime a change is made in the UI """
        if self.style_prompt:
            self.style_prompt.set_value(int(self.custom_rack_style))
        return True

    def set_properties_from_prompts(self):
        style = self.product.get_prompt("Custom Rack Style")
        if style:
            self.style_prompt = style

    def execute(self, context):
        """ This is called when the OK button is clicked """
        # self.update_product_size()
        return {'FINISHED'}

    def invoke(self, context, event):
        """ This is called before the interface is displayed """
        self.product = self.get_product()
        self.plane = self.get_plane()
        self.set_properties_from_prompts()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=sn_utils.get_prop_dialog_width(300))

    def draw(self, context):
        Style = self.product.get_prompt("Custom Rack Style")
        Hook_Qty = self.product.get_prompt("Hook Qty")
        Pin_Qty = self.product.get_prompt("Pin Qty")
        Top_Pin_Qty = self.product.get_prompt("Top Pin Qty")
        Bottom_Pin_Qty = self.product.get_prompt("Bottom Pin Qty")
        Hook_Offset = self.product.get_prompt("Hook Offset")
        Pin_Offset = self.product.get_prompt("Pin Offset")

        layout = self.layout
        box = layout.box()
        self.draw_product_position(box, self.plane)
        self.draw_product_rotation(box, self.plane)
        box.label(text=self.product.obj_bp.snap.name_object)
        box.prop(self.product.obj_x, 'location', index=0, text="Width")

        if Style:
            # Style.draw(box)  # TODO: combobox draw
            box.label(text="Custom Rack Style")
            box.prop(self, "custom_rack_style", expand=True)


        if Pin_Offset:
            Pin_Offset.draw(box, allow_edit=False)

        if Hook_Offset:
            Hook_Offset.draw(box, allow_edit=False)

        if Hook_Qty:
            Hook_Qty.draw(box, allow_edit=False)

        if Pin_Qty:
            Pin_Qty.draw(box, allow_edit=False)

        if Top_Pin_Qty:
            Top_Pin_Qty.draw(box, allow_edit=False)

        if Bottom_Pin_Qty:
            Bottom_Pin_Qty.draw(box, allow_edit=False)

    def get_plane(self):
        parent = self.product.obj_bp.parent
        if not parent:
            return ""
        obj = self.product.obj_bp
        z_rot = obj.rotation_euler.z
        if z_rot == 0:
            return "XZ"
        else:
            return "XY"


class PROMPTS_Belt_Rack_Prompts(sn_types.Prompts_Interface):
    bl_idname = "sn_closets.belt_rack"
    bl_label = "Belt Rack Prompts"
    bl_options = {'UNDO'}

    object_name: StringProperty(name="Object Name",
                                description="Stores the Base Point Object Name"
                                            "so the object can be retrieved from the database.")

    width: FloatProperty(name="Width", unit='LENGTH', precision=4)
    height: FloatProperty(name="Height", unit='LENGTH', precision=4)
    depth: FloatProperty(name="Depth", unit='LENGTH', precision=4)

    belt_rack_category: EnumProperty(
        name="Belt Rack Category",
        items=[
            ('0', 'Synergy', 'Synergy'),
            ('1', 'Elite', 'Elite')],
        default='0')

    synergy_belt_rack_length: EnumProperty(
        name="Belt Rack Length",
        items=[
            ('0', '12"', '12"'),
            ('1', '14"', '14"')],
        default='0')

    elite_belt_rack_length: EnumProperty(
        name="Belt Rack Length",
        items=[
            ('0', '12"', '12"'),
            ('1', '14"', '14"'),
            ('2', '18"', '18"')],
        default='0')

    metal_color: EnumProperty(
        name="Metal Color",
        items=[
            ('0', 'Chrome', 'Chrome'),
            ('1', 'Matte Aluminum', 'Matte Aluminum'),
            ('2', 'Matte Nickel', 'Matte Nickel'),
            ('3', 'Matte Gold', 'Matte Gold'),
            ('4', 'Orb?', 'Orb?'),
            ('5', 'Slate', 'Slate')],
        default='0')

    product = None

    def check(self, context):
        """ This is called everytime a change is made in the UI """
        self.set_prompts_from_properties()
        closet_props.update_render_materials(self, context)
        return True

    def execute(self, context):
        """ This is called when the OK button is clicked """
        # self.update_product_size()
        return {'FINISHED'}

    def invoke(self, context, event):
        """ This is called before the interface is displayed """
        self.product = self.get_product()
        self.set_properties_from_prompts()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=sn_utils.get_prop_dialog_width(300))

    def set_properties_from_prompts(self):
        belt_rack_category = self.product.get_prompt("Belt Rack Category")
        synergy_belt_rack_length = self.product.get_prompt("Synergy Belt Rack Length")
        elite_belt_rack_length = self.product.get_prompt("Elite Belt Rack Length")
        metal_color = self.product.get_prompt("Metal Color")

        if belt_rack_category:
            self.belt_rack_category = str(belt_rack_category.get_value())
        if synergy_belt_rack_length:
            self.synergy_belt_rack_length = str(synergy_belt_rack_length.get_value())
        if elite_belt_rack_length:
            self.elite_belt_rack_length = str(elite_belt_rack_length.get_value())
        if metal_color:
            if belt_rack_category.get_value() == 0:
                metal_color.set_value(0)
                self.metal_color = '0'
            else:
                self.metal_color = str(metal_color.get_value())

    def set_prompts_from_properties(self):
        belt_rack_category = self.product.get_prompt("Belt Rack Category")
        synergy_belt_rack_length = self.product.get_prompt("Synergy Belt Rack Length")
        elite_belt_rack_length = self.product.get_prompt("Elite Belt Rack Length")
        metal_color = self.product.get_prompt("Metal Color")

        if belt_rack_category:
            belt_rack_category.set_value(int(self.belt_rack_category))
        if synergy_belt_rack_length:
            synergy_belt_rack_length.set_value(int(self.synergy_belt_rack_length))
        if elite_belt_rack_length:
            elite_belt_rack_length.set_value(int(self.elite_belt_rack_length))
        if metal_color:
            if belt_rack_category.get_value() == 0:
                metal_color.set_value(0)
                self.metal_color = '0'
            else:
                metal_color.set_value(int(self.metal_color))

    def draw(self, context):
        layout = self.layout
        belt_rack_category = self.product.get_prompt("Belt Rack Category")
        synergy_belt_rack_length = self.product.get_prompt("Synergy Belt Rack Length")
        elite_belt_rack_length = self.product.get_prompt("Elite Belt Rack Length")
        metal_color = self.product.get_prompt("Metal Color")

        row = layout.row()
        row.label(text="Location")
        row.prop(self.product.obj_bp, 'location', index=0, text="")

        if belt_rack_category:
            row = layout.row()
            row.label(text="Category")
            row.prop(self, 'belt_rack_category', expand=True)

        if belt_rack_category:
            if belt_rack_category.get_value() == 1:
                if elite_belt_rack_length:
                    row = layout.row()
                    row.label(text="Length")
                    row.prop(self, 'elite_belt_rack_length', expand=True)

                if metal_color:
                    row = layout.row()
                    row.label(text="Metal Color")
                    row.prop(self, 'metal_color', text='')
            else:
                if synergy_belt_rack_length:
                    row = layout.row()
                    row.label(text="Length")
                    row.prop(self, 'synergy_belt_rack_length', expand=True)


class PROMPTS_Tie_Rack_Prompts(sn_types.Prompts_Interface):
    bl_idname = "sn_closets.tie_rack"
    bl_label = "Tie Rack Prompts"
    bl_options = {'UNDO'}

    object_name: StringProperty(name="Object Name",
                                description="Stores the Base Point Object Name"
                                            "so the object can be retrieved from the database.")

    width: FloatProperty(name="Width", unit='LENGTH', precision=4)
    height: FloatProperty(name="Height", unit='LENGTH', precision=4)
    depth: FloatProperty(name="Depth", unit='LENGTH', precision=4)

    tie_rack_category: EnumProperty(
        name="Tie Rack Category",
        items=[
            ('0', 'Synergy', 'Synergy'),
            ('1', 'Elite', 'Elite')],
        default='0')

    synergy_tie_rack_length: EnumProperty(
        name="Synergy Tie Rack Length",
        items=[
            ('0', '12"', '12"'),
            ('1', '14"', '14"')],
        default='0')

    elite_tie_rack_length: EnumProperty(
        name="Elite Tie Rack Length",
        items=[
            ('0', '12"', '12"'),
            ('1', '14"', '14"'),
            ('2', '18"', '18"')],
        default='0')

    metal_color: EnumProperty(
        name="Metal Color",
        items=[
            ('0', 'Chrome', 'Chrome'),
            ('1', 'Matte Aluminum', 'Matte Aluminum'),
            ('2', 'Matte Nickel', 'Matte Nickel'),
            ('3', 'Matte Gold', 'Matte Gold'),
            ('4', 'Orb?', 'Orb?'),
            ('5', 'Slate', 'Slate')],
        default='0')

    product = None

    def check(self, context):
        """ This is called everytime a change is made in the UI """
        self.set_prompts_from_properties()
        closet_props.update_render_materials(self, context)
        return True

    def execute(self, context):
        """ This is called when the OK button is clicked """
        # self.update_product_size()
        return {'FINISHED'}

    def invoke(self, context, event):
        """ This is called before the interface is displayed """
        self.product = self.get_product()
        self.set_properties_from_prompts()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=sn_utils.get_prop_dialog_width(300))

    def set_properties_from_prompts(self):
        tie_rack_category = self.product.get_prompt("Tie Rack Category")
        synergy_tie_rack_length = self.product.get_prompt("Synergy Tie Rack Length")
        elite_tie_rack_length = self.product.get_prompt("Elite Tie Rack Length")
        metal_color = self.product.get_prompt("Metal Color")

        if tie_rack_category:
            self.tie_rack_category = str(tie_rack_category.get_value())
        if synergy_tie_rack_length:
            self.synergy_tie_rack_length = str(synergy_tie_rack_length.get_value())
        if elite_tie_rack_length:
            self.elite_tie_rack_length = str(elite_tie_rack_length.get_value())
        if metal_color:
            if tie_rack_category.get_value() == 0:
                metal_color.set_value(0)
                self.metal_color = '0'
            else:
                self.metal_color = str(metal_color.get_value())

    def set_prompts_from_properties(self):
        tie_rack_category = self.product.get_prompt("Tie Rack Category")
        synergy_tie_rack_length = self.product.get_prompt("Synergy Tie Rack Length")
        elite_tie_rack_length = self.product.get_prompt("Elite Tie Rack Length")
        metal_color = self.product.get_prompt("Metal Color")

        if tie_rack_category:
            tie_rack_category.set_value(int(self.tie_rack_category))
        if synergy_tie_rack_length:
            synergy_tie_rack_length.set_value(int(self.synergy_tie_rack_length))
        if elite_tie_rack_length:
            elite_tie_rack_length.set_value(int(self.elite_tie_rack_length))
        if metal_color:
            if tie_rack_category.get_value() == 0:
                metal_color.set_value(0)
                self.metal_color = '0'
            else:
                metal_color.set_value(int(self.metal_color))

    def draw(self, context):
        layout = self.layout
        tie_rack_category = self.product.get_prompt("Tie Rack Category")
        synergy_tie_rack_length = self.product.get_prompt("Synergy Tie Rack Length")
        elite_tie_rack_length = self.product.get_prompt("Elite Tie Rack Length")
        metal_color = self.product.get_prompt("Metal Color")

        row = layout.row()
        row.label(text="Location")
        row.prop(self.product.obj_bp, 'location', index=0, text="")

        if tie_rack_category:
            row = layout.row()
            row.label(text="Category")
            row.prop(self, 'tie_rack_category', expand=True)

        if tie_rack_category:
            if tie_rack_category.get_value() == 1:
                if elite_tie_rack_length:
                    row = layout.row()
                    row.label(text="Length")
                    row.prop(self, 'elite_tie_rack_length', expand=True)

                if metal_color:
                    row = layout.row()
                    row.label(text="Metal Color")
                    row.prop(self, 'metal_color', text='')
            else:
                if synergy_tie_rack_length:
                    row = layout.row()
                    row.label(text="Length")
                    row.prop(self, 'synergy_tie_rack_length', expand=True)


bpy.utils.register_class(OPERATOR_Place_Accessory)
bpy.utils.register_class(PROMPTS_Accessories)
bpy.utils.register_class(PROMPTS_Belt_Rack_Prompts)
bpy.utils.register_class(PROMPTS_Tie_Rack_Prompts)
