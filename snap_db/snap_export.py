bl_info = {
    "name": "SNaP Import-Export",
    "author": "Ryan Montes",
    "version": (1, 0, 0),
    "blender": (2, 7, 8),
    "location": "Tools Shelf",
    "description": "SNaP Import-Export",
    "warning": "",
    "wiki_url": "",
    "category": "SNaP"
}

import bpy
import math
import os
from mv import unit, utils, fd_types
from bpy.types import Operator
import xml.etree.ElementTree as ET
import csv
import sqlite3
from sqlite3 import Error
from . import snap_xml
from . import debug_xml_export
import snap_db
from pprint import pprint


BL_DIR = os.path.dirname(bpy.app.binary_path)
CSV_PATH = os.path.join(BL_DIR, "data", "CCItems.csv")
DIR_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', "snap_db")
ITEMS_TABLE_NAME = "CCItems"
DEBUG_MODE = True


def get_slide_size(slide_type, assembly):
    closet_props = assembly.obj_bp.lm_closets

    if closet_props.is_drawer_box_bp:
        drawer_depth = unit.meter_to_inch(assembly.obj_y.location.y)

    if closet_props.is_drawer_side_bp:
        drawer_box_assembly = fd_types.Assembly(assembly.obj_bp.parent)
        drawer_depth = unit.meter_to_inch(drawer_box_assembly.obj_y.location.y)

    mat_props = bpy.context.scene.db_materials
    sizes = []
    slide_type = mat_props.get_drawer_slide_type()

    for size in slide_type.sizes:
        sizes.append(size)

    sizes.reverse()

    for size in sizes:
        if drawer_depth >= float(size.slide_length_inch):
            return size

def get_hardware_sku(obj_bp, assembly, item_name):
    conn = snap_db.connect_db()
    cursor = conn.cursor()
    sku = "Unknown"
    #print(obj_bp, assembly.obj_bp, item_name)

    #Pull
    if assembly.obj_bp.lm_closets.is_handle:
        pull_cat = bpy.context.scene.lm_closets.closet_options.pull_category
        pull_name = bpy.context.scene.lm_closets.closet_options.pull_name
        vendor_id = item_name[:10] # use vendor code in item name for lookup (123.45.678)

        cursor.execute(
            "SELECT\
                sku\
            FROM\
                CCItems\
            WHERE\
                ProductType == 'AC' AND\
                VendorItemNum ='{}'\
            ;".format(vendor_id)
        )

        rows = cursor.fetchall()

        for row in rows:
            sku = row[0]
            #print("FOUND PULL SKU: ", sku)            
        
        conn.close()

        return sku

    #Hinge
    if obj_bp.lm_closets.is_hinge:
        hinge_name = bpy.context.scene.lm_closets.closet_options.hinge_name

        cursor.execute(
            "SELECT\
                sku\
            FROM\
                CCItems\
            WHERE\
                ProductType == 'HW' AND\
                Name LIKE'{}'\
            ;".format("%" + hinge_name + "%")
        )

        rows = cursor.fetchall()

        for row in rows:
            sku = row[0]
            #print("FOUND HINGE SKU: ", sku)            
        
        conn.close()

        return sku

    #Hinge Plate
    if "Mounting Plate" in item_name:
        cursor.execute(
            "SELECT\
                sku\
            FROM\
                CCItems\
            WHERE\
                ProductType == 'HW' AND\
                Name LIKE'{}'\
            ;".format("%" + item_name + "%")
        )

        rows = cursor.fetchall()

        for row in rows:
            sku = row[0]
            #print("FOUND MOUNTING PLATE SKU: ", sku)            
        
        conn.close()

        return sku        
    

    #Slide
    if "Drawer Slide" in item_name:
        mat_props = bpy.context.scene.db_materials
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
                CCItems\
            WHERE\
                ProductType == 'HW' AND\
                Name LIKE '{}' AND\
                Name LIKE '{}'\
            ;".format(
                "%" + slide_name + "%",
                "%" + str(slide_len) + "in%",
            )
        )    

        rows = cursor.fetchall()

        for row in rows:
            sku = row[0]
            #print("FOUND SLIDE SKU: ", sku)            
        
        conn.close()

        return sku        

    #Hamper Basket
    if assembly.obj_bp.lm_closets.is_hamper_bp:
        mat_props = bpy.context.scene.db_materials
        hamper_insert_bp = assembly.obj_bp.parent
        basket_color = mat_props.wire_basket_colors
        basket_width = unit.meter_to_inch(assembly.obj_x.location.x)
        basket_depth = unit.meter_to_inch(assembly.obj_y.location.y)

        #'547.42.231',#Chrome 18x14
        #'547.42.232',#Chrome 24x14
        #'547.42.241',#Chrome 18x16
        #'547.42.242',#Chrome 24x16
        #'547.42.731',#White 18x14
        #'547.42.732',#White 24x14
        #'547.42.741',#White 18x16
        #'547.42.742',#White 24x16

        color_id = 2 if basket_color == 'CHROME' else 7
        width_id = 1 if basket_width == 18.0 else 2
        depth_id = 3 if basket_depth == 14.0 else 4
        vendor_id = '547.42.{}{}{}'.format(color_id,depth_id,width_id)

        cursor.execute(
            "SELECT\
            sku\
            FROM\
                CCItems\
            WHERE\
                ProductType == 'AC' AND\
                VendorItemNum ='{}'\
            ;".format(vendor_id)
        )

        rows = cursor.fetchall()

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
                CCItems\
            WHERE\
                ProductType == 'AC' AND\
                Name LIKE'{}'\
            ;".format("%" + item_name + "%")
        )

        rows = cursor.fetchall()

        for row in rows:
            sku = row[0]
            #print("FOUND BRAKE FLAP SKU: ", sku)            
        
        conn.close()

        return sku

    #Hamper Rack
    if "Hamper Rack" in item_name:
        mat_props = bpy.context.scene.db_materials        
        basket_color = mat_props.wire_basket_colors

        if basket_color == 'CHROME':
            rack_name = "Hamper Rack Chrome"

        elif basket_color == 'WHITE':
            rack_name = "Hamper Rack White"

        cursor.execute(
            "SELECT\
                sku\
            FROM\
                CCItems\
            WHERE\
                ProductType == 'AC' AND\
                Name LIKE'{}'\
            ;".format("%" + rack_name + "%")
        )

        rows = cursor.fetchall()

        for row in rows:
            sku = row[0]
            #print("FOUND HAMPER RACK SKU: ", sku)            
        
        conn.close()

        return sku        

    #Hamper Laundry Bag
    if "Cloth Laundry Bag" in item_name:
        basket_width = unit.meter_to_inch(assembly.obj_x.location.x)

        if basket_width > 18.0:
            bag_name = item_name + " 24"
        else:
            bag_name = item_name + " 18"

        cursor.execute(
            "SELECT\
                sku\
            FROM\
                CCItems\
            WHERE\
                ProductType == 'AC' AND\
                Name LIKE'{}'\
            ;".format("%" + bag_name + "%")
        )

        rows = cursor.fetchall()

        for row in rows:
            sku = row[0]
            #print("FOUND LAUNDRY BAG SKU: ", sku)            
        
        conn.close()

        return sku

    #Rod
    if assembly.obj_bp.lm_closets.is_hanging_rod:
        item_name = bpy.context.scene.lm_closets.closet_options.rods_name
        vendor_id = item_name[-10:]

        cursor.execute(
            "SELECT\
            sku\
            FROM\
                CCItems\
            WHERE\
                ProductType == 'AC' AND\
                VendorItemNum ='{}'\
            ;".format(vendor_id)
        )

        rows = cursor.fetchall()

        for row in rows:
            sku = row[0]
            #print("FOUND HANGING ROD SKU: ", sku)            
        
        conn.close()

        return sku

    #Rod Cup
    if "Pole Cup" in item_name:
        sku = bpy.context.scene.lm_closets.closet_options.pole_cup_name

        #print("FOUND POLE CUP SKU:", sku)

        return sku    

    #KD Fitting
    if "KD Fitting" in item_name:
        mat_props = bpy.context.scene.db_materials
        sku = mat_props.kd_fitting_color
        #print("FOUND KD FITTING SKU:", sku)

        return sku

    #Pegs
    if "Peg Chrome" in item_name:
        cursor.execute(
            "SELECT\
                sku\
            FROM\
                CCItems\
            WHERE\
                ProductType == 'HW' AND\
                Name LIKE'{}'\
            ;".format("%peg%chrome%")
        )

        rows = cursor.fetchall()

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
                CCItems\
            WHERE\
                ProductType == 'AC' AND\
                VendorItemNum =='{}'\
            ;".format("C8055-14A")
        )

        rows = cursor.fetchall()

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
                CCItems\
            WHERE\
                ProductType == 'AC' AND\
                VendorItemNum =='{}'\
            ;".format("C7004-2C")
        )

        rows = cursor.fetchall()

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
                CCItems\
            WHERE\
                ProductType == 'AC' AND\
                VendorItemNum =='{}'\
            ;".format("245.74.200")
        )

        rows = cursor.fetchall()

        for row in rows:
            sku = row[0]
            print("FOUND LATCH SKU:", sku)

        conn.close()

        return sku

    return sku

