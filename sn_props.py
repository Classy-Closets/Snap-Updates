import os
import inspect
import math

import bpy
from bpy.types import PropertyGroup
from bpy.props import (BoolProperty,
                       FloatProperty,
                       IntProperty,
                       StringProperty,
                       PointerProperty,
                       CollectionProperty,
                       EnumProperty,
                       FloatVectorProperty)

from bpy.utils import register_class, unregister_class
from snap.sn_unit import inch

from snap import sn_paths, sn_utils, sn_unit
from snap.libraries.closets import closet_library
from snap.libraries.doors_and_windows import doors_and_windows_library
from snap.libraries.appliances import appliance_library
from . import addon_updater_ops

LIBRARIES = (closet_library,
             doors_and_windows_library,
             appliance_library)
DEV_TOOLS_AVAILABLE = False

try:
    from . import developer_utils
    DEV_TOOLS_AVAILABLE = True
except ImportError as e:
    print(e.msg)


enum_render_type = [('PRR', 'Photo Realistic Render','Photo Realistic Render'),
                        ('NPR', 'Line Drawing','Non-Photo Realistic Render')]


prompt_types = [('FLOAT', "Float", "Float"),
                ('DISTANCE', "Distance", "Distance"),
                ('ANGLE', "Angle", "Angle"),
                ('QUANTITY', "Quantity", "Quantity"),
                ('PERCENTAGE', "Percentage", "Percentage"),
                ('CHECKBOX', "Checkbox", "Checkbox"),
                ('COMBOBOX', "Combobox", "Combobox"),
                ('TEXT', "Text", "Text")]


def update_library_paths(self, context):
    """ EVENT: saves an XML file to disk to store the path
               of the library data.
    """
    bpy.ops.sn_general.update_library_xml()


def update_scene_index(self, context):
    space_data = context.space_data
    v3d = space_data.region_3d
    scene = context.window.scene

    if not scene.snap.elevation_scene:
        scene.snap.initial_view_location = v3d.view_location.copy()
        scene.snap.initial_view_rotation = v3d.view_rotation.copy()
        scene.snap.initial_shade_mode = space_data.shading.type

    context.window.scene = bpy.data.scenes[self.elevation_scene_index]
    scene = context.window.scene

    is_elv = scene.snap.scene_type == 'ELEVATION'
    is_pv = scene.snap.scene_type == 'PLAN_VIEW'
    is_acc = scene.snap.scene_type == 'ACCORDION'
    is_island = scene.snap.scene_type == 'ISLAND'
    is_virt = scene.snap.scene_type == 'VIRTUAL'

    if is_elv or is_pv or is_acc or is_island or is_virt:
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].region_3d.view_perspective = 'CAMERA'
                space_data.shading.type = 'WIREFRAME'

    elif scene.sn_closets.is_drill_scene:
        for window in bpy.context.window_manager.windows:
            screen = window.screen

            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    space_data.shading.type = 'WIREFRAME'
                    bpy.ops.object.select_all(action='SELECT')

                    for region in area.regions:
                        if region.type == 'WINDOW':
                            override = bpy.context.copy()
                            override['window'] = window
                            override['screen'] = screen
                            override['area'] = area
                            override['region'] = region
                            bpy.ops.view3d.view_selected(override, use_all_regions=False)

                bpy.ops.object.select_all(action='DESELECT')

    else:
        v3d.view_location = scene.snap.initial_view_location
        v3d.view_rotation = scene.snap.initial_view_rotation
        space_data.shading.type = scene.snap.initial_shade_mode
        v3d.view_perspective = 'PERSP'


class Variable():

    obj = None
    data_path = ""
    name = ""

    def __init__(self, obj, data_path, name):
        self.obj = obj
        self.data_path = data_path
        self.name = name


class Combobox_Item(PropertyGroup):
    pass


class Library_Item(PropertyGroup):
    package_name: StringProperty(name="Package Name")
    module_name: StringProperty(name="Module Name")
    class_name: StringProperty(name="Class Name")
    placement_id: StringProperty(name="Placement ID")
    prompts_id: StringProperty(name="Prompts ID")

    category_name: StringProperty(name="Category Name")


class Library(PropertyGroup):
    library_items: bpy.props.CollectionProperty(name="Library Items", type=Library_Item)
    lib_type: EnumProperty(
        name="Library Type",
        items=[('SNAP', "Snap", "Snap"),
               ('STANDARD', "Standard", "Standard")
               ], default='SNAP')
    root_dir: StringProperty(
        name="Library Path",
        description="Path to library",
        subtype='DIR_PATH')
    thumbnail_dir: StringProperty(
        name="Library Thumbnails Path",
        description="Path to library thumbnails",
        subtype='DIR_PATH')
    drop_id: StringProperty(
        name="Drop ID",
        description="This is the operator id that gets called when you drop a file onto the 3D Viewport")
    use_custom_icon: BoolProperty(
        name="Use Custom Icon",
        description="Use a Custom Icon",
        default=False)
    icon: StringProperty(
        name="Icon",
        description="This is the icon to display in the panel")
    # default_category: StringProperty(name="Default Category", description="This is the default category")

    def load_library_items_from_module(self, module):
        package_name1, package_name2, module_name = module.__name__.split(".")
        for name, obj in inspect.getmembers(module):
            if hasattr(obj, 'show_in_library') and name != 'ops' and obj.show_in_library:
                item = self.library_items.add()
                item.package_name = package_name1 + "." + package_name2
                item.category_name = obj.category_name
                item.module_name = module_name
                item.class_name = name
                item.name = name


class Asset(PropertyGroup):
    is_selected: BoolProperty(name="Is Selected", default=False)
    preview_found: BoolProperty(name="Preivew Found", default=False)
    library_path: StringProperty(name="Library Path")
    package_name: StringProperty(name="Package Name")
    module_name: StringProperty(name="Module Name")
    category_name: StringProperty(name="Category Name")
    class_name: StringProperty(name="Class Name")


class Pointer(PropertyGroup):
    category: StringProperty(name="Category")
    item_name: StringProperty(name="Item Name")


class Pointer_Slot(PropertyGroup):
    pointer_name: StringProperty(name="Pointer Name", description="")


class Prompt(PropertyGroup):
    prompt_type: EnumProperty(name="Prompt Type", items=prompt_types)

    float_value: FloatProperty(name="Float Value")
    distance_value: FloatProperty(name="Distance Value", subtype='DISTANCE', precision=4)
    angle_value: FloatProperty(name="Angle Value", subtype='ANGLE')
    quantity_value: IntProperty(name="Quantity Value", subtype='DISTANCE', min=0)
    factor_value: FloatProperty(name="Percentage Value", subtype='PERCENTAGE', min=0, max=1)
    checkbox_value: BoolProperty(name="Checkbox Value", description="")
    text_value: StringProperty(name="Text Value", description="")

    calculator_index: IntProperty(name="Calculator Index")

    combobox_items: CollectionProperty(type=Combobox_Item, name="Tabs")
    combobox_index: IntProperty(name="Combobox Index", description="")
    combobox_columns: IntProperty(name="Combobox Columns", default=1, min=1)

    def get_var(self, name=""):
        if name == "":
            name = self.name.replace(" ", "_")
        
        prompt_path = 'snap.prompts["' + self.name + '"]'
        if self.prompt_type == 'FLOAT':
            return Variable(self.id_data, prompt_path + '.float_value', name)
        if self.prompt_type == 'DISTANCE':
            return Variable(self.id_data, prompt_path + '.distance_value', name)
        if self.prompt_type == 'ANGLE':
            return Variable(self.id_data, prompt_path + '.angle_value', name)
        if self.prompt_type == 'QUANTITY':
            return Variable(self.id_data, prompt_path + '.quantity_value', name)
        if self.prompt_type == 'PERCENTAGE':
            return Variable(self.id_data, prompt_path + '.factor_value', name)
        if self.prompt_type == 'CHECKBOX':
            return Variable(self.id_data, prompt_path + '.checkbox_value', name)
        if self.prompt_type == 'COMBOBOX':
            #  TODO: IMPLEMENT UI LIST
            return Variable(self.id_data, prompt_path + '.combobox_index', name)
        if self.prompt_type == 'TEXT':
            return Variable(self.id_data, prompt_path + '.text_value', name)

    def get_value(self):
        if self.prompt_type == 'FLOAT':
            return self.float_value
        if self.prompt_type == 'DISTANCE':
            return self.distance_value
        if self.prompt_type == 'ANGLE':
            return self.angle_value
        if self.prompt_type == 'QUANTITY':
            return self.quantity_value
        if self.prompt_type == 'PERCENTAGE':
            return self.factor_value
        if self.prompt_type == 'CHECKBOX':
            return self.checkbox_value
        if self.prompt_type == 'COMBOBOX':
            #  TODO: IMPLEMENT UI LIST
            return self.combobox_index
        if self.prompt_type == 'TEXT':
            return self.text_value

    def set_value(self, value):
        self.id_data.hide_viewport = False
        if self.prompt_type == 'FLOAT':
            self.float_value = value
        if self.prompt_type == 'DISTANCE':
            self.distance_value = value
        if self.prompt_type == 'ANGLE':
            self.angle_value = math.radians(value)
        if self.prompt_type == 'QUANTITY':
            self.quantity_value = value
        if self.prompt_type == 'PERCENTAGE':
            self.factor_value = value
        if self.prompt_type == 'CHECKBOX':
            self.checkbox_value = value
        if self.prompt_type == 'COMBOBOX':
            #  TODO: IMPLEMENT UI LIST
            self.combobox_index = value
        if self.prompt_type == 'TEXT':
            self.text_value = value
        self.id_data.hide_viewport = True

    def set_formula(self, expression, variables):
        data_path = self.get_data_path()
        driver = self.id_data.driver_add(data_path)
        sn_utils.add_driver_variables(driver, variables)
        driver.driver.expression = expression

    def get_data_path(self):
        prompt_path = 'snap.prompts["' + self.name + '"]'
        data_path = ""
        if self.prompt_type == 'FLOAT':
            data_path = prompt_path + '.float_value'
        if self.prompt_type == 'DISTANCE':
            data_path = prompt_path + '.distance_value'
        if self.prompt_type == 'ANGLE':
            data_path = prompt_path + '.angle_value'
        if self.prompt_type == 'QUANTITY':
            data_path = prompt_path + '.quantity_value'
        if self.prompt_type == 'PERCENTAGE':
            data_path = prompt_path + '.precentage_value'
        if self.prompt_type == 'CHECKBOX':
            data_path = prompt_path + '.checkbox_value'
        if self.prompt_type == 'COMBOBOX':
            data_path = prompt_path + '.combobox_index'
        if self.prompt_type == 'TEXT':
            data_path = prompt_path + '.text_value'
        return data_path

    def draw_prompt_properties(self, layout):
        # RENAME PROMPT, #LOCK VALUE,  #IF COMBOBOX THEN COLUMN NUMBER
        pass

    def draw(self, layout, alt_text="", allow_edit=True):
        row = layout.row()
        if not alt_text:
            row.label(text=self.name)
        if self.prompt_type == 'FLOAT':
            row.prop(self, "float_value", text="")
        if self.prompt_type == 'DISTANCE':
            row.prop(self, "distance_value", text="")
        if self.prompt_type == 'ANGLE':
            row.prop(self, "angle_value", text="")
        if self.prompt_type == 'QUANTITY':
            row.prop(self, "quantity_value", text="")
        if self.prompt_type == 'PERCENTAGE':
            row.prop(self, "factor_value", text="")
        if self.prompt_type == 'CHECKBOX':
            row.prop(self, "checkbox_value", text="")
        if self.prompt_type == 'COMBOBOX':
            if allow_edit:
                props = row.operator('sn_prompt.add_combobox_value', text="", icon='ADD')
                props.obj_name = self.id_data.name
                props.prompt_name = self.name
                props = row.operator('sn_prompt.delete_combobox_value', text="", icon='X')
                props.obj_name = self.id_data.name
                props.prompt_name = self.name
                col = layout.column()
                col.template_list("SN_UL_combobox", " ", self, "combobox_items", self, "combobox_index",
                                  rows=len(self.combobox_items) / self.combobox_columns,
                                  type='GRID', columns=self.combobox_columns)
            else:
                row.template_list("SN_UL_combobox", " ", self, "combobox_items", self, "combobox_index",
                                  rows=len(self.combobox_items) / self.combobox_columns,
                                  type='GRID', columns=self.combobox_columns)

        if self.prompt_type == 'TEXT':
            row.prop(self, "text_value", text="")

        if alt_text:
            row.label(text=alt_text)

        if allow_edit:
            props = row.operator('sn_prompt.delete_prompt', text="", icon="X", emboss=False)
            props.obj_name = self.id_data.name
            props.prompt_name = self.name

    def draw_combobox_prompt(self, layout, allow_edit=False, text=""):
        if self.prompt_type == 'COMBOBOX':
            col = layout.column()
            col.template_list(
                "SN_UL_combobox",
                " ",
                self,
                "combobox_items",
                self,
                "combobox_index",
                rows=len(self.combobox_items),
                type='GRID',
                columns=1)


