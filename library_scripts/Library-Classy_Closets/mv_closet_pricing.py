import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       BoolVectorProperty,
                       PointerProperty,
                       CollectionProperty,
                       EnumProperty)
import math
from mv import fd_types, unit, utils
from . import mv_closet_defaults as props_closet
from . import common_closet_utils

SQ_FT_PRICE = 10
CAM_PRICE = .15
SHELF_PIN_PRICE = .05
MOLDING_LNFT_PRICE = 35

PRICING_PROPERTY_NAMESPACE = "mv_closet_pricing"

def get_pricing_props():
    """ 
    This is a function to get access to all of the scene properties that are registered in this library
    """
    props = eval("bpy.context.scene." + PRICING_PROPERTY_NAMESPACE)
    return props

def get_hinge_price():
    props = get_pricing_props()
    return props.price_per_hinge
    
    #SETUP EXAMPLE FROM SELECTION
#     scene_props = props_closet.get_scene_props()
#     hinge = scene_props.closet_options.hinge_name
#     if hinge == 'Blum Hinge':
#         return 3.54
#     if hinge == 'Grass Hinge':
#         return 6.41
#     if hinge == 'Salice Hinge':
#         return 2.84
#     return 0

def get_slide_price():
    props = get_pricing_props()
    return props.price_per_slide
    
    #SETUP EXAMPLE FROM SELECTION
#     scene_props = props_closet.get_scene_props()
#     slide = scene_props.closet_options.slide_name
#     if slide == 'Accuride Slides':
#         return 3.54
#     if slide == 'Blum Slides':
#         return 6.41
#     if slide == 'Grass Slides':
#         return 5.24
#     if slide == 'Hafele Slides':
#         return 4.99
#     if slide == 'Hettich Slides':
#         return 6.25
#     if slide == 'King Slides':
#         return 3.25
#     if slide == 'Salice Slides':
#         return 4.00   
#     return 0

def get_hamper_price(hamper):
    tilt_out = hamper.get_prompt("Tilt Out Hamper")
    if tilt_out and tilt_out.value():
        return 175
    else:
        return 225

def get_door_hinge_qty(door_height):
    if door_height <= 35:
        return 2
    if door_height <= 45:
        return 3
    if door_height <= 55:
        return 4
    if door_height <= 65:
        return 5
    return 6
    
def get_hamper_hinge_qty(hamper_width):
    if hamper_width <= 35:
        return 2
    return 3
    
def calculate_pull_price(pull_name):
    props = get_pricing_props()
    return props.price_per_pull
    
    #SETUP EXAMPLE FROM SELECTION
#     pricing_props = get_pricing_props()
#     pull_price = 3
#     
#     if "H10" in pull_name:
#         pull_price = 4.50
#     if "H11" in pull_name:
#         pull_price = 2.25
#     if "H14" in pull_name:
#         pull_price = 6.35
#     if "H15" in pull_name:
#         pull_price = 6.00
#     if "H16" in pull_name:
#         pull_price = 4.00
#     if "H17" in pull_name:
#         pull_price = 2.50
#     if "H18" in pull_name:
#         pull_price = 3.25
#     if "H19" in pull_name:
#         pull_price = 5.25
#     if "H25" in pull_name:
#         pull_price = 6.15
#     if "H31" in pull_name:
#         pull_price = 4.75
#     if "H33" in pull_name:
#         pull_price = 5.00
#     if "H39" in pull_name:
#         pull_price = 3.99
#     
#     pricing_props.pull_qty += 1
#     pricing_props.hardware_price_total += pull_price

def calculate_spacer_price(spacer):
    pricing_props = get_pricing_props()
    
    qty = spacer.get_prompt("Y Quantity")
    spacer_qty = 1
    if qty:
        spacer_qty = qty.value()
    pricing_props.spacer_qty += spacer_qty
    pricing_props.hardware_price_total += 8 * spacer_qty    

