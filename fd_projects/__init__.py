# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Project Manager",
    "author": "Ryan Montes",
    "version": (1, 2, 0),
    "blender": (2, 7, 8),
    "location": "Tools Shelf",
    "description": "Project management tools",
    "warning": "",
    "wiki_url": "",
    "category": "SNaP"
}

import bpy
from mv import fd_types, utils, unit
import os
import shutil
import re
import pathlib
from distutils.dir_util import copy_tree
import xml.etree.ElementTree as ET
import subprocess
from bpy.types import PropertyGroup, UIList, Panel, Operator, AddonPreferences
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       BoolVectorProperty,
                       PointerProperty,
                       CollectionProperty,
                       EnumProperty)


def get_project_dir():
    project_dir = bpy.context.user_preferences.addons[__name__.split(".")[1]].preferences.project_dir

    if not os.path.exists(project_dir):
        os.makedirs(project_dir)

    return project_dir                       


def check_project_path():
    print("checking project path...")

    path = bpy.context.scene.project_info.project_path

    if os.path.exists(path):
        print("path exists")

    else:
        print("path DOES NOT exist")


def load_project_info():
    print("Loading project info...")

def reload_projects():
    if 'fd_projects' in bpy.context.user_preferences.addons.keys():
        wm = bpy.context.window_manager.fd_project
        proj_dir = bpy.context.user_preferences.addons['fd_projects'].preferences.project_dir

        if os.path.exists(proj_dir):
            for root, dirs, files in os.walk(proj_dir):
                for dir in dirs:
                    for root, dirs, files in os.walk(os.path.join(proj_dir, dir)):
                        for file in files:
                            fname, ext = file.split(".")
                            if ext == "ccp":
                                tree = ET.parse(os.path.join(proj_dir, dir, file))
                                root = tree.getroot()

                                for elm in root.findall("ProjectInfo"):
                                    items = list(elm)

                                    for item in items:
                                        if item.tag == 'name':
                                            proj_name = item.text
                                
                                proj = wm.projects.add()
                                proj.init(proj_name)

                                for elm in root.findall("Rooms"):
                                    for sub_elm in elm:
                                        #print("Category: ", sub_elm.get("category"))
                                        #print("Path: ", sub_elm.get("path"))
                                        proj.add_room_from_file(sub_elm.get("name"), sub_elm.get("category"), sub_elm.get("path"))

def make_new_name(path, category, new_name):
    return path + "\\" + category + "_" + new_name + ".blend"

def rename_room_callback(self, context):
    if self.file_path:
        curr_opnd_file = bpy.data.filepath
        has_opnd_file = curr_opnd_file != ""
        if not has_opnd_file:
            return
        new_room_name = self.name
        ccp_file = ""
        old_bl_path = str(self.file_path)
        new_bl_path = ""
        projs = context.window_manager.fd_project.projects
        for proj in projs:
            for room in proj.rooms:
                ccp_file = str(proj.file_path)
                if room.file_path == self.file_path and ccp_file != "":
                    xml_tree = ET.parse(ccp_file)
                    xml_root = xml_tree.getroot()
                    for element in xml_root.findall('Rooms'):
                        for element_room in element.getchildren():
                            if element_room.attrib["path"] == old_bl_path:
                                old_room = element_room.attrib["name"]
                                category = element_room.attrib["category"]
                                renaming = old_room != new_room_name
                                is_opnd_room = old_room in curr_opnd_file
                                if renaming and is_opnd_room:
                                    element_room.attrib["name"] = new_room_name
                                    element_room.text = new_room_name
                                    new_bl_path = make_new_name(
                                        proj.dir_path, category, new_room_name
                                    )
                                    bpy.ops.wm.save_as_mainfile(
                                        filepath = new_bl_path)
                                    element_room.attrib["path"] = new_bl_path
                                    xml_tree.write(ccp_file)
                                    bpy.ops.project.open_room( 
                                        file_path = new_bl_path)
                                    os.remove(old_bl_path)
    return