class Calculator_Prompt(PropertyGroup):
    distance_value: FloatProperty(name="Distance Value", subtype='DISTANCE', precision=5)
    equal: BoolProperty(name="Equal", default=True)

    def draw(self, layout):
        row = layout.row()
        row.active = False if self.equal else True
        row.prop(self, 'distance_value', text=self.name)
        row.prop(self, 'equal', text="")

    def get_var(self, calculator_name, name):
        prompt_path = 'snap.calculators["' + calculator_name + '"].prompts["' + self.name + '"]'
        return Variable(self.id_data, prompt_path + '.distance_value', name)

    def get_value(self):
        return self.distance_value


class Calculator(PropertyGroup):
    prompts: CollectionProperty(name="Prompts", type=Calculator_Prompt)
    distance_obj: PointerProperty(name="Distance Obj", type=bpy.types.Object)

    def set_total_distance(self, expression="", variables=[], value=0):
        data_path = 'snap.calculator_distance'
        driver = self.distance_obj.driver_add(data_path)
        sn_utils.add_driver_variables(driver, variables)
        driver.driver.expression = expression

    def draw(self, layout):
        col = layout.column(align=True)
        box = col.box()
        row = box.row()
        row.label(text=self.name)
        props = row.operator('sn_prompt.add_calculator_prompt', text="", icon='ADD')
        props.calculator_name = self.name
        props.obj_name = self.id_data.name
        props = row.operator('sn_prompt.edit_calculator', text="", icon='OUTLINER_DATA_GP_LAYER')
        props.calculator_name = self.name
        props.obj_name = self.id_data.name

        box.prop(self.distance_obj.snap, 'calculator_distance')
        box = col.box()
        for prompt in self.prompts:
            prompt.draw(box)
        box = col.box()
        row = box.row()
        row.scale_y = 1.3
        props = row.operator('sn_prompt.run_calculator')
        props.calculator_name = self.name
        props.obj_name = self.id_data.name

    def add_calculator_prompt(self, name):
        prompt = self.prompts.add()
        prompt.name = name
        return prompt

    def get_calculator_prompt(self, name):
        if name in self.prompts:
            return self.prompts[name]

    def remove_calculator_prompt(self, name):
        pass

    def calculate(self):
        self.distance_obj.hide_viewport = False

        non_equal_prompts_total_value = 0
        equal_prompt_qty = 0
        calc_prompts = []
        for prompt in self.prompts:
            if prompt.equal:
                equal_prompt_qty += 1
                calc_prompts.append(prompt)
            else:
                non_equal_prompts_total_value += prompt.distance_value

        if equal_prompt_qty > 0:
            prompt_value = ((self.distance_obj.snap.calculator_distance - non_equal_prompts_total_value)
                            / equal_prompt_qty)

            for prompt in calc_prompts:
                prompt.distance_value = prompt_value

            self.id_data.location = self.id_data.location

class accordion_view(PropertyGroup):

    break_width: IntProperty(name="Break Accordions Width",
                             description="When accordions are bigger than this value in inches they will be splitted",
                             default=450,
                             min=40,
                             max=10000)
    
    enable_intermediate_walls: BoolProperty(name="Enable Intermediate Walls",
                                            description="when enabled, empty walls can be included on Accordions",
                                            default=True)

    intermediate_space: IntProperty(name="Intermediate Wall Space",
                                    description="Empty walls within this width will be included on Accordions",
                                    default=24,
                                    min=2,
                                    max=1500)

    intermediate_qty: IntProperty(name="Intermediate Walls Quantity",
                                  description="Set the quantity of sequential empty walls to be added on Accordions",
                                  default=2,
                                  min=1,
                                  max=26)

class opengl_dim(PropertyGroup):

    hide: BoolProperty(name="Hide Dimension",
                       description="Show/Hide Dimension",
                       default=False)

    line_only: BoolProperty(name="Dimension Line Only",
                            description="Draw this dimension without text or arrows",
                            default=False)

    gl_color: IntProperty(name="gl_color",
                          default=0,
                          description="Color for the measure")

    standard_colors = {1: (0.8, 0.8, 0.8, 1.0),  # White
                       2: (0.1, 0.1, 0.1, 1.0),  # Black
                       3: (0.8, 0.0, 0.0, 1.0),  # Red
                       4: (0.0, 0.8, 0.0, 1.0),  # Green
                       5: (0.0, 0.0, 0.8, 1.0),  # Blue
                       6: (0.8, 0.8, 0.0, 1.0),  # Yellow
                       7: (0.0, 0.8, 0.8, 1.0),  # Aqua
                       8: (0.8, 0.0, 0.8, 1.0)}  # Violet

    gl_default_color: FloatVectorProperty(name="Default color",
                                          description="Default Color",
                                          default=(0.8, 0.8, 0.8, 1.0),
                                          min=0.1,
                                          max=1,
                                          subtype='COLOR',
                                          size=4)

    gl_width: IntProperty(name='gl_width',
                          min=1,
                          max=10,
                          default=1,
                          description='line width')

    show_label: BoolProperty(name="Show Label",
                             description="Display label for this measure",
                             default=True)

    gl_label: StringProperty(name="Label",
                             maxlen=256,
                             description="Short description (use | for line break)")

    gl_font_size: IntProperty(name="Text Size",
                              description="Text size",
                              default=22,
                              min=6,
                              max=150)

    h_line_text_placement: EnumProperty(name="Horizontal Line Text Placement",
                                        items=[('TOP', "Top", "Top"),
                                               ('BOTTOM', "Bottom", "Bottom")],
                                        default='TOP')

    v_line_text_placement: EnumProperty(name="Vertical Line Text Placement",
                                        items=[('LEFT', "Left", "Left"),
                                               ('RIGHT', "Right", "Right")],
                                        default='LEFT')

    line_to_text_pad: IntProperty(name="Line to Text Padding",
                                  description="Padding between dimension line and text",
                                  default=3,
                                  min=-3000,
                                  max=3000)

    gl_text_x: IntProperty(name="gl_text_x",
                           description="Change font position in X axis",
                           default=0,
                           min=-3000,
                           max=3000)

    gl_text_y: IntProperty(name="gl_text_y",
                           description="Change font position in Y axis",
                           default=0,
                           min=-3000,
                           max=3000)

    gl_arrow_type: EnumProperty(items=(('99', "--", "No arrow"),
                                       ('1', "Line", "The point of the arrow are lines"),
                                       ('2', "Triangle", "The point of the arrow is triangle"),
                                       ('3', "TShape", "The point of the arrow is a T")),
                                name="Arrow Type",
                                description="Dimension Arrow Type",
                                default='99')

    gl_arrow_size: IntProperty(name="Size",
                               description="Arrow size",
                               default=15,
                               min=6,
                               max=500)

    gl_dim_units: EnumProperty(items=(('AUTO', "Default", "Use system scene units"),
                                      ('METER', "Meters", "Meters"),
                                      ('CENTIMETER', "Centimeters", "Centimeters"),
                                      ('MILIMETER', "Millimeters", "Millimeters"),
                                      ('FEET', "Feet", "Feet"),
                                      ('INCH', "Inches", "Inches")),
                               name="Units",
                               default="AUTO",
                               description="Units")

    gl_number_format: EnumProperty(items=(('DECIMAL', "Decimal", "Decimal"),
                                          ('FRACTION', "Fraction", "Fraction")),
                                   name="Number Format",
                                   default='DECIMAL',
                                   description="Number display format")

    gl_imperial_rd_factor: EnumProperty(items=(('2', "1/2\"", "1/2\""),
                                               ('4', "1/4\"", "1/4\""),
                                               ('8', "1/8\"", "1/8\""),
                                               ('16', "1/16\"", "1/16\""),
                                               ('32', "1/32\"", "1/32\"")),
                                        name="Imperial Rounding",
                                        default="32",
                                        description="Rounding Factor")

    gl_precision: IntProperty(name='Precision',
                              min=0,
                              max=5,
                              default=2,
                              description="Number of decimal precision")


