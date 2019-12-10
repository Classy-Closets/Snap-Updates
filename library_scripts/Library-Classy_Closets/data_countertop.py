import bpy
from os import path
from mv import fd_types, unit, utils
from . import mv_closet_defaults as props_closet
from . import common_parts
from . import common_prompts

ASSEMBLY_DIR = path.join(common_parts.LIBRARY_DATA_DIR,"Closet Assemblies")
CTOP_ASSEMBLY_DIR = path.join(ASSEMBLY_DIR,"CC Countertops")
STRAIGHT_CTOP =  path.join(CTOP_ASSEMBLY_DIR,"Straight Countertop.blend")
CORNER_CTOP =  path.join(CTOP_ASSEMBLY_DIR,"Corner Countertop.blend")
STRAIGHT_COUNTER_TOP = path.join(ASSEMBLY_DIR,"Countertop.blend")
PART_WITH_EDGEBANDING = path.join(ASSEMBLY_DIR,"Part with Edgebanding.blend")

class Countertop_Insert(fd_types.Assembly):

    placement_type = "EXTERIOR"
    type_assembly = "INSERT"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".counter_top"
    
    def draw(self):
        self.create_assembly()
        self.obj_bp.mv.export_as_subassembly = True
        
        props = props_closet.get_object_props(self.obj_bp)
        props.is_counter_top_insert_bp = True
        
        self.add_tab(name='Countertop Options',tab_type='VISIBLE')
        self.add_prompt(name="Exposed Left",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Exposed Right",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Exposed Back",prompt_type='CHECKBOX',value=False,tab_index=1)
                
        self.add_prompt(name="Add Left Corner",prompt_type='CHECKBOX',value=False,tab_index=1)
        self.add_prompt(name="Add Right Corner",prompt_type='CHECKBOX',value=False,tab_index=1)             
        self.add_prompt(name="Left Corner Width",prompt_type='DISTANCE',value=unit.inch(24),tab_index=1)  
        self.add_prompt(name="Right Corner Width",prompt_type='DISTANCE',value=unit.inch(24),tab_index=1)  
        self.add_prompt(name="Left Corner Depth",prompt_type='DISTANCE',value=unit.inch(24),tab_index=1)  
        self.add_prompt(name="Right Corner Depth",prompt_type='DISTANCE',value=unit.inch(24),tab_index=1)  
        self.add_prompt(name="Left Depth",prompt_type='DISTANCE',value=unit.inch(12),tab_index=1)  
        self.add_prompt(name="Right Depth",prompt_type='DISTANCE',value=unit.inch(12),tab_index=1)  
                
        self.add_prompt(name="Corner Shape",
                        prompt_type='COMBOBOX',
                        value=0,
                        tab_index=1,
                        items=['Diagonal',
                               'L Shape'],
                        columns=2)        
        
        common_prompts.add_countertop_prompts(self)
        
        Product_Width = self.get_var('dim_x','Product_Width')
        Product_Depth = self.get_var('dim_y','Product_Depth')
        Edge_Type = self.get_var('Edge Type')
        Deck_Thickness = self.get_var('Deck Thickness')
        Deck_Overhang = self.get_var('Deck Overhang')
        Countertop_Type = self.get_var('Countertop Type')
        Exposed_Left = self.get_var('Exposed Left')
        Exposed_Right = self.get_var('Exposed Right')
        Exposed_Back = self.get_var('Exposed Back')                              
        Add_Left_Corner = self.get_var('Add Left Corner')  
        Add_Right_Corner = self.get_var('Add Right Corner')
        Left_Corner_Width = self.get_var('Left Corner Width')  
        Right_Corner_Width = self.get_var('Right Corner Width')
        Left_Corner_Depth = self.get_var('Left Corner Depth')  
        Right_Corner_Depth = self.get_var('Right Corner Depth')
        Left_Depth = self.get_var('Left Depth')  
        Right_Depth = self.get_var('Right Depth')      
        Edge_Type = self.get_var('Edge Type')
        Corner_Shape = self.get_var('Corner Shape')
        
        self.z_dim('Deck_Thickness',[Deck_Thickness])

        ctop = common_parts.add_cc_countertop(self)
        props = props_closet.get_object_props(ctop.obj_bp)
        props.is_countertop_bp = True        
        ctop.set_name("Countertop Deck")
        ctop.x_loc(value = 0)
        ctop.y_loc('Product_Depth',[Product_Depth])
        ctop.z_loc(value = 0)
        ctop.x_rot(value = 0)
        ctop.y_rot(value = 0)
        ctop.z_rot(value = 0)
        ctop.x_dim("Product_Width",[Product_Width])
        ctop.y_dim("-Product_Depth-Deck_Overhang",[Product_Depth,Deck_Overhang])
        ctop.z_dim("Deck_Thickness",[Deck_Thickness])
        ctop.prompt('Edge Type','Edge_Type',[Edge_Type])

        #ctop.prompt("Hide","IF(Countertop_Type==0,False,True)",[Countertop_Type])