class CCP():
    
    filename = ""
    ext = ".ccp"
    tree = None
    
    def __init__(self):
        pass
    
    def create_tree(self):
        root = ET.Element('Root',{'Application':'Classy Designer','ApplicationVersion':'1.0'})
        self.tree = ET.ElementTree(root)
        return root
    
    def add_element(self,root,elm_name,attrib_name=""):
        if attrib_name == "":
            elm = ET.Element(elm_name)
        else:
            elm = ET.Element(elm_name,{'Name':attrib_name})
        root.append(elm)
        return elm
    
    def add_element_with_text(self,root,elm_name,text):
        field = ET.Element(elm_name)
        field.text = text
        root.append(field)
    
    def format_xml_file(self,path):
        """ This makes the xml file readable as a txt doc.
            For some reason the xml.toprettyxml() function
            adds extra blank lines. This makes the xml file
            unreadable. This function just removes
            all of the blank lines.
            arg1: path to xml file
        """
        from xml.dom.minidom import parse
        
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
    
    def write(self, path):
        path = os.path.join(path, self.filename + self.ext)
        
        with open(path, 'w',encoding='utf-8') as file:
            self.tree.write(file,encoding='unicode')
            
        self.format_xml_file(path)


class UL_Projects(UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text="",icon='FILE_SCRIPT')
        layout.label(text=item.name)
        layout.operator("project.delete_project", text="", icon='X', emboss=True).index = index
        #print(index)


class UL_Rooms(UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        path = item.file_path

        layout.label(text="",icon='SNAP_PEEL_OBJECT')
        layout.prop(item, 'name', text='', emboss=False)
        layout.prop(item, "selected", text="")
        layout.operator("project.delete_room", text="", icon='X', emboss=True).index = index


def clean_name(name):
    illegal = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    
    for i in illegal:
        if i in name:
            name = name.replace(i, '')

    return name


def unique_col_name(col, name):
    unique_names = []


def set_name_unique(op, name, value):
    unique_names = ['name']

    if value == "":
        value = "New Project"

    def collection_from_element(op):
        path = op.path_from_id()
        match = re.match(r'(.*)\[\d*\]', path)
        parent = op.id_data
        try:
            coll_path = match.group(1)
        except AttributeError:
            raise TypeError("Propery not element in a collection.") 
        else:
            return parent.path_resolve(coll_path)

    def new_val(stem, nbr):
        return '{st}.{nbr:03d}'.format(st=stem, nbr=int(nbr))

    if name not in unique_names:
        op[name] = value
        return
    if value == getattr(op, name):
        return

    coll = collection_from_element(op)
    if value not in coll:
        op[name] = value
        return

    match = re.match(r'(.*)\.(\d{3,})', value)

    if match is None:
        stem, nbr = value, 1
    else:
        stem, nbr = match.groups()

    nbr_int = int(nbr)    
    new_value = new_val(stem, nbr_int)

    while new_value in coll:
        nbr_int += 1
        new_value = new_val(stem, nbr_int)

    op[name] = new_value


class CollectionMixIn:
    name = bpy.props.StringProperty(name="Project Name", default="", update=rename_room_callback)
    dir_path = bpy.props.StringProperty(name="Directory Path", default="", subtype='DIR_PATH')

    def init(self, col, name=""):
        self.set_unique_name(col, name)
        self.dir_path = os.path.join(get_project_dir(), self.get_clean_name(self.name))

    def format_name(self, stem, nbr):
        return '{st}.{nbr:03d}'.format(st=stem, nbr=int(nbr))

    def get_clean_name(self, name):
        illegal = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '.']
        
        for i in illegal:
            if i in name:
                if i == '.':
                    name = name.replace('.', '_')
                else:
                    name = name.replace(i, '')

        return name

    def set_unique_name(self, col, name):
        if name == "":
            name = "New Project"
            return

        existing_names = []

        for i in col.items():
            existing_names.append(i[0])

        if name not in existing_names:
            self.name = name
            return

        #If name already exists in collection
        match = re.match(r'(.*)\.(\d{3,})', name)

        if match is None:
            stem, nbr = name, 1
        else:
            stem, nbr = match.groups()

        nbr_int = int(nbr)    
        new_name = self.format_name(stem, nbr_int)

        while new_name in col:
            nbr_int += 1
            new_name = self.format_name(stem, nbr_int)

        self.name = new_name            


