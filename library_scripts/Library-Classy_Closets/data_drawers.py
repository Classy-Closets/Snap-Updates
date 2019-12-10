import bpy
from os import path
from mv import fd_types, unit, utils
from . import mv_closet_defaults as props_closet
from . import common_parts
from . import common_prompts
from . import common_lists

LOCK_DRAWER_TYPES=[('None','None','None'),
                   ('Top','Top','Top'),
                   ('Left','Left','Left'),
                   ('Right','Right','Right')]

class Drawer_Stack(fd_types.Assembly):
    """ This drawer insert allows users to specify the quanity of drawers
        and the height of each indiviual drawer front height then the top 
        shelf is automatically placed based on the heights. The remaining 
        space is filled with an opening. The drawer max is 6.
    """
    property_id = props_closet.LIBRARY_NAME_SPACE + ".drawer_prompts"
    placement_type = "SPLITTER"
    type_assembly = "INSERT"
    mirror_y = False
    
    is_pull_out_tray = False
    
    upper_interior = None
    upper_exterior = None
    
    def add_drawers(self):
        dim_x = self.get_var("dim_x")
        dim_y = self.get_var("dim_y")
        Left_Overlay = self.get_var("Left Overlay")
        Right_Overlay = self.get_var("Right Overlay")
        Bottom_Overlay = self.get_var("Bottom Overlay")
        Horizontal_Gap = self.get_var("Horizontal Gap")
        
        Inset_Front = self.get_var("Inset Front")
        Front_Thickness = self.get_var("Front Thickness")
        Door_to_Cabinet_Gap = self.get_var("Door to Cabinet Gap")
        Open = self.get_var("Open")
        Drawer_Quantity = self.get_var("Drawer Quantity")
        Drawer_Stack_Height = self.get_var("Drawer Stack Height")
        Center_Pulls_on_Drawers = self.get_var("Center Pulls on Drawers")
        Drawer_Pull_From_Top = self.get_var("Drawer Pull From Top")
        Use_Double_Pulls = self.get_var("Use Double Pulls")
        Drawer_Box_Slide_Gap = self.get_var("Drawer Box Slide Gap")
        Drawer_Box_Bottom_Gap = self.get_var("Drawer Box Bottom Gap")
        Drawer_Box_Rear_Gap = self.get_var("Drawer Box Rear Gap")
        Drawer_Box_Top_Gap = self.get_var("Drawer Box Top Gap")
        Division_Thickness = self.get_var("Division Thickness")
        Lift_Drawers_From_Bottom = self.get_var("Lift Drawers From Bottom")
        Bottom_Drawer_Space = self.get_var("Bottom Drawer Space")
        No_Pulls = self.get_var("No Pulls")
        
        prev_drawer_empty = None
        
        for i in range(1,7):
            DF_Height = self.get_var("Drawer " + str(i) + " Height","DF_Height")
            Lock_Drawer = self.get_var("Lock " + str(i) + " Drawer","Lock_Drawer")
            
            front_empty = self.add_empty()
            if prev_drawer_empty:
                prev_drawer_z_loc = prev_drawer_empty.get_var('loc_z','prev_drawer_z_loc')
                front_empty.z_loc('prev_drawer_z_loc-DF_Height-Horizontal_Gap',[prev_drawer_z_loc,DF_Height,Horizontal_Gap])
            else:
                front_empty.z_loc('Drawer_Stack_Height-DF_Height+IF(Lift_Drawers_From_Bottom,Bottom_Drawer_Space,0)',
                                  [Drawer_Stack_Height,DF_Height,Lift_Drawers_From_Bottom,Bottom_Drawer_Space])               
            
            df_z_loc = front_empty.get_var('loc_z','df_z_loc')
            
            front = common_parts.add_drawer_front(self)
            front.x_loc('dim_x+Right_Overlay',[dim_x,Right_Overlay])
            front.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(dim_y*Open)',[Door_to_Cabinet_Gap,dim_y,Open,Inset_Front,Front_Thickness])
            front.z_loc('df_z_loc',[df_z_loc])
            front.x_rot(value = 90)
            front.y_rot(value = -90)
            front.z_rot(value = 0)
            front.x_dim('DF_Height',[DF_Height])
            front.y_dim('dim_x+Left_Overlay+Right_Overlay',[dim_x,Left_Overlay,Right_Overlay])
            front.z_dim('Front_Thickness',[Front_Thickness])
            front.prompt('Hide','IF(Drawer_Quantity>' + str(i-1) + ',False,True)',[Drawer_Quantity])
            front.prompt('No Pulls','No_Pulls',[No_Pulls])
            front.prompt('Use Double Pulls','Use_Double_Pulls',[Use_Double_Pulls])
            front.prompt('Center Pulls on Drawers','Center_Pulls_on_Drawers',[Center_Pulls_on_Drawers])
            front.prompt('Drawer Pull From Top','Drawer_Pull_From_Top',[Drawer_Pull_From_Top])
            front.add_prompt(name="Left Overlay",prompt_type='DISTANCE',value=0,tab_index=0)
            front.add_prompt(name="Right Overlay",prompt_type='DISTANCE',value=0,tab_index=0)
            front.prompt('Left Overlay','Left_Overlay',[Left_Overlay])
            front.prompt('Right Overlay','Right_Overlay',[Right_Overlay])            
            
            # front = common_parts.add_drawer_front(self)
            # front.x_loc('-Left_Overlay',[Left_Overlay])
            # front.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(dim_y*Open)',[Door_to_Cabinet_Gap,dim_y,Open,Inset_Front,Front_Thickness])
            # front.z_loc('df_z_loc',[df_z_loc])
            # front.x_rot(value = 90)
            # front.y_rot(value = 0)
            # front.z_rot(value = 0)
            # front.x_dim('dim_x+Left_Overlay+Right_Overlay',[dim_x,Left_Overlay,Right_Overlay])
            # front.y_dim('DF_Height',[DF_Height])
            # front.z_dim('Front_Thickness',[Front_Thickness])
            # front.prompt('Hide','IF(Drawer_Quantity>' + str(i-1) + ',False,True)',[Drawer_Quantity])
            # front.prompt('No Pulls','No_Pulls',[No_Pulls])
            # front.prompt('Use Double Pulls','Use_Double_Pulls',[Use_Double_Pulls])
            # front.prompt('Center Pulls on Drawers','Center_Pulls_on_Drawers',[Center_Pulls_on_Drawers])
            # front.prompt('Drawer Pull From Top','Drawer_Pull_From_Top',[Drawer_Pull_From_Top])
            # front.add_prompt(name="Left Overlay",prompt_type='DISTANCE',value=0,tab_index=0)
            # front.add_prompt(name="Right Overlay",prompt_type='DISTANCE',value=0,tab_index=0)
            # front.prompt('Left Overlay','Left_Overlay',[Left_Overlay])
            # front.prompt('Right Overlay','Right_Overlay',[Right_Overlay])
            
            l_pull = common_parts.add_drawer_pull(self)
            l_pull.set_name("Drawer Pull")
            l_pull.x_loc('-Left_Overlay',[Left_Overlay])
            l_pull.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(dim_y*Open)',[Door_to_Cabinet_Gap,dim_y,Open,Inset_Front,Front_Thickness])
            l_pull.z_loc('df_z_loc',[df_z_loc])
            l_pull.x_rot(value = 90)
            l_pull.y_rot(value = 0)
            l_pull.z_rot(value = 0)
            l_pull.x_dim('dim_x+Left_Overlay+Right_Overlay',[dim_x,Left_Overlay,Right_Overlay])
            l_pull.y_dim('DF_Height',[DF_Height])
            l_pull.z_dim('Front_Thickness',[Front_Thickness])
            l_pull.prompt("Pull X Location",'IF(Center_Pulls_on_Drawers,DF_Height/2,Drawer_Pull_From_Top)',[Center_Pulls_on_Drawers,DF_Height,Drawer_Pull_From_Top])
            l_pull.prompt("Pull Z Location",'IF(Use_Double_Pulls,(dim_x/4),(dim_x/2))+Right_Overlay',[Use_Double_Pulls,dim_x,Right_Overlay])
            l_pull.prompt('Hide','IF(No_Pulls,True,IF(Drawer_Quantity>' + str(i-1) + ',False,True))',[Drawer_Quantity,No_Pulls])
            
            r_pull = common_parts.add_drawer_pull(self)
            r_pull.set_name("Drawer Pull")
            r_pull.x_loc('-Left_Overlay',[Left_Overlay])
            r_pull.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(dim_y*Open)',[Door_to_Cabinet_Gap,dim_y,Open,Inset_Front,Front_Thickness])
            r_pull.z_loc('df_z_loc',[df_z_loc])
            r_pull.x_rot(value = 90)
            r_pull.y_rot(value = 0)
            r_pull.z_rot(value = 0)
            r_pull.x_dim('dim_x+Left_Overlay+Right_Overlay',[dim_x,Left_Overlay,Right_Overlay])
            r_pull.y_dim('DF_Height',[DF_Height])
            r_pull.z_dim('Front_Thickness',[Front_Thickness])
            r_pull.prompt("Pull X Location",'IF(Center_Pulls_on_Drawers,DF_Height/2,Drawer_Pull_From_Top)',[Center_Pulls_on_Drawers,DF_Height,Drawer_Pull_From_Top])
            r_pull.prompt("Pull Z Location",'dim_x-(dim_x/4)+Right_Overlay',[dim_x,Right_Overlay])
            r_pull.prompt('Hide','IF(No_Pulls,True,IF(Drawer_Quantity>' + str(i-1) + ',IF(Use_Double_Pulls,False,True),True))',[No_Pulls,Drawer_Quantity,Use_Double_Pulls])
            
            drawer = common_parts.add_drawer(self)
            drawer.set_name("Drawer Box")
            drawer.x_loc('Drawer_Box_Slide_Gap',[Drawer_Box_Slide_Gap])
            drawer.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(dim_y*Open)',[Door_to_Cabinet_Gap,dim_y,Open,Inset_Front,Front_Thickness])
            drawer.z_loc('df_z_loc+Drawer_Box_Bottom_Gap+IF(Drawer_Quantity==' + str(i) + ',Bottom_Overlay,0)',[df_z_loc,Drawer_Box_Bottom_Gap,Drawer_Quantity,Bottom_Overlay])
            drawer.x_rot(value = 0)
            drawer.y_rot(value = 0)
            drawer.z_rot(value = 0)
            drawer.x_dim('dim_x-(Drawer_Box_Slide_Gap*2)',[dim_x,Drawer_Box_Slide_Gap])
            drawer.y_dim('dim_y-Drawer_Box_Rear_Gap',[dim_y,Drawer_Box_Rear_Gap])
            drawer.z_dim('DF_Height-Drawer_Box_Top_Gap-Drawer_Box_Bottom_Gap',[DF_Height,Drawer_Box_Top_Gap,Drawer_Box_Bottom_Gap])
            drawer.prompt('Hide','IF(Drawer_Quantity>' + str(i-1) + ',False,True)',[Drawer_Quantity])
            
            prev_drawer_empty = front_empty
            
            drawer_z_loc = drawer.get_var('loc_z','drawer_z_loc')
            drawer_z_dim = drawer.get_var('dim_z','drawer_z_dim')
             
            drawer_lock = common_parts.add_lock(self)
            drawer_lock.x_loc('IF(Lock_Drawer==2,-Division_Thickness,IF(Lock_Drawer==3,dim_x+Division_Thickness,dim_x/2))',[Lock_Drawer,dim_x,Division_Thickness])
            drawer_lock.y_loc('IF(Lock_Drawer==1,IF(Inset_Front,0,-Front_Thickness-Door_to_Cabinet_Gap),+INCH(.75))',[Inset_Front,Lock_Drawer,Front_Thickness,Door_to_Cabinet_Gap])
            drawer_lock.z_loc('drawer_z_loc+drawer_z_dim-INCH(.5)',[drawer_z_loc,drawer_z_dim])    
            drawer_lock.y_rot(value = 0)
            drawer_lock.z_rot('IF(Lock_Drawer==2,radians(-90),IF(Lock_Drawer==3,radians(90),0))',[Lock_Drawer])
            drawer_lock.prompt('Hide', 'IF(Lock_Drawer>0,IF(Drawer_Quantity>' + str(i-1) + ',False,True),True)',[Lock_Drawer,Drawer_Quantity])           
            
    def draw(self):
        self.create_assembly()
        self.obj_bp.mv.export_as_subassembly = True
        
        props = props_closet.get_object_props(self.obj_bp)
        props.is_drawer_stack_bp = True
        
        common_prompts.add_thickness_prompts(self)
        common_prompts.add_front_overlay_prompts(self)
        common_prompts.add_pull_prompts(self)
        common_prompts.add_drawer_pull_prompts(self)
        common_prompts.add_drawer_box_prompts(self)
        
        self.add_tab(name='Drawer Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        self.add_prompt(name="Open",prompt_type='PERCENTAGE',value=0,tab_index=0)
        self.add_prompt(name="Lift Drawers From Bottom",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Bottom Drawer Space",prompt_type='DISTANCE',value=0,tab_index=0)     
        self.add_prompt(name="Remove Bottom Shelf",prompt_type='CHECKBOX',value=True,tab_index=0)
        self.add_prompt(name="Remove Top Shelf",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Shelf Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
        self.add_prompt(name="Drawer Quantity",prompt_type='QUANTITY',value=3,tab_index=0)
        self.add_prompt(name="Drawer Stack Height",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Drawer Stack Backing Gap",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Use Mirror",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Cleat Location", prompt_type='COMBOBOX', items=["Above", "Below", "None"], value=0, tab_index=0, columns=3)
        
        for i in range(1,7):
            self.add_prompt(name="Lock " + str(i) + " Drawer",prompt_type='COMBOBOX',items=["None","Top","Left","Right"],value=0,tab_index=0,columns=4)        
            self.add_prompt(name="Drawer " + str(i) + " Height",prompt_type='DISTANCE',value=unit.millimeter(91.95),tab_index=0)
        
        dim_x = self.get_var("dim_x")
        dim_y = self.get_var("dim_y")
        dim_z = self.get_var("dim_z")
        Bottom_Overlay = self.get_var("Bottom Overlay")
        Top_Overlay = self.get_var("Top Overlay")
        Drawer_Stack_Height = self.get_var("Drawer Stack Height")
        Shelf_Thickness = self.get_var("Shelf Thickness")
        dq = self.get_var("Drawer Quantity",'dq')
        df1 = self.get_var("Drawer 1 Height",'df1')
        df2 = self.get_var("Drawer 2 Height",'df2')
        df3 = self.get_var("Drawer 3 Height",'df3')
        df4 = self.get_var("Drawer 4 Height",'df4')
        df5 = self.get_var("Drawer 5 Height",'df5')
        df6 = self.get_var("Drawer 6 Height",'df6')
        hg = self.get_var("Horizontal Gap",'hg')
        Lift_Drawers_From_Bottom = self.get_var("Lift Drawers From Bottom")
        Bottom_Drawer_Space = self.get_var("Bottom Drawer Space")
        Remove_Top_Shelf = self.get_var("Remove Top Shelf")
        Remove_Bottom_Shelf = self.get_var("Remove Bottom Shelf")
        Cleat_Location = self.get_var("Cleat Location")

        self.prompt(
            'Drawer Stack Backing Gap',
            'Drawer_Stack_Height+Shelf_Thickness*2-Top_Overlay+IF(Lift_Drawers_From_Bottom,Bottom_Drawer_Space,0)+INCH(3.65)',
            [Drawer_Stack_Height,Shelf_Thickness,Top_Overlay,Lift_Drawers_From_Bottom,Bottom_Drawer_Space]
        )
        
        self.prompt('Drawer Stack Height',
                    'df1+IF(dq>1,df2+hg,0)+IF(dq>2,df3+hg,0)+IF(dq>3,df4+hg,0)+IF(dq>4,df5+hg,0)+IF(dq>5,df6+hg,0)-Bottom_Overlay+MILLIMETER(.85688)', # ? Change height to allow correct door heights
                    [df1,df2,df3,df4,df5,df6,dq,hg,Bottom_Overlay])
        
        self.add_drawers()
        
        cleat = common_parts.add_cleat(self)
        cleat.set_name("Bottom Cleat")
        cleat.x_loc(value = 0)
        cleat.y_loc('dim_y-IF(Cleat_Location==1,INCH(0.75),0)',[dim_y, Cleat_Location])
        cleat.z_loc('Drawer_Stack_Height+IF(Cleat_Location==0,Shelf_Thickness,0)-Top_Overlay+IF(Lift_Drawers_From_Bottom,Bottom_Drawer_Space,0)',
                        [Drawer_Stack_Height,Shelf_Thickness,Top_Overlay,Lift_Drawers_From_Bottom,Bottom_Drawer_Space,Cleat_Location])
        cleat.x_rot('IF(Cleat_Location==1,radians(-90),radians(90))', [Cleat_Location])
        cleat.y_rot(value = 0)
        cleat.z_rot(value = 0) 
        cleat.x_dim('dim_x',[dim_x])
        cleat.y_dim(value=unit.inch(3.65))
        cleat.prompt("Hide", "IF(Cleat_Location==2,True,False)", [Cleat_Location])   
        
        top_shelf = common_parts.add_shelf(self)
        top_shelf.x_loc(value = 0)
        top_shelf.y_loc(value = 0)
        top_shelf.z_loc('Drawer_Stack_Height+Shelf_Thickness-Top_Overlay+IF(Lift_Drawers_From_Bottom,Bottom_Drawer_Space,0)',
                        [Drawer_Stack_Height,Shelf_Thickness,Top_Overlay,Lift_Drawers_From_Bottom,Bottom_Drawer_Space])
        top_shelf.x_rot(value = 0)
        top_shelf.y_rot(value = 0)
        top_shelf.z_rot(value = 0)
        top_shelf.x_dim('dim_x',[dim_x])
        top_shelf.y_dim('dim_y',[dim_y])
        top_shelf.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        top_shelf.prompt('Hide','IF(Remove_Top_Shelf,True,False)',[Remove_Top_Shelf])
        top_shelf.prompt('Is Locked Shelf',value=True)
        
        second_shelf = common_parts.add_shelf(self)
        second_shelf.x_loc(value = 0)
        second_shelf.y_loc(value = 0)
        second_shelf.z_loc('IF(dq==4,df4,IF(dq==5,df5,IF(dq==6,df6,0)))-Bottom_Overlay+Shelf_Thickness-Top_Overlay+IF(Lift_Drawers_From_Bottom,Bottom_Drawer_Space,0)',
                           [dq,df4,df5,df6,Bottom_Overlay,Shelf_Thickness,Top_Overlay,Lift_Drawers_From_Bottom,Bottom_Drawer_Space])
        second_shelf.x_rot(value = 0)
        second_shelf.y_rot(value = 0)
        second_shelf.z_rot(value = 0)
        second_shelf.x_dim('dim_x',[dim_x])
        second_shelf.y_dim('dim_y',[dim_y])
        second_shelf.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        second_shelf.prompt('Hide','IF(dq>3,False,True)',[dq])
        second_shelf.prompt('Is Locked Shelf',value=True)
        
        top_shelf_z_loc = top_shelf.get_var('loc_z','top_shelf_z_loc')
        
        bottom_shelf = common_parts.add_shelf(self)
        bottom_shelf.x_loc(value = 0)
        bottom_shelf.y_loc(value = 0)
        bottom_shelf.z_loc('IF(Lift_Drawers_From_Bottom,Bottom_Drawer_Space,0)',
                        [Drawer_Stack_Height,Shelf_Thickness,Top_Overlay,Lift_Drawers_From_Bottom,Bottom_Drawer_Space])
        bottom_shelf.x_rot(value = 0)
        bottom_shelf.y_rot(value = 0)
        bottom_shelf.z_rot(value = 0)
        bottom_shelf.x_dim('dim_x',[dim_x])
        bottom_shelf.y_dim('dim_y',[dim_y])
        bottom_shelf.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        bottom_shelf.prompt('Hide','IF(Remove_Bottom_Shelf,True,False)',[Remove_Bottom_Shelf])
        bottom_shelf.prompt('Is Locked Shelf',value=True)
        
        opening = common_parts.add_opening(self)
        opening.x_loc(value = 0)
        opening.y_loc(value = 0)
        opening.z_loc('top_shelf_z_loc',[top_shelf_z_loc])
        opening.x_rot(value = 0)
        opening.y_rot(value = 0)
        opening.z_rot(value = 0)
        opening.x_dim('dim_x',[dim_x])
        opening.y_dim('dim_y',[dim_y])
        opening.z_dim('dim_z-top_shelf_z_loc',[dim_z,top_shelf_z_loc])
        
        if self.upper_exterior:
            opening.obj_bp.mv.exterior_open = False
            
            self.upper_exterior.draw()
            self.upper_exterior.obj_bp.parent = self.obj_bp
            self.upper_exterior.x_loc(value = 0)
            self.upper_exterior.y_loc(value = 0)
            self.upper_exterior.z_loc('top_shelf_z_loc',[top_shelf_z_loc])
            self.upper_exterior.x_rot(value = 0)
            self.upper_exterior.y_rot(value = 0)
            self.upper_exterior.z_rot(value = 0)
            self.upper_exterior.x_dim('dim_x',[dim_x])
            self.upper_exterior.y_dim('dim_y',[dim_y])
            self.upper_exterior.z_dim('dim_z-top_shelf_z_loc',[dim_z,top_shelf_z_loc])
        
        if self.upper_interior:
            opening.obj_bp.mv.interior_open = False
            
            self.upper_interior.draw()
            self.upper_interior.obj_bp.parent = self.obj_bp
            self.upper_interior.x_loc(value = 0)
            self.upper_interior.y_loc(value = 0)
            self.upper_interior.z_loc('top_shelf_z_loc',[top_shelf_z_loc])
            self.upper_interior.x_rot(value = 0)
            self.upper_interior.y_rot(value = 0)
            self.upper_interior.z_rot(value = 0)
            self.upper_interior.x_dim('dim_x',[dim_x])
            self.upper_interior.y_dim('dim_y',[dim_y])
            self.upper_interior.z_dim('dim_z-top_shelf_z_loc',[dim_z,top_shelf_z_loc])          
        
        self.update()
        
class PROMPTS_Drawer_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".drawer_prompts"
    bl_label = "Drawer Prompts" 
    bl_description = "This shows all of the available drawer options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    assembly = None
    part = None
    
    drawer_quantity = bpy.props.EnumProperty(name="Drawer Quantity",
                                   items=[('1',"1",'1'),
                                          ('2',"2",'2'),
                                          ('3',"3",'3'),
                                          ('4',"4",'4'),
                                          ('5',"5",'5'),
                                          ('6',"6",'6')],
                                   default = '3')
    
    drawer_1_height = bpy.props.EnumProperty(name="Drawer 1 Height",
                                   items=common_lists.FRONT_HEIGHTS)
    
    drawer_2_height = bpy.props.EnumProperty(name="Drawer 2 Height",
                                   items=common_lists.FRONT_HEIGHTS)
    
    drawer_3_height = bpy.props.EnumProperty(name="Drawer 3 Height",
                                   items=common_lists.FRONT_HEIGHTS)
    
    drawer_4_height = bpy.props.EnumProperty(name="Drawer 4 Height",
                                   items=common_lists.FRONT_HEIGHTS)

    drawer_5_height = bpy.props.EnumProperty(name="Drawer 5 Height",
                                   items=common_lists.FRONT_HEIGHTS)
    
    drawer_6_height = bpy.props.EnumProperty(name="Drawer 6 Height",
                                   items=common_lists.FRONT_HEIGHTS)
    
    lock_1_drawer = bpy.props.EnumProperty(name="Lock 1 Drawer",
                                           items=LOCK_DRAWER_TYPES,
                                           default = 'None')    
    
    lock_2_drawer = bpy.props.EnumProperty(name="Lock 2 Drawer",
                                           items=LOCK_DRAWER_TYPES,
                                           default = 'None')    
    
    lock_3_drawer = bpy.props.EnumProperty(name="Lock 3 Drawer",
                                           items=LOCK_DRAWER_TYPES,
                                           default = 'None')    
    
    lock_4_drawer = bpy.props.EnumProperty(name="Lock 4 Drawer",
                                           items=LOCK_DRAWER_TYPES,
                                           default = 'None')    
    
    lock_5_drawer = bpy.props.EnumProperty(name="Lock 5 Drawer",
                                           items=LOCK_DRAWER_TYPES,
                                           default = 'None')    
    
    lock_6_drawer = bpy.props.EnumProperty(name="Lock 6 Drawer",
                                           items=LOCK_DRAWER_TYPES,
                                           default = 'None')                        
    
    front_heights = []
    
    drawer_qty_prompt = None
    
    @classmethod
    def poll(cls, context):
        return True
        
    def execute(self, context):
        # THIS NEEDS TO BE RUN TWICE TO AVOID RECAL ERRORS
        utils.run_calculators(utils.get_parent_assembly_bp(self.assembly.obj_bp))
        utils.run_calculators(utils.get_parent_assembly_bp(self.assembly.obj_bp))
        return {'FINISHED'}
        
    def check(self, context):
        if self.drawer_qty_prompt:
            props = props_closet.get_scene_props()
            
            self.drawer_qty_prompt.QuantityValue = int(self.drawer_quantity)
                
            for i in range(1,7):
                drawer_height = self.assembly.get_prompt("Drawer " + str(i) + " Height")
                lock_drawer = self.assembly.get_prompt("Lock " + str(i) + " Drawer")
                slide_type = self.assembly.get_prompt("Drawer " + str(i) + " Slide Type") #DONT REMOVE USED in exec
                if props.closet_defaults.use_32mm_system: 
                    if drawer_height:
                        if not drawer_height.equal:
                            exec("drawer_height.set_value(unit.inch(float(self.drawer_" + str(i) + "_height) / 25.4))")
                if lock_drawer:
                    exec("lock_drawer.set_value(self.lock_" + str(i) + "_drawer)")
                if slide_type:
                    exec("slide_type.set_value(self.drawer_" + str(i) + "_slide)")      
                              
        self.assign_mirror_material(self.assembly.obj_bp)
        utils.run_calculators(self.assembly.obj_bp)
        bpy.ops.cabinetlib.update_scene_from_pointers()
        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport

        # THIS NEEDS TO BE RUN TWICE TO AVOID RECAL ERRORS
        utils.run_calculators(utils.get_parent_assembly_bp(self.assembly.obj_bp))
        utils.run_calculators(utils.get_parent_assembly_bp(self.assembly.obj_bp))
        return True

    def get_front_heights(self):
        self.front_heights = []
        for front in common_lists.FRONT_HEIGHTS:
            self.front_heights.append(front[0])

    def set_properties_from_prompts(self):
        props = props_closet.get_scene_props()
        
        self.get_front_heights()
        
        self.drawer_qty_prompt = self.assembly.get_prompt("Drawer Quantity")
        if self.drawer_qty_prompt:
            self.drawer_quantity = str(self.drawer_qty_prompt.QuantityValue)
                    
            for i in range(1,7):
                drawer_height = self.assembly.get_prompt("Drawer " + str(i) + " Height")
                lock_drawer = self.assembly.get_prompt("Lock " + str(i) + " Drawer") #DONT REMOVE USED in exec
                
                exec("self.lock_" + str(i) + "_drawer = lock_drawer.value()")
                if props.closet_defaults.use_32mm_system:  
                    if drawer_height:
                        value = str(round(drawer_height.DistanceValue * 1000,2))
                        if value in self.front_heights:
                            exec("self.drawer_" + str(i) + "_height = value")

    def assign_mirror_material(self,obj):
        use_mirror = self.assembly.get_prompt("Use Mirror")
        if use_mirror.value():
            if obj.cabinetlib.type_mesh == 'BUYOUT':
                for mat_slot in obj.cabinetlib.material_slots:
                    if "Glass" in mat_slot.name:
                        mat_slot.pointer_name = 'Mirror'  
        else:
            if obj.cabinetlib.type_mesh == 'BUYOUT':
                for mat_slot in obj.cabinetlib.material_slots:
                    if "Glass" in mat_slot.name:
                        mat_slot.pointer_name = 'Glass'  

        for child in obj.children:
            self.assign_mirror_material(child)

    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_assembly_bp = utils.get_assembly_bp(obj)
        self.part = fd_types.Assembly(obj_assembly_bp)
        obj_insert_bp = utils.get_bp(obj,'INSERT')
        self.assembly = fd_types.Assembly(obj_insert_bp)
        self.set_properties_from_prompts()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=450)
    
    def draw_drawer_heights(self,layout):
        col = layout.column(align=True)
        props = props_closet.get_scene_props()
              
        drawer_quantity = self.assembly.get_prompt("Drawer Quantity")
        
        if drawer_quantity:
            row = col.row()
            row.label("Qty:")
            row.prop(self,"drawer_quantity",expand=True)   
            col.separator()     
            for i in range(1,7):
                drawer_height = self.assembly.get_prompt("Drawer " + str(i) + " Height")
                if drawer_height and drawer_quantity.value() >= i:
                    box = col.box()
                    row = box.row(align=True)
                    if props.closet_defaults.use_32mm_system:  
                        row.label("Drawer " + str(i) + " Height:")
                        row.prop(self,'drawer_' + str(i) + '_height',text="")
                    else:
                        drawer_height.draw_prompt(row)
                    row.prop(self,'lock_' + str(i) + '_drawer',text="Lock")

    def is_glass_front(self):
        if "Glass" in self.part.obj_bp.mv.comment:
            return True
        else:
            return False

    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                if self.drawer_qty_prompt:
                    open_drawer = self.assembly.get_prompt('Open')
                    box = layout.box()

                    inset_front = self.assembly.get_prompt('Inset Front')
                    hot = self.assembly.get_prompt('Half Overlay Top')
                    hob = self.assembly.get_prompt('Half Overlay Bottom')
                    hol = self.assembly.get_prompt('Half Overlay Left')
                    hor = self.assembly.get_prompt('Half Overlay Right')
                    use_double_pulls = self.assembly.get_prompt('Use Double Pulls')
                    remove_top_shelf = self.assembly.get_prompt('Remove Top Shelf')
                    remove_bottom_shelf = self.assembly.get_prompt('Remove Bottom Shelf')
                    lift_drawers_from_bottom = self.assembly.get_prompt('Lift Drawers From Bottom')
                    bottom_drawer_space = self.assembly.get_prompt('Bottom Drawer Space')
                    no_pulls = self.assembly.get_prompt('No Pulls')
                    use_mirror = self.assembly.get_prompt("Use Mirror")
                    cleat_loc = self.assembly.get_prompt("Cleat Location")
                    
                    propbox = box.box()
                    propbox.label("Options:",icon='SCRIPT')
                    
                    row = propbox.row()
                    row.label("Open Drawers")
                    row.prop(open_drawer,'PercentageValue',text="")

                    row = propbox.row()
                    if cleat_loc:
                        cleat_loc.draw_prompt(row, text="Cleat Location")

                    row = propbox.row()
                    if lift_drawers_from_bottom:
                        lift_drawers_from_bottom.draw_prompt(row,text="Lift Drawers",split_text=False)
                    if lift_drawers_from_bottom.value():
                        if bottom_drawer_space:
                            bottom_drawer_space.draw_prompt(row,text="")

                    row = propbox.row()
                    if use_double_pulls:
                        use_double_pulls.draw_prompt(row,split_text=False)
                    if no_pulls:
                        no_pulls.draw_prompt(row,split_text=False)
                    
                    row = propbox.row()
                    if remove_top_shelf:
                        remove_top_shelf.draw_prompt(row,split_text=False)                        
                    if remove_bottom_shelf:
                        remove_bottom_shelf.draw_prompt(row,split_text=False)                    
                    
                    row = propbox.row()
                    if inset_front:
                        inset_front.draw_prompt(row,split_text=False)
                        if not inset_front.value():
                            row = propbox.row()
                            row.label("Half Overlays:")
                            hot.draw_prompt(row,split_text=False,text="Top")
                            hob.draw_prompt(row,split_text=False,text="Bottom")
                            hol.draw_prompt(row,split_text=False,text="Left")
                            hor.draw_prompt(row,split_text=False,text="Right")                    

                    if self.is_glass_front():
                        row = propbox.row()
                        use_mirror.draw_prompt(row,split_text=False)

                    self.draw_drawer_heights(box)

class OPS_Drawer_Drop(bpy.types.Operator):
    bl_idname = "closets.insert_drawer_drop"
    bl_label = "Custom drag and drop for drawers insert"

    object_name = bpy.props.StringProperty(name="Object Name")
    product_name = bpy.props.StringProperty(name="Product Name")
    category_name = bpy.props.StringProperty(name="Category Name")
    library_name = bpy.props.StringProperty(name="Library Name")

    insert = None
    default_z_loc = 0.0
    default_height = 0.0
    default_depth = 0.0
    
    openings = []
    objects = []
    
    header_text = "Place Insert   (Esc, Right Click) = Cancel Command  :  (Left Click) = Place Insert"
    
    def execute(self, context):
        return {'FINISHED'}

    def __del__(self):
        bpy.context.area.header_text_set()

    def set_wire_and_xray(self, obj, turn_on):
        if turn_on:
            obj.draw_type = 'WIRE'
        else:
            obj.draw_type = 'TEXTURED'
        obj.show_x_ray = turn_on
        for child in obj.children:
            self.set_wire_and_xray(child,turn_on)

    def get_insert(self,context):
        bpy.ops.object.select_all(action='DESELECT')
        
        if self.object_name in bpy.data.objects:
            bp = bpy.data.objects[self.object_name]
            self.insert = fd_types.Assembly(bp)
        
        if not self.insert:
            lib = context.window_manager.cabinetlib.lib_inserts[self.library_name]
            blend_path = os.path.join(lib.lib_path,self.category_name,self.product_name + ".blend")
            obj_bp = None

            if os.path.exists(blend_path):
                obj_bp = utils.get_group(blend_path)
                self.insert = fd_types.Assembly(obj_bp)
            else:
                self.insert = utils.get_insert_class(context,self.library_name,self.category_name,self.product_name)
    
            if obj_bp:
                pass
            #TODO: SET UP UPDATE OPERATOR
                    # self.insert.update(obj_bp)
            else:
                self.insert.draw()
                self.insert.update()
            
        self.show_openings()
        utils.init_objects(self.insert.obj_bp)
        self.default_z_loc = self.insert.obj_bp.location.z
        self.default_height = self.insert.obj_z.location.z
        self.default_depth = self.insert.obj_y.location.y

    def invoke(self,context,event):
        self.insert = None
        context.window.cursor_set('WAIT')
        self.get_insert(context)
        self.set_wire_and_xray(self.insert.obj_bp, True)
        if self.insert is None:
            bpy.ops.fd_general.error('INVOKE_DEFAULT',message="Could Not Find Insert Class: " + "\\" + self.library_name + "\\" + self.category_name + "\\" + self.product_name)
            return {'CANCELLED'}
        context.window.cursor_set('PAINT_BRUSH')
        context.scene.update() # THE SCENE MUST BE UPDATED FOR RAY CAST TO WORK
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel_drop(self,context,event):
        if self.insert:
            utils.delete_object_and_children(self.insert.obj_bp)
        bpy.context.window.cursor_set('DEFAULT')
        return {'FINISHED'}

    def show_openings(self):
        insert_type = self.insert.obj_bp.mv.placement_type
        for obj in  bpy.context.scene.objects:
            if obj.layers[0]: #Make sure wall is not hidden
                opening = None
                if obj.mv.type_group == 'OPENING':
                    if insert_type in {'INTERIOR','SPLITTER'}:
                        opening = fd_types.Assembly(obj) if obj.mv.interior_open else None
                    if insert_type == 'EXTERIOR':
                        opening = fd_types.Assembly(obj) if obj.mv.exterior_open else None
                    if opening:
                        cage = opening.get_cage()
                        opening.obj_x.hide = True
                        opening.obj_y.hide = True
                        opening.obj_z.hide = True
                        cage.hide_select = False
                        cage.hide = False
                        self.objects.append(cage)

    def selected_opening(self,selected_obj):
        if selected_obj:
            opening = fd_types.Assembly(selected_obj.parent)
            if opening.obj_bp.parent:
                if self.insert.obj_bp.parent is not opening.obj_bp.parent:
                    self.insert.obj_bp.parent = opening.obj_bp.parent
                    self.insert.obj_bp.location = opening.obj_bp.location
                    self.insert.obj_bp.rotation_euler = opening.obj_bp.rotation_euler
                    self.insert.obj_x.location.x = opening.obj_x.location.x
                    self.insert.obj_y.location.y = opening.obj_y.location.y
                    self.insert.obj_z.location.z = opening.obj_z.location.z
                    utils.run_calculators(self.insert.obj_bp)
                    return opening
            
    def set_opening_name(self,obj,name):
        obj.mv.opening_name = name
        for child in obj.children:
            self.set_opening_name(child, name)
        
    def place_insert(self,opening):
        if self.insert.obj_bp.mv.placement_type == 'INTERIOR':
            opening.obj_bp.mv.interior_open = False
        if self.insert.obj_bp.mv.placement_type == 'EXTERIOR':
            opening.obj_bp.mv.exterior_open = False
        if self.insert.obj_bp.mv.placement_type == 'SPLITTER':
            opening.obj_bp.mv.interior_open = False
            opening.obj_bp.mv.exterior_open = False

        utils.copy_assembly_drivers(opening,self.insert)
        self.set_opening_name(self.insert.obj_bp, opening.obj_bp.mv.opening_name)
        self.set_wire_and_xray(self.insert.obj_bp, False)
        
        for obj in self.objects:
            obj.hide = True
            obj.hide_render = True
            obj.hide_select = True

    def insert_drop(self,context,event):
        if len(self.objects) == 0:
            bpy.ops.fd_general.error('INVOKE_DEFAULT',message="There are no openings in this scene.")
            return self.cancel_drop(context,event)
        else:
            selected_point, selected_obj = utils.get_selection_point(context,event,objects=self.objects)
            bpy.ops.object.select_all(action='DESELECT')
            selected_opening = self.selected_opening(selected_obj)
            if selected_opening:
                selected_obj.select = True
    
                if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                    self.place_insert(selected_opening)
                    self.set_backing_bottom_gap(self.insert.obj_bp, selected_opening)
                    context.scene.objects.active = self.insert.obj_bp
                    # THIS NEEDS TO BE RUN TWICE TO AVOID RECAL ERRORS
                    utils.run_calculators(self.insert.obj_bp)
                    utils.run_calculators(self.insert.obj_bp)
                    # TOP LEVEL PRODUCT RECAL
                    utils.run_calculators(utils.get_parent_assembly_bp(self.insert.obj_bp))
                    utils.run_calculators(utils.get_parent_assembly_bp(self.insert.obj_bp))

                    bpy.context.window.cursor_set('DEFAULT')
                    
                    return {'FINISHED'}

            return {'RUNNING_MODAL'}

    def set_backing_bottom_gap(self, insert_bp, selected_opening):
        opening_name = selected_opening.obj_bp.mv.opening_name
        carcass_bp = utils.get_parent_assembly_bp(insert_bp)
        drawer_assembly = fd_types.Assembly(insert_bp)        
        Drawer_Stack_Backing_Gap = drawer_assembly.get_var('Drawer Stack Backing Gap')

        for child in carcass_bp.children:
            if child.lm_closets.is_back_bp:
                if child.mv.opening_name == opening_name:
                    back_assembly = fd_types.Assembly(child)
                    back_assembly.prompt('Backing Insert Gap', 'Drawer_Stack_Backing_Gap', [Drawer_Stack_Backing_Gap])

    def modal(self, context, event):
        context.area.tag_redraw()
        context.area.header_text_set(text=self.header_text)
        
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}
        
        if event.type in {'ESC','RIGHTMOUSE'}:
            self.cancel_drop(context,event)
            return {'FINISHED'}
        
        return self.insert_drop(context,event)


bpy.utils.register_class(PROMPTS_Drawer_Prompts)
bpy.utils.register_class(OPS_Drawer_Drop)
