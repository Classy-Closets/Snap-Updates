import math
from snap.sn_unit import inch

import bpy
from bpy.types import Operator
from bpy.props import StringProperty, FloatProperty

from snap import sn_types, sn_unit, sn_utils
from ..ops.drop_closet import PlaceClosetInsert
from ..common import common_parts
from ..common import common_prompts


class Base_Assembly(sn_types.Assembly):

    type_assembly = "PRODUCT"
    id_prompt = "sn_closets.toe_kick_prompts"
    drop_id = "sn_closets.place_base_assembly"
    show_in_library = True
    placement_type = ""

    library_name = ""
    category_name = ""

    def add_parts(self):
        self.add_prompt("Cleat Width", 'DISTANCE', sn_unit.inch(2.5))
        self.add_prompt("Extend Left Amount", 'DISTANCE', 0)
        self.add_prompt("Extend Right Amount", 'DISTANCE', 0)
        self.add_prompt("Extend Depth Amount", 'DISTANCE', 0)
        self.add_prompt("Variable Width", 'CHECKBOX', False)
        self.add_prompt("Variable Height", 'CHECKBOX', False)
        self.add_prompt("Is Island TK", 'CHECKBOX', False)
        self.add_prompt("TK Skin Thickness", 'DISTANCE', sn_unit.inch(0.25))
        self.add_prompt("Has TK Skin", 'CHECKBOX', False)
        self.add_prompt("Left Return", 'CHECKBOX', False)
        self.add_prompt("Right Return", 'CHECKBOX', False)
        self.add_prompt("Left", 'CHECKBOX', False)  # Deeper Toe Kick Left
        self.add_prompt("Right", 'CHECKBOX', False)  # Deeper Toe Kick Right

        Width = self.obj_x.snap.get_var('location.x', 'Width')
        Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        Height = self.get_prompt("Toe Kick Height").get_var("Height")
        Cleat_Width = self.get_prompt('Cleat Width').get_var()
        Toe_Kick_Thickness = self.get_prompt('Toe Kick Thickness').get_var()
        Extend_Left_Amount = self.get_prompt('Extend Left Amount').get_var()
        Extend_Depth_Amount = self.get_prompt('Extend Depth Amount').get_var()
        TK_Skin_Thickness = self.get_prompt("TK Skin Thickness").get_var()
        Has_TK_Skin = self.get_prompt("Has TK Skin").get_var()
        Left_Return = self.get_prompt("Left Return").get_var()
        Right_Return = self.get_prompt("Right Return").get_var()
        DTKL = self.get_prompt("Left").get_var('DTKL')
        DTKR = self.get_prompt("Right").get_var('DTKR')

        toe_kick_front = common_parts.add_toe_kick(self)
        toe_kick_front.set_name("Toe Kick Front")
        toe_kick_front.obj_bp.snap.comment_2 = "1034"

        TK_Thk = self.get_prompt('Toe Kick Thickness').get_var("TK_Thk")
        EL_Amt = self.get_prompt('Extend Left Amount').get_var("EL_Amt")
        ER_Amt = self.get_prompt('Extend Right Amount').get_var("ER_Amt")
        TK_Sk_Thk = self.get_prompt("TK Skin Thickness").get_var("TK_Sk_Thk")
        LR = self.get_prompt("Left Return").get_var("LR")
        RR = self.get_prompt("Right Return").get_var("RR")
        tk_dim_x =\
            "Width-(TK_Thk*3)+EL_Amt+ER_Amt"+\
            "-IF(DTKL,-TK_Sk_Thk,IF(LR,TK_Sk_Thk,0))"+\
            "-IF(DTKR,-TK_Sk_Thk,IF(RR,TK_Sk_Thk,0))"
        tk_dim_limit =\
            "Width-(TK_Thk)+EL_Amt+ER_Amt"+\
            "-IF(DTKL,-TK_Sk_Thk,IF(LR,TK_Sk_Thk,0))"+\
            "-IF(DTKR,-TK_Sk_Thk,IF(RR,TK_Sk_Thk,0))"
        toe_kick_front.dim_x(
            "IF(("+tk_dim_limit+")>INCH(97.5),INCH(96),"+tk_dim_x+")",
            [Width, TK_Thk, ER_Amt, EL_Amt, LR,
             RR, TK_Sk_Thk, DTKL, DTKR])
        toe_kick_front.dim_y('-Height', [Height])
        toe_kick_front.dim_z('Toe_Kick_Thickness', [Toe_Kick_Thickness])
        toe_kick_front.loc_x(
            "(Toe_Kick_Thickness*1.5)-Extend_Left_Amount"
            "+IF(DTKL,-TK_Skin_Thickness,IF(Left_Return,TK_Skin_Thickness,0))",
            [Toe_Kick_Thickness, Extend_Left_Amount, TK_Skin_Thickness, Left_Return, DTKL])
        toe_kick_front.loc_x('(Toe_Kick_Thickness*1.5)-Extend_Left_Amount', [Toe_Kick_Thickness, Extend_Left_Amount])
        toe_kick_front.loc_y('Depth-Extend_Depth_Amount', [Depth, Extend_Depth_Amount])
        toe_kick_front.rot_x(value=math.radians(-90))

        toe_kick = common_parts.add_toe_kick(self)
        toe_kick.set_name("Toe Kick Back")
        toe_kick.obj_bp.snap.comment_2 = "1034"
        toe_kick.dim_x(
            "IF(("+tk_dim_limit+")>INCH(97.5),INCH(96),"+tk_dim_x+")",
            [Width, TK_Thk, ER_Amt, EL_Amt, LR,
             RR, TK_Sk_Thk, DTKL, DTKR])
        toe_kick.dim_y('-Height', [Height])
        toe_kick.dim_z('-Toe_Kick_Thickness',[Toe_Kick_Thickness])
        toe_kick.loc_x(
            "(Toe_Kick_Thickness*1.5)-Extend_Left_Amount"
            "+IF(DTKL,-TK_Skin_Thickness,IF(Left_Return,TK_Skin_Thickness,0))",
            [Extend_Left_Amount, Toe_Kick_Thickness, TK_Skin_Thickness, Left_Return, DTKL])
        toe_kick.rot_x(value=math.radians(-90))

        left_toe_kick = common_parts.add_toe_kick_end_cap(self)
        left_toe_kick.dim_x('-Depth+Extend_Depth_Amount', [Depth, Extend_Depth_Amount])
        left_toe_kick.dim_y('-Height',[Height])
        left_toe_kick.dim_z('Toe_Kick_Thickness', [Toe_Kick_Thickness])
        left_toe_kick.loc_x(
            "-Extend_Left_Amount+(Toe_Kick_Thickness/2)"
            "+IF(DTKL,-TK_Skin_Thickness,IF(Left_Return,TK_Skin_Thickness,0))",
            [Extend_Left_Amount, Toe_Kick_Thickness, Left_Return, TK_Skin_Thickness, DTKL])
        left_toe_kick.rot_x(value=math.radians(-90))
        left_toe_kick.rot_z(value=math.radians(-90))

        right_toe_kick_limit_x = "INCH(96)-EL_Amt+2.5*TK_Thk"
        right_tk_x_loc =\
            "Width+ER_Amt-(TK_Thk/2)" +\
            "-IF(DTKR,-TK_Sk_Thk,IF(RR,TK_Sk_Thk,0))"
        right_toe_kick = common_parts.add_toe_kick_end_cap(self)
        right_toe_kick.dim_x('-Depth+Extend_Depth_Amount', [Depth, Extend_Depth_Amount])
        right_toe_kick.dim_y('Height',[Height])
        right_toe_kick.dim_z('Toe_Kick_Thickness', [Toe_Kick_Thickness])
        right_toe_kick.loc_x(
            "IF(("+tk_dim_limit+")>INCH(97.5),"+right_toe_kick_limit_x+","+right_tk_x_loc+")",
            [Width, TK_Thk, ER_Amt, EL_Amt, LR,
             RR, TK_Sk_Thk, DTKL, DTKR])
        right_toe_kick.rot_x(value=math.radians(90))
        right_toe_kick.rot_z(value=math.radians(-90))

        toe_kick_stringer = common_parts.add_toe_kick_stringer(self)
        toe_kick_stringer.dim_x(
            "IF(("+tk_dim_limit+")>INCH(97.5),INCH(96),"+tk_dim_x+")",
            [Width, TK_Thk, ER_Amt, EL_Amt, LR,
             RR, TK_Sk_Thk, DTKL, DTKR])
        toe_kick_stringer.dim_y('Cleat_Width', [Cleat_Width])
        toe_kick_stringer.dim_z('Toe_Kick_Thickness', [Toe_Kick_Thickness])
        toe_kick_stringer.loc_x(
            "(Toe_Kick_Thickness*1.5)-Extend_Left_Amount"
            "+IF(DTKL,-TK_Skin_Thickness,IF(Left_Return,TK_Skin_Thickness,0))",
            [Extend_Left_Amount, Toe_Kick_Thickness, TK_Skin_Thickness, Left_Return, DTKL])
        toe_kick_stringer.loc_y(
            'Depth+Toe_Kick_Thickness-Extend_Depth_Amount',
            [Depth, Toe_Kick_Thickness, Extend_Depth_Amount])
        toe_kick_stringer.loc_z('Height-Toe_Kick_Thickness', [Height, Toe_Kick_Thickness])

        toe_kick_stringer = common_parts.add_toe_kick_stringer(self)
        toe_kick_stringer.dim_x(
            "IF(("+tk_dim_limit+")>INCH(97.5),INCH(96),"+tk_dim_x+")",
            [Width, TK_Thk, ER_Amt, EL_Amt, LR,
             RR, TK_Sk_Thk, DTKL, DTKR])
        toe_kick_stringer.dim_y('-Cleat_Width', [Cleat_Width])
        toe_kick_stringer.dim_z('Toe_Kick_Thickness', [Toe_Kick_Thickness])
        toe_kick_stringer.loc_x(
            "(Toe_Kick_Thickness*1.5)-Extend_Left_Amount"
            "+IF(DTKL,-TK_Skin_Thickness,IF(Left_Return,TK_Skin_Thickness,0))",
            [Extend_Left_Amount, Toe_Kick_Thickness, TK_Skin_Thickness, Left_Return, DTKL])
        toe_kick_stringer.loc_y('-Toe_Kick_Thickness', [Toe_Kick_Thickness])

        toe_kick_skin = common_parts.add_toe_kick_skin(self)
        tk_skin_x =\
            "Width-(TK_Thk)+EL_Amt+ER_Amt" +\
            "+IF(AND(DTKL,LR),TK_Sk_Thk,0)+IF(AND(DTKR,RR),TK_Sk_Thk,0)"
        toe_kick_skin.dim_x(
            "IF(("+tk_dim_limit+")>INCH(97.5),INCH(97.5),"+tk_skin_x+")",
            [Width, TK_Thk, ER_Amt, EL_Amt, LR,
             RR, TK_Sk_Thk, DTKL, DTKR])

        toe_kick_skin.dim_y('-Height', [Height])
        toe_kick_skin.dim_z('TK_Skin_Thickness', [TK_Skin_Thickness])
        toe_kick_skin.loc_x(
            '(Toe_Kick_Thickness*0.5)-Extend_Left_Amount-IF(AND(DTKL,Left_Return),TK_Skin_Thickness,0)',
            [Toe_Kick_Thickness, Extend_Left_Amount, DTKL, TK_Skin_Thickness, Left_Return])
        toe_kick_skin.loc_y('Depth-Extend_Depth_Amount-TK_Skin_Thickness',
                            [Depth, Extend_Depth_Amount, TK_Skin_Thickness])
        toe_kick_skin.rot_x(value=math.radians(-90))
        toe_kick_skin.get_prompt('Hide').set_formula("IF(Has_TK_Skin,False,True) or Hide", [self.hide_var, Has_TK_Skin])

        left_skin_return = common_parts.add_toe_kick_skin(self)
        left_skin_return.set_name("Toe Kick Skin Left Return")
        left_skin_return.dim_x('-Depth+Extend_Depth_Amount', [Depth, Extend_Depth_Amount])
        left_skin_return.dim_y('-Height', [Height])
        left_skin_return.dim_z('TK_Skin_Thickness', [TK_Skin_Thickness])
        left_skin_return.loc_x(
            '-Extend_Left_Amount+(Toe_Kick_Thickness/2)-IF(DTKL,TK_Skin_Thickness,0)',
            [Extend_Left_Amount, Toe_Kick_Thickness, DTKL, TK_Skin_Thickness])
        left_skin_return.rot_x(value=math.radians(-90))
        left_skin_return.rot_z(value=math.radians(-90))
        left_skin_return.get_prompt('Hide').set_formula("IF(Left_Return,False,True) or Hide", [self.hide_var, Left_Return])

        right_skin_limit_x = "INCH(96)-EL_Amt+3.5*TK_Thk"
        right_skin_x_loc =\
            "Width+ER_Amt-(TK_Thk/2)" +\
            "-IF(DTKR,0,TK_Sk_Thk)"

        right_skin_return = common_parts.add_toe_kick_skin(self)
        right_skin_return.set_name("Toe Kick Skin Right Return")
        right_skin_return.dim_x('-Depth+Extend_Depth_Amount', [Depth, Extend_Depth_Amount])
        right_skin_return.dim_y('-Height', [Height])
        right_skin_return.dim_z('TK_Skin_Thickness', [TK_Skin_Thickness])
        right_skin_return.loc_x(
            "IF(("+tk_dim_limit+")>INCH(97.5),"+right_skin_limit_x+","+right_skin_x_loc+")",
            [Width, TK_Thk, ER_Amt, EL_Amt, LR,
             RR, TK_Sk_Thk, DTKL, DTKR])
        right_skin_return.rot_x(value=math.radians(-90))
        right_skin_return.rot_z(value=math.radians(-90))
        right_skin_return.get_prompt('Hide').set_formula("IF(Right_Return,False,True) or Hide", [self.hide_var, Right_Return])

    def update(self):
        super().update()

        self.obj_x.location.x = self.width
        self.obj_z.location.z = self.height
        self.obj_y.location.y = -self.depth
        self.obj_bp.snap.export_as_subassembly = True
        self.obj_bp.sn_closets.is_toe_kick_insert_bp = True

    def draw(self):
        self.create_assembly()
        # we are adding a master hide for everything
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()
        common_prompts.add_toe_kick_prompts(self)
        common_prompts.add_thickness_prompts(self)
        self.add_parts()
        self.update()