class Room(bpy.types.PropertyGroup, CollectionMixIn):
    file_path = bpy.props.StringProperty(name="Room Filepath", default="", subtype='FILE_PATH')
    selected = bpy.props.BoolProperty(name="Room Selected",default=False)

    def init(self, name, category, path=None):
        wm = bpy.context.window_manager.fd_project
        col = wm.projects[wm.project_index].rooms
        super().init(col, name=name)

        #Set file name
        self.file_name = self.get_clean_name(category + "_" + self.name)

        if path:
            self.file_path = path

        else:
            #Set filepath
            proj_filepath = wm.projects[wm.project_index].file_path
            self.file_path = os.path.join(os.path.dirname(proj_filepath), '{}.{}'.format(self.file_name, "blend"))

            #Save file to project dir
            bpy.ops.wm.save_as_mainfile(filepath=self.file_path)

            #write info to project file
            tree = ET.parse(proj_filepath)
            root = tree.getroot()

            for elm in root.findall("Rooms"):
                elm_room = ET.Element("Room", {'name': self.name,'category' : category, 'path': self.file_path})
                elm_room.text = self.name
                elm.append(elm_room)

            tree.write(proj_filepath)

    def set_filename(self):
        self.file_name = self.get_clean_name(self.name)

    def set_filepath(self):
        wm = bpy.context.window_manager.fd_project
        proj_filepath = wm.projects[wm.project_index].file_path
        self.file_path = os.path.join(os.path.dirname(proj_filepath), '{}.{}'.format(self.file_name, "blend"))        

bpy.utils.register_class(Room)
        

def update_project_props(self, context):
    self.modify_project_file()

