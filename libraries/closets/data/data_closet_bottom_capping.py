import operator
import math

import bpy
from bpy.types import Operator
from bpy.props import StringProperty, FloatProperty

from snap import sn_types, sn_unit, sn_utils
from ..ops.drop_closet import PlaceClosetInsert
from .. import closet_props
from ..common import common_parts
from ..common import common_prompts


class Bottom_Capping(sn_types.Assembly):
    """ Closet Bottom Capping
    """

    type_assembly = "INSERT"
    placement_type = "SPLITTER"
    id_prompt = "sn_closets.bottom_capping"
    drop_id = "sn_closets.bottom_capping_drop"
    show_in_library = True
    category_name = "Closet Products - Basic"
    mirror_y = True
    max_chamfer_prompts = None

    def update(self):
        self.obj_x.location.x = self.width
        self.obj_y.location.y = -self.depth if self.mirror_y else self.depth
        self.obj_z.location.z = self.height

        self.obj_bp.snap.export_as_subassembly = True
        self.obj_bp['IS_BP_CLOSET_BOTTOM'] = True
        props = self.obj_bp.sn_closets
        props.is_closet_bottom_bp = True
        self.obj_bp['ID_PROMPT'] = self.id_prompt
        self.obj_bp['ID_DROP'] = self.drop_id
        self.obj_bp.snap.placement_type = self.placement_type
        self.obj_bp.snap.type_group = self.type_assembly
        super().update()

    def draw(self):
        self.create_assembly()
        # we are adding a master hide for everything
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()

        self.add_prompt("Extend To Left Panel", 'CHECKBOX', True)
        self.add_prompt("Extend To Right Panel", 'CHECKBOX', True)
        self.add_prompt("Exposed Left", 'CHECKBOX', False)
        self.add_prompt("Exposed Right", 'CHECKBOX', False)
        self.add_prompt("Exposed Back", 'CHECKBOX', False)
        self.add_prompt("Extend Left Amount", 'DISTANCE', sn_unit.inch(0))
        self.add_prompt("Extend Right Amount", 'DISTANCE', sn_unit.inch(0))
        self.add_prompt("Front Overhang", 'DISTANCE', sn_unit.inch(.75))
        self.add_prompt("Max Panel Depth", 'DISTANCE', 0)

        self.max_chamfer_prompts = self.add_empty("OBJ_PROMPTS_Max_Panel_Chamfer")
        self.max_chamfer_prompts.empty_display_size = .01
        self.max_chamfer_prompts.snap.add_prompt('DISTANCE', "Max Panel Front Chamfer")
        self.add_prompt("Max Rear Chamfer", 'DISTANCE', 0)

        # Capping bottom
        self.add_prompt("Partition Height", 'DISTANCE', 0)
        self.add_prompt("Against Left Wall", 'CHECKBOX', True)
        self.add_prompt("Against Right Wall", 'CHECKBOX', True)
        self.add_prompt("Left Partition Extended", 'CHECKBOX', False)
        self.add_prompt("Right Partition Extended", 'CHECKBOX', False)
        self.add_prompt("Left Partition Extension Height", 'DISTANCE', 0)
        self.add_prompt("Right Partition Extension Height", 'DISTANCE', 0)

        common_prompts.add_thickness_prompts(self)

        Width = self.obj_x.snap.get_var('location.x', 'Width')
        Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        Extend_Left = self.get_prompt('Extend To Left Panel').get_var('Extend_Left')        
        Extend_Right = self.get_prompt('Extend To Right Panel').get_var('Extend_Right')      
        Panel_Thickness = self.get_prompt('Panel Thickness').get_var()
        Extend_Left_Amount = self.get_prompt('Extend Left Amount').get_var()
        Extend_Right_Amount = self.get_prompt('Extend Right Amount').get_var()
        Front_Overhang = self.get_prompt('Front Overhang').get_var()
        Exposed_Left = self.get_prompt('Exposed Left').get_var()
        Exposed_Right = self.get_prompt('Exposed Right').get_var()
        Exposed_Back = self.get_prompt('Exposed Back').get_var()

        # Capping Bottom
        Partition_Height = self.get_prompt('Partition Height').get_var()
        LPE = self.get_prompt('Left Partition Extended').get_var('LPE')
        RPE = self.get_prompt('Right Partition Extended').get_var('RPE')

        bottom = common_parts.add_plant_on_top(self)

        bottom.obj_bp.snap.comment_2 = "1024"
        bottom.set_name("Capping Bottom")
        bottom.loc_x(
            'IF(LPE,Panel_Thickness,0)-Extend_Left_Amount',
            [Extend_Left, Extend_Left_Amount, Panel_Thickness, LPE])

        bottom.loc_z('-Partition_Height-Panel_Thickness', [Partition_Height, Panel_Thickness, LPE])
        bottom.rot_x(value=math.radians(180))
        bottom.dim_x(
            "Width-IF(Extend_Left,0,Panel_Thickness/2)"
            "-IF(Extend_Right,0,Panel_Thickness/2)+Extend_Left_Amount+Extend_Right_Amount"
            "-IF(LPE,Panel_Thickness,0)"
            "-IF(RPE,Panel_Thickness,0)",
            [Width, Extend_Left, Extend_Right, Panel_Thickness,
             Extend_Right_Amount, Extend_Left_Amount, LPE, RPE])

        bottom.dim_y('Depth+Front_Overhang', [Depth, Front_Overhang])
        bottom.dim_z('-Panel_Thickness', [Panel_Thickness])
        bottom.get_prompt('Exposed Left').set_formula('Exposed_Left', [Exposed_Left])
        bottom.get_prompt('Exposed Right').set_formula('Exposed_Right', [Exposed_Right])
        bottom.get_prompt('Exposed Back').set_formula('Exposed_Back', [Exposed_Back])

        self.update()


