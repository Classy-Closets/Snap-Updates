import bpy
from . import mv_closet_defaults as props_closet
from mv import fd_types, utils, unit
from os import path
import math
from . import common_parts

PATH = path.join(path.dirname(__file__),"Closet Assemblies")
OBJECT_PATH = path.join(path.dirname(__file__),"Objects")
PEG_OBJECT = path.join(OBJECT_PATH,"Peg Object.blend")
ROBE_HOOK = path.join(OBJECT_PATH,"Robe Hook.blend")
DORB_HOOK = path.join(OBJECT_PATH,"DORB Hook.blend")
COAT_AND_HAT_HOOK = path.join(OBJECT_PATH,"Coat and Hat Hook.blend")
DOUBLE_ROBE_HOOK = path.join(OBJECT_PATH,"Double Robe Hook.blend")
DECO_PANEL = path.join(PATH,"Deco Panel.blend")
#-----------Valet Rod
VALET_ROD = path.join(OBJECT_PATH,"Valet Rod","Valet Rod.blend")
VALET_ROD2 = path.join(OBJECT_PATH,"Valet Rod2.blend")


class Belt_Accessories(fd_types.Assembly):

    type_assembly = "PRODUCT"
    
    drop_id = props_closet.LIBRARY_NAME_SPACE + ".place_closet_accessory"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".accessories"

    def draw(self):
        self.create_assembly()
        
        self.add_tab(name='Main Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        self.add_prompt(name="Custom Rack Style",
                        prompt_type='COMBOBOX',
                        items=["Classic","Deco"],
                        value=0,
                        tab_index=0)
        
        self.add_prompt(name="Add Slide",
                        prompt_type='CHECKBOX',
                        value = True,
                        tab_index=0)
        
        self.add_prompt(name="Hook Type",
                        prompt_type='TEXT',
                        value = "BRK",
                        tab_index=0)
        
        self.add_prompt(name="Pin Qty",
                        prompt_type='QUANTITY',
                        value=11,
                        tab_index=0)        
        
        #SIZES OF STANDARD ACCESSORY PANELS 
        
        self.add_prompt(name="Pin Length",
                        prompt_type='DISTANCE',
                        value = unit.inch(1.5),
                        tab_index=1) 
        
        self.add_prompt(name="Pin Offset",
                        prompt_type='DISTANCE',
                        value = unit.inch(.75),
                        tab_index=1)                                               
        
        width = self.get_var("dim_x",'width')
        height = self.get_var("dim_z",'height')
        depth = self.get_var("dim_y",'depth')
        Pin_Offset = self.get_var("Pin Offset")
        Pin_Qty = self.get_var("Pin Qty")
        Custom_Rack_Style = self.get_var("Custom Rack Style")

        World_Z = self.get_var('world_loc_z','World_Z',transform_type='LOC_Z')
        accessory_height_dim = fd_types.Dimension()
        accessory_height_dim.anchor.parent = self.obj_bp
        accessory_height_dim.start_x(value = 0)
        accessory_height_dim.start_y(value = 0)
        accessory_height_dim.start_z(value = 0)
        accessory_height_dim.end_z('-World_Z',[World_Z])
        
        panel = common_parts.add_accessory_panel(self)
        panel.set_name('Accessory Rack')
        panel.x_dim('width', [width])
        panel.y_dim('depth',[depth])
        panel.z_dim('height',[height])        
        panel.x_loc(value = 0)
        panel.y_loc(value = 0)
        panel.z_loc(value = 0)
        panel.x_rot(value = 0)
        panel.y_rot(value = 0)
        panel.z_rot(value = 0)
        panel.prompt('Hide', 'IF(Custom_Rack_Style==0,False,True)', [Custom_Rack_Style])
        panel.cutpart("Panel")
        
        deco_panel = self.add_assembly(DECO_PANEL)
        deco_panel.set_name('Deco Accessory Rack')
        deco_panel.x_dim('width', [width])
        deco_panel.y_dim('depth',[depth])
        deco_panel.z_dim('height',[height])        
        deco_panel.x_loc(value = 0)
        deco_panel.y_loc(value = 0)
        deco_panel.z_loc(value = 0)
        deco_panel.x_rot(value = 0)
        deco_panel.y_rot(value = 0)
        deco_panel.z_rot(value = 0)
        deco_panel.prompt('Hide', 'IF(Custom_Rack_Style==1,False,True)', [Custom_Rack_Style])
        deco_panel.cutpart("Panel")
        
        pin = self.add_object(PEG_OBJECT)
        pin.set_name('Accessory Pin')        
        pin.x_loc('Pin_Offset',[Pin_Offset])
        pin.y_loc('depth/2', [depth])
        pin.z_loc('height/2', [height])
        pin.x_rot(value = 0)
        pin.y_rot(value = 0)
        pin.z_rot(value = 0)
        pin.material("Chrome")
        mod = pin.obj.modifiers.new('Quantity','ARRAY')
        mod.use_relative_offset = False
        mod.use_constant_offset = True
        
        offset_driver = pin.obj.driver_add('modifiers["Quantity"].constant_offset_displace',0)
        utils.add_variables_to_driver(offset_driver,[width,Pin_Qty,Pin_Offset])
        offset_driver.driver.expression = "(width-Pin_Offset)/Pin_Qty"
        
        count_driver = pin.obj.driver_add('modifiers["Quantity"].count')
        utils.add_variables_to_driver(count_driver,[Pin_Qty])
        count_driver.driver.expression = "Pin_Qty"
        
        
