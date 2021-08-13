import math

import bpy
from bpy.types import Operator
from bpy.props import StringProperty, EnumProperty

from snap import sn_types, sn_unit, sn_utils
from ..ops.drop_closet import PlaceClosetInsert
from .. import closet_props
from ..common import common_parts
from ..common import common_prompts


class Countertop_Insert(sn_types.Assembly):

    type_assembly = "INSERT"
    placement_type = "EXTERIOR"
    id_prompt = "sn_closets.counter_top"
    show_in_library = True
    category_name = "Closet Products - Basic"

    def update(self):
        self.obj_x.location.x = self.width
        self.obj_y.location.y = -self.depth

        self.obj_bp["IS_BP_COUNTERTOP"] = True
        self.obj_bp["ID_PROMPT"] = self.id_prompt
        self.obj_y['IS_MIRROR'] = True
        self.obj_bp.snap.type_group = self.type_assembly
        super().update()

    def draw(self):
        self.create_assembly()
        # we are adding a master hide for everything
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()
        self.obj_bp.snap.export_as_subassembly = True

        props = self.obj_bp.sn_closets
        props.is_counter_top_insert_bp = True

        self.add_prompt("Add Left Corner", 'CHECKBOX', False)
        self.add_prompt("Add Right Corner", 'CHECKBOX', False)
        self.add_prompt("Left Corner Width", 'DISTANCE', sn_unit.inch(24))
        self.add_prompt("Right Corner Width", 'DISTANCE', sn_unit.inch(24))
        self.add_prompt("Left Corner Depth", 'DISTANCE', sn_unit.inch(24))
        self.add_prompt("Right Corner Depth", 'DISTANCE', sn_unit.inch(24))
        self.add_prompt("Left Depth", 'DISTANCE', sn_unit.inch(12))
        self.add_prompt("Right Depth", 'DISTANCE', sn_unit.inch(12))
        self.add_prompt("Add Backsplash", 'CHECKBOX', False)
        self.add_prompt("Backsplash Height", 'DISTANCE', sn_unit.inch(4))
        self.add_prompt("Backsplash Thickness", 'DISTANCE', sn_unit.inch(0.75))
        self.add_prompt("Melamine Thickness", 'DISTANCE', sn_unit.inch(0.75))
        self.add_prompt("Extend To Left Panel", 'CHECKBOX', True)
        self.add_prompt("Extend To Right Panel", 'CHECKBOX', True)
        self.add_prompt("Extend Left Amount", 'DISTANCE', sn_unit.inch(0))
        self.add_prompt("Extend Right Amount", 'DISTANCE', sn_unit.inch(0))
        self.add_prompt("Exposed Left", 'CHECKBOX', False)
        self.add_prompt("Exposed Right", 'CHECKBOX', False)
        self.add_prompt("Exposed Back", 'CHECKBOX', False)
        self.add_prompt("Corner Shape", 'COMBOBOX', 0, ['Diagonal', 'L Shape'])
        common_prompts.add_countertop_prompts(self)

        Product_Width = self.obj_x.snap.get_var('location.x', 'Product_Width')
        Product_Depth = self.obj_y.snap.get_var('location.y', 'Product_Depth')
        Edge_Type = self.get_prompt('Edge Type').get_var()
        Deck_Thickness = self.get_prompt('Deck Thickness').get_var()
        Deck_Overhang = self.get_prompt('Deck Overhang').get_var()
        Countertop_Type = self.get_prompt('Countertop Type').get_var()
        Add_Left_Corner = self.get_prompt('Add Left Corner').get_var()
        Add_Right_Corner = self.get_prompt('Add Right Corner').get_var()
        Left_Corner_Width = self.get_prompt('Left Corner Width').get_var()
        Right_Corner_Width = self.get_prompt('Right Corner Width').get_var()
        Left_Corner_Depth = self.get_prompt('Left Corner Depth').get_var()
        Right_Corner_Depth = self.get_prompt('Right Corner Depth').get_var()
        Left_Depth = self.get_prompt('Left Depth').get_var()
        Right_Depth = self.get_prompt('Right Depth').get_var()
        Corner_Shape = self.get_prompt('Corner Shape').get_var()
        Add_Backsplash = self.get_prompt('Add Backsplash').get_var()
        B_Splash_Height = self.get_prompt('Backsplash Height').get_var('B_Splash_Height')
        B_Splash_Thickness = self.get_prompt('Backsplash Thickness').get_var('B_Splash_Thickness')
        Melamine_Thickness = self.get_prompt('Melamine Thickness').get_var()
        Extend_Left = self.get_prompt('Extend To Left Panel').get_var('Extend_Left')
        Extend_Right = self.get_prompt('Extend To Right Panel').get_var('Extend_Right')
        Extend_Left_Amount = self.get_prompt('Extend Left Amount').get_var()
        Extend_Right_Amount = self.get_prompt('Extend Right Amount').get_var()
        Exposed_Left = self.get_prompt('Exposed Left').get_var()
        Exposed_Right = self.get_prompt('Exposed Right').get_var()
        Exposed_Back = self.get_prompt('Exposed Back').get_var()

        self.dim_z('Deck_Thickness', [Deck_Thickness])

        melamine_deck = common_parts.add_cc_countertop(self)        
        melamine_deck.set_name("Melamine Countertop")
        melamine_deck.loc_x('IF(Add_Left_Corner,0,IF(Extend_Left,0,Deck_Thickness/2)-Extend_Left_Amount)',[Extend_Left,Extend_Left_Amount,Deck_Thickness,Add_Left_Corner])
        melamine_deck.loc_y('Product_Depth',[Product_Depth])
        melamine_deck.dim_x('Product_Width-IF(Extend_Left,0,Deck_Thickness/2)-IF(Extend_Right,0,Deck_Thickness/2)+IF(Add_Left_Corner,0,Extend_Left_Amount)+IF(Add_Right_Corner,0,Extend_Right_Amount)',
                  [Product_Width,Extend_Left,Extend_Right,Deck_Thickness,Extend_Right_Amount,Extend_Left_Amount,Add_Left_Corner,Add_Right_Corner])
        melamine_deck.dim_y("-Product_Depth-Deck_Overhang",[Product_Depth,Deck_Overhang])
        melamine_deck.dim_z("Melamine_Thickness",[Melamine_Thickness])
        melamine_deck.get_prompt("Hide").set_formula("IF(Countertop_Type==0,False,True) or Hide",[Countertop_Type,self.hide_var])
        melamine_deck.get_prompt('Exposed Left').set_formula('Exposed_Left',[Exposed_Left])
        melamine_deck.get_prompt('Exposed Right').set_formula('Exposed_Right',[Exposed_Right])
        melamine_deck.get_prompt('Exposed Back').set_formula('Exposed_Back',[Exposed_Back])

        granite_ctop = common_parts.add_granite_countertop(self)
        granite_ctop.set_name("Granite Countertop")
        granite_ctop.loc_x('IF(Add_Left_Corner,0,IF(Extend_Left,0,Deck_Thickness/2)-Extend_Left_Amount)',[Extend_Left,Extend_Left_Amount,Deck_Thickness,Add_Left_Corner])
        granite_ctop.loc_y('Product_Depth',[Product_Depth])
        granite_ctop.dim_x('Product_Width-IF(Extend_Left,0,Deck_Thickness/2)-IF(Extend_Right,0,Deck_Thickness/2)+IF(Add_Left_Corner,0,Extend_Left_Amount)+IF(Add_Right_Corner,0,Extend_Right_Amount)',
                  [Product_Width,Extend_Left,Extend_Right,Deck_Thickness,Extend_Right_Amount,Extend_Left_Amount,Add_Left_Corner,Add_Right_Corner])
        granite_ctop.dim_y("-Product_Depth-Deck_Overhang",[Product_Depth,Deck_Overhang])
        granite_ctop.dim_z('Deck_Thickness',[Deck_Thickness])
        granite_ctop.get_prompt("Hide").set_formula("IF(Countertop_Type==2,False,True) or Hide",[Countertop_Type,self.hide_var])
        granite_ctop.get_prompt('Edge Type').set_formula('Edge_Type',[Edge_Type])

        hpltop = common_parts.add_hpl_top(self)    
        hpltop.set_name("HPL Countertop")
        hpltop.loc_x('IF(Add_Left_Corner,0,IF(Extend_Left,0,Deck_Thickness/2)-Extend_Left_Amount)',[Extend_Left,Extend_Left_Amount,Deck_Thickness,Add_Left_Corner])
        hpltop.loc_y('Product_Depth',[Product_Depth])
        hpltop.dim_x('Product_Width-IF(Extend_Left,0,Deck_Thickness/2)-IF(Extend_Right,0,Deck_Thickness/2)+IF(Add_Left_Corner,0,Extend_Left_Amount)+IF(Add_Right_Corner,0,Extend_Right_Amount)',
                  [Product_Width,Extend_Left,Extend_Right,Deck_Thickness,Extend_Right_Amount,Extend_Left_Amount,Add_Left_Corner,Add_Right_Corner])
        hpltop.dim_y("-Product_Depth-Deck_Overhang",[Product_Depth,Deck_Overhang])
        hpltop.dim_z('Deck_Thickness',[Deck_Thickness])
        hpltop.get_prompt("Hide").set_formula("IF(Countertop_Type==1,False,True) or Hide",[Countertop_Type,self.hide_var])

        b_splash = common_parts.add_back_splash(self)
        b_splash.set_name("Countertop Backsplash")

        b_splash.loc_x('IF(Add_Left_Corner,-Left_Corner_Width,0)-Extend_Left_Amount',[Add_Left_Corner,Left_Corner_Width,Extend_Left_Amount])
        b_splash.loc_y('Product_Depth',[Product_Depth])
        b_splash.loc_z('IF(Countertop_Type==0,INCH(0.75),INCH(1.5))', [Countertop_Type])
        b_splash.rot_x(value=math.radians(90))

        b_splash.dim_x(
            "Product_Width+IF(Add_Left_Corner,Left_Corner_Width,0)+IF(Add_Right_Corner,Right_Corner_Width,0)+Extend_Right_Amount+Extend_Left_Amount",
            [Product_Width,Add_Left_Corner,Left_Corner_Width,Add_Right_Corner,Right_Corner_Width,Extend_Right_Amount,Extend_Left_Amount]
        )

        b_splash.dim_y("B_Splash_Height",[B_Splash_Height])
        b_splash.dim_z("B_Splash_Thickness",[B_Splash_Thickness])
        b_splash.get_prompt("Hide").set_formula("IF(Add_Backsplash,False,True) or Hide",[Add_Backsplash,self.hide_var])       

        l_corner_ctop = common_parts.add_cc_corner_countertop(self)      
        l_corner_ctop.set_name("Countertop")
        l_corner_ctop.loc_x('-Left_Corner_Width',[Left_Corner_Width])
        l_corner_ctop.loc_y('Product_Depth',[Product_Depth])
        l_corner_ctop.dim_x("Left_Corner_Width",[Left_Corner_Width])
        l_corner_ctop.dim_y("-Left_Corner_Depth",[Left_Corner_Depth])
        l_corner_ctop.dim_z('IF(Countertop_Type == 0,Melamine_Thickness,Deck_Thickness)',[Deck_Thickness,Melamine_Thickness,Countertop_Type])
        l_corner_ctop.get_prompt("Hide").set_formula("IF(Add_Left_Corner,False,True) or Hide",[Add_Left_Corner,self.hide_var])       
        l_corner_ctop.get_prompt('Edge Type').set_formula('IF(Countertop_Type==2,Edge_Type,1)',[Edge_Type,Countertop_Type])
        l_corner_ctop.get_prompt('Right Depth').set_formula('Product_Depth+Deck_Overhang',[Product_Depth,Deck_Overhang])
        l_corner_ctop.get_prompt('Left Depth').set_formula('Left_Depth',[Left_Depth])
        l_corner_ctop.get_prompt('Corner Shape').set_formula('Corner_Shape',[Corner_Shape])

        left_b_splash = common_parts.add_back_splash(self)
        left_b_splash.set_name("Left Countertop Backsplash")
        left_b_splash.loc_x('-Left_Corner_Width',[Left_Corner_Width])
        left_b_splash.loc_y('Product_Depth-B_Splash_Thickness',[Product_Depth,B_Splash_Thickness])
        left_b_splash.loc_z('IF(Countertop_Type==0,INCH(0.75),INCH(1.5))', [Countertop_Type])
        left_b_splash.rot_x(value=math.radians(90))
        left_b_splash.rot_z(value=math.radians(90))
        left_b_splash.dim_x("-Left_Corner_Depth+B_Splash_Thickness",[Left_Corner_Depth,B_Splash_Thickness])
        left_b_splash.dim_y("B_Splash_Height",[B_Splash_Height])
        left_b_splash.dim_z("B_Splash_Thickness",[B_Splash_Thickness]) 
        left_b_splash.get_prompt("Hide").set_formula("IF(AND(Add_Left_Corner,Add_Backsplash),False,True) or Hide",[Add_Left_Corner,Add_Backsplash,self.hide_var])       

        r_corner_ctop = common_parts.add_cc_corner_countertop(self)
        r_corner_ctop.set_name("Countertop")
        r_corner_ctop.loc_x('Product_Width+Right_Corner_Width',[Product_Width,Right_Corner_Width])
        r_corner_ctop.loc_y('Product_Depth',[Product_Depth])
        r_corner_ctop.rot_z(value=math.radians(-90))
        r_corner_ctop.dim_x("Right_Corner_Depth",[Right_Corner_Depth])
        r_corner_ctop.dim_y("-Right_Corner_Width",[Right_Corner_Width])
        r_corner_ctop.dim_z('IF(Countertop_Type == 0,Melamine_Thickness,Deck_Thickness)',[Deck_Thickness,Melamine_Thickness,Countertop_Type])
        r_corner_ctop.get_prompt("Hide").set_formula("IF(Add_Right_Corner,False,True) or Hide",[Add_Right_Corner,self.hide_var])
        r_corner_ctop.get_prompt('Edge Type').set_formula('IF(Countertop_Type==2,Edge_Type,1)',[Edge_Type,Countertop_Type])
        r_corner_ctop.get_prompt('Left Depth').set_formula('Product_Depth+Deck_Overhang',[Product_Depth,Deck_Overhang])
        r_corner_ctop.get_prompt('Right Depth').set_formula('Right_Depth',[Right_Depth])
        r_corner_ctop.get_prompt('Corner Shape').set_formula('Corner_Shape',[Corner_Shape])

        right_b_splash = common_parts.add_back_splash(self)
        right_b_splash.set_name("Right Countertop Backsplash")
        right_b_splash.loc_x('Product_Width+Right_Corner_Width',[Product_Width,Right_Corner_Width])
        right_b_splash.loc_y('Product_Depth-B_Splash_Thickness',[Product_Depth,B_Splash_Thickness])
        right_b_splash.loc_z('IF(Countertop_Type==0,INCH(0.75),INCH(1.5))', [Countertop_Type])
        right_b_splash.rot_x(value=math.radians(90))
        right_b_splash.rot_z(value=math.radians(-90))
        right_b_splash.dim_x("Right_Corner_Depth-B_Splash_Thickness",[Right_Corner_Depth,B_Splash_Thickness])
        right_b_splash.dim_y("B_Splash_Height",[B_Splash_Height])
        right_b_splash.dim_z("B_Splash_Thickness",[B_Splash_Thickness]) 
        right_b_splash.get_prompt("Hide").set_formula("IF(AND(Add_Right_Corner,Add_Backsplash),False,True) or Hide",[Add_Right_Corner,Add_Backsplash,self.hide_var])         

        self.update()
        
