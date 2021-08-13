from os import path
import math

import bpy
from bpy.props import (
    StringProperty,
    FloatProperty,
    EnumProperty
)

from snap import sn_types, sn_unit, sn_utils
from .. import closet_props
from ..common import common_parts
from ..common import common_prompts
from .. import closet_props


class Wall_Cleat(sn_types.Assembly):

    type_assembly = "PRODUCT"
    id_prompt = "closet.wall_cleat"
    #drop_id = "sn_closets.place_wall_cleat"
    show_in_library = True
    category_name = "Closet Products - Add Pards"

    def update(self):
        self.obj_x.location.x = self.width
        self.obj_z.location.z = self.height
        self.obj_y.location.y = -self.depth

        self.obj_bp['ID_PROMPT'] = self.id_prompt
        self.obj_bp["IS_BP_CLOSET"] = True
        self.obj_bp["IS_BP_WALL_CLEAT"] = True
        self.obj_bp.snap.type_group = self.type_assembly
        self.obj_bp.snap.export_as_subassembly = True
        props = self.obj_bp.sn_closets
        props.is_cleat = True
        super().update()

    def draw(self):
        self.create_assembly()

        self.add_prompt("Height", 'DISTANCE', sn_unit.inch(3.64))  # TODO: Remove
        self.add_prompt("Distance Above Floor", 'DISTANCE', sn_unit.inch(60))
        self.add_prompt("Exposed Top", 'CHECKBOX', False)
        self.add_prompt("Exposed Left", 'CHECKBOX', False)
        self.add_prompt("Exposed Right", 'CHECKBOX', False)
        self.add_prompt("Exposed Bottom", 'CHECKBOX', False) 

        common_prompts.add_thickness_prompts(self)

        Width = self.obj_x.snap.get_var("location.x", "Width")
        Height = self.get_prompt("Height").get_var("Height")
        Distance_Above_Floor = self.get_prompt('Distance Above Floor').get_var("Distance_Above_Floor")
        Panel_Thickness = self.get_prompt('Panel Thickness').get_var("Panel_Thickness")
        Exposed_Left = self.get_prompt('Exposed Left').get_var('Exposed_Left')
        Exposed_Right = self.get_prompt('Exposed Right').get_var('Exposed_Right')
        Exposed_Bottom = self.get_prompt('Exposed Bottom').get_var('Exposed_Bottom')
        Exposed_Top = self.get_prompt('Exposed Top').get_var('Exposed_Top')

        cleat = common_parts.add_wall_cleat(self)
        cleat.obj_bp.snap.comment_2 = "1024"
        cleat.set_name("Cleat")

        cleat.loc_z('Distance_Above_Floor', [Distance_Above_Floor])
        cleat.rot_x(value=math.radians(-90))

        cleat.dim_x('Width', [Width])
        cleat.dim_y('-Height', [Height])
        cleat.dim_z('-Panel_Thickness', [Panel_Thickness])

        cleat.get_prompt('Exposed Left').set_formula('Exposed_Left', [Exposed_Left])
        cleat.get_prompt('Exposed Right').set_formula('Exposed_Right', [Exposed_Right])
        cleat.get_prompt('Exposed Bottom').set_formula('Exposed_Bottom', [Exposed_Bottom])
        cleat.get_prompt('Exposed Top').set_formula('Exposed_Top', [Exposed_Top])

        self.update()