class Edgepart(PropertyGroup):
    thickness: FloatProperty(name="Thickness",
                             unit='LENGTH',
                             precision=5)

    mv_pointer_name: StringProperty(name="MV Pointer Name")

    material: StringProperty(name="Material")


class Cutpart(PropertyGroup):
    thickness: FloatProperty(name="Thickness",
                             unit='LENGTH',
                             precision=5)

    mv_pointer_name: StringProperty(name="MV Pointer Name")

    core: StringProperty(name="Core")

    top: StringProperty(name="Top")

    bottom: StringProperty(name="Bottom")


class Library_Pointer(PropertyGroup):
    index: IntProperty(name="Index")

    type: EnumProperty(
        name="Type",
        items=[
            ('NONE', "None", "No Grain"),
            ('WIDTH', "Width", "Width"),
            ('LENGTH', "Length", "Length")])

    library_name: StringProperty(name="Library Name")

    category_name: StringProperty(name="Category Name")

    item_name: StringProperty(name="Item Name")

    pointer_value: FloatProperty(name="Pointer Value")

    assign_material: BoolProperty(name="Assign Material", default=False)  # USED TO Assign Materials with drag and drop


class Specification_Group(PropertyGroup):
    materials: CollectionProperty(name="Materials",
                                  type=Library_Pointer)

    material_index: IntProperty(name="Material Index",
                                default=0)

    cutparts: CollectionProperty(name="Cutparts",
                                 type=Cutpart)

    cutpart_index: IntProperty(name="Cutpart Index",
                               default=0)

    edgeparts: CollectionProperty(name="Edgeparts",
                                  type=Edgepart)

    edgepart_index: IntProperty(name="Edgepart Index",
                                default=0)

    def draw_materials(self, layout):
        box = layout.box()
        row = box.row()
        col = row.column(align=True)
        col.template_list("SNAP_UL_material_pointers", " ", self, "materials", self, "material_index")
        if self.material_index + 1 <= len(self.materials):
            pointer = self.materials[self.material_index]
            box = col.box()
            box.label(text='Category Name: ' + pointer.category_name)
            box.label(text='Material Name: ' + pointer.item_name)

    def draw_cutparts(self, layout):
        box = layout.box()
        row = box.row()
        col = row.column(align=True)
        col.template_list("SNAP_UL_cutparts", " ", self, "cutparts", self, "cutpart_index")
        if self.cutpart_index + 1 <= len(self.cutparts):
            pointer = self.cutparts[self.cutpart_index]
            box = col.box()
            box.prop_search(pointer, 'core', self, 'materials', text="Core Material", icon='NONE')
            box.prop_search(pointer, 'top', self, 'materials', text="Top Material (Exterior)", icon='NODE')
            box.prop_search(pointer, 'bottom', self, 'materials', text="Bottom Material (Interior)", icon='NODE_SEL')

    def draw_edgeparts(self, layout):
        box = layout.box()
        row = box.row()
        col = row.column(align=True)
        col.template_list("SNAP_UL_edgeparts", " ", self, "edgeparts", self, "edgepart_index")
        if self.edgepart_index + 1 <= len(self.edgeparts):
            pointer = self.edgeparts[self.edgepart_index]
            box = col.box()
            box.prop_search(pointer, 'material', self, 'materials', text="Material", icon='EDGESEL')                                   


class Material_Slot(PropertyGroup):
    index: IntProperty(name="Index")
    material_path: StringProperty(name="Material Path")
    pointer_name: StringProperty(name="Pointer Name")
    library_name: StringProperty(name="Library Name")
    category_name: StringProperty(name="Category Name")
    item_name: StringProperty(name="Item Name")


class List_Library_Item(PropertyGroup):
    """ Class to put products, inserts, and parts in a list view
        Used to show all library items
    """
    bp_name: StringProperty(name='BP Name')
    class_name: StringProperty(name='Class Name')
    library_name: StringProperty(name='Library Name')
    category_name: StringProperty(name='Category Name')
    selected: BoolProperty(name="Selected")
    has_thumbnail: BoolProperty(name="Has Thumbnail")
    has_file: BoolProperty(name="Has File")


class List_Library(PropertyGroup):
    package_name: StringProperty(name="Package Name")
    module_name: StringProperty(name="Module Name")
    lib_path: StringProperty(name="Library Path")
    items: CollectionProperty(name="Items", type=List_Library_Item)
    index: IntProperty(name="Index")


class Pline_Vector(PropertyGroup):

    x_loc: FloatProperty(name="X Location", unit='LENGTH')
    y_loc: FloatProperty(name="Y Location", unit='LENGTH')
    z_loc: FloatProperty(name="Z Location", unit='LENGTH')
    bulge: FloatProperty(name="Buldge")

    def add_x_driver(self, token_name, vector_index, expression, driver_vars):
        obj = self.id_data
        data_path = 'snap.mp.machine_tokens.["' + token_name + '"].vector_locations[' + str(vector_index) + '].x_loc'
        driver = obj.driver_add(data_path)
        sn_utils.add_driver_variables(driver, driver_vars)
        driver.driver.expression = expression

    def add_y_driver(self, token_name, vector_index, expression, driver_vars):
        obj = self.id_data
        data_path = 'snap.mp.machine_tokens.["' + token_name + '"].vector_locations[' + str(vector_index) + '].y_loc'
        driver = obj.driver_add(data_path)
        sn_utils.add_driver_variables(driver, driver_vars)
        driver.driver.expression = expression

    def add_z_driver(self, token_name, vector_index, expression, driver_vars):
        obj = self.id_data
        data_path = 'snap.mp.machine_tokens.["' + token_name + '"].vector_locations[' + str(vector_index) + '].z_loc'
        driver = obj.driver_add(data_path)
        sn_utils.add_driver_variables(driver, driver_vars)
        driver.driver.expression = expression

    def add_bulge_driver(self, token_name, vector_index, expression, driver_vars):
        obj = self.id_data
        data_path = 'snap.mp.machine_tokens.["' + token_name + '"].vector_locations[' + str(vector_index) + '].bulge'
        driver = obj.driver_add(data_path)
        sn_utils.add_driver_variables(driver, driver_vars)
        driver.driver.expression = expression


bpy.utils.register_class(Pline_Vector)