class Tie_Accessories(fd_types.Assembly):
 
    type_assembly = "PRODUCT"
    
    drop_id = props_closet.LIBRARY_NAME_SPACE + ".place_closet_accessory"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".accessories"

    def draw(self):
        self.create_assembly()
        
        self.add_tab(name='Main Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        self.add_prompt(name="Custom Rack Style",
                        prompt_type='COMBOBOX',
                        items=["Classic","Deco"],
                        value=0,
                        tab_index=0)
        
        self.add_prompt(name="Add Slide",
                        prompt_type='CHECKBOX',
                        value = True,
                        tab_index=0)
        
        self.add_prompt(name="Hook Type",
                        prompt_type='TEXT',
                        value = "BRK",
                        tab_index=0)
        
        self.add_prompt(name="Top Pin Qty",
                        prompt_type='QUANTITY',
                        value=12,
                        tab_index=0) 
        
        self.add_prompt(name="Bottom Pin Qty",
                        prompt_type='QUANTITY',
                        value=11,
                        tab_index=0)               
        
        #SIZES OF STANDARD ACCESSORY PANELS
         
        self.add_prompt(name="Pin Length",
                        prompt_type='DISTANCE',
                        value = unit.inch(1.5),
                        tab_index=1) 
        
        self.add_prompt(name="Pin Offset",
                        prompt_type='DISTANCE',
                        value = unit.inch(.75),
                        tab_index=1)                                               
        
        width = self.get_var("dim_x",'width')
        height = self.get_var("dim_z",'height')
        depth = self.get_var("dim_y",'depth')
        Pin_Offset = self.get_var("Pin Offset")
        Top_Pin_Qty = self.get_var("Top Pin Qty")
        Bottom_Pin_Qty = self.get_var("Bottom Pin Qty")
        Custom_Rack_Style = self.get_var("Custom Rack Style")

        World_Z = self.get_var('world_loc_z','World_Z',transform_type='LOC_Z')
        accessory_height_dim = fd_types.Dimension()
        accessory_height_dim.anchor.parent = self.obj_bp
        accessory_height_dim.start_x(value = 0)
        accessory_height_dim.start_y(value = 0)
        accessory_height_dim.start_z(value = 0)
        accessory_height_dim.end_z('-World_Z',[World_Z])
        
        panel = common_parts.add_accessory_panel(self)
        panel.set_name('Accessory Rack')
        panel.x_dim('width', [width])
        panel.y_dim('depth',[depth])
        panel.z_dim('height',[height])        
        panel.x_loc(value = 0)
        panel.y_loc(value = 0)
        panel.z_loc(value = 0)
        panel.x_rot(value = 0)
        panel.y_rot(value = 0)
        panel.z_rot(value = 0)
        panel.prompt('Hide', 'IF(Custom_Rack_Style==0,False,True)', [Custom_Rack_Style])
        panel.cutpart("Panel")
        
        deco_panel = self.add_assembly(DECO_PANEL)
        deco_panel.set_name('Deco Accessory Rack')
        deco_panel.x_dim('width', [width])
        deco_panel.y_dim('depth',[depth])
        deco_panel.z_dim('height',[height])        
        deco_panel.x_loc(value = 0)
        deco_panel.y_loc(value = 0)
        deco_panel.z_loc(value = 0)
        deco_panel.x_rot(value = 0)
        deco_panel.y_rot(value = 0)
        deco_panel.z_rot(value = 0)
        deco_panel.prompt('Hide', 'IF(Custom_Rack_Style==1,False,True)', [Custom_Rack_Style]) 
        deco_panel.cutpart("Panel")
        
        top_pin = self.add_object(PEG_OBJECT)
        top_pin.set_name('Accessory Pin')        
        top_pin.x_loc('Pin_Offset',[Pin_Offset])
        top_pin.y_loc('depth/2', [depth])
        top_pin.z_loc('height/1.5', [height])
        top_pin.x_rot(value = 0)
        top_pin.y_rot(value = 0)
        top_pin.z_rot(value = 0)
        top_pin.material("Chrome")
        mod = top_pin.obj.modifiers.new('Quantity','ARRAY')
        mod.use_relative_offset = False
        mod.use_constant_offset = True
        offset_driver = top_pin.obj.driver_add('modifiers["Quantity"].constant_offset_displace',0)
        utils.add_variables_to_driver(offset_driver,[width,Top_Pin_Qty,Pin_Offset])
        offset_driver.driver.expression = "(width-Pin_Offset)/Top_Pin_Qty"
        
        count_driver = top_pin.obj.driver_add('modifiers["Quantity"].count')
        utils.add_variables_to_driver(count_driver,[Top_Pin_Qty])
        count_driver.driver.expression = "Top_Pin_Qty"
        
        bot_pin = self.add_object(PEG_OBJECT)
        bot_pin.set_name('Accessory Pin')        
        bot_pin.x_loc('Pin_Offset*1.5',[Pin_Offset])
        bot_pin.y_loc('depth/2', [depth])
        bot_pin.z_loc('height/3', [height])
        bot_pin.x_rot(value = 0)
        bot_pin.y_rot(value = 0)
        bot_pin.z_rot(value = 0)
        bot_pin.material("Chrome")
        mod = bot_pin.obj.modifiers.new('Quantity','ARRAY')
        mod.use_relative_offset = False
        mod.use_constant_offset = True
        offset_driver = bot_pin.obj.driver_add('modifiers["Quantity"].constant_offset_displace',0)
        utils.add_variables_to_driver(offset_driver,[width,Bottom_Pin_Qty,Pin_Offset])
        offset_driver.driver.expression = "(width-(Pin_Offset*2))/Bottom_Pin_Qty"
        
        count_driver = bot_pin.obj.driver_add('modifiers["Quantity"].count')
        utils.add_variables_to_driver(count_driver,[Bottom_Pin_Qty])
        count_driver.driver.expression = "Bottom_Pin_Qty"
           
 
