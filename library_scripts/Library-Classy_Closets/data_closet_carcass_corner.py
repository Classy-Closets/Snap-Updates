import bpy
from . import mv_closet_defaults as props_closet
from . import common_prompts
from . import common_parts
from . import common_lists
from mv import fd_types, utils, unit
from os import path
import math

ASSEMBLY_DIR = path.join(common_parts.LIBRARY_DATA_DIR,"Assemblies")
PART_WITH_EDGEBANDING = path.join(ASSEMBLY_DIR,"Part with Edgebanding.blend")
PART_WITH_NO_EDGEBANDING = path.join(ASSEMBLY_DIR,"Part with No Edgebanding.blend")
CORNER_NOTCH_PART = path.join(ASSEMBLY_DIR,"Corner Notch Part.blend")
CHAMFERED_PART = path.join(ASSEMBLY_DIR,"Chamfered Part.blend")
RADIUS_CORNER_PART_WITH_EDGEBANDING = path.join(ASSEMBLY_DIR,"Radius Corner Part with Edgebanding.blend")
BENDING_PART = path.join(ASSEMBLY_DIR,"Bending Part.blend")


class L_Shelves(fd_types.Assembly):

    """
    This L Shelf Includes a Back Spine for support and is hanging first
    Also includes the option to change L Shelves to Angled Shelves
    """

    library_name = "Closets By Design"
    category_name = "Corner Units"
    type_assembly = "PRODUCT"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".corner_shelves"
    placement_type = 'Corner'
    # drop_id = "cbddrop.place_corner_l_shelves"

    def draw(self):
        self.create_assembly()
        
        props = props_closet.get_scene_props()
        
        self.add_tab(name='L Shelf Options',tab_type='VISIBLE')
        self.add_tab(name='Material Thickness',tab_type='HIDDEN')
        self.add_tab(name='Shelf Heights',tab_type='VISIBLE')
        self.add_prompt(name="Panel Height",prompt_type='DISTANCE',value=unit.millimeter(float(props.closet_defaults.panel_height)),tab_index=0)
        self.add_prompt(name="Back Inset",prompt_type='DISTANCE',value=unit.inch(.25),tab_index=0)
        self.add_prompt(name="Spine Width",prompt_type='DISTANCE',value=unit.inch(1),tab_index=0)
        self.add_prompt(name="Spine Y Location",prompt_type='DISTANCE',value=unit.inch(2.1),tab_index=0)
        self.add_prompt(name="Cleat Height",prompt_type='DISTANCE',value=unit.inch(3.64),tab_index=0)
        self.add_prompt(name="Left Depth",prompt_type='DISTANCE',value=unit.inch(12),tab_index=0)       
        self.add_prompt(name="Right Depth",prompt_type='DISTANCE',value=unit.inch(12),tab_index=0)  
        self.add_prompt(name="Shelf Quantity",prompt_type='QUANTITY',value=3,tab_index=0)  
        self.add_prompt(name="Add Top",prompt_type='CHECKBOX',value=True,tab_index=0,export=True)  
        self.add_prompt(name="Hide Toe Kick",prompt_type='CHECKBOX',value=False,tab_index=0,export=True)
        self.add_prompt(name="Add Backing",prompt_type='CHECKBOX',value=False,tab_index=0,export=True)
        self.add_prompt(name="Is Hanging",prompt_type='CHECKBOX',value=False,tab_index=0,export=True)
        self.add_prompt(name="Angled Shelves",prompt_type='CHECKBOX',value=False,tab_index=0,export=True)
        self.add_prompt(name="Use Left Swing",prompt_type='CHECKBOX',value=False,tab_index=0,export=True)
        self.add_prompt(name="Pull Location",prompt_type='COMBOBOX',items=["Pull on Left Door","Pull on Right Door"],value=0,tab_index=0,export=True)
        self.add_prompt(name="Force Double Doors",prompt_type='CHECKBOX',value=False,tab_index=0,export=True)
        self.add_prompt(name="Door",prompt_type='CHECKBOX',value=False,tab_index=0,export=True)        
        self.add_prompt(name="Door Pull Height",prompt_type='DISTANCE',value=unit.inch(36),tab_index=0)
        self.add_prompt(name="Door Type",prompt_type='COMBOBOX',items=["Reach Back","Lazy Susan"],value=0,tab_index=0,export=True)
        self.add_prompt(name="Open Door",prompt_type='PERCENTAGE',value=0,tab_index=0)
        self.add_prompt(name="Door Rotation",prompt_type='ANGLE',value=120,tab_index=0)
        self.add_prompt(name="Half Open",prompt_type='PERCENTAGE',value=0.5,tab_index=0)
        self.add_prompt(name="Pull Type",prompt_type='COMBOBOX',items=["Base","Tall","Upper"],value=0,tab_index=0)

        for i in range(1,11):
            self.add_prompt(name="Shelf " + str(i) + " Height",prompt_type='DISTANCE',value=unit.millimeter(493.014),tab_index=2)

        self.add_prompt(
                name="Backing Thickness",
                prompt_type='COMBOBOX',
                items=['1/4"', '3/4"'],
                value=1,
                tab_index=1
            )
        
        common_prompts.add_toe_kick_prompts(self)
        common_prompts.add_thickness_prompts(self)
        common_prompts.add_door_prompts(self)
        common_prompts.add_door_pull_prompts(self)
        
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Panel_Height = self.get_var('Panel Height')
        Left_Depth = self.get_var('Left Depth')
        Right_Depth = self.get_var('Right Depth')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        PT = self.get_var('Panel Thickness',"PT")
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Toe_Kick_Setback = self.get_var('Toe Kick Setback')
        Hide_Toe_Kick = self.get_var('Hide Toe Kick')
        Shelf_Quantity = self.get_var('Shelf Quantity')
        Add_Backing = self.get_var('Add Backing')
        Back_Inset = self.get_var('Back Inset')
        DT = self.get_var('Door Type','DT')

        Add_Top = self.get_var('Add Top')
        Backing_Thickness = self.get_var('Backing Thickness')
        Is_Hanging = self.get_var('Is Hanging')
        Spine_Width = self.get_var('Spine Width')
        Spine_Y_Location = self.get_var('Spine Y Location')
        Cleat_Height = self.get_var('Cleat Height')
        Angled_Shelves = self.get_var('Angled Shelves')
        Door = self.get_var('Door')              
        Door_Pull_Height = self.get_var('Door Pull Height')
        Use_Left_Swing = self.get_var("Use Left Swing")
        Pull_Location = self.get_var("Pull Location")
        Force_Double_Doors = self.get_var("Force Double Doors")
        Open = self.get_var("Open Door",'Open')
        Rotation = self.get_var("Door Rotation",'Rotation')
        Half = self.get_var("Half Open",'Half')
        Pull_Type = self.get_var("Pull Type")
        Base_Pull_Location = self.get_var("Base Pull Location")
        Tall_Pull_Location = self.get_var("Tall Pull Location")
        Upper_Pull_Location = self.get_var("Upper Pull Location")
        World_Z = self.get_var('world_loc_z','World_Z',transform_type='LOC_Z')
        
        inside_height_empty = self.add_empty()
        inside_height_empty.z_loc('IF(Is_Hanging,Panel_Height-(Shelf_Thickness*2)-(Shelf_Thickness*Shelf_Quantity),Height-Toe_Kick_Height-(Shelf_Thickness*2)-(Shelf_Thickness*Shelf_Quantity))',[Panel_Height,Is_Hanging,Height,Toe_Kick_Height,Shelf_Thickness,Shelf_Quantity])
        Inside_Height = inside_height_empty.get_var('loc_z','Inside_Height')
        
        top = common_parts.add_l_shelf(self)
        top.x_loc(value=0)
        top.y_loc(value=0)
        top.z_loc('(Height+IF(Is_Hanging,0,Toe_Kick_Height))',[Height,Toe_Kick_Height,Is_Hanging])
        top.x_rot(value = 0)
        top.y_rot(value = 0)
        top.z_rot(value = 0)
        top.x_dim('Width-PT',[Width,PT])
        top.y_dim('Depth+PT',[Depth,PT])
        top.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        top.prompt('Left Depth','Left_Depth',[Left_Depth])
        top.prompt('Right Depth','Right_Depth',[Right_Depth])
        top.prompt('Hide','IF(Angled_Shelves,True,False)',[Angled_Shelves,Add_Top])
        top.prompt('Is Locked Shelf',value=True)
        top.prompt('Is Forced Locked Shelf',value=True)
        
        top_angled = common_parts.add_angle_shelf(self)
        top_angled.x_loc(value=0)
        top_angled.y_loc(value=0)
        top_angled.z_loc('(Height+IF(Is_Hanging,0,Toe_Kick_Height))',[Height,Toe_Kick_Height,Is_Hanging])
        top_angled.x_rot(value = 0)
        top_angled.y_rot(value = 0)
        top_angled.z_rot(value = 0)
        top_angled.x_dim('Width-PT',[Width,PT])
        top_angled.y_dim('Depth+PT',[Depth,PT])
        top_angled.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        top_angled.prompt('Left Depth','Left_Depth',[Left_Depth])
        top_angled.prompt('Right Depth','Right_Depth',[Right_Depth])
        top_angled.prompt('Hide','IF(Angled_Shelves != True,True,False)',[Angled_Shelves,Add_Top])
        top_angled.prompt('Is Locked Shelf',value=True)
        top_angled.prompt('Is Forced Locked Shelf',value=True)
        
        right_top_cleat = common_parts.add_cleat(self)
        right_top_cleat.set_name("Right Top Cleat")
        right_top_cleat.x_loc('Spine_Width',[Spine_Width])
        right_top_cleat.y_loc(value=0)
        right_top_cleat.z_loc('(IF(Add_Top,Height-Shelf_Thickness,Height))+IF(Is_Hanging,0,Toe_Kick_Height)',[Height,Shelf_Thickness,Add_Top,Is_Hanging,Toe_Kick_Height])
        right_top_cleat.x_rot(value=-90)
        right_top_cleat.y_rot(value=0)
        right_top_cleat.z_rot(value=0)
        right_top_cleat.x_dim('Width-Spine_Width-PT',[Width,PT,Spine_Width])
        right_top_cleat.y_dim('Cleat_Height',[Cleat_Height])
        right_top_cleat.z_dim('-PT',[PT])   
        right_top_cleat.prompt('Hide', 'IF(AND(Add_Backing,Backing_Thickness==1),True,False)', [Add_Backing,Backing_Thickness])   
        
        left_top_cleat = common_parts.add_cleat(self)
        left_top_cleat.set_name("Left Top Cleat")
        left_top_cleat.x_loc(value=0)
        left_top_cleat.y_loc('Depth+PT',[Depth,PT])
        left_top_cleat.z_loc('(IF(Add_Top,Height-Shelf_Thickness,Height))+IF(Is_Hanging,0,Toe_Kick_Height)',[Height,Shelf_Thickness,Add_Top,Is_Hanging,Toe_Kick_Height])
        left_top_cleat.x_rot(value=-90)
        left_top_cleat.y_rot(value=0)
        left_top_cleat.z_rot(value=90)
        left_top_cleat.x_dim('-Depth-Spine_Width-PT',[Depth,PT,Spine_Width])
        left_top_cleat.y_dim('Cleat_Height',[Cleat_Height])
        left_top_cleat.z_dim('-PT',[PT])
        left_top_cleat.prompt('Hide', 'IF(AND(Add_Backing,Backing_Thickness==1),True,False)', [Add_Backing,Backing_Thickness])   
        
        bottom = common_parts.add_l_shelf(self)
        bottom.x_loc(value=0)
        bottom.y_loc(value=0)
        bottom.z_loc('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)',[Is_Hanging,Height,Panel_Height,Toe_Kick_Height])
        bottom.x_rot(value = 0)
        bottom.y_rot(value = 0)
        bottom.z_rot(value = 0)
        bottom.x_dim('Width-PT',[Width,PT])
        bottom.y_dim('Depth+PT',[Depth,PT])
        bottom.z_dim('Shelf_Thickness',[Shelf_Thickness])
        bottom.prompt('Left Depth','Left_Depth',[Left_Depth])
        bottom.prompt('Right Depth','Right_Depth',[Right_Depth])
        bottom.prompt('Hide','IF(Angled_Shelves,True,False)',[Angled_Shelves])    
        bottom.prompt('Is Locked Shelf',value=True)     
        bottom.prompt('Is Forced Locked Shelf',value=True)
        
        bottom_angled = common_parts.add_angle_shelf(self)
        bottom_angled.x_loc(value=0)
        bottom_angled.y_loc(value=0)
        bottom_angled.z_loc('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)',[Is_Hanging,Height,Panel_Height,Toe_Kick_Height])
        bottom_angled.x_rot(value = 0)
        bottom_angled.y_rot(value = 0)
        bottom_angled.z_rot(value = 0)
        bottom_angled.x_dim('Width-PT',[Width,PT])
        bottom_angled.y_dim('Depth+PT',[Depth,PT])
        bottom_angled.z_dim('Shelf_Thickness',[Shelf_Thickness])
        bottom_angled.prompt('Left Depth','Left_Depth',[Left_Depth])
        bottom_angled.prompt('Right Depth','Right_Depth',[Right_Depth])
        bottom_angled.prompt('Hide','IF(Angled_Shelves,False,True)',[Angled_Shelves]) 
        bottom_angled.prompt('Is Locked Shelf',value=True)  
        bottom_angled.prompt('Is Forced Locked Shelf',value=True)
        
        right_bot_cleat = common_parts.add_cleat(self)
        right_bot_cleat.set_name("Right Bottom Cleat")
        right_bot_cleat.x_loc('Spine_Width',[Spine_Width])
        right_bot_cleat.y_loc(value=0)
        right_bot_cleat.z_loc('IF(Is_Hanging,Height-Panel_Height+Shelf_Thickness,Shelf_Thickness+Toe_Kick_Height)',[Height,Panel_Height,Is_Hanging,Shelf_Thickness,Toe_Kick_Height])
        right_bot_cleat.x_rot(value=-90)
        right_bot_cleat.y_rot(value=0)
        right_bot_cleat.z_rot(value=0)
        right_bot_cleat.x_dim('Width-Spine_Width-PT',[Width,PT,Spine_Width])
        right_bot_cleat.y_dim('-Cleat_Height',[Cleat_Height])
        right_bot_cleat.z_dim('-PT',[PT])
        right_bot_cleat.prompt('Hide', 'IF(AND(Add_Backing,Backing_Thickness==1),True,False)', [Add_Backing,Backing_Thickness])        
        
        left_bot_cleat = common_parts.add_cleat(self)
        left_bot_cleat.set_name("Left Bottom Cleat")
        left_bot_cleat.x_loc(value=0)
        left_bot_cleat.y_loc('Depth+PT',[Depth,PT])
        left_bot_cleat.z_loc('IF(Is_Hanging,Height-Panel_Height+Shelf_Thickness,Shelf_Thickness+Toe_Kick_Height)',[Height,Panel_Height,Is_Hanging,Shelf_Thickness,Toe_Kick_Height])
        left_bot_cleat.x_rot(value=-90)
        left_bot_cleat.y_rot(value=0)
        left_bot_cleat.z_rot(value=90)
        left_bot_cleat.x_dim('-Depth-Spine_Width-PT',[Depth,PT,Spine_Width])
        left_bot_cleat.y_dim('-Cleat_Height',[Cleat_Height])
        left_bot_cleat.z_dim('-PT',[PT])
        left_bot_cleat.prompt('Hide', 'IF(AND(Add_Backing,Backing_Thickness==1),True,False)', [Add_Backing,Backing_Thickness])               
        
        left_panel = common_parts.add_panel(self)
        left_panel.set_name("Left Panel")
        left_panel.x_loc(value=0)
        left_panel.y_loc('Depth',[Depth,Add_Backing])
        left_panel.z_loc('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)',[Height,Panel_Height,Is_Hanging,Toe_Kick_Height])
        left_panel.x_rot(value = 0)
        left_panel.y_rot(value = -90)
        left_panel.z_rot(value = -90)
        left_panel.x_dim('Panel_Height',[Panel_Height])
        left_panel.y_dim('Left_Depth',[Left_Depth])
        left_panel.z_dim('PT',[PT])
        left_panel.prompt('Left Depth','Left_Depth',[Left_Depth])#Adding this in order to drill the panel on one side
         
        right_panel = common_parts.add_panel(self)
        right_panel.set_name("Right Panel")
        right_panel.x_loc('Width-PT',[Width,PT])
        right_panel.y_loc(value=0)
        right_panel.z_loc('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)',[Height,Panel_Height,Is_Hanging,Toe_Kick_Height])
        right_panel.x_rot(value = 0)
        right_panel.y_rot(value = -90)
        right_panel.z_rot(value = 180)
        right_panel.x_dim('Panel_Height',[Panel_Height])
        right_panel.y_dim('Right_Depth',[Right_Depth])
        right_panel.z_dim('PT',[PT])
        right_panel.prompt('Right Depth','Right_Depth',[Right_Depth])#Adding this in order to drill the panel on one side
        
        right_back = common_parts.add_corner_back(self)
        right_back.set_name("Backing")
        right_back.x_loc('Width-PT',[Spine_Y_Location,Width,PT])
        right_back.y_loc(value = 0)
        right_back.z_loc('IF(Is_Hanging,Height-Panel_Height+PT+IF(Backing_Thickness==0,Cleat_Height-Back_Inset,0),Toe_Kick_Height+PT+IF(Backing_Thickness==0,Cleat_Height-Back_Inset,0))',[Height,Panel_Height,Is_Hanging,Toe_Kick_Height,Cleat_Height,Back_Inset,PT,Backing_Thickness])
        right_back.x_rot(value = 0)
        right_back.y_rot(value = -90)
        right_back.z_rot(value = -90)
        right_back.x_dim('Panel_Height-IF(Backing_Thickness==0,Cleat_Height*2+Back_Inset,PT)-IF(Add_Top,PT,0)',[Panel_Height,Cleat_Height,Back_Inset,PT,Add_Top,Backing_Thickness])
        right_back.y_dim('-Width+(PT*2)',[Width,PT,Spine_Y_Location])
        right_back.z_dim('IF(Backing_Thickness==0,-INCH(0.25),-INCH(0.75))',[Backing_Thickness])
        right_back.prompt('Hide','IF(Add_Backing,False,True)',[Add_Backing])
        
        left_back = common_parts.add_corner_back(self)
        left_back.x_loc(value = 0)
        left_back.y_loc('Depth+PT',[Spine_Y_Location,Depth,PT])
        left_back.z_loc('IF(Is_Hanging,Height-Panel_Height+PT+IF(Backing_Thickness==0,Cleat_Height-Back_Inset,0),Toe_Kick_Height+PT+IF(Backing_Thickness==0,Cleat_Height-Back_Inset,0))',[Height,Panel_Height,Is_Hanging,Toe_Kick_Height,Cleat_Height,Back_Inset,PT,Backing_Thickness])
        left_back.x_rot(value = 0)
        left_back.y_rot(value = -90)
        left_back.z_rot(value = -180)
        left_back.x_dim('Panel_Height-IF(Backing_Thickness==0,Cleat_Height*2+Back_Inset,PT)-IF(Add_Top,PT,0)',[Panel_Height,Cleat_Height,Back_Inset,PT,Add_Top,Backing_Thickness])
        left_back.y_dim('Depth+PT',[Depth,Spine_Y_Location,PT])
        left_back.z_dim('IF(Backing_Thickness==0,INCH(0.25),INCH(0.75))',[Backing_Thickness])
        left_back.prompt('Hide','IF(Add_Backing,False,True)',[Add_Backing])
        left_back.prompt('Is Left Back',value=True)
        
        spine = common_parts.add_panel(self)
        spine.set_name("Mitered Pard")
        props = props_closet.get_object_props(spine.obj_bp)
        props.is_panel_bp = False
        props.is_mitered_pard_bp = True
        spine.obj_bp.mv.comment_2 = "1510"
        spine.x_loc(value = 0)
        spine.y_loc("-Spine_Y_Location", [Spine_Y_Location])
        spine.z_loc('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)',[Height,Panel_Height,Is_Hanging,Toe_Kick_Height])
        spine.x_rot(value = 0)
        spine.y_rot(value = -90)
        spine.z_rot(value = -45)
        spine.x_dim('Panel_Height',[Panel_Height])
        spine.y_dim(value=unit.inch(2.92))
        spine.z_dim('PT',[PT])
        spine.prompt('Hide','IF(Add_Backing,True,False)',[Add_Backing])
        
        #Toe_Kick   
        left_kick = common_parts.add_toe_kick(self)
        left_kick.obj_bp.mv.comment_2 = "1034"
        left_kick.x_loc('Left_Depth-Toe_Kick_Setback',[Left_Depth,Toe_Kick_Setback])
        left_kick.y_loc('Depth+PT',[Depth,PT,Add_Backing])
        left_kick.z_loc(value = 0)
        left_kick.x_rot(value = 90)
        left_kick.y_rot(value = 0)
        left_kick.z_rot(value = -90)
        left_kick.x_dim('Depth+Right_Depth-Toe_Kick_Setback',[Depth,Right_Depth,Toe_Kick_Setback])
        left_kick.y_dim('Toe_Kick_Height',[Toe_Kick_Height])
        left_kick.z_dim('PT',[PT])        
        left_kick.prompt('Hide','IF(Hide_Toe_Kick,True,IF(Angled_Shelves,True,IF(Is_Hanging,True,False)))',[Hide_Toe_Kick,Angled_Shelves,Is_Hanging])
        
        left_kick_back = common_parts.add_toe_kick(self)
        left_kick_back.set_name("Left Kick Back")
        left_kick_back.obj_bp.mv.comment_2 = "1034"
        left_kick_back.x_loc(value = 0)
        left_kick_back.y_loc('-PT',[PT])
        left_kick_back.z_loc(value = 0)
        left_kick_back.x_rot(value = 90)
        left_kick_back.y_rot(value = 0)
        left_kick_back.z_rot(value = 90)
        left_kick_back.x_dim('Depth+2*PT',[Depth,PT])
        left_kick_back.y_dim('Toe_Kick_Height',[Toe_Kick_Height])
        left_kick_back.z_dim('PT',[PT])
        left_kick_back.prompt('Hide','IF(Hide_Toe_Kick,True,IF(Is_Hanging,True,False))',[Hide_Toe_Kick,Is_Hanging])
        
        left_kick_stringer = common_parts.add_toe_kick(self)
        left_kick_stringer.set_name("Left Kick Stringer")
        left_kick_stringer.obj_bp.mv.comment_2 = "1035"
        left_kick_stringer.x_loc(value = 0)
        left_kick_stringer.y_loc('Depth+PT',[Depth,PT,Add_Backing])
        left_kick_stringer.z_loc(value = 0)
        left_kick_stringer.x_rot(value = 90)
        left_kick_stringer.y_rot(value = 0)
        left_kick_stringer.z_rot(value = 0)
        left_kick_stringer.x_dim('Left_Depth-Toe_Kick_Setback',[Left_Depth,Toe_Kick_Setback])
        left_kick_stringer.y_dim('Toe_Kick_Height',[Toe_Kick_Height])
        left_kick_stringer.z_dim('PT',[PT])
        left_kick_stringer.prompt('Hide','IF(Hide_Toe_Kick,True,IF(Is_Hanging,True,False))',[Hide_Toe_Kick,Is_Hanging])
         
        right_kick = common_parts.add_toe_kick(self)
        right_kick.obj_bp.mv.comment_2 = "1034"
        right_kick.x_loc('Width-PT',[Width,PT,Add_Backing])
        right_kick.y_loc('-Right_Depth+Toe_Kick_Setback',[Right_Depth,Toe_Kick_Setback])
        right_kick.z_loc(value = 0)
        right_kick.x_rot(value = 90)
        right_kick.y_rot(value = 0)
        right_kick.z_rot(value = 180)
        right_kick.x_dim('Width-Left_Depth+Toe_Kick_Setback-Shelf_Thickness',[Width,Left_Depth,Toe_Kick_Setback,Shelf_Thickness])
        right_kick.y_dim('Toe_Kick_Height',[Toe_Kick_Height])
        right_kick.z_dim('PT',[PT])
        right_kick.prompt('Hide','IF(Hide_Toe_Kick,True,IF(Angled_Shelves,True,IF(Is_Hanging,True,False)))',[Hide_Toe_Kick,Angled_Shelves,Is_Hanging])
        
        right_kick_back = common_parts.add_toe_kick(self)
        right_kick_back.set_name("Right Kick Back")
        right_kick_back.obj_bp.mv.comment_2 = "1034"
        right_kick_back.x_loc(value = 0)
        right_kick_back.y_loc(value = 0)
        right_kick_back.z_loc(value = 0)
        right_kick_back.x_rot(value = 90)
        right_kick_back.y_rot(value = 0)
        right_kick_back.z_rot(value = 0)
        right_kick_back.x_dim('Width-PT',[Width,PT])
        right_kick_back.y_dim('Toe_Kick_Height',[Toe_Kick_Height])
        right_kick_back.z_dim('PT',[PT])
        right_kick_back.prompt('Hide','IF(Hide_Toe_Kick,True,IF(Is_Hanging,True,False))',[Hide_Toe_Kick,Is_Hanging])
        
        right_kick_stringer = common_parts.add_toe_kick(self)
        right_kick_stringer.set_name("Right Kick Stringer")
        right_kick_stringer.obj_bp.mv.comment_2 = "1035"
        right_kick_stringer.x_loc('Width',[Width])
        right_kick_stringer.y_loc(value = 0)
        right_kick_stringer.z_loc(value = 0)
        right_kick_stringer.x_rot(value = 90)
        right_kick_stringer.y_rot(value = 0)
        right_kick_stringer.z_rot(value = -90)
        right_kick_stringer.x_dim('Right_Depth-Toe_Kick_Setback',[Right_Depth,Toe_Kick_Setback])
        right_kick_stringer.y_dim('Toe_Kick_Height',[Toe_Kick_Height])
        right_kick_stringer.z_dim('PT',[PT])
        right_kick_stringer.prompt('Hide','IF(Hide_Toe_Kick,True,IF(Is_Hanging,True,False))',[Hide_Toe_Kick,Is_Hanging])
        
        angle_kick = common_parts.add_toe_kick(self)
        angle_kick.set_name("Angle Kick")
        angle_kick.obj_bp.mv.comment_2 = "1034"
        angle_kick.x_loc('Left_Depth-Toe_Kick_Setback-PT+.00635',[Left_Depth,Toe_Kick_Setback,PT])
        angle_kick.y_loc('Depth+PT-.00635',[Depth,PT])
        angle_kick.z_loc(value = 0)
        angle_kick.x_rot(value = 90)
        angle_kick.y_rot(value = 0)
        angle_kick.z_rot('-atan((Depth+Right_Depth-Toe_Kick_Setback)/(Width-Left_Depth+Toe_Kick_Setback))',[Width,Depth,Right_Depth,Left_Depth,Toe_Kick_Setback])
        angle_kick.x_dim('sqrt((Width-Left_Depth+Toe_Kick_Setback-Shelf_Thickness)**2+(Depth+Right_Depth-Toe_Kick_Setback)**2)+.0127',[Width,Depth,Left_Depth,Right_Depth,Toe_Kick_Setback,Shelf_Thickness])
        angle_kick.y_dim('Toe_Kick_Height',[Toe_Kick_Height])
        angle_kick.z_dim('PT',[PT])
        angle_kick.prompt('Hide','IF(Hide_Toe_Kick,True,IF(Is_Hanging,True,IF(Angled_Shelves,False,True)))',[Hide_Toe_Kick,Angled_Shelves,Is_Hanging])             
        
        
        #Doors
        #Left Angled Door     
        angled_door_l = common_parts.add_door(self)
        angled_door_l.set_name("Angled Door Left")
        angled_door_l.x_loc("Left_Depth",[Left_Depth])
        angled_door_l.y_loc("Depth+PT",[Depth,PT])
        angled_door_l.z_loc('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)',[Height,Panel_Height,Is_Hanging,Toe_Kick_Height,Shelf_Thickness])
        angled_door_l.x_rot(value = 0)
        angled_door_l.y_rot(value = -90)
        angled_door_l.z_rot('(atan((Width-Left_Depth)/(Depth+Right_Depth)))+3.14159-radians(Open*Rotation)',[Width,Depth,Right_Depth,Left_Depth,Open,Rotation])
        angled_door_l.x_dim('Panel_Height-(Shelf_Thickness)',[Panel_Height,Shelf_Thickness])
        angled_door_l.y_dim('IF(Force_Double_Doors,(sqrt((Width-Left_Depth-PT)**2+(Depth+Right_Depth+PT)**2)/2)-0.0015875,(sqrt((Width-Left_Depth-PT)**2+(Depth+Right_Depth+PT)**2)))*-1',[Width,Left_Depth,Depth,Right_Depth,PT,Force_Double_Doors])
        angled_door_l.z_dim('PT',[PT])
        angled_door_l.prompt('Hide','IF((Door and Angled_Shelves and Force_Double_Doors and Use_Left_Swing),False,IF((Door and Angled_Shelves and Force_Double_Doors),False,IF((Door and Angled_Shelves and Use_Left_Swing),True,IF((Door and Angled_Shelves),False,True))))',[Door,Use_Left_Swing,Angled_Shelves,Force_Double_Doors])
 
        #Right Angled Door
        angled_door_r = common_parts.add_door(self)
        angled_door_r.set_name("Angled Door Right")
        angled_door_r.x_loc('Width-PT',[Width,PT])        
        angled_door_r.y_loc('-Right_Depth',[Right_Depth])       
        angled_door_r.z_loc('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)',[Height,Panel_Height,Is_Hanging,Toe_Kick_Height,Shelf_Thickness])
        angled_door_r.x_rot(value = 0)
        angled_door_r.y_rot(value = -90)
        angled_door_r.z_rot('(atan((Width-Left_Depth)/(Depth+Right_Depth)))+3.14159+radians(Open*Rotation)',[Width,Depth,Right_Depth,Left_Depth,Open,Rotation])
        angled_door_r.x_dim('Panel_Height-(Shelf_Thickness)',[Panel_Height,Shelf_Thickness])
        angled_door_r.y_dim('IF(Force_Double_Doors,(sqrt((Width-Left_Depth-PT)**2+(Depth+Right_Depth+PT)**2)/2)-0.0015875,(sqrt((Width-Left_Depth-PT)**2+(Depth+Right_Depth+PT)**2)))',[Width,Left_Depth,Depth,Right_Depth,PT,Force_Double_Doors])
        angled_door_r.z_dim('PT',[PT])
        angled_door_r.prompt('Hide','IF((Door and Angled_Shelves and Force_Double_Doors and Use_Left_Swing),False,IF((Door and Angled_Shelves and Force_Double_Doors),False,IF((Door and Angled_Shelves and Use_Left_Swing),False,IF((Door and Angled_Shelves),True,True))))',[Door,Use_Left_Swing,Angled_Shelves,Force_Double_Doors])

        #Left Angled Pull
        angled_door_l_pull = common_parts.add_drawer_pull(self)
        angled_door_l_pull.set_name("Left Door Pull")
        angled_door_l_pull.x_loc("Left_Depth",[Left_Depth])
        angled_door_l_pull.y_loc("Depth+PT",[Depth,PT])
        angled_door_l_pull.z_dim('PT',[PT])
        angled_door_l_pull.y_dim('IF(Force_Double_Doors,(sqrt((Width-Left_Depth-PT)**2+(Depth+Right_Depth+PT)**2)/2)-0.0015875,(sqrt((Width-Left_Depth-PT)**2+(Depth+Right_Depth+PT)**2)))*-1+PT',[Width,Left_Depth,Depth,Right_Depth,PT,Force_Double_Doors])       
        angled_door_l_pull.z_loc('IF(Pull_Type==0,IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)+Base_Pull_Location,IF(Pull_Type==1,Height-Tall_Pull_Location+World_Z,Height-Upper_Pull_Location))',[Door_Pull_Height,Pull_Type,Base_Pull_Location,Tall_Pull_Location,Upper_Pull_Location,Height,World_Z,Toe_Kick_Height,Shelf_Thickness,Is_Hanging,Panel_Height])
        angled_door_l_pull.x_rot(value = 0)
        angled_door_l_pull.y_rot(value = -90)
        angled_door_l_pull.z_rot('(atan((Width-Left_Depth)/(Depth+Right_Depth)))+3.14159-radians(Open*Rotation)',[Width,Depth,Right_Depth,Left_Depth,Open,Rotation])
        angled_door_l_pull.prompt('Hide','IF((Door and Angled_Shelves and Force_Double_Doors and Use_Left_Swing),False,IF((Door and Angled_Shelves and Force_Double_Doors),False,IF((Door and Angled_Shelves and Use_Left_Swing),True,IF((Door and Angled_Shelves),False,True))))',[Door,Use_Left_Swing,Angled_Shelves,Force_Double_Doors])
        
        #Right Angled Pull
        angled_door_r_pull = common_parts.add_drawer_pull(self)
        angled_door_r_pull.set_name("Right Door Pull")
        angled_door_r_pull.x_loc('Width-PT',[Width,PT])
        angled_door_r_pull.y_loc('-Right_Depth',[Right_Depth])
        angled_door_r_pull.z_dim('PT',[PT])
        angled_door_r_pull.y_dim('IF(Force_Double_Doors,(sqrt((Width-Left_Depth-PT)**2+(Depth+Right_Depth+PT)**2)/2)-0.0015875,(sqrt((Width-Left_Depth-PT)**2+(Depth+Right_Depth+PT)**2)))-PT',[Width,Left_Depth,Depth,Right_Depth,PT,Force_Double_Doors])
        angled_door_r_pull.z_loc('IF(Pull_Type==0,IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)+Base_Pull_Location,IF(Pull_Type==1,Height-Tall_Pull_Location+World_Z,Height-Upper_Pull_Location))',[Door_Pull_Height,Pull_Type,Base_Pull_Location,Tall_Pull_Location,Upper_Pull_Location,Height,World_Z,Toe_Kick_Height,Shelf_Thickness,Is_Hanging,Panel_Height])
        angled_door_r_pull.x_rot(value = 0)
        angled_door_r_pull.y_rot(value = -90)
        angled_door_r_pull.z_rot('(atan((Width-Left_Depth)/(Depth+Right_Depth)))+3.14159+radians(Open*Rotation)',[Width,Depth,Right_Depth,Left_Depth,Open,Rotation])
        angled_door_r_pull.prompt('Hide','IF((Door and Angled_Shelves and Force_Double_Doors and Use_Left_Swing),False,IF((Door and Angled_Shelves and Force_Double_Doors),False,IF((Door and Angled_Shelves and Use_Left_Swing),False,IF((Door and Angled_Shelves),True,True))))',[Door,Use_Left_Swing,Angled_Shelves,Force_Double_Doors])
          
        
        #L Reach Back Doors 
        l_door_reach_back_left = common_parts.add_door(self)
        l_door_reach_back_left.set_name("Left Door")
        l_door_reach_back_left.x_loc('Left_Depth',[Depth,Left_Depth])        
        l_door_reach_back_left.y_loc('Depth+(PT/2)',[Depth,PT])       
        l_door_reach_back_left.z_loc('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)',[Height,Panel_Height,Is_Hanging,Toe_Kick_Height,Shelf_Thickness])
        l_door_reach_back_left.x_rot(value = 0)
        l_door_reach_back_left.y_rot(value = -90)
        l_door_reach_back_left.z_rot("radians(180)-IF(DT==0,IF(Pull_Location==0,IF(Open<=Half,radians((Open*2)*Rotation),radians(Rotation)),IF(Open>Half,radians((Open-Half)*2*Rotation),0)),0)",[Pull_Location,Open,Rotation,DT,Half])
        l_door_reach_back_left.x_dim('Panel_Height-(Shelf_Thickness)',[Panel_Height,Shelf_Thickness])
        l_door_reach_back_left.y_dim('Depth+Right_Depth+(PT)',[Depth,Right_Depth,PT])
        l_door_reach_back_left.z_dim('PT',[PT])
        l_door_reach_back_left.prompt('Hide','IF(Angled_Shelves,True,IF(Door,IF(DT==0,False,True),True))',[Door,Angled_Shelves,DT])        

        l_door_reach_back_right = common_parts.add_door(self)
        l_door_reach_back_right.set_name("Right Door")
        l_door_reach_back_right.x_loc('Width-(PT/2)',[Width,PT])        
        l_door_reach_back_right.y_loc('-Right_Depth',[Right_Depth])       
        l_door_reach_back_right.z_loc('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)',[Height,Panel_Height,Is_Hanging,Toe_Kick_Height,Shelf_Thickness])
        l_door_reach_back_right.x_rot(value = 0)
        l_door_reach_back_right.y_rot(value = -90)
        l_door_reach_back_right.z_rot("radians(90)+IF(DT==0,IF(Pull_Location==1,IF(Open<=Half,radians((Open*2)*Rotation),radians(Rotation)),IF(Open>Half,radians((Open-Half)*2*Rotation),0)),0)",[Pull_Location,Open,Rotation,DT,Half])
        l_door_reach_back_right.x_dim('Panel_Height-(Shelf_Thickness)',[Panel_Height,Shelf_Thickness])
        l_door_reach_back_right.y_dim('Width-Left_Depth-(PT)-INCH(0.62)',[Width,Left_Depth,PT])
        l_door_reach_back_right.z_dim('PT',[PT])
        l_door_reach_back_right.prompt('Hide','IF(Angled_Shelves,True,IF(Door,IF(DT==0,False,True),True))',[Door,Angled_Shelves,DT])


        #L Doors Lazy Susan
        l_door_lazy_susan_left = common_parts.add_door(self)
        l_door_lazy_susan_left.set_name("Left Door")
        l_door_lazy_susan_left.x_loc('IF(Pull_Location==0,Left_Depth+IF(Open<Half,(Open*((Width-Left_Depth)*(1+(Open*2))-PT-INCH(0.25))),Open*((Width-Left_Depth)*(1+(Open*(3-(Open*2))))-PT-INCH(0.25))-PT*((Open-Half)*2))+PT,Left_Depth)',[Depth,Left_Depth,PT,Width,Open,Half,Pull_Location])        
        l_door_lazy_susan_left.y_loc('IF(Pull_Location==0,-Right_Depth-PT-(IF(Open<Half,Open*(Width-Left_Depth-(PT*2)-INCH(0.25))*2*(2-(2*Open)),Open*(Width-Left_Depth-(PT*2)-INCH(0.25))*2*(1-((Open-Half)*2))-PT*((Open-Half)*2))),Depth+(PT/2))',[Depth,PT,Open,Half,Width,Left_Depth,PT,Right_Depth,Pull_Location])       
        l_door_lazy_susan_left.z_loc('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)',[Height,Panel_Height,Is_Hanging,Toe_Kick_Height,Shelf_Thickness])
        l_door_lazy_susan_left.x_rot(value = 0)
        l_door_lazy_susan_left.y_rot(value = -90)
        l_door_lazy_susan_left.z_rot('IF(Pull_Location==0,(IF(Open>Half,((Open-Half)*2)*radians(45),0)),radians(180)-(Open*radians(180)))',[Open,Half,Pull_Location])
        l_door_lazy_susan_left.x_dim('Panel_Height-(Shelf_Thickness)',[Panel_Height,Shelf_Thickness])
        l_door_lazy_susan_left.y_dim('Depth+Right_Depth+(PT)+INCH(0.25)',[Depth,Right_Depth,PT])
        l_door_lazy_susan_left.z_dim('PT',[PT])
        l_door_lazy_susan_left.prompt('Hide','IF(Angled_Shelves,True,IF(Door,IF(DT==1,False,True),True))',[Door,DT,Angled_Shelves])        

        l_door_lazy_susan_right = common_parts.add_door(self)
        l_door_lazy_susan_right.set_name("Right Door")
        l_door_lazy_susan_right.x_loc('IF(Pull_Location==0,Width-(PT/2),Left_Depth+PT-(IF(Open<Half,Open*(Depth+Right_Depth+(PT*2))*2*(2-(2*Open)),Open*(Depth+Right_Depth+(PT*2))*2*(1-((Open-Half)*2))+PT*((Open-Half)*2))))',[Depth,PT,Open,Half,Width,Left_Depth,PT,Right_Depth,Pull_Location])
        l_door_lazy_susan_right.y_loc('IF(Pull_Location==0,-Right_Depth,-Right_Depth-PT+IF(Open<Half,(Open*(Depth+Right_Depth+PT-INCH(0.25))*(1+(Open*2))),Open*((Depth+Right_Depth+PT-INCH(0.25))*(1+(Open*(3-(Open*2)))))))',[Depth,Left_Depth,PT,Width,Open,Half,Pull_Location,Right_Depth])        
        l_door_lazy_susan_right.z_loc('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)',[Height,Panel_Height,Is_Hanging,Toe_Kick_Height,Shelf_Thickness])
        l_door_lazy_susan_right.x_rot(value = 0)
        l_door_lazy_susan_right.y_rot(value = -90)
        l_door_lazy_susan_right.z_rot('IF(Pull_Location==0,radians(90)+(Open*radians(180)),radians(-90)-IF(Open>Half,((Open-Half)*2)*radians(45),0))',[Open,Pull_Location,Half])
        l_door_lazy_susan_right.x_dim('Panel_Height-(Shelf_Thickness)',[Panel_Height,Shelf_Thickness])
        l_door_lazy_susan_right.y_dim('Width-Left_Depth-(PT)-INCH(0.25)',[Width,Left_Depth,PT])
        l_door_lazy_susan_right.z_dim('PT',[PT])
        l_door_lazy_susan_right.prompt('Hide','IF(Angled_Shelves,True,IF(Door,IF(DT==1,False,True),True))',[Door,DT,Angled_Shelves])


        #Left L Reachback Pull
        l_door_reachback_left_pull = common_parts.add_drawer_pull(self)
        l_door_reachback_left_pull.set_name("Left Door Pull")
        l_door_reachback_left_pull.x_loc('Left_Depth',[Left_Depth,PT,DT])      
        l_door_reachback_left_pull.y_loc('Depth-(PT/2)',[Depth,Right_Depth,DT,PT])
        l_door_reachback_left_pull.y_dim('Depth+Right_Depth+(PT)',[DT,Depth,Right_Depth,PT])
        l_door_reachback_left_pull.z_dim('PT',[DT,PT])
        l_door_reachback_left_pull.z_loc('IF(Pull_Type==0,IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)+Base_Pull_Location,IF(Pull_Type==1,Height-Tall_Pull_Location+World_Z,Height-Upper_Pull_Location))',[Door_Pull_Height,Pull_Type,Base_Pull_Location,Tall_Pull_Location,Upper_Pull_Location,Height,World_Z,Toe_Kick_Height,Shelf_Thickness,Is_Hanging,Panel_Height])
        l_door_reachback_left_pull.x_rot(value = 0)
        l_door_reachback_left_pull.y_rot(value = -90)
        l_door_reachback_left_pull.z_rot("radians(180)-IF(DT==0,IF(Pull_Location==0,IF(Open<=Half,radians((Open*2)*Rotation),radians(Rotation)),IF(Open>Half,radians((Open-Half)*2*Rotation),0)),0)",[Pull_Location,Open,Rotation,DT,Half])
        l_door_reachback_left_pull.prompt('Hide','IF(Pull_Location==1,True,IF(Angled_Shelves,True,IF(Door,IF(DT==0,False,True),True)))',[Door,Pull_Location,Angled_Shelves,DT])

        #Right L Reachback Pull
        l_door_reachback_right_pull = common_parts.add_drawer_pull(self)
        l_door_reachback_right_pull.set_name("Right Door Pull")
        l_door_reachback_right_pull.x_loc('Width',[Width,DT,Left_Depth,PT])        
        l_door_reachback_right_pull.y_loc('-Right_Depth',[Right_Depth])       
        l_door_reachback_right_pull.y_dim('Width-Left_Depth-(PT)-INCH(0.62)',[DT,Width,Left_Depth,PT])
        l_door_reachback_right_pull.z_dim('PT',[DT,PT])
        l_door_reachback_right_pull.z_loc('IF(Pull_Type==0,IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)+Base_Pull_Location,IF(Pull_Type==1,Height-Tall_Pull_Location+World_Z,Height-Upper_Pull_Location))',[Door_Pull_Height,Pull_Type,Base_Pull_Location,Tall_Pull_Location,Upper_Pull_Location,Height,World_Z,Toe_Kick_Height,Shelf_Thickness,Is_Hanging,Panel_Height])
        l_door_reachback_right_pull.x_rot(value = 0)
        l_door_reachback_right_pull.y_rot(value = -90)
        l_door_reachback_right_pull.z_rot("radians(90)+IF(DT==0,IF(Pull_Location==1,IF(Open<=Half,radians((Open*2)*Rotation),radians(Rotation)),IF(Open>Half,radians((Open-Half)*2*Rotation),0)),0)",[Pull_Location,Open,Rotation,DT,Half])
        l_door_reachback_right_pull.prompt('Hide','IF(Pull_Location==0,True,IF(Angled_Shelves,True,IF(Door,IF(DT==0,False,True),True)))',[Door,Pull_Location,Angled_Shelves,DT])

        #L Lazy Susan Left Pull
        l_door_lazy_susan_left_pull = common_parts.add_drawer_pull(self)
        l_door_lazy_susan_left_pull.set_name("Left Door Pull")
        l_door_lazy_susan_left_pull.x_loc('Left_Depth+IF(Open<Half,(Open*((Width-Left_Depth)*(1+(Open*2))-PT-INCH(0.25))),Open*((Width-Left_Depth)*(1+(Open*(3-(Open*2))))-PT-INCH(0.25))-PT*((Open-Half)*2))+PT',[Depth,Left_Depth,PT,Width,Open,Half,Pull_Location])        
        l_door_lazy_susan_left_pull.y_loc('-Right_Depth+(PT/2)-(IF(Open<Half,Open*(Width-Left_Depth-(PT*2)-INCH(0.25))*2*(2-(2*Open)),Open*(Width-Left_Depth-(PT*2)-INCH(0.25))*2*(1-((Open-Half)*2))-PT*((Open-Half)*2)))',[Depth,PT,Open,Half,Width,Left_Depth,PT,Right_Depth,Pull_Location])       
        l_door_lazy_susan_left_pull.y_dim('(Depth+Right_Depth+(PT)+INCH(0.25))*-1',[Depth,Right_Depth,PT])
        l_door_lazy_susan_left_pull.z_dim('IF(Open>Half,-PT*((Open-Half)*2),0)',[PT,Open,Half])
        l_door_lazy_susan_left_pull.z_loc('IF(Pull_Type==0,IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)+Base_Pull_Location,IF(Pull_Type==1,Height-Tall_Pull_Location+World_Z,Height-Upper_Pull_Location))',[Door_Pull_Height,Pull_Type,Base_Pull_Location,Tall_Pull_Location,Upper_Pull_Location,Height,World_Z,Toe_Kick_Height,Shelf_Thickness,Is_Hanging,Panel_Height])
        l_door_lazy_susan_left_pull.x_rot(value = 0)
        l_door_lazy_susan_left_pull.y_rot(value = -90)
        l_door_lazy_susan_left_pull.z_rot('radians(180)+IF(Open>Half,((Open-Half)*2)*radians(45),0)',[Open,Half,Pull_Location])
        l_door_lazy_susan_left_pull.prompt('Hide','IF(Pull_Location==1,True,IF(Angled_Shelves,True,IF(Door,IF(DT==1,False,True),True)))',[Door,Pull_Location,Angled_Shelves,DT])

        #L Lazy Suasan Right Pull
        l_door_lazy_susan_right_pull = common_parts.add_drawer_pull(self)
        l_door_lazy_susan_right_pull.set_name("Right Door Pull")
        l_door_lazy_susan_right_pull.x_loc('Left_Depth-(IF(Open<Half,Open*(Depth+Right_Depth+(PT*2))*2*(2-(2*Open)),Open*(Depth+Right_Depth+(PT*2))*2*(1-((Open-Half)*2))+PT*((Open-Half)*2)))',[Depth,PT,Open,Half,Width,Left_Depth,PT,Right_Depth,Pull_Location])
        l_door_lazy_susan_right_pull.y_loc('-Right_Depth-PT+IF(Open<Half,(Open*(Depth+Right_Depth+PT-INCH(0.25))*(1+(Open*2))),Open*((Depth+Right_Depth+PT-INCH(0.25))*(1+(Open*(3-(Open*2))))))',[Depth,Left_Depth,PT,Width,Open,Half,Pull_Location,Right_Depth])        
        l_door_lazy_susan_right_pull.y_dim('(Width-Left_Depth-(PT)-INCH(0.25))*-1',[Width,Left_Depth,PT])
        l_door_lazy_susan_right_pull.z_dim('IF(Open>Half,-PT*((Open-Half)*1.5),0)',[PT,Open,Half])
        l_door_lazy_susan_right_pull.z_loc('IF(Pull_Type==0,IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+(Shelf_Thickness/2)+Base_Pull_Location,IF(Pull_Type==1,Height-Tall_Pull_Location+World_Z,Height-Upper_Pull_Location))',[Door_Pull_Height,Pull_Type,Base_Pull_Location,Tall_Pull_Location,Upper_Pull_Location,Height,World_Z,Toe_Kick_Height,Shelf_Thickness,Is_Hanging,Panel_Height])
        l_door_lazy_susan_right_pull.x_rot(value = 0)
        l_door_lazy_susan_right_pull.y_rot(value = -90)
        l_door_lazy_susan_right_pull.z_rot('radians(90)-IF(Open>Half,((Open-Half)*2)*radians(45),0)',[Open,Pull_Location,Half])
        l_door_lazy_susan_right_pull.prompt('Hide','IF(Pull_Location==0,True,IF(Angled_Shelves,True,IF(Door,IF(DT==1,False,True),True)))',[Door,Pull_Location,Angled_Shelves,DT])



        #Shelves
        #Angled Shelves
        previous_angled_shelf = None
        previous_l_shelf = None
        for i in range(1,11):
            Shelf_Height = self.get_var("Shelf " + str(i) + " Height",'Shelf_Height')

            shelf_angled = common_parts.add_angle_shelf(self)

            if previous_angled_shelf:
                prev_shelf_z_loc = previous_angled_shelf.get_var('loc_z','prev_shelf_z_loc')
                shelf_angled.z_loc('prev_shelf_z_loc+Shelf_Height',[prev_shelf_z_loc,Shelf_Height])
            else:
                shelf_angled.z_loc('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+Shelf_Height+Shelf_Thickness',
                                    [Shelf_Height,Is_Hanging,Toe_Kick_Height,Shelf_Thickness,Panel_Height,Height])                           

            shelf_angled.x_loc('IF(Add_Backing,IF(Backing_Thickness==0,INCH(0.25),INCH(0.75)),0)',[Add_Backing,Backing_Thickness])
            shelf_angled.y_loc('IF(Add_Backing,IF(Backing_Thickness==0,-INCH(0.25),-INCH(0.75)),0)',[Add_Backing,Backing_Thickness])
            shelf_angled.x_rot(value = 0)
            shelf_angled.y_rot(value = 0)
            shelf_angled.z_rot(value = 0)
            shelf_angled.x_dim('Width-PT-IF(Add_Backing,IF(Backing_Thickness==0,INCH(0.25),INCH(0.75)),0)',[Width,PT,Add_Backing,Backing_Thickness])
            shelf_angled.y_dim('Depth+PT+IF(Add_Backing,IF(Backing_Thickness==0,INCH(0.25),INCH(0.75)),0)',[Depth,PT,Add_Backing,Backing_Thickness])
            shelf_angled.z_dim('Shelf_Thickness',[Shelf_Thickness])
            shelf_angled.prompt('Left Depth','Left_Depth-IF(Add_Backing,IF(Backing_Thickness==0,INCH(0.25),INCH(0.75)),0)',[Left_Depth,Add_Backing,Backing_Thickness])
            shelf_angled.prompt('Right Depth','Right_Depth-IF(Add_Backing,IF(Backing_Thickness==0,INCH(0.25),INCH(0.75)),0)',[Right_Depth,Add_Backing,Backing_Thickness])
            shelf_angled.prompt('Hide','IF(Angled_Shelves,IF(Shelf_Quantity+1>'+str(i)+',False,True),True)',[Shelf_Quantity,Angled_Shelves])

            previous_angled_shelf = shelf_angled

            l_shelf = common_parts.add_l_shelf(self)
            if previous_l_shelf:
                prev_shelf_z_loc = previous_l_shelf.get_var('loc_z','prev_shelf_z_loc')
                l_shelf.z_loc('prev_shelf_z_loc+Shelf_Height',[prev_shelf_z_loc,Shelf_Height])
            else:
                l_shelf.z_loc('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)+Shelf_Height',
                              [Shelf_Height,Is_Hanging,Toe_Kick_Height,Shelf_Thickness,Height,Panel_Height])

            l_shelf.x_loc('IF(Add_Backing,IF(Backing_Thickness==0,INCH(0.25),INCH(0.75)),0)',[Add_Backing,Backing_Thickness])
            l_shelf.y_loc('IF(Add_Backing,IF(Backing_Thickness==0,-INCH(0.25),-INCH(0.75)),0)',[Add_Backing,Backing_Thickness])
            l_shelf.x_rot(value = 0)
            l_shelf.y_rot(value = 0)
            l_shelf.z_rot(value = 0)
            l_shelf.x_dim('Width-PT-IF(Add_Backing,IF(Backing_Thickness==0,INCH(0.25),INCH(0.75)),0)',[Width,PT,Add_Backing,Backing_Thickness])
            l_shelf.y_dim('Depth+PT+IF(Add_Backing,IF(Backing_Thickness==0,INCH(0.25),INCH(0.75)),0)',[Depth,PT,Add_Backing,Backing_Thickness])
            l_shelf.z_dim('Shelf_Thickness',[Shelf_Thickness])
            l_shelf.prompt('Left Depth','Left_Depth-IF(Add_Backing,IF(Backing_Thickness==0,INCH(0.25),INCH(0.75)),0)',[Left_Depth,Add_Backing,Backing_Thickness])
            l_shelf.prompt('Right Depth','Right_Depth-IF(Add_Backing,IF(Backing_Thickness==0,INCH(0.25),INCH(0.75)),0)',[Right_Depth,Add_Backing,Backing_Thickness])
            l_shelf.prompt('Hide','IF(Angled_Shelves,True,IF(Shelf_Quantity+1>'+str(i)+',False,True))',[Angled_Shelves,Shelf_Quantity])

            previous_l_shelf = l_shelf               

        self.update()


