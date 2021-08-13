import math

import bpy
from bpy.types import Operator
from bpy.props import StringProperty, FloatProperty, EnumProperty

from snap import sn_types, sn_unit, sn_utils
from ..ops.drop_closet import PlaceClosetInsert
from ..common import common_parts
from ..common import common_prompts
from .. import closet_props


class Garage_Leg(sn_types.Assembly):

    type_assembly = "INSERT"
    id_prompt = "sn_closets.garage_leg_prompts"
    drop_id = "sn_closets.place_garage_leg"
    show_in_library = True
    placement_type = ""

    library_name = ""
    category_name = ""

    def update(self):
        self.obj_bp['IS_BP_GARAGE_LEG'] = True
        self.obj_bp['ID_PROMPT'] = self.id_prompt
        self.obj_x.location.x = self.width
        self.obj_z.location.z = self.height
        self.obj_y.location.y = -self.depth
        super().update()

    def pre_draw(self):
        self.create_assembly()
        self.obj_x.location.x = self.width
        self.obj_z.location.z = self.height
        self.obj_y.location.y = -self.depth
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()

        self.add_prompt("Right Height", 'DISTANCE', 0)
        self.add_prompt("Panel Quantity", "QUANTITY", 0)
        self.add_prompt("Opening Quantity", "QUANTITY", 1)
        self.add_prompt("Material Type", "COMBOBOX", 0, ["Plastic", "Metal"])
        self.add_prompt("Metal Color", "COMBOBOX", 0,
                        ["Satin Nickel", "Polished Chrome", "Black Textured", "Silver Aluminum"])

    def draw(self):
        bpy.context.view_layer.update()
        panel_quantity = self.get_prompt("Panel Quantity")
        opening_quantity = self.get_prompt("Opening Quantity")

        Width = self.obj_x.snap.get_var("location.x", "Width")
        Depth = self.obj_y.snap.get_var("location.y", "Depth")
        Left_Height = self.obj_z.snap.get_var('location.z', "Left_Height")
        Right_Height = self.get_prompt('Right Height').get_var("Right_Height")
        Material_Type = self.get_prompt("Material Type").get_var("Material_Type")
        Depth_1 = self.get_prompt("Opening 1 Depth").get_var("Depth_1")
        Last_Depth = self.get_prompt("Opening " + str(opening_quantity.get_value()) + ' Depth').get_var("Last_Depth")

        left_front_plastic_leg = common_parts.add_plastic_leg(self)
        constraint = left_front_plastic_leg.obj_z.constraints.new(type='LIMIT_LOCATION')
        constraint.use_max_z = True
        constraint.max_z = sn_unit.millimeter(168)
        constraint.owner_space = 'LOCAL'
        left_front_plastic_leg.obj_bp['IS_BP_GARAGE_LEG'] = True
        left_front_plastic_leg.dim_x(value=0)
        left_front_plastic_leg.dim_y(value=0)
        left_front_plastic_leg.dim_z("Left_Height", [Left_Height])
        left_front_plastic_leg.loc_x(value=sn_unit.inch(1))
        left_front_plastic_leg.loc_y("-Depth_1+INCH(1.5)", [Depth_1])
        left_front_plastic_leg.loc_z(value=0)
        left_front_plastic_leg.get_prompt('Hide').set_formula('IF(Material_Type == 1, True, False) or Hide', [self.hide_var, Material_Type])

        left_back_plastic_leg = common_parts.add_plastic_leg(self)
        constraint = left_back_plastic_leg.obj_z.constraints.new(type='LIMIT_LOCATION')
        constraint.use_max_z = True
        constraint.max_z = sn_unit.millimeter(168)
        constraint.owner_space = 'LOCAL'
        left_back_plastic_leg.dim_x(value=0)
        left_back_plastic_leg.dim_y(value=0)
        left_back_plastic_leg.dim_z("Left_Height", [Left_Height])
        left_back_plastic_leg.loc_x(value=sn_unit.inch(1))
        left_back_plastic_leg.loc_y(value=sn_unit.inch(-1.5))
        left_back_plastic_leg.loc_z(value=0)
        left_back_plastic_leg.get_prompt('Hide').set_formula('IF(OR(Depth_1<INCH(24.01), Material_Type == 1), True, False) or Hide', [self.hide_var, Material_Type, Depth_1])

        right_front_plastic_leg = common_parts.add_plastic_leg(self)
        constraint = right_front_plastic_leg.obj_z.constraints.new(type='LIMIT_LOCATION')
        constraint.use_max_z = True
        constraint.max_z = sn_unit.millimeter(168)
        constraint.owner_space = 'LOCAL'
        right_front_plastic_leg.dim_x(value=0)
        right_front_plastic_leg.dim_y(value=0)
        right_front_plastic_leg.dim_z("Right_Height", [Right_Height])
        right_front_plastic_leg.loc_x("Width-INCH(1)", [Width])
        right_front_plastic_leg.loc_y("-Last_Depth+INCH(1.5)", [Last_Depth])
        right_front_plastic_leg.loc_z(value=0)
        right_front_plastic_leg.rot_z(value=math.radians(180))
        right_front_plastic_leg.get_prompt('Hide').set_formula('IF(Material_Type == 1, True, False) or Hide', [self.hide_var, Material_Type])

        right_back_plastic_leg = common_parts.add_plastic_leg(self)
        constraint = right_back_plastic_leg.obj_z.constraints.new(type='LIMIT_LOCATION')
        constraint.use_max_z = True
        constraint.max_z = sn_unit.millimeter(168)
        constraint.owner_space = 'LOCAL'
        right_back_plastic_leg.dim_x(value=0)
        right_back_plastic_leg.dim_y(value=0)
        right_back_plastic_leg.dim_z("Right_Height", [Right_Height])
        right_back_plastic_leg.loc_x("Width-INCH(1)", [Width])
        right_back_plastic_leg.loc_y(value=sn_unit.inch(-1.5))
        right_back_plastic_leg.loc_z(value=0)
        right_back_plastic_leg.rot_z(value=math.radians(180))
        right_back_plastic_leg.get_prompt('Hide').set_formula('IF(OR(Material_Type == 1, Last_Depth<INCH(24.01)), True, False) or Hide', [self.hide_var, Material_Type, Last_Depth])

        left_front_metal_leg = common_parts.add_metal_leg(self)
        left_front_metal_leg.dim_x(value=0)
        left_front_metal_leg.dim_y(value=0)
        left_front_metal_leg.dim_z("Left_Height", [Left_Height])
        left_front_metal_leg.loc_x(value=0)
        left_front_metal_leg.loc_y("-Depth_1", [Depth_1])
        left_front_metal_leg.loc_z(value=0)
        left_front_metal_leg.get_prompt('Hide').set_formula('IF(Material_Type == 0, True, False) or Hide', [self.hide_var, Material_Type])

        right_front_metal_leg = common_parts.add_metal_leg(self)
        right_front_metal_leg.dim_x(value=0)
        right_front_metal_leg.dim_y(value=0)
        right_front_metal_leg.dim_z("Right_Height", [Right_Height])
        right_front_metal_leg.loc_x("Width-INCH(3)", [Width])
        right_front_metal_leg.loc_y("-Last_Depth", [Last_Depth])
        right_front_metal_leg.loc_z(value=0)
        right_front_metal_leg.get_prompt('Hide').set_formula('IF(Material_Type == 0, True, False) or Hide', [self.hide_var, Material_Type])

        left_back_metal_leg = common_parts.add_metal_leg(self)
        left_back_metal_leg.dim_x(value=0)
        left_back_metal_leg.dim_y(value=0)
        left_back_metal_leg.dim_z("Left_Height", [Left_Height])
        left_back_metal_leg.loc_x(value=0)
        left_back_metal_leg.loc_y(value=sn_unit.inch(-3))
        left_back_metal_leg.loc_z(value=0)
        left_back_metal_leg.get_prompt('Hide').set_formula('IF(OR(Material_Type == 0, Depth_1<INCH(24.01)), True, False)or Hide', [self.hide_var, Material_Type, Depth_1])

        right_back_metal_leg = common_parts.add_metal_leg(self)
        right_back_metal_leg.dim_x(value=0)
        right_back_metal_leg.dim_y(value=0)
        right_back_metal_leg.dim_z("Right_Height", [Right_Height])
        right_back_metal_leg.loc_x("Width-INCH(3)", [Width])
        right_back_metal_leg.loc_y(value=sn_unit.inch(-3))
        right_back_metal_leg.loc_z(value=0)
        right_back_metal_leg.get_prompt('Hide').set_formula('IF(OR(Material_Type == 0, Last_Depth<INCH(24.01)), True, False) or Hide', [self.hide_var, Material_Type, Last_Depth])

        for i in range(1, opening_quantity.get_value() + 1):
            Opening_Width = self.get_prompt("Opening " + str(i) + " Width").get_var("Opening_Width")
            Opening_Location = self.get_prompt("Opening " + str(i) + " Location").get_var("Opening_Location")
            Opening_Depth = self.get_prompt("Opening " + str(i) + " Depth").get_var("Opening_Depth")

            opening_plastic = common_parts.add_plastic_leg(self)
            constraint = opening_plastic.obj_z.constraints.new(type='LIMIT_LOCATION')
            constraint.use_max_z = True
            constraint.max_z = sn_unit.millimeter(168)
            opening_plastic.dim_x(value=0)
            opening_plastic.dim_y(value=0)
            opening_plastic.dim_z("Left_Height", [Left_Height])
            opening_plastic.loc_x("Opening_Location+(Opening_Width/2)-INCH(0.25)", [Opening_Location, Opening_Width])
            opening_plastic.loc_y("(Opening_Depth/2)*-1", [Opening_Depth])
            opening_plastic.loc_z(value=0)
            opening_plastic.rot_z(value=math.radians(90))
            opening_plastic.get_prompt('Hide').set_formula('IF(OR(Material_Type == 1, Opening_Width<=INCH(35.999)), True, False) or Hide', [self.hide_var, Material_Type, Opening_Width])

            opening_metal = common_parts.add_metal_leg(self)
            opening_metal.dim_x(value=0)
            opening_metal.dim_y(value=0)
            opening_metal.dim_z("Left_Height", [Left_Height])
            opening_metal.loc_x("Opening_Location+(Opening_Width/2)-INCH(1.5)", [Opening_Location, Opening_Width])
            opening_metal.loc_y("(Opening_Depth/2)*-1", [Opening_Depth])
            opening_metal.loc_z(value=0)
            opening_metal.get_prompt('Hide').set_formula('IF(OR(Material_Type == 0, Opening_Width<=INCH(35.999)), True, False)or Hide', [self.hide_var, Material_Type, Opening_Width])

        for i in range(1, panel_quantity.get_value() + 1):
            Panel_Location = self.get_prompt("Panel " + str(i) + " Location").get_var("Panel_Location")
            Current_Depth = self.get_prompt("Opening " + str(i) + " Depth").get_var("Current_Depth")
            Next_Depth = self.get_prompt("Opening " + str(i + 1) + " Depth").get_var("Next_Depth")

            panel_front_plastic = common_parts.add_plastic_leg(self)
            constraint = panel_front_plastic.obj_z.constraints.new(type='LIMIT_LOCATION')
            constraint.use_max_z = True
            constraint.max_z = sn_unit.millimeter(168)
            panel_front_plastic.dim_x(value=0)
            panel_front_plastic.dim_y(value=0)
            panel_front_plastic.dim_z("Left_Height", [Left_Height])
            panel_front_plastic.loc_x("Panel_Location-INCH(.5)", [Panel_Location])
            panel_front_plastic.loc_y("IF(Current_Depth>=Next_Depth,-Current_Depth,-Next_Depth)+INCH(1)", [Current_Depth, Next_Depth])
            panel_front_plastic.loc_z(value=0)
            panel_front_plastic.rot_z(value=math.radians(90))
            panel_front_plastic.get_prompt('Hide').set_formula('IF(Material_Type == 1, True, False) or Hide', [self.hide_var, Material_Type])

            panel_back_plastic = common_parts.add_plastic_leg(self)
            constraint = panel_back_plastic.obj_z.constraints.new(type='LIMIT_LOCATION')
            constraint.use_max_z = True
            constraint.max_z = sn_unit.millimeter(168)
            panel_back_plastic.dim_x(value=0)
            panel_back_plastic.dim_y(value=0)
            panel_back_plastic.dim_z("Left_Height", [Left_Height])
            panel_back_plastic.loc_x("Panel_Location-INCH(.5)", [Panel_Location])
            panel_back_plastic.loc_y(value=sn_unit.inch(-1))
            panel_back_plastic.loc_z(value=0)
            panel_back_plastic.rot_z(value=math.radians(-90))
            panel_back_plastic.get_prompt('Hide').set_formula(
                'IF(OR(Material_Type == 1,IF(Current_Depth>=Next_Depth,Current_Depth,Next_Depth)<INCH(24.01)), True, False) or Hide',
                [self.hide_var, Material_Type, Current_Depth, Next_Depth])

            panel_front_metal = common_parts.add_metal_leg(self)
            panel_front_metal.dim_x(value=0)
            panel_front_metal.dim_y(value=0)
            panel_front_metal.dim_z("Left_Height", [Left_Height])
            panel_front_metal.loc_x("Panel_Location-INCH(1.9)", [Panel_Location])
            panel_front_metal.loc_y("IF(Current_Depth>=Next_Depth,-Current_Depth,-Next_Depth)", [Current_Depth, Next_Depth])
            panel_front_metal.loc_z(value=0)
            panel_front_metal.get_prompt('Hide').set_formula('IF(Material_Type == 0,True, False)or Hide', [self.hide_var, Material_Type])

            panel_back_metal = common_parts.add_metal_leg(self)
            panel_back_metal.dim_x(value=0)
            panel_back_metal.dim_y(value=0)
            panel_back_metal.dim_z("Left_Height", [Left_Height])
            panel_back_metal.loc_x("Panel_Location-INCH(1.9)", [Panel_Location])
            panel_back_metal.loc_y(value=sn_unit.inch(-3))
            panel_back_metal.loc_z(value=0)
            panel_back_metal.get_prompt('Hide').set_formula(
                'IF(OR(Material_Type == 0,IF(Current_Depth>=Next_Depth,Current_Depth,Next_Depth)<INCH(24.01)),True, False)or Hide',
                [self.hide_var, Material_Type, Current_Depth, Next_Depth])

        self.update()