class PROMPTS_Prompts_Bottom_Support(sn_types.Prompts_Interface):
    bl_idname = "sn_closets.bottom_capping"
    bl_label = "Capping Bottom Prompt"
    bl_options = {'UNDO'}

    object_name: StringProperty(
        name="Object Name",
        description="Stores the Base Point Object Name so the object can be retrieved from the database.")

    width: FloatProperty(name="Width", unit='LENGTH', precision=4)
    height: FloatProperty(name="Height", unit='LENGTH', precision=4)
    depth: FloatProperty(name="Depth", unit='LENGTH', precision=4)

    insert = None

    def check(self, context):
        """ This is called everytime a change is made in the UI """
        left_partition_extended = self.insert.get_prompt('Left Partition Extended')
        right_partition_extended = self.insert.get_prompt('Right Partition Extended')
        against_left_wall = self.insert.get_prompt('Against Left Wall')
        against_right_wall = self.insert.get_prompt('Against Right Wall')
        left_partition_extension_height = self.insert.get_prompt("Left Partition Extension Height")
        right_partition_extension_height = self.insert.get_prompt("Right Partition Extension Height")

        prompts = [
            left_partition_extended, right_partition_extended, against_left_wall,
            against_right_wall, left_partition_extension_height,
            right_partition_extension_height]

        if all(prompts):
            if(left_partition_extended.get_value() and left_partition_extension_height.get_value() > 0):
                against_left_wall.set_value(False)
            if(right_partition_extended.get_value() and right_partition_extension_height.get_value() > 0):
                against_right_wall.set_value(False)
        closet_props.update_render_materials(self, context)
        return True

    def execute(self, context):
        """ This is called when the OK button is clicked """
        return {'FINISHED'}

    def invoke(self, context, event):
        """ This is called before the interface is displayed """
        self.insert = self.get_insert()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=sn_utils.get_prop_dialog_width(400))

    def draw(self, context):
        """ This is where you draw the interface """
        layout = self.layout
        box = layout.box()

        exposed_left = self.insert.get_prompt("Exposed Left")
        exposed_right = self.insert.get_prompt("Exposed Right")
        exposed_back = self.insert.get_prompt("Exposed Back")
        extend_left_amount = self.insert.get_prompt("Extend Left Amount")
        extend_right_amount = self.insert.get_prompt("Extend Right Amount")
        front_overhang = self.insert.get_prompt("Front Overhang")
        against_left_wall = self.insert.get_prompt("Against Left Wall")
        against_right_wall = self.insert.get_prompt("Against Right Wall")

        row = box.row()
        extend_left_amount.draw(row, allow_edit=False)
        row = box.row()
        extend_right_amount.draw(row, allow_edit=False)

        row = box.row()
        front_overhang.draw(row, allow_edit=False)

        row = box.row()
        row.label(text="Exposed Edges:")
        ee_box = box.box()
        row = ee_box.row()
        exposed_left.draw(row, alt_text="Left", allow_edit=False)
        exposed_right.draw(row, alt_text="Right", allow_edit=False)
        exposed_back.draw(row, alt_text="Back", allow_edit=False)

        row = box.row()
        row.label(text="Against Wall:")
        aw_box = box.box()
        row = aw_box.row()
        against_left_wall.draw(row, alt_text="Left", allow_edit=False)
        against_right_wall.draw(row, alt_text="Right", allow_edit=False)


