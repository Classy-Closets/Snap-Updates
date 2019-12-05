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
from . import snap_export
import snap_db
from pprint import pprint


BL_DIR = os.path.dirname(bpy.app.binary_path)
CSV_PATH = os.path.join(BL_DIR, "data", "CCItems.csv")
DIR_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', "snap_db")
ITEMS_TABLE_NAME = "CCItems"

class Debug:
    debug_xml = None

    def __init__(self):
        self.dir_clear = False

    def init_dir(self, debug_dir):
        if not os.path.exists(debug_dir):
            os.mkdir(debug_dir)

        for f in os.scandir(debug_dir):
            os.remove(f.path)

        self.dir_clear = True

    def write_debug_part(self, operator, assembly, obj, op_grp, lbl, part_id):
        debug_dir = os.path.join(operator.xml_path, "DEBUG")

        if not self.dir_clear:
            self.init_dir(debug_dir)

        self.debug_xml = snap_xml.Snap_XML()

        #----------Add part name
        if obj.type == 'CURVE':
            part_name = obj.mv.name_object if obj.mv.name_object != "" else obj.name
        else:
            part_name = assembly.obj_bp.mv.name_object if assembly.obj_bp.mv.name_object != "" else assembly.obj_bp.name

        self.debug_xml.filename = "DEBUG_IDP-{}_{}-{}.xml".format(part_id, part_name, obj.name.replace(".", "-"))

        #Add job            
        elm_job = self.debug_xml.add_element(self.debug_xml.root, 'Job', {'ID':"IDJ-1", })
        self.debug_xml.add_element_with_text(elm_job, 'Name', "jobname")
        self.debug_xml.add_element_with_text(elm_job, 'Source', "SNaP")
        elm_unit = self.debug_xml.add_element(elm_job, 'Unit')
        self.debug_xml.add_element_with_text(elm_unit, 'Name', 'dimension')
        self.debug_xml.add_element_with_text(elm_unit, 'Measure', 'inch')            

        #Write Item
        elm_product = self.debug_xml.add_element(elm_job, 'Item', {'ID': "IDI-1", })
        self.debug_xml.add_element_with_text(elm_product,'Name', "jobname")
        self.debug_xml.add_element_with_text(elm_product,'Description', "Unknown")#Str literal OKAY
        self.debug_xml.add_element_with_text(elm_product,'Note', "")#Str literal OKAY             

        #PART NODE
        elm_part = self.debug_xml.add_element(
            elm_product,
            'Part',
            {
                'ID': "IDP-1",
                'MatID': "IDM-1",
                'LabelID': "IDL-1",
                'OpID': "IDOP-1"
            }
        )

        self.debug_xml.add_element_with_text(elm_part, 'Name', part_name)

        self.debug_xml.add_element_with_text(elm_part,'Quantity', operator.get_part_qty(assembly))
        self.debug_xml.add_element_with_text(elm_part,'Width', operator.get_part_width(assembly)) 
        self.debug_xml.add_element_with_text(elm_part,'FinishedWidth', operator.get_part_width(assembly))           
        self.debug_xml.add_element_with_text(elm_part,'Length', operator.get_part_length(assembly))
        self.debug_xml.add_element_with_text(elm_part,'FinishedLength', operator.get_part_length(assembly))
        self.debug_xml.add_element_with_text(elm_part,'Thickness',operator.distance(utils.get_part_thickness(obj)))
        self.debug_xml.add_element_with_text(elm_part,'FinishedThickness', operator.distance(utils.get_part_thickness(obj)))
        self.debug_xml.add_element_with_text(elm_part,'Routing', "SK1")#Str literal okay
        self.debug_xml.add_element_with_text(elm_part,'Class', "make")#Str literal okay
        self.debug_xml.add_element_with_text(elm_part,'Type', "panel")#"panel" for part "unknown" for solid stock

        elm_unit = self.debug_xml.add_element(elm_part,'Unit')
        self.debug_xml.add_element_with_text(elm_unit,'Name', "dimension")#Str literal okay
        self.debug_xml.add_element_with_text(elm_unit,'Measure', "inch")#Str literal okay
        self.debug_xml.add_element_with_text(elm_unit,'RoundFactor', "0")#Str literal okay        

        #MFG NODE
        elm_mfg = self.debug_xml.add_element(elm_job, 'Manufacturing', {'ID': "IDMFG-1", })
        elm_or = self.debug_xml.add_element(elm_mfg, 'Orientation', {'ID': "IDMOR-1", })        

        #Write Orientation TODO determine mirror_x and rotation angle
        self.debug_xml.add_element_with_text(elm_or, "Mirror", "none")#TODO determine mirror_x or none
        self.debug_xml.add_element_with_text(elm_or, "Rotation", "0")#TODO determine rotation angle

        #OPERATION GROUP
        elm_op = self.debug_xml.add_element(elm_mfg,
                                        'OperationGroups',
                                        {'ID': "IDOP-1",
                                        'MfgOrientationID': "IDMOR-1"
                                        })

        segment_coords = [op_grp[1], op_grp[2], op_grp[3], op_grp[4]]
        
        #Segments
        operator.add_panel_segment(elm_op, segment_coords)

        #Circles
        circles = op_grp[5]

        if len(circles) > 0:
            for circle in circles:
                operator.add_panel_circle(elm_op, circle)

        #LABEL
        elm_label = self.debug_xml.add_element(elm_mfg,
                                        'Label',
                                        {'ID': "IDL-1",
                                        'JobID': "IDJ-1",
                                        'PartID': "IDP-1"})

        for idx, item in enumerate(lbl):
            if idx > 0:
                operator.add_label_item(elm_label, item)                    


        #MATERIAL NODE
        elm_material = self.debug_xml.add_element(elm_job, 'Material', {'ID': "IDM-1", })

        self.debug_xml.add_element_with_text(elm_material, 'Name', "material_name")
        self.debug_xml.add_element_with_text(elm_material, 'Type', "sheet")
        self.debug_xml.add_element_with_text(elm_material, 'SKU', "SKU")

        self.debug_xml.write(debug_dir)