class PROMPTS_Garage_Leg_Prompts(sn_types.Prompts_Interface):
    bl_idname = "sn_closets.garage_leg_prompts"
    bl_label = "Garage Leg Prompts"
    bl_options = {'UNDO'}

    object_name: StringProperty(name="Object Name",
                                description="Stores the Base Point Object Name so the "
                                            "object can be retrieved from the database.")

    width: FloatProperty(name="Width", unit='LENGTH', precision=4)
    height: FloatProperty(name="Height", unit='LENGTH', precision=4)
    depth: FloatProperty(name="Depth", unit='LENGTH', precision=4)

    material_type: EnumProperty(
        name="Material Type",
        items=[
            ('0', 'Plastic', 'Plastic'),
            ('1', 'Metal', 'Metal')],
        default='0')

    metal_color: EnumProperty(
        name="Metal Color",
        items=[
            ('0', 'Satin Nickel', 'Satin Nickel'),
            ('1', 'Polished Chrome', 'Polished Chrome'),
            ('2', 'Black Textured', 'Black Textured'),
            ('3', 'Silver Aluminum', 'Silver Aluminum')],
        default='0')

    product = None

    def check(self, context):
        """ This is called everytime a change is made in the UI """
        self.update_product_size()
        self.product.get_prompt("Material Type").set_value(int(self.material_type))
        self.product.get_prompt("Metal Color").set_value(int(self.metal_color))
        closet_props.update_render_materials(self, context)
        return True

    def execute(self, context):
        """ This is called when the OK button is clicked """
        self.update_product_size()
        return {'FINISHED'}

    def invoke(self, context, event):
        """ This is called before the interface is displayed """
        self.product = self.get_insert()
        # self.depth = math.fabs(self.product.obj_y.location.y)
        # self.height = math.fabs(self.product.obj_z.location.z)
        # self.width = math.fabs(self.product.obj_x.location.x)
        self.material_type = str(self.product.get_prompt("Material Type").get_value())
        self.metal_color = str(self.product.get_prompt("Metal Color").get_value())
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=sn_utils.get_prop_dialog_width(500))

    def draw(self, context):
        """ This is where you draw the interface """
        material_type = self.product.get_prompt('Material Type')
        layout = self.layout
        layout.label(text=self.product.obj_bp.snap.name_object)
        self.draw_product_size(layout)
        box = layout.box()
        row = box.row()
        if material_type:
            row.label(text="Material Type")
            row.prop(self, "material_type", text="")
            if material_type.get_value() == 1:
                row = box.row()
                row.label(text="Metal Color")
                row.prop(self, "metal_color", text="")