class Tie_and_Belt_Accessories(fd_types.Assembly):

    type_assembly = "PRODUCT"
    
    drop_id = props_closet.LIBRARY_NAME_SPACE + ".place_closet_accessory"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".accessories"

    def draw(self):
        self.create_assembly()
        
        self.add_tab(name='Main Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        self.add_prompt(name="Custom Rack Style",
                        prompt_type='COMBOBOX',
                        items=["Classic","Deco"],
                        value=0,
                        tab_index=0)
        
        self.add_prompt(name="Add Slide",
                        prompt_type='CHECKBOX',
                        value = True,
                        tab_index=0)
        
        self.add_prompt(name="Hook Type",
                        prompt_type='TEXT',
                        value = "BRK",
                        tab_index=0)
        
        self.add_prompt(name="Top Pin Qty",
                        prompt_type='QUANTITY',
                        value=5,
                        tab_index=0) 
        
        self.add_prompt(name="Bottom Pin Qty",
                        prompt_type='QUANTITY',
                        value=11,
                        tab_index=0)         
        
        #SIZES OF STANDARD ACCESSORY PANELS
        
        self.add_prompt(name="Pin Length",
                        prompt_type='DISTANCE',
                        value = unit.inch(1.5),
                        tab_index=1) 
        
        self.add_prompt(name="Pin Offset",
                        prompt_type='DISTANCE',
                        value = unit.inch(.75),
                        tab_index=1)                                               
        
        width = self.get_var("dim_x",'width')
        height = self.get_var("dim_z",'height')
        depth = self.get_var("dim_y",'depth')
        Top_Pin_Qty = self.get_var("Top Pin Qty")
        Bottom_Pin_Qty = self.get_var("Bottom Pin Qty")
        Pin_Offset = self.get_var("Pin Offset")
        Custom_Rack_Style = self.get_var("Custom Rack Style")

        World_Z = self.get_var('world_loc_z','World_Z',transform_type='LOC_Z')
        accessory_height_dim = fd_types.Dimension()
        accessory_height_dim.anchor.parent = self.obj_bp
        accessory_height_dim.start_x(value = 0)
        accessory_height_dim.start_y(value = 0)
        accessory_height_dim.start_z(value = 0)
        accessory_height_dim.end_z('-World_Z',[World_Z])
        
        panel = common_parts.add_accessory_panel(self)
        panel.set_name('Accessory Rack')
        panel.x_dim('width', [width])
        panel.y_dim('depth',[depth])
        panel.z_dim('height',[height])        
        panel.x_loc(value = 0)
        panel.y_loc(value = 0)
        panel.z_loc(value = 0)
        panel.x_rot(value = 0)
        panel.y_rot(value = 0)
        panel.z_rot(value = 0)
        panel.prompt('Hide', 'IF(Custom_Rack_Style==0,False,True)', [Custom_Rack_Style])
        panel.cutpart("Panel")
        
        deco_panel = self.add_assembly(DECO_PANEL)
        deco_panel.set_name('Deco Accessory Rack')
        deco_panel.x_dim('width', [width])
        deco_panel.y_dim('depth',[depth])
        deco_panel.z_dim('height',[height])        
        deco_panel.x_loc(value = 0)
        deco_panel.y_loc(value = 0)
        deco_panel.z_loc(value = 0)
        deco_panel.x_rot(value = 0)
        deco_panel.y_rot(value = 0)
        deco_panel.z_rot(value = 0)
        deco_panel.prompt('Hide', 'IF(Custom_Rack_Style==1,False,True)', [Custom_Rack_Style])        
        deco_panel.cutpart("Panel")
        
        top_pin = self.add_object(PEG_OBJECT)
        top_pin.set_name('Accessory Pin')        
        top_pin.x_loc('Pin_Offset',[Pin_Offset])
        top_pin.y_loc('depth/2', [depth])
        top_pin.z_loc('height/1.5', [height])
        top_pin.x_rot(value = 0)
        top_pin.y_rot(value = 0)
        top_pin.z_rot(value = 0)
        top_pin.material('Chrome')
        mod = top_pin.obj.modifiers.new('Quantity','ARRAY')
        mod.use_relative_offset = False
        mod.use_constant_offset = True
        offset_driver = top_pin.obj.driver_add('modifiers["Quantity"].constant_offset_displace',0)
        utils.add_variables_to_driver(offset_driver,[width,Top_Pin_Qty,Pin_Offset])
        offset_driver.driver.expression = "((width/2)-Pin_Offset)/Top_Pin_Qty"
        
        count_driver = top_pin.obj.driver_add('modifiers["Quantity"].count')
        utils.add_variables_to_driver(count_driver,[Top_Pin_Qty])
        count_driver.driver.expression = "Top_Pin_Qty"
        
        bot_pin = self.add_object(PEG_OBJECT)
        bot_pin.set_name('Accessory Pin')        
        bot_pin.x_loc('Pin_Offset*2',[Pin_Offset])
        bot_pin.y_loc('depth/2', [depth])
        bot_pin.z_loc('height/3', [height])
        bot_pin.x_rot(value = 0)
        bot_pin.y_rot(value = 0)
        bot_pin.z_rot(value = 0)
        bot_pin.material('Chrome')
        mod = bot_pin.obj.modifiers.new('Quantity','ARRAY')
        mod.use_relative_offset = False
        mod.use_constant_offset = True
        offset_driver = bot_pin.obj.driver_add('modifiers["Quantity"].constant_offset_displace',0)
        utils.add_variables_to_driver(offset_driver,[width,Bottom_Pin_Qty,Pin_Offset])
        offset_driver.driver.expression = "(width-(Pin_Offset*2.5))/Bottom_Pin_Qty"

        count_driver = bot_pin.obj.driver_add('modifiers["Quantity"].count')
        utils.add_variables_to_driver(count_driver,[Bottom_Pin_Qty])
        count_driver.driver.expression = "Bottom_Pin_Qty"        

               