class PROMPTS_Toe_Kick_Prompts(sn_types.Prompts_Interface):
    bl_idname = "sn_closets.toe_kick_prompts"
    bl_label = "Toe Kick Prompt"
    bl_options = {'UNDO'}

    object_name: StringProperty(name="Object Name",
                                description="Stores the Base Point Object Name so the "
                                            "object can be retrieved from the database.")

    width: FloatProperty(name="Width", unit='LENGTH', precision=4)
    height: FloatProperty(name="Height", unit='LENGTH', precision=4)
    depth: FloatProperty(name="Depth", unit='LENGTH', precision=4)

    product = None

    prev_ex_left = 0
    prev_ex_right = 0

    def check_width(self):
        ex_left_amount_value =\
            self.product.get_prompt("Extend Left Amount").get_value()
        ex_right_amount_value =\
            self.product.get_prompt("Extend Right Amount").get_value()
        self.width = math.fabs(self.product.obj_x.location.x)
        TK_Thk = self.product.get_prompt('Toe Kick Thickness').get_value()
        width =\
            self.width + ex_left_amount_value + ex_right_amount_value - TK_Thk
        prev_width =\
            self.prev_ex_left + self.prev_ex_right + self.prev_width - TK_Thk
        max_width = sn_unit.inch(97.5)
        is_width_augmented = round(prev_width, 2) < round(max_width, 2)
        limit_reached =\
            round(width, 2) >= round(max_width, 2) and is_width_augmented
        if limit_reached:
            bpy.ops.snap.log_window("INVOKE_DEFAULT",
                                    message="Maximum Toe Kick width is 97.5\"",
                                    message2="You can add another Toe Kick",
                                    icon="ERROR")
            if self.prev_ex_left == ex_left_amount_value:
                self.product.get_prompt(
                    "Extend Right Amount").set_value(self.prev_ex_right)
            if self.prev_ex_right == ex_right_amount_value:
                self.product.get_prompt(
                    "Extend Left Amount").set_value(self.prev_ex_left)
        else:
            self.prev_ex_left = ex_left_amount_value
            self.prev_ex_right = ex_right_amount_value
        self.prev_width = self.width

    def check_tk_height(self):
        toe_kick_height =\
            self.product.get_prompt("Toe Kick Height").distance_value
        if toe_kick_height < inch(3):
            self.product.get_prompt("Toe Kick Height").set_value(inch(3))
            bpy.ops.snap.log_window('INVOKE_DEFAULT',
                                    message="Minimum Toe Kick Height is 3\"",
                                    icon="ERROR")

    def update_tk_height_parent(self):
        toe_kick_height =\
            self.product.get_prompt("Toe Kick Height").distance_value
        parent = self.product.obj_bp.parent
        children = parent.children
        closet = sn_types.Assembly(obj_bp=parent)
        closet.get_prompt("Toe Kick Height").set_value(toe_kick_height)
        for child in children:
            if "Toe Kick" in child.name:
                toe_kick = child
                tk = sn_types.Assembly(toe_kick)
                tk.get_prompt("Toe Kick Height").set_value(toe_kick_height)

    def update_top_shelf_location(self, top_shelf):
        top_assembly = sn_types.Assembly(obj_bp=top_shelf)
        closet_obj = self.product.obj_bp.parent
        closet = sn_types.Assembly(obj_bp=closet_obj)
        opening_prompt = closet.get_prompt("Opening Quantity")
        if not opening_prompt:
            return
        opening_qty = closet.get_prompt("Opening Quantity").get_value()
        left_thk = closet.get_prompt("Left Side Thickness").get_value()
        panel_thk = closet.get_prompt("Panel Thickness").get_value()
        right_thk = closet.get_prompt("Left Side Thickness").get_value()
        width_1 = closet.get_prompt("Opening 1 Width").distance_value
        tk_height = closet.get_prompt("Toe Kick Height").distance_value
        opening_x0 = 0
        opening_xf = left_thk + width_1 + panel_thk
        top_x0 = top_shelf.location.x
        dim_x = top_assembly.obj_x.location.x
        if dim_x > sn_unit.inch(96):
            dim_x = sn_unit.inch(96)
        top_xf = top_shelf.location.x + dim_x
        is_closet_floor_mounted = True
        max_op_height = 0
        for i in range(1, opening_qty + 1):
            height = closet.get_prompt("Opening " + str(i) + " Height")
            width =\
                closet.get_prompt(
                    "Opening " + str(i) + " Width").distance_value
            height = height.distance_value
            is_floor_mounted =\
                closet.get_prompt(
                    "Opening " + str(i) + " Floor Mounted").get_value()
            if round(top_x0, 2) <= round(opening_x0, 2) and round(top_xf, 2) >= round(opening_xf, 2):
                is_op_reached = True
            else:
                is_op_reached = False
            if is_op_reached:
                is_closet_floor_mounted =\
                    is_closet_floor_mounted and is_floor_mounted
                if height > max_op_height:
                    max_op_height = height
            opening_x0 = opening_xf
            if i == opening_qty-1:
                opening_xf += width + right_thk
            else:
                opening_xf += width + panel_thk
        if is_closet_floor_mounted:
            top_shelf.location.z = max_op_height + tk_height
        else:
            top_shelf.location.z = closet.obj_z.location.z

    def check_parent_top_location(self):
        parent = self.product.obj_bp.parent
        children = parent.children
        for child in children:
            if "Top Shelf" in child.name:
                top_shelf = child
                self.update_top_shelf_location(top_shelf)

    def update_tk_ex_depth_amount(self):
        closet_obj = self.product.obj_bp.parent
        closet = sn_types.Assembly(obj_bp=closet_obj)
        opening_qty_prompt = closet.get_prompt("Opening Quantity")
        if not opening_qty_prompt:
            return
        ex_depth_amount =\
            self.product.get_prompt("Extend Depth Amount").distance_value
        parent = self.product.obj_bp.parent
        children = parent.children
        for child in children:
            if "Toe Kick" in child.name:
                toe_kick = child
                tk = sn_types.Assembly(toe_kick)
                tk.get_prompt("Extend Depth Amount").set_value(ex_depth_amount)

    def check_hang_height(self):
        closet_obj = self.product.obj_bp.parent
        closet = sn_types.Assembly(obj_bp=closet_obj)
        opening_qty_prompt = closet.get_prompt("Opening Quantity")
        if not opening_qty_prompt:
            return
        opening_qty = closet.get_prompt("Opening Quantity").get_value()
        for i in range(1, opening_qty + 1):
            is_floor_mounted =\
                closet.get_prompt(
                    "Opening " + str(i) + " Floor Mounted").get_value()
            if is_floor_mounted:
                tk_height = closet.get_prompt("Toe Kick Height").distance_value
                opening_height =\
                    closet.get_prompt(
                        "Opening " + str(i) + " Height").distance_value
                height = opening_height + tk_height
                if height > closet.obj_z.location.z:
                    closet.obj_z.location.z = height
                    self.hang_heigh = height

    def check(self, context):
        """ This is called everytime a change is made in the UI """
        self.check_tk_height()
        self.update_product_size()
        self.check_width()
        self.update_tk_height_parent()
        self.check_hang_height()
        self.check_parent_top_location()
        self.update_tk_ex_depth_amount()
        return True

    def set_extend_amounts(self):
        ex_left_amount_value =\
            self.product.get_prompt("Extend Left Amount").get_value()
        ex_right_amount_value =\
            self.product.get_prompt("Extend Right Amount").get_value()
        self.prev_ex_left = ex_left_amount_value
        self.prev_ex_right = ex_right_amount_value

    def execute(self, context):
        """ This is called when the OK button is clicked """
        self.update_product_size()
        return {'FINISHED'}

    def invoke(self, context, event):
        """ This is called before the interface is displayed """
        self.product = self.get_insert()
        self.set_extend_amounts()
        self.depth = math.fabs(self.product.obj_y.location.y)
        self.height = math.fabs(self.product.obj_z.location.z)
        self.width = math.fabs(self.product.obj_x.location.x)
        self.prev_width = self.width
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=sn_utils.get_prop_dialog_width(550))

    def draw_product_size(self, layout, use_rot_z=True):

        toe_kick_height = self.product.get_prompt("Toe Kick Height")

        box = layout.box()
        row = box.row()

        col = row.column(align=True)
        row1 = col.row(align=True)
        if sn_utils.object_has_driver(self.product.obj_x):
            row1.label(text='Width: ' + str(sn_unit.meter_to_active_unit(math.fabs(self.product.obj_x.location.x))))
        else:
            row1.label(text='Width:')
            row1.prop(self, 'width', text="")

        row1 = col.row(align=True)
        row1.label(text='Height:')
        row1.prop(toe_kick_height, "distance_value", text="")

        row1 = col.row(align=True)
        if sn_utils.object_has_driver(self.product.obj_y):
            row1.label(text='Depth: ' + str(sn_unit.meter_to_active_unit(math.fabs(self.product.obj_y.location.y))))
        else:
            row1.label(text='Depth:')
            row1.prop(self, 'depth',text="")

        col = row.column(align=True)
        col.label(text="Location X:")
        col.label(text="Location Y:")
        col.label(text="Location Z:")

        col = row.column(align=True)
        col.prop(self.product.obj_bp, 'location', text="")

        if use_rot_z:
            row = box.row()
            row.label(text='Rotation Z:')
            row.prop(self.product.obj_bp, 'rotation_euler', index=2, text="")

    def draw(self, context):
        """ This is where you draw the interface """
        layout = self.layout
        layout.label(text=self.product.obj_bp.snap.name_object)
        self.draw_product_size(layout)

        box = layout.box()
        ex_left_amount = self.product.get_prompt("Extend Left Amount")
        ex_left_amount.draw(box, allow_edit=False)

        ex_right_amount = self.product.get_prompt("Extend Right Amount")
        ex_right_amount.draw(box, allow_edit=False)

        ex_depth_amount = self.product.get_prompt("Extend Depth Amount")
        ex_depth_amount.draw(box, allow_edit=False)

        variable_width = self.product.get_prompt("Variable Width")
        variable_width.draw(box, allow_edit=False)

        variable_height = self.product.get_prompt("Variable Height")
        variable_height.draw(box, allow_edit=False)

        has_tk_skin = self.product.get_prompt("Has TK Skin")
        left_return = self.product.get_prompt("Left Return")
        right_return = self.product.get_prompt("Right Return")
        deeper_tk_left = self.product.get_prompt("Left")
        deeper_tk_right = self.product.get_prompt("Right")

        if has_tk_skin:
            box = layout.box()
            box.label(text='1/4" Toe Kick Skin Options')
            row = box.row()
            has_tk_skin.draw(row, alt_text='Add 1/4" Toe Kick Skin: ', allow_edit=False)

            if has_tk_skin.get_value():
                if left_return and right_return:
                    row = box.row()
                    row.label(text='1/4" Skin Returns')
                    left_return.draw(row, allow_edit=False)
                    right_return.draw(row, allow_edit=False)
                    row = box.row()
                    row.label(text='Deeper Adjacent Toe Kicks: ')
                    deeper_tk_left.draw(row, allow_edit=False)
                    deeper_tk_right.draw(row, allow_edit=False)