class Machine_Token(PropertyGroup):
    show_expanded: BoolProperty(name="Show Expanded", default=False)
    is_disabled: BoolProperty(name="Is Disabled", default=False)

    type_token: EnumProperty(name="Mesh Type",
                             items=[('NONE', "None", "None"),
                                    ('CORNERNOTCH', "CORNERNOTCH", "CORNERNOTCH"),
                                    ('CHAMFER', "CHAMFER", "CHAMFER"),
                                    ('CONST', "CONST", "CONST"),
                                    ('HOLES', "HOLES", "HOLES"),
                                    ('SHLF', "SHLF", "SHLF"),
                                    ('SHELF', "SHELF", "SHELF"),
                                    ('SHELFSTD', "SHELFSTD", "SHELFSTD"),
                                    ('DADO', "DADO", "DADO"),
                                    ('SAW', "SAW", "SAW"),
                                    ('SLIDE', "SLIDE", "SLIDE"),
                                    ('CAMLOCK', "CAMLOCK", "CAMLOCK"),
                                    ('MITER', "MITER", "MITER"),
                                    ('3SIDEDNOTCH', "3SIDEDNOTCH", "3SIDEDNOTCH"),
                                    ('PLINE', "PLINE", "PLINE"),
                                    ('BORE', "BORE", "BORE")],
                             description="Select the Machine Token Type.",
                             default='NONE')

    face: EnumProperty(name="Face",
                       items=[('1', "1", "1"),
                              ('2', "2", "2"),
                              ('3', "3", "3"),
                              ('4', "4", "4"),
                              ('5', "5", "5"),
                              ('6', "6", "6")],
                       description="Select the face to assign the machine token to.",
                       default='1')

    edge: EnumProperty(name="Edge",
                       items=[('1', "1", "1"),
                              ('2', "2", "2"),
                              ('3', "3", "3"),
                              ('4', "4", "4"),
                              ('5', "5", "5"),
                              ('6', "6", "6"),
                              ('7', "7", "7"),
                              ('8', "8", "8")],
                       description="Select the edge to assign the machine token to.",
                       default='1')

    vector_locations: CollectionProperty(name="Vector Location", type=Pline_Vector)
    # buldge_list: CollectionProperty(name="Vector Location",type=Pline_Bulge)

    dim_to_first_const_hole: FloatProperty(name="Dim to First Construction Hole", unit='LENGTH')
    dim_to_last_const_hole: FloatProperty(name="Dim to Last Construction Hole", unit='LENGTH')
    edge_bore_depth: FloatProperty(name="Edge Bore Depth", unit='LENGTH')
    edge_bore_dia: FloatProperty(name="Edge Bore Diameter")
    face_bore_depth: FloatProperty(name="Face Bore Depth", unit='LENGTH')
    face_bore_depth_2: FloatProperty(name="Face Bore Depth 2")
    face_bore_dia: FloatProperty(name="Face Bore Diameter")
    face_bore_dia_2: FloatProperty(name="Face Bore Diameter 2")
    drill_from_opposite_side: BoolProperty(name="Drill From Opposite Side")
    second_hole_at_32mm: BoolProperty(name="Second Hole at 32mm")
    distance_between_holes: FloatProperty(name="Distance Between Holes", unit='LENGTH', precision=4)
    hole_locations: FloatVectorProperty(name="Hole Locations", size=15, unit='LENGTH')
    z_value: FloatProperty(name="Z Value", unit='LENGTH')

    dim_in_x: FloatProperty(name="Dim In X", unit='LENGTH', precision=4)
    dim_in_y: FloatProperty(name="Dim In Y", unit='LENGTH', precision=4)
    dim_in_z: FloatProperty(name="Dim In Z", unit='LENGTH', precision=4)
    end_dim_in_x: FloatProperty(name="End Dim In X", unit='LENGTH', precision=4)
    end_dim_in_y: FloatProperty(name="End Dim In Y", unit='LENGTH', precision=4)
    associative_dia: FloatProperty(name="Associative Diameter")
    associative_depth: FloatProperty(name="Associative Depth", unit='LENGTH')

    lead_in: FloatProperty(name="Lead In", unit='LENGTH')
    lead_out: FloatProperty(name="Lead Out", unit='LENGTH')
    reverse_direction: BoolProperty(name="Reverse Direction")
    beginning_depth: FloatProperty(name="Beginning Depth", unit='LENGTH')
    double_pass: FloatProperty(name="Double Pass", unit='LENGTH')
    lock_joint: FloatProperty(name="Lock Joint", unit='LENGTH')
    panel_penetration: FloatProperty(name="Panel Penetration", unit='LENGTH')

    backset: FloatProperty(name="Backset", unit='LENGTH')
    cam_face: EnumProperty(name="Cam Face",
                           items=[('5', "5", "5"),
                                  ('6', "6", "6")],
                           description="The face number the cam is assigned to.",
                           default='5')

    tool_comp: EnumProperty(name="Tool Compensation",
                            items=[('R', "R", "Right"),
                                   ('C', "C", "Center"),
                                   ('L', "L", "Left")],
                            description="The offset of the router bit",
                            default='R')

    angle: FloatProperty(name="Angle", unit='ROTATION')

    tool_number: StringProperty(name="Tool Number")
    tongue_tool_number: StringProperty(name="Tongue Tool Number")

    space_from_bottom: FloatProperty(name="Space From Bottom", unit='LENGTH')
    space_from_top: FloatProperty(name="Space From Top", unit='LENGTH')
    dim_to_first_row: FloatProperty(name="Dim to First Row", unit='LENGTH')
    dim_to_second_row: FloatProperty(name="Dim to Second Row", unit='LENGTH')
    shelf_hole_spacing: FloatProperty(name="Shelf Hole Spacing", unit='LENGTH')
    shelf_clip_gap: FloatProperty(name="Shelf Clip Gap", unit='LENGTH')

    # SLIDE
    dim_from_drawer_bottom: FloatProperty(name="Dimension from Drawer Bottom", unit='LENGTH')
    dim_to_first_hole: FloatProperty(name="Dimension to First Hole", unit='LENGTH')
    dim_to_second_hole: FloatProperty(name="Dimension to Second Hole", unit='LENGTH')
    dim_to_third_hole: FloatProperty(name="Dimension to Third Hole", unit='LENGTH')
    dim_to_fourth_hole: FloatProperty(name="Dimension to Fourth Hole", unit='LENGTH')
    dim_to_fifth_hole: FloatProperty(name="Dimension to Fifth Hole", unit='LENGTH')
    drawer_slide_clearance: FloatProperty(name="Drawer Slide Clearance", unit='LENGTH')

    def get_hole_locations(self):
        locations = ""
        for x in range(0, len(self.hole_locations) - 1):
            if self.hole_locations[x] != 0:
                locations += str(sn_unit.meter_to_exact_unit(self.hole_locations[x])) + ","
        return locations[:-1]  # Remove last comma

    def get_vector_locations(self):
        vector_string = ""
        for i, vector in enumerate(self.vector_locations):
            x_loc = sn_unit.meter_to_exact_unit(vector.x_loc)
            y_loc = sn_unit.meter_to_exact_unit(vector.y_loc)
            z_loc = sn_unit.meter_to_exact_unit(vector.z_loc)
            vector_string += str(x_loc) + ";" + str(y_loc) + ";" + str(z_loc)
            if i + 1 < len(self.vector_locations):
                vector_string += "|"
        return vector_string

    def get_bulge_list(self):
        bulge_string = ""
        for i, vector in enumerate(self.vector_locations):
            bulge_string += str(vector.bulge)
            if i + 1 < len(self.vector_locations):
                bulge_string += ";"
        return bulge_string

    def create_parameter_dictionary(self):
        param_dict = {}
        if self.type_token == 'CONST':
            param_dict['Par1'] = str(sn_unit.meter_to_exact_unit(self.dim_to_first_const_hole))
            param_dict['Par2'] = str(sn_unit.meter_to_exact_unit(self.dim_to_last_const_hole))
            param_dict['Par3'] = str(sn_unit.meter_to_exact_unit(self.edge_bore_depth))
            param_dict['Par4'] = str(self.edge_bore_dia)
            param_dict['Par5'] = str(sn_unit.meter_to_exact_unit(self.face_bore_depth))
            param_dict['Par6'] = str(self.face_bore_dia)
            param_dict['Par7'] = "1" if self.drill_from_opposite_side else "0"
            param_dict['Par8'] = "1" if self.second_hole_at_32mm else "0"
            param_dict['Par9'] = str(sn_unit.meter_to_exact_unit(self.distance_between_holes))

        if self.type_token == 'HOLES':
            param_dict['Par1'] = self.get_hole_locations()
            param_dict['Par2'] = str(self.edge_bore_dia)
            param_dict['Par3'] = str(sn_unit.meter_to_exact_unit(self.edge_bore_depth))
            param_dict['Par4'] = ""
            param_dict['Par5'] = str(sn_unit.meter_to_exact_unit(self.face_bore_depth))
            param_dict['Par6'] = str(self.face_bore_dia)
            param_dict['Par7'] = str(self.drill_from_opposite_side)
            param_dict['Par8'] = str(self.second_hole_at_32mm)
            param_dict['Par9'] = str(sn_unit.meter_to_exact_unit(self.distance_between_holes))

        if self.type_token in {'DADO', 'SAW'}:
            param_dict['Par1'] = str(sn_unit.meter_to_exact_unit(self.lead_in))
            param_dict['Par2'] = "1" if self.reverse_direction else "0"
            param_dict['Par3'] = str(sn_unit.meter_to_exact_unit(self.beginning_depth))
            param_dict['Par4'] = str(sn_unit.meter_to_exact_unit(self.lead_out))
            param_dict['Par5'] = str(sn_unit.meter_to_exact_unit(self.double_pass))
            param_dict['Par6'] = "0"
            param_dict['Par7'] = str(self.tool_number)
            param_dict['Par8'] = str(sn_unit.meter_to_exact_unit(self.panel_penetration))
            param_dict['Par9'] = str(self.tongue_tool_number)

        if self.type_token == 'CAMLOCK':
            param_dict['Par1'] = self.get_hole_locations()
            param_dict['Par2'] = str(self.edge_bore_dia)
            param_dict['Par3'] = str(sn_unit.meter_to_exact_unit(self.edge_bore_depth))
            param_dict['Par4'] = str(sn_unit.meter_to_exact_unit(self.z_value)) if self.z_value != 0 else ""
            param_dict['Par5'] = str(self.face_bore_dia) + "," + str(self.face_bore_dia_2)
            param_dict['Par6'] = str(sn_unit.meter_to_exact_unit(self.face_bore_depth)) + "," + str(sn_unit.meter_to_exact_unit(self.face_bore_depth_2))
            param_dict['Par7'] = str(sn_unit.meter_to_exact_unit(self.backset))
            param_dict['Par8'] = str(self.cam_face)
            param_dict['Par9'] = "1" if self.drill_from_opposite_side else "0"

        if self.type_token in {'SHLF', 'SHELF', 'SHELFSTD'}:
            param_dict['Par1'] = str(sn_unit.meter_to_exact_unit(self.space_from_bottom))
            param_dict['Par2'] = str(sn_unit.meter_to_exact_unit(self.dim_to_first_row))
            param_dict['Par3'] = str(sn_unit.meter_to_exact_unit(self.face_bore_depth))
            param_dict['Par4'] = str(sn_unit.meter_to_exact_unit(self.space_from_top))
            param_dict['Par5'] = str(sn_unit.meter_to_exact_unit(self.dim_to_second_row))
            param_dict['Par6'] = str(self.face_bore_dia)
            param_dict['Par7'] = str(sn_unit.meter_to_exact_unit(self.shelf_hole_spacing))
            param_dict['Par8'] = str(sn_unit.meter_to_exact_unit(self.shelf_clip_gap))
            param_dict['Par9'] = "1" if self.reverse_direction else "0"

        if self.type_token == 'BORE':
            param_dict['Par1'] = str(sn_unit.meter_to_exact_unit(self.dim_in_x))
            param_dict['Par2'] = str(sn_unit.meter_to_exact_unit(self.dim_in_y))
            param_dict['Par3'] = str(sn_unit.meter_to_exact_unit(self.dim_in_z))
            param_dict['Par4'] = str(self.face_bore_dia)
            param_dict['Par5'] = str(sn_unit.meter_to_exact_unit(self.end_dim_in_x))
            param_dict['Par6'] = str(sn_unit.meter_to_exact_unit(self.end_dim_in_y))
            param_dict['Par7'] = str(sn_unit.meter_to_exact_unit(self.distance_between_holes))
            param_dict['Par8'] = str(self.associative_dia)
            param_dict['Par9'] = str(sn_unit.meter_to_exact_unit(self.associative_depth))

        if self.type_token == 'CORNERNOTCH':
            param_dict['Par1'] = str(sn_unit.meter_to_exact_unit(self.dim_in_x))
            param_dict['Par2'] = str(sn_unit.meter_to_exact_unit(self.dim_in_y))
            param_dict['Par3'] = str(sn_unit.meter_to_exact_unit(self.dim_in_z))
            param_dict['Par4'] = str(sn_unit.meter_to_exact_unit(self.lead_in))
            param_dict['Par5'] = ""
            param_dict['Par6'] = ""
            param_dict['Par7'] = str(self.tool_number)
            param_dict['Par8'] = ""
            param_dict['Par9'] = ""

        if self.type_token == 'CHAMFER':
            param_dict['Par1'] = str(sn_unit.meter_to_exact_unit(self.dim_in_x))
            param_dict['Par2'] = str(sn_unit.meter_to_exact_unit(self.dim_in_y))
            param_dict['Par3'] = str(sn_unit.meter_to_exact_unit(self.dim_in_z))
            param_dict['Par4'] = str(sn_unit.meter_to_exact_unit(self.lead_in))
            param_dict['Par5'] = ""
            param_dict['Par6'] = ""
            param_dict['Par7'] = str(self.tool_number)
            param_dict['Par8'] = ""
            param_dict['Par9'] = ""

        if self.type_token == 'SLIDE':
            param_dict['Par1'] = str(sn_unit.meter_to_exact_unit(self.dim_from_drawer_bottom))
            param_dict['Par2'] = str(sn_unit.meter_to_exact_unit(self.dim_to_first_hole))
            param_dict['Par3'] = str(sn_unit.meter_to_exact_unit(self.dim_to_second_hole))
            param_dict['Par4'] = str(sn_unit.meter_to_exact_unit(self.dim_to_third_hole))
            param_dict['Par5'] = str(sn_unit.meter_to_exact_unit(self.dim_to_fourth_hole))
            param_dict['Par6'] = str(sn_unit.meter_to_exact_unit(self.dim_to_fifth_hole))
            param_dict['Par7'] = str(sn_unit.meter_to_exact_unit(self.face_bore_depth)) + "|" + str(self.face_bore_dia)
            param_dict['Par8'] = str(sn_unit.meter_to_exact_unit(self.drawer_slide_clearance))
            param_dict['Par9'] = ""

        if self.type_token == '3SIDEDNOTCH':
            param_dict['Par1'] = str(sn_unit.meter_to_exact_unit(self.dim_in_x))  # X
            param_dict['Par2'] = str(sn_unit.meter_to_exact_unit(self.dim_in_y))  # Y
            param_dict['Par3'] = str(sn_unit.meter_to_exact_unit(self.dim_in_z))  # Z
            param_dict['Par4'] = str(sn_unit.meter_to_exact_unit(self.end_dim_in_x))  # ENDX
            param_dict['Par5'] = str(sn_unit.meter_to_exact_unit(self.end_dim_in_y))  # ENDY
            param_dict['Par6'] = str(sn_unit.meter_to_exact_unit(self.lead_in))  # LEADINOUT
            param_dict['Par7'] = str(self.tool_number)  # TOOLNUMBER
            param_dict['Par8'] = ""  # DRAW NUMBER
            param_dict['Par9'] = ""  # SEQUENCE NUMBER

        if self.type_token == 'PLINE':
            param_dict['Par1'] = self.get_vector_locations()  # VECTOR LOCATION
            param_dict['Par2'] = self.get_bulge_list()  # BULGE LIST
            param_dict['Par3'] = ""  # FEED SPEEDS
            param_dict['Par4'] = ""  # OPTIONS
            param_dict['Par5'] = ""  # OFFSET
            param_dict['Par6'] = ""  # PROFILE NAME
            param_dict['Par7'] = str(self.tool_number) # TOOLNUMBER
            param_dict['Par8'] = str(self.tool_comp)  # TOOL COMPENSATION
            param_dict['Par9'] = ""  # SEQUENCE

        return param_dict

    def draw_properties(self, layout):
        col = layout.column(align=True)
        box = col.box()
        row = box.row()

        if self.show_expanded:
            row.prop(self, 'show_expanded', text='', icon='TRIA_DOWN', emboss=False)
        else:
            row.prop(self, 'show_expanded', text="", icon='TRIA_RIGHT', emboss=False)
        row.prop(self, "name", text="", icon='LAYER_USED' if self.is_disabled else 'LAYER_ACTIVE')
        row.operator('snap.delete_machine_token', text="", icon='X', emboss=False).token_name = self.name

        if self.show_expanded:
            box = col.box()
            row = box.row()
            row.prop(self, 'type_token', text="")
            row.prop(self, 'face', text="Face")
            if self.type_token == 'CONST':
                col = box.column(align=True)
                col.prop(self, 'dim_to_first_const_hole')
                col.prop(self, 'dim_to_last_const_hole')
                box.prop(self, 'distance_between_holes')
                row = box.row(align=True)
                row.label(text='Edge:')
                row.prop(self, 'edge_bore_depth', text="Depth")
                row.prop(self, 'edge_bore_dia', text="Dia")
                row = box.row(align=True)
                row.label(text='Face:')
                row.prop(self, 'face_bore_depth', text="Depth")
                row.prop(self, 'face_bore_dia', text="Dia")
                row = box.row(align=True)
                row.prop(self, 'drill_from_opposite_side')
                row.prop(self, 'second_hole_at_32mm')
            if self.type_token == 'HOLES':
                box.prop(self, 'hole_locations')
                box.prop(self, 'edge_bore_dia')
                box.prop(self, 'edge_bore_depth')
                box.prop(self, 'face_bore_depth')
                box.prop(self, 'face_bore_dia')
                box.prop(self, 'drill_from_opposite_side')
                box.prop(self, 'z_value')
            if self.type_token in {'SHLF', 'SHELF'}:
                col = box.column(align=True)
                col.prop(self, 'space_from_top')
                col.prop(self, 'space_from_bottom')
                row = box.row(align=True)
                row.prop(self, 'dim_to_first_row')
                row.prop(self, 'dim_to_second_row')
                row = box.row(align=True)
                row.label(text="Drilling:")
                row.prop(self, 'face_bore_dia', text="Dia")
                row.prop(self, 'face_bore_depth', text="Depth")
                row.prop(self, 'shelf_hole_spacing', text="Spacing")
                box.prop(self, 'shelf_clip_gap')
                box.prop(self, 'drill_from_opposite_side')
            if self.type_token == 'SHELFSTD':
                box.label(text='Not Available at this time')
            if self.type_token in {'DADO', 'SAW'}:
                row = box.row(align=True)
                row.label(text='Router Lead:')
                row.prop(self, 'lead_in', text="In")
                row.prop(self, 'lead_out', text="Out")
                box.prop(self, 'beginning_depth')
                box.prop(self, 'double_pass')
                box.prop(self, 'lock_joint')
                box.prop(self, 'panel_penetration')
                box.prop(self, 'tool_number')
                box.prop(self, 'tongue_tool_number')
                box.prop(self, 'reverse_direction')
            if self.type_token == 'SLIDE':
                row.prop(self, 'dim_from_drawer_bottom')
                row.prop(self, 'dim_to_first_hole')
                box.prop(self, 'dim_to_second_hole')
                box.prop(self, 'dim_to_third_hole')
                box.prop(self, 'dim_to_fourth_hole')
                box.prop(self, 'dim_to_fifth_hole')
                box.prop(self, 'face_bore_depth')
                box.prop(self, 'face_bore_dia')
                box.prop(self, 'drawer_slide_clearance')
            if self.type_token == 'CAMLOCK':
                box.prop(self, 'hole_locations')
                box.prop(self, 'edge_bore_dia')
                box.prop(self, 'edge_bore_depth')
                row = box.row()
                row.prop(self, 'face_bore_dia')
                row.prop(self, 'face_bore_depth')
                row = box.row()
                row.prop(self, 'face_bore_dia_2')
                row.prop(self, 'face_bore_depth_2')
                box.prop(self, 'z_value')
                box.prop(self, 'backset')
                box.label(text='Cam Face')
                box.prop(self, 'cam_face', expand=True)
                box.prop(self, 'drill_from_opposite_side')
            if self.type_token == 'MITER':
                box.prop(self, 'edge')
                box.prop(self, 'angle')
                box.prop(self, 'lead_out')
                box.prop(self, 'tool_number')
            if self.type_token == 'BORE':
                row = box.row(align=True)
                row.label(text="Start Dim:")
                row.prop(self, 'dim_in_x', text="X")
                row.prop(self, 'dim_in_y', text="Y")
                row = box.row(align=True)
                row.label(text="End Dim:")
                row.prop(self, 'end_dim_in_x', text="X")
                row.prop(self, 'end_dim_in_y', text="Y")

                row = box.row(align=True)
                row.label(text="Drill Depth: (dim_in_z)")
                row.prop(self, 'dim_in_z', text="")

                row = box.row(align=True)
                row.label(text="Drill Dia: (millimeters)")
                row.prop(self, 'face_bore_dia', text="")

                row = box.row(align=True)
                row.label(text="Distance Between Holes")
                row.prop(self, 'distance_between_holes', text="")

                row = box.row(align=True)
                row.label(text="Associative")
                row.prop(self, 'associative_dia', text="Dia")
                row.prop(self, 'associative_depth', text="Depth")

            if self.type_token == 'CORNERNOTCH':
                box.prop(self, 'dim_in_x')
                box.prop(self, 'dim_in_y')
                box.prop(self, 'dim_in_z')
                box.prop(self, 'lead_in')
                box.prop(self, 'tool_number')
            if self.type_token == 'CHAMFER':
                box.prop(self, 'dim_in_x')
                box.prop(self, 'dim_in_y')
                box.prop(self, 'dim_in_z')
                box.prop(self, 'lead_in')
                box.prop(self, 'tool_number')
            if self.type_token == '3SIDEDNOTCH':
                box.prop(self, 'edge')
                row = box.row(align=True)
                row.label(text="Start Dim:")
                row.prop(self, 'dim_in_x', text="X")
                row.prop(self, 'dim_in_y', text="Y")
                row.prop(self, 'dim_in_z', text="Z")

                row = box.row(align=True)
                row.label(text="End Dim:")
                row.prop(self, 'end_dim_in_x', text="X")
                row.prop(self, 'end_dim_in_y', text="Y")

                box.prop(self, 'lead_in')
                box.prop(self, 'tool_number')
            if self.type_token == 'PLINE':
                row = box.row()
                row.prop(self, 'tool_number')
                row = box.row()
                row.prop(self, 'tool_comp', expand=True)

                for i, vector in enumerate(self.vector_locations):
                    row = box.row(align=True)
                    row.label(text="Vector")
                    row.prop(vector, 'x_loc', text="X")
                    row.prop(vector, 'y_loc', text="Y")
                    row.prop(vector, 'z_loc', text="Z")
                    if i + 1 != len(self.vector_locations):
                        row = box.row(align=True)
                        row.label(text="Bulge")
                        row.prop(vector, 'bulge', text="")

    def add_driver(self, obj, token_property, expression, driver_vars, index=None):
        data_path = 'snap.mp.machine_tokens.["' + \
            self.name + '"].' + token_property

        if data_path != "":
            if index:
                driver = obj.driver_add(data_path, index)
            else:
                driver = obj.driver_add(data_path)
            sn_utils.add_driver_variables(driver, driver_vars)
            driver.driver.expression = expression
        else:
            print("Error: '" + self.name + "' not found while setting expression '" + expression + "'")


