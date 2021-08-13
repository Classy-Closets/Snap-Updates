from os import path
import math
import operator

import bpy
from bpy.types import Operator
from bpy.props import StringProperty, FloatProperty

from snap import sn_types, sn_unit, sn_utils
from ..ops.drop_closet import PlaceClosetInsert
from .. import closet_props
from ..common import common_parts
from ..common import common_prompts
from .. import closet_props


class Top(sn_types.Assembly):
    """ Closet Top Shelf
    """

    type_assembly = "INSERT"
    placement_type = "SPLITTER"
    id_prompt = "sn_closets.top"
    drop_id = "sn_closets.top_shelf_drop"
    show_in_library = True
    category_name = "Closet Products - Basic"
    mirror_y = True

    def add_oversize_prompts(self):
        for i in range(10):
            empty_name = "Oversize Cut {}".format(str(i+1))
            empty = self.add_empty(empty_name)
            
    def update(self):
        self.obj_x.location.x = self.width
        self.obj_y.location.y = -self.depth if self.mirror_y else self.depth
        self.obj_z.location.z = self.height

        self.obj_bp.snap.export_as_subassembly = True
        self.obj_bp['IS_BP_CLOSET_TOP'] = True
        self.obj_bp['ID_PROMPT'] = self.id_prompt
        self.obj_bp['ID_DROP'] = self.drop_id
        self.obj_bp.snap.placement_type = self.placement_type
        self.obj_bp.snap.type_group = self.type_assembly
        self.obj_bp.sn_closets.is_closet_top_bp = True
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
        self.add_prompt("Front Overhang", 'DISTANCE', sn_unit.inch(.5))
        self.add_prompt("Max Panel Depth", 'DISTANCE', 0)
        ppt_obj_panel_max = self.add_prompt_obj("Panel_Max")
        self.add_prompt("Max Panel Front Chamfer", 'DISTANCE', 0, prompt_obj=ppt_obj_panel_max)
        self.add_prompt("Max Rear Chamfer", 'DISTANCE', 0)

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
        
        top = common_parts.add_plant_on_top(self)
        constraint = top.obj_x.constraints.new(type='LIMIT_LOCATION')
        constraint.use_max_x = True
        constraint.max_x = sn_unit.inch(96)
        constraint.owner_space = 'LOCAL'
        top.obj_bp.snap.comment_2 = "1024"
        top.set_name("Topshelf")
        top.loc_x('IF(Extend_Left,0,Panel_Thickness/2)-Extend_Left_Amount',[Extend_Left,Extend_Left_Amount,Panel_Thickness])

        top.rot_x(value=math.radians(180))
        top.dim_x('Width-IF(Extend_Left,0,Panel_Thickness/2)-IF(Extend_Right,0,Panel_Thickness/2)+Extend_Left_Amount+Extend_Right_Amount',
                  [Width,Extend_Left,Extend_Right,Panel_Thickness,Extend_Right_Amount,Extend_Left_Amount])
        top.dim_y('Depth+Front_Overhang',[Depth,Front_Overhang])
        top.dim_z('-Panel_Thickness',[Panel_Thickness])
        
        self.update()