#         ctop.prompt('Exposed Left','Exposed_Left',[Exposed_Left])
#         ctop.prompt('Exposed Right','Exposed_Right',[Exposed_Right])
#         ctop.prompt('Exposed Back','Exposed_Back',[Exposed_Back])
                
        l_corner_ctop = common_parts.add_cc_corner_countertop(self)
        props = props_closet.get_object_props(l_corner_ctop.obj_bp)
        props.is_countertop_bp = True        
        l_corner_ctop.set_name("Countertop Deck")
        l_corner_ctop.x_loc('-Left_Corner_Width',[Left_Corner_Width])
        l_corner_ctop.y_loc('Product_Depth',[Product_Depth])
        l_corner_ctop.z_loc(value = 0)
        l_corner_ctop.x_rot(value = 0)
        l_corner_ctop.y_rot(value = 0)
        l_corner_ctop.z_rot(value = 0)
        l_corner_ctop.x_dim("Left_Corner_Width",[Left_Corner_Width])
        l_corner_ctop.y_dim("-Left_Corner_Depth",[Left_Corner_Depth])
        l_corner_ctop.z_dim("Deck_Thickness",[Deck_Thickness])
        l_corner_ctop.prompt("Hide","IF(Add_Left_Corner,False,True)",[Add_Left_Corner])       
        l_corner_ctop.prompt('Edge Type','Edge_Type',[Edge_Type])
        l_corner_ctop.prompt('Right Depth','Product_Depth+Deck_Overhang',[Product_Depth,Deck_Overhang])
        l_corner_ctop.prompt('Left Depth','Left_Depth',[Left_Depth])
        l_corner_ctop.prompt('Corner Shape','Corner_Shape',[Corner_Shape])
                      
        r_corner_ctop = common_parts.add_cc_corner_countertop(self)
        props = props_closet.get_object_props(r_corner_ctop.obj_bp)
        props.is_countertop_bp = True        
        r_corner_ctop.set_name("Countertop Deck")
        r_corner_ctop.x_loc('Product_Width+Right_Corner_Width',[Product_Width,Right_Corner_Width])
        r_corner_ctop.y_loc('Product_Depth',[Product_Depth])
        r_corner_ctop.z_loc(value = 0)
        r_corner_ctop.x_rot(value = 0)
        r_corner_ctop.y_rot(value = 0)
        r_corner_ctop.z_rot(value = -90)
        r_corner_ctop.x_dim("Right_Corner_Depth",[Right_Corner_Depth])
        r_corner_ctop.y_dim("-Right_Corner_Width",[Right_Corner_Width])
        r_corner_ctop.z_dim("Deck_Thickness",[Deck_Thickness])
        r_corner_ctop.prompt("Hide","IF(Add_Right_Corner,False,True)",[Add_Right_Corner])
        r_corner_ctop.prompt('Edge Type','Edge_Type',[Edge_Type])
        r_corner_ctop.prompt('Left Depth','Product_Depth+Deck_Overhang',[Product_Depth,Deck_Overhang])
        r_corner_ctop.prompt('Right Depth','Right_Depth',[Right_Depth])
        r_corner_ctop.prompt('Corner Shape','Corner_Shape',[Corner_Shape])
        