class DROP_OPERATOR_Place_Garage_Leg(Operator, PlaceClosetInsert):
    bl_idname = "sn_closets.place_garage_leg"
    bl_label = "Place Garage Leg"
    bl_description = "This places the garage leg."
    bl_options = {'UNDO'}

    # READONLY
    object_name: StringProperty(name="Object Name")

    product = None
    show_openings = False
    bottom_capping = None
    selected_panel_1 = None
    selected_panel_2 = None
    objects = []
    panels = []
    openings = []
    sel_product_bp = None
    header_text = (
        "Place Garage Legs- Select Partitions (Left to Right)  "
        "  (Esc, Right Click) = Cancel Command  :  (Left Click) = Select Panel")

    def execute(self, context):
        self.product = self.asset
        return super().execute(context)

    def get_distance_between_panels(self, panel_1, panel_2):
        if panel_1.obj_z.location.z > 0:
            obj_1 = panel_1.obj_z
        else:
            obj_1 = panel_1.obj_bp

        if panel_2.obj_z.location.z > 0:
            obj_2 = panel_2.obj_bp
        else:
            obj_2 = panel_2.obj_z

        x1 = obj_1.matrix_world[0][3]
        y1 = obj_1.matrix_world[1][3]
        z1 = obj_1.matrix_world[2][3]

        x2 = obj_2.matrix_world[0][3]
        y2 = obj_2.matrix_world[1][3]

        # DONT CALCULATE Z DIFFERENCE
        return sn_utils.calc_distance((x1, y1, z1), (x2, y2, z1))

    def product_drop(self, context, event):

        selected_panel_2 = None
        selected_point, selected_obj, ignore = sn_utils.get_selection_point(context, event)
        bpy.ops.object.select_all(action='DESELECT')

        self.sel_product_bp = sn_utils.get_bp(selected_obj, 'PRODUCT')
        sel_assembly_bp = sn_utils.get_assembly_bp(selected_obj)

        if sel_assembly_bp:
            props = sel_assembly_bp.sn_closets
            if props.is_panel_bp:
                selected_obj.select_set(True)
                selected_panel_2 = sn_types.Assembly(sel_assembly_bp)

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and self.selected_panel_1:
            selected_panel_2 = sn_types.Assembly(sel_assembly_bp)
            if selected_panel_2 and selected_panel_2.obj_bp:
                sn_utils.set_wireframe(self.product.obj_bp, False)
                bpy.context.window.cursor_set('DEFAULT')
                bpy.ops.object.select_all(action='DESELECT')
                context.view_layer.objects.active = self.product.obj_bp
                self.product.obj_bp.select_set(True)

                panel_1_bp = self.selected_panel_1.obj_bp
                carcass_product_bp = sn_utils.get_closet_bp(panel_1_bp)
                carcass_assembly = sn_types.Assembly(carcass_product_bp)

                Panel_Thickness = carcass_assembly.get_prompt("Panel Thickness").get_var()
                P1_X_Loc = self.selected_panel_1.obj_bp.snap.get_var('location.x', 'P1_X_Loc')
                P2_X_Loc = selected_panel_2.obj_bp.snap.get_var('location.x', 'P2_X_Loc')

                self.product.loc_x('IF(P1_X_Loc>0,P1_X_Loc-Panel_Thickness,0)',[P1_X_Loc, Panel_Thickness])
                self.product.dim_x('P2_X_Loc-IF(P1_X_Loc>0,P1_X_Loc-Panel_Thickness,0)', [P1_X_Loc, P2_X_Loc, Panel_Thickness])

                panel_depth_1 = abs(self.selected_panel_1.obj_y.location.y)
                panel_depth_2 = abs(selected_panel_2.obj_y.location.y)
                Panel_Depth_1 = self.selected_panel_1.obj_y.snap.get_var('location.y', 'Panel_Depth_1')
                Panel_Depth_2 = selected_panel_2.obj_y.snap.get_var('location.y', 'Panel_Depth_2')
                if panel_depth_1 > panel_depth_2:
                    self.product.dim_y('Panel_Depth_2',[Panel_Depth_2])
                else:
                    self.product.dim_y('Panel_Depth_1',[Panel_Depth_1])

                P1_Z_Loc = self.selected_panel_1.obj_bp.snap.get_var('location.z','P1_Z_Loc')
                P2_Z_Loc = selected_panel_2.obj_bp.snap.get_var('location.z','P2_Z_Loc')
                self.product.dim_z("P1_Z_Loc", [P1_Z_Loc])
                right_height = self.product.get_prompt("Right Height")
                if right_height:
                    right_height.set_formula('P2_Z_Loc', [P2_Z_Loc])
                self.product.obj_bp.snap.type_group = 'INSERT'
                self.product.obj_bp.location.z = 0

                self.get_inculded_panels(self.selected_panel_1, selected_panel_2)
                for i, panel in enumerate(self.panels, 1):
                    self.product.add_prompt("Panel " + str(i) + " Location", "DISTANCE", 0)
                    p_x_loc = panel.obj_bp.snap.get_var("location.x", "p_x_loc")
                    self.product.get_prompt("Panel " + str(i) + " Location").set_formula("p_x_loc", [p_x_loc])

                self.get_included_openings(self.selected_panel_1, selected_panel_2)
                for i, opening in enumerate(self.openings, 1):
                    self.product.add_prompt("Opening " + str(i) + " Location", "DISTANCE", 0)
                    self.product.add_prompt("Opening " + str(i) + " Width", "DISTANCE", 0)
                    self.product.add_prompt("Opening " + str(i) + " Depth", "DISTANCE", 0)

                    opening_x_loc = opening.snap.get_var("location.x", "opening_x_loc")
                    self.product.get_prompt("Opening " + str(i) + " Location").set_formula("opening_x_loc", [opening_x_loc])

                    calculator = carcass_assembly.get_calculator('Opening Widths Calculator')
                    width_prompt = eval("calculator.get_calculator_prompt('Opening {} Width')".format(str(i)))
                    Width = eval("width_prompt.get_var(calculator.name, 'opening_{}_width')".format(str(i)))
                    self.product.get_prompt("Opening " + str(i) + " Width").set_formula('opening_{}_width'.format(str(i)), [Width])

                    Opening_Depth = carcass_assembly.get_prompt('Opening ' + str(i) + ' Depth').get_var("Opening_Depth")
                    self.product.get_prompt("Opening " + str(i) + " Depth").set_formula('Opening_Depth', [Opening_Depth])

                self.product.get_prompt("Panel Quantity").set_value(len(self.panels))
                self.product.get_prompt("Opening Quantity").set_value(len(self.openings))
                self.confirm_placement(context)
                context.area.header_text_set(None)
                self.product.update()
                return {'FINISHED'}
            else:
                return {'RUNNING_MODAL'}

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and self.selected_panel_1 == None:
            self.selected_panel_1 = selected_panel_2
            if self.selected_panel_1 and self.selected_panel_1.obj_bp:
                sn_utils.set_wireframe(self.product.obj_bp, False)
                bpy.context.window.cursor_set('DEFAULT')
                bpy.ops.object.select_all(action='DESELECT')
                context.view_layer.objects.active = self.product.obj_bp
                self.product.obj_bp.parent = self.sel_product_bp

                if self.selected_panel_1.obj_z.location.z > 0:
                    # CENTER OR RIGHT PANEL SELECTED
                    self.product.obj_bp.location = self.selected_panel_1.obj_bp.location
                    self.product.obj_bp.location.x -= self.selected_panel_1.obj_z.location.z
                else:
                    # LEFT PANEL SELECTED
                    self.product.obj_bp.location = self.selected_panel_1.obj_bp.location

        return {'RUNNING_MODAL'}

    def get_included_openings(self, panel_1, panel_2):
        self.openings.clear()
        p1_x_loc = panel_1.obj_bp.location.x
        p2_x_loc = panel_2.obj_bp.location.x
        for child in self.sel_product_bp.children:
            if child.snap.type_group == 'OPENING':
                if p1_x_loc <= child.location.x < p2_x_loc:
                    self.openings.append(child)

    def get_inculded_panels(self, panel_1, panel_2):
        self.panels.clear()
        p1_x_loc = panel_1.obj_bp.location.x
        p2_x_loc = panel_2.obj_bp.location.x

        for child in self.sel_product_bp.children:
            if 'IS_BP_BLIND_CORNER_PANEL' in child:
                continue

            if 'IS_BP_PANEL' in child:
                if p1_x_loc < child.location.x < p2_x_loc:
                    self.panels.append(sn_types.Assembly(child))

    def confirm_placement(self, context):
        self.product.draw()
        # Additional steps here if needed after product.draw before exiting operator
        self.set_child_properties(self.asset.obj_bp)
        self.set_placed_properties(self.asset.obj_bp)
        context.view_layer.objects.active = self.asset.obj_bp

    def modal(self, context, event):
        context.area.tag_redraw()
        self.reset_selection()

        if self.event_is_cancel_command(event):
            context.area.header_text_set(None)
            return self.cancel_drop(context)

        if self.event_is_pass_through(event):
            return {'PASS_THROUGH'}

        return self.product_drop(context, event)


bpy.utils.register_class(DROP_OPERATOR_Place_Garage_Leg)
bpy.utils.register_class(PROMPTS_Garage_Leg_Prompts)