bpy.utils.register_class(Machine_Token)


class Machine_Point(PropertyGroup):

    machine_tokens: CollectionProperty(name="Machine Tokens",
                                       description="Collection of machine tokens ",
                                       type=Machine_Token)

    machine_token_index: IntProperty(name="Machine Token Index")

    def add_machine_token(self, name, token_type, face, edge="1"):
        token = self.machine_tokens.add()
        token.name = name
        token.type_token = token_type
        token.face = face
        token.edge = edge
        return token

    def draw_machine_tokens(self, layout):
        for token in self.machine_tokens:
            token.draw_properties(layout)


bpy.utils.register_class(Machine_Point)


class SnapObjectProps(PropertyGroup):
    show_driver_debug_info: BoolProperty(name="Show Driver Debug Info", default=False)
    pointers: CollectionProperty(name="Pointer Slots", type=Pointer_Slot)
    prompts: CollectionProperty(type=Prompt, name="Prompts")
    calculators: CollectionProperty(type=Calculator, name="Calculators")
    calculator_distance: FloatProperty(name="Calculator Distance", subtype='DISTANCE')
    prompt_index: IntProperty(name="Prompt Index")
    calculator_index: IntProperty(name="Calculator Index")
    pointer_name: StringProperty(name="Pointer Name")
    connected_object: bpy.props.PointerProperty(
        name="Connected Object",
        type=bpy.types.Object,
        description="This is the used to store objects that are connected together.")
    opengl_dim: PointerProperty(type=opengl_dim)
    accordion_view: PointerProperty(type=accordion_view)
    show_object_props: BoolProperty(name="Show Object Props", default=False)
    object_tabs: EnumProperty(name="Object Tabs",
                              items=[('MAIN', "Main", "Show the Main Properties"),
                                     ('DATA', "Data", "Show the Data"),
                                     ('MATERIAL', "Material", "Show the Materials"),
                                     ('MACHINE_TOKEN', "Machine Token", "Show the Machine Tokens")],
                              default='MAIN')

    placement_type: StringProperty(
        name="Placement Type",
        description="Type of placement for products and inserts 'STANDARD','CORNER','INTERIOR','EXTERIOR','SPLITTER'")

    interior_open: BoolProperty(
        name="Interior Open",
        description="Used for inserts to determine if an opening has an interior assembly",
        default=True)

    exterior_open: BoolProperty(
        name="Exterior Open",
        description="Used for inserts to determine if an opening has an exterior assembly",
        default=True)

    comment: StringProperty(name="Comment", description="Comment to store information for reporting.")
    comment_2: StringProperty(name="Comment 2", description="Comment 2 to store information for reporting.")
    comment_3: StringProperty(name="Comment 3", description="Comment 3 to store information for reporting.")

    edge_w1: StringProperty(name="Edge Width 1", description="Name of the edgebanding applied to Width 1")
    edge_l1: StringProperty(name="Edge Length 1", description="Name of the edgebanding applied to Length 1")
    edge_w2: StringProperty(name="Edge Width 2", description="Name of the edgebanding applied to Width 2")
    edge_l2: StringProperty(name="Edge Length 2", description="Name of the edgebanding applied to Length 2")

    cutpart_material_name: StringProperty(name="Cutpart Material Name", description="Name cutpart material name")
    edgeband_material_name: StringProperty(name="Edgeband Material Name", description="Edgeband material name")

    use_multiple_edgeband_pointers: BoolProperty(name="Use Multiple Edgeband Pointers", default=False)
    edgeband_material_name_l1: StringProperty(name="Edgeband Material Name L1", description="Edgeband material name L1")
    edgeband_material_name_l2: StringProperty(name="Edgeband Material Name L2", description="Edgeband material name L2")
    edgeband_material_name_w1: StringProperty(name="Edgeband Material Name W1", description="Edgeband material name W1")
    edgeband_material_name_w2: StringProperty(name="Edgeband Material Name W2", description="Edgeband material name W2")
    solid_stock: StringProperty(name="Solid Stock", description="Name of the solid stock material applied to the obj")

    mp: PointerProperty(name="Machine Point",
                        description="Machining Point",
                        type=Machine_Point)

    type_mesh: EnumProperty(name="Mesh Type",
                            items=[('NONE', "None", "None"),
                                   ('CUTPART', "Cut Part", "Cut Part"),
                                   ('EDGEBANDING', "Edgebanding", "Edgebanding"),
                                   ('SOLIDSTOCK', "Solid Stock", "Solid Stock"),
                                   ('HARDWARE', "Hardware", "Hardware"),
                                   ('BUYOUT', "Buyout", "Buyout"),
                                   ('MACHINING', "Machining", "Machining")],
                            description="Select the Mesh Type.",
                            default='NONE')

    spec_group_name: StringProperty(name="Specification Group Name",
                                    description="Current name of the specification group that is assigned to the group.")

    spec_group_index: IntProperty(name="Specification Group Index")

    material_slots: CollectionProperty(name="Material Slot Collection",
                                       description="Collection of material slots used ",
                                       type=Material_Slot)

    cutpart_name: StringProperty(name="Cutpart Name")
    edgepart_name: StringProperty(name="Edgepart Name")

    dont_export: BoolProperty(name="Dont Export",
                              description="If this is true then the assembly will not be exported for manufacturing",
                              default=False)

    export_product_subassemblies: BoolProperty(
        name="Export Product Subassemblies",
        description="If this is true then all of the inserts marked as a subassembly will be export to microvellum as a unique subassembly",
        default=False)

    export_as_subassembly: BoolProperty(
        name="Export As Subassembly",
        description="If this is true then the assembly will be exported as a subassembly",
        default=False)

    export_nested_subassemblies: BoolProperty(
        name="Export Nested Subassemblies",
        description="If this is true then the assembly will export any nested assemblies",
        default=False
        )                                      

    type_group: EnumProperty(name="Group Type",
                             items=[('NONE', "None", "None"),
                                    ('PRODUCT', "Product", "Product"),
                                    ('INSERT', "Insert", "Insert"),
                                    ('SPLITTER', "Splitter", "Splitter"),
                                    ('OPENING', "Opening", "Opening")],
                             description="Stores the Group Type.",
                             default='NONE')

    item_number: IntProperty(name="Item Number")
    name_object: StringProperty(name="Object Name", description="This is the readable name of the object")

    is_wall_mesh: BoolProperty(name="Is Wall Mesh",
                               description="Determines if the object is a wall mesh.",
                               default=False)

    plan_draw_id: StringProperty(name="Plan Draw ID",
                                 description="This property allows products to have a custom 2D plan view drawing. This is the operator bl_id.")

    is_cabinet_pull: BoolProperty(name="Is Cabinet Pull",
                                   description="Determines if the object is a cabinet pull.",
                                   default=False)

    class_name: StringProperty(name="Class Name", description="This is the python class name the assembly is from")

    delete_protected: BoolProperty(name='Delete Protected', description='Flag for sn_object.delete', default=False)

    def add_prompt(self, prompt_type, prompt_name):
        prompt = self.prompts.add()
        prompt.prompt_type = prompt_type
        prompt.name = prompt_name
        return prompt

    def add_calculator(self, calculator_name, calculator_object):
        calculator = self.calculators.add()
        calculator.distance_obj = calculator_object
        calculator.name = calculator_name
        return calculator

    def add_data_driver(self, property_name, index, expression, variables):
        if index == -1:
            driver = self.id_data.data.driver_add(property_name)
        else:
            driver = self.id_data.data.driver_add(property_name, index)
        sn_utils.add_driver_variables(driver, variables)
        driver.driver.expression = expression

    def add_driver(self, property_name, index, expression, variables):
        if index == -1:
            driver = self.id_data.driver_add(property_name)
        else:
            driver = self.id_data.driver_add(property_name, index)
        sn_utils.add_driver_variables(driver, variables)
        driver.driver.expression = expression

    def delete_prompt(self, name):
        for index, prompt in enumerate(self.prompts):
            if prompt.name == name:
                self.prompts.remove(index)

    def draw_prompts(self, layout):
        row = layout.row(align=True)
        row.scale_y = 1.3
        props = row.operator('sn_prompt.add_prompt', icon='LINENUMBERS_ON')
        props.obj_name = self.id_data.name
        props = row.operator('sn_prompt.add_calculator', icon='SYNTAX_ON')
        props.obj_name = self.id_data.name
        for prompt in self.prompts:
            prompt.draw(layout)
        for cal in self.calculators:
            cal.draw(layout)

    def get_var(self, data_path, name):
        return Variable(self.id_data, data_path, name)

    def get_prompt(self, prompt_name):
        if prompt_name in self.prompts:
            return self.prompts[prompt_name]

    def modifier(self, modifier, property_name, index=-1, expression="", variables=[]):
        driver = modifier.driver_add(property_name, index)
        sn_utils.add_driver_variables(driver, variables)
        driver.driver.expression = expression

    def hide(self, expression, variables):
        driver = self.id_data.driver_add('hide_viewport')
        sn_utils.add_driver_variables(driver, variables)
        driver.driver.expression = expression
        driver = self.id_data.driver_add('hide_render')
        sn_utils.add_driver_variables(driver, variables)
        driver.driver.expression = expression

    def loc_x(self, expression="", variables=[], value=0):
        if expression == "":
            self.id_data.location.x = value
            return
        driver = self.id_data.driver_add('location', 0)
        sn_utils.add_driver_variables(driver, variables)
        driver.driver.expression = expression

    def loc_y(self, expression="", variables=[], value=0):
        if expression == "":
            self.id_data.location.y = value
            return
        driver = self.id_data.driver_add('location', 1)
        sn_utils.add_driver_variables(driver, variables)
        driver.driver.expression = expression

    def loc_z(self, expression="", variables=[], value=0):
        if expression == "":
            self.id_data.location.z = value
            return
        driver = self.id_data.driver_add('location', 2)
        sn_utils.add_driver_variables(driver, variables)
        driver.driver.expression = expression

    def rot_x(self, expression="", variables=[], value=0):
        if expression == "":
            self.id_data.rotation_euler.x = value
            return
        driver = self.id_data.driver_add('rotation_euler', 0)
        sn_utils.add_driver_variables(driver, variables)
        driver.driver.expression = expression

    def rot_y(self, expression="", variables=[], value=0):
        if expression == "":
            self.id_data.rotation_euler.y = value
            return
        driver = self.id_data.driver_add('rotation_euler', 1)
        sn_utils.add_driver_variables(driver, variables)
        driver.driver.expression = expression

    def rot_z(self, expression="", variables=[], value=0):
        if expression == "":
            self.id_data.rotation_euler.z = value
            return
        driver = self.id_data.driver_add('rotation_euler', 2)
        sn_utils.add_driver_variables(driver, variables)
        driver.driver.expression = expression

    @classmethod
    def register(cls):
        bpy.types.Object.snap = PointerProperty(
            name="SNaP",
            description="SNaP Object Properties",
            type=cls
        )

    @classmethod
    def unregister(cls):
        del bpy.types.Object.snap