class Robe_Hook_Accessories(fd_types.Assembly):
 
    type_assembly = "PRODUCT"
    
    drop_id = props_closet.LIBRARY_NAME_SPACE + ".place_closet_accessory"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".accessories"

    def draw(self):
        self.create_assembly()
        
        self.add_tab(name='Main Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        self.add_prompt(name="Custom Rack Style",
                        prompt_type='COMBOBOX',
                        items=["Classic","Deco"],
                        value=0,
                        tab_index=0)
        
        self.add_prompt(name="Add Slide",
                        prompt_type='CHECKBOX',
                        value = True,
                        tab_index=0)
        
        self.add_prompt(name="Hook Type",
                        prompt_type='TEXT',
                        value = "BRK",
                        tab_index=0)
        
        self.add_prompt(name="Hook Qty",
                        prompt_type='QUANTITY',
                        value=1,
                        tab_index=0)        
        
        #SIZES OF STANDARD ACCESSORY PANELS
        
        self.add_prompt(name="Hook Offset",
                        prompt_type='DISTANCE',
                        value = unit.inch(2),
                        tab_index=1)                                               
        
        width = self.get_var("dim_x",'width')
        height = self.get_var("dim_z",'height')
        depth = self.get_var("dim_y",'depth')
        Hook_Qty = self.get_var("Hook Qty")
        Hook_Offset = self.get_var("Hook Offset")
        Custom_Rack_Style = self.get_var("Custom Rack Style")

        World_Z = self.get_var('world_loc_z','World_Z',transform_type='LOC_Z')
        accessory_height_dim = fd_types.Dimension()
        accessory_height_dim.anchor.parent = self.obj_bp
        accessory_height_dim.start_x(value = 0)
        accessory_height_dim.start_y(value = 0)
        accessory_height_dim.start_z(value = 0)
        accessory_height_dim.end_z('-World_Z',[World_Z])
        
        panel = common_parts.add_accessory_panel(self)
        panel.set_name('Accessory Rack')
        panel.x_dim('width', [width])
        panel.y_dim('depth',[depth])
        panel.z_dim('height',[height])        
        panel.x_loc(value = 0)
        panel.y_loc(value = 0)
        panel.z_loc(value = 0)
        panel.x_rot(value = 0)
        panel.y_rot(value = 0)
        panel.z_rot(value = 0)
        panel.prompt('Hide', 'IF(Custom_Rack_Style==0,False,True)', [Custom_Rack_Style])
        panel.cutpart("Panel")
        
        deco_panel = self.add_assembly(DECO_PANEL)
        deco_panel.set_name('Deco Accessory Rack')
        deco_panel.x_dim('width', [width])
        deco_panel.y_dim('depth',[depth])
        deco_panel.z_dim('height',[height])        
        deco_panel.x_loc(value = 0)
        deco_panel.y_loc(value = 0)
        deco_panel.z_loc(value = 0)
        deco_panel.x_rot(value = 0)
        deco_panel.y_rot(value = 0)
        deco_panel.z_rot(value = 0)
        deco_panel.prompt('Hide', 'IF(Custom_Rack_Style==1,False,True)', [Custom_Rack_Style])        
        deco_panel.cutpart("Panel")
        
        hook = self.add_object(ROBE_HOOK)
        hook.set_name('Robe Hook')        
        hook.x_loc('Hook_Offset',[Hook_Offset])
        hook.y_loc('depth', [depth])
        hook.z_loc('height/2', [height])
        hook.x_rot(value = 0)
        hook.y_rot(value = 0)
        hook.z_rot(value = 0)
        hook.material("Chrome")
        mod = hook.obj.modifiers.new('Quantity','ARRAY')
        mod.use_relative_offset = False
        mod.use_constant_offset = True
        offset_driver = hook.obj.driver_add('modifiers["Quantity"].constant_offset_displace',0)
        utils.add_variables_to_driver(offset_driver,[width,Hook_Qty,Hook_Offset])
        offset_driver.driver.expression = "width/Hook_Qty"
        
        count_driver = hook.obj.driver_add('modifiers["Quantity"].count')
        utils.add_variables_to_driver(count_driver,[Hook_Qty])
        count_driver.driver.expression = "Hook_Qty"
        
         
