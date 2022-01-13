from os import path
import math

import bpy
from bpy.props import (
    StringProperty,
    FloatProperty,
    EnumProperty,
    BoolProperty
)

from snap import sn_types, sn_unit, sn_utils
from .. import closet_props
from ..common import common_parts
from ..common import common_prompts
from .. import closet_props


class Topshelf_Support_Corbels(sn_types.Assembly):

    type_assembly = "PRODUCT"
    drop_id = "sn_closets.place_closet_accessory"
    id_prompt = "closet.topshelf_support_corbels"
    show_in_library = True
    category_name = ""
    mid_corbels = []
    extra_cleats = []
    width = sn_unit.inch(34)
    height = sn_unit.inch(12.75)
    depth = sn_unit.inch(12)
    corbel_spacing = sn_unit.inch(48)

    def __init__(self, obj_bp=None):
        super().__init__(obj_bp=obj_bp)
        self.mid_corbels = []
        self.extra_cleats = []
        self.get_mid_corbels()
        self.get_extra_cleats()

    def get_mid_corbels(self):
        for child in self.obj_bp.children:
            if child.get("IS_BP_MID_CORBEL"):
                corbel = sn_types.Assembly(child)
                self.mid_corbels.append(corbel)

    def get_extra_cleats(self):
        for child in self.obj_bp.children:
            if child.get("IS_BP_EXTRA_CLEAT"):
                cleat = sn_types.Assembly(child)
                self.extra_cleats.append(cleat)

    def add_oversize_prompts(self):
        for i in range(10):
            empty_name = "Oversize Cut {}".format(str(i + 1))
            empty = self.add_empty(empty_name)

    def update(self):
        self.obj_bp.snap.export_as_subassembly = True
        self.obj_bp["IS_BP_CLOSET"] = True
        self.obj_bp["IS_TOPSHELF_SUPPORT_CORBELS"] = True

        self.obj_bp['ID_PROMPT'] = self.id_prompt
        self.obj_bp.snap.type_group = self.type_assembly
        super().update()

    def add_mid_corbels(self, amt):
        Width = self.obj_x.snap.get_var('location.x', 'Width')
        Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        Panel_Thickness = self.get_prompt('Panel Thickness').get_var()
        Max_Corbel_Spacing = self.get_prompt("Max Corbel Spacing").get_var()
        Mid_Corbel_Amount = self.get_prompt("Mid Corbel Amount").get_var()
        Cleat_Height = self.get_prompt("Cleat Height").get_var('Cleat_Height')
        Cleat_Thickness = self.get_prompt("Cleat Thickness").get_var()

        for i in range(1, amt + 1):
            mid_corbel = common_parts.add_corbel(self)
            mid_corbel.obj_bp["IS_BP_MID_CORBEL"] = True
            self.mid_corbels.append(mid_corbel)
            mid_corbel.dim_x("Depth", [Depth])
            mid_corbel.dim_y("IF(Depth<INCH(12),Depth,INCH(12))", [Depth])
            mid_corbel.loc_x("(Width/{})*{}-(Panel_Thickness*0.5)".format(str(amt + 1), str(i)), [Width, Max_Corbel_Spacing, Panel_Thickness])
            mid_corbel.rot_x(value=math.radians(-90))
            mid_corbel.rot_z(value=math.radians(-90))
            mid_corbel.dim_z("Panel_Thickness", [Panel_Thickness])
            mid_corbel.get_prompt('Left Depth').set_value(value=0)
            mid_corbel.get_prompt('Right Depth').set_value(value=0)
            mid_corbel.get_prompt('Right Depth').set_value(value=0)

            self.get_prompt("Mid Corbel Amount").set_value(value=amt)

            cleat = common_parts.add_cleat(self)
            cleat.obj_bp["IS_BP_EXTRA_CLEAT"] = True
            self.extra_cleats.append(cleat)
            cleat.set_name("Top Cleat")
            cleat.loc_x("Panel_Thickness*0.5+Width/(Mid_Corbel_Amount+1)*{}".format(str(i)), [Panel_Thickness, Mid_Corbel_Amount, Width])
            cleat.rot_x(value=math.radians(-90))

            if amt == 1:
                cleat.dim_x("Width/2-Panel_Thickness", [Width, Panel_Thickness, Mid_Corbel_Amount])
            elif i == amt:
                cleat.dim_x("Width/IF(Mid_Corbel_Amount>1,Mid_Corbel_Amount+1,1)-Panel_Thickness*1.5", [Width, Panel_Thickness, Mid_Corbel_Amount])
            else:
                cleat.dim_x("Width/IF(Mid_Corbel_Amount>1,Mid_Corbel_Amount+1,1)-Panel_Thickness", [Width, Panel_Thickness, Mid_Corbel_Amount])

            cleat.dim_y('Cleat_Height', [Cleat_Height])
            cleat.dim_z('-Cleat_Thickness', [Cleat_Thickness])

    def draw(self):
        defaults = bpy.context.scene.sn_closets.closet_defaults
        self.create_assembly()
        self.obj_x.location.x = self.width
        depth = defaults.panel_depth

        if defaults.panel_depth < sn_unit.inch(6):
            depth = sn_unit.inch(6)
        if defaults.panel_depth > sn_unit.inch(16):
            depth = sn_unit.inch(16)

        self.obj_y.location.y = depth
        self.obj_z.location.z = self.height

        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()

        self.add_prompt("Distance Above Floor", 'DISTANCE', sn_unit.inch(30))
        self.add_prompt("Extend To Left Panel", 'CHECKBOX', True)
        self.add_prompt("Extend To Right Panel", 'CHECKBOX', True)
        self.add_prompt("Exposed Left", 'CHECKBOX', False)
        self.add_prompt("Exposed Right", 'CHECKBOX', False)
        self.add_prompt("Exposed Back", 'CHECKBOX', False)
        self.add_prompt("Extend Left Amount", 'DISTANCE', sn_unit.inch(0))
        self.add_prompt("Extend Right Amount", 'DISTANCE', sn_unit.inch(0))
        self.add_prompt("Front Overhang", 'DISTANCE', sn_unit.inch(.5))
        self.add_prompt("Max Panel Depth", 'DISTANCE', 0)
        ppt_obj_panel_max = self.add_prompt_obj("Panel_Max")
        self.add_prompt("Max Panel Front Chamfer", 'DISTANCE', 0, prompt_obj=ppt_obj_panel_max)
        self.add_prompt("Max Rear Chamfer", 'DISTANCE', 0)
        self.add_prompt("Max Corbel Spacing", 'DISTANCE', self.corbel_spacing)
        self.add_prompt("Mid Corbel Amount", 'QUANTITY', 0)
        self.add_prompt("Cleat Height", 'DISTANCE', sn_unit.inch(3.64))
        self.add_prompt("Cleat Width", 'DISTANCE', 0)
        # hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        # self.hide_var = hide_prompt.get_var()

        self.add_oversize_prompts()
        common_prompts.add_thickness_prompts(self)

        Width = self.obj_x.snap.get_var('location.x', 'Width')
        Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        Extend_Left = self.get_prompt('Extend To Left Panel').get_var('Extend_Left')        
        Extend_Right = self.get_prompt('Extend To Right Panel').get_var('Extend_Right')      
        Panel_Thickness = self.get_prompt('Panel Thickness').get_var()
        Extend_Left_Amount = self.get_prompt('Extend Left Amount').get_var()
        Extend_Right_Amount = self.get_prompt('Extend Right Amount').get_var()
        Front_Overhang = self.get_prompt('Front Overhang').get_var()
        Cleat_Height = self.get_prompt("Cleat Height").get_var('Cleat_Height')
        Cleat_Thickness = self.get_prompt("Cleat Thickness").get_var()
        Mid_Corbel_Amount = self.get_prompt("Mid Corbel Amount").get_var()

        top = common_parts.add_plant_on_top(self)
        top.obj_bp['IS_BP_CLOSET_TOP'] = True
        constraint = top.obj_y.constraints.new(type='LIMIT_LOCATION')
        constraint.use_min_y = True
        constraint.min_y = sn_unit.inch(6)
        constraint.use_max_y = True
        constraint.max_y = sn_unit.inch(16.5)
        constraint.owner_space = 'LOCAL'
        top.obj_bp.snap.comment_2 = "1024"
        top.set_name("Topshelf")
        top.loc_x('IF(Extend_Left,0,Panel_Thickness/2)-Extend_Left_Amount', [Extend_Left, Extend_Left_Amount, Panel_Thickness])

        top.rot_x(value=math.radians(180))
        top.dim_x('Width-IF(Extend_Left,0,Panel_Thickness/2)-IF(Extend_Right,0,Panel_Thickness/2)+Extend_Left_Amount+Extend_Right_Amount',
                  [Width, Extend_Left, Extend_Right, Panel_Thickness, Extend_Right_Amount, Extend_Left_Amount])
        top.dim_y('Depth+Front_Overhang', [Depth, Front_Overhang])
        top.dim_z('-Panel_Thickness', [Panel_Thickness])

        left_corbel = common_parts.add_corbel(self)
        left_corbel.dim_x("Depth", [Depth])
        left_corbel.dim_y("IF(Depth<INCH(12),Depth,INCH(12))", [Depth])
        left_corbel.rot_x(value=math.radians(-90))
        left_corbel.rot_z(value=math.radians(-90))
        left_corbel.dim_z("Panel_Thickness", [Panel_Thickness])
        left_corbel.get_prompt('Left Depth').set_value(value=0)
        left_corbel.get_prompt('Right Depth').set_value(value=0)

        right_corbel = common_parts.add_corbel(self)
        right_corbel.dim_x("Depth", [Depth])
        right_corbel.dim_y("IF(Depth<INCH(12),Depth,INCH(12))", [Depth])
        right_corbel.loc_x("Width-Panel_Thickness", [Width, Panel_Thickness])
        right_corbel.rot_x(value=math.radians(-90))
        right_corbel.rot_z(value=math.radians(-90))
        right_corbel.dim_z("Panel_Thickness", [Panel_Thickness])
        right_corbel.get_prompt('Left Depth').set_value(value=0)
        right_corbel.get_prompt('Right Depth').set_value(value=0)

        cleat = common_parts.add_cleat(self)
        cleat.set_name("Top Cleat")
        cleat.loc_x("Panel_Thickness", [Panel_Thickness])
        cleat.rot_x(value=math.radians(-90))
        cleat.dim_x("Width/IF(Mid_Corbel_Amount>1,Mid_Corbel_Amount+1,IF(Mid_Corbel_Amount==1,2,1))-Panel_Thickness", [Width, Panel_Thickness, Mid_Corbel_Amount])
        cleat.dim_y('Cleat_Height', [Cleat_Height])
        cleat.dim_z('-Cleat_Thickness', [Cleat_Thickness])

        self.update()


