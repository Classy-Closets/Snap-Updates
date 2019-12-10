import bpy
import math
from os import path
from mv import fd_types, unit, utils
from . import mv_closet_defaults as props_closet
from . import common_parts

class Slanted_Shoe_Shelves(fd_types.Assembly):
    
    property_id = props_closet.LIBRARY_NAME_SPACE + ".shoe_shelf_prompt"
    placement_type = "INTERIOR"
    type_assembly = "INSERT"
    mirror_y = False
    
    shelf_qty = 3
    
    upper_interior = None
    upper_exterior = None
    
    def add_shoe_shelf_prompts(self):
        defaults = props_closet.get_scene_props().closet_defaults
        
        self.add_tab(name='Slanted Shoe Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')

        self.add_prompt(name="Shelf Lip Type",
                        prompt_type='COMBOBOX',
                        items=["Wood Toe","Deco 1","Deco 2","Deco 3",'Steel Fence'],
                        value=0,
                        tab_index=1)
        
        self.add_prompt(name="Adj Shelf Qty",
                        prompt_type='QUANTITY',
                        value=self.shelf_qty,
                        tab_index=0)

        self.add_prompt(name="Shelf Angle",
                        prompt_type='ANGLE',
                        value=math.radians(17.25),
                        tab_index=0)
        
        self.add_prompt(name="Space From Bottom",
                        prompt_type='DISTANCE',
                        value=unit.inch(3.5),
                        tab_index=0)
        
        self.add_prompt(name="Space From Top",
                        prompt_type='DISTANCE',
                        value=unit.inch(8),
                        tab_index=0)
        
        self.add_prompt(name="Shelf Lip Width",
                        prompt_type='DISTANCE',
                        value=defaults.shelf_lip_width,
                        tab_index=0)
        
        self.add_prompt(name="Distance Between Shelves",
                        prompt_type='DISTANCE',
                        value=unit.inch(8),
                        tab_index=0)
        
        self.add_prompt(name="Remove Top Shelf",
                        prompt_type='CHECKBOX',
                        value=False,
                        tab_index=0)
        
        self.add_prompt(name="Adj Shelf Setback",
                        prompt_type='DISTANCE',
                        value=unit.inch(.75),
                        tab_index=0)
        
        self.add_prompt(name="Hole Spacing Qty",
                        prompt_type='QUANTITY',
                        value=0,
                        tab_index=0)
        
        self.add_prompt(name="Adjustable Shelf Thickness",
                        prompt_type='DISTANCE',
                        value=unit.inch(.75),
                        tab_index=1)
        
        Space_From_Bottom = self.get_var("Space From Bottom")
        Space_From_Top = self.get_var("Space From Top")
        Distance_Between_Shelves = self.get_var("Distance Between Shelves")
        Adj_Shelf_Qty = self.get_var("Adj Shelf Qty")
        Shelf_Lip_Type = self.get_var("Shelf Lip Type")
        
        self.prompt('Adj Shelf Setback','IF(Shelf_Lip_Type==4,0,INCH(.75))',[Shelf_Lip_Type])
        
        self.prompt('Hole Spacing Qty','(Space_From_Bottom+Space_From_Top+(Distance_Between_Shelves*(Adj_Shelf_Qty-1)))//MILLIMETER(32)',
                    [Space_From_Bottom,Space_From_Top,Distance_Between_Shelves,Adj_Shelf_Qty])
        
    def draw_shoe_shelves(self):
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Adj_Shelf_Qty = self.get_var("Adj Shelf Qty")
        Adj_Shelf_Setback = self.get_var("Adj Shelf Setback")
        Adjustable_Shelf_Thickness = self.get_var("Adjustable Shelf Thickness")
        Shelf_Clip_Gap = self.get_var("Shelf Clip Gap")
        Shelf_Angle = self.get_var("Shelf Angle")
        Shelf_Lip_Type = self.get_var("Shelf Lip Type")
        Space_From_Bottom = self.get_var("Space From Bottom")
        Distance_Between_Shelves = self.get_var("Distance Between Shelves")
        Shelf_Lip_Width = self.get_var("Shelf Lip Width")
        
        for i in range(1,11):
            adj_shelf = common_parts.add_slanted_shoe_shelf(self)
            adj_shelf.x_loc('Shelf_Clip_Gap',[Shelf_Clip_Gap])
            adj_shelf.y_loc('Depth',[Depth])
            if i == 1:
                adj_shelf.z_loc('Space_From_Bottom',[Space_From_Bottom])
            else:
                adj_shelf.z_loc('Space_From_Bottom+(Distance_Between_Shelves*' + str(i - 1) + ')',[Space_From_Bottom,Adjustable_Shelf_Thickness,Distance_Between_Shelves])
            adj_shelf.x_rot('Shelf_Angle',[Shelf_Angle])
            adj_shelf.y_rot(value = 0)
            adj_shelf.z_rot(value = 0)
            adj_shelf.x_dim('Width-(Shelf_Clip_Gap*2)',[Width,Shelf_Clip_Gap])
            adj_shelf.y_dim('-Depth+Adj_Shelf_Setback',[Depth,Adj_Shelf_Setback])
            adj_shelf.z_dim('Adjustable_Shelf_Thickness',[Adjustable_Shelf_Thickness])
            adj_shelf.prompt('Hide','IF(' + str(i) + '>Adj_Shelf_Qty,True,False)',[Adj_Shelf_Qty])
            
            Z_Loc = adj_shelf.get_var('loc_z','Z_Loc')
            Shelf_Depth = adj_shelf.get_var('dim_y','Shelf_Depth')

            shelf_lip = common_parts.add_shelf_lip(self)
            shelf_lip.x_loc('Shelf_Clip_Gap',[Shelf_Clip_Gap])
            shelf_lip.y_loc('fabs(Depth)-(fabs(Shelf_Depth)*cos(Shelf_Angle))',[Depth,Shelf_Depth,Shelf_Angle])
            shelf_lip.z_loc('Z_Loc-(fabs(Shelf_Depth)*sin(Shelf_Angle))',[Z_Loc,Shelf_Depth,Shelf_Angle])
            shelf_lip.x_rot('Shelf_Angle-radians(90)',[Shelf_Angle])
            shelf_lip.y_rot(value = 0)
            shelf_lip.z_rot(value = 0)
            shelf_lip.x_dim('Width-(Shelf_Clip_Gap*2)',[Width,Shelf_Clip_Gap])
            shelf_lip.y_dim('-Shelf_Lip_Width',[Shelf_Lip_Width])
            shelf_lip.z_dim('-Adjustable_Shelf_Thickness',[Adjustable_Shelf_Thickness])
            shelf_lip.prompt('Hide','IF(' + str(i) + '>Adj_Shelf_Qty,True,IF(Shelf_Lip_Type==0,False,True))',[Shelf_Lip_Type,Adj_Shelf_Qty])
            
            deco_1_shelf_lip = common_parts.add_deco_shelf_lip_1(self)
            deco_1_shelf_lip.x_loc('Shelf_Clip_Gap',[Shelf_Clip_Gap])
            deco_1_shelf_lip.y_loc('fabs(Depth)-(fabs(Shelf_Depth)*cos(Shelf_Angle))',[Depth,Shelf_Depth,Shelf_Angle])
            deco_1_shelf_lip.z_loc('Z_Loc-(fabs(Shelf_Depth)*sin(Shelf_Angle))',[Z_Loc,Shelf_Depth,Shelf_Angle])
            deco_1_shelf_lip.x_rot('Shelf_Angle-radians(90)',[Shelf_Angle])
            deco_1_shelf_lip.y_rot(value = 0)
            deco_1_shelf_lip.z_rot(value = 0)
            deco_1_shelf_lip.x_dim('Width-(Shelf_Clip_Gap*2)',[Width,Shelf_Clip_Gap])
            deco_1_shelf_lip.y_dim('-Shelf_Lip_Width',[Shelf_Lip_Width])
            deco_1_shelf_lip.z_dim('-Adjustable_Shelf_Thickness',[Adjustable_Shelf_Thickness])
            deco_1_shelf_lip.prompt('Hide','IF(' + str(i) + '>Adj_Shelf_Qty,True,IF(Shelf_Lip_Type==1,False,True))',[Shelf_Lip_Type,Adj_Shelf_Qty])

            deco_2_shelf_lip = common_parts.add_deco_shelf_lip_2(self)
            deco_2_shelf_lip.x_loc('Shelf_Clip_Gap',[Shelf_Clip_Gap])
            deco_2_shelf_lip.y_loc('fabs(Depth)-(fabs(Shelf_Depth)*cos(Shelf_Angle))',[Depth,Shelf_Depth,Shelf_Angle])
            deco_2_shelf_lip.z_loc('Z_Loc-(fabs(Shelf_Depth)*sin(Shelf_Angle))',[Z_Loc,Shelf_Depth,Shelf_Angle])
            deco_2_shelf_lip.x_rot('Shelf_Angle-radians(90)',[Shelf_Angle])
            deco_2_shelf_lip.y_rot(value = 0)
            deco_2_shelf_lip.z_rot(value = 0)
            deco_2_shelf_lip.x_dim('Width-(Shelf_Clip_Gap*2)',[Width,Shelf_Clip_Gap])
            deco_2_shelf_lip.y_dim('-Shelf_Lip_Width',[Shelf_Lip_Width])
            deco_2_shelf_lip.z_dim('-Adjustable_Shelf_Thickness',[Adjustable_Shelf_Thickness])
            deco_2_shelf_lip.prompt('Hide','IF(' + str(i) + '>Adj_Shelf_Qty,True,IF(Shelf_Lip_Type==2,False,True))',[Shelf_Lip_Type,Adj_Shelf_Qty])
            
            deco_3_shelf_lip = common_parts.add_deco_shelf_lip_3(self)
            deco_3_shelf_lip.x_loc('Shelf_Clip_Gap',[Shelf_Clip_Gap])
            deco_3_shelf_lip.y_loc('fabs(Depth)-(fabs(Shelf_Depth)*cos(Shelf_Angle))',[Depth,Shelf_Depth,Shelf_Angle])
            deco_3_shelf_lip.z_loc('Z_Loc-(fabs(Shelf_Depth)*sin(Shelf_Angle))',[Z_Loc,Shelf_Depth,Shelf_Angle])
            deco_3_shelf_lip.x_rot('Shelf_Angle-radians(90)',[Shelf_Angle])
            deco_3_shelf_lip.y_rot(value = 0)
            deco_3_shelf_lip.z_rot(value = 0)
            deco_3_shelf_lip.x_dim('Width-(Shelf_Clip_Gap*2)',[Width,Shelf_Clip_Gap])
            deco_3_shelf_lip.y_dim('-Shelf_Lip_Width',[Shelf_Lip_Width])
            deco_3_shelf_lip.z_dim('-Adjustable_Shelf_Thickness',[Adjustable_Shelf_Thickness])
            deco_3_shelf_lip.prompt('Hide','IF(' + str(i) + '>Adj_Shelf_Qty,True,IF(Shelf_Lip_Type==3,False,True))',[Shelf_Lip_Type,Adj_Shelf_Qty])      
            
            steel_fence = common_parts.add_shelf_fence(self)
            steel_fence.x_loc('Shelf_Clip_Gap+INCH(1)',[Shelf_Clip_Gap])
            steel_fence.y_loc('fabs(Depth)-(fabs(Shelf_Depth+INCH(1))*cos(Shelf_Angle))',[Depth,Shelf_Depth,Shelf_Angle])
            steel_fence.z_loc('Z_Loc-(fabs(Shelf_Depth+INCH(1))*sin(Shelf_Angle))',[Z_Loc,Shelf_Depth,Shelf_Angle])
            steel_fence.x_rot('Shelf_Angle+radians(90)',[Shelf_Angle])
            steel_fence.y_rot(value = 0)
            steel_fence.z_rot(value = 0)
            steel_fence.x_dim('Width-(Shelf_Clip_Gap*2)-INCH(2)',[Width,Shelf_Clip_Gap])
            steel_fence.y_dim('-Shelf_Lip_Width',[Shelf_Lip_Width])
            steel_fence.z_dim('-Adjustable_Shelf_Thickness',[Adjustable_Shelf_Thickness])
            steel_fence.prompt('Hide','IF(' + str(i) + '>Adj_Shelf_Qty,True,IF(Shelf_Lip_Type==4,False,True))',[Shelf_Lip_Type,Adj_Shelf_Qty])
            
    def add_insert(self,insert):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Adjustable_Shelf_Thickness = self.get_var("Adjustable Shelf Thickness")
        Hole_Spacing_Qty = self.get_var("Hole Spacing Qty")
        
        insert.x_loc(value = 0)
        insert.y_loc(value = 0)
        insert.z_loc('Hole_Spacing_Qty*MILLIMETER(32)',[Hole_Spacing_Qty,Adjustable_Shelf_Thickness])
        insert.x_rot(value = 0)
        insert.y_rot(value = 0)
        insert.z_rot(value = 0)
        insert.x_dim('Width',[Width])
        insert.y_dim('Depth',[Depth])
        insert.z_dim('Height-(Hole_Spacing_Qty*MILLIMETER(32))',[Height,Hole_Spacing_Qty,Adjustable_Shelf_Thickness]) 
            
    def draw(self):
        self.create_assembly()
        
        self.add_shoe_shelf_prompts()
        self.draw_shoe_shelves()
        
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Adjustable_Shelf_Thickness = self.get_var("Adjustable Shelf Thickness")
        Hole_Spacing_Qty = self.get_var("Hole Spacing Qty")
        Remove_Top_Shelf = self.get_var("Remove Top Shelf")
        
        top_shelf = common_parts.add_shelf(self)
        top_shelf.x_loc(value = 0)
        top_shelf.y_loc(value = 0)
        top_shelf.z_loc('Hole_Spacing_Qty*MILLIMETER(32)',[Hole_Spacing_Qty])
        top_shelf.x_rot(value = 0)
        top_shelf.y_rot(value = 0)
        top_shelf.z_rot(value = 0)
        top_shelf.x_dim('Width',[Width])
        top_shelf.y_dim('Depth',[Depth])
        top_shelf.z_dim('-Adjustable_Shelf_Thickness',[Adjustable_Shelf_Thickness])
        top_shelf.prompt('Hide','IF(Remove_Top_Shelf,True,False)',[Remove_Top_Shelf])
        
        opening = common_parts.add_opening(self)
        opening.set_name("Opening")
        self.add_insert(opening)
        
        if self.upper_exterior:
            opening.obj_bp.mv.exterior_open = False
            self.upper_exterior.draw()
            self.upper_exterior.obj_bp.parent = self.obj_bp
            self.add_insert(self.upper_exterior)
            
        if self.upper_interior:
            opening.obj_bp.mv.interior_open = False
            self.upper_interior.draw()
            self.upper_interior.obj_bp.parent = self.obj_bp
            self.add_insert(self.upper_interior)
        
        self.update()
        