class DROP_OPERATOR_Place_Bottom_Capping(Operator, PlaceClosetInsert):
    bl_idname = "sn_closets.bottom_capping_drop"
    bl_label = "Place Capping Bottom"
    bl_description = "This places the capping bottom."
    bl_options = {'UNDO'}

    show_openings = False
    bottom_capping = None
    selected_panel_1 = None
    selected_panel_2 = None
    objects = []
    panels = []
    openings = []
    sel_product_bp = None
    chamfer_prompts_obj_name = "OBJ_PROMPTS_Max_Panel_Chamfer"
    header_text = (
        "Place Capping Bottom- Select Partitions (Left to Right)  "
        "  (Esc, Right Click) = Cancel Command  :  (Left Click) = Select Panel")

    def execute(self, context):
        self.bottom_capping = self.asset
        return super().execute(context)

    def modal(self, context, event):
        bpy.ops.object.select_all(action='DESELECT')
        context.area.tag_redraw()
        context.area.header_text_set(text=self.header_text)
        self.reset_selection()

        if not self.bottom_capping:
            self.bottom_capping = self.asset

        if self.event_is_cancel_command(event):
            context.area.header_text_set(None)
            return self.cancel_drop(context)

        if self.event_is_pass_through(event):
            return {'PASS_THROUGH'}

        return self.place_insert(context, event)

    def get_chamfer_ppt_obj(self):
        for child in self.bottom_capping.obj_bp.children:
            if self.chamfer_prompts_obj_name in child.name:
                return child

    def get_deepest_panel(self):
        depths = []

        for p in self.panels:
            p.obj_y.hide_viewport = False
            bpy.context.view_layer.update()
            depths.append(abs(p.obj_y.location.y))
            p.obj_y.hide_viewport = True

        return max(depths)

    def get_closest_opening(self, x_loc):
        return lambda op: abs(op - x_loc)

    def is_first_panel(self, panel):
        if panel.obj_z.location.z < 0:
            return True
        else:
            return False

    def get_inculded_panels(self, panel_1, panel_2):
        self.panels.clear()
        p1_x_loc = panel_1.obj_bp.location.x
        p2_x_loc = panel_2.obj_bp.location.x

        for child in self.sel_product_bp.children:
            if 'IS_BP_BLIND_CORNER_PANEL' in child:
                continue

            if 'IS_BP_PANEL' in child:
                if p1_x_loc <= child.location.x <= p2_x_loc:
                    self.panels.append(sn_types.Assembly(child))

    def get_included_openings(self, panel_1, panel_2):
        self.openings.clear()
        p1_x_loc = panel_1.obj_bp.location.x
        p2_x_loc = panel_2.obj_bp.location.x
        for child in self.sel_product_bp.children:
            if child.snap.type_group == 'OPENING':
                if p1_x_loc <= child.location.x < p2_x_loc:
                    self.openings.append(child.sn_closets.opening_name)

    def place_insert(self, context, event):
        selected_point, selected_obj, ignore = sn_utils.get_selection_point(context, event, objects=self.objects)
        bpy.ops.object.select_all(action='DESELECT')

        if selected_obj is not None:
            self.sel_product_bp = sn_utils.get_closet_bp(selected_obj)
            sel_assembly_bp = sn_utils.get_assembly_bp(selected_obj)
            product = sn_types.Assembly(self.sel_product_bp)

            if sel_assembly_bp:
                if 'IS_BP_PANEL' in sel_assembly_bp:
                    selected_obj.select_set(True)
                    hover_panel = sn_types.Assembly(selected_obj.parent)
                    hp_x_loc = hover_panel.obj_bp.location.x

                    if not self.selected_panel_1:
                        if hover_panel.obj_bp.location.x == product.obj_x.location.x:
                            selected_obj.select_set(False)
                            return {'RUNNING_MODAL'}

                        self.bottom_capping.obj_bp.parent = self.sel_product_bp
                        self.bottom_capping.obj_bp.location = hover_panel.obj_bp.location

                        if hover_panel.obj_z.location.z > 0:
                            self.bottom_capping.obj_bp.location.x = hp_x_loc - sn_unit.inch(0.75)

                        self.bottom_capping.obj_x.location.x = sn_unit.inch(18.0)
                        self.bottom_capping.obj_y.location.y = -hover_panel.obj_y.location.y

                    else:
                        self.get_inculded_panels(self.selected_panel_1, hover_panel)
                        sp1_x_loc = self.selected_panel_1.obj_bp.location.x
                        hp_x_loc = hover_panel.obj_bp.location.x
                        bc_length = hp_x_loc - sp1_x_loc
                        same_panel = self.selected_panel_1.obj_bp == hover_panel.obj_bp
                        same_product = self.selected_panel_1.obj_bp.parent == hover_panel.obj_bp.parent
                        hp_to_left = hp_x_loc < sp1_x_loc

                        if same_panel or hp_to_left or not same_product:
                            selected_obj.select_set(False)
                            return {'RUNNING_MODAL'}

                        if self.is_first_panel(self.selected_panel_1):
                            self.bottom_capping.obj_x.location.x = bc_length
                        else:
                            if hp_x_loc < sp1_x_loc:
                                # Hover selection to left
                                pass
                            else:
                                self.bottom_capping.obj_x.location.x = bc_length + sn_unit.inch(0.75)

                        self.bottom_capping.obj_y.location.y = self.get_deepest_panel()

                    if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                        if not self.selected_panel_1:
                            self.selected_panel_1 = hover_panel
                            sn_utils.set_wireframe(self.bottom_capping.obj_bp, False)
                            bpy.ops.object.select_all(action='DESELECT')
                            context.view_layer.objects.active = self.bottom_capping.obj_bp

                            self.bottom_capping.obj_bp.parent = self.sel_product_bp
                            parent_assembly = sn_types.Assembly(self.sel_product_bp)
                            p1_z_loc = self.selected_panel_1.obj_bp.location.z
                            p1_z_dim = self.selected_panel_1.obj_x.location.x

                            if self.selected_panel_1.obj_z.location.z < 0:
                                self.bottom_capping.obj_bp.location.x = self.selected_panel_1.obj_bp.location.x
                            else:
                                self.bottom_capping.obj_bp.location.x = self.selected_panel_1.obj_bp.location.x - sn_unit.inch(0.75)

                            self.bottom_capping.obj_bp.location.z = p1_z_loc + p1_z_dim
                            self.bottom_capping.obj_y.location.y = -self.selected_panel_1.obj_y.location.y

                            self.bottom_capping.obj_bp.sn_closets.opening_name = str(1)
                            extend_left_side = parent_assembly.get_prompt("Extend Left End Pard Down")
                            extend_right_side = parent_assembly.get_prompt("Extend Right End Pard Down")
                            height_left_side = parent_assembly.get_prompt("Height Left Side")
                            height_right_side = parent_assembly.get_prompt("Height Right Side")
                            has_capping_bottom = parent_assembly.get_prompt("Has Capping Bottom")
                            left_partition_extended = self.bottom_capping.get_prompt("Left Partition Extended")
                            right_partition_extended = self.bottom_capping.get_prompt("Right Partition Extended")
                            left_partition_extension_height = self.bottom_capping.get_prompt("Left Partition Extension Height")
                            right_partition_extension_height = self.bottom_capping.get_prompt("Right Partition Extension Height")
                            against_left_wall = self.bottom_capping.get_prompt("Against Left Wall")
                            against_right_wall = self.bottom_capping.get_prompt("Against Right Wall")

                            prompts = [
                                extend_left_side, extend_right_side, height_left_side,
                                height_right_side, left_partition_extended, right_partition_extended,
                                left_partition_extension_height, right_partition_extension_height,
                                against_left_wall, against_right_wall, has_capping_bottom]

                            if all(prompts):
                                self.bottom_capping.get_prompt("Partition Height").set_value(
                                    p1_z_dim - height_left_side.get_value())
                                left_partition_extended.set_value(extend_left_side.get_value())
                                right_partition_extended.set_value(extend_right_side.get_value())
                                left_partition_extension_height.set_value(height_left_side.get_value())
                                right_partition_extension_height.set_value(height_right_side.get_value())

                                if(extend_left_side.get_value() and height_left_side.get_value() > 0):
                                    against_left_wall.set_value(False)
                                if(extend_right_side.get_value() and height_right_side.get_value() > 0):
                                    against_right_wall.set_value(False)
                                has_capping_bottom.set_value(True)

                            return {'RUNNING_MODAL'}

                        if not self.selected_panel_2:
                            self.selected_panel_2 = hover_panel
                            bpy.ops.object.select_all(action='DESELECT')
                            context.view_layer.objects.active = self.bottom_capping.obj_bp
                            self.bottom_capping.obj_bp.select_set(True)

                            if self.selected_panel_1.obj_bp == self.selected_panel_2.obj_bp:
                                self.cancel_drop(context, event)
                                return {'FINISHED'}

                            P1_X_Loc = self.selected_panel_1.obj_bp.snap.get_var('location.x','P1_X_Loc')
                            P2_X_Loc = self.selected_panel_2.obj_bp.snap.get_var('location.x','P2_X_Loc')
                            Panel_Thickness = product.get_prompt('Panel Thickness').get_var()

                            if self.is_first_panel(self.selected_panel_1):
                                self.bottom_capping.loc_x('P1_X_Loc', [P1_X_Loc])
                                self.bottom_capping.dim_x('P2_X_Loc-P1_X_Loc', [P1_X_Loc, P2_X_Loc])
                            else:
                                self.bottom_capping.loc_x('P1_X_Loc-Panel_Thickness', [P1_X_Loc, Panel_Thickness])
                                self.bottom_capping.dim_x(
                                    'P2_X_Loc-P1_X_Loc+Panel_Thickness', [P1_X_Loc, P2_X_Loc, Panel_Thickness])

                            max_panel_formula = "max(("
                            max_panel_vars = []
                            max_panel_fc_formula = ""
                            max_panel_fc_vars = []

                            MPD = self.bottom_capping.get_prompt('Max Panel Depth').get_var('MPD')
                            ppt_obj = self.get_chamfer_ppt_obj()
                            Max_Panel_Front_Chamfer = ppt_obj.snap.get_prompt('Max Panel Front Chamfer').get_var()

                            max_panel_fc_vars.append(MPD)
                            max_panel_fc_tail = "0"

                            for i, panel in enumerate(self.panels):
                                max_panel_formula += "abs(PD{}),".format(i + 1)
                                max_panel_vars.append(panel.obj_y.snap.get_var('location.y', 'PD{}'.format(i + 1)))
                                max_panel_fc_formula += "IF(abs(PD{})==MPD,FCD{},".format(i + 1, i + 1)
                                max_panel_fc_tail += ")"
                                max_panel_fc_vars.append(
                                    panel.obj_y.snap.get_var('location.y', 'PD{}'.format(i + 1)))
                                max_panel_fc_vars.append(
                                    panel.get_prompt("Dog Ear Depth").get_var("FCD{}".format(i + 1)))

                            max_panel_formula += "))"
                            max_panel_fc_formula += max_panel_fc_tail

                            self.bottom_capping.get_prompt('Max Panel Depth').set_formula(max_panel_formula, max_panel_vars)
                            ppt_obj.snap.get_prompt('Max Panel Front Chamfer').set_formula(
                                max_panel_fc_formula, max_panel_fc_vars)
                            self.bottom_capping.dim_y(
                                "MPD-Max_Panel_Front_Chamfer",
                                [MPD, Max_Panel_Front_Chamfer])

                            self.get_included_openings(self.selected_panel_1, self.selected_panel_2)
                            for opening in self.openings:
                                bottom_kd = product.get_prompt("Remove Bottom Hanging Shelf " + opening)
                                if bottom_kd:
                                    bottom_kd.set_value(True)

                            return self.finish(context)

        return {'RUNNING_MODAL'}


bpy.utils.register_class(PROMPTS_Prompts_Bottom_Support)
bpy.utils.register_class(DROP_OPERATOR_Place_Bottom_Capping)