class Project(bpy.types.PropertyGroup, CollectionMixIn):
    file_path = bpy.props.StringProperty(name="Project File Path", default="", subtype='FILE_PATH')
    rooms = CollectionProperty(name="Rooms", type=Room)
    room_index = IntProperty(name="Room Index")

    project_id = bpy.props.IntProperty(name="Project ID", description="Project ID")      
    customer_name = bpy.props.StringProperty(name="Customer Name", description="Customer Name", update=update_project_props)
    client_id = bpy.props.StringProperty(name="Client ID", description="Client ID", update=update_project_props)
    project_address = bpy.props.StringProperty(name="Project Address", description="Project Address", update=update_project_props)
    city = bpy.props.StringProperty(name="City", description="City", update=update_project_props)
    state = bpy.props.StringProperty(name="State", description="State", update=update_project_props)
    zip_code = bpy.props.StringProperty(name="Zip Code", description="Zip Code", update=update_project_props)
    customer_phone_1 = bpy.props.StringProperty(name="Customer Phone 1", description="Customer Phone 1", update=update_project_props)
    customer_phone_2 = bpy.props.StringProperty(name="Customer Phone 2", description="Customer Phone 2", update=update_project_props)
    customer_email = bpy.props.StringProperty(name="Customer Email", description="Customer Email", update=update_project_props)
    project_notes = bpy.props.StringProperty(name="Project Notes", description="Project Notes", update=update_project_props)
    designer = bpy.props.StringProperty(name="Designer", description="Designer", update=update_project_props)
    design_date = bpy.props.StringProperty(name="Design Date", description="Design Date", update=update_project_props)

    main_tabs = bpy.props.EnumProperty(name="Main Tabs",
                                       items=[('INFO',"Info",'Show the project information.'),
                                              ('ROOMS',"Rooms",'Show rooms associated with the current project.')],
                                       default = 'INFO')

    def init(self, name, path=None):
        if bpy.app.background:
            return

        col = bpy.context.window_manager.fd_project.projects
        super().init(col, name=name)
        self.create_dir()
        self.set_filename()
        self.set_filepath()

        #File path passed in
        if path:
            self.read_project_file()
        #File already exists in project directory
        elif os.path.exists(os.path.join(self.dir_path, self.file_name + ".ccp")):
            self.read_project_file()
        else:
            project_id = self.get_id()
            self.project_id = project_id
            self.create_file(project_id)
            
    def create_dir(self):
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)

    def set_filename(self):
        self.file_name = self.get_clean_name(self.name)

    def set_filepath(self):
        self.file_path = os.path.join(self.dir_path, '{}.{}'.format(self.file_name, "ccp"))

    def get_id(self):
        addon_prefs = bpy.context.user_preferences.addons[__name__.split(".")[1]].preferences
        addon_prefs.project_id_count += 1
        bpy.ops.wm.save_userpref()

        return addon_prefs.project_id_count        

    def create_file(self, project_id):
        ccp = CCP()
        ccp.filename = self.file_name
        root = ccp.create_tree()
        project_info = ccp.add_element(root,'ProjectInfo')

        ccp.add_element_with_text(project_info, "project_id", str(project_id))
        ccp.add_element_with_text(project_info, "name", self.name)
        ccp.add_element_with_text(project_info, "customer_name", "None")
        ccp.add_element_with_text(project_info, "client_id", "None")
        ccp.add_element_with_text(project_info, "project_address", "None")
        ccp.add_element_with_text(project_info, "city", "None")
        ccp.add_element_with_text(project_info, "state", "None")
        ccp.add_element_with_text(project_info, "zip_code", "None")
        ccp.add_element_with_text(project_info, "customer_phone_1", "None")
        ccp.add_element_with_text(project_info, "customer_phone_2", "None")
        ccp.add_element_with_text(project_info, "customer_email", "None")
        ccp.add_element_with_text(project_info, "project_notes", "None")
        ccp.add_element_with_text(project_info, "designer", "None")
        ccp.add_element_with_text(project_info, "design_date", "None")

        ccp.add_element(root, 'Rooms')

        ccp.write(self.dir_path)

    def modify_project_file(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        for elm in root.findall("ProjectInfo"):
            items = elm.getchildren()

            for item in items:
                if item.tag == 'customer_name':
                    item.text = self.customer_name

                if item.tag == 'client_id':
                    item.text = self.client_id
                    
                if item.tag == 'project_address':
                    item.text = self.project_address
                
                if item.tag == 'city':
                    item.text = self.city
                
                if item.tag == 'state':
                    item.text = self.state
                
                if item.tag == 'zip_code':
                    item.text = self.zip_code

                if item.tag == 'customer_phone_1':
                    item.text = self.customer_phone_1

                if item.tag == 'customer_phone_2':
                    item.text = self.customer_phone_2

                if item.tag == 'customer_email':
                    item.text = self.customer_email                    

                if item.tag == 'project_notes':
                    item.text = self.project_notes                    

                if item.tag == 'designer':
                    item.text = self.designer

                if item.tag == 'design_date':
                    item.text = self.design_date
        
        tree.write(self.file_path)

    def read_project_file(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        for elm in root.findall("ProjectInfo"):
            items = elm.getchildren()

            for item in items:
                if item.text:
                    
                    if item.tag == 'project_id':
                        self.project_id = int(item.text)

                    if item.tag == 'customer_name':
                        self.customer_name = item.text

                    if item.tag == 'client_id':
                        self.client_id = item.text
                        
                    if item.tag == 'project_address':
                        self.project_address = item.text

                    if item.tag == 'city':
                        self.city = item.text
                    
                    if item.tag == 'state':
                        self.state = item.text

                    if item.tag == 'zip_code':
                        self.zip_code = item.text

                    if item.tag == 'customer_phone_1':
                        self.customer_phone_1 = item.text

                    if item.tag == 'customer_phone_2':
                        self.customer_phone_2 = item.text

                    if item.tag == 'customer_email':
                        self.customer_email = item.text                    

                    if item.tag == 'project_notes':
                        self.project_notes = item.text                    

                    if item.tag == 'designer':
                        self.designer = item.text

                    if item.tag == 'design_date':
                        self.design_date = item.text

    def draw_project_info(self, layout):
        box = layout.box()
        col = box.column()

        col.prop(self, 'customer_name')
        col.prop(self, 'client_id')
        col.prop(self, 'project_address')
        col.prop(self, 'city')
        col.prop(self, 'state')
        col.prop(self, 'zip_code')
        col.prop(self, 'customer_phone_1')
        col.prop(self, 'customer_phone_2')
        col.prop(self, 'customer_email')
        col.prop(self, 'project_notes')
        col.prop(self, 'designer')
        col.prop(self, 'design_date')

    def draw_room_info(self, box):
        row = box.row(align=True)
        row.operator("project.prepare_proj_xml",text="Export Selected Rooms",icon='EXPORT')
        row.menu('MENU_Room_Selection',text="",icon='DOWNARROW_HLT')

        if len(self.rooms) > 0:
            active_room_path = self.rooms[self.room_index].file_path
            col = box.column(align=True)
            col.template_list("UL_Rooms", "", self, "rooms", self, "room_index", maxrows=5)
            col.operator("project.open_room", text="Open Room", icon='LIBRARY_DATA_DIRECT').file_path = active_room_path
        else:
            lbl_box = box.box()
            lbl_box.label(text="There are no rooms in this project", icon='ERROR')

    def draw_render_info(self, layout):
        box = layout.box()
        box.label("RENDERS HERE")

    def draw(self, layout):
        box = layout.box()
        row = box.row()
        row.prop(self, 'main_tabs', expand=True)    
        
        if self.main_tabs == 'INFO':
            self.draw_project_info(box)
            
        if self.main_tabs == 'ROOMS':
            self.draw_room_info(box)

    def add_room(self, name, category):
        room = self.rooms.add()
        room.init(name, category)

    def add_room_from_file(self, name, category, path):
        room = self.rooms.add()
        #if("_" in name):
        #    room_category,room_name = name.split("_")
        #else:
        #    room_category = "Please Select"
        #    room_name = name
        room.init(name, category, path)

bpy.utils.register_class(Project)


class MENU_Project_Tools(bpy.types.Menu):
    bl_label = "Project Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator("fd_general.open_browser_window", text="Open Projects Location in Browser", icon='FILE_FOLDER').path = get_project_dir()

class MENU_Room_Selection(bpy.types.Menu):
    bl_label = "Select Rooms"

    def draw(self, context):
        layout = self.layout
        layout.operator("project.select_all_rooms",text="Select All",icon='CHECKBOX_HLT').select_all = True
        layout.operator("project.select_all_rooms",text="Deselect All",icon='CHECKBOX_DEHLT').select_all = False

        
def update_room_index(self, context): 
    print("event for changing of room index")
 

class WM_PROPERTIES_Projects(bpy.types.PropertyGroup):
    projects = CollectionProperty(name="Projects", type=Project)
    project_index = IntProperty(name="Project Index")
    project_path = StringProperty(name="Project Path", description="Project file path", subtype='FILE_PATH')

    def get_project(self):
        return self.projects[self.project_index]


class PANEL_Project_Info(bpy.types.Panel):
    bl_idname = "project.Project_Info"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "Projects"
    bl_category = "SNaP"
    
    props = None
    
    def draw_header(self, context):
        layout = self.layout
        layout.label('',icon='INFO')

    def draw_common_ops(self, box):
        row = box.row(align=True)
        row.operator("project.create_project", text="Create Project", icon='NEW')
        row.operator("project.import_project", text="Open Project", icon='FILE_FOLDER') 
        row.menu('MENU_Project_Tools', text="", icon='DOWNARROW_HLT')       

    def draw(self, context):
        wm = bpy.context.window_manager.fd_project
        projects = wm.projects
        layout = self.layout
        box = layout.box()

        if len(projects) > 0:
            if(len(projects) < 5):
                box.template_list("UL_Projects", "", wm, "projects", wm, "project_index", rows=len(projects))
                self.draw_common_ops(box)
                active_project = wm.projects[wm.project_index]
                active_project.draw(box)
            else:
                box.template_list("UL_Projects", "", wm, "projects", wm, "project_index", maxrows=5)
                self.draw_common_ops(box)
                active_project = wm.projects[wm.project_index]
                active_project.draw(box)
        else:
            self.draw_common_ops(box)
        


class OPERATOR_Create_Project(bpy.types.Operator):
    """ This will create a project.
    """    
    bl_idname = "project.create_project"
    bl_label = "Create Project"
    bl_description = "Creates a project"

    project_name = bpy.props.StringProperty(name="Project Name", description="Project Name", default="New Project")

    def listdir(self, path):
        return [d for d in os.listdir(path) if os.path.isdir(d)]

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(400))

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        col = box.column(align=True)
        row = col.row()
        row.label("Project Name:")
        row.prop(self, "project_name", text="")        

    def execute(self, context):
        wm = context.window_manager.fd_project

        if self.project_name == "":
            return {'FINISHED'}

        proj = wm.projects.add()
        proj.init(self.project_name)
    
        return {'FINISHED'}


class OPERATOR_Import_Project(bpy.types.Operator):
    """ This will import a project.
    """    
    bl_idname = "project.import_project"
    bl_label = "Import Project"
    bl_description = "Imports a project"

    filename = bpy.props.StringProperty(name="Project File Name", description="Project file name to import")
    filepath = bpy.props.StringProperty(name="Project Path", description="Project path to import", subtype="FILE_PATH")
    directory =  bpy.props.StringProperty(name="Project File Directory Name", description="Project file directory name")

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}    

    def execute(self, context):
        wm = context.window_manager.fd_project

        if pathlib.Path(self.filename).suffix == ".ccp":
            copy_tree(self.directory, os.path.join(get_project_dir(), self.filename.split('.')[0]))
            reload_projects()

        return {'FINISHED'}