def calculate_shelf_hardware_price(shelf):
    pricing_props = get_pricing_props()
    
    cam_qty = shelf.get_prompt("Cam Qty")
    shelf_pin_qty = shelf.get_prompt("Shelf Pin Qty")
     
    if cam_qty:
        pricing_props.cam_qty += cam_qty.value()
        pricing_props.hardware_price_total += cam_qty.value() * pricing_props.price_per_cam
        for i in range(cam_qty.value()):
            add_hardware(shelf,"Cam")
     
    if shelf_pin_qty:
        pricing_props.shelf_pin_qty += shelf_pin_qty.value()
        pricing_props.hardware_price_total += shelf_pin_qty.value() * pricing_props.price_per_shelf_pin
        for i in range(shelf_pin_qty.value()):
            add_hardware(shelf,"Shelf Pin")

def calculate_rod_price(rod):
    length = rod.obj_x.location.x
    quantity = rod.get_prompt("Z Quantity")
    if quantity:
        qty = quantity.value()
    else:
        qty = 1
    pricing_props = get_pricing_props()
    pricing_props.hanging_rod_qty += (unit.meter_to_inch(length) / 12) * qty
    pricing_props.hanging_rod_price_total += ((unit.meter_to_inch(length) / 12) * qty) * pricing_props.hanging_rod_price_per_unit

def calculate_hamper_price(insert):
    pricing_props = get_pricing_props()
    pricing_props.hamper_qty += 1
    pricing_props.hardware_price_total += 200
    tilt_out = insert.get_prompt("Tilt Out Hamper")
    if tilt_out and tilt_out.value():
        hinge_qty = get_hamper_hinge_qty(unit.meter_to_inch(insert.obj_x.location.x))
        hinge_price = hinge_qty * get_hinge_price()
        pricing_props.hinge_qty += hinge_qty
        pricing_props.hardware_price_total += hinge_price
    else:
        pricing_props.slide_qty += 1
        pricing_props.hardware_price_total += get_slide_price()

def calculate_material_price(part):
    qty = 1
    qty_z = part.get_prompt("Z Quantity")
    qty_x = part.get_prompt("X Quantity")
    
    if qty_z:
        qty *= qty_z.value()
        
    if qty_x:
        qty *= qty_x.value()

    pricing_props = get_pricing_props()
    length_inches = unit.meter_to_active_unit(math.fabs(part.obj_x.location.x))
    width_inches = unit.meter_to_active_unit(math.fabs(part.obj_y.location.y))
    pricing_props.sheet_material_qty += ((width_inches * length_inches) / 144) * qty
    pricing_props.material_price_total += (((width_inches * length_inches) / 144) * pricing_props.material_price_per_unit) * qty
    
def calculate_door_material_price(part):
    pricing_props = get_pricing_props()
    door_props = props_closet.get_object_props(part.obj_bp)
    length_inches = unit.meter_to_active_unit(math.fabs(part.obj_x.location.x))
    width_inches = unit.meter_to_active_unit(math.fabs(part.obj_y.location.y))
    price_factor = 12
    if door_props.door_type == 'FLAT':
        price_factor = 25
    if door_props.door_type == 'DECO':
        price_factor = 50
    pricing_props.door_qty += 1
    pricing_props.door_drawer_price_total += ((width_inches * length_inches) / 144) * price_factor
    
def calculate_drawer_front_material_price(part):
    pricing_props = get_pricing_props()
    door_props = props_closet.get_object_props(part.obj_bp)
    length_inches = unit.meter_to_active_unit(math.fabs(part.obj_x.location.x))
    width_inches = unit.meter_to_active_unit(math.fabs(part.obj_y.location.y))
    price_factor = 12
    if door_props.door_type == 'FLAT':
        price_factor = 25
    if door_props.door_type == 'DECO':
        price_factor = 50
    pricing_props.drawer_front_qty += 1
    pricing_props.door_drawer_price_total += ((width_inches * length_inches) / 144) * price_factor    
    