class library_items(PropertyGroup):
    is_selected: BoolProperty(name="Is Selected")
    name: StringProperty(name="Library Item Name")


class Library_Package(bpy.types.PropertyGroup):
    lib_path: StringProperty(name="Library Path", subtype='DIR_PATH', update=update_library_paths)
    enabled: BoolProperty(name="Enabled", default=True, update=update_library_paths)


class sn_image(PropertyGroup):
    image_name: StringProperty(name="Image Name",
                               description="The Image name that is assign to the image view")

    is_plan_view: BoolProperty(name="Is Plan View",
                               default=False,
                               description="This determines if the image is a 2D Plan View")

    is_elv_view: BoolProperty(name="Is Elv View",
                              default=False,
                              description="This determines if the image is a 2D Elevation View")

    is_acc_view: BoolProperty(name="Is Accordion View",
                              default=False,
                              description="This determines if the image is a 2D Accordion View")
    
    is_island_view: BoolProperty(name="Is Island View",
                                 default=False,
                                 description="This determines if the image is a 2D Island View")

    is_virtual_view: BoolProperty(name="Is Virtual View",
                                  default=False,
                                  description="This determines if the image is a Virtual View - Used only to form elevations occlusions")


class SnapWindowManagerProps(PropertyGroup):
    libraries: CollectionProperty(name="Libraries", type=Library)
    assets: CollectionProperty(name='Assets', type=Asset)

    library_types: EnumProperty(
        name="Library Types",
        items=[
            ('PRODUCT',"Product","Product"),
            ('INSERT',"Insert","Insert")],
        default='PRODUCT')

    lib_products: CollectionProperty(name="Library Products", type=List_Library)
    lib_product_index: IntProperty(name="Library Product Index", default=0)
    lib_inserts: CollectionProperty(name="Library Inserts", type=List_Library)
    lib_insert_index: IntProperty(name="Library Insert Index", default=0)
    lib_insert: PointerProperty(name="Library Insert", type=List_Library)
    current_item: IntProperty(name="Current Item", default=0)
    total_items: IntProperty(name="Total Items", default=0)

    use_opengl_dimensions: BoolProperty(name="Use OpenGL Dimensions",
                                        description="Use OpenGL Dimensions",
                                        default=False)

    elevation_scene_index: IntProperty(name="2d Elevation Scene Index",
                                       default=0,
                                       update=update_scene_index)

    library_packages: CollectionProperty(name="Library Packages", type=Library_Package)

    library_module_path: StringProperty(name="Library Module Path", default="",
                                        subtype='DIR_PATH', update=update_library_paths)
    assembly_library_path: StringProperty(name="Assembly Library Path", default="",
                                          subtype='DIR_PATH', update=update_library_paths)
    object_library_path: StringProperty(name="Object Library Path", default="",
                                        subtype='DIR_PATH', update=update_library_paths)
    material_library_path: StringProperty(name="Material Library Path", default="",
                                          subtype='DIR_PATH', update=update_library_paths)
    world_library_path: StringProperty(name="World Library Path", default="",
                                       subtype='DIR_PATH', update=update_library_paths)

    image_views: CollectionProperty(name="Image Views",
                                    type=sn_image,
                                    description="Collection of all of the views to be printed.")

    image_view_index: IntProperty(name="Image View Index",
                                  default=0)

    def get_library_assets(self):
        library_path = sn_paths.CLOSET_THUMB_DIR

        for asset in self.assets:
            self.assets.remove(0)

        for lib in LIBRARIES:
            for name, obj in inspect.getmembers(lib):
                if hasattr(obj, 'show_in_library') and name != 'ops' and obj.show_in_library:
                    asset = self.assets.add()
                    asset.asset_path = " "
                    asset.name = name.replace("_", " ")
                    asset.category_name = obj.category_name
                    asset.library_path = os.path.join(library_path, asset.category_name)
                    asset.package_name = lib.__name__.split(".")[-2]
                    asset.module_name = lib.__name__.split(".")[-1]
                    asset.class_name = name

    def get_asset(self, filepath):
        directory, file = os.path.split(filepath)
        filename, ext = os.path.splitext(file)
        obj = None

        for lib in LIBRARIES:
            for asset in self.assets:
                item_name = asset.name.replace("PRODUCT ", "").replace("INSERT ", "")
                if filename == item_name:
                    if hasattr(lib, asset.class_name):
                        asset_cls = getattr(lib, asset.class_name)
                        obj = asset_cls()
                        break
        if obj:
            return obj
        else:
            bpy.ops.snap.message_box(
                'INVOKE_DEFAULT',
                message="Could Not Find Class: {}".format(filename))

    def add_library(self, name, lib_type, root_dir, drop_id, icon, use_custom_icon, thumbnail_dir=""):
        lib = self.libraries.add()
        lib.name = name
        lib.lib_type = lib_type
        lib.root_dir = root_dir
        lib.drop_id = drop_id
        lib.use_custom_icon = use_custom_icon
        lib.icon = icon

        if lib.lib_type == 'SNAP':
            lib.thumbnail_dir = thumbnail_dir

        return lib

    def remove_library(self, name):
        for i, lib in enumerate(self.libraries):
            if lib.name == name:
                self.libraries.remove(i)

    @classmethod
    def register(cls):
        bpy.types.WindowManager.snap = PointerProperty(
            name="SNaP",
            description="SNaP Window Manager Properties",
            type=cls,
        )

    @classmethod
    def unregister(cls):
        del bpy.types.WindowManager.snap


