import bpy
import math
import os
from snap import sn_types, sn_utils, sn_unit, sn_paths

WINDOW_FRAMES = os.path.join(sn_paths.DOORS_AND_WINDOWS_ROOT, 'assets', 'Windows', "Window Frames")
WINDOW_GLASS = os.path.join(sn_paths.DOORS_AND_WINDOWS_ROOT, 'assets', 'Windows', "Window Glass")

MATERIAL_FILE = os.path.join(sn_paths.DOORS_AND_WINDOWS_ROOT, 'assets', 'Windows', "materials", "materials.blend")
HEIGHT_ABOVE_FLOOR = sn_unit.inch(40.0)
DEFAULT_WIDTH = sn_unit.inch(36.0)
DEFAULT_HEIGHT = sn_unit.inch(36.0)
DEFAULT_DEPTH = sn_unit.inch(6.5)


class Window(sn_types.Assembly):
    library_name = "Windows"
    category_name = ""
    assembly_name = ""
    id_prompt = "sn_entry_windows.window_prompts"
    show_in_library = True
    type_assembly = "PRODUCT"
    mirror_z = False
    mirror_y = False
    width = 0
    height = 0
    depth = 0

    height_above_floor = 0
    window_frame = ""
    window_divider = ""
    window_blinds = ""

    def update(self):
        super().update()
        self.obj_bp["IS_BP_WINDOW"] = True
        if hasattr(self, 'assembly_name'):
            self.set_name(self.assembly_name)
        self.obj_x.location.x = self.width
        if self.obj_bp.get('mirror_y'):
            self.obj_y.location.y = -self.depth
        else:
            self.obj_y.location.y = self.depth

        if self.obj_bp.get('mirror_z'):
            self.obj_z.location.z = -self.height
        else:
            self.obj_z.location.z = self.height

        self.loc_z(value=self.height_above_floor)

    def draw(self):
        self.create_assembly()
        self.obj_bp.snap.dont_export = True

        self.obj_bp['ID_PROMPT'] = self.id_prompt

        self.add_prompt("Array X", 'QUANTITY', 1)
        self.add_prompt("Array X Offset", 'DISTANCE', sn_unit.inch(6))

        Width = self.obj_x.snap.get_var("location.x", "Width")
        Height = self.obj_z.snap.get_var("location.z", "Height")
        Depth = self.obj_y.snap.get_var("location.y", "Depth")
        Array_X = self.get_prompt("Array X").get_var()
        Array_X_Offset = self.get_prompt("Array X Offset").get_var()

        frame = self.add_assembly_from_file(os.path.join(WINDOW_FRAMES, self.window_frame))
        frame = sn_types.Part(obj_bp=frame)

        frame.set_name(self.window_frame)
        frame.dim_x('Width', [Width])
        frame.dim_y('Depth', [Depth])
        frame.dim_z('Height', [Height])
        Array_X_prompt = frame.add_prompt("Array X", "QUANTITY", 1)
        Array_X_prompt.set_formula("Array_X", [Array_X])

        Array_X_Offset_prompt = frame.add_prompt("Array X Offset", "DISTANCE", sn_unit.inch(6))
        Array_X_Offset_prompt.set_formula("Array_X_Offset", [Array_X_Offset])
        frame.assign_material("Glass", MATERIAL_FILE, "Glass")
        frame.assign_material("Frame", MATERIAL_FILE, "White")
        frame.draw_as_hidden_line()

        if self.window_frame == "Window_Frame_Hung.blend":
            # we need the min and max height, which were previously included directly in the blend file
            # the actual variables pointing to these values are in the frame hung blend file
            frame.add_prompt("Min Height", "FLOAT", 0)
            frame.add_prompt("Max Height", "FLOAT", 48)

            # we also need to add the proper prompts


        if self.window_divider != "":
            if self.window_frame == "Window_Frame_Fixed.blend":
                divider = self.add_assembly_from_file(os.path.join(WINDOW_GLASS, self.window_divider))
                divider = sn_types.Part(obj_bp=divider)

                divider.set_name(self.window_divider)
                divider.loc_x(value=sn_unit.inch(4.0))
                divider.loc_y(value=sn_unit.inch(3.86))
                divider.loc_z(value=sn_unit.inch(2.75))
                divider.dim_x('Width-INCH(8.0)', [Width])
                divider.dim_z('Height-INCH(6.75)', [Height])
                Array_X_prompt = divider.add_prompt("Array X", "QUANTITY", 1)
                Array_X_prompt.set_formula("Array_X", [Array_X])
                Array_X_Offset_prompt = divider.add_prompt("Array X Offset", "DISTANCE", sn_unit.inch(6))
                Array_X_Offset_prompt.set_formula("Width+Array_X_Offset", [Array_X_Offset, Width])
                divider.assign_material("Frame", MATERIAL_FILE, "White")

            if self.window_frame == "Window_Frame_Hung.blend":
                divider_1 = self.add_assembly_from_file(os.path.join(WINDOW_GLASS, self.window_divider))
                divider_1 = sn_types.Part(obj_bp=divider_1)

                divider_1.set_name(self.window_divider + " 1")
                divider_1.loc_x(value=sn_unit.inch(4.0))
                divider_1.loc_y(value=sn_unit.inch(3.86))
                divider_1.loc_z(value=sn_unit.inch(2.75))
                divider_1.dim_x('Width-INCH(8)', [Width])
                divider_1.dim_z('(Height*0.5)-INCH(5)', [Height])
                Array_X_prompt = divider_1.add_prompt("Array X", "QUANTITY", 1)
                Array_X_prompt.set_formula("Array_X", [Array_X])
                Array_X_Offset_prompt = divider_1.add_prompt("Array X Offset", "DISTANCE", sn_unit.inch(6))
                Array_X_Offset_prompt.set_formula("Width+Array_X_Offset", [Array_X_Offset, Width])
                divider_1.assign_material("Frame", MATERIAL_FILE, "White")

                divider_2 = self.add_assembly_from_file(os.path.join(WINDOW_GLASS, self.window_divider))
                divider_2 = sn_types.Part(obj_bp=divider_2)

                divider_2.set_name(self.window_divider + " 2")
                divider_2.loc_x(value=sn_unit.inch(3))
                divider_2.loc_y(value=sn_unit.inch(3))
                divider_2.loc_z('Height*0.5', [Height])
                divider_2.dim_x('Width-INCH(6)', [Width])
                divider_2.dim_z('(Height*0.5)-INCH(3)', [Height])
                Array_X_prompt = divider_2.add_prompt("Array X", "QUANTITY", 1)
                Array_X_prompt.set_formula("Array_X", [Array_X])
                Array_X_Offset_prompt = divider_2.add_prompt("Array X Offset", "DISTANCE", sn_unit.inch(6))
                Array_X_Offset_prompt.set_formula("Width+Array_X_Offset", [Array_X_Offset, Width])
                divider_2.assign_material("Frame", MATERIAL_FILE, "White")

            if self.window_frame == "Window_Frame_Sliding.blend":
                divider_1 = self.add_assembly_from_file(os.path.join(WINDOW_GLASS, self.window_divider))
                divider_1 = sn_types.Part(obj_bp=divider_1)

                divider_1.set_name(self.window_divider + " 1")
                divider_1.loc_x(value=sn_unit.inch(3.5))
                divider_1.loc_y(value=sn_unit.inch(3.86))
                divider_1.loc_z(value=sn_unit.inch(2))
                divider_1.dim_x('(Width*0.5)-INCH(4)', [Width])
                divider_1.dim_z('Height-INCH(5.5)', [Height])
                Array_X_prompt = divider_1.add_prompt("Array X", "QUANTITY", 1)
                Array_X_prompt.set_formula("Array_X", [Array_X])
                Array_X_Offset_prompt = divider_1.add_prompt("Array X Offset", "DISTANCE", sn_unit.inch(6))
                Array_X_Offset_prompt.set_formula("Width+Array_X_Offset", [Array_X_Offset, Width])
                divider_1.assign_material("Frame", MATERIAL_FILE, "White")

                divider_2 = self.add_assembly_from_file(os.path.join(WINDOW_GLASS, self.window_divider))
                divider_2 = sn_types.Part(obj_bp=divider_2)

                divider_2.set_name(self.window_divider + " 2")
                divider_2.loc_x('(Width*0.5)+INCH(0.75)', [Width])
                divider_2.loc_y(value=sn_unit.inch(3))
                divider_2.loc_z(value=sn_unit.inch(1.5))
                divider_2.dim_x('(Width*0.5)-INCH(3.25)', [Width])
                divider_2.dim_z('Height-INCH(4)', [Height])
                Array_X_prompt = divider_2.add_prompt("Array X", "QUANTITY", 1)
                Array_X_prompt.set_formula("Array_X", [Array_X])
                Array_X_Offset_prompt = divider_2.add_prompt("Array X Offset", "DISTANCE", sn_unit.inch(6))
                Array_X_Offset_prompt.set_formula("Width+Array_X_Offset", [Array_X_Offset, Width])
                divider_2.assign_material("Frame", MATERIAL_FILE, "White")

            if self.window_frame == "Window_Frame_Triple.blend":
                divider = self.add_assembly_from_file(os.path.join(WINDOW_GLASS, self.window_divider))
                divider = sn_types.Part(obj_bp=divider)

                divider.set_name(self.window_divider + " 1")
                divider.loc_x(value=sn_unit.inch(15))
                divider.loc_y(value=sn_unit.inch(3))
                divider.loc_z(value=sn_unit.inch(1.5))
                divider.dim_x('Width-INCH(30)', [Width])
                divider.dim_z('Height-INCH(13.5)', [Height])
                Array_X_prompt = divider.add_prompt("Array X", "QUANTITY", 1)
                Array_X_prompt.set_formula("Array_X", [Array_X])
                Array_X_Offset_prompt = divider.add_prompt("Array X Offset", "DISTANCE", sn_unit.inch(6))
                Array_X_Offset_prompt.set_formula("Width+Array_X_Offset", [Array_X_Offset, Width])
                divider.assign_material("Frame", MATERIAL_FILE, "White")

        self.update()


