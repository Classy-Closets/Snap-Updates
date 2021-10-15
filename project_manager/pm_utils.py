import bpy
import os
import re
import xml.etree.ElementTree as ET
import shutil
import ctypes
import snap

FILE_ATTRIBUTE_HIDDEN = 0x02


def get_project_dir():
    project_dir = bpy.context.preferences.addons[__name__.split(".")[0]].preferences.project_dir
    # print('project directory is {}'.format(project_dir))

    if not os.path.exists(project_dir):
        os.makedirs(project_dir)

    return project_dir


def load_project_info():
    print("Loading project info...")


def set_file_attr_hidden(path):
    ret = ctypes.windll.kernel32.SetFileAttributesW(path, FILE_ATTRIBUTE_HIDDEN)
    if not ret:
        raise ctypes.WinError()


def create_hidden_folder(path):
    hidden_folder = os.path.join(path, ".snap")
    if not os.path.exists(hidden_folder):
        os.makedirs(hidden_folder)
        set_file_attr_hidden(hidden_folder)


def hide_project_file(filepath):
    filename = os.path.basename(filepath)
    dir_name = os.path.dirname(filepath)
    hidden_folder = os.path.join(dir_name, ".snap")
    if os.path.exists(hidden_folder):
        new_path = os.path.join(hidden_folder, filename)

    shutil.move(filepath, new_path)
    return new_path


def reload_projects():
    wm = bpy.context.window_manager.sn_project
    for project in wm.projects:
        wm.projects.remove(0)
    wm.project_index = 0
    load_projects()


def load_projects():
    """ Loads all projects.
    """
    proj_dir = get_project_dir()
    bl_path = bpy.data.filepath.split(os.path.sep)
    current_project_name = ''
    proj_dir_norm = os.path.normpath(proj_dir)
    if bl_path[0] != '' and bl_path[-3] == os.path.basename(proj_dir_norm):
        current_project_name = bl_path[-2]
        current_bfile_name = bl_path[-1]
    project_index = 0
    current_project_index = None

    wm = bpy.context.window_manager.sn_project

    if os.path.exists(proj_dir):
        for dir_name, sub_dirs, files in os.walk(proj_dir):
            snap_dir = None
            ccp_path = None

            if os.path.basename(dir_name) == ".snap":
                snap_dir = dir_name

            for filename in files:
                _, ext = os.path.splitext(os.path.basename(filename))
                # Ensure older projects have a hidden project folder
                # If there is no existing hidden folder but there is a .ccp, create hidden folder and move .ccp
                if not snap_dir and ext == ".ccp":
                    create_hidden_folder(dir_name)
                    path = os.path.join(dir_name, filename)
                    ccp_path = hide_project_file(path)
                if snap_dir and ext == ".ccp":
                    ccp_path = os.path.join(dir_name, filename)
                if ccp_path:
                    proj_name = None
                    try:
                        tree = ET.parse(ccp_path)
                        root = tree.getroot()

                        for elm in root.findall("ProjectInfo"):
                            items = list(elm)

                            for item in items:
                                if item.tag == 'name':
                                    proj_name = item.text

                        if proj_name and proj_name not in wm.projects:
                            proj = wm.projects.add()
                            proj.init(proj_name)
                            wm.project_index = project_index
                            if proj_name == current_project_name:
                                current_project_index = project_index

                            for elm in root.findall("Rooms"):
                                for sub_elm in elm:
                                    rel_path = os.path.join(*sub_elm.get("path").split(os.sep)[-2:])
                                    proj_dir = get_project_dir()
                                    room_filepath = os.path.join(proj_dir, rel_path)
                                    if(sub_elm.get("category")):
                                        proj.add_room_from_file(sub_elm.get("name"),
                                                                sub_elm.get("category"),
                                                                room_filepath,
                                                                project_index=project_index)
                                    else:
                                        proj.add_room_from_file(sub_elm.get("name"),
                                                                "No Category Selected",
                                                                room_filepath,
                                                                project_index=project_index)

                            project_index += 1

                    except ET.ParseError as err:
                        print('Cannot load project "{}": ParseError - '.format(os.path.basename(ccp_path)), err)

        if current_project_index is not None:
            wm.project_index = current_project_index
            current_project = wm.projects[wm.project_index]
            wm.current_file_project = current_project.name

            for index, room in enumerate(current_project.rooms):
                if room.file_path == bpy.data.filepath:
                    current_project.room_index = index
                    wm.current_file_room = room.name
                    print("Found Room:", room.name, current_bfile_name)

        else:
            wm.project_index = 0

class CCP():

    filename = ""
    ext = ".ccp"
    tree = None

    def __init__(self):
        pass

    def create_tree(self):
        root = ET.Element('Root', {'Application': 'SNaP', 'ApplicationVersion': snap.bl_info['version']})
        self.tree = ET.ElementTree(root)
        return root

    def add_element(self, root, elm_name, attrib_name=""):
        if attrib_name == "":
            elm = ET.Element(elm_name)
        else:
            elm = ET.Element(elm_name, {'Name': attrib_name})
        root.append(elm)
        return elm

    def add_element_with_text(self, root, elm_name, text):
        field = ET.Element(elm_name)
        field.text = text
        root.append(field)

    def format_xml_file(self, path):
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

        file = open(path, 'w')
        file.write(pretty_xml)
        file.close()

        cleaned_lines = []
        with open(path, "r") as f:
            lines = f.readlines()
            for ln in lines:
                ln.strip()
                if "<" in ln:
                    cleaned_lines.append(ln)

        with open(path, "w") as f:
            f.writelines(cleaned_lines)

    def write(self, path):
        path = os.path.join(path, self.filename + self.ext)

        with open(path, 'w', encoding='utf-8') as file:
            self.tree.write(file, encoding='unicode')

        self.format_xml_file(path)


def clean_name(name):
    illegal = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']

    for i in illegal:
        if i in name:
            name = name.replace(i, '')

    return name


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
