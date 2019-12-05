import bpy
import os
from mv import unit, utils, fd_types
import xml.etree.ElementTree as ET

class Snap_XML():
    
    tree = None
    xsi =  "http://www.w3.org/2001/XMLSchema-instance"
    xsd =  "http://www.cadcode.com/wsxml.xsd"
    ns = {"xmlns:xsi": xsi, "xsi:noNamespaceSchemaLocation": xsd}
    filename = "snap_job.xml"

    existing_items = []
    existing_assemblies = []
    existing_parts = []
    existing_labels = []
    existing_mats = []
    existing_ops = []
    existing_ors = []

    item_count = 0
    assembly_count = 0
    part_count = 0
    label_count = 0
    mat_count = 0
    op_count = 0
    or_count = 0    

    def __init__(self):
        #Check if XML already exists
        proj_props = bpy.context.window_manager.fd_project
        proj_name = proj_props.projects[proj_props.project_index].name
        path = os.path.join(os.path.dirname(bpy.utils.user_resource('DATAFILES')), "projects", proj_name, Snap_XML.filename)

        if os.path.exists(path):
            self.tree = ET.parse(path)
            self.root = self.tree.getroot().find("Job")

        else:
            attrib = dict([ (k, v) for k, v in self.ns.items() ])
            self.root = ET.Element('Batch', attrib)
            self.tree = ET.ElementTree(self.root)

    def set_counts(self):
        #Collect
        for item in self.root.findall("Item"):
            self.existing_items.append(item)

            for part in item.findall("Part"):
                self.existing_parts.append(part)

            for assembly in item.findall("Assembly"):
                self.existing_assemblies.append(assembly)

                for part in assembly.findall("Part"):
                    self.existing_parts.append(part)

                for assembly in assembly.findall("Assembly"):
                    self.existing_assemblies.append(assembly)

                    for part in assembly.findall("Part"):
                        self.existing_parts.append(part)

        mfg = self.root.find("Manufacturing")

        for orientation in mfg.findall("Orientation"):
            self.existing_ors.append(orientation)

        for op_grp in mfg.findall("OperationGroups"):
            self.existing_ops.append(op_grp)

        for label in mfg.findall("Label"):
            self.existing_labels.append(label)            

        for mat in self.root.findall("Material"):
            self.existing_mats.append(mat)

        #Set counts
        for item in self.existing_items:
            item_num = item.attrib.get('ID')
            _ , num = item_num.split('-')
            int_num = int(num)

            if int_num > self.item_count:
                self.item_count = int_num
            elif int_num == self.item_count:
                self.item_count = int_num + 1

        for assembly in self.existing_assemblies:
            assembly_num = assembly.attrib.get('ID')
            _ , num = assembly_num.split('-')
            int_num = int(num)

            if int_num > self.assembly_count:
                self.assembly_count = int_num
            elif int_num == self.assembly_count:
                self.assembly_count = int_num + 1                

        for part in self.existing_parts:
            part_num = part.attrib.get('ID')
            _ , num = part_num.split('-')
            int_num = int(num)

            if int_num > self.part_count:
                self.part_count = int_num
            elif int_num == self.part_count:
                self.part_count = int_num + 1                

        for label in self.existing_labels:
            label_num = label.attrib.get('ID')
            _ , num = label_num.split('-')
            int_num = int(num)

            if int_num > self.label_count:
                self.label_count = int_num
            elif int_num == self.label_count:
                self.label_count = int_num + 1                
                
        for mat in self.existing_mats:
            mat_num = mat.attrib.get('ID')
            _ , num = mat_num.split('-')
            int_num = int(num)

            if int_num > self.mat_count:
                self.mat_count = int_num
            elif int_num == self.mat_count:
                self.mat_count = int_num + 1                

        for op in self.existing_ops:
            op_num = op.attrib.get('ID')
            _ , num = op_num.split('-')
            int_num = int(num)

            if int_num > self.op_count:
                self.op_count = int_num
            elif int_num == self.op_count:
                self.op_count = int_num + 1                  

        for orientation in self.existing_ors:
            or_num = orientation.attrib.get('ID')
            _ , num = or_num.split('-')
            int_num = int(num)

            if int_num > self.or_count:
                self.or_count = int_num
            elif int_num == self.or_count:
                self.or_count = int_num + 1                 

    def add_element(self, root, elm_name, attrib=None):
        if not attrib:
            elm = ET.Element(elm_name)
        else:
            elm = ET.Element(elm_name, attrib)
        root.append(elm)
        return elm
    
    def add_element_with_text(self,root,elm_name,text):
        field = ET.Element(elm_name)
        field.text = text
        root.append(field)
    
    def insert_element(self, idx, root, elm_name, attrib=None):
        if not attrib:
            elm = ET.Element(elm_name)
        else:
            elm = ET.Element(elm_name, attrib)
        root.insert(idx, elm)
        return elm

    def format_xml_file(self,path):
        """ This makes the xml file readable as a txt doc.
            For some reason the xml.toprettyxml() function
            adds extra blank lines. This makes the xml file
            unreadable. This function just removes
            all of the blank lines.
            arg1: path to xml file
        """
        from xml.dom.minidom import parse
        

        print("parse path: ", path)
        xml = parse(path)
        pretty_xml = xml.toprettyxml()
        
        file = open(path,'w')
        file.write(pretty_xml)
        file.close()
        
        cleaned_lines = []
        with open(path,"r") as f:
            lines = f.readlines()
            for l in lines:
                l.strip()
                if "<" in l:
                    cleaned_lines.append(l)
            
        with open (path,"w") as f:
            f.writelines(cleaned_lines)
    
    def write(self, dir):
        proj_props = bpy.context.window_manager.fd_project
        proj_name = proj_props.projects[proj_props.project_index].name
        path = os.path.join(dir, self.filename)

        with open(path, 'w',encoding='utf-8') as file:
            self.tree.write(file,encoding='unicode')            
            
        #self.format_xml_file(path)