def get_export_prompts(obj_bp):
    """ Used in create_fluid_project_xml
        this collects all of the needed product prompts for the 121 product match
    """
    
    prompts = {}
    
    def add_prompt(prompt):
        if prompt.Type == 'NUMBER':
            prompts[prompt.name] = str(prompt.NumberValue)
        if prompt.Type == 'QUANTITY':
            prompts[prompt.name] = str(prompt.QuantityValue)
        if prompt.Type == 'COMBOBOX':
            prompts[prompt.name] = str(prompt.COL_EnumItem[prompt.EnumIndex].name)
        if prompt.Type == 'CHECKBOX':
            prompts[prompt.name] = str(prompt.CheckBoxValue)
        if prompt.Type == 'TEXT':
            prompts[prompt.name] = str(prompt.TextValue)
        if prompt.Type == 'DISTANCE':
            prompts[prompt.name] = str(round(unit.meter_to_active_unit(prompt.DistanceValue),4))
        if prompt.Type == 'ANGLE':
            prompts[prompt.name] = str(prompt.AngleValue)
        if prompt.Type == 'PERCENTAGE':
            prompts[prompt.name] = str(prompt.PercentageValue)
        if prompt.Type == 'PRICE':
            prompts[prompt.name] = str(prompt.PriceValue)
    
    def add_child_prompts(obj):
        for child in obj.children:
            if child.mv.type == 'BPASSEMBLY':
                add_prompts(child)
            if len(child.children) > 0:
                add_child_prompts(child)
        
    def add_prompts(obj):
        for prompt in obj.mv.PromptPage.COL_Prompt:
            if prompt.export:
                add_prompt(prompt)
                
    add_prompts(obj_bp)
    add_child_prompts(obj_bp)

    return prompts