class PROMPTS_Wall_Cleat_Prompts(sn_types.Prompts_Interface):
    bl_idname = "closet.wall_cleat"
    bl_label = "Wall Cleat Prompts"
    bl_options = {'UNDO'}
    
    object_name: StringProperty(name="Object Name",
                                           description="Stores the Base Point Object Name \
                                           so the object can be retrieved from the database.")
    
    width: FloatProperty(name="Width",unit='LENGTH',precision=4)
    height: FloatProperty(name="Height",unit='LENGTH',precision=4)
    depth: FloatProperty(name="Depth",unit='LENGTH',precision=4)


    placement_on_wall: EnumProperty(name="Placement on Wall",items=[('SELECTED_POINT',"Selected Point",""),
                                                                     ('FILL',"Fill",""),
                                                                     ('FILL_LEFT',"Fill Left",""),
                                                                     ('LEFT',"Left",""),
                                                                     ('CENTER',"Center",""),
                                                                     ('RIGHT',"Right",""),
                                                                     ('FILL_RIGHT',"Fill Right","")],default = 'SELECTED_POINT')

    current_location: FloatProperty(name="Current Location", default=0,subtype='DISTANCE')
    left_offset: FloatProperty(name="Left Offset", default=0,subtype='DISTANCE')
    right_offset: FloatProperty(name="Right Offset", default=0,subtype='DISTANCE') 

    product = None

    selected_location = 0
    default_width = 0

    def check(self, context):
        self.product.obj_x.location.x = self.width
        closet_props.update_render_materials(self, context)
        self.update_placement(context)
        return True

    def execute(self, context):
        """ This is called when the OK button is clicked """
        self.update_product_size()
        return {'FINISHED'}

    def invoke(self, context, event):
        """ This is called before the interface is displayed """
        self.product = self.get_product()
        self.current_location = self.product.obj_bp.location.x
        self.selected_location = self.product.obj_bp.location.x
        self.default_width = self.product.obj_x.location.x
        self.width = self.product.obj_x.location.x
        self.placement_on_wall = 'SELECTED_POINT'
        self.left_offset = 0
        self.right_offset = 0

        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=sn_utils.get_prop_dialog_width(400))

    def update_placement(self, context):
        left_x = self.product.get_collision_location('LEFT')
        right_x = self.product.get_collision_location('RIGHT')
        if self.placement_on_wall == 'SELECTED_POINT':
            self.product.obj_bp.location.x = self.current_location
        if self.placement_on_wall == 'LEFT':
            self.product.obj_bp.location.x = left_x + self.left_offset
            self.product.obj_x.location.x = self.width
        if self.placement_on_wall == 'RIGHT':
            if self.product.obj_bp.snap.placement_type == 'Corner':
                self.product.obj_bp.rotation_euler.z = math.radians(-90)
            self.product.obj_x.location.x = self.width
            self.product.obj_bp.location.x = (right_x - self.product.calc_width()) - self.right_offset

    def set_product_defaults(self):
        self.product.obj_bp.location.x = self.selected_location + self.left_offset
        self.product.obj_x.location.x = self.default_width - (self.left_offset + self.right_offset)

    def draw_product_placement(self, layout):
        box = layout.box()

        row = box.row(align=True)
        row.label(text='Placement', icon='LATTICE_DATA')
        row.prop_enum(self, "placement_on_wall", 'SELECTED_POINT', icon='RESTRICT_SELECT_OFF', text="Selected Point")
        row.prop_enum(self, "placement_on_wall", 'LEFT', icon='TRIA_LEFT', text="Left")
        row.prop_enum(self, "placement_on_wall", 'RIGHT', icon='TRIA_RIGHT', text="Right")

        if self.placement_on_wall in 'LEFT':
            row = box.row(align=True)
            row.label(text='Offset', icon='BACK')
            row.prop(self, "left_offset", icon='TRIA_LEFT', text="Left")

        if self.placement_on_wall in 'RIGHT':
            row = box.row(align=True)
            row.label(text='Offset', icon='FORWARD')
            row.prop(self, "right_offset", icon='TRIA_RIGHT', text="Right")

        if self.placement_on_wall == 'SELECTED_POINT':
            row = box.row()
            row.label(text='Location:')
            row.prop(self, 'current_location', text="")

        row.label(text='Move Off Wall:')
        row.prop(self.product.obj_bp, 'location', index=1, text="")

    def draw(self, context):
        """ This is where you draw the interface """
        layout = self.layout
        layout.label(text=self.product.obj_bp.snap.name_object)
        self.draw_product_size(layout, use_rot_z=False)
        box = layout.box()

        distance_above_floor = self.product.get_prompt("Distance Above Floor")
        height = self.product.get_prompt("Height")
        exposed_top = self.product.get_prompt("Exposed Top")
        exposed_left = self.product.get_prompt("Exposed Left")
        exposed_right = self.product.get_prompt("Exposed Right")
        exposed_bottom = self.product.get_prompt("Exposed Bottom")

        row = box.row()
        row.prop(height, "distance_value", text="Height:")
        row = box.row()
        row.prop(distance_above_floor, "distance_value", text="Distance Above Floor:")

        split = box.split()
        col = split.column(align=True)
        edgebanding_prompts = [exposed_left, exposed_right, exposed_bottom, exposed_top]

        if all(edgebanding_prompts):
            col.label(text="Exposed Edges:")
            row = col.row()
            row.prop(exposed_left, 'checkbox_value', text="Left")
            row.prop(exposed_top, 'checkbox_value', text="Top")
            row = col.row()
            row.prop(exposed_right, 'checkbox_value', text="Right")
            row.prop(exposed_bottom, 'checkbox_value', text="Bottom")
        row = box.row()

        self.draw_product_placement(layout)


bpy.utils.register_class(PROMPTS_Wall_Cleat_Prompts)
