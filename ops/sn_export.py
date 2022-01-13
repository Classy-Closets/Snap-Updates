import math
import os
import xml.etree.ElementTree as ET
import filecmp
import re

import bpy
import bmesh
from bpy.types import Operator

from snap import sn_types
from snap import sn_utils
from snap import sn_unit
from snap import sn_xml
from snap import sn_db
from snap.libraries.closets.data import data_drawers
from ..libraries.closets.common import common_lists

try:
    from ..developer_utils import debug_xml_export
except ImportError as e:
    print(e.msg)


BL_DIR = os.path.dirname(bpy.app.binary_path)
CSV_PATH = os.path.join(BL_DIR, "data", "CCItems.csv")
DIR_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', "sn_db")


def get_slide_size(slide_type, assembly):
    closet_props = assembly.obj_bp.sn_closets

    if closet_props.is_drawer_box_bp:
        drawer_depth = sn_unit.meter_to_inch(assembly.obj_y.location.y)

    if closet_props.is_drawer_side_bp:
        drawer_box_assembly = sn_types.Assembly(assembly.obj_bp.parent)
        drawer_depth = sn_unit.meter_to_inch(drawer_box_assembly.obj_y.location.y)

    mat_props = bpy.context.scene.closet_materials
    sizes = []
    slide_type = mat_props.get_drawer_slide_type()

    for size in slide_type.sizes:
        sizes.append(size)

    sizes.reverse()

    for size in sizes:
        if drawer_depth >= float(size.slide_length_inch):
            return size