def calculate_hamper_front_material_price(part):
    pricing_props = get_pricing_props()
    door_props = props_closet.get_object_props(part.obj_bp)
    length_inches = unit.meter_to_active_unit(math.fabs(part.obj_x.location.x))
    width_inches = unit.meter_to_active_unit(math.fabs(part.obj_y.location.y))
    price_factor = 12
    if door_props.door_type == 'FLAT':
        price_factor = 25
    if door_props.door_type == 'DECO':
        price_factor = 50
    pricing_props.hamper_front_qty += 1
    pricing_props.door_drawer_price_total += ((width_inches * length_inches) / 144) * price_factor        
    
def calculate_door_hinge_price(door):
    pricing_props = get_pricing_props()
    hinge_qty = get_door_hinge_qty(unit.meter_to_inch(door.obj_x.location.x))
    hinge_price = hinge_qty * get_hinge_price()        
    
    pricing_props.hinge_qty += hinge_qty
    pricing_props.hardware_price_total += hinge_price   
    
def calculate_basket_price(basket):
    scene_props = props_closet.get_scene_props()
    pricing_props = get_pricing_props()
    width = unit.meter_to_inch(basket.obj_x.location.x)
    depth = unit.meter_to_inch(basket.obj_y.location.y)
    height = unit.meter_to_inch(basket.obj_x.location.z)
    basket_price = 0
    
    if width <= 18:
        if depth <= 12:
            if height <= 3:
                basket_price =  140 
            elif height <= 6:
                basket_price =  140 
            elif height <= 8:
                basket_price = 140 
        elif depth <= 16:
            if height <= 3:
                basket_price = 140 
            elif height <= 6:
                basket_price = 140 
            elif height <= 8:
                basket_price = 140 
    elif width <= 24:
        if depth <= 12:
            if height <= 3:
                basket_price = 140 
            elif height <= 6:
                basket_price = 140 
            elif height <= 8:
                basket_price = 140 
        elif depth <= 16:
            if height <= 3:
                basket_price = 140 
            elif height <= 6:
                basket_price = 140 
            elif height <= 8:
                basket_price = 140 
    elif width <=30:
        if depth <= 12:
            if height <= 3:
                basket_price = 140 
            elif height <= 6:
                basket_price = 140 
            elif height <= 8:
                basket_price = 140 
        elif depth <= 16:
            if height <= 3:
                basket_price = 140 
            elif height <= 6:
                basket_price = 140 
            elif height <= 8:
                basket_price = 140 
            
    pricing_props.wire_basket_qty += 1
    pricing_props.hardware_price_total += basket_price
    add_hardware(basket,scene_props.closet_options.slide_name)

def calculate_slide_price(assembly):
    scene_props = props_closet.get_scene_props()
    pricing_props = get_pricing_props()

    pricing_props.hardware_price_total += get_slide_price()
    pricing_props.slide_qty += 1
    add_hardware(assembly,scene_props.closet_options.slide_name)

def calculate_drawer_box_price(drawer_box):
    pricing_props = get_pricing_props()
    width = unit.meter_to_inch(drawer_box.obj_x.location.x)
    depth = unit.meter_to_inch(drawer_box.obj_y.location.y)
    height = unit.meter_to_inch(drawer_box.obj_z.location.z)    
    
    area = width * depth * height
    
    pricing_props.drawer_box_qty += 1
    pricing_props.door_drawer_price_total += area * .08
    
def calculate_shelf_fence_price(fence):
    pricing_props = get_pricing_props()
    
    length = unit.meter_to_inch(fence.obj_x.location.x)

    shelf_fence_price = (length / 12) * 14    
    
    pricing_props.shelf_fence_qty += 1
    pricing_props.hardware_price_total += shelf_fence_price  
    
def calculate_molding_price(obj):
    pricing_props = get_pricing_props()
    length = unit.meter_to_feet(utils.get_curve_length(obj))
    pricing_props.molding_qty += length
    pricing_props.molding_price_total += length * pricing_props.molding_price_per_unit

def calculate_hanging_rail_price(assembly):
    pricing_props = get_pricing_props()
    length = unit.meter_to_feet(assembly.obj_x.location.x)
    pricing_props.molding_qty += length
    pricing_props.molding_price_total += length * pricing_props.hanging_rail_price_per_unit