#         hpltop = common_parts.add_hpl_top(self)
#         props = props_closet.get_object_props(hpltop.obj_bp)     
#         hpltop.set_name("HPL Deck")
#         hpltop.x_loc(value = 0)
#         hpltop.y_loc('Product_Depth',[Product_Depth])
#         hpltop.z_loc(value = 0)
#         hpltop.x_rot(value = 0)
#         hpltop.y_rot(value = 0)
#         hpltop.z_rot(value = 0)
#         hpltop.x_dim("Product_Width",[Product_Width])
#         hpltop.y_dim("-Product_Depth-Deck_Overhang",[Product_Depth,Deck_Overhang])
#         hpltop.z_dim("Deck_Thickness",[Deck_Thickness])
#         hpltop.prompt("Hide","IF(Countertop_Type==1,False,True)",[Countertop_Type])
#         hpltop.prompt('Exposed Left','Exposed_Left',[Exposed_Left])
#         hpltop.prompt('Exposed Right','Exposed_Right',[Exposed_Right])
#         hpltop.prompt('Exposed Back','Exposed_Back',[Exposed_Back])                
#                 
#         granite_deck = common_parts.add_countertop(self)
#         granite_deck.set_name("Granite Deck")
#         granite_deck.x_loc(value = 0)
#         granite_deck.y_loc('Product_Depth',[Product_Depth])
#         granite_deck.z_loc(value = 0)
#         granite_deck.x_rot(value = 0)
#         granite_deck.y_rot(value = 0)
#         granite_deck.z_rot(value = 0)
#         granite_deck.x_dim("Product_Width",[Product_Width])
#         granite_deck.y_dim("-Product_Depth-Deck_Overhang",[Product_Depth,Deck_Overhang])
#         granite_deck.z_dim("Deck_Thickness",[Deck_Thickness])
#         granite_deck.prompt("Edge Type","Edge_Type",[Edge_Type])
#         granite_deck.prompt("Hide","IF(Countertop_Type==2,False,True)",[Countertop_Type])
# 
#         granite_deck = common_parts.add_countertop(self)
#         granite_deck.set_name("Granite Deck")
#         granite_deck.x_loc(value = 0)
#         granite_deck.y_loc('Product_Depth',[Product_Depth])
#         granite_deck.z_loc(value = 0)
#         granite_deck.x_rot(value = 0)
#         granite_deck.y_rot(value = 0)
#         granite_deck.z_rot(value = 0)
#         granite_deck.x_dim("Product_Width",[Product_Width])
#         granite_deck.y_dim("-Product_Depth-Deck_Overhang",[Product_Depth,Deck_Overhang])
#         granite_deck.z_dim("Deck_Thickness",[Deck_Thickness])
#         granite_deck.prompt("Edge Type","Edge_Type",[Edge_Type])
#         granite_deck.prompt("Hide","IF(Countertop_Type==2,False,True)",[Countertop_Type])

        self.update()
        