def get_hardware_sku(obj_bp, assembly, item_name):
    conn = sn_db.connect_db()
    cursor = conn.cursor()
    # sku = "Unknown"
    # Return Special Order SKU as default if nothing is found
    sku = 'SO-0000001'



    #Pull
    if assembly.obj_bp.sn_closets.is_handle:
        pull_cat = bpy.context.scene.sn_closets.closet_options.pull_category
        pull_name = bpy.context.scene.sn_closets.closet_options.pull_name
        vendor_id = item_name[:10] # use vendor code in item name for lookup (123.45.678)

        cursor.execute(
            "SELECT\
                sku\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'AC' AND\
                VendorItemNum ='{}'\
            ;".format(vendor_id, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )

        rows = cursor.fetchall()

        if len(rows) == 0:
            print("SKU match not found for selected part - VendorItemNum: {}".format(vendor_id))
            print("Special Order Sku Returned: SO-0000001")
            return 'SO-0000001'
        for row in rows:
            sku = row[0]
            #print("FOUND PULL SKU: ", sku)            
        
        conn.close()
        return sku

    #Hinge
    if assembly.obj_bp.sn_closets.is_hinge or 'Hinge' in item_name:
        hinge_name = bpy.context.scene.sn_closets.closet_options.hinge_name

        cursor.execute(
            "SELECT\
                sku\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'HW' AND\
                Name LIKE'{}'\
            ;".format("%" + hinge_name + "%", CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("SKU match not found for selected part - Hinge Name: {}".format(hinge_name))
            print("Special Order Sku Returned: SO-0000001")
            return 'SO-0000001'
        for row in rows:
            sku = row[0]
            # print("FOUND HINGE SKU: ", sku)            
        
        conn.close()
        return sku

    # Hinge Plate
    if "Mounting Plate" in item_name and not assembly.obj_bp.get("IS_BP_GARAGE_LEG"):
        cursor.execute(
            "SELECT\
                sku\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'HW' AND\
                Name LIKE'{}'\
            ;".format("%" + item_name + "%", CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("SKU match not found for selected part - Item Name: {}".format(item_name))
            print("Special Order Sku Returned: SO-0000001")
            return 'SO-0000001'
        for row in rows:
            sku = row[0]
            #print("FOUND MOUNTING PLATE SKU: ", sku)            
        
        conn.close()
        return sku

    # Jewelry / Suspended Inserts
    if assembly.obj_bp.get("IS_BP_DRAWER_BOX"):
        is_jewelry = "jewelry" in item_name.lower()
        is_velvet_liner = "velvet" in item_name.lower()
        if is_jewelry or is_velvet_liner:
            cursor.execute(
                "SELECT\
                    sku\
                FROM\
                    {CCItems}\
                WHERE\
                    ProductType == 'AC' AND\
                    Name == '{}' \
                ;".format(
                    item_name,
                    CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location
                )
            )
            rows = cursor.fetchall()

            for row in rows:
                sku = row[0]
            
            conn.close()
            return sku
        
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
                    sku\
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

            if len(rows) == 0:
                print("SKU match not found for selected part: {}".format(slide_name))
                print("Special Order Sku Returned: SO-0000001")
                return 'SO-0000001'
            for row in rows:
                sku = row[0]
                # print("FOUND SLIDE SKU: ", sku)

            conn.close()
            return sku
        else:
            # print("Found Non Standard Slide: ", item_name)
            cursor.execute(
                "SELECT\
                    sku\
                FROM\
                    {CCItems}\
                WHERE\
                    ProductType == 'HW' AND\
                    DisplayName LIKE '{}'\
                ;".format(
                    "%" + item_name + "%",
                    CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location
                )
            )
            rows = cursor.fetchall()

            if len(rows) == 0:
                print("SKU match not found for selected part: {}".format(item_name))
                print("Special Order Sku Returned: SO-0000001")
                return 'SO-0000001'
            for row in rows:
                sku = row[0]
                # print("FOUND SLIDE SKU: ", sku)

            conn.close()
            return sku



    # Hamper Laundry Bag
    if "Cloth Laundry Bag" in item_name:
        basket_width = sn_unit.meter_to_inch(assembly.obj_x.location.x)

        if basket_width > 18.0:
            bag_name = item_name + " 24"
        else:
            bag_name = item_name + " 18"

        cursor.execute(
            "SELECT\
                sku\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'AC' AND\
                Name LIKE'{}'\
            ;".format("%" + bag_name + "%", CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("SKU match not found for selected part: {}".format(bag_name))
            print("Special Order Sku Returned: SO-0000001")
            return 'SO-0000001'
        for row in rows:
            sku = row[0]
            #print("FOUND LAUNDRY BAG SKU: ", sku)            
        
        conn.close()
        return sku

    # Hamper Tilt Out Laundry Bag
    if "HAMPER TILT OUT" in item_name:
        cursor.execute(
            "SELECT\
                sku\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'AC' AND\
                Name LIKE'{}'\
            ;".format("%" + item_name + "%", CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("SKU match not found for selected part: {}".format(item_name))
            print("Special Order Sku Returned: SO-0000001")
            return 'SO-0000001'
        for row in rows:
            sku = row[0]
            # print("FOUND LAUNDRY BAG SKU: ", sku)            
        
        conn.close()
        return sku

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
            sku\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'AC' AND\
                VendorItemNum ='{}'\
            ;".format(vendor_id, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("SKU match not found for selected part - VendorID: {}".format(vendor_id))
            print("Special Order Sku Returned: SO-0000001")
            return 'SO-0000001'
        for row in rows:
            sku = row[0]
            #print("FOUND HAMPER BASKET SKU: ", sku)            
        
        conn.close()
        return sku        

    #Hamper Brake Flaps
    if "Hamper Brake Flap Left" in item_name or "Hamper Brake Flap Right" in item_name:
        cursor.execute(
            "SELECT\
                sku\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'AC' AND\
                Name LIKE'{}'\
            ;".format("%" + item_name + "%", CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("SKU match not found for selected part: {}".format(item_name))
            print("Special Order Sku Returned: SO-0000001")
            return 'SO-0000001'
        for row in rows:
            sku = row[0]
            #print("FOUND BRAKE FLAP SKU: ", sku)            
        
        conn.close()
        return sku

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
                sku\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'AC' AND\
                Name LIKE'{}'\
            ;".format("%" + rack_name + "%", CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("SKU match not found for selected part: {}".format(rack_name))
            print("Special Order Sku Returned: SO-0000001")
            return 'SO-0000001'
        for row in rows:
            sku = row[0]
            #print("FOUND HAMPER RACK SKU: ", sku)            
        
        conn.close()
        return sku        

    #Rod
    if assembly.obj_bp.sn_closets.is_hanging_rod:
        # print("is_hanging_rod", assembly.obj_bp)
        item_name = bpy.context.scene.sn_closets.closet_options.rods_name
        vendor_id = item_name[-10:]

        cursor.execute(
            "SELECT\
            sku\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'AC' AND\
                VendorItemNum ='{}'\
            ;".format(vendor_id, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("SKU match not found for selected part - VendorItemNum: {}".format(vendor_id))
            print("Special Order Sku Returned: SO-0000001")
            return 'SO-0000001'
        for row in rows:
            sku = row[0]
            #print("FOUND HANGING ROD SKU: ", sku)            
        
        conn.close()
        return sku

    #Rod Cup
    if "Pole Cup" in item_name:
        name = bpy.context.scene.sn_closets.closet_options.pole_cup_name
        cursor.execute(
            "SELECT\
                sku\
            FROM\
                {CCItems}\
            WHERE\
                ProductType IN ('AC', 'HW') AND\
                Name LIKE'%{}%'\
            ;".format(name, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("SKU match not found for selected part: {}".format(name))
            print("Special Order Sku Returned: SO-0000001")
            return 'SO-0000001'
        for row in rows:
            sku = row[0]
            #print("FOUND POLE CUP SKU:", sku)

        conn.close()
        return sku
    

    #KD Fitting
    if "KD Fitting" in item_name:
        mat_props = bpy.context.scene.closet_materials
        name = mat_props.kd_fitting_color
        cursor.execute(
            "SELECT\
                sku\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'HW' AND\
                Name LIKE'%{}%'\
            ;".format(name, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("SKU match not found for selected part - Item Name: {}".format(name))
            print("Special Order Sku Returned: SO-0000001")
            return 'SO-0000001'
        for row in rows:
            sku = row[0]
            #print("FOUND KD FITTING SKU:", sku)

        conn.close()
        return sku

    #Pegs
    if "Peg Chrome" in item_name:
        cursor.execute(
            "SELECT\
                sku\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'HW' AND\
                Name LIKE'{}'\
            ;".format("%peg%chrome%", CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("SKU match not found for selected part: {}".format(item_name))
            print("Special Order Sku Returned: SO-0000001")
            return 'SO-0000001'
        for row in rows:
            sku = row[0]
            #print("FOUND CHROME PEG SKU: ", sku)

        conn.close()
        return sku

    #Door lock
    if item_name == "Door Lock":
        print("DOOR LOCK")
        cursor.execute(
            "SELECT\
                sku\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'AC' AND\
                VendorItemNum =='{}'\
            ;".format("C8055-14A", CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("SKU match not found for selected part: {}".format(item_name))
            print("Special Order Sku Returned: SO-0000001")
            return 'SO-0000001'
        for row in rows:
            sku = row[0]
            print("FOUND DOOR LOCK SKU:", sku)

        conn.close()
        return sku

    #Door lock cam
    if item_name == "Door Lock Cam":
        print("DOOR LOCK CAM")
        cursor.execute(
            "SELECT\
                sku\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'AC' AND\
                VendorItemNum =='{}'\
            ;".format("C7004-2C", CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("SKU match not found for selected part: {}".format(item_name))
            print("Special Order Sku Returned: SO-0000001")
            return 'SO-0000001'
        for row in rows:
            sku = row[0]
            print("FOUND LOCK CAM SKU:", sku)

        conn.close()
        return sku

    #Door lock latch finger
    if item_name == "Door Lock Latch":
        print("DOOR LOCK LATCH")

        cursor.execute(
            "SELECT\
                sku\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'AC' AND\
                VendorItemNum =='{}'\
            ;".format("245.74.200", CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("SKU match not found for selected part: {}".format(item_name))
            print("Special Order Sku Returned: SO-0000001")
            return 'SO-0000001'
        for row in rows:
            sku = row[0]
            print("FOUND LATCH SKU:", sku)

        conn.close()
        return sku

    #----------Closet Accessories
    # Valet Rod
    if 'Valet Rod' in item_name:
        parent_assembly = sn_types.Assembly(assembly.obj_bp.parent)
        valet_category = parent_assembly.get_prompt('Valet Category')
        valet_length = parent_assembly.get_prompt('Valet Length')
        metal_color = parent_assembly.get_prompt("Metal Color")
        valet_category_name = 'Synergy'
        metal_color_name = 'Chrome'
        prompts = [valet_category, valet_length, metal_color]

        if all(prompts):
            if valet_category.get_value() == 1:
                valet_category_name = 'ELITE'

            if metal_color.get_value() == 0:
                metal_color_name = 'Chrome'
            elif metal_color.get_value() == 1:
                metal_color_name = 'Matt Alum'
            elif metal_color.get_value() == 2:
                metal_color_name = 'Matt Nickel'
            elif metal_color.get_value() == 3:
                metal_color_name = 'Matt Gold'
            elif metal_color.get_value() == 4:
                metal_color_name = 'ORB'
            elif metal_color.get_value() == 5:
                metal_color_name = 'Slate'

            if valet_category.get_value() == 1:
                valet_category_name = 'ELITE'
                if metal_color.get_value() == 0:
                    metal_color_name = 'Pol Chrome'
                metal_color_name = metal_color_name.upper()

            cursor.execute(
                "SELECT\
                    sku\
                FROM\
                    {CCItems}\
                WHERE\
                    ProductType == 'AC' AND\
                    Name IN ('{category} Valet Rail {color} {length}', '{category} VALET ROD {color} {length}')\
                ;".format(
                    CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location,
                    category=valet_category_name,
                    color=metal_color_name,
                    length=valet_length.combobox_items[valet_length.get_value()].name)
            )
            rows = cursor.fetchall()

            if len(rows) == 0:
                print("SKU match not found for selected part: {}".format(item_name))
                print("Special Order Sku Returned: SO-0000001")
                return 'SO-0000001'
            for row in rows:
                sku = row[0]
                # print("FOUND VALET ROD SKU:", sku)

            conn.close()
        return sku

    # Valet Rod 2
    if item_name == "Valet Rod 2":
        print(item_name)
        sku = "AC-0000176"
        return sku

    # Wire Basket
    if "Wire Basket" in item_name:
        print(item_name)
        sku = "AC-0000001"
        return sku

    # Pants Rack
    if item_name == "Pants Rack":
        print(item_name)
        return sku

    # Tie Rack
    if "IS_BP_TIE_RACK" in assembly.obj_bp:
        parent_assembly = sn_types.Assembly(assembly.obj_bp.parent)
        tie_rack_category = assembly.get_prompt('Tie Rack Category')
        synergy_tie_rack_length = assembly.get_prompt('Synergy Tie Rack Length')
        elite_tie_rack_length = assembly.get_prompt('Elite Tie Rack Length')
        tie_rack_length = synergy_tie_rack_length
        metal_color = assembly.get_prompt("Metal Color")
        tie_rack_category_name = 'Synergy'
        metal_color_name = 'Chrome'
        prompts = [tie_rack_category, tie_rack_length, metal_color]

        if all(prompts):
            if metal_color.get_value() == 0:
                metal_color_name = 'Chrome'
            elif metal_color.get_value() == 1:
                metal_color_name = 'Matt Alum'
            elif metal_color.get_value() == 2:
                metal_color_name = 'Matt Nickel'
            elif metal_color.get_value() == 3:
                metal_color_name = 'Matt Gold'
            elif metal_color.get_value() == 4:
                metal_color_name = 'ORB'
            elif metal_color.get_value() == 5:
                metal_color_name = 'Slate'

            if tie_rack_category.get_value() == 1:
                tie_rack_category_name = 'ELITE'
                if metal_color.get_value() == 0:
                    metal_color_name = 'Pol Chrome'
                metal_color_name = metal_color_name.upper()
                tie_rack_length = elite_tie_rack_length

            cursor.execute(
                "SELECT\
                    sku\
                FROM\
                    {CCItems}\
                WHERE\
                    ProductType == 'AC' AND\
                    Name IN ('{category} Tie {color} {length}', '{category} TIE RACK {color} {length}')\
                ;".format(
                    CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location,
                    category=tie_rack_category_name,
                    color=metal_color_name,
                    length=tie_rack_length.combobox_items[tie_rack_length.get_value()].name)
            )
            rows = cursor.fetchall()

            if len(rows) == 0:
                print("SKU match not found for selected part: {}".format(assembly.obj_bp))
                print("Special Order Sku Returned: SO-0000001")
                return 'SO-0000001'
            for row in rows:
                sku = row[0]
                print("FOUND TIE RACK SKU:", sku)

            conn.close()
        return sku

    # Belt Rack
    if "IS_BP_BELT_RACK" in assembly.obj_bp:
        parent_assembly = sn_types.Assembly(assembly.obj_bp.parent)
        belt_rack_category = assembly.get_prompt('Belt Rack Category')
        synergy_belt_rack_length = assembly.get_prompt('Synergy Belt Rack Length')
        elite_belt_rack_length = assembly.get_prompt('Elite Belt Rack Length')
        belt_rack_length = synergy_belt_rack_length
        metal_color = assembly.get_prompt("Metal Color")
        belt_rack_category_name = 'Synergy'
        metal_color_name = 'Chrome'
        prompts = [belt_rack_category, belt_rack_length, metal_color]

        if all(prompts):
            if belt_rack_category.get_value() == 1:
                belt_rack_category_name = 'ELITE'

            if metal_color.get_value() == 0:
                metal_color_name = 'Chrome'
            elif metal_color.get_value() == 1:
                metal_color_name = 'Matt Alum'
            elif metal_color.get_value() == 2:
                metal_color_name = 'Matt Nickel'
            elif metal_color.get_value() == 3:
                metal_color_name = 'Matt Gold'
            elif metal_color.get_value() == 4:
                metal_color_name = 'ORB'
            elif metal_color.get_value() == 5:
                metal_color_name = 'Slate'

            if belt_rack_category.get_value() == 1:
                belt_rack_category_name = 'ELITE'
                if metal_color.get_value() == 0:
                    metal_color_name = 'Pol Chrome'
                metal_color_name = metal_color_name.upper()
                belt_rack_length = elite_belt_rack_length

            cursor.execute(
                "SELECT\
                    sku\
                FROM\
                    {CCItems}\
                WHERE\
                    ProductType == 'AC' AND\
                    Name IN ('{category} Belt {color} {length}', '{category} BELT RACK {color} {length}')\
                ;".format(
                    CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location,
                    category=belt_rack_category_name,
                    color=metal_color_name,
                    length=belt_rack_length.combobox_items[belt_rack_length.get_value()].name)
            )
            rows = cursor.fetchall()

            if len(rows) == 0:
                print("SKU match not found for selected part: {}".format(assembly.obj_bp))
                print("Special Order Sku Returned: SO-0000001")
                return 'SO-0000001'
            for row in rows:
                sku = row[0]
                # print("FOUND BELT RACK SKU:", sku)

            conn.close()
        return sku

    #Robe Hook
    if item_name == "Robe Hook":
        print(item_name)
        sku = "AC-0000203"
        return sku

    # Garage Leg Hardware
    if 'IS_BP_GARAGE_LEG' in assembly.obj_bp:
        if item_name == 'Plastic Leg Mounting Plates':
            return 'AC-0000491'
        elif item_name == '80mm Plastic Legs':
            return 'AC-0000487'
        elif item_name == '100mm Plastic Legs':
            return 'AC-0000488'
        elif item_name == '120mm Plastic Legs':
            return 'AC-0000489'
        elif item_name == '150mm Plastic Legs':
            return 'AC-0000490'
        elif item_name == 'Metal Leg Mounting Plates':
            return 'AC-0000482'
        elif item_name == 'Thread Inserts':
            return 'AC-0000483'
        elif item_name == 'Metal Leg Levelers':
            return 'AC-0000481'
        # elif item_name == 'Full Length Nickel Legs':
        #     vendor_item_number = '635.20.066'
        elif item_name == 'Length of Brushed Steel Legs (in feet)':
            return 'AC-0000484'
        elif item_name == 'Length Of Black Matte Legs (in feet)':
            return 'AC-0000485'
        elif item_name == 'Length Of Polished Chrome Legs (in feet)':
            return 'AC-0000486'
        else:
            print("Unkown vendor item number for: ", item_name)
            return sku
    
    print("No Hardware or Accessory SKU found. Special Order SKU number returned")
    return sku 


def get_export_prompts(obj_bp):
    """ Used in create_fluid_project_xml
        this collects all of the needed product prompts for the 121 product match
    """
    
    prompts = {}
    
    def add_prompt(prompt):
        if prompt.Type == 'NUMBER':
            prompts[prompt.name] = str(prompt.float_value)
        if prompt.Type == 'QUANTITY':
            prompts[prompt.name] = str(prompt.quantity_value)
        if prompt.Type == 'COMBOBOX':
            prompts[prompt.name] = str(prompt.COL_EnumItem[prompt.combobox_index].name)
        if prompt.Type == 'CHECKBOX':
            prompts[prompt.name] = str(prompt.checkbox_value)
        if prompt.Type == 'TEXT':
            prompts[prompt.name] = str(prompt.text_value)
        if prompt.Type == 'DISTANCE':
            prompts[prompt.name] = str(round(sn_unit.meter_to_active_unit(prompt.distance_value),2))
        if prompt.Type == 'ANGLE':
            prompts[prompt.name] = str(prompt.angle_value)
        if prompt.Type == 'PERCENTAGE':
            prompts[prompt.name] = str(prompt.factor_value)
        if prompt.Type == 'PRICE':
            prompts[prompt.name] = str(prompt.float_value)
    
    def add_child_prompts(obj):
        for child in obj.children:
            if child.get('IS_BP_ASSEMBLY'):
                add_prompts(child)
            if len(child.children) > 0:
                add_child_prompts(child)
        
    def add_prompts(obj):
        for prompt in obj.snap.PromptPage.COL_Prompt:
            if prompt.export:
                add_prompt(prompt)
                
    add_prompts(obj_bp)
    add_child_prompts(obj_bp)

    return prompts


def get_cutpart(obj_bp):
    for child in obj_bp.children:
        if child.type == 'MESH' and child.snap.type_mesh == 'CUTPART':
            return child


class OPS_Export_XML(Operator):
    bl_idname = "sn_export.export_xml"
    bl_label = "Export XML File"
    bl_description = "This will export an XML file. The file must be saved first."

    walls = []
    products = []
    buyout_products = []

    cover_cleat_lengths = []
    cover_cleat_bp = None

    single_exposed_flat_crown = []
    top_edgebanded_flat_crown = []
    flat_crown_heights = []
    flat_crown_lengths = []
    flat_crown_bp = None

    crown_molding_lengths = []
    crown_molding_bp = None

    inverted_base_lengths = []
    inverted_base_bp = None

    base_molding_lengths = []
    base_molding_bp = None

    tk_skin_heights = []
    tk_skin_lengths = []
    tk_skin_bp = None

    hang_rod_lengths = []
    hang_rod_bp = None
    hang_rods_collected = False

    cleat_bp = None
    is_wrap_around = False

    plastic_leg_list = []
    metal_leg_list = []
    
    buyout_materials = []
    edgeband_materials = {}
    solid_stock_materials = {}

    op_groups = []
    labels = []

    mfg_node = None

    job_number = 0

    job_count = 0 #Does not currently increment
    item_count = 0 
    assembly_count = 0 
    part_count = 0
    mfg_count = 0 #Does not currently increment
    label_count = 0
    mat_count = 0
    op_count = 0
    or_count = 0

    xml = None
    xml_path: bpy.props.StringProperty(name="XML Path", subtype='DIR_PATH')

    debugger = None

    top_shelf_sizes = (60.0, 72.0, 84.0, 96.0)
    top_shelf_offset = 6.0    

    @classmethod
    def poll(cls, context):
        if bpy.data.filepath != "":
            return True
        else:
            return False

    def distance(self,distance):
        return str(math.fabs(round(sn_unit.meter_to_active_unit(distance),2)))
    
    def location(self,location):
        return str(round(sn_unit.meter_to_active_unit(location),2))
    
    def angle(self,angle):
        return str(round(math.degrees(angle),2))
    
    def clear_and_collect_data(self,context):
        for product in self.products:
            self.products.remove(product)
        
        for wall in self.walls:
            self.walls.remove(wall)

        #bpy.ops.fd_material.get_materials()

        for scene in bpy.data.scenes:
            if scene.snap.scene_type == 'NONE':
                for obj in scene.objects:
                    if not obj.snap.dont_export:
                        if 'IS_BP_WALL' in obj:
                            self.walls.append(obj)
                        if "IS_BP_ASSEMBLY" in obj or "IS_ASSEMBLY_BP" in obj:  # TODO: remove IS_ASSEMBLY_BP
                            if obj.snap.type_group == 'PRODUCT':
                                self.products.append(obj)

    def get_var_sec_length(self, x):
        increment = 3
        offset = sn_unit.inch(2.5)
        max_len = 97

        for length in range(increment, max_len, increment):
            length = sn_unit.inch(length)
            if x < length:
                if length - x <= offset:
                    return length + sn_unit.inch(increment)
                else:
                    return length    
            
        return length    

    def is_variable_section(self, assembly):
        opening_name = assembly.obj_bp.sn_closets.opening_name
        if opening_name:
            carcass_bp = sn_utils.get_closet_bp(assembly.obj_bp)
            carcass_assembly = sn_types.Assembly(carcass_bp)
            variable_section = carcass_assembly.get_prompt("CTF Opening {}".format(opening_name)).get_value()
            
            return variable_section

        else:
            return False

    def is_var_width_toe_kick(self,assembly):
        p_assembly = sn_types.Assembly(assembly.obj_bp.parent)

        if p_assembly.obj_bp.sn_closets.is_toe_kick_insert_bp:
            var_width = p_assembly.get_prompt("Variable Width")
            if var_width:
                if var_width.get_value():
                    return True
        return False

    def is_var_height_toe_kick(self,assembly):
        p_assembly = sn_types.Assembly(assembly.obj_bp.parent)

        if p_assembly.obj_bp.sn_closets.is_toe_kick_insert_bp:
            var_height = p_assembly.get_prompt("Variable Height")
            if var_height:
                if var_height.get_value():
                    return True
        return False

    def get_product_z_location(self,product):
        #Height Above Floor
        if product.obj_bp.location.z > 0:
            return product.obj_bp.location.z - math.fabs(product.obj_z.location.z)
        else:
            return product.obj_bp.location.z
    
    def get_part_qty(self,assembly):
        qty = 1
        z_quantity = assembly.get_prompt("Z Quantity")
        x_quantity = assembly.get_prompt("X Quantity")
        if z_quantity:
            qty += z_quantity.get_value() - 1
        
        if x_quantity:
            qty += x_quantity.get_value() - 1
            
        return str(qty)
        
    def get_part_width(self,assembly):
        width = math.fabs(assembly.obj_y.location.y)
        oversize_width = assembly.get_prompt("Oversize Width")

        if oversize_width:
            width += oversize_width.get_value()
        if assembly.obj_bp.sn_closets.is_filler_bp:
            width += sn_unit.inch(2)
            if width < sn_unit.inch(4):
                    width = sn_unit.inch(4)

        if self.is_var_height_toe_kick(assembly):
            #Exclude stringer parts and tk skins
            if not assembly.obj_bp.sn_closets.is_toe_kick_stringer_bp and not assembly.obj_bp.sn_closets.is_toe_kick_skin_bp and not assembly.obj_bp.get('IS_BP_TOE_KICK_END_CAP'):
                width += sn_unit.inch(3.0)

        if assembly.obj_bp.sn_closets.is_closet_bottom_bp:
            against_left_wall = assembly.get_prompt("Against Left Wall")
            against_right_wall = assembly.get_prompt("Against Right Wall")
            if(against_left_wall and against_right_wall):
                if(against_left_wall.get_value()):
                    width += sn_unit.inch(3.0)
                if(against_right_wall.get_value()):
                    width += sn_unit.inch(3.0)

        return self.distance(width)
    
    def get_part_length(self,assembly):
        length = math.fabs(assembly.obj_x.location.x)
        props = assembly.obj_bp.sn_closets
        parent_bp = assembly.obj_bp.parent

        if self.is_variable_section(assembly):
            if props.is_hanging_rod:
                length = self.get_var_sec_length(length)
            if props.is_cleat_bp or props.is_shelf_bp:
                if not props.is_door_bp:
                    length = self.get_var_sec_length(length)

        if self.is_var_width_toe_kick(assembly):
            #Exclude end cap parts
            if not assembly.obj_bp.get('IS_BP_TOE_KICK_END_CAP'):
                length += sn_unit.inch(3.0)

        # TK Endcaps lengths and widths are swapped
        if self.is_var_height_toe_kick(assembly) and assembly.obj_bp.get('IS_BP_TOE_KICK_END_CAP'):
            length += sn_unit.inch(3.0)

        if parent_bp.sn_closets.is_closet_top_bp:
            top_shelf_assembly = sn_types.Assembly(assembly.obj_bp)
            Exposed_Left = top_shelf_assembly.get_prompt("Exposed Left")
            Exposed_Right = top_shelf_assembly.get_prompt("Exposed Right")

            if Exposed_Left and Exposed_Right:
                if Exposed_Left.get_value() == False or Exposed_Right.get_value() == False:
                    print("Oversizing top shelf - length:",sn_unit.meter_to_inch(length))
                    length = self.get_os_top_shelf_length(length)
                    length = sn_unit.inch(length)
                    print("Top shelf oversize length",length)
        
        if parent_bp.sn_closets.is_closet_bottom_bp:
            capping_bottom_assembly = sn_types.Assembly(parent_bp)
            against_left_wall = capping_bottom_assembly.get_prompt("Against Left Wall")
            against_right_wall = capping_bottom_assembly.get_prompt("Against Right Wall")
            if against_left_wall:
                if against_left_wall.get_value():
                    length += sn_unit.inch(3)
            if against_right_wall:
                if against_right_wall.get_value():
                    length += sn_unit.inch(3)

        if assembly.obj_bp.get('IS_BP_PLANT_ON_TOP'):
            if parent_bp.get("IS_BP_L_SHELVES"):
                length += sn_unit.inch(6)

        if assembly.obj_bp.sn_closets.is_cleat_bp:
            if assembly.obj_bp.parent.get("IS_BP_L_SHELVES") or assembly.obj_bp.parent.get("IS_BP_CORNER_SHELVES"):
                current_inches = sn_unit.meter_to_inch(length)
                current_inches = round(current_inches, 2)
                current_inches = math.ceil(current_inches)
                current_inches += 1
                while current_inches % 3 != 0:
                    current_inches += 1
                length = sn_unit.inch_to_millimeter(current_inches) / 1000
                
        return self.distance(length)

    def get_os_top_shelf_length(self, x):
        for i,length in enumerate(self.top_shelf_sizes):
            if sn_unit.meter_to_inch(x) + self.top_shelf_offset >= self.top_shelf_sizes[-1]:
                return self.top_shelf_sizes[-1]

            if sn_unit.meter_to_inch(x) < length:
                if length - sn_unit.meter_to_inch(x) <= self.top_shelf_offset:
                    return self.top_shelf_sizes[i+1]
                else:
                    return self.top_shelf_sizes[i]  
        
    def get_part_x_location(self,obj,value):
        if obj.parent is None or obj.parent.snap.type_group == 'PRODUCT':
            return self.location(value)
        value += obj.parent.location.x
        return self.get_part_x_location(obj.parent,value)

    def get_part_y_location(self,obj,value):
        if obj.parent is None or obj.parent.snap.type_group == 'PRODUCT':
            return self.location(value)
        value += obj.parent.location.y
        return self.get_part_y_location(obj.parent,value)

    def get_part_z_location(self,obj,value):
        if obj.parent is None or obj.parent.snap.type_group == 'PRODUCT':
            return self.location(value)
        value += obj.parent.location.z
        return self.get_part_z_location(obj.parent,value)

    def get_part_comment(self,obj):
        if not obj.snap.comment_2 == "":
            return obj.snap.comment_2
        else:
            return ""
    
    def get_part_category_number(self, assembly, obj, mat_sku, part_name):
        category_number = ""
        material_number = ""
        closet_materials = bpy.context.scene.closet_materials

        if mat_sku != None:
            if "PL" in mat_sku:
                material_number = "11"
            elif "SN" in mat_sku:
                material_number = "12"
            else:
                material_number = "10"
        else:
            material_number = "10"

        # Shelves
        if obj.get("IS_SHELF"):
            is_locked_shelf = assembly.get_prompt("Is Locked Shelf")
            if is_locked_shelf and is_locked_shelf.get_value():
                category_number = material_number + "21"
            else:
                category_number = material_number + "01"
        if obj.get("IS_BP_L_SHELF"):
            is_locked_shelf = assembly.get_prompt("Is Locked Shelf")
            if is_locked_shelf and is_locked_shelf.get_value():
                category_number = material_number + "22"
            else:
                category_number = material_number + "02"
        if obj.get("IS_BP_ANGLE_SHELF"):
            is_locked_shelf = assembly.get_prompt("Is Locked Shelf")
            if is_locked_shelf and is_locked_shelf.get_value():
                category_number = material_number + "23"
            else:
                category_number = material_number + "03"
        if obj.get("IS_BP_SLANTED_SHELF"):
            category_number = material_number + "04"
        if obj.get("IS_BP_PLANT_ON_TOP"):
            category_number = material_number + "11"
        # Pullout shelf catnum = material_number + 12

        # Partitions
        if obj.get("IS_BP_PANEL"):
            if obj.parent.get("IS_BP_ISLAND"):
                category_number = material_number + "33"
            else:
                catnum = assembly.get_prompt("CatNum")
                if catnum:
                    category_number = material_number + str(catnum.get_value())
                else:
                    category_number = material_number + "31"
        if obj.get("IS_BP_MITERED_PARD"):
            category_number = material_number + "35"
        if obj.get("IS_FILLER"):
            category_number = material_number + "64"
        # 22mm Partition catnum = material_number + 34

        # Cleats
        if obj.get("IS_CLEAT"):
            if obj.get("IS_COVER_CLEAT"):
                category_number = material_number + "42"
            else:
                category_number = material_number + "41"
        
        # Melamine Slab Doors
        if obj.get("IS_DOOR"):
            catnum = assembly.get_prompt("CatNum")
            if catnum:
                category_number = material_number + str(catnum.get_value())
            else:
                category_number = material_number + "52"
            # Slab Door with Insert = material_number + 53
            # Slab False Door = material_number + 54
            # Slab Ironing Board Door = material_number + 55

        # Melamine Drawer Face
        if obj.get("IS_BP_DRAWER_FRONT"):
            category_number = material_number + "56"
            # Slab Drawer Front with Insert = material_number + 57

        # Drawer Box
        use_dovetail_construction = assembly.get_prompt("Use Dovetail Construction")
        drawer_material_number = "20"
        if use_dovetail_construction:
            drawer_material_number = "22"
        # Many more drawer material/contruction numbers. These two are all we have in SNaP now
        if obj.get("IS_BP_DRAWER_SUB_FRONT"):
            category_number = drawer_material_number + "01"
        if obj.get("IS_BP_DRAWER_BACK"):
            category_number = drawer_material_number + "02"
        if obj.get("IS_BP_DRAWER_SIDE"):
            category_number = drawer_material_number + "03"
        if obj.get("IS_BP_DRAWER_BOTTOM"):
            category_number = drawer_material_number + "04"
        
        # Melamine Hamper Face
        if obj.get("IS_BP_HAMPER_FRONT"):
            category_number = material_number + "58"
        
        # Backing
        if obj.get("IS_BACK"):
            category_number = material_number + "61"

        # Crown Molding
        if obj.get("IS_BP_CROWN_MOLDING"):
            if "Valance" in part_name:
                category_number = material_number + "62"
            else:
                if mat_sku != None:
                    if "PL" in mat_sku:
                        material_number = "17"
                    else:
                        material_number = "18"
                else:
                    material_number = "17"
                if "Traditional Large" in part_name:
                    category_number = material_number + "02"
                elif "Traditional Small" in part_name:
                    category_number = material_number + "03"
                elif "King George" == part_name:
                    category_number = material_number + "04"
                elif "Ogee" in part_name:
                    category_number = material_number + "23"

        # Strikers
        if obj.get("IS_DOOR_STRIKER"):
            category_number = material_number + "63"

        # Toe Kicks
        if obj.get("IS_BP_TOE_KICK"):
            category_number = material_number + "92"
        if obj.get("IS_BP_TOE_KICK_END_CAP"):
            category_number = material_number + "91"
        if obj.get("IS_BP_TOE_KICK_STRINGER"):
            category_number = material_number + "93"
        if obj.get("IS_BP_TOE_KICK_SKIN"):
            category_number = material_number + "99"

        # Countertop
        if obj.get("IS_BP_COUNTERTOP"):
            parent_obj = obj.parent
            parent_assembly = sn_types.Assembly(parent_obj)
            countertop_type = parent_assembly.get_prompt("Countertop Type")
            if countertop_type:
                # Melamine
                if countertop_type.get_value() == 0:
                    category_number = "9001"

                # HPL
                elif countertop_type.get_value() == 1:
                    category_number = "9002"

                # Granite
                else:
                    category_number = "9004"

            else:
                category_number = "9003"

        # Hardware
        if obj.snap.type_mesh == 'HARDWARE' or obj.sn_closets.is_temp_hardware:
            category_number = "9751"

        # Accessories
        if obj.get("IS_BP_ACCESSORY") or obj.sn_closets.is_accessory_bp:
            category_number = "9701"

        # Wooden Door, Drawer, and Hamper Faces
        if obj.get("IS_DOOR") or obj.get("IS_BP_HAMPER_FRONT") or obj.get("IS_BP_DRAWER_FRONT"):
            door_style_ppt = assembly.get_prompt("Door Style")
            if door_style_ppt:
                door_style = door_style_ppt.get_value()
                if door_style != "Slab Door":
                    # print("Current Door Style: ", door_style)
                    assembly_number = "None"
                    material_number = "None"
                    part_number = "None"

                    # Determine Assembly
                    if obj.get("IS_BP_DRAWER_FRONT"):
                        assembly_number = "4"
                    else:
                        assembly_number = "3"

                    # Determine Material
                    is_raised = False
                    is_recessed = False
                    is_glass = False
                    is_painted = False
                    is_stained = False
                    is_glazed = False
                    is_std = False
                    is_brshd = False
                    is_dstd = False

                    raised_styles = [
                        "Aviano", "Colina", "Florence", 
                        "Pisa", "Bergamo", "Capri", 
                        "Venice", "Sienna", "Napoli", 
                        "Molino Vechio"]
                    recessed_styles = [
                        "Volterra", "Portofino", "Carrera", 
                        "Milano", "Merano", "Palermo", 
                        "Verona", "Rome", "San Marino"]
                    for style in raised_styles:
                        if style in door_style:
                            is_raised = True
                    for style in recessed_styles:
                        if style in door_style:
                            is_recessed = True

                    if "Glass" in door_style:
                        is_glass = True

                    if "PL" in mat_sku:
                        is_painted = True
                    if "SN" in mat_sku:
                        is_stained = True

                    glaze_color = closet_materials.get_glaze_color().name
                    glaze_style = closet_materials.get_glaze_style().name
                    if glaze_color != "None":
                        is_glazed = True
                    if is_glazed:
                        if glaze_style == "Brushed Thin":
                            is_brshd = True
                        elif glaze_style == "Dusted Thin":
                            is_dstd = True
                        else:
                            is_std = True

                    if is_recessed:
                        if is_painted:
                            if is_glass:
                                if is_glazed:
                                    if is_std:
                                        material_number = "17"
                                    elif is_brshd:
                                        material_number = "21"
                                    elif is_dstd:
                                        material_number = "25"
                                else:
                                    material_number = "13"
                            else:
                                if is_glazed:
                                    if is_std:
                                        material_number = "14"
                                    elif is_brshd:
                                        material_number = "18"
                                    elif is_dstd:
                                        material_number = "22"
                                else:
                                    material_number = "10"
                        elif is_stained:
                            if is_glass:
                                if is_glazed:
                                    if is_std:
                                        material_number = "57"
                                    elif is_brshd:
                                        material_number = "61"
                                    elif is_dstd:
                                        material_number = "65"
                                else:
                                    material_number = "53"
                            else:
                                if is_glazed:
                                    if is_std:
                                        material_number = "54"
                                    elif is_brshd:
                                        material_number = "58"
                                    elif is_dstd:
                                        material_number = "62"
                                else:
                                    material_number = "50"
                    elif is_raised:
                        if is_painted:
                            if is_glass:
                                if is_glazed:
                                    if is_std:
                                        material_number = "33"
                                    elif is_brshd:
                                        material_number = "37"
                                    elif is_dstd:
                                        material_number = "41"
                                else:
                                    material_number = "29"
                            else:
                                if is_glazed:
                                    if is_std:
                                        material_number = "30"
                                    elif is_brshd:
                                        material_number = "34"
                                    elif is_dstd:
                                        material_number = "38"
                                else:
                                    material_number = "26"
                        elif is_stained:
                            if is_glass:
                                if is_glazed:
                                    if is_std:
                                        material_number = "73"
                                    elif is_brshd:
                                        material_number = "77"
                                    elif is_dstd:
                                        material_number = "81"
                                else:
                                    material_number = "69"
                            else:
                                if is_glazed:
                                    if is_std:
                                        material_number = "70"
                                    elif is_brshd:
                                        material_number = "74"
                                    elif is_dstd:
                                        material_number = "78"
                                else:
                                    material_number = "66"
                    else:
                        if is_glass:
                            material_number = "03"
                        else:
                            material_number = "00"
                    
                    # Determine Part Number
                    # Currently, we only have entire assemblies, we will break 5 Piece doors into the seperate parts in the future, which we will need to change part_number when we do
                    part_number = "0"

                    category_number = assembly_number + material_number + part_number

        # print(category_number)
        return category_number
                    
                
                    
                    
                    

        
        # MISC.
        if obj.sn_closets.is_divider_bp:
            category_number = material_number + "67"
        # Firout = material_number + 66
        # File Rail Support = material_number + 68
        # Follow Strip = material_number + 69
        # Corble = material_number + 71

        


    def get_part_base_point(self,assembly):
        mx = False
        my = False
        mz = False
        
        if assembly.obj_x.location.x < 0:
            mx = True
        if assembly.obj_y.location.y < 0:
            my = True
        if assembly.obj_z.location.z < 0:
            mz = True
            
        if (mx == False) and (my == False) and (mz == False):
            return "1"
        if (mx == False) and (my == False) and (mz == True):
            return "2"        
        if (mx == False) and (my == True) and (mz == False):
            return "3"
        if (mx == False) and (my == True) and (mz == True):
            return "4"
        if (mx == True) and (my == True) and (mz == False):
            return "5"
        if (mx == True) and (my == True) and (mz == True):
            return "6"        
        if (mx == True) and (my == False) and (mz == False):
            return "7"
        if (mx == True) and (my == False) and (mz == True):
            return "8"   
             
        return "1"

    def get_edgebanding_name(self,obj,edge,spec_group):
        if obj.snap.edgeband_material_name != "" and edge != "":
            thickness = sn_utils.get_edgebanding_thickness_from_pointer_name(edge,spec_group)
            edge_mat_name = obj.snap.edgeband_material_name
            if edge_mat_name not in self.edgeband_materials and edge_mat_name != "":
                self.edgeband_materials[edge_mat_name] = thickness
            return edge_mat_name
        else:
            thickness = sn_utils.get_edgebanding_thickness_from_pointer_name(edge,spec_group)
            edge_mat_name = sn_utils.get_edgebanding_name_from_pointer_name(edge,spec_group)
            if edge_mat_name not in self.edgeband_materials and edge_mat_name != "":
                self.edgeband_materials[edge_mat_name] = thickness                
            return edge_mat_name
    
    def get_edgebanding_name_w1(self,obj,edge,spec_group):
        if obj.snap.edgeband_material_name_w1 != "" and edge != "":
            thickness = sn_utils.get_edgebanding_thickness_from_pointer_name(edge,spec_group)
            edge_mat_name = obj.snap.edgeband_material_name_w1
            if edge_mat_name not in self.edgeband_materials and edge_mat_name != "":
                self.edgeband_materials[edge_mat_name] = thickness
            return edge_mat_name
        else:
            thickness = sn_utils.get_edgebanding_thickness_from_pointer_name(edge,spec_group)
            edge_mat_name = sn_utils.get_edgebanding_name_from_pointer_name(edge,spec_group)
            if edge_mat_name not in self.edgeband_materials and edge_mat_name != "":
                self.edgeband_materials[edge_mat_name] = thickness                
            return edge_mat_name    
    
    def get_edgebanding_name_w2(self,obj,edge,spec_group):
        if obj.snap.edgeband_material_name_w2 != "" and edge != "":
            thickness = sn_utils.get_edgebanding_thickness_from_pointer_name(edge,spec_group)
            edge_mat_name = obj.snap.edgeband_material_name_w2
            if edge_mat_name not in self.edgeband_materials and edge_mat_name != "":
                self.edgeband_materials[edge_mat_name] = thickness
            return edge_mat_name
        else:
            thickness = sn_utils.get_edgebanding_thickness_from_pointer_name(edge,spec_group)
            edge_mat_name = sn_utils.get_edgebanding_name_from_pointer_name(edge,spec_group)
            if edge_mat_name not in self.edgeband_materials and edge_mat_name != "":
                self.edgeband_materials[edge_mat_name] = thickness                
            return edge_mat_name        
    
    def get_edgebanding_name_l1(self,obj,edge,spec_group):
        if obj.snap.edgeband_material_name_l1 != "" and edge != "":
            thickness = sn_utils.get_edgebanding_thickness_from_pointer_name(edge,spec_group)
            edge_mat_name = obj.snap.edgeband_material_name_l1
            if edge_mat_name not in self.edgeband_materials and edge_mat_name != "":
                self.edgeband_materials[edge_mat_name] = thickness
            return edge_mat_name
        else:
            thickness = sn_utils.get_edgebanding_thickness_from_pointer_name(edge,spec_group)
            edge_mat_name = sn_utils.get_edgebanding_name_from_pointer_name(edge,spec_group)
            if edge_mat_name not in self.edgeband_materials and edge_mat_name != "":
                self.edgeband_materials[edge_mat_name] = thickness                
            return edge_mat_name          
    
    def get_edgebanding_name_l2(self,obj,edge,spec_group):
        if obj.snap.edgeband_material_name_l2 != "" and edge != "":
            thickness = sn_utils.get_edgebanding_thickness_from_pointer_name(edge,spec_group)
            edge_mat_name = obj.snap.edgeband_material_name_l2
            if edge_mat_name not in self.edgeband_materials and edge_mat_name != "":
                self.edgeband_materials[edge_mat_name] = thickness
            return edge_mat_name
        else:
            thickness = sn_utils.get_edgebanding_thickness_from_pointer_name(edge,spec_group)
            edge_mat_name = sn_utils.get_edgebanding_name_from_pointer_name(edge,spec_group)
            if edge_mat_name not in self.edgeband_materials and edge_mat_name != "":
                self.edgeband_materials[edge_mat_name] = thickness                
            return edge_mat_name

    def get_pull_drilling(self, assembly, token, circles):
        normal_z = 1
        org_displacement = 0

        if token.face == '6':
            normal_z = -1
            org_displacement = self.distance(sn_utils.get_part_thickness(get_cutpart(assembly.obj_bp)))

        param_dict = token.create_parameter_dictionary()  
        dim_in_x = float(param_dict['Par1'])
        dim_in_y = float(param_dict['Par2'])
        dim_in_z = float(param_dict['Par3'])
        bore_dia_meter = sn_unit.millimeter(float(param_dict['Par4']))
        bore_dia = sn_unit.meter_to_inch(bore_dia_meter)
        end_dim_in_x = float(param_dict['Par5'])
        end_dim_in_y = float(param_dict['Par6'])
        #distance_between_holes = float(param_dict['Par7'])                                          

        #Hole 1
        cir_dict = {}
        cir_dict['cen_x'] = dim_in_x
        cir_dict['cen_y'] = dim_in_y
        cir_dict['cen_z'] = dim_in_z
        cir_dict['diameter'] = bore_dia
        cir_dict['normal_z'] = normal_z
        cir_dict['org_displacement'] = 0
        circles.append(cir_dict)

        #Hole 2
        cir_dict = {}
        cir_dict['cen_x'] = end_dim_in_x
        cir_dict['cen_y'] = end_dim_in_y
        cir_dict['cen_z'] = dim_in_z
        cir_dict['diameter'] = bore_dia
        cir_dict['normal_z'] = normal_z
        cir_dict['org_displacement'] = 0
        circles.append(cir_dict)

        return circles

    def get_door_hinge_drilling(self, assembly, token, circles):
        door_swing = assembly.get_prompt("Door Swing").get_value()
        door_x_dim = sn_unit.meter_to_inch(assembly.obj_x.location.x)
        door_y_dim = abs(sn_unit.meter_to_inch(assembly.obj_y.location.y))
        normal_z = -1
        org_displacement = self.distance(sn_utils.get_part_thickness(get_cutpart(assembly.obj_bp)))
        bore_dia = sn_unit.meter_to_inch(sn_unit.millimeter(35))
        dim_in_x = sn_unit.meter_to_inch(sn_unit.millimeter(78))
        dim_in_y = sn_unit.meter_to_inch(sn_unit.millimeter(21))
        bore_depth = sn_unit.meter_to_inch(sn_unit.millimeter(14))
        screw_hole_y_dim = sn_unit.meter_to_inch(sn_unit.millimeter(10))
        screw_hole_dia = sn_unit.meter_to_inch(sn_unit.millimeter(2))
        distance_between_holes = sn_unit.meter_to_inch(sn_unit.millimeter(45))
        mid_hole_offset = sn_unit.meter_to_inch(sn_unit.millimeter(16))
        screw_hole_depth = sn_unit.meter_to_inch(sn_unit.millimeter(4))

        if door_swing == "Bottom":
            print("Bottom swing hamper door")

        #Bottom
        #Add Main hole
        cir = {}
        cir['cen_x'] = -dim_in_x
        cir['cen_y'] = dim_in_y
        cir['cen_z'] = bore_depth
        cir['diameter'] = bore_dia 
        cir['normal_z'] = normal_z
        cir['org_displacement'] = org_displacement
        circles.append(cir)                                        

        #Add screw hole left
        cir = {}
        cir['cen_x'] = -(dim_in_x - distance_between_holes * 0.5)
        cir['cen_y'] = dim_in_y + screw_hole_y_dim
        cir['cen_z'] = screw_hole_depth
        cir['diameter'] = screw_hole_dia 
        cir['normal_z'] = normal_z
        cir['org_displacement'] = org_displacement
        circles.append(cir)                                        

        #add screw hole right
        cir = {}
        cir['cen_x'] = -(dim_in_x + distance_between_holes * 0.5)
        cir['cen_y'] = dim_in_y + screw_hole_y_dim
        cir['cen_z'] = screw_hole_depth
        cir['diameter'] = screw_hole_dia 
        cir['normal_z'] = normal_z
        cir['org_displacement'] = org_displacement
        circles.append(cir)

        dim_in_x = door_x_dim - dim_in_x

        #Top
        #Add Main hole
        cir = {}
        cir['cen_x'] = -dim_in_x
        cir['cen_y'] = dim_in_y
        cir['cen_z'] = bore_depth
        cir['diameter'] = bore_dia 
        cir['normal_z'] = normal_z
        cir['org_displacement'] = org_displacement
        circles.append(cir)                                        

        #Add screw hole left
        cir = {}
        cir['cen_x'] = -(dim_in_x - distance_between_holes * 0.5)
        cir['cen_y'] = dim_in_y + screw_hole_y_dim
        cir['cen_z'] = screw_hole_depth
        cir['diameter'] = screw_hole_dia 
        cir['normal_z'] = normal_z
        cir['org_displacement'] = org_displacement
        circles.append(cir)                                        

        #add screw hole right
        cir = {}
        cir['cen_x'] = -(dim_in_x + distance_between_holes * 0.5)
        cir['cen_y'] = dim_in_y + screw_hole_y_dim
        cir['cen_z'] = screw_hole_depth
        cir['diameter'] = screw_hole_dia 
        cir['normal_z'] = normal_z
        cir['org_displacement'] = org_displacement
        circles.append(cir)

        #Mid hinge drilling for doors longer than 39H Count
        if door_x_dim > 50:
            if(round(sn_unit.meter_to_millimeter(door_x_dim)/32) % 2 == 0):
                if door_swing == "Left":
                    dim_in_x = door_x_dim * 0.5 + mid_hole_offset
                else:
                    dim_in_x = door_x_dim * 0.5 - mid_hole_offset
            else:
                dim_in_x = door_x_dim * 0.5            

            #Add Main hole
            cir = {}
            cir['cen_x'] = -dim_in_x
            cir['cen_y'] = dim_in_y
            cir['cen_z'] = bore_depth
            cir['diameter'] = bore_dia 
            cir['normal_z'] = normal_z
            cir['org_displacement'] = org_displacement
            circles.append(cir)                                        

            #Add screw hole left
            cir = {}
            cir['cen_x'] = -(dim_in_x - distance_between_holes * 0.5)
            cir['cen_y'] = dim_in_y + screw_hole_y_dim
            cir['cen_z'] = screw_hole_depth
            cir['diameter'] = screw_hole_dia 
            cir['normal_z'] = normal_z
            cir['org_displacement'] = org_displacement
            circles.append(cir)                                        

            #add screw hole right
            cir = {}
            cir['cen_x'] = -(dim_in_x + distance_between_holes * 0.5)
            cir['cen_y'] = dim_in_y + screw_hole_y_dim
            cir['cen_z'] = screw_hole_depth
            cir['diameter'] = screw_hole_dia 
            cir['normal_z'] = normal_z
            cir['org_displacement'] = org_displacement
            circles.append(cir)

        return circles

    def get_hamper_door_hinge_drilling(self, assembly, token, circles):
        #door_x_dim = sn_unit.meter_to_inch(assembly.obj_x.location.x)
        door_y_dim = abs(sn_unit.meter_to_inch(assembly.obj_y.location.y))
        normal_z = -1
        org_displacement = self.distance(sn_utils.get_part_thickness(get_cutpart(assembly.obj_bp)))
        bore_dia = sn_unit.meter_to_inch(sn_unit.millimeter(35))
        dim_in_x = sn_unit.meter_to_inch(sn_unit.millimeter(21))
        dim_in_y = sn_unit.meter_to_inch(sn_unit.millimeter(78))                                   
        bore_depth = sn_unit.meter_to_inch(sn_unit.millimeter(11.5))
        screw_hole_x_dim = sn_unit.meter_to_inch(sn_unit.millimeter(9.5)) 
        screw_hole_dia = sn_unit.meter_to_inch(sn_unit.millimeter(0.5)) 
        distance_between_holes = sn_unit.meter_to_inch(sn_unit.millimeter(45))

        #Right
        cir = {}
        cir['cen_x'] = -dim_in_y  # -dim_in_x
        cir['cen_y'] = dim_in_x  # dim_in_y
        cir['cen_z'] = bore_depth
        cir['diameter'] = bore_dia 
        cir['normal_z'] = normal_z
        cir['org_displacement'] = org_displacement
        circles.append(cir)                                        

        cir = {}
        cir['cen_x'] = -(dim_in_y + distance_between_holes * 0.5)
        cir['cen_y'] = dim_in_x + screw_hole_x_dim
        cir['cen_z'] = bore_depth
        cir['diameter'] = screw_hole_dia 
        cir['normal_z'] = normal_z
        cir['org_displacement'] = org_displacement
        circles.append(cir)                                        

        cir = {}
        cir['cen_x'] = -(dim_in_y - distance_between_holes * 0.5)
        cir['cen_y'] = dim_in_x + screw_hole_x_dim
        cir['cen_z'] = bore_depth
        cir['diameter'] = screw_hole_dia 
        cir['normal_z'] = normal_z
        cir['org_displacement'] = org_displacement
        circles.append(cir)

        dim_in_y = door_y_dim - dim_in_y

        #Left
        cir = {}
        cir['cen_x'] = -dim_in_y  # -dim_in_x
        cir['cen_y'] = dim_in_x  # dim_in_y
        cir['cen_z'] = bore_depth
        cir['diameter'] = bore_dia 
        cir['normal_z'] = normal_z
        cir['org_displacement'] = org_displacement
        circles.append(cir)                                        

        cir = {}
        cir['cen_x'] = -(dim_in_y + distance_between_holes * 0.5)
        cir['cen_y'] = dim_in_x + screw_hole_x_dim
        cir['cen_z'] = bore_depth
        cir['diameter'] = screw_hole_dia 
        cir['normal_z'] = normal_z
        cir['org_displacement'] = org_displacement
        circles.append(cir)                                        

        cir = {}
        cir['cen_x'] = -(dim_in_y - distance_between_holes * 0.5)
        cir['cen_y'] = dim_in_x + screw_hole_x_dim
        cir['cen_z'] = bore_depth
        cir['diameter'] = screw_hole_dia 
        cir['normal_z'] = normal_z
        cir['org_displacement'] = org_displacement
        circles.append(cir)

        return circles

    def get_shelf_kd_drilling(self, assembly, token, token_name, circles):
        #Two Left Holes For KD Shelf
        if token_name == 'Left Drilling':                      
            normal_z = 1
            org_displacement = 0

            if token.face == '5':
                normal_z = -1
                org_displacement = self.distance(sn_utils.get_part_thickness(get_cutpart(assembly.obj_bp)))

            param_dict = token.create_parameter_dictionary()
            if param_dict['Par1'] != '':
                dim_in_x_1,dim_in_x_2 = param_dict['Par1'].split(",")
            else:
                dim_in_x_1 = 0
                dim_in_x_2 = 0
            dim_in_y = param_dict['Par7']
            bore_depth,irrelevant = param_dict['Par6'].split(",")
            more_irrelevant,cam_hole_dia = param_dict['Par5'].split(",")                                  

            #Back Left Hole
            cir = {}
            cir['cen_x'] = -float(dim_in_x_2)
            cir['cen_y'] = float(dim_in_y)
            cir['cen_z'] = float(bore_depth)
            cir['diameter'] = sn_unit.meter_to_inch(sn_unit.millimeter(float(cam_hole_dia)))
            cir['normal_z'] = normal_z
            cir['org_displacement'] = org_displacement
            circles.append(cir)

            #Front Left Hole
            cir = {}
            cir['cen_x'] = -float(dim_in_x_1)
            cir['cen_y'] = float(dim_in_y)
            cir['cen_z'] = float(bore_depth)
            cir['diameter'] = sn_unit.meter_to_inch(sn_unit.millimeter(float(cam_hole_dia)))
            cir['normal_z'] = normal_z
            cir['org_displacement'] = org_displacement
            circles.append(cir)


        #Two Right Holes For KD Shelf
        if token_name == 'Right Drilling':                                   
            normal_z = 1
            org_displacement = 0
            if token.face == '5':
                normal_z = -1
                org_displacement = self.distance(sn_utils.get_part_thickness(get_cutpart(assembly.obj_bp)))

            param_dict = token.create_parameter_dictionary()
            if param_dict['Par1'] != '':
                dim_in_x_1,dim_in_x_2 = param_dict['Par1'].split(",")
            else:
                dim_in_x_1 = 0
                dim_in_x_2 = 0
            dim_in_y = param_dict['Par7']                          
            bore_depth,irrelevant = param_dict['Par6'].split(",")
            more_irrelevant,cam_hole_dia = param_dict['Par5'].split(",")                                   

            #Back Right Hole
            cir = {}
            cir['cen_x'] = -float(dim_in_x_2)
            cir['cen_y'] = float(dim_in_y)
            cir['cen_z'] = float(bore_depth)
            cir['diameter'] = sn_unit.meter_to_inch(sn_unit.millimeter(float(cam_hole_dia)))
            cir['normal_z'] = normal_z
            cir['org_displacement'] = org_displacement
            circles.append(cir)
            
            #Front Right Hole
            cir = {}
            cir['cen_x'] = -float(dim_in_x_1)
            cir['cen_y'] = float(dim_in_y)
            cir['cen_z'] = float(bore_depth)
            cir['diameter'] = sn_unit.meter_to_inch(sn_unit.millimeter(float(cam_hole_dia)))
            cir['normal_z'] = normal_z
            cir['org_displacement'] = org_displacement
            circles.append(cir)


        return circles

    def get_system_hole_drilling(self, assembly, token, circles):
        param_dict = token.create_parameter_dictionary()
        start_dim_x = float(param_dict['Par1'])                                        
        start_dim_y = float(param_dict['Par2'])
        drill_depth = float(param_dict['Par3'])
        bore_dia = sn_unit.meter_to_inch(float(param_dict['Par4']))#Convert to inches
        end_dim_x = float(param_dict['Par5'])
        #end_dim_in_y = float(param_dict['Par6'])
        distance_between_holes = float(param_dict['Par7'])

        normal_z = 1
        org_displacement = 0

        if token.face == '5':
            normal_z = -1
            org_displacement = self.distance(sn_utils.get_part_thickness(get_cutpart(assembly.obj_bp)))
            start_dim_x = -start_dim_x
            end_dim_x = -end_dim_x

        #First Hole
        cir = {}
        cir['cen_x'] = start_dim_x
        cir['cen_y'] = start_dim_y
        cir['cen_z'] = drill_depth
        cir['diameter'] = bore_dia
        cir['normal_z'] = normal_z
        cir['org_displacement'] = org_displacement
        circles.append(cir)

        x = start_dim_x
    
        #All other holes
        if token.face == '6':
            while x > end_dim_x:
                x -= distance_between_holes
                if x < 0: break
                cir = {}
                cir['cen_x'] = x
                cir['cen_y'] = start_dim_y
                cir['cen_z'] = drill_depth
                cir['diameter'] = bore_dia
                cir['normal_z'] = normal_z
                cir['org_displacement'] = org_displacement
                circles.append(cir)

        if token.face == '5':
            while x < end_dim_x and x < 0:
                x += distance_between_holes
                if x > 0: break
                cir = {}
                cir['cen_x'] = x
                cir['cen_y'] = start_dim_y
                cir['cen_z'] = drill_depth
                cir['diameter'] = bore_dia
                cir['normal_z'] = normal_z
                cir['org_displacement'] = org_displacement
                circles.append(cir)

        return circles

    def get_slide_drilling(self, assembly, token, circles):
        closet_materials = bpy.context.scene.closet_materials
        param_dict = token.create_parameter_dictionary()

        slide_type = closet_materials.get_drawer_slide_type()
        slide_size = get_slide_size(slide_type, assembly)
        front_hole_dim_m = sn_unit.millimeter(slide_size.front_hole_dim_mm)
        front_hole_dim_inch = sn_unit.meter_to_inch(front_hole_dim_m)
        back_hole_dim_m = sn_unit.millimeter(slide_size.back_hole_dim_mm)
        back_hole_dim_inch = sn_unit.meter_to_inch(back_hole_dim_m)
        
        dim_from_drawer_bottom = 0.5 # 0.5" should this be added to csv files?
        dim_to_first_hole = front_hole_dim_inch
        dim_to_second_hole = back_hole_dim_inch
        bore_depth_and_dia = param_dict['Par7']
        bore_depth, bore_dia = bore_depth_and_dia.split("|")
        bore_depth_f = float(bore_depth)
        bore_dia_meter = sn_unit.millimeter(float(bore_dia))
        bore_dia_inch = sn_unit.meter_to_inch(bore_dia_meter)

        #Front Hole
        cir = {}
        cir['cen_x'] = dim_to_first_hole
        cir['cen_y'] = dim_from_drawer_bottom
        cir['cen_z'] = bore_depth_f
        cir['diameter'] = bore_dia_inch 
        cir['normal_z'] = 1
        cir['org_displacement'] = 0
        circles.append(cir)

        #Back Hole
        cir = {}
        cir['cen_x'] = dim_to_second_hole
        cir['cen_y'] = dim_from_drawer_bottom
        cir['cen_z'] = bore_depth_f
        cir['diameter'] = bore_dia_inch 
        cir['normal_z'] = 1
        cir['org_displacement'] = 0
        circles.append(cir)

        return circles

    def get_drilling(self, assembly):
        circles = []
        sys_holes = (
            'System Holes Right Top Front',
            'System Holes Right Top Rear',
            'System Holes Right Bottom Front',
            'System Holes Right Bottom Rear',
            'System Holes Left Top Front',
            'System Holes Left Top Rear',
            'System Holes Left Bottom Front',
            'System Holes Left Bottom Rear',
            'System Holes Mid Left',
            'System Holes Mid Right'
        )        

        for child in assembly.obj_bp.children:
            if child.type == 'MESH':
                tokens = child.snap.mp.machine_tokens
                if len(tokens) > 0:
                    for token in tokens:
                        if not token.is_disabled:
                            token_name = token.name if token.name != "" else "Unnamed"

                            if token_name == "Unnamed":
                                print("Unnamed machine token!")

                            if token.type_token == 'BORE':
                                if token_name in sys_holes:
                                    circles = self.get_system_hole_drilling(assembly, token, circles)

                                if token_name == 'Pull Drilling':
                                    circles = self.get_pull_drilling(assembly, token, circles)

                                if token_name == 'Door Hinge Drilling':
                                    circles = self.get_door_hinge_drilling(assembly, token, circles)                                            

                                if token_name == "Hamper Door Hinge Drilling":
                                    circles = self.get_hamper_door_hinge_drilling(assembly, token, circles)

                                if token_name == 'Shelf and Rod Holes':
                                    print("Found machine token:", token_name)

                            if token.type_token == 'SLIDE':
                                circles = self.get_slide_drilling(assembly, token, circles)

                            if token.type_token == 'CAMLOCK':
                                circles = self.get_shelf_kd_drilling(assembly, token, token_name, circles)

        return circles

    def set_job_number(self):
        dirname = os.path.dirname(bpy.data.filepath).split("\\")[-1]
        filname = "{}.ccp".format(dirname)
        tree = ET.parse(os.path.join(os.path.dirname(bpy.data.filepath), ".snap", filname))
        root = tree.getroot()
        elm_pinfo = root.find("ProjectInfo")
        project_id = int(elm_pinfo.find("project_id").text)
        proj_user_prefs = bpy.context.preferences.addons["snap"].preferences
        designer_id = proj_user_prefs.designer_id
        self.job_number = "{0:0=3d}.{1:0=4d}".format(designer_id, project_id)

    def write_oversize_top_shelf_part(self, node, obj, side="", shelf_length_inch=97):
        # shelf_length_inch = 97 #96
        closet_materials = bpy.context.scene.closet_materials

        for child in obj.children:
            if child.snap.type_mesh == 'CUTPART':
                obj = child

        if obj.get('IS_BP_ASSEMBLY'):
            assembly = sn_types.Assembly(obj_bp=obj)
        else:
            assembly = sn_types.Assembly(obj.parent)

        if assembly.obj_bp.snap.type_group != "PRODUCT":
            elm_part = self.xml.add_element(
                node,
                'Part',
                {
                    'ID': "IDP-{}".format(self.part_count),
                    'MatID': "IDM-{}".format(self.mat_count),
                    'LabelID': "IDL-{}".format(self.label_count),
                    'OpID': "IDOP-{}".format(self.op_count)
                }
            )

            part_name = assembly.obj_bp.snap.name_object if assembly.obj_bp.snap.name_object != "" else assembly.obj_bp.name
            self.xml.add_element_with_text(elm_part, 'Name', part_name + " Shelf")
            self.xml.add_element_with_text(elm_part,'Quantity', self.get_part_qty(assembly))
            self.xml.add_element_with_text(elm_part,'Width', self.get_part_width(assembly)) 
            self.xml.add_element_with_text(elm_part,'FinishedWidth', self.get_part_width(assembly))           
            self.xml.add_element_with_text(elm_part,'Length', self.distance(sn_unit.inch(shelf_length_inch)))
            self.xml.add_element_with_text(elm_part,'FinishedLength', self.distance(sn_unit.inch(shelf_length_inch)))
            self.xml.add_element_with_text(elm_part,'Thickness',self.distance(sn_utils.get_part_thickness(obj)))
            self.xml.add_element_with_text(elm_part,'FinishedThickness', self.distance(sn_utils.get_part_thickness(obj)))
            self.xml.add_element_with_text(elm_part,'Routing', "SK1")
            self.xml.add_element_with_text(elm_part,'Class', "make")
            self.xml.add_element_with_text(elm_part,'Type', "panel")

            elm_unit = self.xml.add_element(elm_part,'Unit')
            self.xml.add_element_with_text(elm_unit,'Name', "dimension")
            self.xml.add_element_with_text(elm_unit,'Measure', "inch")
            self.xml.add_element_with_text(elm_unit,'RoundFactor', "0")

            #Edgebanding
            carcass_bp = sn_utils.get_closet_bp(obj)
            carcass_assembly = sn_types.Assembly(carcass_bp)
            primary_edge_color_name = closet_materials.edges.get_edge_color().name

            edge_1 = ''
            edge_2 = ''
            edge_3 = ''
            edge_4 = ''
            edge_1_sku = ''
            edge_2_sku = ''
            edge_3_sku = ''
            edge_4_sku = ''

            is_countertop_ppt = assembly.get_prompt("Is Countertop")
            if is_countertop_ppt and is_countertop_ppt.get_value() == False:
                if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                    edge_2 = "L1"
                else:
                    edge_2 = "S1"
                edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                
                carcass_bp = sn_utils.get_closet_bp(obj)
                if carcass_bp.get('IS_BP_L_SHELVES'):
                    exposed_left = assembly.get_prompt("Exposed Left")
                    exposed_right = assembly.get_prompt("Exposed Right")
                    if exposed_left and exposed_right:
                        if exposed_left.get_value() or exposed_right.get_value():
                            if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                                edge_1 = "S1"
                            else:
                                edge_1 = "L1"
                            edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                else:
                    carcass_assembly = sn_types.Assembly(carcass_bp)
                    l_carcass_end_cond_prompt = carcass_assembly.get_prompt("Left End Condition")
                    r_carcass_end_cond_prompt = carcass_assembly.get_prompt("Right End Condition")
                    l_carcass_end_cond = ''
                    r_carcass_end_cond = ''
                    if l_carcass_end_cond_prompt and r_carcass_end_cond_prompt:
                        l_carcass_end_cond = l_carcass_end_cond_prompt.get_value()
                        r_carcass_end_cond = r_carcass_end_cond_prompt.get_value()
                    l_assembly_end_cond_prompt = assembly.get_prompt("Exposed Left")
                    r_assembly_end_cond_prompt = assembly.get_prompt("Exposed Right")
                    b_assembly_end_cond_prompt = assembly.get_prompt("Exposed Back")
                    l_assembly_end_cond = ''
                    r_assembly_end_cond = ''
                    b_assembly_end_cond = ''
                    if l_assembly_end_cond_prompt and r_assembly_end_cond_prompt and b_assembly_end_cond_prompt:
                        l_assembly_end_cond = l_assembly_end_cond_prompt.get_value()
                        r_assembly_end_cond = r_assembly_end_cond_prompt.get_value()
                        b_assembly_end_cond = b_assembly_end_cond_prompt.get_value()
                    if (l_carcass_end_cond == 0 and r_carcass_end_cond != 0) or (l_assembly_end_cond == True and r_assembly_end_cond != True):
                        if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                            edge_1 = "S1"
                        else:
                            edge_1 = "L1"
                        edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)                  

                    if (l_carcass_end_cond != 0 and r_carcass_end_cond == 0) or (l_assembly_end_cond != True and r_assembly_end_cond == True):
                        if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                            edge_3 = "S2"
                        else:
                            edge_3 = "L2"
                        edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)

                    if (l_carcass_end_cond == 0 and r_carcass_end_cond == 0) or (l_assembly_end_cond == True and r_assembly_end_cond == True):
                        if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                            edge_1 = "S1"
                            edge_3 = "S2"
                        else:
                            edge_1 = "L1"
                            edge_3 = "L2"
                        edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                        edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                    
                    if(b_assembly_end_cond):
                        if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                            edge_4 = "L2"
                        else:
                            edge_4 = "S2"
                        edge_4_sku = closet_materials.get_edge_sku(obj, assembly, part_name)            

            shelf_x_location = self.get_part_x_location(assembly.obj_bp,assembly.obj_bp.location.x)

            if side == "Right":
                shelf_x_location = str(float(shelf_x_location) + shelf_length_inch)                    

            #Create and add label
            lbl = [
                ("IDL-{}".format(self.label_count), "IDJ-{}".format(self.job_count), "IDP-{}".format(self.part_count)),                
                ("dcname", "text", part_name + " Shelf"),
                ("name", "text", part_name + " Shelf"),
                ("wallname", "text", sn_utils.get_wall_bp(obj).snap.name_object),
                ("x", "text", shelf_x_location),
                ("y", "text", self.get_part_y_location(assembly.obj_bp,assembly.obj_bp.location.y)),
                ("z", "text", self.get_part_z_location(assembly.obj_bp,assembly.obj_bp.location.z)),
                ("lenx", "text", self.distance(sn_unit.inch(shelf_length_inch))),
                ("leny", "text", self.get_part_width(assembly)),
                ("lenz", "text", self.distance(sn_utils.get_part_thickness(obj))),
                ("rotx", "text", str(int(math.degrees(assembly.obj_bp.rotation_euler.x)))),
                ("roty", "text", str(int(math.degrees(assembly.obj_bp.rotation_euler.x)))),
                ("rotz", "text", str(int(math.degrees(assembly.obj_bp.rotation_euler.x)))),
                ("boml", "text", self.distance(sn_unit.inch(shelf_length_inch))),
                ("bomt", "text",  self.distance(sn_utils.get_part_thickness(obj))),
                ("bomw", "text", self.get_part_width(assembly)),
                ("catnum", "text", self.get_part_category_number(assembly, assembly.obj_bp, closet_materials.get_mat_sku(obj, assembly, part_name), part_name)),
                ("sku", "text", closet_materials.get_mat_sku(obj, assembly, part_name)),
                ("cncmirror", "text", ""),
                ("cncrotation", "text", "180"),
                ("cutl", "text", self.distance(sn_unit.inch(shelf_length_inch))),
                ("cutt", "text", self.distance(sn_utils.get_part_thickness(obj))),
                ("cutw", "text", self.get_part_width(assembly)),
                ("primaryedgecolorname", "text", primary_edge_color_name),
                ("edgeband1", "text", edge_1),
                ("edgeband1sku", "text", edge_1_sku),
                ("edgeband1name", "text", primary_edge_color_name if edge_1 != '' else ''),
                ("edgeband2", "text", edge_2),
                ("edgeband2sku", "text", edge_2_sku),
                ("edgeband2name", "text", primary_edge_color_name if edge_2 != '' else ''),
                ("edgeband3", "text", edge_3),
                ("edgeband3sku", "text", edge_3_sku),
                ("edgeband3name", "text", primary_edge_color_name if edge_3 != '' else ''),
                ("edgeband4", "text", edge_4),
                ("edgeband4sku", "text", edge_4_sku),
                ("edgeband4name", "text", primary_edge_color_name if edge_4 != '' else '')]

            self.labels.append(lbl)
            self.label_count += 1

            #Create and add OperationGroup
            #Get info for segments
            X = self.distance(sn_unit.inch(shelf_length_inch))
            Y = self.get_part_width(assembly)
            Z = self.distance(sn_utils.get_part_thickness(obj))
            W = 0

            upper_right = (X, Y, Z, W)
            upper_left = (0, Y, Z, W)
            lower_left = (0, 0, Z, W)
            lower_right = (X, 0, Z, W)
            circles = []

            op_grp = [
                ("IDOP-{}".format(self.op_count), "IDMOR-{}".format(self.or_count)),
                upper_right,#Segment 1
                upper_left,#Segment 2
                lower_left,#Segment 3
                lower_right,#Segment 4
                circles
            ]

            self.op_groups.append(op_grp)
            self.op_count += 1         
            
            #DEBUG            
            if self.debugger:
                self.debugger.write_debug_part(self, assembly, obj, op_grp, lbl, self.part_count)

            self.part_count += 1

    def write_oversize_top_shelf(self, node, obj):
        self.write_oversize_top_shelf_part(node, obj, side="Left", shelf_length_inch=96)
        self.write_oversize_top_shelf_part(node, obj, side="Right", shelf_length_inch=60)

    def write_accessory(self, elm, obj_bp, spec_group):
        assembly = sn_types.Assembly(obj_bp)
        sub_name = assembly.obj_bp.snap.name_object if assembly.obj_bp.snap.name_object != "" else assembly.obj_bp.name
        elm_subassembly = self.xml.add_element(elm, "Assembly", {'ID': "IDA-{}".format(self.assembly_count)})
        self.xml.add_element_with_text(elm_subassembly, 'Name', sub_name)
        self.xml.add_element_with_text(elm_subassembly, 'Quantity', "1")

        for child in obj_bp.children:
            if child.snap.type_mesh in ('HARDWARE', 'BUYOUT'):
                qty = '1'

                if "IS_BP_BELT_RACK" not in obj_bp and "IS_BP_TIE_RACK" not in obj_bp:
                    try:
                        qty = child.modifiers['Quantity'].count
                    except KeyError:
                        print("Writing Closet Accessory '{}'- 'Quantity' modifier not found.".format(obj_bp))

                self.write_hardware_node(elm_subassembly, child, name=child.snap.name_object, qty=str(qty))

        self.write_parts_for_subassembly(elm_subassembly, assembly.obj_bp, spec_group)
        self.assembly_count += 1

    def write_products(self, project_node):
        specgroups = bpy.context.scene.snap.spec_groups
        item_name, _ = os.path.splitext(bpy.path.basename(bpy.data.filepath))
        room_category_dict = {
            "Please Select": "No Category Found",
            "FG-CLST": "Closet",
            "FG-ENTC": "Entertainment Center",
            "FG-GARG": "Garage",
            "FG-HMOF": "Home Office",
            "FG-LNDY": "Laundry",
            "FG-MDRM": "Mud Room",
            "FG-PNTY": "Pantry",
            "FG-KITN": "Kitchen",
            "FG-BATH": "Bathroom",
            "FG-RFCE": "Reface",
            "FG-RMDL": "Remodel",
            "FG-STNE": "Stone",
            "FG-SPEC": "Specialty",
            "FG-COMM": "Commercial",
            "FG-CMSS": "Commercial Solid Surface",
            "FG-CMST": "Commercial Stone"
        }
        if("_" in item_name):
            # Old Room Names
            room_category_num, room_name = item_name.split("_")
            room_category_name = "Unknown"
        else:
            room_name = item_name
            room_category_num = bpy.context.scene.sn_roombuilder.room_category
            room_category_name = room_category_dict[room_category_num]

        existing_items = project_node.findall("Item")

        if existing_items:
            idx = list(project_node).index(existing_items[-1]) + 1
            elm_product = self.xml.insert_element(idx, project_node, 'Item', {'ID': "IDI-{}".format(self.item_count)})

        else:
            elm_product = self.xml.add_element(project_node, 'Item', {'ID': "IDI-{}".format(self.item_count)})

        item_number = "{0:0=2d}".format(self.item_count + 1)

        self.xml.add_element_with_text(elm_product,'Name', self.job_number + "." + item_number)
        self.xml.add_element_with_text(elm_product,'Description', room_name)
        #self.xml.add_element_with_text(elm_product,'Room Category', room_category_name)
        #self.xml.add_element_with_text(elm_product,'GL ACCT NUM', room_category_num)
        self.xml.add_element_with_text(elm_product,'Note', "")#Str literal OKAY       

        spec_group = None

        for obj_product in self.products:
            spec_group = specgroups[obj_product.snap.spec_group_index]
            product = sn_types.Assembly(obj_product)

            if obj_product.sn_closets.is_accessory_bp:
                self.write_accessory(elm_product, obj_product, spec_group)
                continue

            #self.write_prompts_for_assembly(elm_product, product)
            self.write_parts_for_product(elm_product,obj_product,spec_group)
            self.write_subassemblies_for_product(elm_product,obj_product,spec_group)
        
        #Add Full Sized Products
        if not spec_group:
            spec_group = specgroups[0]
        self.write_full_sized_cover_cleat(elm_product,spec_group)
        self.write_full_sized_flat_crown(elm_product,spec_group)
        self.write_full_sized_crown_molding(elm_product,spec_group)
        self.write_full_sized_inverted_base(elm_product,spec_group)
        self.write_full_sized_base_molding(elm_product,spec_group)
        self.write_full_sized_tk_skin(elm_product,spec_group)
        self.write_full_sized_hang_rod(elm_product,spec_group)
        self.write_full_sized_cleat_stock(elm_product,spec_group)
        self.write_garage_legs(elm_product,spec_group)

        info = [('DrawingNum', self.job_number + "." + item_number),
                ('RoomName', item_name),
                ('RoomCategory', room_category_name + ":" + room_category_num),
        ]

        for f in info:
            elm_var = self.xml.add_element(elm_product, 'Var')
            self.xml.add_element_with_text(elm_var, 'Name', f[0])
            self.xml.add_element_with_text(elm_var, 'Value', f[1])

        self.item_count += 1

    def write_full_sized_cover_cleat(self,elm_parts,spec_group):
        if self.cover_cleat_bp:
            closet_materials = bpy.context.scene.closet_materials
            cover_cleat = sn_types.Assembly(self.cover_cleat_bp)
            mat_sku = closet_materials.get_mat_sku(self.cover_cleat_bp, cover_cleat)
            mat_inventory_name = closet_materials.get_mat_inventory_name(sku=mat_sku)
            total_cover_cleat = 0
            for length in self.cover_cleat_lengths:
                total_cover_cleat += float(length)

            if total_cover_cleat <= 80:
                needed_full_lengths = 1
            else:
                needed_full_lengths = (total_cover_cleat/96)/2 #96
                if(mat_inventory_name == "Oxford White" or mat_inventory_name =="Cabinet Almond" or mat_inventory_name =="Duraply Almond" or mat_inventory_name =="Duraply White"):
                    needed_full_lengths = needed_full_lengths * 2
                needed_full_lengths = math.ceil(needed_full_lengths)
                if(needed_full_lengths < 3):
                    needed_full_lengths += 1
                elif(needed_full_lengths < 6):
                    needed_full_lengths += 2
                else:
                    needed_full_lengths += 3

            for i in range(0,needed_full_lengths):
                cover_cleat = sn_types.Assembly(self.cover_cleat_bp)
                cover_cleat.obj_x.location.x = sn_unit.inch(96)

                for child in cover_cleat.obj_bp.children:
                    if child.snap.type_mesh == 'CUTPART':
                        if not child.hide_viewport:
                            self.write_part_node(elm_parts, child, spec_group)    

    def write_full_sized_flat_crown(self, elm_parts, spec_group):
        if self.flat_crown_bp:
            flat_crown = sn_types.Assembly(self.flat_crown_bp)

            different_heights = []

            for height in self.flat_crown_heights:
                if height not in different_heights:
                    different_heights.append(height)

            for height in different_heights:
                total_flat_crown = 0
                for i in range(len(self.flat_crown_lengths)):
                    if(float(self.flat_crown_heights[i]) == float(height)):
                        total_flat_crown += float(self.flat_crown_lengths[i])

                needed_full_lengths = 0
                if(total_flat_crown < 80):  # In inches, total_flat_crown has already been converted to inches
                    needed_full_lengths = 1
                else:
                    needed_full_lengths = math.ceil((total_flat_crown / 96))  # 96
                    if(needed_full_lengths < 4):
                        needed_full_lengths += 1
                    elif(needed_full_lengths < 7):
                        needed_full_lengths += 2
                    else:
                        needed_full_lengths += 3

                for i in range(0, needed_full_lengths):
                    flat_crown.obj_y.location.y = float(sn_unit.inch_to_millimeter(height) / 1000)
                    flat_crown.obj_x.location.x = sn_unit.inch(96)
                    for child in flat_crown.obj_bp.children:
                        if child.snap.type_mesh == 'CUTPART':
                            if not child.hide_viewport:
                                self.write_part_node(elm_parts, child, spec_group)

    def write_full_sized_crown_molding(self,elm_parts,spec_group):     
        if self.crown_molding_bp:
            crown_molding = sn_types.Assembly(self.crown_molding_bp)
            
            total_crown_molding = 0
            for length in self.crown_molding_lengths:
                total_crown_molding += float(length)

            if(len(self.crown_molding_lengths)==1 and total_crown_molding < sn_unit.inch(93)):
                needed_full_lengths = 1
            else:
                needed_full_lengths = math.ceil((total_crown_molding/96)) #96
                if(needed_full_lengths < 4):
                    needed_full_lengths += 1
                elif(needed_full_lengths < 7):
                    needed_full_lengths += 2
                else:
                    needed_full_lengths += 3

            for i in range(0,needed_full_lengths):
                crown_molding = sn_types.Assembly(self.crown_molding_bp)
                crown_molding.obj_x.location.x = sn_unit.inch(96)
                crown_molding.obj_y.location.y = sn_unit.inch(2.5)
                crown_molding.obj_z.location.z = sn_unit.inch(0.625)
                crown_molding.obj_bp["IS_BP_CROWN_MOLDING"] = True
                self.write_part_node(elm_parts, crown_molding.obj_bp, spec_group)

    def write_full_sized_inverted_base(self,elm_parts,spec_group):     
        if self.inverted_base_bp:
            inverted_base = sn_types.Assembly(self.inverted_base_bp)
            inverted_base.obj_bp.snap.name_object = "Inverted Base"
            inverted_base.obj_x.location.x = sn_unit.inch(96)
            total_inverted_base = 0
            for length in self.inverted_base_lengths:
                total_inverted_base += float(length)
            if(len(self.inverted_base_lengths)==1 and total_inverted_base < sn_unit.inch(93)):
                needed_full_lengths = 1
            else:
                needed_full_lengths = math.ceil((total_inverted_base/96)) #96
                if(needed_full_lengths < 4):
                    needed_full_lengths += 1
                elif(needed_full_lengths < 7):
                    needed_full_lengths += 2
                else:
                    needed_full_lengths += 3

            for i in range(0,needed_full_lengths):
                self.write_part_node(elm_parts, inverted_base.obj_bp, spec_group)

    def write_full_sized_base_molding(self,elm_parts,spec_group):       
        if self.base_molding_bp:
            base_molding = sn_types.Assembly(self.base_molding_bp)
            total_base_molding = 0
            for length in self.base_molding_lengths:
                total_base_molding += float(length)

            if(len(self.base_molding_lengths)==1 and total_base_molding < sn_unit.inch(93)):
                needed_full_lengths = 1
            else:
                needed_full_lengths = math.ceil((total_base_molding/96)) #96
                if(needed_full_lengths < 4):
                    needed_full_lengths += 1
                elif(needed_full_lengths < 7):
                    needed_full_lengths += 2
                else:
                    needed_full_lengths += 3

            for i in range(0,needed_full_lengths):
                base_molding = sn_types.Assembly(self.base_molding_bp)
                base_molding.obj_x.location.x = sn_unit.inch(96)
                self.write_part_node(elm_parts, base_molding.obj_bp, spec_group)   

    def write_full_sized_tk_skin(self,elm_parts,spec_group):
        if self.tk_skin_bp:
            tk_skin = sn_types.Assembly(self.tk_skin_bp)
            different_heights = []

            for height in self.tk_skin_heights:
                if not height in different_heights:
                    different_heights.append(height)

            for height in different_heights:
                total_tk_skin = 0
                for i in range (len(self.tk_skin_lengths)):
                    if(float(self.tk_skin_heights[i]) == float(height)):
                        total_tk_skin += float(self.tk_skin_lengths[i])

                if(len(self.tk_skin_lengths)==1 and total_tk_skin < 93):
                    needed_full_lengths = 1
                elif(total_tk_skin < 80):
                    needed_full_lengths = 1
                else:
                    needed_full_lengths = math.ceil((total_tk_skin/96)) #96
                    if(needed_full_lengths < 4):
                        needed_full_lengths += 1
                    else:
                        needed_full_lengths += 2

                for i in range(0, needed_full_lengths):
                    tk_skin.obj_x.location.x = sn_unit.inch(96)
                    tk_skin.obj_y.location.y = float(sn_unit.inch_to_millimeter(float(height)) / 1000) + sn_unit.inch(1)
                    tk_skin.obj_z.location.z = sn_unit.inch(0.25)
                    for child in tk_skin.obj_bp.children:
                        if child.snap.type_mesh == 'CUTPART':
                            if not child.hide_get():
                                self.write_part_node(elm_parts, child, spec_group)

    def write_full_sized_hang_rod(self,elm_parts,spec_group):
        if self.hang_rod_bp and len(self.hang_rod_lengths) > 0:
            self.hang_rods_collected = True
            total_rod_length = 0
            for length in self.hang_rod_lengths:
                total_rod_length += float(length)

            rod_qty = math.ceil(total_rod_length / 96)
            self.write_hardware_node(elm_parts, self.hang_rod_bp, qty=rod_qty)
     
    def write_full_sized_cleat_stock(self,elm_parts,spec_group):
        if self.cleat_bp:
            closet_materials = bpy.context.scene.closet_materials
            cleat_assembly = sn_types.Assembly(self.cleat_bp)
            cleat_assembly.obj_x.location.x = sn_unit.inch(96)
            cleat_assembly.obj_y.location.y = sn_unit.inch(3.64)
            cleat_assembly.obj_bp["IS_WALL_CLEAT"] = False
            cleat_assembly.obj_bp.name = "Cleat Stock"
            cleat_assembly.obj_bp.snap.name_object = "Cleat Stock"

            mat_sku = closet_materials.get_mat_sku(cleat_assembly.obj_bp, cleat_assembly)
            mat_inventory_name = closet_materials.get_mat_inventory_name(sku=mat_sku)
            if(mat_inventory_name == "Oxford White" or mat_inventory_name =="Cabinet Almond" or mat_inventory_name =="Duraply Almond" or mat_inventory_name =="Duraply White"):
                if self.is_wrap_around:
                    for child in cleat_assembly.obj_bp.children:
                        if child.snap.type_mesh == 'CUTPART':
                            if not child.hide_viewport:
                                print("Adding Two White/Almond Cleat Stocks")
                                self.write_part_node(elm_parts, child, spec_group)
                                self.write_part_node(elm_parts, child, spec_group)
            else:
                for child in cleat_assembly.obj_bp.children:
                    if child.snap.type_mesh == 'CUTPART':
                        if not child.hide_viewport:
                            self.write_part_node(elm_parts, child, spec_group)
                            self.write_part_node(elm_parts, child, spec_group)

    def write_garage_legs(self, elm_parts, spec_group):
        if len(self.plastic_leg_list) > 0:
            needed_mounting_plates = 0
            needed_80_mm = 0
            needed_100_mm = 0
            needed_120_mm = 0
            needed_150_mm = 0
            obj = None
            for leg in self.plastic_leg_list:
                needed_mounting_plates += 1
                leg_assembly = sn_types.Assembly(leg)
                leg_height = leg_assembly.obj_z.location.z * 1000  # In millimeters
                if leg_height < 80:
                    needed_80_mm += 1
                elif leg_height < 100:
                    needed_100_mm += 1
                elif leg_height < 120:
                    needed_120_mm += 1
                else:
                    needed_150_mm += 1
                    leg_assembly.obj_z.location.z = sn_unit.millimeter(150)
                obj = leg

            self.write_hardware_node(elm_parts, obj, name='Plastic Leg Mounting Plates', qty=needed_mounting_plates)
            if needed_80_mm > 0:
                self.write_hardware_node(elm_parts, obj, name='80mm Plastic Legs', qty=needed_80_mm)
            if needed_100_mm > 0:
                self.write_hardware_node(elm_parts, obj, name='100mm Plastic Legs', qty=needed_100_mm)
            if needed_120_mm > 0:
                self.write_hardware_node(elm_parts, obj, name='120mm Plastic Legs', qty=needed_120_mm)
            if needed_150_mm > 0:
                self.write_hardware_node(elm_parts, obj, name='150mm Plastic Legs', qty=needed_150_mm)

        if len(self.metal_leg_list) > 0:
            needed_mounting_plates = 0
            needed_thread_insert = 0
            needed_levelers = 0
            total_steel_length = 0
            total_black_length = 0
            total_chrome_length = 0
            obj = None

            for leg in self.metal_leg_list:
                needed_mounting_plates += 1
                needed_thread_insert += 1
                needed_levelers += 1
                leg_assembly = sn_types.Assembly(leg)
                leg_length = sn_unit.meter_to_feet(leg_assembly.obj_z.location.z) # In millimeters
                parent_assembly = sn_types.Assembly(leg.parent)
                metal_color = parent_assembly.get_prompt("Metal Color")
                if metal_color:
                    if metal_color.get_value() == 0:
                        total_steel_length += leg_length
                    elif metal_color.get_value() == 1:
                        total_black_length += leg_length
                    elif metal_color.get_value() == 2:
                        total_chrome_length += leg_length
                    else:
                        print("Found Unknown Color: ", metal_color.get_value())
                obj = leg

            needed_steel_length = math.ceil(total_steel_length)
            needed_black_length = math.ceil(total_black_length)
            needed_chrome_length = math.ceil(total_chrome_length)

            self.write_hardware_node(elm_parts, obj, name='Metal Leg Mounting Plates', qty=needed_mounting_plates)
            self.write_hardware_node(elm_parts, obj, name='Thread Inserts', qty=needed_thread_insert)
            self.write_hardware_node(elm_parts, obj, name='Metal Leg Levelers', qty=needed_levelers)
            if needed_steel_length > 0:
                self.write_hardware_node(elm_parts, obj, name='Length of Brushed Steel Legs (in feet)', qty=needed_steel_length)
            if needed_chrome_length > 0:
                self.write_hardware_node(elm_parts, obj, name='Length Of Black Matte Legs (in feet)', qty=needed_black_length)
            if needed_black_length > 0:
                self.write_hardware_node(elm_parts, obj, name='Length Of Polished Chrome Legs (in feet)', qty=needed_chrome_length)


    def write_parts_for_product(self,elm_parts,obj_bp,spec_group):
        for child in obj_bp.children:
            #Write part nodes for cleat and append cover cleat length to cover_cleat_lengths
            if child.sn_closets.is_cleat_bp:
                for nchild in child.children:
                    if nchild.snap.type_mesh == 'CUTPART':
                        if not nchild.hide_viewport:
                            self.cleat_bp = child
                            self.write_part_node(elm_parts, nchild, spec_group)

                    if nchild.sn_closets.is_cleat_bp:
                        for nnchild in nchild.children:
                            if nnchild.snap.type_mesh == 'CUTPART':
                                if not nnchild.hide_viewport:
                                    #If it is an unhidden cover cleat cutpart, add it's length to cover_cleat_lengths
                                    cover_cleat_assembly = sn_types.Assembly(nnchild.parent)
                                    self.cover_cleat_bp = cover_cleat_assembly.obj_bp
                                    self.cover_cleat_lengths.append(self.get_part_length(cover_cleat_assembly))
                continue
            if child.sn_closets.is_crown_molding or child.sn_closets.is_base_molding:
                if(child.sn_closets.is_empty_molding):
                    if(child.sn_closets.is_crown_molding):
                        crown_molding_assembly = sn_types.Assembly(child)
                        length = self.get_part_length(crown_molding_assembly)
                        crown_to_ceiling = crown_molding_assembly.get_prompt("Crown To Ceiling").get_value()
                        self.crown_molding_bp = crown_molding_assembly.obj_bp
                        self.crown_molding_lengths.append(length)
                        if(crown_to_ceiling):
                            self.inverted_base_bp = crown_molding_assembly.obj_bp
                            self.inverted_base_lengths.append(length)
                    elif(child.sn_closets.is_base_molding):
                        base_molding_assembly = sn_types.Assembly(child)
                        self.base_molding_bp = child
                        self.base_molding_lengths.append(self.get_part_length(base_molding_assembly))
                else:
                    for nchild in child.children:
                        for nnchild in nchild.children:
                            if nnchild.snap.type_mesh == 'CUTPART':
                                if not nnchild.hide_viewport:
                                    if "IS_BP_FLAT_CROWN" in nchild:
                                        flat_crown_assembly = sn_types.Assembly(nnchild.parent)
                                        p_flat_crown_assembly = sn_types.Assembly(flat_crown_assembly.obj_bp.parent)
                                        EL = flat_crown_assembly.get_prompt("Exposed Left").get_value()
                                        ER = flat_crown_assembly.get_prompt("Exposed Right").get_value()
                                        EB = flat_crown_assembly.get_prompt("Exposed Back").get_value()
                                        var_height = p_flat_crown_assembly.get_prompt("Extend To Ceiling")
                                        length = self.get_part_length(flat_crown_assembly)
                                        height = float(self.get_part_width(flat_crown_assembly))
                                        if var_height:
                                            if var_height.get_value():
                                                height = height + 2

                                        if(not EL and not ER):
                                            self.flat_crown_heights.append(height)
                                        if(EL and ER):
                                            if(float(length) > 96):
                                                flat_crown_assembly.get_prompt("Exposed Left").set_value(False)
                                                flat_crown_assembly.get_prompt("Exposed Right").set_value(False)
                                                if(flat_crown_assembly.obj_bp.snap.name_object != "Right" and flat_crown_assembly.obj_bp.snap.name_object != "Left"):
                                                    self.flat_crown_bp = flat_crown_assembly.obj_bp
                                                number_of_lengths = math.ceil(length/96)
                                                if(number_of_lengths == 2):
                                                    self.single_exposed_flat_crown.append(True)
                                                    self.single_exposed_flat_crown.append(True)
                                                    if(EB):
                                                        self.top_edgebanded_flat_crown.append(True)
                                                        self.top_edgebanded_flat_crown.append(True)
                                                    self.flat_crown_lengths.append(sn_unit.inch(96))
                                                    self.flat_crown_lengths.append(sn_unit.inch(96))
                                                    self.flat_crown_heights.append(height)
                                                else:
                                                    self.single_exposed_flat_crown.append(True)
                                                    self.single_exposed_flat_crown.append(True)
                                                    if(EB):
                                                        self.top_edgebanded_flat_crown.append(True)
                                                        self.top_edgebanded_flat_crown.append(True)
                                                    self.flat_crown_lengths.append(sn_unit.inch(96))
                                                    self.flat_crown_lengths.append(sn_unit.inch(96))
                                                    self.flat_crown_heights.append(height)
                                                    number_of_lengths = number_of_lengths - 2
                                                    for x in range(number_of_lengths):
                                                        if(EB):
                                                            self.top_edgebanded_flat_crown.append(True)
                                                        self.flat_crown_lengths.append(sn_unit.inch(96))
                                                        self.flat_crown_heights.append(height)
                                            else:
                                                self.write_part_node(elm_parts, nnchild, spec_group)
                                        elif((EL and not ER) or (not EL and ER)):
                                            if(flat_crown_assembly.obj_bp.snap.name_object != "Right" and flat_crown_assembly.obj_bp.snap.name_object != "Left"):
                                                self.flat_crown_bp = flat_crown_assembly.obj_bp
                                            self.single_exposed_flat_crown.append(True)
                                            if(EB):
                                                self.top_edgebanded_flat_crown.append(True)
                                            self.flat_crown_lengths.append(self.get_part_length(flat_crown_assembly))
                                            self.flat_crown_heights.append(height)
                                        else:
                                            if(flat_crown_assembly.obj_bp.snap.name_object != "Right" and flat_crown_assembly.obj_bp.snap.name_object != "Left"):
                                                self.flat_crown_bp = flat_crown_assembly.obj_bp
                                            if(EB):
                                                self.top_edgebanded_flat_crown.append(True)
                                            self.flat_crown_lengths.append(self.get_part_length(flat_crown_assembly)) 
                    continue

            if child.sn_closets.is_toe_kick_skin_bp:
                for nchild in child.children:
                    if nchild.snap.type_mesh == 'CUTPART':
                        if not nchild.hide_viewport and not nchild.hide_get():
                            tk_skin_assembly = sn_types.Assembly(child)
                            if tk_skin_assembly.obj_bp.snap.name_object == "Toe Kick Skin":
                                self.tk_skin_bp = tk_skin_assembly.obj_bp
                            self.tk_skin_lengths.append(self.get_part_length(tk_skin_assembly))

                            height = float(self.get_part_width(tk_skin_assembly))
                            tk_assembly = sn_types.Assembly(child.parent)
                            var_height = tk_assembly.get_prompt("Variable Height")
                            if var_height:
                                if var_height.get_value():
                                    height += 2
                            self.tk_skin_heights.append(str(height)) 
                continue
                
            if child.snap.type_group == 'INSERT':
                continue

            for nchild in child.children:
                if nchild.snap.type_mesh == 'HARDWARE':
                    if not nchild.hide_viewport:
                        if 'IS_BP_BELT_RACK' not in child and 'IS_BP_TIE_RACK' not in child:
                            self.write_hardware_node(elm_parts, nchild)

                if nchild.snap.type_mesh in {'CUTPART','SOLIDSTOCK','BUYOUT'}:
                    if not nchild.hide_viewport:
                        self.write_part_node(elm_parts, nchild, spec_group)

            self.write_parts_for_product(elm_parts, child, spec_group)
            
    def get_subassemblies(self, obj_bp, subassemblies=None):
        if subassemblies is None:
            subassemblies = []

        for child in obj_bp.children:
            # Check panels for attached accessories
            if child.sn_closets.is_panel_bp:
                assembly = sn_types.Assembly(child)
                self.get_subassemblies(assembly.obj_bp, subassemblies)
                # Should we be checking if export_as_subassembly is true here?
            if child.get('IS_BP_ASSEMBLY') and child.snap.type_group == 'INSERT' and not child.get('IS_BP_CROWN_MOLDING'):  # I added this conditional for a fix with flat crown, but curious about the question above
                assembly = sn_types.Assembly(child)
                hide = assembly.get_prompt("Hide")
                if hide:
                    if hide.get_value():
                        continue
                subassemblies.append(assembly)

                self.get_subassemblies(assembly.obj_bp, subassemblies)

        return subassemblies

    def write_subassemblies_for_product(self, elm_product, obj_bp, spec_group, subassemblies=None):
        if subassemblies is None:
            subassemblies = self.get_subassemblies(obj_bp)
        
        for assembly in subassemblies:

            # Had to move some of the garage leg logic here due to how the assembly is set up
            if assembly.obj_bp.get('IS_BP_GARAGE_LEG'):
                hide = sn_types.Assembly(assembly.obj_bp).get_prompt("Hide") # Don't know why, but only retrieving the Hide prompt let me actually find the unhidden legs
                if hide:
                    if not hide.get_value():
                        for child in assembly.obj_bp.children:
                            for nchild in child.children:
                                if not nchild.hide_viewport:
                                    if child.get('IS_BP_PLASTIC_LEG'):
                                        if child not in self.plastic_leg_list:
                                            self.plastic_leg_list.append(child)
                                    elif child.get('IS_BP_METAL_LEG'):
                                        if child not in self.metal_leg_list:
                                            self.metal_leg_list.append(child)
                continue

            sub_name = assembly.obj_bp.snap.name_object if assembly.obj_bp.snap.name_object != "" else assembly.obj_bp.name
            elm_subassembly = self.xml.add_element(elm_product, "Assembly", {'ID': "IDA-{}".format(self.assembly_count)})
            self.xml.add_element_with_text(elm_subassembly, 'Name', sub_name)
            self.xml.add_element_with_text(elm_subassembly, 'Quantity', "1")

            if sub_name == "Top Shelf":
                for child in assembly.obj_bp.children:
                    if child.sn_closets.is_plant_on_top_bp:
                        top_shelf_assembly = sn_types.Assembly(child)
                        extend_left = assembly.get_prompt("Extend Left Amount")
                        extend_right = assembly.get_prompt("Extend Right Amount")
                        if extend_left and extend_right:
                            if (extend_left.get_value() > 0) or (extend_right.get_value() > 0):
                                self.is_wrap_around = True
                        if top_shelf_assembly.obj_x.location.x + sn_unit.inch(self.top_shelf_offset) > sn_unit.inch(96):
                            self.write_oversize_top_shelf(elm_subassembly, child)
                            self.assembly_count += 1
                            return

            self.write_parts_for_subassembly(elm_subassembly, assembly.obj_bp, spec_group)
            self.assembly_count += 1

            is_drawer_stack = assembly.obj_bp.sn_closets.is_drawer_stack_bp
            export_nested = assembly.obj_bp.snap.export_nested_subassemblies

            if is_drawer_stack or export_nested:
                self.write_nested_subassemblies(elm_subassembly, assembly.obj_bp, spec_group)

            if assembly.obj_bp.sn_closets.is_hamper_insert_bp:
                hamper_type = assembly.get_prompt("Hamper Type").get_value()
                self.write_hardware_node(elm_subassembly, obj_bp, name="Hamper Brake Flap Left")
                self.write_hardware_node(elm_subassembly, obj_bp, name="Hamper Brake Flap Right")
                self.write_hardware_node(elm_subassembly, obj_bp, name="Hamper Rack")

                if hamper_type == 1:
                    basket_width = round(sn_unit.meter_to_inch(assembly.obj_x.location.x), 2)
                    if basket_width >= 18.0:
                        if basket_width < 24.0:
                            self.write_hardware_node(elm_subassembly, obj_bp, name='HAMPER TILT OUT 18" 20H')
                        elif basket_width < 30.0:
                            self.write_hardware_node(elm_subassembly, obj_bp, name='HAMPER TILT OUT 24" 20H DOUBLE BAG')
                        else:
                            self.write_hardware_node(elm_subassembly, obj_bp, name='HAMPER TILT OUT 30" 20H DOUBLE BAG')
            
    def write_nested_subassemblies(self,elm_subassembly, obj_bp, spec_group):
        for child in obj_bp.children:
            if child.snap.export_as_subassembly and child.sn_closets.is_drawer_box_bp:
                assembly = sn_types.Assembly(child)
                hide = assembly.get_prompt("Hide")
                if hide:
                    if hide.get_value():
                        continue
                sub_name = assembly.obj_bp.snap.name_object if assembly.obj_bp.snap.name_object != "" else assembly.obj_bp.name
                elm_item = self.xml.add_element(elm_subassembly, 'Assembly', {'ID': "IDA-{}".format(self.assembly_count)})
                self.xml.add_element_with_text(elm_item, 'Name', sub_name)
                self.xml.add_element_with_text(elm_item, 'Quantity', "1")
                self.write_parts_for_subassembly(elm_item, assembly.obj_bp, spec_group)
                self.assembly_count += 1

    def write_parts_for_subassembly(self,elm_parts,obj_bp,spec_group):
        # Slides
        if obj_bp.get("IS_BP_DRAWER_BOX"):
            assembly = sn_types.Assembly(obj_bp)
            parent_assembly = sn_types.Assembly(obj_bp.parent)
            slide_type = assembly.get_prompt('Slide Type')
            if slide_type:
                if slide_type.get_value() == 0:

                    slide_size = 10
                    sizes = [10, 12, 14, 16, 18, 20, 22]
                    for size in sizes:
                        if sn_unit.meter_to_inch(assembly.obj_y.location.y) >= size:
                            slide_size = size

                    sidemount_options = parent_assembly.get_prompt("Sidemount Options")
                    if sidemount_options:
                        if sidemount_options.get_value() == 0:
                            self.write_hardware_node(elm_parts, obj_bp, name="Hafele BB " + str(slide_size) + "in")
                        else:
                            self.write_hardware_node(elm_parts, obj_bp, name="HR BB SC " + str(slide_size) + "in")
                else:

                    slide_size = 9
                    sizes = [9, 12, 15, 18, 21]
                    for size in sizes:
                        if sn_unit.meter_to_inch(assembly.obj_y.location.y) >= size:
                            slide_size = size

                    undermount_options = parent_assembly.get_prompt("Undermount Options")
                    if undermount_options:
                        if undermount_options.get_value() == 0:
                            self.write_hardware_node(elm_parts, obj_bp, name="Hettich 4D " + str(slide_size) + "in")
                            self.write_hardware_node(elm_parts, obj_bp, name="Hettich 4D Clip and Spacer set")
                        elif undermount_options.get_value() == 1:
                            self.write_hardware_node(elm_parts, obj_bp, name="Hettich V6 " + str(slide_size) + "in")
                            self.write_hardware_node(elm_parts, obj_bp, name="Hettich L & R Locking set")
                        elif undermount_options.get_value() == 2:
                            self.write_hardware_node(elm_parts, obj_bp, name="Blumotion UM " + str(slide_size) + "in")
                            self.write_hardware_node(elm_parts, obj_bp, name="Blumotion Locking Device L")
                            self.write_hardware_node(elm_parts, obj_bp, name="Blumotion Locking Device R")
                        else:
                            self.write_hardware_node(elm_parts, obj_bp, name="KING SLIDE UM SC " + str(slide_size) + "in")
                            self.write_hardware_node(elm_parts, obj_bp, name="KING LOCKING DEVICE LEFT")
                            self.write_hardware_node(elm_parts, obj_bp, name="KING LOCKING DEVICE RIGHT")
            else:
                
                self.write_hardware_node(elm_parts, obj_bp, name="Drawer Slide L")
                self.write_hardware_node(elm_parts, obj_bp, name="Drawer Slide R")
        #Slides
        if obj_bp.sn_closets.is_drawer_box_bp:
            drawers_dict = self.get_jewel_inserts_data(obj_bp)
            if len(drawers_dict) > 0:
                for drawer, inserts in drawers_dict.items():
                    for insert in inserts:
                        if insert != 'None':
                            self.write_hardware_node(elm_parts, drawer, name=insert)
        #Locked shelf - add KD fittings (4)
        if obj_bp.sn_closets.is_shelf_bp:
            assembly = sn_types.Assembly(obj_bp)
            is_locked_shelf = assembly.get_prompt("Is Locked Shelf").get_value()

            if is_locked_shelf:
                self.write_hardware_node(elm_parts, obj_bp, name="KD Fitting",qty=4)

        #Door lock for doors 
        if obj_bp.sn_closets.is_door_insert_bp:
            door_insert = sn_types.Assembly(obj_bp)
            lock_door = door_insert.get_prompt("Lock Door").get_value()
            double_door_auto_switch = door_insert.get_prompt("Double Door Auto Switch").get_value()
            double_door = door_insert.get_prompt("Force Double Doors").get_value()

            if lock_door:
                self.write_hardware_node(elm_parts, obj_bp, name="Door Lock")
                self.write_hardware_node(elm_parts, obj_bp, name="Door Lock Cam")

                #Double door
                if double_door or door_insert.obj_x.location.x > double_door_auto_switch:
                    self.write_hardware_node(elm_parts, obj_bp, name="Door Lock Latch")               

        for child in obj_bp.children:
            if child.sn_closets.is_toe_kick_skin_bp:
                for nchild in child.children:
                    if nchild.snap.type_mesh == 'CUTPART':
                        if not nchild.hide_viewport and not nchild.hide_get():
                            tk_skin_assembly = sn_types.Assembly(child)
                            if tk_skin_assembly.obj_bp.snap.name_object == "Toe Kick Skin":
                                self.tk_skin_bp = tk_skin_assembly.obj_bp
                            self.tk_skin_lengths.append(self.get_part_length(tk_skin_assembly))

                            height = float(self.get_part_width(tk_skin_assembly))
                            tk_assembly = sn_types.Assembly(child.parent)
                            var_height = tk_assembly.get_prompt("Variable Height")
                            if var_height:
                                if var_height.get_value():
                                    height += 2
                            self.tk_skin_heights.append(str(height))

                continue

            if child.sn_closets.is_hanging_rod:
                for nchild in child.children:
                    if not nchild.hide_viewport and not nchild.hide_get():
                        self.write_hardware_node(elm_parts, obj_bp, name="Pole Cup")
                        self.write_hardware_node(elm_parts, obj_bp, name="Pole Cup")  

            if child.snap.type_mesh == 'HARDWARE':
                needed_hardware = 0
                for nchild in child.children:
                    if not nchild.hide_viewport:
                        needed_hardware = 1
                
                # This is needed for specific single parts. We need them to export as hardware with sku numbers, they were exporting as products.
                if needed_hardware == 1:
                    if child.name == 'Sliding Panels Rack':
                        self.write_hardware_node(elm_parts, child, 'Pants Rack')
                    elif child.name == 'Single Pull Out Canvas Hamper':
                        self.write_hardware_node(elm_parts, child, name="Cloth Laundry Bag")
                    elif child.name == 'Double Pull Out Canvas Hamper':
                        self.write_hardware_node(elm_parts, child, name="Cloth Laundry Bag")
                        self.write_hardware_node(elm_parts, child, name="Cloth Laundry Bag")
                    continue

            for nchild in child.children:

                if nchild.snap.type_mesh == 'HARDWARE':
                    if not nchild.hide_viewport:
                        if obj_bp.sn_closets.is_hamper_insert_bp:  # Adding in all this hamper logic here to ensure we only export wire baskets here.
                            if child.sn_closets.is_hamper_bp:
                                hamper_assembly = sn_types.Assembly(obj_bp)
                                hamper_type = hamper_assembly.get_prompt("Hamper Type")
                                if hamper_type:
                                    if hamper_type.get_value() == 0:
                                        self.write_hardware_node(elm_parts, nchild)
                            else:
                                self.write_hardware_node(elm_parts, nchild)
                        else:
                            self.write_hardware_node(elm_parts, nchild)

                if nchild.snap.type_mesh in {'CUTPART','SOLIDSTOCK','BUYOUT'}:
                    if not nchild.hide_viewport:
                        self.write_part_node(elm_parts, nchild, spec_group)

    def get_jewel_inserts_data(self, obj_bp):
        drawers_dict = {}
        dad = obj_bp.parent
        dad_assy = sn_types.Assembly(dad)
        insert_indexes = []
        dad_width = round(sn_unit.meter_to_inch(dad_assy.obj_x.location.x))
        insert_indexes = []
        dad_dict = dad_assy.get_prompt_dict()
        dad_pmpts = dad_dict.items()
        dd_query = 'Use Double Drawer'
        dd_prompts = [v for v in dad_pmpts if dd_query in v[0] and v[1] == True]
        ji_query = 'Has Jewelry Insert'
        ji_prompts = [v for v in dad_pmpts if ji_query in v[0] and v[1] == True]
        si_query = 'Has Sliding Insert'
        si_prompts = [v for v in dad_pmpts if si_query in v[0] and v[1] == True]
        if len(dd_prompts) > 0 and len(ji_prompts) == 0:
            self.iterate_dbl_drawers(obj_bp, drawers_dict, dad, dad_assy,
                                     insert_indexes, dad_width, dd_prompts)
        if len(ji_prompts) > 0 and len(dd_prompts) == 0:
            self.iterate_jwl_inserts(obj_bp, drawers_dict, dad, dad_assy,
                                     insert_indexes, dad_width,
                                     ji_prompts, si_prompts)
        return drawers_dict

    def iterate_dbl_drawers(self, obj_bp, drawers_dict, dad, dad_assy, 
                            insert_indexes, dad_width, dd_prompts):
        for prompt in dd_prompts:
            siblings = {}
            siblings_by_idx = {}
            insert_number = re.findall(r'\d{1}', prompt[0])[0]
            insert_indexes.append(int(insert_number))
            for obj in dad.children:
                if obj.sn_closets.is_drawer_box_bp:
                    loc_z_metric = sn_unit.meter_to_inch(obj.location[2])
                    loc_z = round(loc_z_metric, 2)
                    siblings[loc_z] = obj
            for i, key in enumerate(sorted(siblings.keys())):
                siblings_by_idx[i + 1] = siblings[key]
            for index in insert_indexes:
                if siblings_by_idx[index].name == obj_bp.name:
                    insert_pmpt = dad_assy.get_prompt(
                        f"Jewelry Insert Type {index}")
                    if insert_pmpt is not None:
                        insert_type = insert_pmpt.get_value()
                        if insert_type == 0:
                            qry_dict = None
                            insert_width = 0
                            if 18 <= dad_width < 21:
                                insert_width = 18
                            elif 21 <= dad_width < 24:
                                insert_width = 21
                            elif 24 <= dad_width:
                                insert_width = 24
                            qry_up = f'Upper Jewelry Insert Velvet Liner {insert_width}in {insert_number}'
                            qry_down = f'Lower Jewelry Insert Velvet Liner {insert_width}in {insert_number}'
                            up = dad_assy.get_prompt(qry_up).get_value()
                            down = dad_assy.get_prompt(qry_down).get_value()
                            if insert_width == 18:
                                qry_dict = common_lists.JEWELRY_INSERTS_VELVET_LINERS_18IN_DICT
                            elif insert_width == 21:
                                qry_dict = common_lists.JEWELRY_INSERTS_VELVET_LINERS_21IN_DICT
                            elif insert_width == 24:
                                qry_dict = common_lists.JEWELRY_INSERTS_VELVET_LINERS_24IN_DICT
                            if qry_dict is not None:
                                up_label = qry_dict.get(up)
                                down_label = qry_dict.get(down)
                                drawers_dict[obj_bp] = []
                                drawers_dict[obj_bp].append(up_label)
                                drawers_dict[obj_bp].append(down_label)

    def iterate_jwl_inserts(self, obj_bp, drawers_dict, dad, dad_assy, 
                            insert_indexes, dad_width, ji_prompts, si_prompts):
        has_sld_ins = len(si_prompts) > 0
        for prompt in ji_prompts:
            siblings = {}
            siblings_by_idx = {}
            insert_number = re.findall(r'\d{1}', prompt[0])[0]
            insert_indexes.append(int(insert_number))
            for obj in dad.children:
                if obj.sn_closets.is_drawer_box_bp:
                    loc_z_metric = sn_unit.meter_to_inch(obj.location[2])
                    loc_z = round(loc_z_metric, 2)
                    siblings[loc_z] = obj
            for i, key in enumerate(sorted(siblings.keys())):
                siblings_by_idx[i + 1] = siblings[key]
            for index in insert_indexes:
                if siblings_by_idx[index].name == obj_bp.name:
                    insert_pmpt = dad_assy.get_prompt(
                        f"Jewelry Insert Type {index}")
                    if insert_pmpt is not None:
                        insert_type = insert_pmpt.get_value()
                        if insert_type == 1:
                            # Standard Opening
                            qry_ji = f'Jewelry Insert {dad_width}in {insert_number}'
                            qry_si = f'Sliding Insert {dad_width}in {insert_number}'
                            ji = dad_assy.get_prompt(qry_ji).get_value()
                            si = dad_assy.get_prompt(qry_si).get_value()
                            if dad_width == 18:
                                ji_label = common_lists.JEWELRY_INSERTS_18IN_DICT.get(ji)
                                si_label = common_lists.SLIDING_INSERTS_18IN_DICT.get(si)
                                drawers_dict[obj_bp] = []
                                drawers_dict[obj_bp].append(ji_label)
                                if has_sld_ins:
                                    drawers_dict[obj_bp].append(si_label)
                            elif dad_width == 21:
                                ji_label = common_lists.JEWELRY_INSERTS_21IN_DICT.get(ji)
                                si_label = common_lists.SLIDING_INSERTS_21IN_DICT.get(si)
                                drawers_dict[obj_bp] = []
                                drawers_dict[obj_bp].append(ji_label)
                                if has_sld_ins:
                                    drawers_dict[obj_bp].append(si_label)
                            elif dad_width == 24:
                                ji_label = common_lists.JEWELRY_INSERTS_24IN_DICT.get(ji)
                                si_label = common_lists.SLIDING_INSERTS_24IN_DICT.get(si)
                                drawers_dict[obj_bp] = []
                                drawers_dict[obj_bp].append(ji_label)
                                if has_sld_ins:
                                    drawers_dict[obj_bp].append(si_label)
                        elif insert_type == 2:
                            # Non-Standard, Great than 16" deep
                            if 18 <= dad_width < 21:
                                qry_ji = f'Lower Jewelry Insert Velvet Liner 18in {insert_number}'
                                ji = dad_assy.get_prompt(qry_ji).get_value()
                                ji_label = common_lists.JEWELRY_INSERTS_VELVET_LINERS_18IN_DICT.get(ji)
                                drawers_dict[obj_bp] = []
                                drawers_dict[obj_bp].append(ji_label)
                            elif 21 <= dad_width < 24:
                                qry_ji = f'Lower Jewelry Insert Velvet Liner 21in {insert_number}'
                                ji = dad_assy.get_prompt(qry_ji).get_value()
                                ji_label = common_lists.JEWELRY_INSERTS_VELVET_LINERS_21IN_DICT.get(ji)
                                drawers_dict[obj_bp] = []
                                drawers_dict[obj_bp].append(ji_label)
                            elif 24 <= dad_width:
                                qry_ji = f'Lower Jewelry Insert Velvet Liner 24in {insert_number}'
                                ji = dad_assy.get_prompt(qry_ji).get_value()
                                ji_label = common_lists.JEWELRY_INSERTS_VELVET_LINERS_24IN_DICT.get(ji)
                                drawers_dict[obj_bp] = []
                                drawers_dict[obj_bp].append(ji_label)
                        elif insert_type == 3:
                            # Non-Standard, Lower than 16" deep
                            qry_vl = f'Velvet Liner {insert_number}'
                            vl = dad_assy.get_prompt(qry_vl).get_value()
                            vl_label = common_lists.VELVET_LINERS_DICT.get(vl)
                            drawers_dict[obj_bp] = []
                            drawers_dict[obj_bp].append(vl_label)

    def write_parts_for_nested_subassembly(self,elm_parts,obj_bp,spec_group):
        for child in obj_bp.children:

            if child.snap.type_mesh == 'HARDWARE':
                if not child.hide_viewport:
                    self.write_hardware_node(elm_parts, child)

            if child.snap.type_mesh in {'CUTPART','SOLIDSTOCK','BUYOUT'}:
                if not child.hide_viewport:
                    self.write_part_node(elm_parts, child, spec_group)                  

    def write_prompts_for_assembly(self,elm_prompts,assembly):
        prompts_dict = get_export_prompts(assembly.obj_bp)
        for prompt in prompts_dict:
            elm_prompt = self.xml.add_element(elm_prompts,'Prompt',{'Name': prompt})
            prompt_value = prompts_dict[prompt]
            if prompt_value == 'True':
                prompt_value = str(1)
            if prompt_value == 'False':
                prompt_value = str(0)
            self.xml.add_element_with_text(elm_prompt,'Value',prompt_value)

        #HEIGHT ABOVE FLOOR FOR PRODUCT IS OVERRIDDEN BY THE Z ORIGIN
        if assembly.obj_bp.snap.type_group == 'PRODUCT':
            if assembly.obj_bp.location.z > 0:
                elm_prompt = self.xml.add_element(elm_prompts,'Prompt',"HeightAboveFloor")
                self.xml.add_element_with_text(elm_prompt,'Value',"0")                  
    
    def write_hardware_node(self, elm_product, obj_bp, name="", qty=1):
        if obj_bp.get('IS_BP_ASSEMBLY'):
            assembly = sn_types.Assembly(obj_bp=obj_bp)
        else:
            assembly = sn_types.Assembly(obj_bp.parent)

        if name != "":
            hardware_name = name
        else:
            hardware_name = obj_bp.snap.name_object if obj_bp.snap.name_object != "" else obj_bp.name

        part_length = self.distance(0)
        is_hanging_rod = assembly.obj_bp.sn_closets.is_hanging_rod
        rods_name = bpy.context.scene.sn_closets.closet_options.rods_name

        if is_hanging_rod:
            if "Oval" in rods_name:
                part_length = self.get_part_length(assembly)
            else:
                self.hang_rod_lengths.append(self.get_part_length(assembly))
                if self.hang_rod_bp is None:
                    self.hang_rod_bp = assembly.obj_bp
                if not self.hang_rods_collected:
                    return

        elm_hdw_part = self.xml.add_element(elm_product,
                                        'Part',
                                        {'ID': "IDP-{}".format(self.part_count),
                                        'LabelID': "IDL-{}".format(self.label_count)                          
                                        })
        
        self.xml.add_element_with_text(elm_hdw_part, 'Name', hardware_name)
        self.xml.add_element_with_text(elm_hdw_part, 'Quantity', str(qty))
        self.xml.add_element_with_text(elm_hdw_part, 'Routing', "HDSTK")#Str literal OKAY
        self.xml.add_element_with_text(elm_hdw_part, 'Type', "hardware")#Str literal OKAY

        lbl = [
            ("IDL-{}".format(self.label_count), "IDJ-{}".format(self.job_count), "IDP-{}".format(self.part_count)),
            ("name", "text", hardware_name),
            ("wallname", "text", 'Island' if sn_utils.get_closet_bp(obj_bp).get("IS_BP_ISLAND") else sn_utils.get_wall_bp(obj_bp).snap.name_object),
            ("x", "text", "0"),
            ("y", "text", "0"),
            ("z", "text", "0"),
            ("lenx", "text", part_length),
            ("leny", "text", "0"),
            ("lenz", "text", "0"),
            ("rotx", "text", str(int(math.degrees(assembly.obj_bp.rotation_euler.x)))),
            ("roty", "text", str(int(math.degrees(assembly.obj_bp.rotation_euler.y)))),
            ("rotz", "text", str(int(math.degrees(assembly.obj_bp.rotation_euler.z)))),
            ("material", "text", ""),#Str literal OKAY
            ("copies", "text", ""),#Str literal OKaY
            ("sku", "text", get_hardware_sku(obj_bp, assembly, hardware_name)),#Get sku value from Database
            ("color", "text", ""),#Str literal OKAY
            ("type", "text", "hardware")#Str literal OKAY
        ]

        self.labels.append(lbl)
        self.label_count += 1
        self.part_count += 1

    def is_wood_part(self, obj, assembly, mat_inventory_name):
        """
        Used to determine if a part is a 'Wood Part' that needs a routing of 'No_Cut'
        and a class of 'Draw'. We can add to this logic as more wooden parts are
        created.
        """
        wooden_materials = ["BBBB", "1/4 BIRCH VENEER PRE FINISHED"]
        obj_props = assembly.obj_bp.sn_closets
        if(obj_props.is_door_bp or obj_props.is_drawer_front_bp or obj_props.is_hamper_front_bp or obj.get('IS_DOOR') or obj.get('IS_BP_DRAWER_FRONT')):
            if(assembly.get_prompt("Door Style")):
                door_style = assembly.get_prompt("Door Style").get_value()
                if (door_style != "Slab Door") and (door_style != "Melamine Glass Door"):
                    return True
        for cur_mat in wooden_materials:
            if cur_mat in mat_inventory_name:
                return True
        return False

    def write_part_node(self,node,obj,spec_group):
        if obj.get('IS_BP_ASSEMBLY'):
            assembly = sn_types.Assembly(obj_bp=obj)
        else:
            assembly = sn_types.Assembly(obj.parent)
        if assembly.obj_bp.snap.type_group != "PRODUCT":

            obj_props = assembly.obj_bp.sn_closets
            closet_materials = bpy.context.scene.closet_materials

            if obj_props.is_shelf_bp or obj_props.is_glass_shelf_bp:
                    is_locked_shelf = assembly.get_prompt("Is Locked Shelf")
                    shelf_qty = 1

                    for child in assembly.obj_bp.children:
                        if child.snap.type_mesh in ('CUTPART', 'BUYOUT'):
                            try:
                                shelf_qty = child.modifiers['ZQuantity'].count
                            except KeyError:
                                print("Writing Shelf Part - 'ZQuantity' modifier not found.")            

                    for _ in range(shelf_qty):
                        if is_locked_shelf and is_locked_shelf.get_value() == True:
                            self.write_hardware_node(node, assembly.obj_bp, name="KD Fitting", qty=4)

                        else:
                            self.write_hardware_node(node, assembly.obj_bp, name="Peg Chrome", qty=4)
            if assembly.obj_bp.get('IS_BP_L_SHELF') or assembly.obj_bp.get('IS_BP_ANGLE_SHELF'):
                parent_assembly = sn_types.Assembly(assembly.obj_bp.parent)

                is_locked_shelf = assembly.get_prompt("Is Locked Shelf")
                add_backing = parent_assembly.get_prompt("Add Backing")

                quantity = 5
                if add_backing:
                    if add_backing.get_value():
                        quantity = 6

                if is_locked_shelf:
                    if is_locked_shelf.get_value():
                        self.write_hardware_node(node, assembly.obj_bp, name="KD Fitting",qty=quantity)
                    else:
                        self.write_hardware_node(node, assembly.obj_bp, name="Peg Chrome", qty=quantity)
                else:
                    self.write_hardware_node(node, assembly.obj_bp, name="Peg Chrome", qty=quantity)

            #----------Add part name
            if obj.type == 'CURVE':
                part_name = obj.snap.name_object if obj.snap.name_object != "" else obj.name
            else:
                part_name = assembly.obj_bp.snap.name_object if assembly.obj_bp.snap.name_object != "" else assembly.obj_bp.name

                is_locked_shelf = assembly.get_prompt("Is Locked Shelf")                

                #TODO: This is for old lib data, correct part names now set on assembly creation
                if part_name == "Panel":
                    part_name = "Partition"
                if part_name == "Top":
                    part_name = "Top Shelf"
                if is_locked_shelf and is_locked_shelf.get_value() == True:
                    if assembly.obj_bp.parent.get("IS_BP_L_SHELVES"):
                        part_name = "L KD Shelf"
                    elif assembly.obj_bp.parent.get("IS_BP_CORNER_SHELVES"):
                        part_name = "Corner KD Shelf"
                    else:
                        part_name = "KD Shelf"
                if part_name == "Shelf" :
                    part_name = "Adj Shelf"
                if part_name == 'Left Filler' or part_name == 'Right Filler':
                    part_name = 'Filler'
                if 'Accessory Cleat' in part_name:
                    part_name = 'Wall Cleat'
            part_name_splitted = part_name.split(".")
            part_name = part_name_splitted[0]            
            mat_sku = closet_materials.get_mat_sku(obj, assembly, part_name)
            mat_inventory_name = closet_materials.get_mat_inventory_name(sku=mat_sku)
            
            if part_name == "Cover Cleat":
                if mat_inventory_name == "Oxford White" or  mat_inventory_name =="Duraply White":
                    mat_inventory_name = "White Paper 11300"
                    mat_sku = "PM-0000002"
                elif mat_inventory_name == "Cabinet Almond" or mat_inventory_name =="Duraply Almond":
                    mat_inventory_name = "Almond Paper 11300"
                    mat_sku = "PM-0000001"

            if assembly.obj_bp.get('IS_BP_LAYERED_CROWN'):
                part_name = 'Layered Crown'

            if(part_name == "File Rail"):
                    mat_inventory_name = "White Paper 12310"
                    mat_sku = "PM-0000004"
            if obj_props.is_countertop_bp:
                l_assembly_end_cond = assembly.get_prompt("Exposed Left")
                r_assembly_end_cond = assembly.get_prompt("Exposed Right")

                if l_assembly_end_cond and l_assembly_end_cond.get_value() != True:
                        assembly.obj_x.location.x += sn_unit.inch(3)
                if r_assembly_end_cond and r_assembly_end_cond.get_value() != True:
                    assembly.obj_x.location.x += sn_unit.inch(3)
            if(part_name == "Inverted Base"):
                mat_inventory_name = "BASE ALDER 3 1/4X1/2 WM633"
                mat_sku = "MD-0000025"

            mat_id = self.write_material(mat_inventory_name, mat_sku)

            elm_part = self.xml.add_element(
                node,
                'Part',
                {
                    'ID': "IDP-{}".format(self.part_count),
                    'MatID': "IDM-{}".format(mat_id),
                    'LabelID': "IDL-{}".format(self.label_count),
                    'OpID': "IDOP-{}".format(self.op_count)
                }
            )

            self.xml.add_element_with_text(elm_part, 'Name', part_name)
            self.xml.add_element_with_text(elm_part,'Quantity', self.get_part_qty(assembly))
            self.xml.add_element_with_text(elm_part,'Width', self.get_part_width(assembly)) 
            self.xml.add_element_with_text(elm_part,'FinishedWidth', self.get_part_width(assembly))           
            self.xml.add_element_with_text(elm_part,'Length', self.get_part_length(assembly))
            self.xml.add_element_with_text(elm_part,'FinishedLength', self.get_part_length(assembly))
            self.xml.add_element_with_text(elm_part,'Thickness',self.distance(sn_utils.get_part_thickness(obj)))
            self.xml.add_element_with_text(elm_part,'FinishedThickness', self.distance(sn_utils.get_part_thickness(obj)))
            if(part_name == "Cover Cleat"):
                if(mat_inventory_name == "White Paper 11300" or mat_inventory_name == "Almond Paper 11300"):
                    self.xml.add_element_with_text(elm_part, 'Routing', "No_Cut")  # Str literal okay
                    self.xml.add_element_with_text(elm_part, 'Class', "draw")  # Str literal okay
                else:
                    self.xml.add_element_with_text(elm_part, 'Routing', "SK1")  # Str literal okay
                    self.xml.add_element_with_text(elm_part, 'Class', "make")  # Str literal okay
            elif(part_name == "Toe Kick Stringer"):
                self.xml.add_element_with_text(elm_part, 'Routing', "No_Cut")  # Str literal okay
                self.xml.add_element_with_text(elm_part, 'Class', "draw")  # Str literal okay
            if self.is_wood_part(obj, assembly, mat_inventory_name):
                self.xml.add_element_with_text(elm_part, 'Routing', "No_Cut")  # Str literal okay
                self.xml.add_element_with_text(elm_part, 'Class', "draw")  # Str literal okay
            else:
                self.xml.add_element_with_text(elm_part, 'Routing', "SK1")  # Str literal okay
                self.xml.add_element_with_text(elm_part, 'Class', "make")  # Str literal okay

            if obj.sn_closets.is_crown_molding:
                self.xml.add_element_with_text(elm_part,'Type', "molding")
            else:
                self.xml.add_element_with_text(elm_part,'Type', "panel") #"panel" for part "unknown" for solid stock

            elm_unit = self.xml.add_element(elm_part,'Unit')
            self.xml.add_element_with_text(elm_unit,'Name', "dimension")#Str literal okay
            self.xml.add_element_with_text(elm_unit,'Measure', "inch")#Str literal okay
            self.xml.add_element_with_text(elm_unit,'RoundFactor', "0")#Str literal okay


            obj_props = assembly.obj_bp.sn_closets
            closet_materials = bpy.context.scene.closet_materials

            #EDGEBANDING
            primary_edge_color_name = ''
            edge_1 = ''
            edge_2 = ''
            edge_3 = ''
            edge_4 = ''
            edge_1_sku = ''
            edge_2_sku = ''
            edge_3_sku = ''
            edge_4_sku = ''

            edge_color_name = closet_materials.get_edge_inventory_name(closet_materials.get_edge_sku(obj, assembly, part_name))
            secondary_edge_color_name = closet_materials.get_edge_inventory_name(closet_materials.get_secondary_edge_sku(obj, assembly, part_name))
            door_drawer_edge_color_name = closet_materials.get_edge_inventory_name(closet_materials.get_edge_sku(obj, assembly, part_name))

            if obj_props.is_cleat_bp:
                edge_1_color_name = secondary_edge_color_name
                edge_2_color_name = secondary_edge_color_name
                edge_3_color_name = secondary_edge_color_name
                edge_4_color_name = secondary_edge_color_name
                primary_edge_color_name = secondary_edge_color_name

            elif obj_props.is_door_bp or obj_props.is_drawer_front_bp:
                edge_1_color_name = door_drawer_edge_color_name
                edge_2_color_name = door_drawer_edge_color_name
                edge_3_color_name = door_drawer_edge_color_name
                edge_4_color_name = door_drawer_edge_color_name
                primary_edge_color_name = door_drawer_edge_color_name
            else:
                edge_1_color_name = edge_color_name
                edge_2_color_name = edge_color_name
                edge_3_color_name = edge_color_name
                edge_4_color_name = edge_color_name
                primary_edge_color_name = edge_color_name

            #Doors
            if obj_props.is_door_bp or obj_props.is_hamper_front_bp:
                door_style = "Slab Door"
                door_style_ppt = assembly.get_prompt("Door Style")
                if door_style_ppt:
                    door_style = door_style_ppt.get_value()
                if door_style == "Slab Door":
                    if(abs(assembly.obj_x.location.x)<abs(assembly.obj_y.location.y)):
                        edge_1 = "L1"
                        edge_2 = "S1"
                        edge_3 = "L2"
                        edge_4 = "S2"
                    else:
                        edge_1 = "S1"
                        edge_2 = "L1"
                        edge_3 = "S2"
                        edge_4 = "L2"
                    edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                    edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                    edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                    edge_4_sku = closet_materials.get_edge_sku(obj, assembly, part_name)

            #Panel, Shelf
            if (obj_props.is_panel_bp or obj_props.is_shelf_bp) and (not obj_props.is_glass_shelf_bp or obj.get('IS_GLASS_SHELF')):
                #If the Panels/Shelves are attached to an Island
                if(obj.parent.parent and obj.parent.parent.sn_closets.is_island and sn_types.Assembly(obj.parent.parent).get_prompt("Depth 2")):
                    if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                        edge_2 = "L1"
                        edge_4 = "L2"
                    else:
                        edge_2 = "S1"
                        edge_4 = "S2"
                    edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                    edge_4_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                else:
                    if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                        edge_2 = "L1"
                    else:
                        edge_2 = "S1"
                    edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                    exposed_bottom = assembly.get_prompt("Exposed Bottom")
                    if exposed_bottom:
                        if exposed_bottom.get_value() or assembly.obj_x.location.x <= sn_unit.inch(46.10):
                            if(abs(assembly.obj_x.location.x) > abs(assembly.obj_y.location.y)):
                                edge_1 = "S1"
                                edge_3 = "S2"
                            else:
                                edge_1 = "L1"
                                edge_3 = "L2"
                            edge_1_sku = closet_materials.get_secondary_edge_sku(obj, assembly, part_name)
                            edge_3_sku = closet_materials.get_secondary_edge_sku(obj, assembly, part_name)
                            edge_1_color_name = secondary_edge_color_name
                            edge_3_color_name = secondary_edge_color_name

            #Blind Corner Panels
            if obj_props.is_blind_corner_panel_bp:
                if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                    edge_1 = "S1"
                    edge_2 = "L1"
                    edge_3 = "S2"
                else:
                    edge_1 = "L1"
                    edge_2 = "S1"
                    edge_3 = "L2"
                edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)    
                edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)

            # Angled Shelves
            if obj_props.is_angle_shelf_bp:
                if part_name == "Angled Top Shelf":
                    if obj.parent:
                        if obj.parent.parent:
                            exposed_left = sn_types.Assembly(obj.parent.parent).get_prompt('Exposed Left')
                            exposed_right = sn_types.Assembly(obj.parent.parent).get_prompt('Exposed Right')
                            if exposed_left and exposed_right:
                                if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                                    if exposed_left.get_value():
                                        edge_2 = "L1"
                                        edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                                        if exposed_right.get_value():
                                            edge_4 = "L2"
                                            edge_4_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                                    elif exposed_right.get_value():
                                        edge_2 = "L1"
                                        edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                                else:
                                    if exposed_left.get_value():
                                        edge_2 = "S1"
                                        edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                                        if exposed_right.get_value():
                                            edge_4 = "S2"
                                            edge_4_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                                        elif exposed_right.get_value():
                                            edge_2 = "S1"
                                            edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)

                                edge_3 = "CORNER"
                                edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)

            #Drawers
            if obj_props.is_drawer_front_bp:
                if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                    edge_1 = "L1"
                    edge_2 = "S1"
                    edge_3 = "L2"
                    edge_4 = "S2"
                else:
                    edge_1 = "S1"
                    edge_2 = "L1"
                    edge_3 = "S2"
                    edge_4 = "L2"
                edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)    
                edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                edge_4_sku = closet_materials.get_edge_sku(obj, assembly, part_name)                            

            if obj_props.is_drawer_sub_front_bp:
                if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                    edge_2 = "L1"
                else:
                    edge_2 = "S1"
                edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name) 

            if obj_props.is_drawer_side_bp:
                if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                    edge_2 = "S1"
                else:
                    edge_2 = "L1"
                edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name) 

            if obj_props.is_drawer_back_bp:
                if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                    edge_2 = "L1"
                else:
                    edge_2 = "S1"
                edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name) 
            
            if obj_props.is_file_rail_bp:
                if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                    edge_2 = "S1"
                else:
                    edge_2 = "L1"
                edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)

            #Cleats
            if obj_props.is_cleat_bp or "IS_CLEAT" in assembly.obj_bp:
                if obj_props.is_cover_cleat_bp:                                    
                    if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                        edge_2 = "L1"
                    else:
                        edge_2 = "S1"
                    if(mat_inventory_name == "Oxford White" or mat_inventory_name =="Duraply White" or mat_inventory_name =="White Paper 11300"):
                        edge_2_sku = "EB-0000316"
                    elif(mat_inventory_name == "Cabinet Almond" or mat_inventory_name =="Duraply Almond" or mat_inventory_name =="Almond Paper 11300"):
                        edge_2_sku = "EB-0000315"
                    else:
                        edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                elif assembly.obj_bp.get("IS_WALL_CLEAT"):
                    #Wall Cleat
                    exposed_left = assembly.get_prompt('Exposed Left')
                    exposed_top = assembly.get_prompt('Exposed Top')
                    exposed_right = assembly.get_prompt('Exposed Right')
                    exposed_bottom = assembly.get_prompt('Exposed Bottom')
                    edgebanding_prompts = [exposed_left,exposed_top,exposed_right,exposed_bottom]
                    if all(edgebanding_prompts):
                        if(abs(assembly.obj_x.location.x)<abs(assembly.obj_y.location.y)):
                            if exposed_left.get_value():
                                edge_1 ="L1"
                                edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                                if exposed_right.get_value():
                                    edge_3 ="L2"
                                    edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                            elif exposed_right.get_value():
                                edge_3 ="L1"
                                edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name) 

                            if exposed_top.get_value():
                                edge_2 ="S1"
                                edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                                if exposed_bottom.get_value():
                                    edge_4 ="S2"
                                    edge_4_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                            elif exposed_bottom.get_value():
                                edge_4 ="S1"        
                        else:
                            if exposed_left.get_value():
                                edge_1 ="S1"
                                edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                                if exposed_right.get_value():
                                    edge_3 ="S2"
                                    edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                            elif exposed_right.get_value():
                                edge_3 ="S1"
                                edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name) 

                            if exposed_top.get_value():
                                edge_2 ="L1"
                                edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                                if exposed_bottom.get_value():
                                    edge_4 ="L2"
                                    edge_4_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                            elif exposed_bottom.get_value():
                                edge_4 ="L1"        

                    else:   
                        if(abs(assembly.obj_x.location.x)<abs(assembly.obj_y.location.y)):
                            edge_1 = "L1"
                            edge_2 = "S1"
                            edge_3 = "L2"
                            edge_4 = "S2"
                        else:
                            edge_1 = "S1"
                            edge_2 = "L1"
                            edge_3 = "S2"
                            edge_4 = "L2"
                        edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                        edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                        edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                        edge_4_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                else:
                    if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                        edge_2 = "L1"
                    else:
                        edge_2 = "S1"
                    edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)

            #Door striker
            if  obj_props.is_door_striker_bp:
                if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                    edge_2 = "L1"
                else:
                    edge_2 = "S1"
                edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)                

            #L Shelf
            if obj_props.is_l_shelf_bp:
                if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                    edge_1 = "L1"
                    edge_2 = "L1"
                else:
                    edge_2 = "S1"
                    edge_2 = "S1"
                edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)                
                edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)                

            #Shelf lip
            if obj_props.is_shelf_lip_bp:
                if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                    edge_2 = "L1"
                else:
                    edge_2 = "S1"
                edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name) 

            #Top shelf
            if obj_props.is_plant_on_top_bp:
                is_countertop_ppt = assembly.get_prompt("Is Countertop")
                if is_countertop_ppt and is_countertop_ppt.get_value() == False:

                    if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                        edge_2 = "L1"
                    else:
                        edge_2 = "S1"
                    edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                    
                    carcass_bp = sn_utils.get_closet_bp(obj)
                    if carcass_bp.get('IS_BP_L_SHELVES'):
                        exposed_left = assembly.get_prompt("Exposed Left")
                        exposed_right = assembly.get_prompt("Exposed Right")
                        if exposed_left and exposed_right:
                            if exposed_left.get_value() or exposed_right.get_value():
                                if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                                    edge_1 = "S1"
                                else:
                                    edge_1 = "L1"
                                edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                    else:
                        carcass_assembly = sn_types.Assembly(carcass_bp)
                        l_carcass_end_cond_prompt = carcass_assembly.get_prompt("Left End Condition")
                        r_carcass_end_cond_prompt = carcass_assembly.get_prompt("Right End Condition")
                        l_carcass_end_cond = ''
                        r_carcass_end_cond = ''
                        if l_carcass_end_cond_prompt and r_carcass_end_cond_prompt:
                            l_carcass_end_cond = l_carcass_end_cond_prompt.get_value()
                            r_carcass_end_cond = r_carcass_end_cond_prompt.get_value()
                        l_assembly_end_cond_prompt = assembly.get_prompt("Exposed Left")
                        r_assembly_end_cond_prompt = assembly.get_prompt("Exposed Right")
                        b_assembly_end_cond_prompt = assembly.get_prompt("Exposed Back")
                        l_assembly_end_cond = ''
                        r_assembly_end_cond = ''
                        b_assembly_end_cond = ''
                        if l_assembly_end_cond_prompt and r_assembly_end_cond_prompt and b_assembly_end_cond_prompt:
                            l_assembly_end_cond = l_assembly_end_cond_prompt.get_value()
                            r_assembly_end_cond = r_assembly_end_cond_prompt.get_value()
                            b_assembly_end_cond = b_assembly_end_cond_prompt.get_value()
                        if (l_carcass_end_cond == 0 and r_carcass_end_cond != 0) or (l_assembly_end_cond == True and r_assembly_end_cond != True):
                            if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                                edge_1 = "S1"
                            else:
                                edge_1 = "L1"
                            edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)                  

                        if (l_carcass_end_cond != 0 and r_carcass_end_cond == 0) or (l_assembly_end_cond != True and r_assembly_end_cond == True):
                            if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                                edge_3 = "S2"
                            else:
                                edge_3 = "L2"
                            edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)

                        if (l_carcass_end_cond == 0 and r_carcass_end_cond == 0) or (l_assembly_end_cond == True and r_assembly_end_cond == True):
                            if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                                edge_1 = "S1"
                                edge_3 = "S2"
                            else:
                                edge_1 = "L1"
                                edge_3 = "L2"
                            edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                            edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                        
                        if(b_assembly_end_cond):
                            if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                                edge_4 = "L2"
                            else:
                                edge_4 = "S2"
                            edge_4_sku = closet_materials.get_edge_sku(obj, assembly, part_name)

            #Edge Bottom Of Filler
            if obj_props.is_filler_bp:
                carcass_bp = sn_utils.get_closet_bp(obj)
                carcass_assembly = sn_types.Assembly(carcass_bp)
                edge_bottom_of_left_filler = carcass_assembly.get_prompt("Edge Bottom of Left Filler")
                edge_bottom_of_right_filler = carcass_assembly.get_prompt("Edge Bottom of Right Filler")
                if  part_name == "Left Filler":
                    if edge_bottom_of_left_filler:
                        if edge_bottom_of_left_filler.get_value():
                            if(abs(assembly.obj_x.location.x) > abs(assembly.obj_y.location.y)):
                                edge_3 = "S1"
                            else:
                                edge_3 = ""
                            edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)

                    # removing distinction between right and left filler
                    part_name = 'Filler'
                if  part_name == "Right Filler":
                    if edge_bottom_of_right_filler:
                        if edge_bottom_of_right_filler.get_value():
                            if(abs(assembly.obj_x.location.x) > abs(assembly.obj_y.location.y)):
                                edge_3 = "S1"
                            else:
                                edge_3 = ""
                            edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)

                    # removing distinction between right and left filler
                    part_name = 'Filler'
                #Left Capping Filler
                if  part_name == "Left Capping Filler":
                    if(abs(assembly.obj_x.location.x) > abs(assembly.obj_y.location.y)):
                        edge_1 = "S1"
                        edge_2 = "L1"
                        edge_3 = "S2"
                    else:
                        edge_1 = "L1"
                        edge_2 = "S1"
                        edge_3 = "L2"
                    edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                    edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                    edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                #Left Capping Filler
                if  part_name == "Right Capping Filler":
                    if(abs(assembly.obj_x.location.x) > abs(assembly.obj_y.location.y)):
                        edge_1 = "S1"
                        edge_2 = "L1"
                        edge_3 = "S2"
                    else:
                        edge_1 = "L1"
                        edge_2 = "S1"
                        edge_3 = "L2"
                    edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                    edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                    edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
            #Bottom Capping
            if obj_props.is_closet_bottom_bp:
                if(assembly.get_prompt("Is Countertop").get_value() == False):
                    if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                        edge_2 = "L1"
                    else:
                        edge_2 = "S1"
                    edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                    
                    carcass_bp = sn_utils.get_closet_bp(obj)
                    carcass_assembly = sn_types.Assembly(carcass_bp)
                    l_carcass_end_cond_prompt = carcass_assembly.get_prompt("Left End Condition")
                    r_carcass_end_cond_prompt = carcass_assembly.get_prompt("Right End Condition")
                    l_carcass_end_cond = ''
                    r_carcass_end_cond = ''
                    if l_carcass_end_cond_prompt and r_carcass_end_cond_prompt:
                        l_carcass_end_cond = l_carcass_end_cond_prompt.get_value()
                        r_carcass_end_cond = r_carcass_end_cond_prompt.get_value()
                    l_assembly_end_cond_prompt = assembly.get_prompt("Exposed Left")
                    r_assembly_end_cond_prompt = assembly.get_prompt("Exposed Right")
                    b_assembly_end_cond_prompt = assembly.get_prompt("Exposed Back")
                    l_assembly_end_cond = ''
                    r_assembly_end_cond = ''
                    b_assembly_end_cond = ''
                    if l_assembly_end_cond_prompt and r_assembly_end_cond and b_assembly_end_cond:
                        l_assembly_end_cond = l_assembly_end_cond_prompt.get_value()
                        r_assembly_end_cond = r_assembly_end_cond_prompt.get_value()
                        b_assembly_end_cond = b_assembly_end_cond_prompt.get_value()
                    if (l_carcass_end_cond == 'EP' and r_carcass_end_cond != 'EP') or (l_assembly_end_cond == True and r_assembly_end_cond != True):
                        if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                            edge_1 = "S1"
                        else:
                            edge_1 = "L1"
                        edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)                  

                    if (l_carcass_end_cond != 'EP' and r_carcass_end_cond == 'EP') or (l_assembly_end_cond != True and r_assembly_end_cond == True):
                        if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                            edge_3 = "S2"
                        else:
                            edge_3 = "L2"
                        edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)

                    if (l_carcass_end_cond == 'EP' and r_carcass_end_cond == 'EP') or (l_assembly_end_cond == True and r_assembly_end_cond == True):
                        if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                            edge_1 = "S1"
                            edge_3 = "S2"
                        else:
                            edge_1 = "L1"
                            edge_3 = "L2"
                        edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                        edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                    
                    if(b_assembly_end_cond):
                        if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                            edge_4 = "L2"
                        else:
                            edge_4 = "S2"
                        edge_4_sku = closet_materials.get_edge_sku(obj, assembly, part_name)

            # Counter Top
            if obj_props.is_countertop_bp:
                if assembly.obj_bp.parent and assembly.obj_bp.parent.sn_closets.is_island:
                    l_assembly_end_cond_prompt = assembly.get_prompt("Exposed Left")
                    r_assembly_end_cond_prompt = assembly.get_prompt("Exposed Right")
                    l_assembly_end_cond = ''
                    r_assembly_end_cond = ''
                    if l_assembly_end_cond_prompt and r_assembly_end_cond_prompt:
                        l_assembly_end_cond = l_assembly_end_cond_prompt.get_value()
                        r_assembly_end_cond = r_assembly_end_cond_prompt.get_value()
                    if(l_assembly_end_cond and r_assembly_end_cond):
                        if(abs(assembly.obj_x.location.x) > abs(assembly.obj_y.location.y)):
                            edge_1 = "S1"
                            edge_2 = "L1"
                            edge_3 = "S2"
                            edge_4 = "L2"
                        else:
                            edge_1 = "L1"
                            edge_2 = "S1"
                            edge_3 = "L2"
                            edge_4 = "S2"
                        edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                        edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                        edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                        edge_4_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                    elif(l_assembly_end_cond == False and r_assembly_end_cond):
                        if(abs(assembly.obj_x.location.x) > abs(assembly.obj_y.location.y)):
                            edge_2 = "L1"
                            edge_3 = "S2"
                            edge_4 = "L2"
                        else:
                            edge_2 = "S1"
                            edge_3 = "L2"
                            edge_4 = "S2"
                        edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                        edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                        edge_4_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                    elif(l_assembly_end_cond and r_assembly_end_cond == False):
                        if(abs(assembly.obj_x.location.x) > abs(assembly.obj_y.location.y)):
                            edge_1 = "S1"
                            edge_2 = "L1"
                            edge_4 = "L2"
                        else:
                            edge_1 = "L1"
                            edge_2 = "S1"
                            edge_4 = "S2"
                        edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                        edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                        edge_4_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                    else:
                        if(abs(assembly.obj_x.location.x) > abs(assembly.obj_y.location.y)):
                            edge_2 = "L1"
                            edge_4 = "L2"
                        else:
                            edge_2 = "S1"
                            edge_4 = "S2"
                        edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                        edge_4_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                else:
                    if(abs(assembly.obj_x.location.x) > abs(assembly.obj_y.location.y)):
                        edge_2 = "L1"
                    else:
                        edge_2 = "S1"
                    
                    carcass_bp = sn_utils.get_closet_bp(obj)
                    carcass_assembly = sn_types.Assembly(carcass_bp)
                    parent_assembly = sn_types.Assembly(assembly.obj_bp.parent)
                    Countertop_Type = parent_assembly.get_prompt("Countertop Type")

                    # If countertop is not Melamine, do not add edgebanding
                    if Countertop_Type and Countertop_Type.get_value() == 0:
                        edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)

                    if Countertop_Type and Countertop_Type.get_value() != 1 or Countertop_Type.get_value() != 2:
                        l_carcass_end_cond_prompt = carcass_assembly.get_prompt("Left End Condition")
                        r_carcass_end_cond_prompt = carcass_assembly.get_prompt("Right End Condition")
                        l_carcass_end_cond = ''
                        r_carcass_end_cond = ''
                        if l_carcass_end_cond_prompt and r_carcass_end_cond_prompt:
                            l_carcass_end_cond = l_carcass_end_cond_prompt.get_value()
                            r_carcass_end_cond = r_carcass_end_cond_prompt.get_value()
                        l_assembly_end_cond_prompt = assembly.get_prompt("Exposed Left")
                        r_assembly_end_cond_prompt = assembly.get_prompt("Exposed Right")
                        b_assembly_end_cond_prompt = assembly.get_prompt("Exposed Back")
                        l_assembly_end_cond = ''
                        r_assembly_end_cond = ''
                        b_assembly_end_cond = ''
                        if l_assembly_end_cond_prompt and r_assembly_end_cond_prompt and b_assembly_end_cond_prompt:
                            l_assembly_end_cond = l_assembly_end_cond_prompt.get_value()
                            r_assembly_end_cond = r_assembly_end_cond_prompt.get_value()
                            b_assembly_end_cond = b_assembly_end_cond_prompt.get_value()

                        if (l_carcass_end_cond == 0 and r_carcass_end_cond != 0) or (l_assembly_end_cond == True and r_assembly_end_cond != True):
                            if(abs(assembly.obj_x.location.x) > abs(assembly.obj_y.location.y)):
                                edge_1 = "S1"
                            else:
                                edge_1 = "L1"
                            edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)                  

                        if (l_carcass_end_cond != 0 and r_carcass_end_cond == 0) or (l_assembly_end_cond != True and r_assembly_end_cond == True):
                            if(abs(assembly.obj_x.location.x) > abs(assembly.obj_y.location.y)):
                                edge_3 = "S2"
                            else:
                                edge_3 = "L2"
                            edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)

                        if (l_carcass_end_cond == 0 and r_carcass_end_cond == 0) or (l_assembly_end_cond == True and r_assembly_end_cond == True):
                            if(abs(assembly.obj_x.location.x) > abs(assembly.obj_y.location.y)):
                                edge_1 = "S1"
                                edge_3 = "S2"
                            else:
                                edge_1 = "L1"
                                edge_3 = "L2"
                            edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                            edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                        
                        if b_assembly_end_cond:
                            if(abs(assembly.obj_x.location.x) > abs(assembly.obj_y.location.y)):
                                edge_4 = "L2"
                            else:
                                edge_4 = "S2"
                            edge_4_sku = closet_materials.get_edge_sku(obj, assembly, part_name)

            if obj_props.is_back_bp:
                if(obj.parent.parent and obj.parent.parent.sn_closets.is_island):
                    island_assembly = sn_types.Assembly(obj.parent.parent)
                    l_assembly_end_cond_prompt = assembly.get_prompt("Exposed Left")
                    r_assembly_end_cond_prompt = assembly.get_prompt("Exposed Right")
                    l_assembly_end_cond = ''
                    r_assembly_end_cond = ''
                    if l_assembly_end_cond_prompt and r_assembly_end_cond and b_assembly_end_cond:
                        l_assembly_end_cond = l_assembly_end_cond_prompt.get_value()
                        r_assembly_end_cond = r_assembly_end_cond_prompt.get_value()
                    is_double = island_assembly.get_prompt("Depth 2")
                    if(is_double == None):
                        if(l_assembly_end_cond == False and r_assembly_end_cond == False):
                            if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                                edge_2 = "S1"
                                edge_4 = "S2"
                            else:
                                edge_2 = "L1"
                                edge_4 = "L2"
                            edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                            edge_4_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                        elif(l_assembly_end_cond == False and r_assembly_end_cond ):
                            if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                                edge_2 = "S1"
                            else:
                                edge_2 = "L1"
                            edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                        elif(l_assembly_end_cond and r_assembly_end_cond == False):
                            if(abs(assembly.obj_x.location.x)>abs(assembly.obj_y.location.y)):
                                edge_2 = "S1"
                            else:
                                edge_2 = "L1"
                            edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
        
            #Toe Kick
            if obj_props.is_toe_kick_end_cap_bp:
                parent_assembly = sn_types.Assembly(obj.parent.parent)
                has_tk_skin = parent_assembly.get_prompt("Add TK Skin")
                if has_tk_skin:
                    if not has_tk_skin.get_value():
                        # If the Toe Kick is Attached to an Island
                        if(obj.parent.parent and obj.parent.parent.sn_closets.is_island):
                            if(abs(assembly.obj_x.location.x)<abs(assembly.obj_y.location.y)):
                                edge_1 = "S1"
                                edge_3 = "S2"
                            else:
                                edge_1 = "L1"
                                edge_3 = "L2"
                            edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                            edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                        else:                          
                            if(abs(assembly.obj_x.location.x)<abs(assembly.obj_y.location.y)):
                                edge_1 = "S1"
                            else:
                                edge_1 = "L1"
                            edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)

            #Flat Crown
            if "IS_BP_FLAT_CROWN" in assembly.obj_bp:
                EL = assembly.get_prompt("Exposed Left").get_value()
                ER = assembly.get_prompt("Exposed Right").get_value()
                EB = assembly.get_prompt("Exposed Back").get_value()
                edge_2 = "L1"
                edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                if((EL and ER) and assembly.obj_y.location.y < sn_unit.inch(96)):
                    edge_1 = "S1"
                    edge_3 = "S2"
                    edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                    edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                    if(EB):
                        edge_4 = "L2"
                        edge_4_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                else:
                    if(len(self.single_exposed_flat_crown) > 0 ):
                        if(self.single_exposed_flat_crown[0]):
                            edge_1 = "S1"
                            edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                            self.single_exposed_flat_crown.pop()
                    if(len(self.top_edgebanded_flat_crown) > 0 ):
                        if(self.top_edgebanded_flat_crown[0]):
                            edge_4 = "L2"
                            edge_4_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                            self.top_edgebanded_flat_crown.pop()

            len_x = self.get_part_length(assembly)
            len_y = self.get_part_width(assembly)

            if obj_props.is_hamper_front_bp:
                len_x = self.get_part_width(assembly)
                len_y = self.get_part_length(assembly)          

            
            #Create and add label
            lbl = [
                ("IDL-{}".format(self.label_count), "IDJ-{}".format(self.job_count), "IDP-{}".format(self.part_count)),                
                ("dcname", "text", part_name),
                ("name", "text", part_name),
                ("wallname", "text", 'Island' if sn_utils.get_closet_bp(obj).get("IS_BP_ISLAND") else sn_utils.get_wall_bp(obj).snap.name_object),
                ("variablesection", "text", str(self.is_variable_section(assembly))),
                ("x", "text", self.get_part_x_location(assembly.obj_bp,assembly.obj_bp.location.x)),
                ("y", "text", self.get_part_y_location(assembly.obj_bp,assembly.obj_bp.location.y)),
                ("z", "text", self.get_part_z_location(assembly.obj_bp,assembly.obj_bp.location.z)),
                ("lenx", "text", len_x),
                ("leny", "text", len_y),
                ("lenz", "text", self.distance(sn_utils.get_part_thickness(obj))),
                ("rotx", "text", str(int(math.degrees(assembly.obj_bp.rotation_euler.x)))),
                ("roty", "text", str(int(math.degrees(assembly.obj_bp.rotation_euler.x)))),
                ("rotz", "text", str(int(math.degrees(assembly.obj_bp.rotation_euler.x)))),
                ("boml", "text", self.get_part_length(assembly)),
                ("bomt", "text",  self.distance(sn_utils.get_part_thickness(obj))),
                ("bomw", "text", self.get_part_width(assembly)),
                ("catnum", "text", self.get_part_category_number(assembly, assembly.obj_bp, mat_sku, part_name)),#Part Comments2
            ]
            # Ken Needs anything new added to the label section to be added before SKU
            door_style = ""
            glass_color = closet_materials.get_glass_color().name
            glaze_color = closet_materials.get_glaze_color().name
            glaze_style = closet_materials.get_glaze_style().name
            has_center_rail = "No"
            center_rail_distance_from_center = 0
            if(obj_props.is_door_bp or obj_props.is_drawer_front_bp or obj_props.is_hamper_front_bp or obj.get('IS_DOOR') or obj.get('IS_BP_DRAWER_FRONT') or obj_props.is_glass_shelf_bp):     
                if(assembly.get_prompt("Door Style")):
                    door_style = assembly.get_prompt("Door Style").get_value()
                    parent_assembly = sn_types.Assembly(obj.parent.parent)
                    has_center_rail_ppt = parent_assembly.get_prompt("Has Center Rail")
                    center_rail_distance_from_center_ppt = parent_assembly.get_prompt("Center Rail Distance From Center")                
                    prompts = [has_center_rail_ppt,center_rail_distance_from_center_ppt]
                    if all(prompts) and (has_center_rail_ppt.get_value()):
                        has_center_rail = "Yes"
                        center_rail_distance_from_center = sn_unit.meter_to_inch(center_rail_distance_from_center_ppt.get_value())
                door_lbl = [
                    ("style", "text", door_style if door_style != '' else 'None'),
                    ("glazecolor", "text", glaze_color if door_style != '' else 'None'),
                    ("glazestyle", "text", glaze_style if door_style != '' else 'None'),
                    ("glasscolor", "text", glass_color if glass_color != '' else 'None'),
                    ("has_center_rail", "text", has_center_rail),
                    ("center_rail_distance_from_center", "text", str(center_rail_distance_from_center) if has_center_rail == "Yes" else 'None'),
                ]
                lbl.extend(door_lbl)
            
            second_lbl = [
                ("sku", "text", mat_sku),
                ("cncmirror", "text", ""),#Str literal OKAY
                ("cncrotation", "text", "180"),#Str literal OKAY
                ("cutl", "text", self.get_part_length(assembly)),#Part.AdjustedCutPartLength 
                ("cutt", "text", self.distance(sn_utils.get_part_thickness(obj))),
                ("cutw", "text", self.get_part_width(assembly)),#Part.AdjustedCutPartWidth
                ("primaryedgecolorname", "text", primary_edge_color_name if edge_1 != '' or edge_2 != '' or edge_3 != '' or edge_4 != '' else ''),
                ("edgeband1", "text", edge_1),
                ("edgeband1sku", "text", edge_1_sku),
                ("edgeband1name", "text", edge_1_color_name if edge_1 != '' else ''),
                ("edgeband2", "text", edge_2),
                ("edgeband2sku", "text", edge_2_sku),
                ("edgeband2name", "text", edge_2_color_name if edge_2 != '' else ''),
                ("edgeband3", "text", edge_3),
                ("edgeband3sku", "text", edge_3_sku),
                ("edgeband3name", "text", edge_3_color_name if edge_3 != '' else ''),
                ("edgeband4", "text", edge_4),
                ("edgeband4sku", "text", edge_4_sku),
                ("edgeband4name", "text", edge_4_color_name if edge_4 != '' else '')
            ]  
            lbl.extend(second_lbl)

            self.labels.append(lbl)
            self.label_count += 1

            #Create and add OperationGroup
            #Get info for segments
            X = self.get_part_length(assembly)
            Y = self.get_part_width(assembly)
            Z = self.distance(sn_utils.get_part_thickness(obj))
            W = 0

            if obj_props.is_hamper_front_bp:
                X = self.get_part_width(assembly)
                Y = self.get_part_length(assembly)

            upper_right = (X, Y, Z, W)
            upper_left = (0, Y, Z, W)
            lower_left = (0, 0, Z, W)
            lower_right = (X, 0, Z, W)

            drilling = self.get_drilling(assembly)

            op_grp = [
                ("IDOP-{}".format(self.op_count), "IDMOR-{}".format(self.or_count)),
                upper_right,#Segment 1
                upper_left,#Segment 2
                lower_left,#Segment 3
                lower_right,#Segment 4
                drilling
            ]

            #Create and operation group for every part
            self.op_groups.append(op_grp)
            self.op_count += 1

            if self.debugger:
                self.debugger.write_debug_part(self, assembly, obj, op_grp, lbl, self.part_count)

            self.part_count += 1
    
    def write_material(self,mat_name,mat_sku):
        elm_job = self.xml.tree.findall("Job")[0]
        existing_mats = elm_job.findall("Material")
        mat_exists = self.material_node_exists(mat_sku)

        if not mat_exists:
            mat_id = self.mat_count

            if existing_mats:
                idx = list(elm_job).index(existing_mats[-1]) + 1
                elm_material = self.xml.insert_element(idx, elm_job, 'Material', {'ID': "IDM-{}".format(mat_id)})

            else:
                elm_material = self.xml.add_element(elm_job, 'Material', {'ID': "IDM-{}".format(mat_id)})

            self.xml.add_element_with_text(elm_material, 'Name', mat_name)
            if (mat_sku != None) and ('MD' in mat_sku):
                self.xml.add_element_with_text(elm_material, 'Type', "milled_lumber")
            else:
                self.xml.add_element_with_text(elm_material, 'Type', "sheet")
            self.xml.add_element_with_text(elm_material, 'SKU', mat_sku)

            self.mat_count += 1
        
        else:
            mat_id = self.get_mat_id(mat_sku) 

        return mat_id

    def get_mat_id(self,sku):
        elm_job = self.xml.tree.findall("Job")[0]
        existing_mats = elm_job.findall("Material")

        for mat in existing_mats:
            if mat.find("SKU").text == sku:
                mat_id = mat.attrib['ID']
                mat_id_num = mat_id.replace('IDM-',"")
        
        return mat_id_num

    def material_node_exists(self,sku):
        elm_job = self.xml.tree.findall("Job")[0]
        existing_mats = elm_job.findall("Material")
        mat_exists = False

        for mat in existing_mats:
            if mat.find("SKU").text == sku:
                mat_exists = True

        return mat_exists

    def write_edgebanding(self,project_node):
        elm_edgebanding = self.xml.add_element(project_node,"Edgebanding")
        for edgeband in self.edgeband_materials:
            elm_edge = self.xml.add_element(elm_edgebanding,'Edgeband',edgeband)
            self.xml.add_element_with_text(elm_edge,'Type',"3")
            self.xml.add_element_with_text(elm_edge,'Thickness',str(self.edgeband_materials[edgeband]))

    def write_buyout_materials(self,project_node):
        elm_buyouts = self.xml.add_element(project_node,"Buyouts")
        for buyout in self.buyout_materials:
            buyout_name = buyout if buyout != "" else "Unnamed"
            self.xml.add_element(elm_buyouts,'Buyout',buyout_name)
    
    def write_solid_stock_material(self,project_node):
        elm_solid_stocks = self.xml.add_element(project_node,"SolidStocks")
        for solid_stock in self.solid_stock_materials:
            solid_stock_name = solid_stock if solid_stock != "" else "Unnamed"
            elm_solid_stock = self.xml.add_element(elm_solid_stocks,'SolidStock',solid_stock_name)
            self.xml.add_element_with_text(elm_solid_stock,'Thickness',str(sn_unit.meter_to_active_unit(self.solid_stock_materials[solid_stock])))
        
    def write_spec_groups(self,project_node):
        #Currently not being used but we might need to export spec groups at some point
        elm_spec_groups = self.xml.add_element(project_node,"SpecGroups")
        
        for spec_group in bpy.context.scene.snap.spec_groups:
            spec_group_name = spec_group.name if spec_group.name != "" else "Unnamed"
            elm_spec_group = self.xml.add_element(elm_spec_groups,'SpecGroup',spec_group_name)
            elm_cutparts = self.xml.add_element(elm_spec_group,'CutParts')
            for cutpart in spec_group.cutparts:
                elm_cutpart_name = cutpart.mv_pointer_name if cutpart.mv_pointer_name != "" else "Unnamed"
                elm_cutpart = self.xml.add_element(elm_cutparts,'PointerName',elm_cutpart_name)
                mat_name = sn_utils.get_material_name_from_pointer(cutpart,spec_group)
                material_name = mat_name if mat_name != "" else "Unnamed"
                self.xml.add_element_with_text(elm_cutpart,'MaterialName',material_name)
                 
            elm_edgeparts = self.xml.add_element(elm_spec_group,'EdgeParts')
            for edgepart in spec_group.edgeparts:
                elm_edgepart_name = edgepart.mv_pointer_name if edgepart.mv_pointer_name != "" else "Unnamed"
                elm_edgepart = self.xml.add_element(elm_edgeparts,'PointerName',elm_edgepart_name)
                mat_name = sn_utils.get_edgebanding_name_from_pointer_name(edgepart.name,spec_group)
                edge_material_name = mat_name if mat_name != "" else "Unnamed"
                self.xml.add_element_with_text(elm_edgepart,'MaterialName',edge_material_name)

    def write_job_info(self, elm_job):
        dirname = os.path.dirname(bpy.data.filepath).split("\\")[-1]
        filname = "{}.ccp".format(dirname)
        tree = ET.parse(os.path.join(os.path.dirname(bpy.data.filepath), ".snap", filname))
        root = tree.getroot()
        elm_pinfo = root.find("ProjectInfo")
        elm_rooms = root.find("Rooms")
        rooms = list(elm_rooms)

        wm = bpy.context.window_manager.sn_project
        project_name = wm.current_file_project
        customer_name = elm_pinfo.find("customer_name").text
        client_id = elm_pinfo.find("client_id").text
        proj_address = elm_pinfo.find("project_address").text
        city = elm_pinfo.find("city").text
        state = elm_pinfo.find("state").text
        zip_code = elm_pinfo.find("zip_code").text
        cphone_1 = elm_pinfo.find("customer_phone_1").text
        cphone_2 = elm_pinfo.find("customer_phone_2").text
        c_email = elm_pinfo.find("customer_email").text
        proj_notes = elm_pinfo.find("project_notes").text
        designer = elm_pinfo.find("designer").text
        total_room_count = str(len(rooms))
        design_date = elm_pinfo.find("design_date").text

        info = [('projectname', project_name),
                ('jobnumber', self.job_number),
                ('customername', customer_name),
                ('clientid', client_id),
                ('projectaddress', proj_address),
                ('city', city),
                ('state', state),
                ('zipcode', zip_code),
                ('customerphone1', cphone_1),
                ('customerphone2', cphone_2),
                ('customeremail', c_email),
                ('projectnotes', proj_notes),
                ('designer', designer),
                ('totalroomcount', total_room_count),
                ('designdate', design_date)
        ]

        for f in info:
            elm_var = self.xml.add_element(elm_job, 'Var')
            self.xml.add_element_with_text(elm_var, 'Name', f[0])
            self.xml.add_element_with_text(elm_var, 'Value', f[1])

    def write_manufacturing_info(self, context, project_node, create_mfg_node=False):
        if create_mfg_node:
            elm_mfg = self.xml.add_element(project_node, 'Manufacturing', {'ID': "IDMFG-{}".format(self.or_count)})
            elm_or = self.xml.add_element(elm_mfg, 'Orientation', {'ID': "IDMOR-{}".format(self.or_count)})
        else:
            elm_mfg = self.xml.root.find("Manufacturing")

            #Get index of last existing orientation
            existing_or = elm_mfg.findall("Orientation")
            idx = list(elm_mfg).index(existing_or[-1]) + 1           
            elm_or = self.xml.insert_element(idx, elm_mfg, 'Orientation', {'ID': "IDMOR-{}".format(self.or_count)})            

        #Write Orientation TODO determine mirror_x and rotation angle
        self.xml.add_element_with_text(elm_or, "Mirror", "none")#TODO determine mirror_x or none
        self.xml.add_element_with_text(elm_or, "Rotation", "0")#TODO determine rotation angle

        self.write_operation_groups(elm_mfg)
        self.write_labels(elm_mfg)

    def update_mfg_node(self):
        """Resets manufacturing node position above materials if needed
        """
        job_node = self.xml.tree.findall("Job")[0]
        mfg_node = job_node.find("Manufacturing")
        mat_nodes = job_node.findall("Material")

        if len(mat_nodes) < 1:
            return
        else:
            mat_node_1 = mat_nodes[0]
            mat_node_pos = list(job_node).index(mat_node_1)
            mfg_node_position = list(job_node).index(mfg_node)

            if mat_node_pos < mfg_node_position:
                job_node.remove(mfg_node)
                job_node.insert(mat_node_pos, mfg_node)

    def write_operation_groups(self, elm_mfg):
        for op_grp in self.op_groups:

            #Get index of last existing opgrp
            existing_or = elm_mfg.findall("OperationGroups")

            if existing_or:
                idx = list(elm_mfg).index(existing_or[-1]) + 1           
                elm_op = self.xml.insert_element(idx, 
                                                elm_mfg,
                                                'OperationGroups',
                                                {'ID': op_grp[0][0],
                                                'MfgOrientationID': op_grp[0][1]#ToDo: create counter for mfg_orientation and match up
                                                })             

            else:
                elm_op = self.xml.add_element(elm_mfg,
                                             'OperationGroups',
                                             {'ID': op_grp[0][0],
                                             'MfgOrientationID': op_grp[0][1]#ToDo: create counter for mfg_orientation and match up
                                             })

            segment_coords = [op_grp[1], op_grp[2], op_grp[3], op_grp[4]]
            
            #Segments
            self.add_panel_segment(elm_op, segment_coords)

            #Circles
            circles = op_grp[5]

            if len(circles) > 0:
                for circle in circles:
                    self.add_panel_circle(elm_op, circle)

    def add_panel_circle(self, elm_parent, circle):
        cen_x = circle['cen_x']
        cen_y = circle['cen_y']
        cen_z = circle['cen_z']
        diameter = circle['diameter']
        normal_z = circle['normal_z']
        org_displacement = circle['org_displacement']

        self.xml.add_element_with_text(elm_parent, "Type", "drilled_hole")
        elm_circle = self.xml.add_element(elm_parent, "Circle")

        self.xml.add_element(
            elm_circle,
            "Center",
            {
                'x': str(cen_x),
                'y': str(cen_y),
                'z': "-{}".format(str(round(cen_z,2)))
            }
        )

        self.xml.add_element_with_text(elm_circle, "Diameter", str(diameter))

        self.xml.add_element(
            elm_circle,
            "Normal",
            {
                'x': "0",
                'y': "0",
                'z': str(normal_z)
            }
        )     

        self.xml.add_element_with_text(elm_circle, "OrgDisplacement", str(org_displacement))
        self.xml.add_element_with_text(elm_parent, "Comment", "")      

    def add_panel_segment(self, elm_parent, coords):
        self.xml.add_element_with_text(elm_parent, "Type", "panel")#Str literal okay

        for idx, i in enumerate(coords):
            if idx != len(coords) - 1:
                next_coord = coords[idx + 1]

            elif idx == len(coords) - 1:
                next_coord = coords[0]

            elm_seg = self.xml.add_element(elm_parent, 'Segment')

            self.xml.add_element(elm_seg, 'StartCoor', {'x': str(i[0]),#X
                                                        'y': str(i[1]),#Y
                                                        'z': '-{}'.format(str(i[2])),#Z
                                                        'w': "0"})#Appears to be 0, MM uses Vector.Bulge

            self.xml.add_element(elm_seg, 'StartNormal', {'x': "0",#Str literal OKAY
                                                          'y': "0",#Str literal OKAY
                                                          'z': "1"})#Str literal OKAY

            self.xml.add_element_with_text(elm_seg, 'StartOrgDisplacement', "0")#Str literal OKAY

            self.xml.add_element(elm_seg, 'EndCoor', {'x': str(next_coord[0]),#Next coordinate X
                                                      'y': str(next_coord[1]),#Next coordinate Y
                                                      'z': '-{}'.format(str(next_coord[2])),#Next coordinate Z
                                                      'w': "0"})#Str literal OKAY

            self.xml.add_element(elm_seg, 'EndNormal', {'x': "0",#Str literal OKAY
                                                        'y': "0",#Str literal OKAY
                                                        'z': "1"})#Str literal OKAY

            self.xml.add_element_with_text(elm_seg, 'EndOrgDisplacement', "0")#Str literal OKAY

    def write_labels(self, elm_mfg):
        for lbl in self.labels:
            elm_label = self.xml.add_element(elm_mfg,
                                            'Label',
                                            {'ID': lbl[0][0],
                                            'JobID': lbl[0][1],
                                            'PartID': lbl[0][2]})

            for idx, item in enumerate(lbl):
                if idx > 0:
                    self.add_label_item(elm_label, item)

    def add_label_item(self, lbl_node, item):
        self.xml.add_element_with_text(lbl_node, "Name", item[0])
        self.xml.add_element_with_text(lbl_node, "Type", item[1])
        self.xml.add_element_with_text(lbl_node, "Value", item[2])

    def execute(self, context):
        bpy.ops.sn_closets.update_drawer_boxes(add=True)
        debug_mode = context.preferences.addons["snap"].preferences.debug_mode
        debug_machining = context.preferences.addons["snap"].preferences.debug_mac
        self.debug_mode = debug_mode

        if debug_mode and debug_machining:
            self.debugger = debug_xml_export.Debug()

        self.clear_and_collect_data(context)

        #Replaces project name (filname)
        job_id = "IDJ-{}".format(self.job_count)
        self.set_job_number()

        job_name = self.job_number
        job_source = "SNaP"

        proj_props = bpy.context.window_manager.sn_project
        path = os.path.join(self.xml_path, sn_xml.Snap_XML.filename)

        self.xml = sn_xml.Snap_XML(path=path)

        #If XML does not already exist do initial setup, 
        if not os.path.exists(path):
            #Add job            
            elm_job = self.xml.add_element(self.xml.root, 'Job', {'ID':job_id, })
            self.xml.add_element_with_text(elm_job, 'Name', job_name)
            self.xml.add_element_with_text(elm_job, 'Source', job_source)
            elm_unit = self.xml.add_element(elm_job, 'Unit')
            self.xml.add_element_with_text(elm_unit, 'Name', 'dimension')
            self.xml.add_element_with_text(elm_unit, 'Measure', 'inch')            

            #Write Item
            self.write_products(elm_job)
            self.write_manufacturing_info(context, elm_job, create_mfg_node=True)
            self.write_job_info(elm_job)
            self.update_mfg_node()

        #If XML already exists, set counts
        else:
            self.xml.set_counts()
            self.item_count = self.xml.item_count
            self.assembly_count = self.xml.assembly_count
            self.part_count = self.xml.part_count
            self.label_count = self.xml.label_count
            self.mat_count = self.xml.mat_count
            self.op_count = self.xml.op_count
            self.or_count = self.xml.or_count       

            #Write item
            self.write_products(self.xml.root)
            self.write_manufacturing_info(context, self.xml.root)

        #self.write_edgebanding(elm_project)
        #self.write_buyout_materials(elm_project)
        #self.write_solid_stock_material(elm_project)

        self.xml.write(self.xml_path)

        if self.debugger:
            self.debugger.create_drilling_preview()

        return {'FINISHED'}


def register():
    bpy.utils.register_class(OPS_Export_XML)


def unregister():
    bpy.utils.unregister_class(OPS_Export_XML)    
    
