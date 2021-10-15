import bpy
import os
import re
import xml.etree.ElementTree as ET
from bpy.types import UIList, PropertyGroup, Menu
from bpy.props import (StringProperty,
                       BoolProperty,
                       EnumProperty,
                       IntProperty,
                       CollectionProperty,
                       PointerProperty)
from . import pm_utils
from shutil import copyfile


def update_project_props(self, context):
    self.modify_project_file()


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

        props = bpy.context.window_manager.sn_project

        proj = props.projects[props.project_index]
        for room in proj.rooms:
            ccp_file = str(proj.file_path)
            if room.file_path == self.file_path and ccp_file != "":
                xml_tree = ET.parse(ccp_file)
                xml_root = xml_tree.getroot()
                for element in xml_root.findall('Rooms'):
                    for element_room in list(element):
                        if element_room.attrib["path"] == old_bl_path:
                            old_room = element_room.attrib["name"]
                            category = element_room.attrib["category"]
                            renaming = old_room != new_room_name
                            is_opnd_room = old_room in curr_opnd_file
                            if renaming:
                                element_room.attrib["name"] = new_room_name
                                element_room.text = new_room_name
                                new_bl_path = make_new_name(
                                    proj.dir_path, category, new_room_name
                                )
                                element_room.attrib["path"] = new_bl_path
                                xml_tree.write(ccp_file)
                                copyfile(old_bl_path, new_bl_path)
                                if is_opnd_room:
                                    bpy.ops.project_manager.open_room(file_path=new_bl_path)
                                else:
                                    room.file_path = new_bl_path

                                os.remove(old_bl_path)
                                return


class CollectionMixIn:
    name: StringProperty(name="Project Name", default="", update=rename_room_callback)
    dir_path: StringProperty(name="Directory Path", default="", subtype='DIR_PATH')

    def init(self, col, name=""):
        self.set_unique_name(col, name)
        self.dir_path = os.path.join(pm_utils.get_project_dir(), self.get_clean_name(self.name))

    def format_name(self, stem, nbr):
        return '{st}.{nbr:03d}'.format(st=stem, nbr=int(nbr))

    def get_clean_name(self, name):
        illegal = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']

        for i in illegal:
            if i in name:
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

        # If name already exists in collection
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


class Room(PropertyGroup, CollectionMixIn):
    file_path: StringProperty(name="Room Filepath", default="", subtype='FILE_PATH')
    selected: BoolProperty(name="Room Selected", default=False)

    def init(self, name, category, path=None, project_index=None):
        wm = bpy.context.window_manager.sn_project
        # On initial load, project index won't work.
        col = wm.projects[project_index or wm.project_index].rooms
        super().init(col, name=name)

        # Set file name
        self.file_name = self.get_clean_name(category + "_" + self.name)

        if path:
            self.file_path = path

        else:
            # Set filepath
            project = wm.projects[wm.project_index]
            proj_dir = os.path.join(project.dir_path, project.name)
            self.file_path = os.path.join(os.path.dirname(proj_dir), '{}.{}'.format(self.file_name, "blend"))

            # Save file to project dir
            bpy.ops.wm.save_as_mainfile(filepath=self.file_path)
            wm.current_file_project = project.name
            wm.current_file_room = self.name

            # write info to project file
            tree = ET.parse(project.file_path)
            root = tree.getroot()

            for elm in root.findall("Rooms"):
                # we want to save using relative path
                rel_loc = os.path.join(*self.file_path.split(os.sep)[-2:])
                elm_room = ET.Element("Room", {'name': self.name, 'category': category, 'path': rel_loc})
                elm_room.text = self.name
                elm.append(elm_room)

            tree.write(project.file_path)

    def set_filename(self):
        self.file_name = self.get_clean_name(self.name)

    def set_filepath(self):
        wm = bpy.context.window_manager.sn_project
        proj_filepath = wm.projects[wm.project_index].file_path
        self.file_path = os.path.join(os.path.dirname(proj_filepath), '{}.{}'.format(self.file_name, "blend"))