def add_hardware(part,hardware_name):
    obj = utils.create_single_vertex(hardware_name)
    obj_props = props_closet.get_object_props(obj)
    obj_props.is_temp_obj = True    
    obj.cabinetlib.type_mesh = 'HARDWARE'
    obj.mv.name_object = hardware_name
    obj.parent = part.obj_bp

def clear_temp_objects():
    temp_objects = []
    for obj in bpy.data.objects:
        obj_props = props_closet.get_object_props(obj)
        if obj_props.is_temp_obj:
            temp_objects.append(obj)
    utils.delete_obj_list(temp_objects)

def scene_assemblies(context):
    for obj in bpy.context.scene.objects:
        if obj.mv.type == 'BPASSEMBLY':
            assembly = fd_types.Assembly(obj)
            if common_closet_utils.part_is_not_hidden(assembly):
                yield assembly
        
def scene_molding(context):
    for obj in bpy.context.scene.objects:
        props = props_closet.get_object_props(obj)
        if props.is_crown_molding or props.is_base_molding:
            yield obj

class OPERATOR_Calculate_Price(bpy.types.Operator):
    bl_idname = PRICING_PROPERTY_NAMESPACE + ".calculate_price"
    bl_label = "Calculate Price"
    bl_description = "Calculate Price for Closet"

    def execute(self, context):
        props = get_pricing_props()
        
        props.reset()
        clear_temp_objects()
        props.calculate_price(context)
        props.export_properties()
        return {'FINISHED'}

class PROPS_Price_Adjustment(bpy.types.PropertyGroup):      
    
    price = FloatProperty(name="Price",default=0)
    
    def draw(self,layout):
        row = layout.row()
        row.label(self,"name")
        row.label(self,"price")
        
bpy.utils.register_class(PROPS_Price_Adjustment)