class OPERATOR_Delete_Project(Operator):
    bl_idname = "project.delete_project"
    bl_label = "Delete Project" 
    bl_options = {'UNDO'}

    index = bpy.props.IntProperty(name="Project Index")

    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)

    def draw(self,context):
        layout = self.layout
        box = layout.box()
        col = box.column()

        props = context.window_manager.fd_project
        proj = props.projects[self.index]

        col.label("'{}'".format(proj.name))        
        col.label("Are you sure you want to delete this project?")      

    def execute(self, context):
        props = context.window_manager.fd_project
        proj = props.projects[self.index]
        proj_filepath = props.projects[self.index].file_path
        proj.proj_dir = os.path.join(get_project_dir(), proj.name)
        rbin_path = os.path.join(os.path.expanduser("~"), "Documents", "SNaP Projects Recycle Bin")
        rbin_proj_path = os.path.join(rbin_path, proj.name)
        props.projects.remove(self.index)
        props.project_index = 0

        if os.path.exists(rbin_proj_path):
            shutil.rmtree(rbin_proj_path)

        if not os.path.exists(rbin_path):  
            os.mkdir(rbin_path)

        shutil.move(proj.proj_dir, rbin_path)

        return {'FINISHED'}


class OPERATOR_Add_Room(bpy.types.Operator):
    """ This will add a room to the active project.
    """    
    bl_idname = "project.add_room"
    bl_label = "Add Room"
    bl_description = "Adds a room to the active project"

    room_name = bpy.props.StringProperty(name="Room Name", description="Room Name")
    room_category = EnumProperty(name="Room Category",
                                description="Select the Category of the Room",
                                items=[("Please Select","REQUIRED Please Select a Category","Please Select a Category"),
                                       ("41110","Closet","Closet"),
                                       ("41120","Entertainment Center","Entertainment Center"),
                                       ("41130","Garage","Garage"),
                                       ("41140","Home Office","Home Office"),
                                       ("41150","Laundry","Laundry"),
                                       ("41160","Mud Room","Mud Room"),
                                       ("41170","Pantry","Pantry"),
                                       ("41210","Kitchen","Kitchen"),
                                       ("41220","Bathroom","Bathroom"),
                                       ("41230","Reface","Reface"),
                                       ("41240","Remodel","Remodel"),
                                       ("41250","Stone","Stone")]) 
    def execute(self, context):
        props = context.window_manager.fd_project

        if len(props.projects) > 0:
            project = props.projects[props.project_index]
            room = project.add_room(self.room_name, self.room_category)
            project.main_tabs = 'ROOMS'       

        return {'FINISHED'}


