import bpy
from bpy.types import Panel
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
from snap import sn_types, sn_unit, sn_utils, sn_db
from . import closet_props
from . import closet_utils

SQ_FT_PRICE = 10
CAM_PRICE = 2.628571429
SHELF_PIN_PRICE = .05
MOLDING_LNFT_PRICE = 35

PRICING_PROPERTY_NAMESPACE = "sn_closet_pricing"


def get_pricing_props():
    """ 
    This is a function to get access to all of the scene properties that are registered in this library
    """
    props = eval("bpy.context.scene." + PRICING_PROPERTY_NAMESPACE)
    return props


def get_hinge_price():
    scene_props = bpy.context.scene.sn_closets
    hinge = scene_props.closet_options.hinge_name
    rows = sn_db.query_db(
        "SELECT\
            SKU,\
            FranchisePrice,\
            RetailPrice\
        FROM\
            {CCItems}\
        WHERE\
            Name LIKE '%{hinge_name}%'\
                ;\
        ".format(CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location, hinge_name=hinge)
    )

    for row in rows:
        sku = row[0]
        franchise_price = float(row[1])
        retail_price = float(row[2])

    return retail_price


def get_slide_size(slide_type, assembly):
    closet_props = assembly.obj_bp.sn_closets

    if closet_props.is_drawer_box_bp:
        drawer_depth = sn_unit.meter_to_inch(assembly.obj_y.location.y)

    if closet_props.is_drawer_side_bp:
        drawer_box_assembly = sn_types.Assembly(assembly.obj_bp.parent)
        drawer_depth = sn_unit.meter_to_inch(drawer_box_assembly.obj_y.location.y)

    if closet_props.is_hamper_insert_bp:
        material_props = bpy.context.scene.closet_materials
        material_sku = material_props.get_mat_sku(assembly.obj_bp, assembly)
        material_name = material_props.get_mat_inventory_name(sku=material_sku)
        hamper_assembly = sn_types.Assembly(assembly.obj_bp.parent)
        drawer_depth = sn_unit.meter_to_inch(assembly.obj_y.location.y)
        drawer_depth1 = sn_unit.meter_to_inch(hamper_assembly.obj_y.location.y)

    if closet_props.is_basket_bp:
        material_props = bpy.context.scene.closet_materials
        material_sku = material_props.get_mat_sku(assembly.obj_bp, assembly)
        material_name = material_props.get_mat_inventory_name(sku=material_sku)
        drawer_depth = sn_unit.meter_to_inch(assembly.obj_y.location.y)


    sizes = []
    # mat_props = bpy.context.scene.closet_materials
    # slide_type = mat_props.get_drawer_slide_type()

    for size in slide_type.sizes:
        sizes.append(size)

    sizes.reverse()

    for size in sizes:
        if drawer_depth >= float(size.slide_length_inch):
            return size


def get_slide_price(assembly):
    material_props = bpy.context.scene.closet_materials
    slide_type = material_props.get_drawer_slide_type()
    slide_name = slide_type.name
    slide_size = get_slide_size(slide_type, assembly)
    slide_len = slide_size.slide_length_inch
    if "Blum" in slide_name:
        slide_name = "Blumotion UM"

    rows = sn_db.query_db(
        "SELECT\
            SKU,\
            FranchisePrice,\
            RetailPrice\
        FROM\
            {CCItems}\
        WHERE\
            Name LIKE '%{name}%' AND\
            Name LIKE '%{len}%'\
                ;\
        ".format(CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location, name=slide_name, len=str(int(slide_len)))
    )
    for row in rows:
        sku = row[0]
        franchise_price = float(row[1])
        retail_price = float(row[2])
    return retail_price