class SnapInterface(PropertyGroup):

    render_type_tabs: EnumProperty(
        name="Render Type Tabs",
        items=enum_render_type,
        default='PRR')

    use_default_blender_interface: BoolProperty(
        name="Use Default Blender Interface",
        default=False,
        description="Show Default Blender interface")


class SnapSceneProps(PropertyGroup):
    assembly_tabs: EnumProperty(
        name="Assembly Tabs",
        items=[
            ('MAIN', "Main", "Show the Main Properties"),
            ('PROMPTS', "Prompts", "Show the Prompts"),
            ('OBJECTS', "Objects", "Show the Objects"),
            ('LOGIC', "Logic", "Show the Assembly Logic")],
        default='MAIN')

    driver_tabs: EnumProperty(
        name="Driver Tabs",
        items=[
            ('LOC_X', "Location X", "Show the X Location Driver"),
            ('LOC_Y', "Location Y", "Show the Y Location Driver"),
            ('LOC_Z', "Location Z", "Show the Z Location Driver"),
            ('ROT_X', "Rotation X", "Show the X Rotation Driver"),
            ('ROT_Y', "Rotation Y", "Show the Y Rotation Driver"),
            ('ROT_Z', "Rotation Z", "Show the Z Rotation Driver"),
            ('DIM_X', "Dimension X", "Show the X Dimension Driver"),
            ('DIM_Y', "Dimension Y", "Show the Y Dimension Driver"),
            ('DIM_Z', "Dimension Z", "Show the Z Dimension Driver"),
            ('PROMPTS', "Prompts", "Show the Prompt Drivers"),
            ('CALCULATORS', "Calculators", "Show the Calculator Drivers"),
            ('SELECTED_OBJECT', "Selected Object",
             "Show the Drivers for the Selected Object")],
        default='SELECTED_OBJECT')

    driver_override_object: PointerProperty(name="Active Library Name", type=bpy.types.Object)
    active_library_name: StringProperty(name="Active Library Name", default="")
    active_library: StringProperty(name="Active Library")
    active_category: StringProperty(name="Active Category")
    material_pointers: bpy.props.CollectionProperty(name="Material Pointers", type=Pointer)
    spec_group_tabs: EnumProperty(
        name="Library Tabs",
        items=[('GLOBALS',"Globals","Global Variable Options"),
                ('MATERIALS',"Materials","Rendering Materials"),
                ('CUTPARTS',"Cut Parts","Cut Parts for cabinets"),
                ('EDGEPARTS',"Library Builder","Edge banding for cabinets")],
        default = 'MATERIALS')
    spec_groups: bpy.props.CollectionProperty(name="Spec Groups", type=Specification_Group)
    spec_group_index: IntProperty(name="Spec Group Index", default=0)

    default_wall_height: FloatProperty(name="Default Wall Height",
                                       description="Enter the default height when drawings walls",
                                       default=inch(108),
                                       unit='LENGTH',
                                       subtype='DISTANCE',
                                       precision=5)
    default_wall_depth: FloatProperty(name="Default Wall Depth",
                                      description="Enter the default depth when drawings walls",
                                      default=inch(6),
                                      unit='LENGTH',
                                      subtype='DISTANCE',
                                      precision=5)

    opengl_dim: PointerProperty(type=opengl_dim)
    accordion_view: PointerProperty(type=accordion_view)

    scene_type: EnumProperty(
        name="SNaP Scene Type",
        items=[
            ('NONE', 'None', 'None'),
            ('ELEVATION', 'Elevation View', 'Elevation View'),
            ('PLAN_VIEW', 'Plan View', 'Plan View'),
            ('ACCORDION', 'Accordion View', 'Accordion View'),
            ('ISLAND', 'Island View', 'Island View'),
            ('VIRTUAL', 'Virtual View', 'Virtual View')
        ],
        default='NONE'
    )

    plan_view_scene: BoolProperty(
        name="Plan View Scene",
        description="Scene used for rendering project plan view",
        default=False)

    elevation_scene: BoolProperty(
        name="Elevation Scene",
        description="Scene used for rendering elevations",
        default=False)

    accordion_view_scene: BoolProperty(name="Accordion View Scene",
                                  description="Scene used for rendering project accordion view",
                                  default=False)

    island_view_scene: BoolProperty(name="Island View Scene",
                                  description="Scene used for rendering project island view",
                                  default=False)

    virtual_view_scene: BoolProperty(name="Virtual View Scene",
                                  description="Scene used only for creating occlusions at elevations",
                                  default=False)


    name_scene: StringProperty(name="Scene Name",
                               description="This is the readable name of the scene") 

    ui: PointerProperty(name="Interface", type=SnapInterface)

    initial_shade_mode: StringProperty(name="Initial Shade Mode")   

    initial_view_location: FloatVectorProperty(name="Initial View Location",
                                               size=3)

    initial_view_rotation: FloatVectorProperty(name="Initial View Rotation",
                                               size=4)

    elevation_selected: BoolProperty(name="Selected for Elevation Rendering")

    job_name: StringProperty(name="Job Name")

    job_number: StringProperty(name="Job Number")

    install_date: StringProperty(name="Install Date")

    designer_name: StringProperty(name="Designer Name")

    designer_phone: StringProperty(name="Designer Phone")

    client_name: StringProperty(name="Client Name")

    client_number: StringProperty(name="Client Number")

    client_phone: StringProperty(name="Client Phone")

    client_email: StringProperty(name="Client Email")

    job_comments: StringProperty(name="Job Comments")

    tear_out: StringProperty(name="Tear Out (Y/N)")

    touch_up: StringProperty(name="Touch Up (Y/N)")

    block_wall: StringProperty(name="Block Wall (Y/N)")

    new_construction: StringProperty(name="New Construction (Y/N)")

    elevator: StringProperty(name="Elevator (Y/N)")

    stairs: StringProperty(name="Stairs (Y/N)")
    
    floor: StringProperty(name="Floor Type")
    
    door: StringProperty(name="Door Type")
    
    base_height: StringProperty(name="Baseboard Height")
    
    parking: StringProperty(name="Parking Instructions")

    @classmethod
    def register(cls):
        bpy.types.Scene.snap = PointerProperty(
            name="SNaP Scene Properties",
            description="SNaP Scene Properties",
            type=cls,
        )

    @classmethod
    def unregister(cls):
        del bpy.types.Scene.snap


class SnapAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def expand_adv_opts(self, context):
        self.expand_dev_panel = self.use_adv_options

    designer_id: IntProperty(name="Designer ID", description="Desiger ID")
    project_id_count: IntProperty(name="Project ID", description="Project ID")
    project_dir: StringProperty(
        name="Projects Directory",
        subtype='DIR_PATH',
        default=os.path.join(os.path.expanduser("~"), "Documents", "SNaP Projects"))
    assets_filepath: StringProperty(
        name="Assets Filepath",
        subtype='FILE_PATH')
    debug_mode: BoolProperty(
        name="Debug Mode",
        description="If enabled, run in debug mode",
        default=DEV_TOOLS_AVAILABLE)
    debug_updater: BoolProperty(
        name="Debug Updater",
        description="If enabled, run updater in debug mode",
        default=False)
    debug_export: BoolProperty(
        name="Debug XML Export",
        description="If enabled, run XML export in debug mode",
        default=False,)
    debug_mac: BoolProperty(
        name="Debug Machining Export",
        description="If enabled, create machining debug parts",
        default=False,)
    expand_dev_panel: BoolProperty(
        name="Expand Development Panel",
        description="Expand Development panel for advanced options",
        default=False,)
    use_adv_options: BoolProperty(
        name="SNaP Advanced options",
        description="Use advanced options",
        default=False,
        update=expand_adv_opts)
    default_csv_path: StringProperty(
        name="Default CSV Filepath",
        subtype='FILE_PATH',
        default=sn_paths.CSV_PATH)

    enable_franchise_pricing: BoolProperty(
        name="Enable Franchise Pricing View",
        description="If enabled, show franchise pricing in Project Pricing",
        default=False)

    franchise_location: EnumProperty(name="",
                                description="Select Franchise Materials List Location",
                                   items=[('PHX',"Phoenix",'Phoenix'),
                                          ('DAL',"Dallas",'Dallas'),
                                          ('SD',"San Diego",'San Diego'),
                                          ('DEN',"Denver",'Denver'),
                                          ('5',"Location 5",'5'),
                                          ('6',"Location 6",'6'),
                                          ('7',"Location 7",'7'),
                                          ('8',"Location 8",'8'),
                                          ('9',"Location 9",'9')],
                                   default = 'PHX')

    auto_check_update: bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=True)

    updater_interval_months: bpy.props.IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        min=0)

    updater_interval_days: bpy.props.IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=7,
        min=0,
        max=31)

    updater_interval_hours: bpy.props.IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23)

    updater_interval_minutes: bpy.props.IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59)

    updater_key: StringProperty(
        name="Access Key",
        default="")

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row = box.row()
        split = row.split(factor=0.5)
        row = split.row()
        row.label(text="Designer ID:")
        row.prop(self, "designer_id", text="")
        box.prop(self, "project_dir", text="Projects Directory")

        box = layout.box()
        box.label(text="Franchise Materials Locations")
        row = box.row()
        row.prop(self, "franchise_location")

        row = layout.row(align=True)
        row.prop(
            self,
            "expand_dev_panel",
            text="",
            icon='TRIA_DOWN' if self.expand_dev_panel else 'TRIA_RIGHT',
            emboss=False)
        row.prop(self, "use_adv_options", text="")
        row.label(text="SNaP Advanced options")

        if self.expand_dev_panel:
            box = layout.box()
            box.enabled = self.use_adv_options
            row = box.row()
            row.prop(self, "debug_mode")
            row.prop(self, "debug_mac")
            row = box.row()
            row.prop(self, "enable_franchise_pricing")

            addon_updater_ops.update_settings_ui(self, context)


classes = (
    SnapInterface,
    opengl_dim,  # TODO: tmp
    accordion_view,
    Combobox_Item,
    Library_Item,
    Library,
    Pointer_Slot,
    Pointer,
    Material_Slot,
    List_Library_Item,
    List_Library,
    Library_Pointer,
    Cutpart,
    Edgepart,
    Specification_Group,
    Asset,
    Prompt,
    Calculator_Prompt,
    Calculator,
    sn_image,  # TODO: tmp1
    Library_Package,  # TODO: tmp
    library_items,  # TODO: tmp
    SnapObjectProps,
    SnapWindowManagerProps,
    SnapSceneProps,
    SnapAddonPreferences,
)


def register():
    for cls in classes:
        register_class(cls)


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)