class PROMPTS_Top_Shelf(sn_types.Prompts_Interface):
    bl_idname = "sn_closets.top"
    bl_label = "Top Shelf Prompt"
    bl_options = {'UNDO'}
    
    object_name: StringProperty(name="Object Name",
                                           description="Stores the Base Point Object Name \
                                           so the object can be retrieved from the database.")
    
    width: FloatProperty(name="Width",unit='LENGTH',precision=4)
    height: FloatProperty(name="Height",unit='LENGTH',precision=4)
    depth: FloatProperty(name="Depth",unit='LENGTH',precision=4)    
    
    insert = None
    top_shelf = None

    prev_ex_left = 0
    prev_ex_right = 0
    prev_width = 0

    def check(self, context):
        """ This is called everytime a change is made in the UI """
        self.check_width()
        closet_props.update_render_materials(self, context)
        return True

    def execute(self, context):
        """ This is called when the OK button is clicked """
        return {'FINISHED'}

    def invoke(self,context,event):
        """ This is called before the interface is displayed """
        self.insert = self.get_insert()
        wm = context.window_manager
        self.get_top_shelf_obj()
        self.set_previous_values()
        return wm.invoke_props_dialog(self, width=sn_utils.get_prop_dialog_width(400))

    def draw(self, context):
        """ This is where you draw the interface """
        layout = self.layout
        layout.label(text=self.insert.obj_bp.name)
        box = layout.box()

        top_assembly = sn_types.Assembly(obj_bp=self.top_shelf)
        exposed_left = top_assembly.get_prompt("Exposed Left")
        exposed_right = top_assembly.get_prompt("Exposed Right")
        exposed_back = top_assembly.get_prompt("Exposed Back")
        extend_left_amount = self.insert.get_prompt("Extend Left Amount")
        extend_right_amount = self.insert.get_prompt("Extend Right Amount")
        front_overhang = self.insert.get_prompt("Front Overhang")

        row = box.row()
        row.prop(extend_left_amount, "distance_value", text="Extend Left:")
        row = box.row()
        row.prop(extend_right_amount, "distance_value", text="Extend Right:")
        row = box.row()
        row.prop(front_overhang, "distance_value", text="Extend Front:")

        row = box.row()
        row.label(text="Exposed Edges:")
        row.prop(exposed_left, "checkbox_value", text="Left")
        row.prop(exposed_right, "checkbox_value", text="Right")
        row.prop(exposed_back, "checkbox_value", text="Back")

    def get_top_shelf_obj(self):
        children = self.insert.obj_bp.children
        for child in children:
            if "Topshelf" in child.name:
                self.top_shelf = child

    def check_width(self):
        extend_left_amount =\
            self.insert.get_prompt("Extend Left Amount").get_value()
        extend_right_amount =\
            self.insert.get_prompt("Extend Right Amount").get_value()
        width = self.insert.obj_x.location.x
        total_width =\
            extend_left_amount + extend_right_amount + width
        prev_total_width =\
            self.prev_ex_left + self.prev_ex_right + self.width
        max_width = sn_unit.inch(96)
        is_width_augmented =\
            round(prev_total_width, 2) < round(max_width, 2)
        limit_reached =\
            round(total_width, 2) >= round(max_width, 2) and is_width_augmented
        if limit_reached:
            bpy.ops.snap.log_window("INVOKE_DEFAULT",
                                    message="Maximum Top Shelf width is 96\"",
                                    message2="You can add another Top Shelf",
                                    icon="ERROR")
            if self.prev_ex_left == extend_left_amount:
                self.insert.get_prompt(
                    "Extend Right Amount").set_value(self.prev_ex_right)
            if self.prev_ex_right == extend_right_amount:
                self.insert.get_prompt(
                    "Extend Left Amount").set_value(self.prev_ex_left)
        else:
            self.prev_ex_left = extend_left_amount
            self.prev_ex_right = extend_right_amount
        self.prev_width = width

    def set_previous_values(self):
        ex_left_amount_value =\
            self.insert.get_prompt("Extend Left Amount").get_value()
        ex_right_amount_value =\
            self.insert.get_prompt("Extend Right Amount").get_value()
        self.prev_ex_left = ex_left_amount_value
        self.prev_ex_right = ex_right_amount_value
        self.prev_width = self.insert.obj_x.location.x


bpy.utils.register_class(PROMPTS_Top_Shelf)