class Corner_L_Shelves(fd_types.Assembly):

    """
    This L Shelf Includes a Full Back for support and is floor mounted first
    """

    library_name = "Closets By Design"
    category_name = "Corner Units"
    type_assembly = "PRODUCT"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".corner_shelves"
    placement_type = 'Corner'
    # drop_id = "cbddrop.place_corner_l_shelves"

    def draw(self):
        self.create_assembly()
        
        props = props_closet.get_scene_props()
        
        self.add_tab(name='L Shelf Options',tab_type='VISIBLE')
        self.add_tab(name='Material Thickness',tab_type='HIDDEN')
        self.add_prompt(name="Panel Height",prompt_type='DISTANCE',value=unit.millimeter(float(props.closet_defaults.panel_height)),tab_index=0)
        self.add_prompt(name="Left Depth",prompt_type='DISTANCE',value=unit.inch(12),tab_index=0)       
        self.add_prompt(name="Right Depth",prompt_type='DISTANCE',value=unit.inch(12),tab_index=0)  
        self.add_prompt(name="Shelf Quantity",prompt_type='QUANTITY',value=3,tab_index=0)  
        self.add_prompt(name="Add Backing",prompt_type='CHECKBOX',value=False,tab_index=1,export=True)
        self.add_prompt(name="Is Hanging",prompt_type='CHECKBOX',value=False,tab_index=1,export=True)
        self.add_prompt(name="Remove Left Side",prompt_type='CHECKBOX',value=False,tab_index=1,export=True)
        self.add_prompt(name="Remove Right Side",prompt_type='CHECKBOX',value=False,tab_index=1,export=True)
        
        common_prompts.add_toe_kick_prompts(self)
        common_prompts.add_thickness_prompts(self)
        
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Panel_Height = self.get_var('Panel Height')
        Left_Depth = self.get_var('Left Depth')
        Right_Depth = self.get_var('Right Depth')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        Panel_Thickness = self.get_var('Panel Thickness')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Toe_Kick_Setback = self.get_var('Toe Kick Setback')
        Shelf_Quantity = self.get_var('Shelf Quantity')
        Add_Backing = self.get_var('Add Backing')
        Back_Thickness = self.get_var('Back Thickness')
        Is_Hanging = self.get_var('Is Hanging')
        RLS = self.get_var('Remove Left Side',"RLS")
        RRS = self.get_var('Remove Right Side',"RRS")
        
        inside_height_empty = self.add_empty()
        inside_height_empty.z_loc('IF(Is_Hanging,Panel_Height-(Shelf_Thickness*2)-(Shelf_Thickness*Shelf_Quantity),Height-Toe_Kick_Height-(Shelf_Thickness*2)-(Shelf_Thickness*Shelf_Quantity))',[Panel_Height,Is_Hanging,Height,Toe_Kick_Height,Shelf_Thickness,Shelf_Quantity])
        Inside_Height = inside_height_empty.get_var('loc_z','Inside_Height')
        
        top = common_parts.add_l_shelf(self)
        top.x_loc('IF(Add_Backing,Back_Thickness,0)',[Add_Backing,Back_Thickness])
        top.y_loc('-Panel_Thickness',[Add_Backing,Back_Thickness,Panel_Thickness])
        top.z_loc('Height',[Height])
        top.x_rot(value = 0)
        top.y_rot(value = 0)
        top.z_rot(value = 0)
        top.x_dim('IF(RRS,Width,Width-Panel_Thickness)',[RRS,Width,Panel_Thickness])
        top.y_dim('IF(RLS,Depth+Panel_Thickness,Depth+(Panel_Thickness*2))',[RLS,Depth,Panel_Thickness])
        top.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        top.prompt('Left Depth','Left_Depth',[Left_Depth])
        top.prompt('Right Depth','Right_Depth-Panel_Thickness',[Right_Depth,Panel_Thickness])
        
        bottom = common_parts.add_l_shelf(self)
        bottom.x_loc('IF(Add_Backing,Back_Thickness,0)',[Add_Backing,Back_Thickness])
        bottom.y_loc('-Panel_Thickness',[Add_Backing,Back_Thickness,Panel_Thickness])
        bottom.z_loc('IF(Is_Hanging,Height-Panel_Height,Toe_Kick_Height)',[Is_Hanging,Height,Panel_Height,Toe_Kick_Height])
        bottom.x_rot(value = 0)
        bottom.y_rot(value = 0)
        bottom.z_rot(value = 0)
        bottom.x_dim('IF(RRS,Width,Width-Panel_Thickness)',[RRS,Width,Panel_Thickness])
        bottom.y_dim('IF(RLS,Depth+Panel_Thickness,Depth+(Panel_Thickness*2))',[RLS,Depth,Panel_Thickness])
        bottom.z_dim('Shelf_Thickness',[Shelf_Thickness])
        bottom.prompt('Left Depth','Left_Depth',[Left_Depth])
        bottom.prompt('Right Depth','Right_Depth-Panel_Thickness',[Right_Depth,Panel_Thickness])
        
        shelf = common_parts.add_l_shelf(self)
        shelf.x_loc('IF(Add_Backing,Back_Thickness,0)',[Add_Backing,Back_Thickness])
        shelf.y_loc('-Shelf_Thickness',[Shelf_Thickness,Add_Backing,Back_Thickness])
        shelf.z_loc('IF(Is_Hanging,Height-Panel_Height+Shelf_Thickness+(Inside_Height/(Shelf_Quantity+1)),Toe_Kick_Height+Shelf_Thickness+(Inside_Height/(Shelf_Quantity+1)))',[Is_Hanging,Panel_Height,Height,Inside_Height,Toe_Kick_Height,Shelf_Thickness,Shelf_Quantity])
        shelf.x_rot(value = 0)
        shelf.y_rot(value = 0)
        shelf.z_rot(value = 0)
        shelf.x_dim('IF(RRS,Width,Width-Panel_Thickness)',[RRS,Width,Panel_Thickness])
        shelf.y_dim('IF(RLS,Depth+Panel_Thickness,Depth+(Panel_Thickness*2))',[RLS,Depth,Panel_Thickness])
        shelf.z_dim('Shelf_Thickness',[Shelf_Thickness])
        shelf.prompt('Left Depth','Left_Depth',[Left_Depth])
        shelf.prompt('Right Depth','Right_Depth-Shelf_Thickness',[Right_Depth,Shelf_Thickness])
        shelf.prompt('Hide','IF(Shelf_Quantity==0,True,False)',[Shelf_Quantity])
        shelf.prompt('Z Quantity','Shelf_Quantity',[Shelf_Quantity])
        shelf.prompt('Z Offset','(Inside_Height/(Shelf_Quantity+1))+Shelf_Thickness',[Inside_Height,Shelf_Quantity,Shelf_Thickness])
        
        left_panel = common_parts.add_panel(self)
        left_panel.set_name("Left Panel")
        left_panel.x_loc('IF(Add_Backing,Back_Thickness,0)',[Add_Backing,Back_Thickness])
        left_panel.y_loc('Depth',[Depth,Add_Backing,Back_Thickness])
        left_panel.z_loc('IF(Is_Hanging,Height-Panel_Height,0)',[Height,Panel_Height,Is_Hanging])
        left_panel.x_rot(value = 0)
        left_panel.y_rot(value = -90)
        left_panel.z_rot(value = -90)
        left_panel.x_dim('IF(Is_Hanging,Panel_Height,Height)',[Is_Hanging,Panel_Height,Height])
        left_panel.y_dim('Left_Depth',[Left_Depth])
        left_panel.z_dim(value = unit.inch(.75))
        left_panel.prompt('Hide','IF(RLS,True,False)',[RLS])
        left_panel.prompt('Right Depth','Left_Depth',[Left_Depth]) #USED FOR DRILLING
        
        right_panel = common_parts.add_panel(self)
        right_panel.x_loc('Width+IF(Add_Backing,Back_Thickness,0)',[Width,Add_Backing,Back_Thickness])
        right_panel.y_loc(value = 0)
        right_panel.z_loc('IF(Is_Hanging,Height-Panel_Height,0)',[Height,Panel_Height,Is_Hanging])
        right_panel.x_rot(value = 0)
        right_panel.y_rot(value = -90)
        right_panel.z_rot(value = 180)
        right_panel.x_dim('IF(Is_Hanging,Panel_Height,Height)',[Is_Hanging,Panel_Height,Height])
        right_panel.y_dim('Right_Depth',[Right_Depth])
        right_panel.z_dim(value = unit.inch(-.75))
        right_panel.prompt('Hide','IF(RRS,True,False)',[RRS])
        right_panel.prompt('Left Depth','Right_Depth',[Right_Depth]) #USED FOR DRILLING
        
        wall_panel = common_parts.add_panel(self)
        wall_panel.set_name("Wall Panel")
        wall_panel.x_loc('IF(Add_Backing,Back_Thickness,0)',[Add_Backing,Back_Thickness])
        wall_panel.y_loc(value = 0)
        wall_panel.z_loc('IF(Is_Hanging,Height-Panel_Height,0)',[Height,Panel_Height,Is_Hanging])
        wall_panel.x_rot(value = 0)
        wall_panel.y_rot(value = -90)
        wall_panel.z_rot(value = -90)
        wall_panel.x_dim('IF(Is_Hanging,Panel_Height,Height)',[Is_Hanging,Panel_Height,Height])
        wall_panel.y_dim('IF(RRS,Width,Width-Panel_Thickness)',[RRS,Width,Panel_Thickness])
        wall_panel.z_dim(value = unit.inch(-.75))
        wall_panel.prompt('Right Depth','Width-Panel_Thickness',[Width,Panel_Thickness]) #USED FOR DRILLING
        
        back = common_parts.add_back(self)
        back.x_loc(value = 0)
        back.y_loc(value = 0)
        back.z_loc('IF(Is_Hanging,Height-Panel_Height,0)',[Height,Panel_Height,Is_Hanging])
        back.x_rot(value = 0)
        back.y_rot(value = -90)
        back.z_rot(value = -180)
        back.x_dim('IF(Is_Hanging,Panel_Height,Height)',[Is_Hanging,Panel_Height,Height])
        back.y_dim('fabs(Depth)',[Depth])
        back.z_dim('Back_Thickness',[Back_Thickness])
        back.prompt('Hide','IF(Add_Backing,False,True)',[Add_Backing])
        
        left_kick = common_parts.add_toe_kick(self)
        left_kick.x_loc('Left_Depth-Toe_Kick_Setback+IF(Add_Backing,Back_Thickness,0)',[Left_Depth,Toe_Kick_Setback,Add_Backing,Back_Thickness])
        left_kick.y_loc('Depth+Panel_Thickness',[Depth,Panel_Thickness,Add_Backing,Back_Thickness])
        left_kick.z_loc(value = 0)
        left_kick.x_rot(value = 90)
        left_kick.y_rot(value = 0)
        left_kick.z_rot(value = -90)
        left_kick.x_dim('Depth+Right_Depth-Toe_Kick_Setback',[Depth,Right_Depth,Toe_Kick_Setback])
        left_kick.y_dim('Toe_Kick_Height',[Toe_Kick_Height])
        left_kick.z_dim(value = unit.inch(.75))
        left_kick.prompt('Hide','IF(Is_Hanging,True,False)',[Is_Hanging])
        
        right_kick = common_parts.add_toe_kick(self)
        right_kick.x_loc('Width-Panel_Thickness',[Width,Panel_Thickness,Add_Backing,Back_Thickness])
        right_kick.y_loc('-Right_Depth+Toe_Kick_Setback',[Right_Depth,Toe_Kick_Setback,Add_Backing,Back_Thickness])
        right_kick.z_loc(value = 0)
        right_kick.x_rot(value = 90)
        right_kick.y_rot(value = 0)
        right_kick.z_rot(value = 180)
        right_kick.x_dim('Width-Left_Depth+Toe_Kick_Setback-Shelf_Thickness',[Width,Left_Depth,Toe_Kick_Setback,Shelf_Thickness])
        right_kick.y_dim('Toe_Kick_Height',[Toe_Kick_Height])
        right_kick.z_dim(value = unit.inch(.75))
        right_kick.prompt('Hide','IF(Is_Hanging,True,False)',[Is_Hanging])
        
        self.update()