class Double_Robe_Hook_Accessories(fd_types.Assembly):

    type_assembly = "PRODUCT"
    
    drop_id = props_closet.LIBRARY_NAME_SPACE + ".place_closet_accessory"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".accessories"

    def draw(self):
        self.create_assembly()
        
        self.add_tab(name='Main Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        self.add_prompt(name="Custom Rack Style",
                        prompt_type='COMBOBOX',
                        items=["Classic","Deco"],
                        value=0,
                        tab_index=0)
        
        self.add_prompt(name="Add Slide",
                        prompt_type='CHECKBOX',
                        value = True,
                        tab_index=0)
        
        self.add_prompt(name="Hook Type",
                        prompt_type='TEXT',
                        value = "BRK",
                        tab_index=0)

        self.add_prompt(name="Hook Qty",
                        prompt_type='QUANTITY',
                        value=1,
                        tab_index=0)        
        
        #SIZES OF STANDARD ACCESSORY PANELS
        
        self.add_prompt(name="Hook Offset",
                        prompt_type='DISTANCE',
                        value = unit.inch(2),
                        tab_index=1)                                                   
        
        width = self.get_var("dim_x",'width')
        height = self.get_var("dim_z",'height')
        depth = self.get_var("dim_y",'depth')
        Hook_Qty = self.get_var("Hook Qty")
        Hook_Offset = self.get_var("Hook Offset")
        Custom_Rack_Style = self.get_var("Custom Rack Style")

        World_Z = self.get_var('world_loc_z','World_Z',transform_type='LOC_Z')
        accessory_height_dim = fd_types.Dimension()
        accessory_height_dim.anchor.parent = self.obj_bp
        accessory_height_dim.start_x(value = 0)
        accessory_height_dim.start_y(value = 0)
        accessory_height_dim.start_z(value = 0)
        accessory_height_dim.end_z('-World_Z',[World_Z])
        
        panel = common_parts.add_accessory_panel(self)
        panel.set_name('Accessory Rack')
        panel.x_dim('width', [width])
        panel.y_dim('depth',[depth])
        panel.z_dim('height',[height])        
        panel.x_loc(value = 0)
        panel.y_loc(value = 0)
        panel.z_loc(value = 0)
        panel.x_rot(value = 0)
        panel.y_rot(value = 0)
        panel.z_rot(value = 0)
        panel.prompt('Hide', 'IF(Custom_Rack_Style==0,False,True)', [Custom_Rack_Style])
        panel.cutpart("Panel")
        
        deco_panel = self.add_assembly(DECO_PANEL)
        deco_panel.set_name('Deco Accessory Rack')
        deco_panel.x_dim('width', [width])
        deco_panel.y_dim('depth',[depth])
        deco_panel.z_dim('height',[height])        
        deco_panel.x_loc(value = 0)
        deco_panel.y_loc(value = 0)
        deco_panel.z_loc(value = 0)
        deco_panel.x_rot(value = 0)
        deco_panel.y_rot(value = 0)
        deco_panel.z_rot(value = 0)
        deco_panel.prompt('Hide', 'IF(Custom_Rack_Style==1,False,True)', [Custom_Rack_Style])        
        deco_panel.cutpart("Panel")
        
        hook = self.add_object(DOUBLE_ROBE_HOOK)
        hook.set_name('Robe Hook')        
        hook.x_loc('Hook_Offset',[Hook_Offset])
        hook.y_loc('depth', [depth])
        hook.z_loc('height/2', [height])
        hook.x_rot(value = 0)
        hook.y_rot(value = 0)
        hook.z_rot(value = 0)
        hook.material("Chrome")
        mod = hook.obj.modifiers.new('Quantity','ARRAY')
        mod.use_relative_offset = False
        mod.use_constant_offset = True
        offset_driver = hook.obj.driver_add('modifiers["Quantity"].constant_offset_displace',0)
        utils.add_variables_to_driver(offset_driver,[width,Hook_Qty,Hook_Offset])
        offset_driver.driver.expression = "width/Hook_Qty"
        
        count_driver = hook.obj.driver_add('modifiers["Quantity"].count')
        utils.add_variables_to_driver(count_driver,[Hook_Qty])
        count_driver.driver.expression = "Hook_Qty"        
         
         