class PROMPTS_Counter_Top(sn_types.Prompts_Interface):
    bl_idname = "sn_closets.counter_top"
    bl_label = "Countertop Prompt" 
    bl_description = "This shows all of the available Countertop options"
    bl_options = {'UNDO'}
    
    object_name: StringProperty(name="Object Name")

    countertop_type: EnumProperty(
        name="Countertop Type",
        items=[
            ('0', 'Melamine', 'Melamine'),
            ('1', 'HPL', 'HPL'),
            ('2', 'Granite', 'Granite')],
        default='0')

    edge_type: EnumProperty(
        name="Countertop Edge Type",
        items=[
            ('0', 'Waterfall', 'Waterfall'),
            ('1', 'Flat Front', 'Flat Front'),
            ('2', '180 Degree', '180 Degree'),
            ('3', 'Alder Miter', 'Alder Miter')],
        default='0')

    assembly = None
    countertop_type_prompt = None
    edge_type_prompt = None
        
    def check(self, context):
        Add_Left_Corner = self.assembly.get_prompt("Add Left Corner")
        Add_Right_Corner = self.assembly.get_prompt("Add Right Corner")
        extend_left_amount = self.assembly.get_prompt("Extend Left Amount")
        extend_right_amount = self.assembly.get_prompt("Extend Right Amount")
        prompts = [Add_Left_Corner,Add_Right_Corner,extend_left_amount,extend_right_amount]

        if self.countertop_type_prompt:
            self.countertop_type_prompt.set_value(int(self.countertop_type))
        if self.edge_type_prompt:
            self.edge_type_prompt.set_value(int(self.edge_type))
        
        if all(prompts):
            if(Add_Left_Corner.get_value()):
                extend_left_amount.set_value(sn_unit.inch(0)) 
            if(Add_Right_Corner.get_value()):   
                extend_right_amount.set_value(sn_unit.inch(0))
        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport
        closet_props.update_render_materials(self, context)   
        return True
        
    def execute(self, context):
        return {'FINISHED'}
        
    def invoke(self,context,event):
        self.assembly = self.get_insert()
        self.countertop_type_prompt = self.assembly.get_prompt("Countertop Type")
        self.edge_type_prompt = self.assembly.get_prompt("Edge Type")
        self.countertop_type = str(self.countertop_type_prompt.combobox_index)
        self.edge_type = str(self.edge_type_prompt.combobox_index)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=sn_utils.get_prop_dialog_width(475))          
        
    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                Countertop_Type = self.assembly.get_prompt("Countertop Type")
                Countertop_Thickness = self.assembly.get_prompt("Countertop Thickness")
                Edge_Type = self.assembly.get_prompt("Edge Type")
                HPL_Material_Name = self.assembly.get_prompt("HPL Material Name")
                HPL_Material_Number = self.assembly.get_prompt("HPL Material Number")
                Deck_Overhang = self.assembly.get_prompt("Deck Overhang")  
                Add_Left_Corner = self.assembly.get_prompt("Add Left Corner")
                Add_Right_Corner = self.assembly.get_prompt("Add Right Corner")
                Corner_Shape = self.assembly.get_prompt("Corner Shape")
                Add_Backsplash = self.assembly.get_prompt('Add Backsplash')
                B_Splash_Height = self.assembly.get_prompt('Backsplash Height')
                B_Splash_Thickness = self.assembly.get_prompt('Backsplash Thickness') 
                extend_left_amount = self.assembly.get_prompt("Extend Left Amount")
                extend_right_amount = self.assembly.get_prompt("Extend Right Amount")
                exposed_left = self.assembly.get_prompt("Exposed Left")
                exposed_right = self.assembly.get_prompt("Exposed Right")      
                exposed_back = self.assembly.get_prompt("Exposed Back")            
                
                box = layout.box()   
                row = box.row()

                if Deck_Overhang:
                    row = box.row()
                    row.prop(Deck_Overhang, "distance_value", text="Front Overhang:")

                if extend_left_amount and Add_Left_Corner.get_value() == False:                        
                    row = box.row()
                    row.prop(extend_left_amount, "distance_value", text="Left Overhang:")

                if extend_right_amount and Add_Right_Corner.get_value() == False:    
                    row = box.row()
                    row.prop(extend_right_amount, "distance_value", text="Right Overhang:")

                row = box.row()
                row.label(text="Exposed Ends:")
                row.prop(exposed_left, "checkbox_value", text="Left")
                row.prop(exposed_right, "checkbox_value", text="Right")      
                row.prop(exposed_back, "checkbox_value", text="Back")
           
                row = box.row()
                row.label(text="Countertop Height:")
                row.prop(self.assembly.obj_bp,'location',index=2,text="")

                row = box.row()
                row.prop(Add_Backsplash, "checkbox_value", text=Add_Backsplash.name)

                if Add_Backsplash.get_value():
                    row = box.row()
                    row.prop(B_Splash_Height, "distance_value", text=B_Splash_Height.name)
                    row = box.row()
                    row.prop(B_Splash_Thickness, "distance_value", text=B_Splash_Thickness.name)
                
                row = box.row()
                row.label(text="Add Corner:")
                row.prop(Add_Left_Corner, "checkbox_value", text=Add_Left_Corner.name)
                row.prop(Add_Right_Corner, "checkbox_value", text=Add_Right_Corner.name)
                
                if Add_Left_Corner.get_value():
                    Left_Corner_Width = self.assembly.get_prompt("Left Corner Width")
                    Left_Corner_Depth = self.assembly.get_prompt("Left Corner Depth")
                    Left_Depth = self.assembly.get_prompt("Left Depth")
                    row = box.row()
                    row.label(text="Left Corner Size:")
                    row = box.row(align=True)
                    row.prop(Left_Corner_Width, "distance_value", text=Left_Corner_Width.name)
                    row.prop(Left_Corner_Depth, "distance_value", text=Left_Corner_Depth.name)
                    row.prop(Left_Depth, "distance_value", text=Left_Depth.name)
                
                if Add_Right_Corner.get_value():
                    Right_Corner_Width = self.assembly.get_prompt("Right Corner Width")
                    Right_Corner_Depth = self.assembly.get_prompt("Right Corner Depth")
                    Right_Depth = self.assembly.get_prompt("Right Depth")
                    row = box.row()
                    row.label(text="Right Corner Size:")
                    row = box.row(align=True)
                    row.prop(Right_Corner_Width, "distance_value", text=Right_Corner_Width.name)
                    row.prop(Right_Corner_Depth, "distance_value", text=Right_Corner_Depth.name)
                    row.prop(Right_Depth, "distance_value", text=Right_Depth.name)

                if Add_Left_Corner.get_value() or Add_Right_Corner.get_value():
                    row = box.row()
                    row.prop(Corner_Shape, "combobox_index", text=Corner_Shape.name)

                if Countertop_Type:
                    row = box.row()
                    row.label(text=Countertop_Type.name)
                    row.prop(self, "countertop_type", expand=True)

                    if self.countertop_type == '2':
                        if Edge_Type:
                            row = box.row()
                            row.label(text=Edge_Type.name)
                            row.prop(self, "edge_type", expand=True)
                        pass