class OPERATOR_Open_Room(bpy.types.Operator):
    """ This will open room .blend file.
    """    
    bl_idname = "project.open_room"
    bl_label = "Open Room"
    bl_description = "Opens a room file"

    file_path = bpy.props.StringProperty(name="File Path", description="Room File Path", subtype="FILE_PATH")

    def execute(self, context):
        props = context.window_manager.fd_project

        if len(props.projects) > 0:
            project = props.projects[props.project_index]

        proj_name, _ = os.path.basename(project.file_path).split('.')
        room_path = os.path.join(get_project_dir(), proj_name, os.path.basename(self.file_path))
        bpy.ops.wm.open_mainfile(filepath=room_path)

        return {'FINISHED'}


class OPERATOR_Delete_Room(Operator):
    bl_idname = "project.delete_room"
    bl_label = "Delete Room" 
    bl_options = {'UNDO'}

    room_name = bpy.props.StringProperty(name="Room Name", description="Room Name")
    index = bpy.props.IntProperty(name="Project Index")


    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)

    def draw(self,context):
        layout = self.layout
        box = layout.box()
        col = box.column()

        props = context.window_manager.fd_project
        proj = props.projects[props.project_index]
        room = proj.rooms[self.index]

        col.label("'{}'".format(room.name))        
        col.label("Are you sure you want to delete this room?")  

    def execute(self, context):
        props = context.window_manager.fd_project
        proj = props.projects[props.project_index]
        room = proj.rooms[self.index]
        self.room_name = room.name

        proj.rooms.remove(self.index)

        tree = ET.parse(proj.file_path)
        root = tree.getroot()

        for elm in root.findall("Rooms"):
            items = elm.getchildren()

            for item in items:
                if item.get("name") == self.room_name:
                    room_filepath = item.get("path")
                    elm.remove(item)

        tree.write(proj.file_path)

        #ToDo: install send2trash to interpreter to use here instead
        os.remove(room_filepath)
        proj.room_index = 0

        return {'FINISHED'}        