class DORB_Hook_Accessories(fd_types.Assembly):
 
    type_assembly = "PRODUCT"
    
    drop_id = props_closet.LIBRARY_NAME_SPACE + ".place_closet_accessory"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".accessories"

    def draw(self):
        self.create_assembly()
        
        self.add_tab(name='Main Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        self.add_prompt(name="Custom Rack Style",
                        prompt_type='COMBOBOX',
                        items=["Classic","Deco"],
                        value=0,
                        tab_index=0)
        
        self.add_prompt(name="Add Slide",
                        prompt_type='CHECKBOX',
                        value = True,
                        tab_index=0)
        
        self.add_prompt(name="Hook Type",
                        prompt_type='TEXT',
                        value = "BRK",
                        tab_index=0)
             
        self.add_prompt(name="Hook Qty",
                        prompt_type='QUANTITY',
                        value=1,
                        tab_index=0)        
        
        #SIZES OF STANDARD ACCESSORY PANELS
        
        self.add_prompt(name="Hook Offset",
                        prompt_type='DISTANCE',
                        value = unit.inch(2),
                        tab_index=1)                                                   
        
        width = self.get_var("dim_x",'width')
        height = self.get_var("dim_z",'height')
        depth = self.get_var("dim_y",'depth')
        Hook_Qty = self.get_var("Hook Qty")
        Hook_Offset = self.get_var("Hook Offset")
        Custom_Rack_Style = self.get_var("Custom Rack Style")


        World_Z = self.get_var('world_loc_z','World_Z',transform_type='LOC_Z')
        accessory_height_dim = fd_types.Dimension()
        accessory_height_dim.anchor.parent = self.obj_bp
        accessory_height_dim.start_x(value = 0)
        accessory_height_dim.start_y(value = 0)
        accessory_height_dim.start_z(value = 0)
        accessory_height_dim.end_z('-World_Z',[World_Z])
        
        panel = common_parts.add_accessory_panel(self)
        panel.set_name('Accessory Rack')
        panel.x_dim('width', [width])
        panel.y_dim('depth',[depth])
        panel.z_dim('height',[height])        
        panel.x_loc(value = 0)
        panel.y_loc(value = 0)
        panel.z_loc(value = 0)
        panel.x_rot(value = 0)
        panel.y_rot(value = 0)
        panel.z_rot(value = 0)
        panel.prompt('Hide', 'IF(Custom_Rack_Style==0,False,True)', [Custom_Rack_Style])
        panel.cutpart("Panel")
        
        deco_panel = self.add_assembly(DECO_PANEL)
        deco_panel.set_name('Deco Accessory Rack')
        deco_panel.x_dim('width', [width])
        deco_panel.y_dim('depth',[depth])
        deco_panel.z_dim('height',[height])        
        deco_panel.x_loc(value = 0)
        deco_panel.y_loc(value = 0)
        deco_panel.z_loc(value = 0)
        deco_panel.x_rot(value = 0)
        deco_panel.y_rot(value = 0)
        deco_panel.z_rot(value = 0)
        deco_panel.prompt('Hide', 'IF(Custom_Rack_Style==1,False,True)', [Custom_Rack_Style])        
        deco_panel.cutpart("Panel")
        
        hook = self.add_object(DORB_HOOK)
        hook.set_name('Robe Hook')        
        hook.x_loc('Hook_Offset',[Hook_Offset])
        hook.y_loc('depth', [depth])
        hook.z_loc('height/2', [height])
        hook.x_rot(value = 0)
        hook.y_rot(value = 0)
        hook.z_rot(value = 0)
        hook.material("Chrome")
        mod = hook.obj.modifiers.new('Quantity','ARRAY')
        mod.use_relative_offset = False
        mod.use_constant_offset = True
        offset_driver = hook.obj.driver_add('modifiers["Quantity"].constant_offset_displace',0)
        utils.add_variables_to_driver(offset_driver,[width,Hook_Qty,Hook_Offset])
        offset_driver.driver.expression = "width/Hook_Qty"
        
        count_driver = hook.obj.driver_add('modifiers["Quantity"].count')
        utils.add_variables_to_driver(count_driver,[Hook_Qty])
        count_driver.driver.expression = "Hook_Qty" 
                 
                 