class PROMPTS_Window_Prompts(bpy.types.Operator):
    bl_idname = "sn_entry_windows.window_prompts"
    bl_label = "Window Prompts"
    bl_options = {'UNDO'}

    object_name: bpy.props.StringProperty(name="Object Name")

    product = None

    width: bpy.props.FloatProperty(name="Width", unit='LENGTH', precision=4)
    height: bpy.props.FloatProperty(name="Height", unit='LENGTH', precision=4)
    depth: bpy.props.FloatProperty(name="Depth", unit='LENGTH', precision=4)

    loc_x: bpy.props.FloatProperty(name="X Location", unit='LENGTH', precision=4)

    base_point: bpy.props.EnumProperty(name="Main Tabs",
                                       items=[('LEFT', "Left", 'Left'),
                                              ('CENTER', "Center", 'Center'),
                                              ('RIGHT', "Right", 'Right')],
                                       default='LEFT')

    array_x: bpy.props.IntProperty(name="Array X", min=0,)

    array_x_offset: bpy.props.FloatProperty(name="Array X Offset", unit='LENGTH', precision=4)

    array_x_prompt = None

    array_x_offset_prompt = None

    start_x = 0
    start_width = 0

    @classmethod
    def poll(cls, context):
        return True

    def check(self, context):
        self.product.obj_x.location.x = self.width

        if self.base_point == 'LEFT':
            self.product.obj_bp.location.x = self.loc_x
        elif self.base_point == 'CENTER':
            self.product.obj_bp.location.x = self.loc_x - (self.product.obj_x.location.x - self.start_width) / 2
        else:
            self.product.obj_bp.location.x = self.loc_x - (self.product.obj_x.location.x - self.start_width)

        if self.product.obj_bp.get('mirror_y'):
            self.product.obj_y.location.y = -self.depth
        else:
            self.product.obj_y.location.y = self.depth

        if self.product.obj_bp.get('mirror_z'):
            self.product.obj_z.location.z = -self.height
        else:
            self.product.obj_z.location.z = self.height

        if self.array_x_prompt:
            self.array_x_prompt.set_value(self.array_x)

        if self.array_x_offset_prompt:
            self.array_x_offset_prompt.set_value(self.array_x_offset)

        self.product.obj_bp.location = self.product.obj_bp.location
        self.product.obj_bp.location = self.product.obj_bp.location

        return True

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        obj = context.object
        obj_product_bp = sn_utils.get_bp(obj, 'PRODUCT')
        self.product = sn_types.Part(obj_product_bp)
        if self.product.obj_bp:
            self.depth = math.fabs(self.product.obj_y.location.y)
            self.height = math.fabs(self.product.obj_z.location.z)
            self.width = math.fabs(self.product.obj_x.location.x)

            self.start_x = self.product.obj_bp.location.x
            self.loc_x = self.product.obj_bp.location.x
            self.start_width = math.fabs(self.product.obj_x.location.x)

            self.array_x_prompt = self.product.get_prompt("Array X")
            self.array_x = self.array_x_prompt.get_value()

            self.array_x_offset_prompt = self.product.get_prompt("Array X Offset")
            self.array_x_offset = self.array_x_offset_prompt.get_value()

        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=480)

    def draw_product_size(self, layout):
        row = layout.row()
        box = row.box()
        col = box.column(align=True)

        row1 = col.row(align=True)
        if self.object_has_driver(self.product.obj_x):
            row1.label(text='Width: ' + str(sn_unit.meter_to_active_unit(math.fabs(self.product.obj_x.location.x))))
        else:
            row1.label(text='Width:')
            row1.prop(self, 'width', text="")
            row1.prop(self.product.obj_x, 'hide_viewport', text="")

        row1 = col.row(align=True)
        if self.object_has_driver(self.product.obj_z):
            row1.label(text='Height: ' + str(sn_unit.meter_to_active_unit(math.fabs(self.product.obj_z.location.z))))
        else:
            row1.label(text='Height:')
            row1.prop(self, 'height', text="")
            row1.prop(self.product.obj_z, 'hide_viewport', text="")

        row1 = col.row(align=True)
        if self.object_has_driver(self.product.obj_y):
            row1.label(text='Depth: ' + str(sn_unit.meter_to_active_unit(math.fabs(self.product.obj_y.location.y))))
        else:
            row1.label(text='Depth:')
            row1.prop(self, 'depth', text="")
            row1.prop(self.product.obj_y, 'hide_viewport', text="")

    def object_has_driver(self, obj):
        if obj.animation_data:
            if len(obj.animation_data.drivers) > 0:
                return True

    def draw_product_prompts(self, layout):

        array_x = self.product.get_prompt("Array X")
        array_x_offset = self.product.get_prompt("Array X Offset")

        box = layout.box()
        box.label(text="Main Options:")

        col = box.column()
        row = col.row(align=True)
        row.label(text="Array X:")
        row.prop(self, 'array_x', text="",)
        row = col.row(align=True)
        row.label(text="Array X Offset:")
        row.prop(self, 'array_x_offset', text="")

    def draw_product_placment(self, layout):
        box = layout.box()
        col = box.column()
        row = col.row(align=True)
        row.label(text='Location X:')
        row.prop(self, 'loc_x', text="")
        row = col.row(align=True)
        row.label(text='Location Z:')
        row.prop(self.product.obj_bp, 'location', index=2, text="")

    def draw(self, context):
        layout = self.layout
        if self.product.obj_bp:
            if self.product.obj_bp.name in context.scene.objects:
                box = layout.box()

                split = box.split(factor=.8)
                split.label(text=self.product.obj_bp.name, icon='LATTICE_DATA')
                row = box.row()
                row.label(text="Set Base Point:")
                row.prop(self, 'base_point', expand=True)
                self.draw_product_size(box)
                self.draw_product_placment(box)
                self.draw_product_prompts(box)


def register():
    bpy.utils.register_class(PROMPTS_Window_Prompts)


def unregister():
    bpy.utils.unregister_class(PROMPTS_Window_Prompts)