class OPERATOR_Place_Countertop(Operator, PlaceClosetInsert):
    bl_idname = "sn_closets.place_countertop"
    bl_label = "Place Countertop"
    bl_description = "This allows you to place a countertop."
    bl_options = {'UNDO'}
    
    show_openings = False
    assembly = None
    selected_obj = None
    selected_point = None    

    def execute(self, context):
        self.assembly = self.asset
        return super().execute(context)

    def ctop_drop(self, context, event):
        if self.selected_obj:
            sel_product_bp = sn_utils.get_closet_bp(self.selected_obj)
            sel_assembly_bp = sn_utils.get_assembly_bp(self.selected_obj)

            if sel_product_bp and sel_assembly_bp:
                product = sn_types.Assembly(sel_product_bp)
                props = product.obj_bp.sn_closets
                if product and 'IS_BP_CLOSET' in product.obj_bp:
                    heights = []
                    depths = []
                    for i in range(1,10):
                        height = product.get_prompt("Opening " + str(i) + " Height")
                        if height: 
                            heights.append(height.get_value())
                        depth = product.get_prompt("Opening " + str(i) + " Depth")
                        if depth: 
                            depths.append(depth.get_value())
                            
                    scene_props = bpy.context.scene.sn_closets
                    
                    tk_height = product.get_prompt("Toe Kick Height")
                    placement_height = 0
                    if scene_props.closet_defaults.use_plant_on_top:
                        placement_height = max(heights) + sn_unit.millimeter(16)
                    else:
                        placement_height = max(heights)                   
                    
                    if tk_height:
                        placement_height += tk_height.get_value()

                    self.assembly.obj_bp.parent = product.obj_bp
                    self.assembly.obj_bp.location.z = placement_height             
                    self.assembly.obj_bp.location.y = -max(depths)
                    self.assembly.obj_x.location.x = product.obj_x.location.x
                    self.assembly.obj_y.location.y = max(depths)

                if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                    carcass_bp = sn_utils.get_closet_bp(self.assembly.obj_bp)
                    for child in carcass_bp.children:
                        if "IS_BP_DRAWER_STACK" in child or "IS_BP_HAMPER" in child:
                            child_assembly = sn_types.Assembly(child)
                            cleat_location = child_assembly.get_prompt("Cleat Location")
                            if cleat_location:
                                cleat_location.set_value(1)  # Setting Cleat Location to Below

                    sn_utils.set_wireframe(self.assembly.obj_bp, False)
                    bpy.context.window.cursor_set('DEFAULT')
                    bpy.ops.object.select_all(action='DESELECT')
                    context.view_layer.objects.active = self.assembly.obj_bp
                    self.assembly.obj_bp.select_set(True)
                    closet_props.update_render_materials(self, context) 
                    return self.finish(context)
                    # return {'FINISHED'}

        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        context.area.tag_redraw()
        bpy.ops.object.select_all(action='DESELECT')        
        self.selected_point, self.selected_obj, _ = sn_utils.get_selection_point(context,event)
        
        if self.event_is_cancel_command(event):
            context.area.header_text_set(None)
            return self.cancel_drop(context)
        
        if event.type in {'ESC'}:
            self.cancel_drop(context, event)
            return {'FINISHED'}
        
        return self.ctop_drop(context, event)    
        
bpy.utils.register_class(PROMPTS_Counter_Top)
bpy.utils.register_class(OPERATOR_Place_Countertop)