class Corner_Angle_Shelves(fd_types.Assembly):

    library_name = "Closets By Design"
    category_name = "Corner Units"
    type_assembly = "PRODUCT"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".outside_corner_angle_shelves"
    placement_type = 'Corner'
    # drop_id = "cbddrop.place_corner_l_shelves"

    def draw(self):
        self.create_assembly()
        
        self.add_tab(name='Angle Shelf Options',tab_type='VISIBLE')
        self.add_tab(name='Material Thickness',tab_type='HIDDEN')
        self.add_prompt(name="Left Depth",prompt_type='DISTANCE',value=unit.inch(12),tab_index=0)       
        self.add_prompt(name="Right Depth",prompt_type='DISTANCE',value=unit.inch(12),tab_index=0)
        self.add_prompt(name="Shelf Quantity",prompt_type='QUANTITY',value=3,tab_index=0)
        common_prompts.add_toe_kick_prompts(self)
        common_prompts.add_thickness_prompts(self)
        
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Left_Depth = self.get_var('Left Depth')
        Right_Depth = self.get_var('Right Depth')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        Panel_Thickness = self.get_var('Panel Thickness')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Toe_Kick_Setback = self.get_var('Toe Kick Setback')
        Shelf_Quantity = self.get_var('Shelf Quantity')

        self.x_dim('fabs(Depth)',[Depth])
        
        shelf_inside_height_empty = self.add_empty()
        shelf_inside_height_empty.z_loc('Height-(Shelf_Thickness*2)-Toe_Kick_Height-(Shelf_Thickness*Shelf_Quantity)',[Height,Toe_Kick_Height,Shelf_Thickness,Shelf_Quantity])
        Shelf_Inside_Height = shelf_inside_height_empty.get_var('loc_z','Shelf_Inside_Height')                      
        
        top = common_parts.add_angle_shelf(self)
        top.x_loc('+Shelf_Thickness',[Shelf_Thickness])
        top.y_loc('-Shelf_Thickness',[Shelf_Thickness])
        top.z_loc('Height',[Height])
        top.x_rot(value = 0)
        top.y_rot(value = 0)
        top.z_rot(value = 0)
        top.x_dim('Width-(Panel_Thickness*3)',[Width,Panel_Thickness])
        top.y_dim('Depth+(Panel_Thickness*3)',[Depth,Panel_Thickness])
        top.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        top.prompt('Left Depth','Left_Depth',[Left_Depth])
        top.prompt('Right Depth','Right_Depth',[Right_Depth])
        
        bottom = common_parts.add_angle_shelf(self)
        bottom.x_loc('+Shelf_Thickness',[Shelf_Thickness])
        bottom.y_loc('-Shelf_Thickness',[Shelf_Thickness])
        bottom.z_loc('Toe_Kick_Height',[Toe_Kick_Height])
        bottom.x_rot(value = 0)
        bottom.y_rot(value = 0)
        bottom.z_rot(value = 0)
        bottom.x_dim('Width-(Panel_Thickness*3)',[Width,Panel_Thickness])
        bottom.y_dim('Depth+(Panel_Thickness*3)',[Depth,Panel_Thickness])
        bottom.z_dim('Shelf_Thickness',[Shelf_Thickness])
        bottom.prompt('Left Depth','Left_Depth',[Left_Depth])
        bottom.prompt('Right Depth','Right_Depth',[Right_Depth])
        
        shelf = common_parts.add_angle_shelf(self)
        shelf.x_loc('Shelf_Thickness',[Shelf_Thickness])
        shelf.y_loc('-Shelf_Thickness',[Shelf_Thickness])
        shelf.z_loc('Toe_Kick_Height+Shelf_Thickness+(Shelf_Inside_Height/(Shelf_Quantity+1))',[Height,Shelf_Inside_Height,Toe_Kick_Height,Shelf_Thickness,Shelf_Quantity])
        shelf.x_rot(value = 0)
        shelf.y_rot(value = 0)
        shelf.z_rot(value = 0)
        shelf.x_dim('Width-(Panel_Thickness*3)',[Width,Panel_Thickness])
        shelf.y_dim('Depth+(Panel_Thickness*3)',[Depth,Panel_Thickness])
        shelf.z_dim('Shelf_Thickness',[Shelf_Thickness])
        shelf.prompt('Left Depth','Left_Depth',[Left_Depth])
        shelf.prompt('Right Depth','Right_Depth',[Right_Depth,Shelf_Thickness])
        shelf.prompt('Hide','IF(Shelf_Quantity>0,False,True)',[Shelf_Quantity])
        shelf.prompt('Z Quantity','Shelf_Quantity',[Shelf_Quantity])
        shelf.prompt('Z Offset','(Shelf_Inside_Height/(Shelf_Quantity+1))+Shelf_Thickness',[Shelf_Inside_Height,Shelf_Quantity,Shelf_Thickness])  
        
        wall_panel = common_parts.add_panel(self)
        wall_panel.set_name("Wall Panel")
        wall_panel.x_loc(value = 0)
        wall_panel.y_loc(value = 0)
        wall_panel.z_loc(value = 0)
        wall_panel.x_rot(value = 0)
        wall_panel.y_rot(value = -90)
        wall_panel.z_rot(value = -90)
        wall_panel.x_dim('Height',[Height])
        wall_panel.y_dim('Width-Panel_Thickness',[Width,Panel_Thickness])
        wall_panel.z_dim(value = unit.inch(-.75))
        wall_panel.prompt('Right Depth','Width-Panel_Thickness',[Width,Panel_Thickness]) #USED FOR DRILLING
        
        wall_pane2 = common_parts.add_panel(self)
        wall_pane2.set_name("Wall Panel")
        wall_pane2.x_loc(value = 0)
        wall_pane2.y_loc(value = 0)
        wall_pane2.z_loc(value = 0)
        wall_pane2.x_rot(value = 0)
        wall_pane2.y_rot(value = -90)
        wall_pane2.z_rot(value = 0)
        wall_pane2.x_dim('Height',[Height])
        wall_pane2.y_dim('Depth+Panel_Thickness',[Depth,Panel_Thickness])
        wall_pane2.z_dim(value = unit.inch(-.75))
        wall_pane2.prompt('Right Depth','fabs(Depth)-Panel_Thickness',[Depth,Panel_Thickness]) #USED FOR DRILLING
        
        toe_kick = common_parts.add_toe_kick(self)
        toe_kick.x_loc('Left_Depth-(Toe_Kick_Setback/1.5)',[Left_Depth,Toe_Kick_Setback])
        toe_kick.y_loc('Depth+Panel_Thickness+(Toe_Kick_Setback/1.5)',[Depth,Panel_Thickness,Toe_Kick_Setback])
        toe_kick.z_loc(value = 0)
        toe_kick.x_rot(value = 90)
        toe_kick.y_rot(value = 0)
        toe_kick.z_rot('atan((fabs(Depth)-Panel_Thickness-Right_Depth)/(fabs(Width)-Panel_Thickness-Left_Depth))',[Depth,Panel_Thickness,Right_Depth,Width,Panel_Thickness,Left_Depth])
        toe_kick.x_dim('sqrt(((fabs(Depth)-Panel_Thickness-Right_Depth)**2)+((fabs(Width)-Panel_Thickness-Left_Depth)**2))',[Depth,Panel_Thickness,Right_Depth,Width,Panel_Thickness,Left_Depth])
        toe_kick.y_dim('Toe_Kick_Height',[Toe_Kick_Height])
        toe_kick.z_dim(value = unit.inch(.75))
        
        left_side = common_parts.add_panel(self)
        left_side.set_name("Left Side")
        left_side.x_loc('+Panel_Thickness',[Width,Panel_Thickness])
        left_side.y_loc('Depth+(Panel_Thickness*2)',[Depth,Panel_Thickness])
        left_side.z_loc(value = 0)
        left_side.x_rot(value = -90)
        left_side.y_rot(value = -90)
        left_side.z_rot(value = 0)
        left_side.x_dim('Height',[Height])
        left_side.y_dim('Left_Depth',[Width,Left_Depth,Toe_Kick_Setback,Panel_Thickness])
        left_side.z_dim(value = unit.inch(-.75)) 
        left_side.prompt('Right Depth','Left_Depth',[Left_Depth]) #USED FOR DRILLING
        
        right_side = common_parts.add_panel(self)
        right_side.set_name("Right Side")
        right_side.x_loc('Width-Panel_Thickness',[Width,Panel_Thickness])
        right_side.y_loc('-Panel_Thickness',[Depth,Panel_Thickness])
        right_side.z_loc(value = 0)
        right_side.x_rot(value = -180)
        right_side.y_rot(value = -90)
        right_side.z_rot(value = 0)
        right_side.x_dim('Height',[Height])
        right_side.y_dim('Right_Depth',[Depth,Right_Depth,Toe_Kick_Setback,Panel_Thickness])
        right_side.z_dim(value = unit.inch(-.75))
        right_side.prompt('Left Depth','Right_Depth',[Right_Depth]) #USED FOR DRILLING
        
        self.update() 
        
        