class OPS_Export_XML(Operator):
    bl_idname = "snap_db.export_xml"
    bl_label = "Export XML File"
    bl_description = "This will export an XML file. The file must be saved first."
    
    walls = []
    products = []
    buyout_products = []
    
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
    xml_path = bpy.props.StringProperty(name="XML Path", subtype='DIR_PATH')

    @classmethod
    def poll(cls, context):
        if bpy.data.filepath != "":
            return True
        else:
            return False

    def distance(self,distance):
        return str(math.fabs(round(unit.meter_to_active_unit(distance),4)))
    
    def location(self,location):
        return str(round(unit.meter_to_active_unit(location),4))
    
    def angle(self,angle):
        return str(round(math.degrees(angle),4))
    
    def clear_and_collect_data(self,context):
        for product in self.products:
            self.products.remove(product)
        
        for wall in self.walls:
            self.walls.remove(wall)

        bpy.ops.fd_material.get_materials()

        for scene in bpy.data.scenes:
            if not scene.mv.plan_view_scene and not scene.mv.elevation_scene:
                for obj in scene.objects:
                    if not obj.mv.dont_export:
                        if obj.mv.type == 'BPWALL':
                            self.walls.append(obj)
                        if obj.mv.type == 'BPASSEMBLY':
                            if obj.mv.type_group == 'PRODUCT':
                                self.products.append(obj)

    def get_var_sec_length(self, x):
        increment = 3
        offset = unit.inch(0.5)
        max_len = 97

        for length in range(increment, max_len, increment):
            length = unit.inch(length)
            if x < length:
                if length - x <= offset:
                    return length + unit.inch(increment)
                else:
                    return length        

    def is_variable_section(self, assembly):
        opening_name = assembly.obj_bp.mv.opening_name

        if opening_name:
            carcass_bp = utils.get_parent_assembly_bp(assembly.obj_bp)
            carcass_assembly = fd_types.Assembly(carcass_bp)
            variable_section = carcass_assembly.get_prompt("CTF Opening {}".format(opening_name)).value()

            return variable_section

        else:
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
            qty += z_quantity.value() - 1
        
        if x_quantity:
            qty += x_quantity.value() - 1
            
        return str(qty)
        
    def get_part_width(self,assembly):
        width = math.fabs(assembly.obj_y.location.y)
        oversize_width = assembly.get_prompt("Oversize Width")
        if oversize_width:
            width += oversize_width.value()
        return self.distance(width)
    
    def get_part_length(self,assembly):
        length = math.fabs(assembly.obj_x.location.x)
        props = assembly.obj_bp.lm_closets

        if self.is_variable_section(assembly):
            if props.is_cleat_bp or props.is_shelf_bp:
                if not props.is_door_bp:
                    length = self.get_var_sec_length(length)
                    # length += oversize_length

        return self.distance(length)
        
    def get_part_x_location(self,obj,value):
        if obj.parent is None or obj.parent.mv.type_group == 'PRODUCT':
            return self.location(value)
        value += obj.parent.location.x
        return self.get_part_x_location(obj.parent,value)

    def get_part_y_location(self,obj,value):
        if obj.parent is None or obj.parent.mv.type_group == 'PRODUCT':
            return self.location(value)
        value += obj.parent.location.y
        return self.get_part_y_location(obj.parent,value)

    def get_part_z_location(self,obj,value):
        if obj.parent is None or obj.parent.mv.type_group == 'PRODUCT':
            return self.location(value)
        value += obj.parent.location.z
        return self.get_part_z_location(obj.parent,value)

    def get_part_comment(self,obj):
        if not obj.mv.comment_2 == "":
            return obj.mv.comment_2
        else:
            return ""

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
        if obj.mv.edgeband_material_name != "" and edge != "":
            thickness = utils.get_edgebanding_thickness_from_pointer_name(edge,spec_group)
            edge_mat_name = obj.mv.edgeband_material_name
            if edge_mat_name not in self.edgeband_materials and edge_mat_name != "":
                self.edgeband_materials[edge_mat_name] = thickness
            return edge_mat_name
        else:
            thickness = utils.get_edgebanding_thickness_from_pointer_name(edge,spec_group)
            edge_mat_name = utils.get_edgebanding_name_from_pointer_name(edge,spec_group)
            if edge_mat_name not in self.edgeband_materials and edge_mat_name != "":
                self.edgeband_materials[edge_mat_name] = thickness                
            return edge_mat_name
    
    def get_edgebanding_name_w1(self,obj,edge,spec_group):
        if obj.mv.edgeband_material_name_w1 != "" and edge != "":
            thickness = utils.get_edgebanding_thickness_from_pointer_name(edge,spec_group)
            edge_mat_name = obj.mv.edgeband_material_name_w1
            if edge_mat_name not in self.edgeband_materials and edge_mat_name != "":
                self.edgeband_materials[edge_mat_name] = thickness
            return edge_mat_name
        else:
            thickness = utils.get_edgebanding_thickness_from_pointer_name(edge,spec_group)
            edge_mat_name = utils.get_edgebanding_name_from_pointer_name(edge,spec_group)
            if edge_mat_name not in self.edgeband_materials and edge_mat_name != "":
                self.edgeband_materials[edge_mat_name] = thickness                
            return edge_mat_name    
    
    def get_edgebanding_name_w2(self,obj,edge,spec_group):
        if obj.mv.edgeband_material_name_w2 != "" and edge != "":
            thickness = utils.get_edgebanding_thickness_from_pointer_name(edge,spec_group)
            edge_mat_name = obj.mv.edgeband_material_name_w2
            if edge_mat_name not in self.edgeband_materials and edge_mat_name != "":
                self.edgeband_materials[edge_mat_name] = thickness
            return edge_mat_name
        else:
            thickness = utils.get_edgebanding_thickness_from_pointer_name(edge,spec_group)
            edge_mat_name = utils.get_edgebanding_name_from_pointer_name(edge,spec_group)
            if edge_mat_name not in self.edgeband_materials and edge_mat_name != "":
                self.edgeband_materials[edge_mat_name] = thickness                
            return edge_mat_name        
    
    def get_edgebanding_name_l1(self,obj,edge,spec_group):
        if obj.mv.edgeband_material_name_l1 != "" and edge != "":
            thickness = utils.get_edgebanding_thickness_from_pointer_name(edge,spec_group)
            edge_mat_name = obj.mv.edgeband_material_name_l1
            if edge_mat_name not in self.edgeband_materials and edge_mat_name != "":
                self.edgeband_materials[edge_mat_name] = thickness
            return edge_mat_name
        else:
            thickness = utils.get_edgebanding_thickness_from_pointer_name(edge,spec_group)
            edge_mat_name = utils.get_edgebanding_name_from_pointer_name(edge,spec_group)
            if edge_mat_name not in self.edgeband_materials and edge_mat_name != "":
                self.edgeband_materials[edge_mat_name] = thickness                
            return edge_mat_name          
    
    def get_edgebanding_name_l2(self,obj,edge,spec_group):
        if obj.mv.edgeband_material_name_l2 != "" and edge != "":
            thickness = utils.get_edgebanding_thickness_from_pointer_name(edge,spec_group)
            edge_mat_name = obj.mv.edgeband_material_name_l2
            if edge_mat_name not in self.edgeband_materials and edge_mat_name != "":
                self.edgeband_materials[edge_mat_name] = thickness
            return edge_mat_name
        else:
            thickness = utils.get_edgebanding_thickness_from_pointer_name(edge,spec_group)
            edge_mat_name = utils.get_edgebanding_name_from_pointer_name(edge,spec_group)
            if edge_mat_name not in self.edgeband_materials and edge_mat_name != "":
                self.edgeband_materials[edge_mat_name] = thickness                
            return edge_mat_name

    def set_job_number(self):
        dirname = os.path.dirname(bpy.data.filepath).split("\\")[-1]
        filname = "{}.ccp".format(dirname)
        tree = ET.parse(os.path.join(os.path.dirname(bpy.data.filepath), filname))
        root = tree.getroot()
        elm_pinfo = root.find("ProjectInfo")
        project_id = int(elm_pinfo.find("project_id").text)
        proj_user_prefs = bpy.context.user_preferences.addons["fd_projects"].preferences
        designer_id = proj_user_prefs.designer_id
        self.job_number = "{0:0=3d}.{1:0=4d}".format(designer_id, project_id)

    def write_oversize_top_shelf_part(self, node, obj, side=""):
        shelf_length_inch = 96
        closet_materials = bpy.context.scene.db_materials

        for child in obj.children:
            if child.cabinetlib.type_mesh == 'CUTPART':
                obj = child

        if obj.mv.type == 'BPASSEMBLY':
            assembly = fd_types.Assembly(obj)
        else:
            assembly = fd_types.Assembly(obj.parent)

        if assembly.obj_bp.mv.type_group != "PRODUCT":
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

            part_name = assembly.obj_bp.mv.name_object if assembly.obj_bp.mv.name_object != "" else assembly.obj_bp.name
            self.xml.add_element_with_text(elm_part, 'Name', part_name + " Shelf " + side)
            self.xml.add_element_with_text(elm_part,'Quantity', self.get_part_qty(assembly))
            self.xml.add_element_with_text(elm_part,'Width', self.get_part_width(assembly)) 
            self.xml.add_element_with_text(elm_part,'FinishedWidth', self.get_part_width(assembly))           
            self.xml.add_element_with_text(elm_part,'Length', self.distance(unit.inch(shelf_length_inch)))
            self.xml.add_element_with_text(elm_part,'FinishedLength', self.distance(unit.inch(shelf_length_inch)))
            self.xml.add_element_with_text(elm_part,'Thickness',self.distance(utils.get_part_thickness(obj)))
            self.xml.add_element_with_text(elm_part,'FinishedThickness', self.distance(utils.get_part_thickness(obj)))
            self.xml.add_element_with_text(elm_part,'Routing', "SK1")
            self.xml.add_element_with_text(elm_part,'Class', "make")
            self.xml.add_element_with_text(elm_part,'Type', "panel")

            elm_unit = self.xml.add_element(elm_part,'Unit')
            self.xml.add_element_with_text(elm_unit,'Name', "dimension")
            self.xml.add_element_with_text(elm_unit,'Measure', "inch")
            self.xml.add_element_with_text(elm_unit,'RoundFactor', "0")

            #Edgebanding
            carcass_bp = utils.get_parent_assembly_bp(obj)
            carcass_assembly = fd_types.Assembly(carcass_bp)
            l_end_cond = carcass_assembly.get_prompt("Left End Condition").value()
            r_end_cond = carcass_assembly.get_prompt("Right End Condition").value()

            edge_2 = ''
            edge_2_sku = ''

            edge_1 = 'EBF'
            edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)            

            if side == 'Left':
                if l_end_cond == 'EP':
                    edge_2 = 'EBL'
                    edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
            
            if side == 'Right':
                if r_end_cond == 'EP':
                    edge_2 = 'EBR'
                    edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)

            shelf_x_location = self.get_part_x_location(assembly.obj_bp,assembly.obj_bp.location.x)

            if side == "Right":
                shelf_x_location = str(float(shelf_x_location) + shelf_length_inch)                    

            #Create and add label
            lbl = [
                ("IDL-{}".format(self.label_count), "IDJ-{}".format(self.job_count), "IDP-{}".format(self.part_count)),                
                ("dcname", "text", part_name + " Shelf " + side),
                ("name", "text", part_name + " Shelf " + side),
                ("x", "text", shelf_x_location),
                ("y", "text", self.get_part_y_location(assembly.obj_bp,assembly.obj_bp.location.y)),
                ("z", "text", self.get_part_z_location(assembly.obj_bp,assembly.obj_bp.location.z)),
                ("lenx", "text", self.distance(unit.inch(shelf_length_inch))),
                ("leny", "text", self.get_part_width(assembly)),
                ("lenz", "text", self.distance(utils.get_part_thickness(obj))),
                ("rotx", "text", str(int(math.degrees(assembly.obj_bp.rotation_euler.x)))),
                ("roty", "text", str(int(math.degrees(assembly.obj_bp.rotation_euler.x)))),
                ("rotz", "text", str(int(math.degrees(assembly.obj_bp.rotation_euler.x)))),
                ("boml", "text", self.distance(unit.inch(shelf_length_inch))),
                ("bomt", "text",  self.distance(utils.get_part_thickness(obj))),
                ("bomw", "text", self.get_part_width(assembly)),
                ("catnum", "text", self.get_part_comment(assembly.obj_bp)),
                ("sku", "text", closet_materials.get_mat_sku(obj, assembly, part_name)),
                ("cncmirror", "text", ""),
                ("cncrotation", "text", "180"),
                ("cutl", "text", self.distance(unit.inch(shelf_length_inch))),
                ("cutt", "text", self.distance(utils.get_part_thickness(obj))),
                ("cutw", "text", self.get_part_width(assembly)),
                ("edge1name", "text", edge_1),
                ("edge1sku", "text", edge_1_sku),
                ("edge2name", "text", edge_2),
                ("edge2sku", "text", edge_2_sku),
                ("edge3name", "text", ''),
                ("edge3sku", "text", ''),
                ("edge4name", "text", ''),
                ("edge4sku", "text", '')]

            self.labels.append(lbl)
            self.label_count += 1

            #Create and add OperationGroup
            #Get info for segments
            X = self.distance(unit.inch(shelf_length_inch))
            Y = self.get_part_width(assembly)
            Z = self.distance(utils.get_part_thickness(obj))
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
            self.debug.write_debug_part(self, assembly, obj, op_grp, lbl, self.part_count)
            self.part_count += 1

    def write_oversize_top_shelf(self, node, obj):
        self.write_oversize_top_shelf_part(node, obj, side="Left")
        self.write_oversize_top_shelf_part(node, obj, side="Right")

    def write_products(self,project_node):
        specgroups = bpy.context.scene.mv.spec_groups
        item_name, _ = bpy.path.basename(bpy.data.filepath).split('.')

        existing_items = project_node.findall("Item")

        if existing_items:
            idx = project_node.getchildren().index(existing_items[-1]) + 1
            elm_product = self.xml.insert_element(idx, project_node, 'Item', {'ID': "IDI-{}".format(self.item_count)})
        
        else:
            elm_product = self.xml.add_element(project_node, 'Item', {'ID': "IDI-{}".format(self.item_count)})

        item_number = "{0:0=2d}".format(self.item_count + 1)

        self.xml.add_element_with_text(elm_product,'Name', self.job_number + "." + item_number)
        self.xml.add_element_with_text(elm_product,'Description', item_name)#Str literal OKAY
        self.xml.add_element_with_text(elm_product,'Note', "")#Str literal OKAY        

        for obj_product in self.products:
            spec_group = specgroups[obj_product.cabinetlib.spec_group_index]
            product = fd_types.Assembly(obj_product)
            
            #PRODUCTS MARKED TO EXPORT SUBASSEMBLIES WILL EXPORT A STRUCTURE
            #NESTED ONLY THREE LEVELS DEEP
            #PRODUCTS NOT MARKED WILL EXPORT A FLAT STRUCTURE ONE LEVEL DEEP
            if product.obj_bp.mv.export_product_subassemblies:
                use_recursive = False
            else:
                use_recursive = True
            
            #self.write_prompts_for_assembly(elm_product, product)
            self.write_parts_for_product(elm_product,obj_product,spec_group,recursive=use_recursive)

            #HARDWARE
            self.write_hardware_for_assembly(elm_product,obj_product,recursive=use_recursive)
            
            if not use_recursive:
                self.write_subassemblies_for_product(elm_product,obj_product,spec_group)

        self.item_count += 1
            
    def write_parts_for_product(self,elm_parts,obj_bp,spec_group,recursive=False):
        for child in obj_bp.children:
            for nchild in child.children:

                if nchild.cabinetlib.type_mesh == 'HARDWARE':
                    if not nchild.hide:
                        self.write_hardware_node(elm_parts, nchild)

                if nchild.cabinetlib.type_mesh in {'CUTPART','SOLIDSTOCK','BUYOUT'}:
                    if not nchild.hide:
                        self.write_part_node(elm_parts, nchild, spec_group, recursive=recursive)

                        if nchild.cabinetlib.type_mesh == 'CUTPART':
                            #self.op_groups.append("IDOP-{}".format(self.op_count))
                            #self.op_count += 1
                            pass

                        if nchild.cabinetlib.type_mesh == 'SOLIDSTOCK':
                            #Solid Stock op_groups here
                            #print("TODO: SOLIDSTOCK OPERATION GROUPS")
                            pass

                        if nchild.cabinetlib.type_mesh == 'BUYOUT':
                            #Buyout op_groups here
                            #print("BUYOUT")
                            pass                            

            if recursive:
                self.write_parts_for_product(elm_parts, child, spec_group, recursive=recursive)
            
    def write_subassemblies_for_product(self,elm_product,obj_bp,spec_group):
        for child in obj_bp.children:
            if child.mv.export_as_subassembly:
                assembly = fd_types.Assembly(child)
                hide = assembly.get_prompt("Hide")
                if hide:
                    if hide.value():
                        continue #SKIP HIDDEN SUBASSEMBLIES
                comment = ""
                for achild in assembly.obj_bp.children:
                    if achild.mv.comment != "":
                        comment = achild.mv.comment
                        break

                sub_name = assembly.obj_bp.mv.name_object if assembly.obj_bp.mv.name_object != "" else assembly.obj_bp.name
                elm_subassembly = self.xml.add_element(elm_product, "Assembly", {'ID': "IDA-{}".format(self.assembly_count)})
                self.xml.add_element_with_text(elm_subassembly, 'Name', sub_name)
                self.xml.add_element_with_text(elm_subassembly, 'Quantity', "1")

                if sub_name == "Top Shelf":
                    for child in assembly.obj_bp.children:
                        if child.lm_closets.is_plant_on_top_bp:
                            top_shelf_assembly = fd_types.Assembly(child)
                            if top_shelf_assembly.obj_x.location.x > unit.inch(97):
                                self.write_oversize_top_shelf(elm_subassembly, child)
                                self.assembly_count += 1
                                return
                
                #self.write_prompts_for_assembly(elm_subassembly, assembly)                
                self.write_parts_for_subassembly(elm_subassembly,assembly.obj_bp,spec_group)

                #HARDWARE
                self.write_hardware_for_assembly(elm_subassembly,assembly.obj_bp,recursive=True)                
                
                self.assembly_count += 1
                self.write_nested_subassemblies(elm_subassembly, assembly.obj_bp, spec_group)

        if obj_bp.lm_closets.is_hamper_insert_bp:
            assembly = fd_types.Assembly(obj_bp)
            hamper_type = assembly.get_prompt("Hamper Type").value()

            self.write_hardware_node(elm_subassembly, obj_bp, name="Hamper Brake Flap Left")
            self.write_hardware_node(elm_subassembly, obj_bp, name="Hamper Brake Flap Right")
            self.write_hardware_node(elm_subassembly, obj_bp, name="Hamper Rack")

            if hamper_type == 'Canvas':           
                self.write_hardware_node(elm_subassembly, obj_bp, name="Cloth Laundry Bag")
            
    def write_nested_subassemblies(self,elm_subassembly,obj_bp,spec_group):
        if obj_bp.lm_closets.is_hamper_insert_bp:
            assembly = fd_types.Assembly(obj_bp)
            hamper_type = assembly.get_prompt("Hamper Type").value()

            self.write_hardware_node(elm_subassembly, obj_bp, name="Hamper Brake Flap Left")
            self.write_hardware_node(elm_subassembly, obj_bp, name="Hamper Brake Flap Right")
            self.write_hardware_node(elm_subassembly, obj_bp, name="Hamper Rack")

            if hamper_type == 'Canvas':           
                self.write_hardware_node(elm_subassembly, obj_bp, name="Cloth Laundry Bag")

        for child in obj_bp.children:
            if child.mv.export_as_subassembly:
                assembly = fd_types.Assembly(child)
                hide = assembly.get_prompt("Hide")
                if hide:
                    if hide.value():
                        continue #SKIP HIDDEN SUBASSEMBLIES
                comment = ""
                for achild in assembly.obj_bp.children:
                    if achild.mv.comment != "":
                        comment = achild.mv.comment
                        break
                sub_name = assembly.obj_bp.mv.name_object if assembly.obj_bp.mv.name_object != "" else assembly.obj_bp.name
                elm_item = self.xml.add_element(elm_subassembly, 'Assembly', {'ID': "IDA-{}".format(self.assembly_count)})

                self.xml.add_element_with_text(elm_item, 'Name', sub_name)
                self.xml.add_element_with_text(elm_item, 'Quantity', "1")
                
                #self.write_prompts_for_assembly(elm_prompts, assembly)
                self.write_parts_for_subassembly(elm_item,assembly.obj_bp,spec_group)

                #HARDWARE
                self.write_hardware_for_assembly(elm_item,assembly.obj_bp)

                self.assembly_count += 1              

    def write_parts_for_subassembly(self,elm_parts,obj_bp,spec_group):
        #Slides
        if obj_bp.lm_closets.is_drawer_box_bp:
            self.write_hardware_node(elm_parts, obj_bp, name="Drawer Slide L")
            self.write_hardware_node(elm_parts, obj_bp, name="Drawer Slide R")

        #Locked shelf - add KD fittings (4)
        if obj_bp.lm_closets.is_shelf_bp:
            assembly = fd_types.Assembly(obj_bp)
            is_locked_shelf = assembly.get_prompt("Is Locked Shelf").value()

            if is_locked_shelf:
                self.write_hardware_node(elm_parts, obj_bp, name="KD Fitting")
                self.write_hardware_node(elm_parts, obj_bp, name="KD Fitting")
                self.write_hardware_node(elm_parts, obj_bp, name="KD Fitting")
                self.write_hardware_node(elm_parts, obj_bp, name="KD Fitting")

        #Door lock for doors 
        if obj_bp.lm_closets.is_door_insert_bp:
            door_insert = fd_types.Assembly(obj_bp)
            lock_door = door_insert.get_prompt("Lock Door").value()
            double_door_auto_switch = door_insert.get_prompt("Double Door Auto Switch").value()
            double_door = door_insert.get_prompt("Force Double Doors").value()

            if lock_door:
                self.write_hardware_node(elm_parts, obj_bp, name="Door Lock")
                self.write_hardware_node(elm_parts, obj_bp, name="Door Lock Cam")

                #Double door
                if double_door or door_insert.obj_x.location.x > double_door_auto_switch:
                    self.write_hardware_node(elm_parts, obj_bp, name="Door Lock Latch")               

        for child in obj_bp.children:
            if child.lm_closets.is_hanging_rod:
                for nchild in child.children:
                    if not nchild.hide:
                        self.write_hardware_node(elm_parts, obj_bp, name="Pole Cup")
                        self.write_hardware_node(elm_parts, obj_bp, name="Pole Cup")  

            for nchild in child.children:

                if nchild.cabinetlib.type_mesh == 'HARDWARE':
                    if not nchild.hide:
                        self.write_hardware_node(elm_parts, nchild)

                if nchild.cabinetlib.type_mesh in {'CUTPART','SOLIDSTOCK','BUYOUT'}:
                    if not nchild.hide:
                        self.write_part_node(elm_parts, nchild, spec_group)

                        if nchild.cabinetlib.type_mesh == 'CUTPART':
                            #self.op_groups.append("IDOP-{}".format(self.op_count))
                            #self.op_count += 1
                            pass                 

                        if nchild.cabinetlib.type_mesh == 'SOLIDSTOCK':
                            #Solid Stock op_groups here
                            #print("TODO: SOLIDSTOCK OPERATION GROUPS")
                            pass

                        if nchild.cabinetlib.type_mesh == 'BUYOUT':
                            #Buyout op_groups here
                            #print("BUYOUT")
                            pass                                   

    def write_parts_for_nested_subassembly(self,elm_parts,obj_bp,spec_group):
        for child in obj_bp.children:

            if child.cabinetlib.type_mesh == 'HARDWARE':
                if not child.hide:
                    self.write_hardware_node(elm_parts, child)

            if child.cabinetlib.type_mesh in {'CUTPART','SOLIDSTOCK','BUYOUT'}:
                if not child.hide:
                    self.write_part_node(elm_parts, child, spec_group)

                    if child.cabinetlib.type_mesh == 'CUTPART':
                        #self.op_groups.append("IDOP-{}".format(self.op_count))
                        #self.op_count += 1
                        pass                    

                    if child.cabinetlib.type_mesh == 'SOLIDSTOCK':
                        #Solid Stock op_groups here
                        #print("TODO: SOLIDSTOCK OPERATION GROUPS")
                        pass

                    if child.cabinetlib.type_mesh == 'BUYOUT':
                        #Buyout op_groups here
                        #print("BUYOUT")
                        pass                        
    
    #NEW
    def write_hardware_for_assembly(self,elm_hardware,obj_bp,recursive=False):
        pass

        # for child in obj_bp.children:
        #     if child.cabinetlib.type_mesh == 'HARDWARE':
        #         if not child.hide:
        #             hardware_name = child.mv.name_object if child.mv.name_object != "" else child.name
        #             elm_item = self.xml.add_element(elm_hardware,'Hardware',hardware_name)
                    
        #             if child.mv.hardware_x_dim != 0:
        #                 self.xml.add_element_with_text(elm_item,'XDimension',self.distance(child.mv.hardware_x_dim))
        #             else:
        #                 self.xml.add_element_with_text(elm_item,'XDimension',self.distance(child.dimensions.x))
                        
        #             if child.mv.hardware_y_dim != 0:
        #                 self.xml.add_element_with_text(elm_item,'YDimension',self.distance(child.mv.hardware_y_dim))
        #             else:
        #                 self.xml.add_element_with_text(elm_item,'YDimension',self.distance(child.dimensions.y))
                        
        #             if child.mv.hardware_z_dim != 0:
        #                 self.xml.add_element_with_text(elm_item,'ZDimension',self.distance(child.mv.hardware_z_dim))
        #             else:
        #                 self.xml.add_element_with_text(elm_item,'ZDimension',self.distance(child.dimensions.z))
                        
        #             if recursive:
        #                 product_bp = utils.get_bp(child,'PRODUCT')
        #                 loc_pos = product_bp.matrix_world.inverted() * child.matrix_world
        #                 x_loc = self.location(loc_pos[0][3])
        #                 y_loc = self.location(loc_pos[1][3])
        #                 z_loc = self.location(loc_pos[2][3])                                     
        #                 self.xml.add_element_with_text(elm_item,'XOrigin',x_loc)
        #                 self.xml.add_element_with_text(elm_item,'YOrigin',y_loc)
        #                 self.xml.add_element_with_text(elm_item,'ZOrigin',z_loc)   
        #             else:
        #                 loc_pos = child.parent.matrix_world.inverted() * child.matrix_world
        #                 x_loc = self.location(loc_pos[0][3])
        #                 y_loc = self.location(loc_pos[1][3])
        #                 z_loc = self.location(loc_pos[2][3])
        #                 self.xml.add_element_with_text(elm_item,'XOrigin',x_loc)
        #                 self.xml.add_element_with_text(elm_item,'YOrigin',y_loc)
        #                 self.xml.add_element_with_text(elm_item,'ZOrigin',z_loc)
                        
        #             self.xml.add_element_with_text(elm_item,'Comment',child.mv.comment)
        #             self.write_machine_tokens(elm_item,child)
                    
        #             self.xml.add_element_with_text(elm_item,'AssociativeHardwareRotation',str(child.mv.associative_rotation))
                    
        #     if recursive:
        #         self.write_hardware_for_assembly(elm_hardware, child, recursive=recursive)

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
        if assembly.obj_bp.mv.type_group == 'PRODUCT':
            if assembly.obj_bp.location.z > 0:
                elm_prompt = self.xml.add_element(elm_prompts,'Prompt',"HeightAboveFloor")
                self.xml.add_element_with_text(elm_prompt,'Value',"0")                  
    
    def write_hardware_node(self, elm_product, obj_bp, name=""):
        if obj_bp.mv.type == 'BPASSEMBLY':
            assembly = fd_types.Assembly(obj_bp)
        else:
            assembly = fd_types.Assembly(obj_bp.parent)

        if name != "":
            hardware_name = name
        
        else:
            hardware_name = obj_bp.mv.name_object if obj_bp.mv.name_object != "" else obj_bp.name
        
        elm_hdw_part = self.xml.add_element(elm_product,
                                        'Part',
                                        {'ID': "IDP-{}".format(self.part_count),
                                        'LabelID': "IDL-{}".format(self.label_count)                          
                                        })
        
        self.xml.add_element_with_text(elm_hdw_part, 'Name', hardware_name)
        self.xml.add_element_with_text(elm_hdw_part, 'Quantity', "1")
        self.xml.add_element_with_text(elm_hdw_part, 'Routing', "HDSTK")#Str literal OKAY
        self.xml.add_element_with_text(elm_hdw_part, 'Type', "hardware")#Str literal OKAY

        lbl = [
            ("IDL-{}".format(self.label_count), "IDJ-{}".format(self.job_count), "IDP-{}".format(self.part_count)),
            ("name", "text", hardware_name),
            ("x", "text", "0"),
            ("y", "text", "0"),
            ("z", "text", "0"),
            ("lenx", "text", "0"),
            ("leny", "text", "0"),
            ("lenz", "text", "0"),
            ("rotx", "text", str(int(math.degrees(assembly.obj_bp.rotation_euler.x)))),
            ("roty", "text", str(int(math.degrees(assembly.obj_bp.rotation_euler.y)))),
            ("rotz", "text", str(int(math.degrees(assembly.obj_bp.rotation_euler.z)))),
            ("material", "text", ""),#Str literal OKAY
            ("copies", "text", ""),#Str literal OKAY
            ("sku", "text", get_hardware_sku(obj_bp, assembly, hardware_name)),#Get sku value from Database
            ("color", "text", ""),#Str literal OKAY
            ("type", "text", "hardware")#Str literal OKAY
        ]

        self.labels.append(lbl)
        self.label_count += 1
        self.part_count += 1

    def write_part_node(self,node,obj,spec_group,recursive=False):
        if obj.mv.type == 'BPASSEMBLY':
            assembly = fd_types.Assembly(obj)
        else:
            assembly = fd_types.Assembly(obj.parent)

        if assembly.obj_bp.lm_closets.is_shelf_bp:
                is_locked_shelf = assembly.get_prompt("Is Locked Shelf").value()

                if is_locked_shelf:
                    self.write_hardware_node(node, assembly.obj_bp, name="KD Fitting")
                    self.write_hardware_node(node, assembly.obj_bp, name="KD Fitting")
                    self.write_hardware_node(node, assembly.obj_bp, name="KD Fitting")
                    self.write_hardware_node(node, assembly.obj_bp, name="KD Fitting")

                else:
                    self.write_hardware_node(node, assembly.obj_bp, name="Peg Chrome")
                    self.write_hardware_node(node, assembly.obj_bp, name="Peg Chrome")
                    self.write_hardware_node(node, assembly.obj_bp, name="Peg Chrome")
                    self.write_hardware_node(node, assembly.obj_bp, name="Peg Chrome")

        if assembly.obj_bp.mv.type_group != "PRODUCT":

            unique_mat = False
            obj_props = assembly.obj_bp.lm_closets
            closet_materials = bpy.context.scene.db_materials
            if obj_props.is_back_bp:
                if obj_props.use_unique_material:
                    unique_mat = True
                    mat_name = obj_props.unique_mat_colors
                    unique_mat_sku = closet_materials.get_mat_sku(mat_name=mat_name)
                    mat_inventory_name = closet_materials.get_mat_inventory_name(sku=unique_mat_sku)
                    mat_id = self.write_single_material(mat_inventory_name, unique_mat_sku)

            elm_part = self.xml.add_element(
                node,
                'Part',
                {
                    'ID': "IDP-{}".format(self.part_count),
                    'MatID': "IDM-{}".format(self.mat_count if not unique_mat else mat_id),
                    'LabelID': "IDL-{}".format(self.label_count),
                    'OpID': "IDOP-{}".format(self.op_count)
                }
            )

            #----------Add part name
            if obj.type == 'CURVE':
                part_name = obj.mv.name_object if obj.mv.name_object != "" else obj.name
            else:
                part_name = assembly.obj_bp.mv.name_object if assembly.obj_bp.mv.name_object != "" else assembly.obj_bp.name

            self.xml.add_element_with_text(elm_part, 'Name', part_name)
            self.xml.add_element_with_text(elm_part,'Quantity', self.get_part_qty(assembly))
            self.xml.add_element_with_text(elm_part,'Width', self.get_part_width(assembly)) 
            self.xml.add_element_with_text(elm_part,'FinishedWidth', self.get_part_width(assembly))           
            self.xml.add_element_with_text(elm_part,'Length', self.get_part_length(assembly))
            self.xml.add_element_with_text(elm_part,'FinishedLength', self.get_part_length(assembly))
            self.xml.add_element_with_text(elm_part,'Thickness',self.distance(utils.get_part_thickness(obj)))
            self.xml.add_element_with_text(elm_part,'FinishedThickness', self.distance(utils.get_part_thickness(obj)))
            self.xml.add_element_with_text(elm_part,'Routing', "SK1")#Str literal okay
            self.xml.add_element_with_text(elm_part,'Class', "make")#Str literal okay
            self.xml.add_element_with_text(elm_part,'Type', "panel")#"panel" for part "unknown" for solid stock

            elm_unit = self.xml.add_element(elm_part,'Unit')
            self.xml.add_element_with_text(elm_unit,'Name', "dimension")#Str literal okay
            self.xml.add_element_with_text(elm_unit,'Measure', "inch")#Str literal okay
            self.xml.add_element_with_text(elm_unit,'RoundFactor', "0")#Str literal okay

            closet_materials = bpy.context.scene.db_materials

            #EDGEBANDING
            edge_1 = ''
            edge_2 = ''
            edge_3 = ''
            edge_4 = ''
            edge_1_sku = ''
            edge_2_sku = ''
            edge_3_sku = ''
            edge_4_sku = ''

            obj_props = assembly.obj_bp.lm_closets

            #print(assembly.obj_bp, assembly.obj_bp.parent)
            #Doors
            if obj_props.is_door_bp or obj_props.is_hamper_front_bp:
                edge_1 = 'EBT'
                edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                edge_2 = 'EBR'
                edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                edge_3 = 'EBB'
                edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                edge_4 = 'EBL'
                edge_4_sku = closet_materials.get_edge_sku(obj, assembly, part_name)

            #Panel, Shelf
            if obj_props.is_panel_bp or obj_props.is_shelf_bp:
                edge_1 = 'EBF'
                edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)

            #Drawers
            if obj_props.is_drawer_front_bp:
                edge_1 = 'EBT'
                edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)    
                edge_2 = 'EBR'
                edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                edge_3 = 'EBB'
                edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                edge_4 = 'EBL'
                edge_4_sku = closet_materials.get_edge_sku(obj, assembly, part_name)                            

            if obj_props.is_drawer_sub_front_bp:
                edge_1 = 'EBT'
                edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name) 

            if obj_props.is_drawer_side_bp:
                edge_1 = 'EBT'
                edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name) 

            if obj_props.is_drawer_back_bp:
                edge_1 = 'EBT'
                edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name) 

            #Cleats
            if obj_props.is_cleat_bp:
                if "Top" in assembly.obj_bp.mv.name:
                    edge_1 = 'EBB'
                    edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)                      

                elif "Bottom" in assembly.obj_bp.mv.name:
                    edge_1 = 'EBT'
                    edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)                     

            #Door striker
            if  obj_props.is_door_striker_bp:
                edge_1 = 'EBF'
                edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)                

            #L Shelf
            if obj_props.is_l_shelf_bp:
                edge_1 = 'EBF'
                edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)                
                edge_2 = 'EBF'
                edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)                

            #Shelf lip
            if obj_props.is_shelf_lip_bp:
                edge_1 = 'EBT'
                edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)

            #Top shelf
            if obj_props.is_plant_on_top_bp:
                edge_1 = 'EBF'
                edge_1_sku = closet_materials.get_edge_sku(obj, assembly, part_name)
                
                carcass_bp = utils.get_parent_assembly_bp(obj)
                carcass_assembly = fd_types.Assembly(carcass_bp)
                l_end_cond = carcass_assembly.get_prompt("Left End Condition").value()
                r_end_cond = carcass_assembly.get_prompt("Right End Condition").value()

                if l_end_cond == 'EP' and r_end_cond != 'EP':
                    edge_2 = 'EBL'
                    edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)                    

                if r_end_cond == 'EP' and l_end_cond != 'EP':
                    edge_2 = 'EBR'
                    edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)

                if l_end_cond == 'EP' and r_end_cond == 'EP':
                    edge_2 = 'EBL'
                    edge_2_sku = closet_materials.get_edge_sku(obj, assembly, part_name)                    
                    edge_3 = 'EBR'
                    edge_3_sku = closet_materials.get_edge_sku(obj, assembly, part_name)

            #Create and add label
            lbl = [
                ("IDL-{}".format(self.label_count), "IDJ-{}".format(self.job_count), "IDP-{}".format(self.part_count)),                
                ("dcname", "text", part_name),
                ("name", "text", part_name),
                ("variablesection", "text", str(self.is_variable_section(assembly))),
                ("x", "text", self.get_part_x_location(assembly.obj_bp,assembly.obj_bp.location.x)),
                ("y", "text", self.get_part_y_location(assembly.obj_bp,assembly.obj_bp.location.y)),
                ("z", "text", self.get_part_z_location(assembly.obj_bp,assembly.obj_bp.location.z)),
                ("lenx", "text", self.get_part_length(assembly)),
                ("leny", "text", self.get_part_width(assembly)),
                ("lenz", "text", self.distance(utils.get_part_thickness(obj))),
                ("rotx", "text", str(int(math.degrees(assembly.obj_bp.rotation_euler.x)))),
                ("roty", "text", str(int(math.degrees(assembly.obj_bp.rotation_euler.x)))),
                ("rotz", "text", str(int(math.degrees(assembly.obj_bp.rotation_euler.x)))),
                ("boml", "text", self.get_part_length(assembly)),
                ("bomt", "text",  self.distance(utils.get_part_thickness(obj))),
                ("bomw", "text", self.get_part_width(assembly)),
                ("catnum", "text", self.get_part_comment(assembly.obj_bp)),#Part Comments2
                ("sku", "text", closet_materials.get_mat_sku(obj, assembly, part_name) if not unique_mat else unique_mat_sku),#Get sku value from Database
                ("cncmirror", "text", ""),#Str literal OKAY
                ("cncrotation", "text", "180"),#Str literal OKAY
                ("cutl", "text", self.get_part_length(assembly)),#Part.AdjustedCutPartLength 
                ("cutt", "text", self.distance(utils.get_part_thickness(obj))),
                ("cutw", "text", self.get_part_width(assembly)),#Part.AdjustedCutPartWidth
                ("edge1name", "text", edge_1),
                ("edge1sku", "text", edge_1_sku),
                ("edge2name", "text", edge_2),
                ("edge2sku", "text", edge_2_sku),
                ("edge3name", "text", edge_3),
                ("edge3sku", "text", edge_3_sku),
                ("edge4name", "text", edge_4),
                ("edge4sku", "text", edge_4_sku)]

            self.labels.append(lbl)
            self.label_count += 1

            #Create and add OperationGroup
            #Get info for segments
            X = self.get_part_length(assembly)
            Y = self.get_part_width(assembly)
            Z = self.distance(utils.get_part_thickness(obj))
            W = 0

            #Drawer front assembly X and Y is flipped for wood grain direction
            if obj_props.is_drawer_front_bp:
                X = self.get_part_width(assembly)
                Y = self.get_part_length(assembly)


            upper_right = (X, Y, Z, W)
            upper_left = (0, Y, Z, W)
            lower_left = (0, 0, Z, W)
            lower_right = (X, 0, Z, W)

            #Add circles
            circles = []

            #Look for machine tokens in assembly meshes
            for child in assembly.obj_bp.children:
                if child.type == 'MESH':
                    tokens = child.mv.mp.machine_tokens

                    if len(tokens) > 0:
                        for token in tokens:
                            if not token.is_disabled:
                                if token.type_token == 'BORE':
                                    token_name = token.name if token.name != "" else "Unnamed"
                                    
                                    if token_name == "Unnamed":
                                        print("Unnamed machine token!")

                                    if token_name == 'Pull Drilling':                                   
                                        normal_z = 1
                                        org_displacement = 0

                                        if token.face == '6':
                                            normal_z = -1
                                            org_displacement = self.distance(utils.get_part_thickness(obj))

                                        param_dict = token.create_parameter_dictionary()  
                                        dim_in_x = float(param_dict['Par1'])
                                        dim_in_y = float(param_dict['Par2'])
                                        dim_in_z = float(param_dict['Par3'])
                                        bore_dia_meter = unit.millimeter(float(param_dict['Par4']))
                                        bore_dia = unit.meter_to_inch(bore_dia_meter)
                                        end_dim_in_x = float(param_dict['Par5'])
                                        end_dim_in_y = float(param_dict['Par6'])
                                        distance_between_holes = float(param_dict['Par7'])                                          

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

                                    #System holes
                                    sys_holes = (
                                        'System Holes Right Top Front',
                                        'System Holes Right Top Rear',
                                        'System Holes Right Bottom Front',
                                        'System Holes Right Bottom Rear',
                                        'System Holes Left Top Front',
                                        'System Holes Left Top Rear',
                                        'System Holes Left Bottom Front',
                                        'System Holes Left Bottom Rear',
                                    )
                                    
                                    if token_name in sys_holes:                     
                                        param_dict = token.create_parameter_dictionary()
                                        start_dim_x = float(param_dict['Par1'])                                        
                                        start_dim_y = float(param_dict['Par2'])
                                        drill_depth = float(param_dict['Par3'])
                                        bore_dia = unit.meter_to_inch(float(param_dict['Par4']))#Convert to inches
                                        end_dim_x = float(param_dict['Par5'])
                                        end_dim_in_y = float(param_dict['Par6'])
                                        distance_between_holes = float(param_dict['Par7'])

                                        normal_z = 1
                                        org_displacement = 0

                                        if token.face == '6':
                                            normal_z = -1
                                            org_displacement = self.distance(utils.get_part_thickness(obj))
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

                                                cir = {}
                                                cir['cen_x'] = x
                                                cir['cen_y'] = start_dim_y
                                                cir['cen_z'] = drill_depth
                                                cir['diameter'] = bore_dia
                                                cir['normal_z'] = normal_z
                                                cir['org_displacement'] = org_displacement
                                                circles.append(cir)
                                        else:
                                            while x < end_dim_x:
                                                x += distance_between_holes

                                                cir = {}
                                                cir['cen_x'] = x
                                                cir['cen_y'] = start_dim_y
                                                cir['cen_z'] = drill_depth
                                                cir['diameter'] = bore_dia
                                                cir['normal_z'] = normal_z
                                                cir['org_displacement'] = org_displacement
                                                circles.append(cir)

                                    if token_name == 'Door Hinge Drilling':
                                        door_swing = assembly.get_prompt("Door Swing").value()
                                        door_x_dim = unit.meter_to_inch(assembly.obj_x.location.x)
                                        door_y_dim = abs(unit.meter_to_inch(assembly.obj_y.location.y))
                                        normal_z = -1
                                        org_displacement = self.distance(utils.get_part_thickness(obj))
                                        bore_dia = unit.meter_to_inch(unit.millimeter(35))
                                        dim_in_x = unit.meter_to_inch(unit.millimeter(78))
                                        dim_in_y = unit.meter_to_inch(unit.millimeter(21))                                   
                                        bore_depth = unit.meter_to_inch(unit.millimeter(11.5))
                                        screw_hole_y_dim = unit.meter_to_inch(unit.millimeter(9.5)) 
                                        screw_hole_dia = unit.meter_to_inch(unit.millimeter(0.5)) 
                                        distance_between_holes = unit.meter_to_inch(unit.millimeter(45))
                                        mid_hole_offset = unit.meter_to_inch(unit.millimeter(16))

                                        if door_swing == "Left":
                                            dim_in_y = door_y_dim - unit.meter_to_inch(unit.millimeter(21))
                                            screw_hole_y_dim = -(screw_hole_y_dim)

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
                                        cir['cen_z'] = bore_depth
                                        cir['diameter'] = screw_hole_dia 
                                        cir['normal_z'] = normal_z
                                        cir['org_displacement'] = org_displacement
                                        circles.append(cir)                                        

                                        #add screw hole right
                                        cir = {}
                                        cir['cen_x'] = -(dim_in_x + distance_between_holes * 0.5)
                                        cir['cen_y'] = dim_in_y + screw_hole_y_dim
                                        cir['cen_z'] = bore_depth
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
                                        cir['cen_z'] = bore_depth
                                        cir['diameter'] = screw_hole_dia 
                                        cir['normal_z'] = normal_z
                                        cir['org_displacement'] = org_displacement
                                        circles.append(cir)                                        

                                        #add screw hole right
                                        cir = {}
                                        cir['cen_x'] = -(dim_in_x + distance_between_holes * 0.5)
                                        cir['cen_y'] = dim_in_y + screw_hole_y_dim
                                        cir['cen_z'] = bore_depth
                                        cir['diameter'] = screw_hole_dia 
                                        cir['normal_z'] = normal_z
                                        cir['org_displacement'] = org_displacement
                                        circles.append(cir)

                                        #Mid hinge drilling for doors longer than 52"
                                        if door_x_dim > 52:
                                            dim_in_x = door_x_dim * 0.5 - mid_hole_offset

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
                                            cir['cen_z'] = bore_depth
                                            cir['diameter'] = screw_hole_dia 
                                            cir['normal_z'] = normal_z
                                            cir['org_displacement'] = org_displacement
                                            circles.append(cir)                                        

                                            #add screw hole right
                                            cir = {}
                                            cir['cen_x'] = -(dim_in_x + distance_between_holes * 0.5)
                                            cir['cen_y'] = dim_in_y + screw_hole_y_dim
                                            cir['cen_z'] = bore_depth
                                            cir['diameter'] = screw_hole_dia 
                                            cir['normal_z'] = normal_z
                                            cir['org_displacement'] = org_displacement
                                            circles.append(cir)                                            

                                    if token_name == "Hamper Door Hinge Drilling":
                                        door_x_dim = unit.meter_to_inch(assembly.obj_x.location.x)
                                        door_y_dim = abs(unit.meter_to_inch(assembly.obj_y.location.y))
                                        normal_z = -1
                                        org_displacement = self.distance(utils.get_part_thickness(obj))
                                        bore_dia = unit.meter_to_inch(unit.millimeter(35))
                                        dim_in_x = unit.meter_to_inch(unit.millimeter(21))
                                        dim_in_y = unit.meter_to_inch(unit.millimeter(78))                                   
                                        bore_depth = unit.meter_to_inch(unit.millimeter(11.5))
                                        screw_hole_x_dim = unit.meter_to_inch(unit.millimeter(9.5)) 
                                        screw_hole_dia = unit.meter_to_inch(unit.millimeter(0.5)) 
                                        distance_between_holes = unit.meter_to_inch(unit.millimeter(45))

                                        #Right
                                        cir = {}
                                        cir['cen_x'] = -dim_in_x
                                        cir['cen_y'] = dim_in_y
                                        cir['cen_z'] = bore_depth
                                        cir['diameter'] = bore_dia 
                                        cir['normal_z'] = normal_z
                                        cir['org_displacement'] = org_displacement
                                        circles.append(cir)                                        

                                        cir = {}
                                        cir['cen_x'] = -(dim_in_x + screw_hole_x_dim)
                                        cir['cen_y'] = dim_in_y + distance_between_holes * 0.5
                                        cir['cen_z'] = bore_depth
                                        cir['diameter'] = screw_hole_dia 
                                        cir['normal_z'] = normal_z
                                        cir['org_displacement'] = org_displacement
                                        circles.append(cir)                                        

                                        cir = {}
                                        cir['cen_x'] = -(dim_in_x + screw_hole_x_dim)
                                        cir['cen_y'] = dim_in_y - distance_between_holes * 0.5
                                        cir['cen_z'] = bore_depth
                                        cir['diameter'] = screw_hole_dia 
                                        cir['normal_z'] = normal_z
                                        cir['org_displacement'] = org_displacement
                                        circles.append(cir)

                                        dim_in_y = door_y_dim - dim_in_y

                                        #Left
                                        cir = {}
                                        cir['cen_x'] = -dim_in_x
                                        cir['cen_y'] = dim_in_y
                                        cir['cen_z'] = bore_depth
                                        cir['diameter'] = bore_dia 
                                        cir['normal_z'] = normal_z
                                        cir['org_displacement'] = org_displacement
                                        circles.append(cir)                                        

                                        cir = {}
                                        cir['cen_x'] = -(dim_in_x + screw_hole_x_dim)
                                        cir['cen_y'] = dim_in_y + distance_between_holes * 0.5
                                        cir['cen_z'] = bore_depth
                                        cir['diameter'] = screw_hole_dia 
                                        cir['normal_z'] = normal_z
                                        cir['org_displacement'] = org_displacement
                                        circles.append(cir)                                        

                                        cir = {}
                                        cir['cen_x'] = -(dim_in_x + screw_hole_x_dim)
                                        cir['cen_y'] = dim_in_y - distance_between_holes * 0.5
                                        cir['cen_z'] = bore_depth
                                        cir['diameter'] = screw_hole_dia 
                                        cir['normal_z'] = normal_z
                                        cir['org_displacement'] = org_displacement
                                        circles.append(cir)

                                    if token_name == 'Shelf and Rod Holes':
                                        print("Found machine token:", token_name)


                                    #Middle hanging rods
                                    if token_name == 'System Holes Mid':
                                        print("Found machine token:", token_name)
                                        

                                if token.type_token == 'SLIDE':
                                    param_dict = token.create_parameter_dictionary()

                                    slide_type = closet_materials.get_drawer_slide_type()
                                    slide_size = get_slide_size(slide_type, assembly)
                                    front_hole_dim_m = unit.millimeter(slide_size.front_hole_dim_mm)
                                    front_hole_dim_inch = unit.meter_to_inch(front_hole_dim_m)
                                    back_hole_dim_m = unit.millimeter(slide_size.back_hole_dim_mm)
                                    back_hole_dim_inch = unit.meter_to_inch(back_hole_dim_m)
                                    
                                    dim_from_drawer_bottom = 0.5 # 0.5" should this be added to csv files?
                                    dim_to_first_hole = front_hole_dim_inch
                                    dim_to_second_hole = back_hole_dim_inch
                                    bore_depth_and_dia = param_dict['Par7']
                                    bore_depth, bore_dia = bore_depth_and_dia.split("|")
                                    bore_depth_f = float(bore_depth)
                                    bore_dia_meter = unit.millimeter(float(bore_dia))
                                    bore_dia_inch = unit.meter_to_inch(bore_dia_meter)

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

            op_grp = [
                ("IDOP-{}".format(self.op_count), "IDMOR-{}".format(self.or_count)),
                upper_right,#Segment 1
                upper_left,#Segment 2
                lower_left,#Segment 3
                lower_right,#Segment 4
                circles
            ]

            #Create and operation group for every part
            self.op_groups.append(op_grp)
            self.op_count += 1

            #get token info for writing to op group later
            #self.write_machine_tokens(elm_part, obj)            

            self.debug.write_debug_part(self, assembly, obj, op_grp, lbl, self.part_count)

            self.part_count += 1
    
    def write_single_material(self,mat_name,mat_sku):
        elm_job = self.xml.tree.findall("Job")[0]
        existing_mats = elm_job.findall("Material")
        mat_id = self.mat_count

        if existing_mats:
            idx = elm_job.getchildren().index(existing_mats[-1]) + 1
            elm_material = self.xml.insert_element(idx, elm_job, 'Material', {'ID': "IDM-{}".format(mat_id)})

        else:
            elm_material = self.xml.add_element(elm_job, 'Material', {'ID': "IDM-{}".format(mat_id)})

        self.xml.add_element_with_text(elm_material, 'Name', mat_name)
        self.xml.add_element_with_text(elm_material, 'Type', "sheet")
        self.xml.add_element_with_text(elm_material, 'SKU', mat_sku)

        self.mat_count += 1

        return mat_id

    def write_materials(self,project_node):
        closet_materials = bpy.context.scene.db_materials
        material_name = closet_materials.get_mat_inventory_name()
        existing_mats = project_node.findall("Material")

        if existing_mats:
            idx = project_node.getchildren().index(existing_mats[-1]) + 1
            elm_material = self.xml.insert_element(idx, project_node, 'Material', {'ID': "IDM-{}".format(self.mat_count)})

        else:
            elm_material = self.xml.add_element(project_node, 'Material', {'ID': "IDM-{}".format(self.mat_count)})

        self.xml.add_element_with_text(elm_material, 'Name', material_name)
        self.xml.add_element_with_text(elm_material, 'Type', "sheet")
        self.xml.add_element_with_text(elm_material, 'SKU', closet_materials.get_mat_sku())

        self.mat_count += 1

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
            self.xml.add_element_with_text(elm_solid_stock,'Thickness',str(unit.meter_to_active_unit(self.solid_stock_materials[solid_stock])))
        
    def write_spec_groups(self,project_node):
        #Currently not being used but we might need to export spec groups at some point
        elm_spec_groups = self.xml.add_element(project_node,"SpecGroups")
        
        for spec_group in bpy.context.scene.mv.spec_groups:
            spec_group_name = spec_group.name if spec_group.name != "" else "Unnamed"
            elm_spec_group = self.xml.add_element(elm_spec_groups,'SpecGroup',spec_group_name)
            elm_cutparts = self.xml.add_element(elm_spec_group,'CutParts')
            for cutpart in spec_group.cutparts:
                elm_cutpart_name = cutpart.mv_pointer_name if cutpart.mv_pointer_name != "" else "Unnamed"
                elm_cutpart = self.xml.add_element(elm_cutparts,'PointerName',elm_cutpart_name)
                mat_name = utils.get_material_name_from_pointer(cutpart,spec_group)
                material_name = mat_name if mat_name != "" else "Unnamed"
                self.xml.add_element_with_text(elm_cutpart,'MaterialName',material_name)
                 
            elm_edgeparts = self.xml.add_element(elm_spec_group,'EdgeParts')
            for edgepart in spec_group.edgeparts:
                elm_edgepart_name = edgepart.mv_pointer_name if edgepart.mv_pointer_name != "" else "Unnamed"
                elm_edgepart = self.xml.add_element(elm_edgeparts,'PointerName',elm_edgepart_name)
                mat_name = utils.get_edgebanding_name_from_pointer_name(edgepart.name,spec_group)
                edge_material_name = mat_name if mat_name != "" else "Unnamed"
                self.xml.add_element_with_text(elm_edgepart,'MaterialName',edge_material_name)

    def write_machine_tokens(self,elm_part,obj_part):
        #print("WRITING machine token for:")
        #print(obj_part)
        pass
        #NO MachineTokens XML ELEMENT NEEDED
        # elm_tokens = self.xml.add_element(elm_part,"MachineTokens")

        #LOOP TOKENS ON THIS PART
        for token in obj_part.mv.mp.machine_tokens:
            if not token.is_disabled:
                token_name = token.name if token.name != "" else "Unnamed"

                #NO MachineTokens XML ELEMENT NEEDED
                #elm_token = self.xml.add_element(elm_tokens,'MachineToken',token_name)
                param_dict = token.create_parameter_dictionary()

                #Only type_token used in (CORNERNOTCH, CHAMFER, SLIDE, BORE)
                if token.type_token in {'CORNERNOTCH','CHAMFER','3SIDEDNOTCH'}:
                    #print("token.type_token: 'CORNERNOTCH','CHAMFER','3SIDEDNOTCH'")
                    instructions = token.type_token + token.face + " " + token.edge
                    #print("instructions:", instructions)

                elif token.type_token == 'SLIDE':
                    #print("token.type_token: 'SLIDE'")
                    instructions = token.type_token
                    #print("instructions:", instructions)
                    
                else:
                    #print("token.type_token: ALL OTHERS")
                    instructions = token.type_token + token.face
                    #print("instructions:", instructions)

                #BORE info from token
                # if self.type_token == 'BORE':
                #     param_dict['Par1'] = str(unit.meter_to_exact_unit(self.dim_in_x))
                #     param_dict['Par2'] = str(unit.meter_to_exact_unit(self.dim_in_y))
                #     param_dict['Par3'] = str(unit.meter_to_exact_unit(self.dim_in_z))
                #     param_dict['Par4'] = str(self.face_bore_dia)
                #     param_dict['Par5'] = str(unit.meter_to_exact_unit(self.end_dim_in_x))
                #     param_dict['Par6'] = str(unit.meter_to_exact_unit(self.end_dim_in_y))
                #     param_dict['Par7'] = str(unit.meter_to_exact_unit(self.distance_between_holes))
                #     param_dict['Par8'] = str(self.associative_dia)
                #     param_dict['Par9'] = str(unit.meter_to_exact_unit(self.associative_depth))     

                #print("Attempting to add Element:")
                #self.xml.add_element_with_text(elm_token,'Instruction',instructions)
                #print("\t", instructions)

                #self.xml.add_element_with_text(elm_token,'Par1',param_dict['Par1'])
                #print("\t par1", param_dict['Par1'])

                #self.xml.add_element_with_text(elm_token,'Par2',param_dict['Par2'])
                #print("\t par2", param_dict['Par2'])

                #self.xml.add_element_with_text(elm_token,'Par3',param_dict['Par3'])
                #print("\t par3", param_dict['Par3'])

                #self.xml.add_element_with_text(elm_token,'Par4',param_dict['Par4'])
                #print("\t par4", param_dict['Par4'])

                #self.xml.add_element_with_text(elm_token,'Par5',param_dict['Par5'])
                #print("\t par5", param_dict['Par5'])

                #self.xml.add_element_with_text(elm_token,'Par6',param_dict['Par6'])
                #print("\t par6", param_dict['Par6'])

                #self.xml.add_element_with_text(elm_token,'Par7',param_dict['Par7'])
                #print("\t par7", param_dict['Par7'])

                #self.xml.add_element_with_text(elm_token,'Par8',param_dict['Par8'])
                #print("\t par8", param_dict['Par8'])

                #self.xml.add_element_with_text(elm_token,'Par9',param_dict['Par9'])
                #print("\t par9", param_dict['Par9'])
 
    def write_job_info(self, elm_job):
        dirname = os.path.dirname(bpy.data.filepath).split("\\")[-1]
        filname = "{}.ccp".format(dirname)
        tree = ET.parse(os.path.join(os.path.dirname(bpy.data.filepath), filname))
        root = tree.getroot()
        elm_pinfo = root.find("ProjectInfo")
        elm_rooms = root.find("Rooms")
        rooms = elm_rooms.getchildren()

        customer_name = elm_pinfo.find("customer_name").text
        client_id = elm_pinfo.find("client_id").text
        proj_address = elm_pinfo.find("project_address").text
        cphone_1 = elm_pinfo.find("customer_phone_1").text
        cphone_2 = elm_pinfo.find("customer_phone_2").text
        c_email = elm_pinfo.find("customer_email").text
        proj_notes = elm_pinfo.find("project_notes").text
        designer = elm_pinfo.find("designer").text
        total_room_count = str(len(rooms))
        design_date = elm_pinfo.find("design_date").text

        info = [('jobnumber', self.job_number),
                ('customername', customer_name),
                ('clientid', client_id),
                ('projectaddress', proj_address),
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
            idx = elm_mfg.getchildren().index(existing_or[-1]) + 1           
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
        mat_node_1 = job_node.findall("Material")[0]
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
                idx = elm_mfg.getchildren().index(existing_or[-1]) + 1           
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
                'z': "-{}".format(str(cen_z))
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
        if DEBUG_MODE:
            self.debug = debug_xml_export.Debug()

        self.clear_and_collect_data(context)

        #Replaces project name (filname)
        job_id = "IDJ-{}".format(self.job_count)
        self.set_job_number()

        job_name = self.job_number
        job_source = "SNaP"

        proj_props = bpy.context.window_manager.fd_project
        proj_name = proj_props.projects[proj_props.project_index].name
        path = os.path.join(os.path.dirname(bpy.utils.user_resource('DATAFILES')), "projects", proj_name, snap_xml.Snap_XML.filename)

        self.xml = snap_xml.Snap_XML()

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
            self.write_materials(elm_job)
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
            self.write_materials(self.xml.root)

        #self.write_edgebanding(elm_project)
        #self.write_buyout_materials(elm_project)
        #self.write_solid_stock_material(elm_project)

        self.xml.write(self.xml_path)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(OPS_Export_XML)


def unregister():
    bpy.utils.unregister_class(OPS_Export_XML)    
    