class Coat_and_Hat_Hook_Accessories(fd_types.Assembly):

    type_assembly = "PRODUCT"
    
    drop_id = props_closet.LIBRARY_NAME_SPACE + ".place_closet_accessory"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".accessories"

    def draw(self):
        self.create_assembly()
        
        self.add_tab(name='Main Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        self.add_prompt(name="Custom Rack Style",
                        prompt_type='COMBOBOX',
                        items=["Classic","Deco"],
                        value=0,
                        tab_index=0)
        
        self.add_prompt(name="Add Slide",
                        prompt_type='CHECKBOX',
                        value = True,
                        tab_index=0)
        
        self.add_prompt(name="Hook Type",
                        prompt_type='TEXT',
                        value = "BRK",
                        tab_index=0)
        self.add_prompt(name="Hook Qty",
                        prompt_type='QUANTITY',
                        value=1,
                        tab_index=0)        
        
        #SIZES OF STANDARD ACCESSORY PANELS
        
        self.add_prompt(name="Hook Offset",
                        prompt_type='DISTANCE',
                        value = unit.inch(2),
                        tab_index=1)                                                   
        
        width = self.get_var("dim_x",'width')
        height = self.get_var("dim_z",'height')
        depth = self.get_var("dim_y",'depth')
        Hook_Qty = self.get_var("Hook Qty")
        Hook_Offset = self.get_var("Hook Offset")
        Custom_Rack_Style = self.get_var("Custom Rack Style")

        World_Z = self.get_var('world_loc_z','World_Z',transform_type='LOC_Z')
        accessory_height_dim = fd_types.Dimension()
        accessory_height_dim.anchor.parent = self.obj_bp
        accessory_height_dim.start_x(value = 0)
        accessory_height_dim.start_y(value = 0)
        accessory_height_dim.start_z(value = 0)
        accessory_height_dim.end_z('-World_Z',[World_Z])
        
        panel = common_parts.add_accessory_panel(self)
        panel.set_name('Accessory Rack')
        panel.x_dim('width', [width])
        panel.y_dim('depth',[depth])
        panel.z_dim('height',[height])        
        panel.x_loc(value = 0)
        panel.y_loc(value = 0)
        panel.z_loc(value = 0)
        panel.x_rot(value = 0)
        panel.y_rot(value = 0)
        panel.z_rot(value = 0)
        panel.prompt('Hide', 'IF(Custom_Rack_Style==0,False,True)', [Custom_Rack_Style])
        panel.cutpart("Panel")
        
        deco_panel = self.add_assembly(DECO_PANEL)
        deco_panel.set_name('Deco Accessory Rack')
        deco_panel.x_dim('width', [width])
        deco_panel.y_dim('depth',[depth])
        deco_panel.z_dim('height',[height])        
        deco_panel.x_loc(value = 0)
        deco_panel.y_loc(value = 0)
        deco_panel.z_loc(value = 0)
        deco_panel.x_rot(value = 0)
        deco_panel.y_rot(value = 0)
        deco_panel.z_rot(value = 0)
        deco_panel.prompt('Hide', 'IF(Custom_Rack_Style==1,False,True)', [Custom_Rack_Style])        
        deco_panel.cutpart("Panel")
        
        hook = self.add_object(COAT_AND_HAT_HOOK)
        hook.set_name('Robe Hook')        
        hook.x_loc('Hook_Offset',[Hook_Offset])
        hook.y_loc('depth', [depth])
        hook.z_loc('height/2', [height])
        hook.x_rot(value = 0)
        hook.y_rot(value = 0)
        hook.z_rot(value = 0)
        hook.material("Chrome")
        mod = hook.obj.modifiers.new('Quantity','ARRAY')
        mod.use_relative_offset = False
        mod.use_constant_offset = True
        offset_driver = hook.obj.driver_add('modifiers["Quantity"].constant_offset_displace',0)
        utils.add_variables_to_driver(offset_driver,[width,Hook_Qty,Hook_Offset])
        offset_driver.driver.expression = "width/Hook_Qty"
        
        count_driver = hook.obj.driver_add('modifiers["Quantity"].count')
        utils.add_variables_to_driver(count_driver,[Hook_Qty])
        count_driver.driver.expression = "Hook_Qty"        
 
        self.update()
    