class Corner_Triangle_Shelves(fd_types.Assembly):

    library_name = "Closets By Design"
    category_name = "Corner Units"
    type_assembly = "PRODUCT"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".outside_corner_shelves"
    placement_type = 'Corner'
    # drop_id = "cbddrop.place_corner_l_shelves"

    def draw(self):
        self.create_assembly()
        
        self.add_tab(name='Angle Shelf Options',tab_type='VISIBLE')
        self.add_tab(name='Material Thickness',tab_type='HIDDEN')
        self.add_prompt(name="Left Depth",prompt_type='DISTANCE',value=unit.inch(12),tab_index=0)       
        self.add_prompt(name="Right Depth",prompt_type='DISTANCE',value=unit.inch(12),tab_index=0)  
        self.add_prompt(name="Shelf Quantity",prompt_type='QUANTITY',value=3,tab_index=0) 
 
        common_prompts.add_toe_kick_prompts(self)
        common_prompts.add_thickness_prompts(self)
        
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Left_Depth = self.get_var('Left Depth')
        Right_Depth = self.get_var('Right Depth')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        Panel_Thickness = self.get_var('Panel Thickness')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Toe_Kick_Setback = self.get_var('Toe Kick Setback')
        Shelf_Quantity = self.get_var('Shelf Quantity')

        self.x_dim('fabs(Depth)',[Depth])
        
        inside_height_empty = self.add_empty()
        inside_height_empty.z_loc('Height-Toe_Kick_Height-(Shelf_Thickness*2)-(Shelf_Thickness*Shelf_Quantity)',[Height,Toe_Kick_Height,Shelf_Thickness,Shelf_Quantity])
        Inside_Height = inside_height_empty.get_var('loc_z','Inside_Height')
        
        top = common_parts.add_angle_shelf(self)
        top.x_loc('Panel_Thickness',[Panel_Thickness])
        top.y_loc('-Panel_Thickness',[Panel_Thickness])
        top.z_loc('Height',[Height])
        top.x_rot(value = 0)
        top.y_rot(value = 0)
        top.z_rot(value = 0)
        top.x_dim('Width-(Panel_Thickness*2)',[Width,Panel_Thickness])
        top.y_dim('Depth+(Panel_Thickness*2)',[Depth,Panel_Thickness])
        top.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        top.prompt('Left Depth',value = 0)
        top.prompt('Right Depth',value = 0)
        
        bottom = common_parts.add_angle_shelf(self)
        bottom.x_loc('Panel_Thickness',[Panel_Thickness])
        bottom.y_loc('-Panel_Thickness',[Panel_Thickness])
        bottom.z_loc('Toe_Kick_Height',[Toe_Kick_Height])
        bottom.x_rot(value = 0)
        bottom.y_rot(value = 0)
        bottom.z_rot(value = 0)
        bottom.x_dim('Width-(Panel_Thickness*2)',[Width,Panel_Thickness])
        bottom.y_dim('Depth+(Panel_Thickness*2)',[Depth,Panel_Thickness])
        bottom.z_dim('Shelf_Thickness',[Shelf_Thickness])
        bottom.prompt('Left Depth',value = 0)
        bottom.prompt('Right Depth',value = 0)
        
        shelf = common_parts.add_angle_shelf(self)
        shelf.x_loc('Panel_Thickness',[Panel_Thickness])
        shelf.y_loc('-Panel_Thickness',[Panel_Thickness])
        shelf.z_loc('Toe_Kick_Height+Shelf_Thickness+(Inside_Height/(Shelf_Quantity+1))',[Height,Inside_Height,Toe_Kick_Height,Shelf_Thickness,Shelf_Quantity])
        shelf.x_rot(value = 0)
        shelf.y_rot(value = 0)
        shelf.z_rot(value = 0)
        shelf.x_dim('Width-(Panel_Thickness*2)',[Width,Panel_Thickness])
        shelf.y_dim('Depth+(Panel_Thickness*2)',[Depth,Panel_Thickness])
        shelf.z_dim('Shelf_Thickness',[Shelf_Thickness])
        shelf.prompt('Left Depth',value = 0)
        shelf.prompt('Right Depth',value = 0)
        shelf.prompt('Hide','IF(Shelf_Quantity==0,True,False)',[Shelf_Quantity])
        shelf.prompt('Z Quantity','Shelf_Quantity',[Shelf_Quantity])
        shelf.prompt('Z Offset','(Inside_Height/(Shelf_Quantity+1))+Shelf_Thickness',[Inside_Height,Shelf_Quantity,Shelf_Thickness])
        
        wall_panel = common_parts.add_panel(self)
        wall_panel.set_name("Wall Panel")
        wall_panel.x_loc(value = 0)
        wall_panel.y_loc(value = 0)
        wall_panel.z_loc(value = 0)
        wall_panel.x_rot(value = 0)
        wall_panel.y_rot(value = -90)
        wall_panel.z_rot(value = -90)
        wall_panel.x_dim('Height',[Height])
        wall_panel.y_dim('Width-Panel_Thickness',[Width,Panel_Thickness])
        wall_panel.z_dim(value = unit.inch(-.75))
        
        wall_pane2 = common_parts.add_panel(self)
        wall_pane2.set_name("Wall Panel")
        wall_pane2.x_loc(value = 0)
        wall_pane2.y_loc(value = 0)
        wall_pane2.z_loc(value = 0)
        wall_pane2.x_rot(value = 0)
        wall_pane2.y_rot(value = -90)
        wall_pane2.z_rot(value = 0)
        wall_pane2.x_dim('Height',[Height])
        wall_pane2.y_dim('Depth+Panel_Thickness',[Depth,Panel_Thickness])
        wall_pane2.z_dim(value = unit.inch(-.75))
        
        toe_kick = common_parts.add_toe_kick(self)
        toe_kick.x_loc('Width-(Toe_Kick_Setback*2)',[Width,Toe_Kick_Setback])
        toe_kick.y_loc(value = 0)
        toe_kick.z_loc(value = 0)
        toe_kick.x_rot(value = 90)
        toe_kick.y_rot(value = 0)
        toe_kick.x_dim('sqrt(((fabs(Depth)-Toe_Kick_Setback)**2.2)+((fabs(Width)-Toe_Kick_Setback)**2.2))*-1',[Width,Depth,Toe_Kick_Setback])
        toe_kick.z_rot('atan((fabs(Depth)+Toe_Kick_Setback)/(fabs(Width)+Toe_Kick_Setback))',[Width,Depth,Toe_Kick_Setback])
        toe_kick.y_dim('Toe_Kick_Height',[Toe_Kick_Height])
        toe_kick.z_dim(value = unit.inch(.75))
        
        self.update()        