class Project(PropertyGroup, CollectionMixIn):
    file_path: StringProperty(name="Project File Path", default="", subtype='FILE_PATH')
    rooms: CollectionProperty(name="Rooms", type=Room)
    room_index: IntProperty(name="Room Index")

    project_id: IntProperty(name="Project ID", description="Project ID")
    customer_name: StringProperty(name="Customer Name",
                                  description="Customer Name",
                                  update=update_project_props)
    client_id: StringProperty(name="Client ID", description="Client ID", update=update_project_props)
    project_address: StringProperty(name="Project Address",
                                    description="Project Address",
                                    update=update_project_props)
    city: StringProperty(name="City", description="City", update=update_project_props)
    state: StringProperty(name="State", description="State", update=update_project_props)
    zip_code: StringProperty(name="Zip Code", description="Zip Code", update=update_project_props)
    customer_phone_1: StringProperty(name="Customer Phone 1",
                                     description="Customer Phone 1",
                                     update=update_project_props)
    customer_phone_2: StringProperty(name="Customer Phone 2",
                                     description="Customer Phone 2",
                                     update=update_project_props)
    customer_email: StringProperty(name="Customer Email",
                                   description="Customer Email",
                                   update=update_project_props)
    project_notes: StringProperty(name="Project Notes",
                                  description="Project Notes",
                                  update=update_project_props)
    designer: StringProperty(name="Designer", description="Designer", update=update_project_props)
    design_date: StringProperty(name="Design Date", description="Design Date", update=update_project_props)

    def init(self, name, path=None):
        col = bpy.context.window_manager.sn_project.projects
        super().init(col, name=name)

        self.create_dir()
        self.set_filename()
        proj_filepath = os.path.join(self.dir_path, ".snap", '{}.{}'.format(self.file_name, "ccp"))
        self.set_filepath(proj_filepath)

        # File path passed in
        if path:
            self.read_project_file()
        # File already exists in project directory
        elif os.path.exists(proj_filepath):
            self.read_project_file()
        else:
            project_id = self.get_id()
            self.project_id = project_id
            self.create_file(project_id)

    def create_dir(self):
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)
        pm_utils.create_hidden_folder(self.dir_path)    

    def set_filename(self):
        self.file_name = self.get_clean_name(self.name)

    def set_filepath(self, proj_filepath):
        self.file_path = proj_filepath

    def get_id(self):
        addon_prefs = bpy.context.preferences.addons[__name__.split(".")[0]].preferences
        addon_prefs.project_id_count += 1
        bpy.ops.wm.save_userpref()

        return addon_prefs.project_id_count

    def create_file(self, project_id):
        ccp = pm_utils.CCP()
        ccp.filename = self.file_name
        root = ccp.create_tree()
        project_info = ccp.add_element(root, 'ProjectInfo')

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

        ccp.write(os.path.join(self.dir_path, ".snap"))

    def modify_project_file(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        for elm in root.findall("ProjectInfo"):
            items = list(elm)

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
            items = list(elm)

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

    def draw_room_info(self, layout):
        active_room_path = self.rooms[self.room_index].file_path
        col = layout.column(align=True)
        col.template_list("SNAP_UL_Rooms", "", self, "rooms", self, "room_index", maxrows=5)
        row = col.row(align=True)
        row.operator(
            "project_manager.open_room",
            text="Open Room",
            icon='FILE_TICK').file_path = active_room_path

    def draw_render_info(self, layout):
        box = layout.box()
        box.label(text="RENDERS HERE")

    def draw(self, layout):
        if len(self.rooms) > 0:
            self.draw_room_info(layout)
        else:
            layout.label(text="No rooms", icon='ERROR')

    def add_room(self, name, category, project_index=None):
        room = self.rooms.add()
        room.init(name, category, project_index=project_index)

    def add_room_from_file(self, name, category, path, project_index=None):
        room = self.rooms.add()
        room.init(name, category, path, project_index=project_index)


class WM_PROPERTIES_Projects(PropertyGroup):
    projects: CollectionProperty(name="Projects", type=Project)
    project_index: IntProperty(name="Project Index")
    current_file_room: StringProperty(name="Current File Room", description="Current blend file room name")
    current_file_project: StringProperty(name="Current File Project", description="Current blend file project name")
    use_compact_ui: BoolProperty(name="Use Compact Projects UI Panel", default=False)

    def get_project(self):
        return self.projects[self.project_index]

    @classmethod
    def register(cls):

        bpy.types.WindowManager.sn_project = PointerProperty(
            name="Project Settings",
            description="SNaP Project Manager Properties",
            type=cls,
        )


classes = (
    Room,
    Project,
    WM_PROPERTIES_Projects
)


register, unregister = bpy.utils.register_classes_factory(classes)