class OPERATOR_Place_Accessory(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".place_closet_accessory"
    bl_label = "Place Accessory"
    bl_description = "This allows you to place an accessory object into the scene."
    bl_options = {'UNDO'}
     
    #READONLY
    object_name = bpy.props.StringProperty(name="Object Name")
     
    product = None
     
    def invoke(self, context, event):
        bp = bpy.data.objects[self.object_name]
        self.product = fd_types.Assembly(bp)
        context.window.cursor_set('PAINT_BRUSH')
        context.scene.update() # THE SCENE MUST BE UPDATED FOR RAY CAST TO WORK
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
 
    def get_rotation(self,obj,prev_rotation):
        rotation = obj.rotation_euler.z + prev_rotation
        if obj.parent:
            return self.get_rotation(obj.parent, rotation)
        else:
            return rotation
 
    def cancel_drop(self,context,event):
        if self.product:
            utils.delete_object_and_children(self.product.obj_bp)
        bpy.context.window.cursor_set('DEFAULT')
        return {'FINISHED'}
 
    def accessory_drop(self,context,event):
        selected_point, selected_obj = utils.get_selection_point(context,event)
        bpy.ops.object.select_all(action='DESELECT')
        selected_assembly = None
         
        self.product.obj_bp.location = selected_point
        self.product.obj_bp.parent = None
         
        if selected_obj:
            wall_bp = utils.get_wall_bp(selected_obj)
            selected_assembly_bp = utils.get_assembly_bp(selected_obj)
            selected_assembly = fd_types.Assembly(selected_assembly_bp)
             
            if wall_bp:
                self.product.obj_bp.parent = wall_bp
                loc_pos = wall_bp.matrix_world.inverted() * selected_point
                 
                self.product.obj_bp.location = loc_pos
                 
                self.product.obj_bp.rotation_euler.z = 0
                self.product.obj_bp.rotation_euler.y = 0
                self.product.obj_bp.rotation_euler.x = 0
                 
            if selected_assembly and selected_assembly.obj_bp:
                props = props_closet.get_object_props(selected_assembly.obj_bp)
                 
                if props.is_panel_bp:
             
                    ass_world_loc = (selected_assembly.obj_bp.matrix_world[0][3],
                    selected_assembly.obj_bp.matrix_world[1][3],
                    selected_assembly.obj_bp.matrix_world[2][3])
                 
                    ass_z_world_loc = (selected_assembly.obj_z.matrix_world[0][3],
                                       selected_assembly.obj_z.matrix_world[1][3],
                                       selected_assembly.obj_z.matrix_world[2][3])                
                     
                    dist_to_bp = math.fabs(utils.calc_distance(selected_point,ass_world_loc))
                    dist_to_z = math.fabs(utils.calc_distance(selected_point,ass_z_world_loc))
     
                    loc_pos = selected_assembly.obj_bp.matrix_world.inverted() * selected_point
     
                    self.product.obj_bp.parent = selected_assembly.obj_bp
                     
                    self.product.obj_bp.location.x = loc_pos[0]
                     
                    self.product.obj_bp.location.z = 0
                     
                    self.product.obj_x.location.x = math.fabs(selected_assembly.obj_y.location.y) #SET DEPTH
                     
                    if selected_assembly.obj_z.location.z < 0: #LEFT PANEL
                        if dist_to_bp > dist_to_z:#PLACE ON RIGHT SIDE
                            self.product.obj_bp.location.y = selected_assembly.obj_y.location.y
                            self.product.obj_bp.rotation_euler.x = math.radians(90)
                            self.product.obj_bp.rotation_euler.y = math.radians(0)
                            self.product.obj_bp.rotation_euler.z = math.radians(90)   
                            self.product.obj_bp.location.z = selected_assembly.obj_z.location.z                     
                        else:#PLACE ON LEFT SIDE
                            self.product.obj_bp.location.y = 0
                            self.product.obj_bp.rotation_euler.x = math.radians(90)
                            self.product.obj_bp.rotation_euler.y = math.radians(180)
                            self.product.obj_bp.rotation_euler.z = math.radians(90)   
                            self.product.obj_bp.location.z = 0
                    else: # CENTER AND RIGHT PANEL
                        if dist_to_bp > dist_to_z:#PLACE ON LEFT SIDE
                            self.product.obj_bp.location.y = 0
                            self.product.obj_bp.rotation_euler.x = math.radians(90)
                            self.product.obj_bp.rotation_euler.y = math.radians(180)
                            self.product.obj_bp.rotation_euler.z = math.radians(90) 
                            self.product.obj_bp.location.z = selected_assembly.obj_z.location.z                       
                        else:#PLACE ON RIGHT SIDE
                            self.product.obj_bp.location.y = selected_assembly.obj_y.location.y
                            self.product.obj_bp.rotation_euler.x = math.radians(90)
                            self.product.obj_bp.rotation_euler.y = math.radians(0)
                            self.product.obj_bp.rotation_euler.z = math.radians(90)
                            self.product.obj_bp.location.z = 0                  
 
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            bpy.context.window.cursor_set('DEFAULT')
            bpy.ops.object.select_all(action='DESELECT')
            utils.set_wireframe(self.product.obj_bp,False)
            context.scene.objects.active = self.product.obj_bp
            self.product.obj_bp.select = True
            return {'FINISHED'}
         
        return {'RUNNING_MODAL'}
     
    def modal(self, context, event):
        context.area.tag_redraw()
         
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}
         
        if event.type in {'ESC'}:
            self.cancel_drop(context,event)
            return {'FINISHED'}    
         
        return self.accessory_drop(context,event)

    
class PROMPTS_Accessories(fd_types.Prompts_Interface):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".accessories"
    bl_label = "Accessories"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name",
                                           description="Stores the Base Point Object Name \
                                           so the object can be retrieved from the database.")
    
    width = bpy.props.FloatProperty(name="Width",unit='LENGTH',precision=4)
    height = bpy.props.FloatProperty(name="Height",unit='LENGTH',precision=4)
    depth = bpy.props.FloatProperty(name="Depth",unit='LENGTH',precision=4)    
    
    product = None

    def check(self, context):
        """ This is called everytime a change is made in the UI """
#         self.update_product_size()
        return True

    def execute(self, context):
        """ This is called when the OK button is clicked """
#         self.update_product_size()
        return {'FINISHED'}

    def invoke(self,context,event):
        """ This is called before the interface is displayed """
        self.product = self.get_product()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(300))
        
    def draw(self, context):
        """ This is where you draw the interface """
        Style = self.product.get_prompt("Custom Rack Style")
        Add_Slide = self.product.get_prompt("Add Slide")
        Hook_Qty = self.product.get_prompt("Hook Qty")
        Pin_Qty = self.product.get_prompt("Pin Qty") 
        Top_Pin_Qty = self.product.get_prompt("Top Pin Qty")
        Bottom_Pin_Qty = self.product.get_prompt("Bottom Pin Qty")
        Hook_Offset = self.product.get_prompt("Hook Offset")   
        Pin_Offset = self.product.get_prompt("Pin Offset")   
        
        layout = self.layout
        box = layout.box()
        box.label(self.product.obj_bp.mv.name_object)
        box.prop(self.product.obj_x,'location',index=0,text="")
        
        if Style:
            Style.draw_prompt(box)
            
        if Add_Slide:
            Add_Slide.draw_prompt(box)
            
        if Pin_Offset:
            Pin_Offset.draw_prompt(box)            
            
        if Hook_Offset:
            Hook_Offset.draw_prompt(box)            
            
        if Hook_Qty:
            Hook_Qty.draw_prompt(box)            
            
        if Pin_Qty:
            Pin_Qty.draw_prompt(box)            
            
        if Top_Pin_Qty:
            Top_Pin_Qty.draw_prompt(box)
            
        if Bottom_Pin_Qty:
            Bottom_Pin_Qty.draw_prompt(box)                        
    
bpy.utils.register_class(OPERATOR_Place_Accessory)
bpy.utils.register_class(PROMPTS_Accessories)

    