class PROMPTS_Topshelf_Support_Corbels(sn_types.Prompts_Interface):
    bl_idname = "closet.topshelf_support_corbels"
    bl_label = "Top Shelf Support Corbels Prompt"
    bl_options = {'UNDO'}

    width: FloatProperty(name="Width",unit='LENGTH',precision=4)
    height: FloatProperty(name="Height",unit='LENGTH',precision=4)
    depth: FloatProperty(name="Depth", unit='LENGTH', precision=4, min=sn_unit.inch(6), max=sn_unit.inch(16))

    placement_on_wall: EnumProperty(name="Placement on Wall",items=[('SELECTED_POINT',"Selected Point",""),
                                                                     ('FILL',"Fill",""),
                                                                     ('FILL_LEFT',"Fill Left",""),
                                                                     ('LEFT',"Left",""),
                                                                     ('CENTER',"Center",""),
                                                                     ('RIGHT',"Right",""),
                                                                     ('FILL_RIGHT',"Fill Right","")],default = 'SELECTED_POINT')

    current_location: FloatProperty(name="Current Location", default=0, subtype='DISTANCE', precision=4)
    left_offset: FloatProperty(name="Left Offset", default=0, subtype='DISTANCE')
    right_offset: FloatProperty(name="Right Offset", default=0, subtype='DISTANCE')

    product = None
    top_shelf = None

    def get_assemblies(self):
        children = self.product.obj_bp.children
        for child in children:
            if "IS_BP_PLANT_ON_TOP" in child:
                self.top_shelf = sn_types.Assembly(child)

    def remove_corbels(self):
        for product in self.product.mid_corbels:
            sn_utils.delete_object_and_children(product.obj_bp)
        self.product.mid_corbels.clear()

    def remove_cleats(self):
        for product in self.product.extra_cleats:
            sn_utils.delete_object_and_children(product.obj_bp)
        self.product.extra_cleats.clear()

    def update_mid_corbels(self, context):
        corbel_amt = 0
        max_corbel_spacing = self.product.get_prompt("Max Corbel Spacing").get_value()

        if self.product.obj_x.location.x >= max_corbel_spacing:
            corbel_amt = int(self.product.obj_x.location.x // max_corbel_spacing)
            if len(self.product.mid_corbels) != corbel_amt:
                self.remove_corbels()
                self.remove_cleats()
                self.product.add_mid_corbels(corbel_amt)
                self.product.update()
                closet_props.update_render_materials(self, context)
        elif self.product.mid_corbels:
            self.remove_corbels()
            self.remove_cleats()
            self.product.get_prompt("Mid Corbel Amount").set_value(value=0)

    def check(self, context):
        self.update_mid_corbels(context)
        closet_props.update_render_materials(self, context)
        self.product.obj_x.location.x = self.width
        self.product.obj_y.location.y = self.depth
        self.update_placement(context)
        return True

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        """ This is called before the interface is displayed """
        self.product = None
        self.top_shelf = None
        obj_product_bp = sn_utils.get_bp(context.object, 'PRODUCT')
        self.product = Topshelf_Support_Corbels(obj_product_bp)
        self.current_location = self.product.obj_bp.location.x
        self.width = self.product.obj_x.location.x
        self.depth = self.product.obj_y.location.y
        self.placement_on_wall = 'SELECTED_POINT'
        self.left_offset = 0
        self.right_offset = 0
        self.update_mid_corbels(context)
        self.get_assemblies()

        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=sn_utils.get_prop_dialog_width(400))

    def update_placement(self, context):
        left_x = self.product.get_collision_location('LEFT')
        right_x = self.product.get_collision_location('RIGHT')
        offsets = self.left_offset + self.right_offset

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
        if self.placement_on_wall == 'FILL':
            self.product.obj_bp.location.x = left_x + self.left_offset
            self.product.obj_x.location.x = (right_x - left_x - offsets)
        if self.placement_on_wall == 'CENTER':
            self.product.obj_x.location.x = self.width
            x_loc = left_x + (right_x - left_x) / 2 - (self.product.calc_width() / 2)
            self.product.obj_bp.location.x = x_loc

        self.update_mid_corbels(context)

    def draw_product_placement(self, layout):
        box = layout.box()
        row = box.row()
        row.label(text='Placement', icon='LATTICE_DATA')
        row = box.row()
        row.label(text='Height Above Floor:')
        row.prop(self.product.obj_bp, 'location', index=2, text="")
        row = box.row()
        col = row.column(align=True)
        col.prop_enum(self, "placement_on_wall", 'SELECTED_POINT', icon='RESTRICT_SELECT_OFF', text="Selected Point")
        row = col.row(align=True)
        row.prop_enum(self, "placement_on_wall", 'FILL', icon='ARROW_LEFTRIGHT', text="Fill")
        row.prop_enum(self, "placement_on_wall", 'LEFT', icon='TRIA_LEFT', text="Left")
        row.prop_enum(self, "placement_on_wall", 'CENTER', icon='TRIA_UP_BAR', text="Center")
        row.prop_enum(self, "placement_on_wall", 'RIGHT', icon='TRIA_RIGHT', text="Right")

        if self.placement_on_wall == 'FILL':
            row = box.row()
            row.label(text='Offset', icon='ARROW_LEFTRIGHT')
            row.prop(self, "left_offset", icon='TRIA_LEFT', text="Left")
            row.prop(self, "right_offset", icon='TRIA_RIGHT', text="Right")

        if self.placement_on_wall in 'LEFT':
            row = box.row()
            row.label(text='Offset', icon='BACK')
            row.prop(self, "left_offset", icon='TRIA_LEFT', text="Left")

        if self.placement_on_wall in 'CENTER':
            row = box.row()

        if self.placement_on_wall in 'RIGHT':
            row = box.row()
            row.label(text='Offset', icon='FORWARD')
            row.prop(self, "right_offset", icon='TRIA_RIGHT', text="Right")

        if self.placement_on_wall == 'SELECTED_POINT':
            row = box.row()
            row.label(text='Location:')
            row.prop(self, 'current_location', text="")

    def draw(self, context):
        exposed_left = self.top_shelf.get_prompt("Exposed Left")
        exposed_right = self.top_shelf.get_prompt("Exposed Right")
        extend_left_amount = self.product.get_prompt("Extend Left Amount")
        extend_right_amount = self.product.get_prompt("Extend Right Amount")
        front_overhang = self.product.get_prompt("Front Overhang")

        layout = self.layout
        box = layout.box()
        row = box.row()
        col = row.column()
        col.prop(extend_left_amount, "distance_value", text="Extend Left:")
        col = row.column()
        row.prop(front_overhang, "distance_value", text="Extend Front:")
        col = row.column()
        col.prop(extend_right_amount, "distance_value", text="Extend Right:")

        row = box.row()
        row.label(text="Exposed Edges:")
        row.prop(exposed_left, "checkbox_value", text="Left")
        row.prop(exposed_right, "checkbox_value", text="Right")

        row = box.row()
        row.label(text='Width:')
        row.prop(self, 'width', text="")
        row.label(text='Depth:')
        row.prop(self, 'depth', text="")

        self.draw_product_placement(layout)


bpy.utils.register_class(PROMPTS_Topshelf_Support_Corbels)