class SN_CLOSET_OT_Place_Top(Operator, PlaceClosetInsert):
    bl_idname = "sn_closets.top_shelf_drop"
    bl_label = "Place Top"
    bl_description = "This places the top."
    bl_options = {'UNDO'}

    show_openings = False
    top_shelf = None
    selected_panel_1 = None
    selected_panel_2 = None
    objects = []
    panels = []
    max_shelf_length = 96.0
    sel_product_bp = None
    panel_bps = []
    header_text = "Place Top Shelf - Select Partitions (Left to Right)   (Esc, Right Click) = Cancel Command  :  (Left Click) = Select Panel"
    
    # def __del__(self):
    #     bpy.context.area.header_text_set()

    def execute(self, context):
        self.top_shelf = self.asset
        return super().execute(context)

    def get_deepest_panel(self):
        depths = []
        for p in self.panels:
            depths.append(abs(p.obj_y.location.y))
        return max(depths)

    def get_closest_opening(self,x_loc):
        return lambda op : abs(op - x_loc)

    def get_panels(self):
        self.panel_bps.clear()

        for child in self.sel_product_bp.children:
            if 'IS_BP_PANEL' in child and 'PARTITION_NUMBER' in child:
                self.panel_bps.append(child)

        self.panel_bps.sort(key=lambda a: int(a['PARTITION_NUMBER']))

        for i,bp in enumerate(self.panel_bps):
            print(i,sn_unit.inch(bp.location.x))
            
    def is_first_panel(self, panel):
        if panel.obj_z.location.z < 0:
            return True
        else:
            return False

    def is_last_panel(self, panel):
        self.get_panels()
        last_panel_bp = self.panel_bps[-1]
        if panel.obj_bp is last_panel_bp:
            return True
        else:
            return False

    def get_inculded_panels(self,panel_1,panel_2):
        self.panels.clear()
        p1_x_loc = panel_1.obj_bp.location.x
        p2_x_loc = panel_2.obj_bp.location.x

        for child in self.sel_product_bp.children:
            if 'IS_BP_BLIND_CORNER_PANEL' in child:
                continue
            
            if 'IS_BP_PANEL' in child:
                if p1_x_loc <= child.location.x <= p2_x_loc:
                    self.panels.append(sn_types.Assembly(child))

    def place_insert(self, context, event):
        selected_point, selected_obj, _ = sn_utils.get_selection_point(context, event, objects=self.objects)
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

                        self.top_shelf.obj_bp.parent = self.sel_product_bp
                        self.top_shelf.obj_bp.location = hover_panel.obj_bp.location

                        if hover_panel.obj_z.location.z > 0:
                            self.top_shelf.obj_bp.location.x = hp_x_loc - sn_unit.inch(0.75)

                        self.top_shelf.obj_bp.location.z += hover_panel.obj_x.location.x
                        self.top_shelf.obj_x.location.x = sn_unit.inch(18.0)
                        self.top_shelf.obj_y.location.y = -hover_panel.obj_y.location.y

                    else:
                        self.get_inculded_panels(self.selected_panel_1, hover_panel)
                        sp1_x_loc = self.selected_panel_1.obj_bp.location.x
                        hp_x_loc = hover_panel.obj_bp.location.x
                        ts_length = hp_x_loc - sp1_x_loc
                        same_panel = self.selected_panel_1.obj_bp == hover_panel.obj_bp
                        same_product = self.selected_panel_1.obj_bp.parent == hover_panel.obj_bp.parent
                        hp_to_left = hp_x_loc < sp1_x_loc
                        hp_out_of_reach = sn_unit.meter_to_inch(ts_length) > self.max_shelf_length

                        if same_panel or hp_to_left or not same_product or hp_out_of_reach:
                            selected_obj.select_set(False)
                            if same_product and hp_out_of_reach:
                                bpy.ops.snap.log_window("INVOKE_DEFAULT",
                                            message="Maximum Top Shelf width is 96\"",
                                            message2="You can add another Top Shelf",
                                            icon="ERROR")
                            return {'RUNNING_MODAL'}

                        if self.is_first_panel(self.selected_panel_1):
                            self.top_shelf.obj_x.location.x = ts_length
                        else:
                            if hp_x_loc < sp1_x_loc:
                                #Hover selection to left
                                pass
                            else:
                                self.top_shelf.obj_x.location.x = ts_length + sn_unit.inch(0.75)

                        self.top_shelf.obj_y.location.y = self.get_deepest_panel()

                    if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                        if not self.selected_panel_1:
                            self.selected_panel_1 = hover_panel
                            sn_utils.set_wireframe(self.top_shelf.obj_bp,False)
                            bpy.ops.object.select_all(action='DESELECT')
                            context.view_layer.objects.active = self.top_shelf.obj_bp

                            self.top_shelf.obj_bp.parent = self.sel_product_bp
                            p1_z_loc = self.selected_panel_1.obj_bp.location.z
                            p1_z_dim = self.selected_panel_1.obj_x.location.x

                            if self.selected_panel_1.obj_z.location.z < 0:
                                self.top_shelf.obj_bp.location.x = self.selected_panel_1.obj_bp.location.x
                            else:
                                self.top_shelf.obj_bp.location.x = self.selected_panel_1.obj_bp.location.x - sn_unit.inch(0.75)
                            self.top_shelf.obj_bp.location.z = p1_z_loc + p1_z_dim
                            self.top_shelf.obj_y.location.y = -self.selected_panel_1.obj_y.location.y

                            return {'RUNNING_MODAL'}

                        if not self.selected_panel_2:
                            self.selected_panel_2 = hover_panel
                            bpy.ops.object.select_all(action='DESELECT')
                            context.view_layer.objects.active = self.top_shelf.obj_bp
                            self.top_shelf.obj_bp.select_set(True)

                            if self.selected_panel_1.obj_bp == self.selected_panel_2.obj_bp:
                                self.cancel_drop(context,event)
                                return {'FINISHED'}

                            pard = sn_types.Assembly(self.selected_panel_1.obj_bp.parent)
                            Left_Side_Wall_Filler = pard.get_prompt('Left Side Wall Filler').get_var()
                            Right_Side_Wall_Filler = pard.get_prompt('Right Side Wall Filler').get_var()

                            P1_X_Loc = self.selected_panel_1.obj_bp.snap.get_var('location.x', 'P1_X_Loc')
                            P2_X_Loc = self.selected_panel_2.obj_bp.snap.get_var('location.x', 'P2_X_Loc')
                            Panel_Thickness = product.get_prompt('Panel Thickness').get_var()
                            if self.is_first_panel(self.selected_panel_1):
                                self.top_shelf.loc_x('P1_X_Loc-Left_Side_Wall_Filler', [P1_X_Loc, Left_Side_Wall_Filler])
                                if self.is_last_panel(self.selected_panel_2):
                                    self.top_shelf.dim_x('P2_X_Loc-P1_X_Loc+Left_Side_Wall_Filler+Right_Side_Wall_Filler', 
                                        [P1_X_Loc, P2_X_Loc, Left_Side_Wall_Filler,Right_Side_Wall_Filler])
                                else:
                                    self.top_shelf.dim_x('P2_X_Loc-P1_X_Loc+Left_Side_Wall_Filler',
                                        [P1_X_Loc, P2_X_Loc, Left_Side_Wall_Filler])
                            else:
                                self.top_shelf.loc_x('P1_X_Loc-Panel_Thickness',[P1_X_Loc, Panel_Thickness, Left_Side_Wall_Filler])
                                if self.is_last_panel(self.selected_panel_2):
                                    self.top_shelf.dim_x('P2_X_Loc-P1_X_Loc+Panel_Thickness+Right_Side_Wall_Filler', 
                                        [P1_X_Loc, P2_X_Loc, Panel_Thickness, Right_Side_Wall_Filler])
                                else:
                                    self.top_shelf.dim_x('P2_X_Loc-P1_X_Loc+Panel_Thickness', 
                                        [P1_X_Loc, P2_X_Loc, Panel_Thickness])

                            max_panel_formula = "max(("
                            max_panel_vars = []
                            max_panel_fc_formula = ""
                            max_panel_fc_vars = []

                            MPD = self.top_shelf.get_prompt('Max Panel Depth').get_var('MPD')
                            Max_Panel_Front_Chamfer = self.top_shelf.get_prompt('Max Panel Front Chamfer').get_var()

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

                            self.top_shelf.get_prompt('Max Panel Depth').set_formula(max_panel_formula, max_panel_vars)
                            self.top_shelf.get_prompt('Max Panel Front Chamfer').set_formula(
                                max_panel_fc_formula, max_panel_fc_vars)
                            self.top_shelf.dim_y(
                                "MPD-Max_Panel_Front_Chamfer",
                                [MPD, Max_Panel_Front_Chamfer])

                            return self.finish(context)

        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        bpy.ops.object.select_all(action='DESELECT')
        context.area.tag_redraw()
        context.area.header_text_set(text=self.header_text)
        self.reset_selection()

        if self.event_is_cancel_command(event):
            context.area.header_text_set(None)
            return self.cancel_drop(context)

        if self.event_is_pass_through(event):
            return {'PASS_THROUGH'}

        return self.place_insert(context, event)


bpy.utils.register_class(SN_CLOSET_OT_Place_Top)