class PROMPTS_Shoe_Shelf_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".shoe_shelf_prompt"
    bl_label = "Shoe Shelf Prompts" 
    bl_description = "This shows all of the available shoe shelf options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    shelf_qty = bpy.props.IntProperty(name="Shelf Quantity",min=1,max=10)

    adj_shelf_qty_prompt = None

    assembly = None
    
    @classmethod
    def poll(cls, context):
        return True
        
    def check(self, context):
        utils.run_calculators(self.assembly.obj_bp)
        
        if self.adj_shelf_qty_prompt:
            self.adj_shelf_qty_prompt.set_value(self.shelf_qty)
            
        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport
        
        return True
        
    def execute(self, context):
        return {'FINISHED'}

    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj,'INSERT')
        self.assembly = fd_types.Assembly(obj_insert_bp)
        
        self.adj_shelf_qty_prompt = self.assembly.get_prompt("Adj Shelf Qty")

        if self.adj_shelf_qty_prompt:
            self.shelf_qty = self.adj_shelf_qty_prompt.value()

        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=330)
        
    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                
                if self.adj_shelf_qty_prompt:
                    shelf_lip_type = self.assembly.get_prompt("Shelf Lip Type")
                    space_from_bottom = self.assembly.get_prompt("Space From Bottom")
                    space_from_top = self.assembly.get_prompt("Space From Top")
                    dist_between_shelves = self.assembly.get_prompt("Distance Between Shelves")
                    remove_top_shelf = self.assembly.get_prompt("Remove Top Shelf")
                    
                    box = layout.box()
                    row = box.row()
                    row.label("Adjustable Shelf Options:")
                    
                    row = box.row()
                    shelf_lip_type.draw_prompt(row)

                    row = box.row()
                    row.label("Shelf Quantity")
                    row.prop(self,'shelf_qty',text="")
                    
                    row = box.row()
                    space_from_top.draw_prompt(row)
                    
                    row = box.row()
                    space_from_bottom.draw_prompt(row)                    
                    
                    row = box.row()
                    dist_between_shelves.draw_prompt(row)                        
                    
                    row = box.row()
                    remove_top_shelf.draw_prompt(row)

bpy.utils.register_class(PROMPTS_Shoe_Shelf_Prompts)        
        