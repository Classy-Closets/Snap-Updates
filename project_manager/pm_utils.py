import bpy
import os
import re
import xml.etree.ElementTree as ET


def check_project_path():
    print("checking project path...")

    path = bpy.context.scene.project_info.project_path

    if os.path.exists(path):
        print("path exists")
    else:
        print("path DOES NOT exist")


def get_project_dir():
    project_dir = bpy.context.preferences.addons[__name__.split(".")[0]].preferences.project_dir
    # print('project directory is {}'.format(project_dir))

    if not os.path.exists(project_dir):
        os.makedirs(project_dir)

    return project_dir


def load_project_info():
    print("Loading project info...")


def reload_projects():
    wm = bpy.context.window_manager.sn_project
    proj_dir = bpy.context.preferences.addons['snap'].preferences.project_dir

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
                                    # This should work, regardless of if it is an absolute or relative path
                                    rel_path = os.path.join(*sub_elm.get("path").split(os.sep)[-2:])
                                    proj_dir = pm_utils.get_project_dir()
                                    room_filepath = os.path.join(proj_dir, rel_path)
                                    proj.add_room_from_file(sub_elm.get("name"),
                                                            sub_elm.get("category"),
                                                            room_filepath)


class CCP():

    filename = ""
    ext = ".ccp"
    tree = None

    def __init__(self):
        pass

    def create_tree(self):
        root = ET.Element('Root', {'Application': 'Classy Designer', 'ApplicationVersion': '1.0'})
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