class PROPS_Pricing(bpy.types.PropertyGroup):
    
    pricing_tabs = EnumProperty(name="Pricing Tabs",
                                items=[('SETUP',"Setup",'Setup Pricing information'),
                                       ('PRICING',"Pricing",'View Pricing Information')])       
    
    auto_calculate_on_save = BoolProperty(name="Auto Calculate On Save",
                                          default=False,
                                          description="Automatically calculate the pricing information")
    
    #SETUP
    material_price_per_unit = FloatProperty(name="Material Price Per SqFt",default=0)
    molding_price_per_unit = FloatProperty(name="Molding Price Per Linear Ft",default=0)
    hanging_rod_price_per_unit = FloatProperty(name="Hanging Rod Price Per Linear Ft",default=0)
    hanging_rail_price_per_unit = FloatProperty(name="Hanging Rail Price Per Linear Ft",default=0)

    price_per_hinge = FloatProperty(name="Price Per Hinge",default=0)
    price_per_cam = FloatProperty(name="Price Per Cam",default=0)
    price_per_shelf_pin = FloatProperty(name="Price Per Shelf Pin",default=0)
    price_per_slide = FloatProperty(name="Price Per Slide",default=0)
    price_per_pull = FloatProperty(name="Price Per Pull",default=0)
    
    #TOTALS
    material_price_total = FloatProperty(name="Material Price Total",default=0)
    hanging_rod_price_total = FloatProperty(name="hanging Rod Price Total",default=0)
    hardware_price_total = FloatProperty(name="Hardware Price Total",default=0)
    door_drawer_price_total = FloatProperty(name="Door Drawer Price Total",default=0)
    molding_price_total = FloatProperty(name="Molding Price Total",default=0)
    
    sheet_material_qty = FloatProperty(name="Sheet Material Quantity",default=0)
    hanging_rod_qty = FloatProperty(name="Hanging Rod Quantity",default=0)
    
    pull_qty = IntProperty(name="Pull Quantity",default=0)
    slide_qty = IntProperty(name="Pull Quantity",default=0)
    cam_qty = IntProperty(name="Cam Quantity",default=0)
    hinge_qty = IntProperty(name="Hinge Quantity",default=0)
    shelf_pin_qty = IntProperty(name="Shelf Pin Quantity",default=0)
    wire_basket_qty = IntProperty(name="Wire Basket Quantity",default=0)
    hamper_qty = IntProperty(name="Hamper Quantity",default=0)
    spacer_qty = IntProperty(name="Spacer Quantity",default=0)
    shelf_fence_qty = IntProperty(name="Shelf Fence Quantity",default=0)
    
    door_qty = IntProperty(name="Door Quantity",default=0)
    drawer_front_qty = IntProperty(name="Drawer Front Quantity",default=0)
    hamper_front_qty = IntProperty(name="Hamper Front Quantity",default=0)
    drawer_box_qty = IntProperty(name="Drawer Box Quantity",default=0)
    molding_qty = FloatProperty(name="Molding Quantity",default=0)
    
    price_adjustments = CollectionProperty(name="Price Adjustments",type=PROPS_Price_Adjustment)
    
    def reset(self):
        '''
            This function resets all of the pricing properties back to their default
            This should be run before you calculate the price to ensure there is no
            values stored from a previous calculation
        '''
        self.material_price_total = 0
        self.hanging_rod_price_total = 0
        self.hardware_price_total = 0
        self.door_drawer_price_total = 0
        self.molding_price_total = 0
        self.sheet_material_qty = 0
        self.hanging_rod_qty = 0
        self.pull_qty = 0
        self.slide_qty = 0
        self.cam_qty = 0
        self.hinge_qty = 0
        self.shelf_pin_qty = 0
        self.wire_basket_qty = 0
        self.hamper_qty = 0
        self.spacer_qty = 0
        self.shelf_fence_qty = 0
        self.door_qty = 0
        self.drawer_front_qty = 0
        self.hamper_front_qty = 0
        self.drawer_box_qty = 0
        self.molding_qty = 0

    def calculate_price(self,context):
        '''
            This function calculates the price of the current scene
        '''
        for assembly in scene_assemblies(context):

            props = props_closet.get_object_props(assembly.obj_bp)
            
            if props.is_panel_bp:
                calculate_material_price(assembly)
            
            if props.is_shelf_bp:
                calculate_material_price(assembly)       
                calculate_shelf_hardware_price(assembly)
            
            if props.is_slanted_shelf_bp:
                calculate_material_price(assembly)
            
            if props.is_toe_kick_bp:
                calculate_material_price(assembly)
            
            if props.is_filler_bp:
                calculate_material_price(assembly)
            
            if props.is_cleat_bp:
                calculate_material_price(assembly)
            
            if props.is_shelf_lip_bp:
                calculate_material_price(assembly)
            
            if props.is_divider_bp:
                calculate_material_price(assembly)
            
            if props.is_back_bp:
                calculate_material_price(assembly)
            
            if props.is_plant_on_top_bp:
                calculate_material_price(assembly)
            
            if props.is_hanging_rod:
                calculate_rod_price(assembly)
            
            if props.is_door_bp:
                calculate_door_material_price(assembly)
                calculate_door_hinge_price(assembly)
            
            if props.is_drawer_front_bp:
                calculate_drawer_front_material_price(assembly)
            
            if props.is_hamper_front_bp:
                calculate_hamper_front_material_price(assembly)

            if props.is_hamper_insert_bp:
                calculate_hamper_price(assembly)
                
            if props.is_basket_bp:
                calculate_basket_price(assembly)
            
            if props.is_drawer_box_bp:
                calculate_slide_price(assembly)
                calculate_drawer_box_price(assembly)
            
            if props.is_sliding_shelf_bp:
                calculate_slide_price(assembly)
                calculate_material_price(assembly)
            
            if props.is_rollout_tray_bp:
                calculate_slide_price(assembly)
                calculate_drawer_box_price(assembly)
            
            if props.is_handle:
                calculate_pull_price(assembly.obj_bp.mv.name_object)          
            
            if props.is_spacer_bp:
                calculate_spacer_price(assembly)
            
            if props.is_shelf_fence_bp:
                calculate_shelf_fence_price(assembly)

        for obj in scene_molding(context):
            props = props_closet.get_object_props(obj)
            
            if props.is_crown_molding or props.is_base_molding:
                calculate_molding_price(obj)

    def export_properties(self):
        common_closet_utils.set_room_prop("Closet Library: Material Price Total",str(self.material_price_total))
        common_closet_utils.set_room_prop("Closet Library: Hardware Price Total",str(self.hardware_price_total))
        common_closet_utils.set_room_prop("Closet Library: Door and Drawer Front Price Total",str(self.door_drawer_price_total))
        common_closet_utils.set_room_prop("Closet Library: Molding Price Total",str(self.molding_price_total))
        common_closet_utils.set_room_prop("Closet Library: Hanging Rod Price Total",str(self.hanging_rod_price_total))
        
        total = self.material_price_total + self.hardware_price_total + self.door_drawer_price_total + self.molding_price_total + self.hanging_rod_price_total
        
        common_closet_utils.set_room_prop("Closet Library: Closet Price Total",str(total))
        common_closet_utils.set_room_prop("Closet Library: Sheet Material Sq Ft Total",str(self.sheet_material_qty))
        common_closet_utils.set_room_prop("Closet Library: Hanging Rod LFt Total",str(self.hanging_rod_qty))
        common_closet_utils.set_room_prop("Closet Library: Pull Qty",str(self.pull_qty))
        common_closet_utils.set_room_prop("Closet Library: Slide Qty",str(self.slide_qty))
        common_closet_utils.set_room_prop("Closet Library: Cam Qty",str(self.cam_qty))
        common_closet_utils.set_room_prop("Closet Library: Hinge Qty",str(self.hinge_qty))
        common_closet_utils.set_room_prop("Closet Library: Shelf Pin Qty",str(self.shelf_pin_qty))
        common_closet_utils.set_room_prop("Closet Library: Wire Basket Qty",str(self.wire_basket_qty))
        common_closet_utils.set_room_prop("Closet Library: Hamper Qty",str(self.hamper_qty))
        common_closet_utils.set_room_prop("Closet Library: Door Qty",str(self.door_qty))
        common_closet_utils.set_room_prop("Closet Library: Drawer Front Qty",str(self.drawer_front_qty))
        common_closet_utils.set_room_prop("Closet Library: Drawer Box Qty",str(self.drawer_box_qty))
        common_closet_utils.set_room_prop("Closet Library: Molding Qty",str(self.molding_qty))
        
    def draw(self,layout):
        main_box = layout.box()

        row = main_box.row()
        row.scale_y = 1.3
        row.operator(PRICING_PROPERTY_NAMESPACE + ".calculate_price",icon='FILE_TICK')
        row.prop(self,'auto_calculate_on_save',text="Auto Calculate on Save")        
        
        main_col = main_box.column(align=True)
        
        row = main_col.row(align=True)
        row.scale_y = 1.1
        row.prop_enum(self, "pricing_tabs", 'SETUP', icon='PREFERENCES', text="Setup")
        row.prop_enum(self, "pricing_tabs", 'PRICING', icon='PREFERENCES', text="Pricing Info")
        
        if self.pricing_tabs == 'SETUP':

            box = main_col.box()
            box.label("Sheet Material Costs:")
            
            row = box.row()
            row.label("Price Per Unit:")
            row.prop(self,'material_price_per_unit',text="")            

            box = main_col.box()
            box.label("Solid Stock Costs:")            
            
            row = box.row()
            row.label("Hanging Rod Price Per Unit:")
            row.prop(self,'hanging_rod_price_per_unit',text="")
            
            row = box.row()
            row.label("Molding Rod Price Per Unit:")
            row.prop(self,'molding_price_per_unit',text="")              
            
            row = box.row()
            row.label("Hanging Rail Price Per Unit:")
            row.prop(self,'haning_rail_price_per_unit',text="")                         

            box = main_col.box()
            box.label("Hardware Material Costs:")
            
            row = box.row()
            row.label("Hinge Price Per Unit:")
            row.prop(self,'price_per_hinge',text="")
            
            row = box.row()
            row.label("Cam Price Per Unit:")
            row.prop(self,'price_per_cam',text="")
            
            row = box.row()
            row.label("Shelf Pin Price Per Unit:")
            row.prop(self,'price_per_shelf_pin',text="")
            
            row = box.row()
            row.label("Pull Price Per Unit:")
            row.prop(self,'price_per_pull',text="")    
            
            row = box.row()
            row.label("Slides Price Per Unit:")
            row.prop(self,'price_per_slide',text="")
            
        if self.pricing_tabs == 'PRICING':
            
            box = main_col.box()
            col = box.column()
            col.label("Material Price: " + unit.draw_dollar_price(self.material_price_total))
            col.label("Square Footage Quantity: " + str(round(self.sheet_material_qty,2)),icon='BLANK1')
            
            col.separator()
            
            col.label("Hanging Rod Price: " + unit.draw_dollar_price(self.hanging_rod_price_total)) 
            col.label("Hanging Rod Linear Footage Quantity: " + str(round(self.hanging_rod_qty,2)),icon='BLANK1')
            
            col.separator()
            
            col.label("Molding Price: " + unit.draw_dollar_price(self.molding_price_total)) 
            col.label("Linear Footage Quantity: " + str(round(self.molding_qty,2)),icon='BLANK1')
            
            col.separator()
            
            col.label("Hardware Price: " + unit.draw_dollar_price(self.hardware_price_total))
            col.label("Pull Quantity: " + str(self.pull_qty),icon='BLANK1') 
            col.label("Drawer Slide Quantity: " + str(self.slide_qty),icon='BLANK1') 
            col.label("Drawer Spacer Quantity: " + str(self.spacer_qty),icon='BLANK1')
            col.label("Wire Basket Quantity: " + str(self.wire_basket_qty),icon='BLANK1')
            col.label("Hamper Quantity: " + str(self.hamper_qty),icon='BLANK1')
            col.label("Cam Quantity: " + str(self.cam_qty),icon='BLANK1') 
            col.label("Hinge Quantity: " + str(self.hinge_qty),icon='BLANK1') 
            col.label("Shelf Pin Quantity: " + str(self.shelf_pin_qty),icon='BLANK1')
            col.label("Shelf Fence Quantity: " + str(self.shelf_fence_qty),icon='BLANK1') 
            
            col.separator()
            
            col.label("Door & Drawer Front Price: " + unit.draw_dollar_price(self.door_drawer_price_total))
            col.label("Door Quantity: " + str(self.door_qty),icon='BLANK1')
            col.label("Drawer Front Quantity: " + str(self.drawer_front_qty),icon='BLANK1')
            col.label("Hamper Front Quantity: " + str(self.hamper_front_qty),icon='BLANK1') 
            col.label("Drawer Box Quantity: " + str(self.drawer_box_qty),icon='BLANK1')
            
            col.separator()
            
            for price_adjustment in self.price_adjustments:
                price_adjustment.draw(col)


class PANEL_Closet_Pricing_Setup(bpy.types.Panel):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + "Closet_Price"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "Closet Price"
    bl_category = "Fluid Designer"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label('',icon='BLANK1')

    def draw(self, context):
        props = get_pricing_props()
        props.draw(self.layout)


# REGISTER CLASSES
bpy.utils.register_class(OPERATOR_Calculate_Price)
bpy.utils.register_class(PROPS_Pricing)
bpy.utils.register_class(PANEL_Closet_Pricing_Setup)
exec("bpy.types.Scene." + PRICING_PROPERTY_NAMESPACE + "= PointerProperty(type = PROPS_Pricing)")


# AUTO CALL OPERATOR ON SAVE
@bpy.app.handlers.persistent
def calculate_pricing(scene=None):
    props = get_pricing_props()
    if props.auto_calculate_on_save:
        exec("bpy.ops." + PRICING_PROPERTY_NAMESPACE + ".calculate_price()")
bpy.app.handlers.save_pre.append(calculate_pricing)