def get_basket_price(assembly):
    #Hamper Basket
    if assembly.obj_bp.sn_closets.is_basket_bp:
        material_props = bpy.context.scene.closet_materials
        material_sku = material_props.get_mat_sku(assembly.obj_bp, assembly)
        material_name = material_props.get_mat_inventory_name(sku=material_sku)
        hamper_insert_bp = assembly.obj_bp.parent
        basket_color = material_props.wire_basket_colors
        basket_width = sn_unit.meter_to_inch(assembly.obj_x.location.x)
        basket_depth = sn_unit.meter_to_inch(assembly.obj_y.location.y)
        color_id = 2 if basket_color == 'CHROME' else 7
        width_id = 1 if basket_width == 18.0 else 2
        depth_id = 3 if basket_depth == 14.0 else 4
        vendor_id = '547.42.{}{}{}'.format(color_id,depth_id,width_id)

        rows = sn_db.query_db(
            "SELECT\
                FranchisePrice,\
                RetailPrice\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'AC' AND\
                VendorItemNum ='{}'\
            ;".format(vendor_id, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )

        for row in rows:
            franchise_price = row[0]
            retail_price = row[1]           
        return retail_price        


def get_pull_price(assembly):
    pull_cat = bpy.context.scene.sn_closets.closet_options.pull_category
    pull_name = bpy.context.scene.sn_closets.closet_options.pull_name
    item_name = assembly.obj_bp.snap.name_object
    vendor_id = item_name[:10] # use vendor code in item name for lookup (123.45.678)

    rows = sn_db.query_db(
        "SELECT\
            FranchisePrice,\
            RetailPrice\
        FROM\
            {CCItems}\
        WHERE\
            ProductType == 'AC' AND\
            VendorItemNum ='{}'\
        ;".format(pull_name, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
    )

    for row in rows:
        franchise_price = row[0]
        retail_price = row[1]           
    return retail_price


def get_rod_price(assembly):
    #Rod
    item_name = bpy.context.scene.sn_closets.closet_options.rods_name
    vendor_id = item_name[-10:]
    rows = sn_db.query_db(
        "SELECT\
            FranchisePrice,\
            RetailPrice\
        FROM\
            {CCItems}\
        WHERE\
            ProductType == 'AC' AND\
            VendorItemNum ='{}'\
        ;".format(vendor_id, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
    )

    for row in rows:
        franchise_price = row[0]
        retail_price = row[1]

    return retail_price


def get_pole_cup_price(assembly):
    #Rod Cup
    item_name = bpy.context.scene.sn_closets.closet_options.pole_cup_name
    rows = sn_db.query_db(
        "SELECT\
            FranchisePrice,\
            RetailPrice\
        FROM\
            {CCItems}\
        WHERE\
            SKU = '{SKU}'\
        ;".format(SKU=item_name, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
    )

    for row in rows:
        franchise_price = row[0]
        retail_price = row[1]
    return retail_price


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


def calculate_pull_price(assembly, pull_price):
    pricing_props = get_pricing_props()
    pricing_props.pull_qty += 1
    pricing_props.hardware_price_total += pull_price


def calculate_spacer_price(spacer):
    pricing_props = get_pricing_props()
    qty = spacer.get_prompt("Y Quantity")
    spacer_qty = 1
    if qty:
        spacer_qty = qty.get_value()
    pricing_props.spacer_qty += spacer_qty
    pricing_props.hardware_price_total += 8 * spacer_qty  


def calculate_shelf_hardware_price(shelf):
    pricing_props = get_pricing_props()
    cam_qty = shelf.get_prompt("Cam Qty")
    shelf_pin_qty = shelf.get_prompt("Shelf Pin Qty")

    if cam_qty:
        pricing_props.cam_qty += cam_qty.get_value()
        pricing_props.hardware_price_total += cam_qty.get_value() * CAM_PRICE
        for i in range(cam_qty.get_value()):
            add_hardware(shelf, "Cam")

    if shelf_pin_qty:
        pricing_props.shelf_pin_qty += shelf_pin_qty.get_value()
        pricing_props.hardware_price_total += shelf_pin_qty.get_value() * SHELF_PIN_PRICE
        for i in range(shelf_pin_qty.get_value()):
            add_hardware(shelf, "Shelf Pin")


def calculate_rod_price(rod, rod_price, pole_cup_price):
    length = rod.obj_x.location.x
    quantity = rod.get_prompt("Z Quantity")
    if quantity:
        qty = quantity.get_value()
    else:
        qty = 1
    pricing_props = get_pricing_props()
    pricing_props.hanging_rod_qty += (sn_unit.meter_to_inch(length) / 12) * qty
    pricing_props.hanging_rod_price_total += ((sn_unit.meter_to_inch(length) / 12) * qty) * rod_price
    cup_qty = 2
    cup_price = cup_qty * pole_cup_price
    pricing_props.pole_cup_qty += cup_qty
    pricing_props.hardware_price_total += cup_price


def calculate_hamper_price(insert, slide_price):
    pricing_props = get_pricing_props()
    tilt_out = insert.get_prompt("Tilt Out Hamper")
    if tilt_out and tilt_out.get_value():
        hinge_qty = get_hamper_hinge_qty(sn_unit.meter_to_inch(insert.obj_x.location.x))
        hinge_price = hinge_qty * get_hinge_price()
        pricing_props.hinge_qty += hinge_qty
        pricing_props.hardware_price_total += hinge_price
    else:
        pricing_props.slide_qty += 1
        pricing_props.hardware_price_total += slide_price


def get_material_price(assembly):
    material_props = bpy.context.scene.closet_materials
    material_sku = material_props.get_mat_sku(assembly.obj_bp, assembly)
    material_name = material_props.get_mat_inventory_name(sku=material_sku)
    rows = sn_db.query_db(
        "SELECT\
            SKU,\
            FranchisePrice,\
            RetailPrice,\
            UOM\
        FROM\
            {CCItems}\
        WHERE\
            SKU = '{SKU}'\
                ;\
        ".format(CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location, SKU=material_sku)
    )

    for row in rows:
        sku = row[0]
        franchise_price = float(row[1])
        retail_price = float(row[2])
        uom = row[3]
    return retail_price


def calculate_material_price(part, material_price):
    pricing_props = get_pricing_props()
    length_inches = sn_unit.meter_to_active_unit(math.fabs(part.obj_x.location.x))
    width_inches = sn_unit.meter_to_active_unit(math.fabs(part.obj_y.location.y))
    pricing_props.sheet_material_qty += ((width_inches * length_inches) / 144)
    pricing_props.material_price_total += ((width_inches * length_inches) / 144) * material_price


def calculate_door_material_price(part):
    pricing_props = get_pricing_props()
    door_props = part.obj_bp.sn_closets
    length_inches = sn_unit.meter_to_active_unit(math.fabs(part.obj_x.location.x))
    width_inches = sn_unit.meter_to_active_unit(math.fabs(part.obj_y.location.y))
    price_factor = 12
    if door_props.door_type == 'FLAT':
        price_factor = 25
    if door_props.door_type == 'DECO':
        price_factor = 50
    pricing_props.door_qty += 1
    pricing_props.door_drawer_price_total += ((width_inches * length_inches) / 144) * price_factor


def calculate_drawer_front_material_price(part):
    pricing_props = get_pricing_props()
    door_props = part.obj_bp.sn_closets
    length_inches = sn_unit.meter_to_active_unit(math.fabs(part.obj_x.location.x))
    width_inches = sn_unit.meter_to_active_unit(math.fabs(part.obj_y.location.y))
    price_factor = 12
    if door_props.door_type == 'FLAT':
        price_factor = 25
    if door_props.door_type == 'DECO':
        price_factor = 50
    pricing_props.drawer_front_qty += 1
    pricing_props.door_drawer_price_total += ((width_inches * length_inches) / 144) * price_factor    


def calculate_hamper_front_material_price(part):
    pricing_props = get_pricing_props()
    door_props = part.obj_bp.sn_closets
    length_inches = sn_unit.meter_to_active_unit(math.fabs(part.obj_x.location.x))
    width_inches = sn_unit.meter_to_active_unit(math.fabs(part.obj_y.location.y))
    price_factor = 12
    if door_props.door_type == 'FLAT':
        price_factor = 25
    if door_props.door_type == 'DECO':
        price_factor = 50
    pricing_props.hamper_front_qty += 1
    pricing_props.door_drawer_price_total += ((width_inches * length_inches) / 144) * price_factor        


def calculate_door_hinge_price(door):
    pricing_props = get_pricing_props()
    hinge_qty = get_door_hinge_qty(sn_unit.meter_to_inch(door.obj_x.location.x))
    hinge_price = hinge_qty * get_hinge_price()        
    pricing_props.hinge_qty += hinge_qty
    pricing_props.hardware_price_total += hinge_price   


def calculate_basket_price(basket, slide_price):
    pricing_props = get_pricing_props()         
    pricing_props.wire_basket_qty += 1
    pricing_props.slide_qty += 1
    pricing_props.hardware_price_total += get_basket_price(basket)
    pricing_props.hardware_price_total += slide_price
    add_hardware(basket, bpy.context.scene.closet_materials.get_drawer_slide_type().name)


def calculate_drawer_box_price(drawer_box, slide_price):
    scene_props = bpy.context.scene.sn_closets
    pricing_props = get_pricing_props()
    width = sn_unit.meter_to_inch(drawer_box.obj_x.location.x)
    depth = sn_unit.meter_to_inch(drawer_box.obj_y.location.y)
    height = sn_unit.meter_to_inch(drawer_box.obj_z.location.z)    
    area = width * depth * height
    pricing_props.hardware_price_total += slide_price
    pricing_props.drawer_box_qty += 1
    pricing_props.slide_qty += 1
    pricing_props.door_drawer_price_total += area * .08
    add_hardware(drawer_box, bpy.context.scene.closet_materials.get_drawer_slide_type().name)


def calculate_shelf_fence_price(fence):
    pricing_props = get_pricing_props()
    length = sn_unit.meter_to_inch(fence.obj_x.location.x)

    shelf_fence_price = (length / 12) * 14
    pricing_props.shelf_fence_qty += 1
    pricing_props.hardware_price_total += shelf_fence_price  


def calculate_molding_price(obj):
    pricing_props = get_pricing_props()
    length = sn_unit.meter_to_feet(sn_utils.get_curve_length(obj))
    pricing_props.molding_qty += length
    pricing_props.molding_price_total += length * MOLDING_LNFT_PRICE


def calculate_accessory_price(assembly, item_name):
    pricing_props = get_pricing_props()
    pricing_props.accessory_price_total += get_hardware_price(assembly, item_name)


def calculate_total_price():
    pricing_props = get_pricing_props()
    pricing_props.project_total = pricing_props.accessory_price_total + pricing_props.material_price_total + pricing_props.hanging_rod_price_total + pricing_props.door_drawer_price_total + pricing_props.hardware_price_total + pricing_props.molding_price_total


def get_hardware_price(assembly, item_name):
    conn = sn_db.connect_db()
    cursor = conn.cursor()
    sku = "Unknown"
    retail_prince = 0
    #print(obj_bp, assembly.obj_bp, item_name)

    #Pull
    if assembly.obj_bp.sn_closets.is_handle:
        pull_cat = bpy.context.scene.sn_closets.closet_options.pull_category
        pull_name = bpy.context.scene.sn_closets.closet_options.pull_name
        vendor_id = item_name[:10] # use vendor code in item name for lookup (123.45.678)

        cursor.execute(
            "SELECT\
                FranchisePrice,\
                RetailPrice\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'AC' AND\
                VendorItemNum ='{}'\
            ;".format(vendor_id, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )

        rows = cursor.fetchall()

        for row in rows:
            franchise_price = row[0]
            retail_price = row[1]
            #print("FOUND PULL SKU: ", sku)            
        
        conn.close()
        return retail_price

    #Hinge
    if assembly.obj_bp.sn_closets.is_hinge:
        hinge_name = bpy.context.scene.sn_closets.closet_options.hinge_name

        cursor.execute(
            "SELECT\
                FranchisePrice,\
                RetailPrice\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'HW' AND\
                Name LIKE'{}'\
            ;".format("%" + hinge_name + "%", CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )

        rows = cursor.fetchall()

        for row in rows:
            franchise_price = row[0]
            retail_price = row[1]
            #print("FOUND HINGE SKU: ", sku)            
        
        conn.close()

        return retail_price

    #Hinge Plate
    if "Mounting Plate" in item_name:
        cursor.execute(
            "SELECT\
                FranchisePrice,\
                RetailPrice\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'HW' AND\
                Name LIKE'{}'\
            ;".format("%" + item_name + "%", CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )

        rows = cursor.fetchall()

        for row in rows:
            franchise_price = row[0]
            retail_price = row[1]
            #print("FOUND MOUNTING PLATE SKU: ", sku)            
        
        conn.close()
        return retail_price        
    

    #Slide
    if "Drawer Slide" in item_name:
        mat_props = bpy.context.scene.closet_materials
        slide_type = mat_props.get_drawer_slide_type()
        slide_name = slide_type.name
        slide_size = get_slide_size(slide_type, assembly)
        slide_len = slide_size.slide_length_inch

        if slide_len % 1 == 0:
            slide_len = int(slide_len)

        cursor.execute(
            "SELECT\
                FranchisePrice,\
                RetailPrice\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'HW' AND\
                Name LIKE '{}' AND\
                Name LIKE '{}'\
            ;".format(
                "%" + slide_name + "%",
                "%" + str(slide_len) + "%",
                CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location
            )
        )    

        rows = cursor.fetchall()
        for row in rows:
            franchise_price = row[0]
            retail_price = row[1]
            #print("FOUND SLIDE SKU: ", sku)            
        
        conn.close()
        return retail_price        

    #Hamper Basket
    if assembly.obj_bp.sn_closets.is_hamper_bp:
        mat_props = bpy.context.scene.closet_materials
        hamper_insert_bp = assembly.obj_bp.parent
        basket_color = mat_props.wire_basket_colors
        basket_width = sn_unit.meter_to_inch(assembly.obj_x.location.x)
        basket_depth = sn_unit.meter_to_inch(assembly.obj_y.location.y)
        color_id = 2 if basket_color == 'CHROME' else 7
        width_id = 1 if basket_width == 18.0 else 2
        depth_id = 3 if basket_depth == 14.0 else 4
        vendor_id = '547.42.{}{}{}'.format(color_id,depth_id,width_id)

        cursor.execute(
            "SELECT\
                FranchisePrice,\
                RetailPrice\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'AC' AND\
                VendorItemNum ='{}'\
            ;".format(vendor_id, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )

        rows = cursor.fetchall()
        for row in rows:
            franchise_price = row[0]
            retail_price = row[1]
            #print("FOUND HAMPER BASKET SKU: ", sku)            
        
        conn.close()
        return retail_price        

    #Hamper Brake Flaps
    if "Hamper Brake Flap Left" in item_name or "Hamper Brake Flap Right" in item_name:
        cursor.execute(
            "SELECT\
                FranchisePrice,\
                RetailPrice\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'AC' AND\
                Name LIKE'{}'\
            ;".format("%" + item_name + "%", CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )

        rows = cursor.fetchall()

        for row in rows:
            franchise_price = row[0]
            retail_price = row[1]
            #print("FOUND BRAKE FLAP SKU: ", sku)            
        
        conn.close()

        return retail_price

    #Hamper Rack
    if "Hamper Rack" in item_name:
        mat_props = bpy.context.scene.closet_materials        
        basket_color = mat_props.wire_basket_colors

        if basket_color == 'CHROME':
            rack_name = "Hamper Rack Chrome"

        elif basket_color == 'WHITE':
            rack_name = "Hamper Rack White"

        cursor.execute(
            "SELECT\
                FranchisePrice,\
                RetailPrice\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'AC' AND\
                Name LIKE'{}'\
            ;".format("%" + rack_name + "%", CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )

        rows = cursor.fetchall()

        for row in rows:
            franchise_price = row[0]
            retail_price = row[1]
            #print("FOUND HAMPER RACK SKU: ", sku)            
        
        conn.close()

        return retail_price        

    #Hamper Laundry Bag
    if "Cloth Laundry Bag" in item_name:
        basket_width = sn_unit.meter_to_inch(assembly.obj_x.location.x)

        if basket_width > 18.0:
            bag_name = item_name + " 24"
        else:
            bag_name = item_name + " 18"

        cursor.execute(
            "SELECT\
                FranchisePrice,\
                RetailPrice\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'AC' AND\
                Name LIKE'{}'\
            ;".format("%" + bag_name + "%", CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )

        rows = cursor.fetchall()

        for row in rows:
            franchise_price = row[0]
            retail_price = row[1]
            #print("FOUND LAUNDRY BAG SKU: ", sku)            
        
        conn.close()

        return retail_price

    #Rod
    if assembly.obj_bp.sn_closets.is_hanging_rod:
        item_name = bpy.context.scene.sn_closets.closet_options.rods_name
        vendor_id = item_name[-10:]

        cursor.execute(
            "SELECT\
                FranchisePrice,\
                RetailPrice\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'AC' AND\
                VendorItemNum ='{}'\
            ;".format(vendor_id, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )

        rows = cursor.fetchall()

        for row in rows:
            franchise_price = row[0]
            retail_price = row[1]
            #print("FOUND HANGING ROD SKU: ", sku)            
        
        conn.close()

        return retail_price

    #Rod Cup
    if "Pole Cup" in item_name:
        sku = bpy.context.scene.sn_closets.closet_options.pole_cup_name

        #print("FOUND POLE CUP SKU:", sku)

        return sku    

    #KD Fitting
    if "KD Fitting" in item_name:
        mat_props = bpy.context.scene.closet_materials
        sku = mat_props.kd_fitting_color
        #print("FOUND KD FITTING SKU:", sku)

        return sku

    #Pegs
    if "Peg Chrome" in item_name:
        cursor.execute(
            "SELECT\
                FranchisePrice,\
                RetailPrice\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'HW' AND\
                Name LIKE'{}'\
            ;".format("%peg%chrome%", CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )

        rows = cursor.fetchall()

        for row in rows:
            franchise_price = row[0]
            retail_price = row[1]
            #print("FOUND CHROME PEG SKU: ", sku)

        conn.close()

        return retail_price

    #Door lock
    if item_name == "Door Lock":
        print("DOOR LOCK")
        cursor.execute(
            "SELECT\
                FranchisePrice,\
                RetailPrice\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'AC' AND\
                VendorItemNum =='{}'\
            ;".format("C8055-14A", CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )

        rows = cursor.fetchall()

        for row in rows:
            franchise_price = row[0]
            retail_price = row[1]
            print("FOUND DOOR LOCK SKU:", sku)

        conn.close()

        return retail_price

    #Door lock cam
    if item_name == "Door Lock Cam":
        print("DOOR LOCK CAM")

        cursor.execute(
            "SELECT\
                FranchisePrice,\
                RetailPrice\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'AC' AND\
                VendorItemNum =='{}'\
            ;".format("C7004-2C", CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )

        rows = cursor.fetchall()

        for row in rows:
            franchise_price = row[0]
            retail_price = row[1]
            print("FOUND LOCK CAM SKU:", sku)

        conn.close()

        return retail_price

    #Door lock latch finger
    if item_name == "Door Lock Latch":
        print("DOOR LOCK LATCH")

        cursor.execute(
            "SELECT\
                FranchisePrice,\
                RetailPrice\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'AC' AND\
                VendorItemNum =='{}'\
            ;".format("245.74.200", CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )

        rows = cursor.fetchall()

        for row in rows:
            franchise_price = row[0]
            retail_price = row[1]
            print("FOUND LATCH SKU:", sku)

        conn.close()

        return retail_price

    #----------Closet Accessories
    #Valet Rod
    if "Valet Rod" in item_name:
        sku = "AC-0000177"
        rows = sn_db.query_db(
        "SELECT\
            SKU,\
            FranchisePrice,\
            RetailPrice\
        FROM\
            {CCItems}\
        WHERE\
            SKU = '{sku_num}'\
                ;\
        ".format(CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location, sku_num=sku)
        )
        for row in rows:
            sku = row[0]
            franchise_price = float(row[1])
            retail_price = float(row[2])
        return retail_price

    #Valet Rod 2
    if "Valet Rod 2" in item_name:
        sku = "AC-0000176"
        rows = sn_db.query_db(
        "SELECT\
            SKU,\
            FranchisePrice,\
            RetailPrice\
        FROM\
            {CCItems}\
        WHERE\
            SKU = '{sku_num}'\
                ;\
        ".format(CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location, sku_num=sku)
        )
        for row in rows:
            sku = row[0]
            franchise_price = float(row[1])
            retail_price = float(row[2])
        return retail_price

    #Wire Basket
    if "Wire Basket" in item_name:
        sku = "AC-0000001"
        rows = sn_db.query_db(
        "SELECT\
            SKU,\
            FranchisePrice,\
            RetailPrice\
        FROM\
            {CCItems}\
        WHERE\
            SKU = '{sku_num}'\
                ;\
        ".format(CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location, sku_num=sku)
        )
        for row in rows:
            sku = row[0]
            franchise_price = float(row[1])
            retail_price = float(row[2])
        return retail_price

    #Tie Rack
    if "Tie Rack" in item_name:
        sku = "AC-0000153"
        rows = sn_db.query_db(
        "SELECT\
            SKU,\
            FranchisePrice,\
            RetailPrice\
        FROM\
            {CCItems}\
        WHERE\
            SKU = '{sku_num}'\
                ;\
        ".format(CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location, sku_num=sku)
        )
        for row in rows:
            sku = row[0]
            franchise_price = float(row[1])
            retail_price = float(row[2])
        return retail_price

    #Belt Rack
    if "Belt Rack" in item_name:
        sku = "AC-0000143"
        rows = sn_db.query_db(
        "SELECT\
            SKU,\
            FranchisePrice,\
            RetailPrice\
        FROM\
            {CCItems}\
        WHERE\
            SKU = '{sku_num}'\
                ;\
        ".format(CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location, sku_num=sku)
        )
        for row in rows:
            sku = row[0]
            franchise_price = float(row[1])
            retail_price = float(row[2])
        return retail_price

    #Robe Hook
    if "Robe Hook" in item_name:
        sku = "AC-0000188"
        rows = sn_db.query_db(
        "SELECT\
            SKU,\
            FranchisePrice,\
            RetailPrice\
        FROM\
            {CCItems}\
        WHERE\
            SKU = '{sku_num}'\
                ;\
        ".format(CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location, sku_num=sku)
        )
        for row in rows:
            sku = row[0]
            franchise_price = float(row[1])
            retail_price = float(row[2])
        return retail_price


def add_hardware(part, hardware_name):
    obj = sn_utils.create_single_vertex(hardware_name)
    obj_props = obj.sn_closets
    obj_props.is_temp_obj = True
    obj.snap.type_mesh = 'HARDWARE'
    obj.snap.name_object = hardware_name
    obj.parent = part.obj_bp

    # obj = sn_utils.create_single_vertex(hardware_name)
    # obj_props = obj.sn_closets
    # obj_props.is_temp_obj = True    
    # obj.cabinetlib.type_mesh = 'HARDWARE'
    # obj.snap.name_object = hardware_name
    # obj.parent = part.obj_bp


def clear_temp_objects():
    temp_objects = []
    for obj in bpy.data.objects:
        obj_props = obj.sn_closets
        if obj_props.is_temp_obj:
            temp_objects.append(obj)
    sn_utils.delete_obj_list(temp_objects)


def scene_assemblies(context):
    for obj in bpy.context.scene.objects:
        if obj.get('IS_BP_ASSEMBLY'):
            assembly = sn_types.Assembly(obj)
            if closet_utils.part_is_not_hidden(assembly):
                yield assembly


def scene_molding(context):
    for obj in bpy.context.scene.objects:
        props = obj.sn_closets
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
        # sn_pricing.calculate_price()
        return {'FINISHED'}


class PROPS_Price_Adjustment(bpy.types.PropertyGroup):

    price: FloatProperty(name="Price", default=0)

    def draw(self, layout):
        row = layout.row()
        row.label(text="name")
        row.label(text="price")


bpy.utils.register_class(PROPS_Price_Adjustment)


class PROPS_Pricing(bpy.types.PropertyGroup):

    pricing_tabs: EnumProperty(
        # name="Pricing Tabs",
        # items=[('SETUP',"Setup",'Setup Pricing information'),
            #    ('PRICING',"Pricing",'View Pricing Information')])
        name="Pricing Tabs",
        items=[('PRICING',"Pricing",'View Pricing Information')])
    
    auto_calculate_on_save: BoolProperty(name="Auto Calculate On Save",
                                          default=False,
                                          description="Automatically calculate the pricing information")
    
    #SETUP
    # material_price_per_unit: FloatProperty(name="Material Price Per Unit",default=0)
    # molding_price_per_unit: FloatProperty(name="Molding Price Per Linear Ft",default=0)
    # hanging_rod_price_per_unit: FloatProperty(name="Hanging Rod Price Per Linear Ft",default=0)
    # hanging_rail_price_per_unit: FloatProperty(name="Hanging Rail Price Per Linear Ft",default=0)

    # price_per_hinge: FloatProperty(name="Price Per Hinge",default=0)
    # price_per_cam: FloatProperty(name="Price Per Cam",default=0)
    # price_per_shelf_pin: FloatProperty(name="Price Per Shelf Pin",default=0)
    # price_per_slide: FloatProperty(name="Price Per Slide",default=0)
    # price_per_pull: FloatProperty(name="Price Per Pull",default=0)    
    
    #TOTALS
    material_price_total: FloatProperty(name="Material Price Total",default=0)
    hanging_rod_price_total: FloatProperty(name="hanging Rod Price Total",default=0)
    hardware_price_total: FloatProperty(name="Hardware Price Total",default=0)
    accessory_price_total: FloatProperty(name="Accessory Price Total", default=0)
    door_drawer_price_total: FloatProperty(name="Door Drawer Price Total",default=0)
    molding_price_total: FloatProperty(name="Molding Price Total",default=0)
    project_total: FloatProperty(name="Project Price Total", default=0)
    
    sheet_material_qty: FloatProperty(name="Sheet Material Quantity",default=0)
    hanging_rod_qty: FloatProperty(name="Hanging Rod Quantity",default=0)
    
    pole_cup_qty: IntProperty(name="Pole Cup Quantity",default=0)
    pull_qty: IntProperty(name="Pull Quantity",default=0)
    slide_qty: IntProperty(name="Slide Quantity",default=0)
    cam_qty: IntProperty(name="Cam Quantity",default=0)
    hinge_qty: IntProperty(name="Hinge Quantity",default=0)
    shelf_pin_qty: IntProperty(name="Shelf Pin Quantity",default=0)
    wire_basket_qty: IntProperty(name="Wire Basket Quantity",default=0)
    hamper_qty: IntProperty(name="Hamper Quantity",default=0)
    spacer_qty: IntProperty(name="Spacer Quantity",default=0)
    shelf_fence_qty: IntProperty(name="Shelf Fence Quantity",default=0)
    
    door_qty: IntProperty(name="Door Quantity",default=0)
    drawer_front_qty: IntProperty(name="Drawer Front Quantity",default=0)
    hamper_front_qty: IntProperty(name="Hamper Front Quantity",default=0)
    drawer_box_qty: IntProperty(name="Drawer Box Quantity",default=0)
    molding_qty: FloatProperty(name="Molding Quantity",default=0)
    
    price_adjustments: CollectionProperty(name="Price Adjustments",type=PROPS_Price_Adjustment)
    
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
        self.pole_cup_qty = 0
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
        self.project_total = 0
        self.accessory_price_total = 0

    def calculate_price(self,context):
        '''
            This function calculates the price of the current scene
        '''
        for assembly in scene_assemblies(context):

            props = assembly.obj_bp.sn_closets
            item_name = assembly.obj_bp.snap.name_object if assembly.obj_bp.snap.name_object != "" else assembly.obj_bp.name
            
            if props.is_panel_bp:
                calculate_material_price(assembly, get_material_price(assembly))
            
            if props.is_shelf_bp:
                calculate_material_price(assembly, get_material_price(assembly))       
                calculate_shelf_hardware_price(assembly)
            
            if props.is_toe_kick_bp:
                calculate_material_price(assembly, get_material_price(assembly))
            
            if props.is_filler_bp:
                calculate_material_price(assembly, get_material_price(assembly))
            
            if props.is_cleat_bp:
                calculate_material_price(assembly, get_material_price(assembly))
            
            if props.is_shelf_lip_bp:
                calculate_material_price(assembly, get_material_price(assembly))
            
            if props.is_divider_bp:
                calculate_material_price(assembly, get_material_price(assembly))
            
            if props.is_back_bp:
                calculate_material_price(assembly, get_material_price(assembly))
            
            if props.is_hanging_rod:
                calculate_rod_price(assembly, get_rod_price(assembly), get_pole_cup_price(assembly))
            
            if props.is_door_bp:
                calculate_door_material_price(assembly, get_material_price(assembly))
                calculate_door_hinge_price(assembly)
            
            if props.is_drawer_front_bp:
                calculate_drawer_front_material_price(assembly)
            
            if props.is_hamper_front_bp:
                calculate_hamper_front_material_price(assembly)

            if props.is_hamper_insert_bp:
                calculate_hamper_price(assembly, get_slide_price(assembly))
                
            if props.is_basket_bp:
                calculate_basket_price(assembly, get_slide_price(assembly))
            
            if props.is_drawer_box_bp:
                calculate_drawer_box_price(assembly, get_slide_price(assembly))
                # calc slide price
            
            if props.is_handle:
                calculate_pull_price(assembly, get_pull_price(assembly))                   
            
            if props.is_spacer_bp:
                calculate_spacer_price(assembly)          
            
            if props.is_shelf_fence_bp:
                calculate_shelf_fence_price(assembly)

            if props.is_accessory_bp:
                calculate_accessory_price(assembly, item_name)

        for obj in scene_molding(context):
            props = obj.sn_closets
            
            if props.is_crown_molding or props.is_base_molding:
                calculate_molding_price(obj)

        calculate_total_price()

    def export_properties(self):
        closet_utils.set_room_prop("Closet Library: Material Price Total",str(self.material_price_total))
        closet_utils.set_room_prop("Closet Library: Hardware Price Total",str(self.hardware_price_total))
        closet_utils.set_room_prop("Closet Library: Door and Drawer Front Price Total",str(self.door_drawer_price_total))
        closet_utils.set_room_prop("Closet Library: Molding Price Total",str(self.molding_price_total))
        closet_utils.set_room_prop("Closet Library: Hanging Rod Price Total",str(self.hanging_rod_price_total))
        
        project_total = self.material_price_total + self.hardware_price_total + self.door_drawer_price_total + self.molding_price_total + self.hanging_rod_price_total
        
        closet_utils.set_room_prop("Closet Library: Closet Price Total",str(project_total))
        closet_utils.set_room_prop("Closet Library: Sheet Material Sq Ft Total",str(self.sheet_material_qty))
        closet_utils.set_room_prop("Closet Library: Hanging Rod LFt Total",str(self.hanging_rod_qty))
        closet_utils.set_room_prop("Closet Library: Pull Qty",str(self.pull_qty))
        closet_utils.set_room_prop("Closet Library: Slide Qty",str(self.slide_qty))
        closet_utils.set_room_prop("Closet Library: Cam Qty",str(self.cam_qty))
        closet_utils.set_room_prop("Closet Library: Hinge Qty",str(self.hinge_qty))
        closet_utils.set_room_prop("Closet Library: Shelf Pin Qty",str(self.shelf_pin_qty))
        closet_utils.set_room_prop("Closet Library: Wire Basket Qty",str(self.wire_basket_qty))
        closet_utils.set_room_prop("Closet Library: Hamper Qty",str(self.hamper_qty))
        closet_utils.set_room_prop("Closet Library: Door Qty",str(self.door_qty))
        closet_utils.set_room_prop("Closet Library: Drawer Front Qty",str(self.drawer_front_qty))
        closet_utils.set_room_prop("Closet Library: Drawer Box Qty",str(self.drawer_box_qty))
        closet_utils.set_room_prop("Closet Library: Molding Qty",str(self.molding_qty))
        
        # closet_utils.set_room_prop("Closet Library: Pull Name",self.pull_name)
        # closet_utils.set_room_prop("Closet Library: Slide Name",self.slide_name)
        # closet_utils.set_room_prop("Closet Library: Slide Name",self.hinge_name)

    def draw(self,layout):
        main_box = layout.box()

        row = main_box.row()
        row.scale_y = 1.3
        row.operator(PRICING_PROPERTY_NAMESPACE + ".calculate_price",icon='FILE_TICK')
        row.prop(self,'auto_calculate_on_save',text="Auto Calculate on Save")        
        
        main_col = main_box.column(align=True)
        
        row = main_col.row(align=True)
        row.scale_y = 1.1
        # row.prop_enum(self, "pricing_tabs", 'SETUP', icon='PREFERENCES', text="Setup")
        row.prop_enum(self, "pricing_tabs", 'PRICING', icon='PREFERENCES', text="Pricing Info")
        
        if self.pricing_tabs == 'SETUP':

            box = main_col.box()
            box.label(text="Sheet Material Costs:")
            
            row = box.row()
            row.label(text="Panels Price Per Unit:")
            row.prop(self,'material_price_per_unit',text="")
            
            row = box.row()
            row.label(text="Shelf Price Per Unit:")
            row.prop(self,'material_price_per_unit',text="")          
            
            row = box.row()
            row.label(text="Cleat Price Per Unit:")
            row.prop(self,'material_price_per_unit',text="")            
            
            row = box.row()
            row.label(text="Toe Kick Price Per Unit:")
            row.prop(self,'material_price_per_unit',text="")              
            
            box = main_col.box()
            box.label(text="Solid Stock Costs:")            
            
            row = box.row()
            row.label(text="Hanging Rod Price Per Unit:")
            row.prop(self,'hanging_rod_price_per_unit',text="")          
            
            row = box.row()
            row.label(text="Hanging Rail Price Per Unit:")
            row.prop(self,'hanging_rail_price_per_unit',text="")              
            
            box = main_col.box()
            box.label(text="Hardware Material Costs:")
            
            row = box.row()
            row.label(text="Hinge Price Per Unit:")
            row.prop(self,'material_price_per_unit',text="")
            
            row = box.row()
            row.label(text="Cam Price Per Unit:")
            row.prop(self,'material_price_per_unit',text="")
            
            row = box.row()
            row.label(text="Shelf Pin Price Per Unit:")
            row.prop(self,'material_price_per_unit',text="")
            
            row = box.row()
            row.label(text="Pull Price Per Unit:")
            row.prop(self,'material_price_per_unit',text="")    
            
            row = box.row()
            row.label(text="Slides Price Per Unit:")
            row.prop(self,'material_price_per_unit',text="")
            
        if self.pricing_tabs == 'PRICING':
            
            box = main_col.box()
            col = box.column()
            col.label(text="Material Price: " + sn_unit.draw_dollar_price(self.material_price_total))
            col.label(text="Square Footage Quantity: " + str(round(self.sheet_material_qty,2)),icon='BLANK1')
            
            col.separator()
            
            col.label(text="Hanging Rod Price: " + sn_unit.draw_dollar_price(self.hanging_rod_price_total)) 
            col.label(text="Hanging Rod Linear Footage Quantity: " + str(round(self.hanging_rod_qty,2)),icon='BLANK1')
            
            col.separator()
            
            col.label(text="Molding Price: " + sn_unit.draw_dollar_price(self.molding_price_total)) 
            col.label(text="Linear Footage Quantity: " + str(round(self.molding_qty,2)),icon='BLANK1')
            
            col.separator()
            
            col.label(text="Hardware Price: " + sn_unit.draw_dollar_price(self.hardware_price_total))
            if self.pull_qty != 0:
                col.label(text="Pull Quantity: " + str(self.pull_qty),icon='BLANK1')
            if self.slide_qty != 0: 
                col.label(text="Drawer Slide Quantity: " + str(self.slide_qty),icon='BLANK1') 
            if self.spacer_qty != 0:
                col.label(text="Drawer Spacer Quantity: " + str(self.spacer_qty),icon='BLANK1')
            if self.wire_basket_qty != 0:
                col.label(text="Wire Basket Quantity: " + str(self.wire_basket_qty),icon='BLANK1')
            if self.hamper_qty != 0:
                col.label(text="Hamper Quantity: " + str(self.hamper_qty),icon='BLANK1')
            if self.cam_qty != 0:
                col.label(text="Cam Quantity: " + str(self.cam_qty),icon='BLANK1')
            if self.hinge_qty != 0: 
                col.label(text="Hinge Quantity: " + str(self.hinge_qty),icon='BLANK1')
            if self.shelf_pin_qty != 0:
                col.label(text="Shelf Pin Quantity: " + str(self.shelf_pin_qty),icon='BLANK1')
            if self.shelf_fence_qty != 0:
                col.label(text="Shelf Fence Quantity: " + str(self.shelf_fence_qty),icon='BLANK1')
            if self.pole_cup_qty != 0:
                col.label(text="Pole Cup Quantity: " + str(self.pole_cup_qty),icon='BLANK1')
            
            col.separator()

            col.label(text="Accessories Price: " + sn_unit.draw_dollar_price(self.accessory_price_total))

            col.separator()
            
            col.label(text="Door & Drawer Front Price: " + sn_unit.draw_dollar_price(self.door_drawer_price_total))
            if self.door_qty != 0:
                col.label(text="Door Quantity: " + str(self.door_qty),icon='BLANK1')
            if self.drawer_front_qty != 0:
                col.label(text="Drawer Front Quantity: " + str(self.drawer_front_qty),icon='BLANK1')
            if self.hamper_front_qty != 0:
                col.label(text="Hamper Front Quantity: " + str(self.hamper_front_qty),icon='BLANK1')
            if self.drawer_box_qty != 0: 
                col.label(text="Drawer Box Quantity: " + str(self.drawer_box_qty),icon='BLANK1')
            
            col.separator()

            col.label(text="Total Project Price: " + sn_unit.draw_dollar_price(self.project_total))
            
            for price_adjustment in self.price_adjustments:
                price_adjustment.draw(col)


class SN_PT_Closet_Pricing_Setup(Panel):
    bl_label = "Closet Pricing"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text='',icon='BLANK1')

    def draw(self, context):
        props = get_pricing_props()
        props.draw(self.layout)


# REGISTER CLASSES
bpy.utils.register_class(OPERATOR_Calculate_Price)
bpy.utils.register_class(PROPS_Pricing)
bpy.utils.register_class(SN_PT_Closet_Pricing_Setup)
exec("bpy.types.Scene." + PRICING_PROPERTY_NAMESPACE + "= PointerProperty(type = PROPS_Pricing)")


# AUTO CALL OPERATOR ON SAVE
@bpy.app.handlers.persistent
def calculate_pricing(scene=None):
    props = get_pricing_props()
    if props.auto_calculate_on_save:
        exec("bpy.ops." + PRICING_PROPERTY_NAMESPACE + ".calculate_price()")
bpy.app.handlers.save_pre.append(calculate_pricing)