class PROMPTS_Counter_Top(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".counter_top"
    bl_label = "Counter Top Prompts" 
    bl_description = "This shows all of the available counter top options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")

    assembly = None
    
    @classmethod
    def poll(cls, context):
        return True
        
    def assign_material(self,obj):
        
        if obj.type == 'CUTPART':
            for slot in obj.cabinetlib.material_slots:
                Countertop_Type = self.assembly.get_prompt("Countertop Type")
                
                if Countertop_Type.value() == 'Melamine':
                    if slot.name in {'Core','Exterior','Interior'}:
                        slot.pointer_name = "Closet_Part_Surfaces"
                        
                    if slot.name == 'LeftEdge':
                        Exposed_Left = self.assembly.get_prompt("Exposed Left")
                        if Exposed_Left.value():
                            slot.pointer_name = "Closet_Part_Edges_Secondary"
                        else:
                            slot.pointer_name = "Core"
                    if slot.name == 'RightEdge':
                        Exposed_Right = self.assembly.get_prompt("Exposed Right")
                        if Exposed_Right.value():
                            slot.pointer_name = "Closet_Part_Edges_Secondary"
                        else:
                            slot.pointer_name = "Core"                            
                    if slot.name == 'BackEdge':
                        Exposed_Back = self.assembly.get_prompt("Exposed Back")
                        if Exposed_Back.value():
                            slot.pointer_name = "Closet_Part_Edges_Secondary"
                        else:
                            slot.pointer_name = "Core"     
                                                   
                    if slot.name == 'Edgebanding':
                        slot.pointer_name = "Closet_Part_Edges"

                if Countertop_Type.value() == 'HPL':
                    slot.pointer_name = "Countertop_Surface"
                    
                if Countertop_Type.value() == 'Granite':
                    slot.pointer_name = "Countertop_Surface"    

                
        for child in obj.children:
            self.assign_material(child)
        
    def check(self, context):
        #self.assign_material(self.assembly.obj_bp)
        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport
        return True
        
    def execute(self, context):
        return {'FINISHED'}
        
    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj,'INSERT')
        self.assembly = fd_types.Assembly(obj_insert_bp)
        
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(330))          
        
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
                Exposed_Left = self.assembly.get_prompt("Exposed Left")
                Exposed_Right = self.assembly.get_prompt("Exposed Right")
                Exposed_Back = self.assembly.get_prompt("Exposed Back")
                
                Add_Left_Corner = self.assembly.get_prompt("Add Left Corner")
                Add_Right_Corner = self.assembly.get_prompt("Add Right Corner")
                Corner_Shape = self.assembly.get_prompt("Corner Shape")
                
                box = layout.box()   
                row = box.row()
                row.label("Countertop Width:")
                row.prop(self.assembly.obj_x,'location',index=0,text="")
                
                if Deck_Overhang:
                    row = box.row()
                    Deck_Overhang.draw_prompt(row,text="Front Overhang:")
                           
                row = box.row()
                row.label("Horizontal Location:")
                row.prop(self.assembly.obj_bp,'location',index=0,text="")
                
                row = box.row()
                row.label("Countertop Height:")
                row.prop(self.assembly.obj_bp,'location',index=2,text="")  
                
                if Countertop_Type.value() != 'Melamine':
                    row = box.row()
                    Edge_Type.draw_prompt(row)
                
                row = box.row()
                Corner_Shape.draw_prompt(row)
                
                row = box.row()
                row.label("Add Corner:")
                Add_Left_Corner.draw_prompt(row,text="Left",split_text=False)
                Add_Right_Corner.draw_prompt(row,text="Right",split_text=False)
                
                if Add_Left_Corner.value():
                    Left_Corner_Width = self.assembly.get_prompt("Left Corner Width")
                    Left_Corner_Depth = self.assembly.get_prompt("Left Corner Depth")
                    Left_Depth = self.assembly.get_prompt("Left Depth")
                    row = box.row(align=True)
                    row.label("Left Corner Size:")
                    Left_Corner_Width.draw_prompt(row,text="Depth",split_text=False)
                    Left_Corner_Depth.draw_prompt(row,text="Width",split_text=False)
                    Left_Depth.draw_prompt(row,text="Left End Depth",split_text=False)
                
                if Add_Right_Corner.value():
                    Right_Corner_Width = self.assembly.get_prompt("Right Corner Width")
                    Right_Corner_Depth = self.assembly.get_prompt("Right Corner Depth")
                    Right_Depth = self.assembly.get_prompt("Right Depth")
                    row = box.row(align=True)
                    row.label("Right Corner Size:")
                    Right_Corner_Width.draw_prompt(row,text="Depth",split_text=False)
                    Right_Corner_Depth.draw_prompt(row,text="Width",split_text=False)
                    Right_Depth.draw_prompt(row,text="Right End Depth",split_text=False)
                
                if Countertop_Type:
#                     Countertop_Type.draw_prompt(box)
                    
                    if Countertop_Type.value() == 'Melamine' and Countertop_Thickness:
#                         Countertop_Thickness.draw_prompt(box)
                        row = box.row()
                        row.label("Exposed Edges:")
                        Exposed_Left.draw_prompt(row,text="Left",split_text=False)
                        Exposed_Right.draw_prompt(row,text="Right",split_text=False)       
                        Exposed_Back.draw_prompt(row,text="Back",split_text=False)   
                        
                    if Countertop_Type.value() == 'HPL':
#                         if HPL_Material_Name:
#                             HPL_Material_Name.draw_prompt(box)
#                         if HPL_Material_Number:           
#                             HPL_Material_Number.draw_prompt(box) 
                        pass
                    
                    if Countertop_Type.value() == 'Granite':
#                         if Edge_Type:                            
#                             Edge_Type.draw_prompt(box)
                        pass
        
class OPERATOR_Place_Countertop(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".place_countertop"
    bl_label = "Place Countertop"
    bl_description = "This allows you to place a countertop."
    bl_options = {'UNDO'}
    
    #READONLY
    object_name = bpy.props.StringProperty(name="Object Name")
    
    assembly = None

    def invoke(self, context, event):
        bp = bpy.data.objects[self.object_name]
        self.assembly = fd_types.Assembly(bp)
        utils.set_wireframe(self.assembly.obj_bp,True)
        context.window.cursor_set('PAINT_BRUSH')
        context.scene.update() # THE SCENE MUST BE UPDATED FOR RAY CAST TO WORK
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel_drop(self,context,event):
        if self.assembly:
            utils.delete_object_and_children(self.assembly.obj_bp)
        bpy.context.window.cursor_set('DEFAULT')
        return {'FINISHED'}

    def ctop_drop(self,context,event):
        selected_point, selected_obj = utils.get_selection_point(context,event)
        bpy.ops.object.select_all(action='DESELECT')
        sel_product_bp = utils.get_bp(selected_obj,'PRODUCT')
        sel_assembly_bp = utils.get_assembly_bp(selected_obj)

        if sel_product_bp and sel_assembly_bp:
            product = fd_types.Assembly(sel_product_bp)
            props = props_closet.get_object_props(product.obj_bp)
            if product and props.is_closet:
#                 try:
#                     opening_number = int(sel_assembly_bp.mv.opening_name)
#                     height = product.get_prompt("Opening " + str(opening_number) + " Height")
#                 except:
#                     print("ERROR")
                # LOOP THROUGH ALL OPENINGS AND DETERMINE HOW FAR LEFT AND RIGHT THE CTOP CAN BE EXTENDED.
                heights = []
                depths = []
                for i in range(1,10):
                    height = product.get_prompt("Opening " + str(i) + " Height")
                    if height: 
                        heights.append(height.value())
                    depth = product.get_prompt("Opening " + str(i) + " Depth")
                    if depth: 
                        depths.append(depth.value())
                        
                scene_props = props_closet.get_scene_props()
                
                tk_height = product.get_prompt("Toe Kick Height")
                placement_height = 0
                if scene_props.closet_defaults.use_plant_on_top:
                    placement_height = max(heights) + unit.millimeter(16)
                else:
                    placement_height = max(heights)                   
                
                if tk_height:
                    placement_height += tk_height.value() 

                self.assembly.obj_bp.parent = product.obj_bp
                self.assembly.obj_bp.location.z = placement_height             
                self.assembly.obj_bp.location.y = -max(depths)
                self.assembly.obj_x.location.x = product.obj_x.location.x
                self.assembly.obj_y.location.y = max(depths)

            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                utils.set_wireframe(self.assembly.obj_bp,False)
                bpy.context.window.cursor_set('DEFAULT')
                bpy.ops.object.select_all(action='DESELECT')
                context.scene.objects.active = self.assembly.obj_bp
                self.assembly.obj_bp.select = True
                return {'FINISHED'}
        
        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        context.area.tag_redraw()
        
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}
        
        if event.type in {'ESC'}:
            self.cancel_drop(context,event)
            return {'FINISHED'}
        
        return self.ctop_drop(context,event)    
        
bpy.utils.register_class(PROMPTS_Counter_Top)
bpy.utils.register_class(OPERATOR_Place_Countertop)