class OPERATOR_select_all_rooms(Operator):   
    bl_idname = "project.select_all_rooms"
    bl_label = "Select All Rooms"
    bl_description = "This will select all of the rooms in the project"
    
    select_all = BoolProperty(name="Select All",default=True)
    
    @classmethod
    def poll(cls, context):
        return True

    def execute(self,context):
        props = context.window_manager.fd_project
        proj = props.projects[props.project_index]

        for room in proj.rooms:
            room.selected = self.select_all
            
        return{'FINISHED'}


class OPERATOR_Prepare_Project_XML(Operator):
    """ This creates the project XML, collecting and writing information from each room (.blend) file in the project.
    """       
    bl_idname = "project.prepare_proj_xml"
    bl_label = "Create Project XML" 
    bl_options = {'UNDO'}

    tmp_filename = "export_temp.py"
    xml_filename = "snap_job.xml"
    proj_dir = bpy.props.StringProperty(name="Project Directory", subtype='DIR_PATH')

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=300)

    def draw(self, context):
        props = context.window_manager.fd_project
        proj = props.get_project()
        box = self.layout.box()
        box.label("Project:  {}".format(proj.name))

    def create_prep_script(self):
        nrm_dir = self.proj_dir.replace("\\", "/")
        file = open(os.path.join(bpy.app.tempdir, self.tmp_filename),'w')
        file.write("import bpy\n")
        file.write("bpy.ops.snap_db.export_xml('INVOKE_DEFAULT', xml_path='{}')\n".format(nrm_dir))
        file.close()
        
        return os.path.join(bpy.app.tempdir, self.tmp_filename)    
    
    def execute(self,context):
        proj_props = bpy.context.window_manager.fd_project
        proj_name = proj_props.projects[proj_props.project_index].name
        path = os.path.join(get_project_dir(), proj_name, self.xml_filename)
        proj = proj_props.projects[proj_props.project_index]        

        if os.path.exists(path):
            os.remove(path)

        self.proj_dir = os.path.join(get_project_dir(), proj_name)
        script_path = self.create_prep_script()

        #Call blender in background and run XML export on each room file in project
        for room in proj.rooms:
            if room.selected:
                subprocess.call(bpy.app.binary_path + ' "' + room.file_path + '" -b --python "' + script_path + '"')

        return{'FINISHED'}