class Corner_Pie_Shelves(fd_types.Assembly):

    library_name = "Closets By Design"
    category_name = "Corner Units"
    type_assembly = "PRODUCT"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".outside_corner_shelves"
    placement_type = 'Corner'
    # drop_id = "cbddrop.place_corner_l_shelves"

    def draw(self):
        self.create_assembly()
        
        self.add_tab(name='Angle Shelf Options',tab_type='VISIBLE')
        self.add_tab(name='Material Thickness',tab_type='HIDDEN')
        self.add_prompt(name="Left Depth",prompt_type='DISTANCE',value=unit.inch(12),tab_index=0)       
        self.add_prompt(name="Right Depth",prompt_type='DISTANCE',value=unit.inch(12),tab_index=0)  
        self.add_prompt(name="Shelf Quantity",prompt_type='QUANTITY',value=3,tab_index=0)  
        common_prompts.add_toe_kick_prompts(self)
        common_prompts.add_thickness_prompts(self)
        
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Left_Depth = self.get_var('Left Depth')
        Right_Depth = self.get_var('Right Depth')
        Shelf_Thickness = self.get_var('Shelf Thickness')
        Panel_Thickness = self.get_var('Panel Thickness')
        Toe_Kick_Height = self.get_var('Toe Kick Height')
        Toe_Kick_Setback = self.get_var('Toe Kick Setback')
        Shelf_Quantity = self.get_var('Shelf Quantity')
        
        self.x_dim('fabs(Depth)',[Depth])
        
        inside_height_empty = self.add_empty()
        inside_height_empty.z_loc('Height-Toe_Kick_Height-(Shelf_Thickness*2)-(Shelf_Thickness*Shelf_Quantity)',[Height,Toe_Kick_Height,Shelf_Thickness,Shelf_Quantity])
        Inside_Height = inside_height_empty.get_var('loc_z','Inside_Height')
        
        top = common_parts.add_radius_shelf(self)
        top.x_loc('Panel_Thickness',[Panel_Thickness])
        top.y_loc('-Panel_Thickness',[Panel_Thickness])
        top.z_loc('Height-Panel_Thickness',[Height,Panel_Thickness])
        top.x_rot(value = 0)
        top.y_rot(value = 180)
        top.z_rot(value = 90)
        top.x_dim('fabs(Depth)-Panel_Thickness',[Depth,Panel_Thickness])
        top.y_dim('(Width-Panel_Thickness)*-1',[Width,Panel_Thickness])
        top.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        top.prompt('Radius','Width-Panel_Thickness',[Width,Panel_Thickness])
        
        bottom = common_parts.add_radius_shelf(self)
        bottom.x_loc('Panel_Thickness',[Panel_Thickness])
        bottom.y_loc('-Panel_Thickness',[Panel_Thickness])
        bottom.z_loc('Toe_Kick_Height',[Toe_Kick_Height])
        bottom.x_rot(value = 0)
        bottom.y_rot(value = 180)
        bottom.z_rot(value = 90)
        bottom.x_dim('fabs(Depth)-Panel_Thickness',[Depth,Panel_Thickness])
        bottom.y_dim('(Width-Panel_Thickness)*-1',[Width,Panel_Thickness])
        bottom.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        bottom.prompt('Radius','Width-Panel_Thickness',[Width,Panel_Thickness])
        
        shelf = common_parts.add_radius_shelf(self)
        shelf.x_loc('Panel_Thickness',[Panel_Thickness])
        shelf.y_loc('-Panel_Thickness',[Panel_Thickness])
        shelf.z_loc('Height-Shelf_Thickness-(Inside_Height/(Shelf_Quantity+1))',[Height,Inside_Height,Toe_Kick_Height,Shelf_Thickness,Shelf_Quantity])
        shelf.x_rot(value = 0)
        shelf.y_rot(value = 180)
        shelf.z_rot(value = 90)
        shelf.x_dim('fabs(Depth)-Panel_Thickness',[Depth,Panel_Thickness])
        shelf.y_dim('(Width-Panel_Thickness)*-1',[Width,Panel_Thickness])
        shelf.z_dim('Shelf_Thickness',[Shelf_Thickness])
        shelf.prompt('Radius','Width-Panel_Thickness',[Width,Panel_Thickness])
        shelf.prompt('Hide','IF(Shelf_Quantity==0,True,False)',[Shelf_Quantity])
        shelf.prompt('Z Quantity','Shelf_Quantity',[Shelf_Quantity])
        shelf.prompt('Z Offset','(Inside_Height/(Shelf_Quantity+1))+Shelf_Thickness',[Inside_Height,Shelf_Quantity,Shelf_Thickness])
        
        wall_panel = common_parts.add_panel(self)
        wall_panel.set_name("Wall Panel")
        wall_panel.x_loc(value = 0)
        wall_panel.y_loc(value = 0)
        wall_panel.z_loc(value = 0)
        wall_panel.x_rot(value = 0)
        wall_panel.y_rot(value = -90)
        wall_panel.z_rot(value = -90)
        wall_panel.x_dim('Height',[Height])
        wall_panel.y_dim('Width',[Width,Panel_Thickness])
        wall_panel.z_dim(value = unit.inch(-.75))
        
        wall_pane2 = common_parts.add_panel(self)
        wall_pane2.set_name("Wall Panel")
        wall_pane2.x_loc(value = 0)
        wall_pane2.y_loc(value = 0)
        wall_pane2.z_loc(value = 0)
        wall_pane2.x_rot(value = 0)
        wall_pane2.y_rot(value = -90)
        wall_pane2.z_rot(value = 0)
        wall_pane2.x_dim('Height',[Height])
        wall_pane2.y_dim('Depth',[Depth,Panel_Thickness])
        wall_pane2.z_dim(value = unit.inch(-.75))
        
        toe_kick = common_parts.add_toe_kick_radius(self)
        toe_kick.x_loc('Width-Toe_Kick_Setback',[Width,Toe_Kick_Setback])
        toe_kick.y_loc(value = 0)
        toe_kick.z_loc(value = 0)
        toe_kick.x_rot(value = 90)
        toe_kick.y_rot(value = 0)
        toe_kick.z_rot(value = -90)
        toe_kick.x_dim('radians(90)*(Width-Toe_Kick_Setback)',[Width,Toe_Kick_Setback])
        toe_kick.y_dim('Toe_Kick_Height',[Toe_Kick_Height])
        toe_kick.z_dim(value = unit.inch(.75))
        toe_kick.prompt('Bending',value=math.radians(90))
        toe_kick.prompt('Hide','IF(Shelf_Quantity==0,True,False)',[Shelf_Quantity])
        
        self.update()               