class DROP_OPERATOR_Place_Base_Assembly(Operator, PlaceClosetInsert):
    bl_idname = "sn_closets.place_base_assembly"
    bl_label = "Place Base Assembly"
    bl_description = "This places the base assembly"
    bl_options = {'UNDO'}

    # READONLY
    object_name: StringProperty(name="Object Name")

    product = None
    selected_obj = None
    selected_point = None
    selected_panel_1 = None
    max_shelf_length = 96.0

    def execute(self, context):
        self.is_log_shown = False
        self.product = self.asset
        if "Toe_Kick" in str(type(self.insert)):
            self.max_shelf_length = 96.0
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

    def is_first_panel(self, panel):
        if panel.obj_z.location.z < 0:
            return True
        else:
            return False

    def get_Ext_Depth_Amount(self, closet):
        children = closet.children
        for child in children:
            if "Toe Kick" in child.name:
                tk = sn_types.Assembly(obj_bp=child)
                Ext_Depth_Amount =\
                    tk.get_prompt("Extend Depth Amount").distance_value
                return Ext_Depth_Amount
        return 0

    def product_drop(self, context, event):
        selected_panel_2 = None

        if self.selected_obj is not None:
            sel_product_bp = sn_utils.get_bp(self.selected_obj, 'PRODUCT')
            sel_assembly_bp = sn_utils.get_assembly_bp(self.selected_obj)
            product = sn_types.Assembly(sel_product_bp)

            if sel_assembly_bp:
                hover_panel = sn_types.Assembly(self.selected_obj.parent)
                props = sel_assembly_bp.sn_closets
                is_end_cap = "End Cap" in self.selected_obj.parent.name
                is_right = hover_panel.obj_bp.location.x > sn_unit.inch(1)
                is_right_end_cap = is_end_cap and is_right
                if props.is_panel_bp or is_right_end_cap:
                    self.selected_obj.select_set(True)
                    selected_panel_2 = sn_types.Assembly(sel_assembly_bp)
                if not self.selected_panel_1 and product.obj_x is not None:
                    hv_x_loc = hover_panel.obj_bp.location.x
                    if "End Cap" in hover_panel.obj_bp.name:
                        hv_x_loc += hover_panel.obj_bp.parent.location.x
                    if round(hv_x_loc, 1) == round(product.obj_x.location.x, 1):
                        self.selected_obj.select_set(False)
                        return {'RUNNING_MODAL'}
                if "Toe_Kick" in str(type(self.insert)) and self.selected_panel_1:
                    hv_x_loc = hover_panel.obj_bp.location.x
                    sp1_x_loc = self.selected_panel_1.obj_bp.location.x
                    same_panel = self.selected_panel_1.obj_bp == hover_panel.obj_bp
                    if "End Cap" in self.selected_panel_1.obj_bp.name:
                        same_product =\
                            self.selected_panel_1.obj_bp.parent.parent == hover_panel.obj_bp.parent
                        sp1_x_loc += self.selected_panel_1.obj_bp.parent.location.x
                    else:
                        same_product =\
                            self.selected_panel_1.obj_bp.parent == hover_panel.obj_bp.parent
                    hp_to_left = round(hv_x_loc, 1) <= round(sp1_x_loc, 1)
                    ts_length = hv_x_loc - sp1_x_loc
                    hp_out_of_reach =\
                        sn_unit.meter_to_inch(ts_length) > self.max_shelf_length

                    if same_panel or hp_to_left or not same_product or hp_out_of_reach:
                        self.selected_obj.select_set(False)
                        if not self.is_log_shown and same_product and hp_out_of_reach:
                            bpy.ops.snap.log_window("INVOKE_DEFAULT",
                                        message="Maximum Toe Kick width is 97.5\"",
                                        message2="You can add another Toe Kick",
                                        icon="ERROR")
                            self.is_log_shown = True 
                        return {'RUNNING_MODAL'}

                    if self.is_first_panel(self.selected_panel_1):
                        self.product.obj_x.location.x = ts_length
                    else:
                        if hv_x_loc < sp1_x_loc:
                            pass
                        else:
                            self.product.obj_x.location.x = ts_length + sn_unit.inch(0.75)

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

                    Toe_Kick_Setback = carcass_assembly.get_prompt("Toe Kick Setback").get_var()
                    Panel_Thickness = carcass_assembly.get_prompt("Panel Thickness").get_var()
                    P1_X_Loc = self.selected_panel_1.obj_bp.snap.get_var('location.x','P1_X_Loc')
                    P2_X_Loc = selected_panel_2.obj_bp.snap.get_var('location.x','P2_X_Loc')

                    if "End Cap" in self.selected_panel_1.obj_bp.name:
                        Parent_X_Loc = self.selected_panel_1.obj_bp.parent.snap.get_var('location.x', 'Parent_X_Loc')
                        self.product.loc_x(
                            'IF(P1_X_Loc>0,P1_X_Loc+Parent_X_Loc-Panel_Thickness,0)',
                            [P1_X_Loc,Panel_Thickness, Parent_X_Loc])
                        self.product.dim_x(
                            'P2_X_Loc-IF(P1_X_Loc>0,P1_X_Loc+Parent_X_Loc-Panel_Thickness,0)',
                            [P1_X_Loc,P2_X_Loc,Panel_Thickness, Parent_X_Loc])
                        tk_setback = '0'
                        ext_depth = 'Extend_Depth_Amount'
                        panel_assembly = sn_types.Assembly(obj_bp=panel_1_bp)
                        tk_assembly = sn_types.Assembly(obj_bp=panel_1_bp.parent)
                        toe_kick_height = abs(panel_assembly.obj_y.location.y)
                        self.product.get_prompt("Toe Kick Height").set_value(toe_kick_height)
                        ext_Depth_Amount = tk_assembly.get_prompt("Extend Depth Amount").distance_value
                        self.product.get_prompt("Extend Depth Amount").set_value(ext_Depth_Amount)
                        panel_depth_1 = abs(self.selected_panel_1.obj_x.location.x) - ext_Depth_Amount
                        Panel_Depth_1 = self.selected_panel_1.obj_x.snap.get_var('location.x', 'Panel_Depth_1')
                    else:
                        self.product.loc_x('IF(P1_X_Loc>0,P1_X_Loc-Panel_Thickness,0)',[P1_X_Loc,Panel_Thickness])
                        self.product.dim_x(
                            'IF(P2_X_Loc-IF(P1_X_Loc>0,P1_X_Loc-Panel_Thickness,0)>INCH(97.5),'
                            'INCH(97.5),'
                            'P2_X_Loc-IF(P1_X_Loc>0,P1_X_Loc-Panel_Thickness,0))',
                            [P1_X_Loc,P2_X_Loc,Panel_Thickness])
                        panel_depth_1 = abs(self.selected_panel_1.obj_y.location.y)
                        Panel_Depth_1 = self.selected_panel_1.obj_y.snap.get_var('location.y', 'Panel_Depth_1')
                        tk_setback = 'Toe_Kick_Setback'
                        ext_depth = '0'
                        closet_obj = panel_1_bp.parent
                        closet = sn_types.Assembly(obj_bp=closet_obj)
                        toe_kick_height = closet.get_prompt("Toe Kick Height").distance_value
                        self.product.get_prompt("Toe Kick Height").set_value(toe_kick_height)
                        ext_Depth_Amount = self.get_Ext_Depth_Amount(closet_obj)
                        self.product.get_prompt("Extend Depth Amount").set_value(ext_Depth_Amount)

                    Extend_Depth_Amount = self.product.get_prompt('Extend Depth Amount').get_var()
                    panel_depth_2 = abs(selected_panel_2.obj_y.location.y)
                    Panel_Depth_2 = selected_panel_2.obj_y.snap.get_var('location.y', 'Panel_Depth_2')
                    if panel_depth_1 > panel_depth_2:
                        self.product.dim_y(
                            '-abs(Panel_Depth_2)+' + tk_setback+ '+' + ext_depth,
                            [Panel_Depth_2, Toe_Kick_Setback, Extend_Depth_Amount])
                    else:
                        self.product.dim_y(
                            '-abs(Panel_Depth_1)+' + tk_setback + '+' + ext_depth,
                            [Panel_Depth_1, Toe_Kick_Setback, Extend_Depth_Amount])

                    self.product.obj_bp.snap.type_group = 'INSERT'
                    self.product.obj_bp.location.z = 0

                    return self.finish(context)
                else:
                    return {'RUNNING_MODAL'}

            if event.type == 'LEFTMOUSE' and event.value == 'PRESS' and self.selected_panel_1 == None:
                self.selected_panel_1 = selected_panel_2
                if self.selected_panel_1 and self.selected_panel_1.obj_bp:
                    sn_utils.set_wireframe(self.product.obj_bp,False)
                    bpy.context.window.cursor_set('DEFAULT')
                    bpy.ops.object.select_all(action='DESELECT')
                    context.view_layer.objects.active = self.product.obj_bp
                    self.product.obj_bp.parent = sel_product_bp
                    if "End Cap" in self.selected_panel_1.obj_bp.name:
                        self.product.obj_bp.location = self.selected_panel_1.obj_bp.location
                        parent_loc_x = self.selected_panel_1.obj_bp.parent.location.x
                        self.product.obj_bp.location.x += parent_loc_x
                        panel_1_bp = self.selected_panel_1.obj_bp
                        tk_assembly = sn_types.Assembly(obj_bp=panel_1_bp)
                        toe_kick_height = abs(tk_assembly.obj_y.location.y)
                        self.product.get_prompt("Toe Kick Height").set_value(toe_kick_height)
                        self.product.obj_y.location.y = -tk_assembly.obj_x.location.x
                    else:
                        if self.selected_panel_1.obj_z.location.z > 0:
                            #CENTER OR RIGHT PANEL SELECTED
                            self.product.obj_bp.location = self.selected_panel_1.obj_bp.location
                            self.product.obj_bp.location.x -= self.selected_panel_1.obj_z.location.z
                        else:
                            #LEFT PANEL SELECTED
                            self.product.obj_bp.location = self.selected_panel_1.obj_bp.location
                        closet = self.selected_panel_1.obj_bp.parent
                        closet_assembly = sn_types.Assembly(obj_bp=closet)
                        tk_setback = closet_assembly.get_prompt("Toe Kick Setback").distance_value
                        ext_Depth_Amount = self.get_Ext_Depth_Amount(closet)
                        dim_y = self.selected_panel_1.obj_y.location.y + tk_setback - ext_Depth_Amount
                        self.product.obj_y.location.y = dim_y
                        toe_kick_height = closet_assembly.get_prompt("Toe Kick Height").distance_value
                        self.product.get_prompt("Toe Kick Height").set_value(toe_kick_height)
                    self.product.obj_bp.location.z = 0
                    
        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        context.area.tag_redraw()
        self.reset_selection()
        bpy.ops.object.select_all(action='DESELECT')
        self.selected_point, self.selected_obj, _ = sn_utils.get_selection_point(context,event)

        if self.event_is_cancel_command(event):
            context.area.header_text_set(None)
            return self.cancel_drop(context)

        if self.event_is_pass_through(event):
            return {'PASS_THROUGH'}
        
        return self.product_drop(context, event)


bpy.utils.register_class(DROP_OPERATOR_Place_Base_Assembly)
bpy.utils.register_class(PROMPTS_Toe_Kick_Prompts)