def register():
    bpy.utils.register_class(WM_PROPERTIES_Projects)
    bpy.types.WindowManager.fd_project = bpy.props.PointerProperty(type=WM_PROPERTIES_Projects)
    bpy.utils.register_class(UL_Projects)
    bpy.utils.register_class(UL_Rooms)
    bpy.utils.register_class(MENU_Project_Tools)
    bpy.utils.register_class(MENU_Room_Selection)
    bpy.utils.register_class(PANEL_Project_Info)
    bpy.utils.register_class(OPERATOR_Create_Project)
    bpy.utils.register_class(OPERATOR_Import_Project)
    bpy.utils.register_class(OPERATOR_Delete_Project)
    bpy.utils.register_class(OPERATOR_Add_Room)
    bpy.utils.register_class(OPERATOR_Open_Room)
    bpy.utils.register_class(OPERATOR_Delete_Room)
    bpy.utils.register_class(OPERATOR_select_all_rooms)
    bpy.utils.register_class(OPERATOR_Prepare_Project_XML)

    addon_prefs = bpy.context.user_preferences.addons[__name__.split(".")[1]].preferences

    if not os.path.exists(addon_prefs.project_dir):
        os.makedirs(addon_prefs.project_dir)
    

def unregister():
    bpy.utils.unregister_class(WM_PROPERTIES_Projects)
    del bpy.types.WindowManager.fd_project
    bpy.utils.unregister_class(UL_Projects)
    bpy.utils.unregister_class(UL_Rooms)
    bpy.utils.unregister_class(MENU_Project_Tools)
    bpy.utils.unregister_class(MENU_Room_Selection)
    bpy.utils.unregister_class(PANEL_Project_Info)
    bpy.utils.unregister_class(OPERATOR_Create_Project)
    bpy.utils.unregister_class(OPERATOR_Import_Project)
    bpy.utils.unregister_class(OPERATOR_Delete_Project)
    bpy.utils.unregister_class(OPERATOR_Add_Room)
    bpy.utils.unregister_class(OPERATOR_Open_Room)
    bpy.utils.unregister_class(OPERATOR_Delete_Room)
    bpy.utils.unregister_class(OPERATOR_select_all_rooms)
    bpy.utils.unregister_class(OPERATOR_Prepare_Project_XML)