def update_product_height(self,context):
    # THIS IS A HACK!
    # FOR SOME REASON THE FORMULAS IN THE PRODUCT WILL NOT
    # RECALCULATE WHEN THE PANEL HEIGHT IS CHANGED
    obj_product_bp = utils.get_bp(context.active_object,'PRODUCT')
    product = fd_types.Assembly(obj_product_bp)
    if product:
        product.obj_z.location.z = product.obj_z.location.z


class PROMPTS_Corner_Shelves(fd_types.Prompts_Interface):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".corner_shelves"
    bl_label = "Corner Shelves Prompts"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name",
                                           description="Stores the Base Point Object Name \
                                           so the object can be retrieved from the database.")
    
    width = bpy.props.FloatProperty(name="Width",unit='LENGTH',precision=4)
    height = bpy.props.FloatProperty(name="Height",unit='LENGTH',precision=4)
    depth = bpy.props.FloatProperty(name="Depth",unit='LENGTH',precision=4)   
    
    Product_Height = bpy.props.EnumProperty(name="Product Height",
                                            items=common_lists.PANEL_HEIGHTS,
                                            update=update_product_height) 

    Door_Type = bpy.props.EnumProperty(name="Door Type",
                                       items=[("Reach Back","Reach Back","Reach Back"),
                                              ("Lazy Susan","Lazy Susan","Lazy Susan")],
                                       default='Reach Back')

    Pull_Location = bpy.props.EnumProperty(name="Pull Location",
                                           items=[("Pull on Left Door","Pull on Left Door","Pull on Left Door"),
                                                  ("Pull on Right Door","Pull on Right Door","Pull on Right Door")],
                                           default="Pull on Left Door")

    Pull_Type = bpy.props.EnumProperty(name="Pull Type",
                                       items=[("Base","Base","Base"),
                                              ("Tall","Tall","Tall"),
                                              ("Upper","Upper","Upper")],
                                       default="Base")

    Shelf_1_Height = bpy.props.EnumProperty(name="Shelf 1 Height",
                                             items = common_lists.SHELF_IN_DOOR_HEIGHTS)
    
    Shelf_2_Height = bpy.props.EnumProperty(name="Shelf 2 Height",
                                             items = common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_3_Height = bpy.props.EnumProperty(name="Shelf 3 Height",
                                             items = common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_4_Height = bpy.props.EnumProperty(name="Shelf 4 Height",
                                             items = common_lists.SHELF_IN_DOOR_HEIGHTS)
    
    Shelf_5_Height = bpy.props.EnumProperty(name="Shelf 5 Height",
                                             items = common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_6_Height = bpy.props.EnumProperty(name="Shelf 6 Height",
                                             items = common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_7_Height = bpy.props.EnumProperty(name="Shelf 7 Height",
                                             items = common_lists.SHELF_IN_DOOR_HEIGHTS)
    
    Shelf_8_Height = bpy.props.EnumProperty(name="Shelf 8 Height",
                                             items = common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_9_Height = bpy.props.EnumProperty(name="Shelf 9 Height",
                                             items = common_lists.SHELF_IN_DOOR_HEIGHTS)

    Shelf_10_Height = bpy.props.EnumProperty(name="Shelf 10 Height",
                                              items = common_lists.SHELF_IN_DOOR_HEIGHTS)

    shelf_quantity = bpy.props.EnumProperty(name="Shelf Quantity",
                                            items=[('0',"0",'0'),
                                                   ('1',"1",'1'),
                                                   ('2',"2",'2'),
                                                   ('3',"3",'3'),
                                                   ('4',"4",'4'),
                                                   ('5',"5",'5'),
                                                   ('6',"6",'6'),
                                                   ('7',"7",'7'),
                                                   ('8',"8",'8'),
                                                   ('9',"9",'9'),
                                                   ('10',"10",'10')],
                                            default = '3')                                         
    
    product = None

    def check(self, context):
        """ This is called everytime a change is made in the UI """
        self.set_prompts_from_properties()
        self.product.obj_x.location.x = self.width
        self.product.obj_y.location.y = -self.depth
        props_closet.update_render_materials(self, context)
        # self.update_product_size()
        return True      

    def execute(self, context):
        """ This is called when the OK button is clicked """
        # self.update_product_size()
        return {'FINISHED'}

    def invoke(self,context,event):
        """ This is called before the interface is displayed """
        self.product = self.get_product()
        self.set_properties_from_prompts()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(400))

    def set_prompts_from_properties(self):
        ''' This should be called in the check function to set the prompts
            to the same values as the class properties
        '''
        door_type = self.product.get_prompt('Door Type')
        pull_location = self.product.get_prompt('Pull Location')
        pull_type = self.product.get_prompt('Pull Type')
        is_hanging = self.product.get_prompt("Is Hanging")
        panel_height = self.product.get_prompt("Panel Height")
        shelf_quantity = self.product.get_prompt("Shelf Quantity")
        shelf_thickness = self.product.get_prompt("Shelf Thickness")
        toe_kick_height = self.product.get_prompt("Toe Kick Height")

        prompts = [door_type,pull_location,pull_type,is_hanging,panel_height,shelf_quantity,shelf_thickness,toe_kick_height]
        if all(prompts):
            door_type.set_value(self.Door_Type)
            pull_location.set_value(self.Pull_Location)
            pull_type.set_value(self.Pull_Type)
            if is_hanging.value():
                panel_height.set_value(float(self.Product_Height) / 1000)
            else:
                panel_height.set_value(float(self.Product_Height) / 1000)
                self.product.obj_z.location.z = float(self.Product_Height) / 1000

        
            shelf_quantity.set_value(int(self.shelf_quantity))
            for i in range(1,int(self.shelf_quantity)+1):
                shelf = self.product.get_prompt("Shelf " + str(i) + " Height")

                hole_count = round(((panel_height.value())*1000)/32)
                holes_per_shelf = round(hole_count/(int(self.shelf_quantity)+1))
                remainder = hole_count - (holes_per_shelf * (int(self.shelf_quantity)))
            
                if(i <= remainder):
                    holes_per_shelf = holes_per_shelf + 1
                if(holes_per_shelf >=3):
                    shelf.set_value(float(common_lists.SHELF_IN_DOOR_HEIGHTS[holes_per_shelf-3][0])/1000)
                    exec("self.Shelf_" + str(i) + "_Height = common_lists.SHELF_IN_DOOR_HEIGHTS[holes_per_shelf-3][0]")
                else:
                    shelf.set_value(float(common_lists.SHELF_IN_DOOR_HEIGHTS[0][0])/1000)
                    exec("self.Shelf_" + str(i) + "_Height = common_lists.SHELF_IN_DOOR_HEIGHTS[0][0]")
        
    def set_properties_from_prompts(self):
        ''' This should be called in the invoke function to set the class properties
            to the same values as the prompts
        '''
        panel_height = self.product.get_prompt("Panel Height")
        door_type = self.product.get_prompt('Door Type')
        pull_location = self.product.get_prompt('Pull Location')
        pull_type = self.product.get_prompt('Pull Type')
        shelf_quantity = self.product.get_prompt("Shelf Quantity")

        prompts = [door_type,pull_location,pull_type,panel_height,shelf_quantity]
        if all(prompts):
            self.Door_Type = door_type.value()
            self.Pull_Location = pull_location.value()
            self.Pull_Type = pull_type.value()
            for index, height in enumerate(common_lists.PANEL_HEIGHTS):
                if not round(panel_height.value()*1000,0) >= int(height[0]):
                    self.Product_Height = common_lists.PANEL_HEIGHTS[index - 1][0]
                    break
            
            
            self.shelf_quantity = str(shelf_quantity.value())
            for i in range(1,11):
                shelf = self.product.get_prompt("Shelf " + str(i) + " Height")
                if shelf:
                    value = round(shelf.value() * 1000,3)
                    for index, height in enumerate(common_lists.SHELF_IN_DOOR_HEIGHTS):
                        if not value >= float(height[0]):
                            exec("self.Shelf_" + str(i) + "_Height = common_lists.SHELF_IN_DOOR_HEIGHTS[index - 1][0]")
                            break
            
    
    def draw_product_size(self,layout):
        box = layout.box()
        row = box.row()
        
        col = row.column(align=True)
        row1 = col.row(align=True)
        if utils.object_has_driver(self.product.obj_x):
            row1.label('Width: ' + str(unit.meter_to_active_unit(math.fabs(self.product.obj_x.location.x))))
        else:
            row1.label('Width:')
            row1.prop(self,'width',text="")
            row1.prop(self.product.obj_x,'hide',text="")
        
        row1 = col.row(align=True)
        if utils.object_has_driver(self.product.obj_z):
            row1.label('Height: ' + str(unit.meter_to_active_unit(math.fabs(self.product.obj_z.location.z))))
        else:
            row1.label('Height:')
            row1.prop(self,'Product_Height',text="")
            row1.prop(self.product.obj_z,'hide',text="")
        
        row1 = col.row(align=True)
        if utils.object_has_driver(self.product.obj_y):
            row1.label('Depth: ' + str(unit.meter_to_active_unit(math.fabs(self.product.obj_y.location.y))))
        else:
            row1.label('Depth:')
            row1.prop(self,'depth',text="")
            row1.prop(self.product.obj_y,'hide',text="")
            
        col = row.column(align=True)
        col.label("Location X:")
        col.label("Location Y:")
        col.label("Location Z:")
        
        col = row.column(align=True)
        col.prop(self.product.obj_bp,'location',text="")
        

        Toe_Kick_Height = self.product.get_prompt("Toe Kick Height") 
        
        if Toe_Kick_Height:
            row = box.row()
            Toe_Kick_Height.draw_prompt(row)        
         
        is_hanging = self.product.get_prompt("Is Hanging")
          
        if is_hanging:
            row = box.row()
            is_hanging.draw_prompt(row)
            if is_hanging.value():
                row.prop(self.product.obj_z,'location',index=2,text="Hanging Height")
         
        row = box.row()
        row.label('Rotation Z:')
        row.prop(self.product.obj_bp,'rotation_euler',index=2,text="")  
 

    def draw(self, context):
        """ This is where you draw the interface """
        Left_Depth = self.product.get_prompt("Left Depth")
        Right_Depth = self.product.get_prompt("Right Depth")
        Shelf_Quantity = self.product.get_prompt("Shelf Quantity")
        Add_Backing = self.product.get_prompt("Add Backing")
        Backing_Thickness = self.product.get_prompt("Backing Thickness")
        Add_Top = self.product.get_prompt("Add Top")
        Hide_Toe_Kick = self.product.get_prompt("Hide Toe Kick")
        Door = self.product.get_prompt("Door")
        Use_Left_Swing = self.product.get_prompt("Use Left Swing")
        Pull_Location = self.product.get_prompt("Pull Location")
        Force_Double_Doors = self.product.get_prompt("Force Double Doors")
        Door_Pull_Height = self.product.get_prompt("Door Pull Height")
        Door_Type = self.product.get_prompt("Door Type")
        Angled_Shelves = self.product.get_prompt("Angled Shelves")
        Open_Door = self.product.get_prompt("Open Door")
        Base_Pull_Location = self.product.get_prompt("Base Pull Location")
        Tall_Pull_Location = self.product.get_prompt("Tall Pull Location")
        Upper_Pull_Location = self.product.get_prompt("Upper Pull Location")
         
        layout = self.layout
        self.draw_product_size(layout)        
        
        if Left_Depth:
            box = layout.box()
            row = box.row()
            Left_Depth.draw_prompt(row)
        
        if Right_Depth:
            Right_Depth.draw_prompt(row)
            
        if Shelf_Quantity:
            col = box.column(align=True)
            row = col.row()
            row.label("Qty:")
            row.prop(self,"shelf_quantity",expand=True)   
            col.separator()
            
        if Add_Backing:
            row = box.row()
            Add_Backing.draw_prompt(row)

        #if Backing_Thickness:
        #    if Add_Backing.value() == True:
        #        row = box.row()
        #        Backing_Thickness.draw_prompt(row)
            
            
        #if Add_Top:
        #    row = box.row()
        #    Add_Top.draw_prompt(row)            
                
                
        # row = box.row()
        # Hide_Toe_Kick.draw_prompt(row)
       
        row = box.row()
        Door.draw_prompt(row)
        if Door.value():
            if Angled_Shelves and Door_Type:
                if Angled_Shelves.value() == False:
                    row = box.row()
                    row.prop(self,'Door_Type',text="Door Type")
                    #Door_Type.draw_prompt(row)
                    row = box.row()
                    #Pull_Location.draw_prompt(row)
                    row.prop(self,'Pull_Location',text="Pull Location")

            row = box.row()
            #Door_Pull_Height.draw_prompt(row)
            row.prop(self,'Pull_Type',text="Pull Type")
            row = box.row()
            if self.Pull_Type == 'Base':
                Base_Pull_Location.draw_prompt(row)
            elif self.Pull_Type == 'Tall':
                Tall_Pull_Location.draw_prompt(row)
            else:
                Upper_Pull_Location.draw_prompt(row)

            if Open_Door: 
                row = box.row()
                Open_Door.draw_prompt(row)

            if Angled_Shelves:
                if Angled_Shelves.value():
                    row = box.row()
                    Use_Left_Swing.draw_prompt(row)
                    row = box.row() 
                    Force_Double_Doors.draw_prompt(row)
            

class PROMPTS_Outside_Corner_Shelves(fd_types.Prompts_Interface):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".outside_corner_shelves"
    bl_label = "Outside Corner Shelves Prompts"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name",
                                           description="Stores the Base Point Object Name \
                                           so the object can be retrieved from the database.")
    
    height = bpy.props.FloatProperty(name="Height",unit='LENGTH',precision=4)
    depth = bpy.props.FloatProperty(name="Depth",unit='LENGTH',precision=4)    
    
    product = None

    def check(self, context):
        """ This is called everytime a change is made in the UI """
        self.update_product_size()
        return True

    def execute(self, context):
        """ This is called when the OK button is clicked """
        self.update_product_size()
        return {'FINISHED'}

    def invoke(self,context,event):
        """ This is called before the interface is displayed """
        self.product = self.get_product()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(400))
        
    def draw(self, context):
        """ This is where you draw the interface """
        layout = self.layout
        self.draw_product_size(layout)
        
        Left_Depth = self.product.get_prompt("Left Depth")
        Right_Depth = self.product.get_prompt("Right Depth")
        Shelf_Quantity = self.product.get_prompt("Shelf Quantity")
        
        box = layout.box()
        row = box.row()
        Shelf_Quantity.draw_prompt(row)
 
        
class PROMPTS_Outside_Corner_Angle_Shelves(fd_types.Prompts_Interface):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".outside_corner_angle_shelves"
    bl_label = "Outside Corner Angle Shelves Prompts"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name",
                                           description="Stores the Base Point Object Name \
                                           so the object can be retrieved from the database.")
    
    height = bpy.props.FloatProperty(name="Height",unit='LENGTH',precision=4)
    depth = bpy.props.FloatProperty(name="Depth",unit='LENGTH',precision=4)    
    
    product = None

    def check(self, context):
        """ This is called everytime a change is made in the UI """
        self.update_product_size()
        return True

    def execute(self, context):
        """ This is called when the OK button is clicked """
        self.update_product_size()
        return {'FINISHED'}

    def invoke(self,context,event):
        """ This is called before the interface is displayed """
        self.product = self.get_product()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(400))
        
    def draw(self, context):
        """ This is where you draw the interface """
        
        Left_Depth = self.product.get_prompt("Left Depth")
        Right_Depth = self.product.get_prompt("Right Depth")
        Shelf_Quantity = self.product.get_prompt("Shelf Quantity")
                
        layout = self.layout
        self.draw_product_size(layout)
        box = layout.box()
        row = box.row()
        Left_Depth.draw_prompt(row) 
        Right_Depth.draw_prompt(row)
        box = layout.box()
        row = box.row()
        Shelf_Quantity.draw_prompt(row)
        

class DROP_OPERATOR_Place_L_Shelves(bpy.types.Operator):
    bl_idname = "cbddrop.place_corner_l_shelves"
    bl_label = "Place Valance"
    bl_description = "This places a valance part on a shelf."
    bl_options = {'UNDO'}
    
    #READONLY
    object_name = bpy.props.StringProperty(name="Object Name")
    
    product = None
    
    def invoke(self, context, event):
        bp = bpy.data.objects[self.object_name]
        self.product = fd_types.Assembly(bp)
        self.product.obj_z.location.z = 0
        self.product.obj_x.location.x = 0
        utils.set_wireframe(self.product.obj_bp,True)
        context.window.cursor_set('PAINT_BRUSH')
        context.scene.update() # THE SCENE MUST BE UPDATED FOR RAY CAST TO WORK
        context.window_manager.modal_handler_add(self)
        context.area.header_text_set(text="Select first shelf to add backing to.")
        return {'RUNNING_MODAL'}

    def cancel_drop(self,context,event):
        if self.product:
            utils.delete_object_and_children(self.product.obj_bp)
        bpy.context.window.cursor_set('DEFAULT')
        context.area.header_text_set()
        return {'FINISHED'}

    def product_drop(self,context,event):
        selected_point, selected_obj = utils.get_selection_point(context,event)
        bpy.ops.object.select_all(action='DESELECT')
        context.area.header_text_set(text="Select shelf to add valance to")
        sel_assembly_bp = utils.get_assembly_bp(selected_obj)
        
        if sel_assembly_bp:
            
            if sel_assembly_bp.lm_cbd.is_shelf_bp:

                #HIGHLIGHT SELCTED ASSEMBLY
                sel_assembly = fd_types.Assembly(sel_assembly_bp)
                selected_obj.select = True                    
                
                #PARENT TO SHELF. THIS CAN BE THE PRODUCT OR INSERT
                self.product.obj_bp.parent = sel_assembly.obj_bp
                self.product.obj_bp.location.y = sel_assembly.obj_y.location.y
                self.product.obj_bp.location.z = sel_assembly.obj_z.location.z
                
                #Set Width of the back to the same as the shelf
                self.product.obj_x.location.x = sel_assembly.obj_x.location.x
                    
                if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                    utils.copy_drivers(sel_assembly.obj_x,self.product.obj_x)
                    
                    utils.set_wireframe(self.product.obj_bp,False)
                    bpy.context.window.cursor_set('DEFAULT')
                    bpy.ops.object.select_all(action='DESELECT')
                    context.scene.objects.active = self.product.obj_bp
                    self.product.obj_bp.select = True
                    context.area.header_text_set()
                    return {'FINISHED'}
            else:
                self.product.obj_x.location.x = 0
        else:
            self.product.obj_x.location.x = 0

        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        context.area.tag_redraw()
        
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}
        
        if event.type in {'ESC'}:
            self.cancel_drop(context,event)
            return {'FINISHED'}
        
        return self.product_drop(context,event)      


bpy.utils.register_class(DROP_OPERATOR_Place_L_Shelves)
bpy.utils.register_class(PROMPTS_Corner_Shelves)
bpy.utils.register_class(PROMPTS_Outside_Corner_Shelves)
bpy.utils.register_class(PROMPTS_Outside_Corner_Angle_Shelves)