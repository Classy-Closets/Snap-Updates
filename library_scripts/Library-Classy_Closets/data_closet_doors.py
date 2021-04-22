import bpy
from os import path
from mv import fd_types, unit, utils
from . import mv_closet_defaults as props_closet
from . import common_parts
from . import common_prompts
from . import common_lists
import math

class Doors(fd_types.Assembly):
    
    placement_type = "EXTERIOR"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".door_prompts"
    type_assembly = "INSERT"
    mirror_y = False
    
    door_type = "" # {Base, Tall, Upper, Sink, Suspended}
    striker_depth = unit.inch(3.4)
    striker_thickness = unit.inch(0.75)
    
    def add_common_doors_prompts(self):
        props = props_closet.get_scene_props()
        defaults = props.closet_defaults   
        
        self.add_tab(name='Door Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
        
        common_prompts.add_thickness_prompts(self)
        common_prompts.add_front_overlay_prompts(self)
        common_prompts.add_pull_prompts(self)
        common_prompts.add_door_prompts(self)
        common_prompts.add_door_pull_prompts(self)
        common_prompts.add_door_lock_prompts(self)
        
        if defaults.use_plant_on_top and self.door_type == 'Upper':
            door_height = unit.millimeter(1184)
        else:
            door_height = unit.millimeter(653.288)

        for i in range(1,16):
            self.add_prompt(name="Shelf " + str(i) + " Height",prompt_type='DISTANCE',value=unit.millimeter(76.962),tab_index=0)
            self.add_prompt(name="Shelf " + str(i) + " Setback",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Shelf Stack Height",prompt_type='DISTANCE',value=0,tab_index=0)
        
        self.add_prompt(name="Fill Opening",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Insert Height",prompt_type='DISTANCE',value=door_height,tab_index=0)
        self.add_prompt(name="Offset For Plant On Top",prompt_type='CHECKBOX',value=defaults.use_plant_on_top,tab_index=0)
        self.add_prompt(name="Add Striker",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Striker Depth",prompt_type='DISTANCE',value=self.striker_depth,tab_index=0)
        self.add_prompt(name="Striker Thickness",prompt_type='DISTANCE',value=self.striker_thickness,tab_index=0)
        self.add_prompt(name="Use Mirror",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Glass Shelves",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Doors Backing Gap",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Add Shelves",prompt_type='CHECKBOX',value=0,tab_index=0)
        self.add_prompt(name="Shelf Quantity",prompt_type='QUANTITY',value=3,tab_index=0)
        self.add_prompt(name="Shelf Backing Setback",prompt_type='DISTANCE',value=0,tab_index=0)

        self.add_prompt(name="Top KD",prompt_type='CHECKBOX',value=True,tab_index=0)
        self.add_prompt(name="Bottom KD",prompt_type='CHECKBOX',value=True,tab_index=0)
        self.add_prompt(name="Pard Has Top KD",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Pard Has Bottom KD",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Placed In Invalid Opening",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Has Blind Left Corner",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Has Blind Right Corner",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Left Blind Corner Depth",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Right Blind Corner Depth",prompt_type='DISTANCE',value=0,tab_index=0)

        self.add_prompt(name="Is Slab Door",prompt_type='CHECKBOX',value=True,tab_index=0)
        self.add_prompt(name="Has Center Rail",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Center Rail Distance From Center",prompt_type='DISTANCE',value=0,tab_index=0)

        
        
        self.add_prompt(name="Full Overlay",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Evenly Space Shelves",prompt_type='CHECKBOX',value=True,tab_index=0)
        
        self.add_prompt(
            name="Glass Shelf Thickness",
            prompt_type='COMBOBOX',
            items=['1/4"','3/8"','1/2"'],
            value=0,
            tab_index=0,
            columns=3
            )

        ST = self.get_var("Glass Shelf Thickness", "ST")
        self.add_prompt(name="Glass Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
        self.prompt('Glass Thickness','IF(ST==0,INCH(0.25),IF(ST==1,INCH(0.375),INCH(0.5)))',[ST])

        sgi = self.get_var('cabinetlib.spec_group_index','sgi')
        
        self.prompt('Front Thickness','THICKNESS(sgi,"Slab_Door")',[sgi])

    def set_door_drivers(self,assembly):
        Height = self.get_var('dim_z','Height')
        Door_Gap = self.get_var("Door to Cabinet Gap",'Door_Gap')
        Top_Thickness = self.get_var("Top Thickness",)
        Bottom_Thickness = self.get_var("Bottom Thickness")
        Top_Overlay = self.get_var("Top Overlay")
        Bottom_Overlay = self.get_var("Bottom Overlay")
        eta = self.get_var("Extend Top Amount",'eta')
        eba = self.get_var("Extend Bottom Amount",'eba')
        Front_Thickness = self.get_var("Front Thickness")
        Insert_Height = self.get_var("Insert Height")
        Fill_Opening = self.get_var("Fill Opening")
        Door_Type = self.get_var("Door Type")
        
        assembly.y_loc('-Door_Gap',[Door_Gap,Front_Thickness])
        assembly.z_loc('IF(Door_Type==2,IF(Fill_Opening,0,Height-Insert_Height)+IF(eba==0,-Bottom_Overlay,-eba-Bottom_Thickness),IF(eba==0,-Bottom_Overlay,-eba-Bottom_Thickness))',
                       [Fill_Opening,Door_Type,Height,Insert_Height,eba,Bottom_Thickness,Bottom_Overlay])
        assembly.x_rot(value = 0)
        assembly.y_rot(value = -90)
        assembly.x_dim('IF(Fill_Opening,Height,Insert_Height)+IF(eta==0,Top_Overlay,Top_Thickness+eta)+IF(eba==0,Bottom_Overlay,Bottom_Thickness+eba)',
                       [Fill_Opening,Insert_Height,Height,Top_Overlay,Bottom_Overlay,eta,eba,Top_Thickness,Bottom_Thickness])
        assembly.z_dim('Front_Thickness',[Front_Thickness])
        
    def set_pull_drivers(self,assembly):
        self.set_door_drivers(assembly)
        
        Height = self.get_var('dim_z','Height')
        Pull_Length = assembly.get_var("Pull Length")
        Pull_From_Edge = self.get_var("Pull From Edge")
        Base_Pull_Location = self.get_var("Base Pull Location")
        Tall_Pull_Location = self.get_var("Tall Pull Location")
        Upper_Pull_Location = self.get_var("Upper Pull Location")
        World_Z = self.get_var('world_loc_z','World_Z',transform_type='LOC_Z')
        Insert_Height = self.get_var("Insert Height")
        Fill_Opening = self.get_var("Fill Opening")
        Door_Type = self.get_var("Door Type")
        
        assembly.prompt("Pull X Location",'Pull_From_Edge',[Pull_From_Edge])
        assembly.prompt("Pull Z Location",'IF(Door_Type==0,Base_Pull_Location+(Pull_Length/2),IF(Door_Type==1,IF(Fill_Opening,Height,Insert_Height)-Tall_Pull_Location+(Pull_Length/2)+World_Z,IF(Fill_Opening,Height,Insert_Height)-Upper_Pull_Location-(Pull_Length/2)))',
                        [Door_Type,Base_Pull_Location,Pull_Length,Fill_Opening,Insert_Height,Upper_Pull_Location,Tall_Pull_Location,World_Z,Height])

    def add_shelves(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Shelf_Quantity = self.get_var("Shelf Quantity")
        Shelf_Backing_Setback = self.get_var("Shelf Backing Setback")
        ST = self.get_var("Shelf Thickness",'ST')
        Insert_Height = self.get_var("Insert Height")
        Opening_Height = self.get_var("Opening Height")
        Fill_Opening = self.get_var("Fill Opening")
        Door_Type = self.get_var("Door Type")
        Glass_Shelves = self.get_var("Glass Shelves")
        Shelf_Stack_Height = self.get_var("Shelf Stack Height")
        Fill_Opening = self.get_var("Fill Opening")
        Door_Type = self.get_var("Door Type")

        Add_Shelves = self.get_var("Add Shelves")

        previous_splitter = None          
        
        for i in range(1,16):

            Shelf_Height = self.get_var("Shelf " + str(i) + " Height", 'Shelf_Height')

            shelf_empty = self.add_empty()
            if previous_splitter:
                prev_shelf_z_loc = previous_splitter.get_var('loc_z','prev_shelf_z_loc')
                shelf_empty.z_loc('prev_shelf_z_loc+Shelf_Height',[prev_shelf_z_loc,Shelf_Height])
            else:
                shelf_empty.z_loc('IF(Fill_Opening,Shelf_Height,IF(Door_Type != 2,Shelf_Height,Height-Insert_Height+Shelf_Height))',
                                  [Fill_Opening,Shelf_Height,Insert_Height,Height,Door_Type])   

            sh_z_loc = shelf_empty.get_var('loc_z','sh_z_loc')
                
            splitter = common_parts.add_shelf(self)
            
            Is_Locked_Shelf = splitter.get_var('Is Locked Shelf')
            Adj_Shelf_Setback = splitter.get_var('Adj Shelf Setback')
            Locked_Shelf_Setback = splitter.get_var('Locked Shelf Setback')
            Adj_Shelf_Clip_Gap = splitter.get_var('Adj Shelf Clip Gap')    
            Shelf_Setback = self.get_var("Shelf " + str(i) + " Setback", 'Shelf_Setback')
            
            splitter.x_loc('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)',[Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
            splitter.y_loc('Depth-Shelf_Backing_Setback',[Depth,Shelf_Backing_Setback])
            splitter.z_loc('sh_z_loc',[sh_z_loc])
            splitter.x_rot(value = 0)
            splitter.y_rot(value = 0)
            splitter.z_rot(value = 0)
            splitter.x_dim('Width-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',[Width,Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
            splitter.y_dim('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)+Shelf_Setback+Shelf_Backing_Setback',[Depth,Locked_Shelf_Setback,Is_Locked_Shelf,Adj_Shelf_Setback,Shelf_Setback,Shelf_Backing_Setback])
            splitter.z_dim('ST',[ST])
            splitter.prompt('Hide','IF(Add_Shelves,IF(Shelf_Quantity+1>'+str(i)+',False,True),True)',[Add_Shelves,Shelf_Quantity])
            
            previous_splitter = splitter

    def add_glass_shelves(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Shelf_Qty = self.get_var("Shelf Qty")
        Glass_Thickness = self.get_var("Glass Thickness")
        Insert_Height = self.get_var("Insert Height")
        Fill_Opening = self.get_var("Fill Opening")
        Door_Type = self.get_var("Door Type")
        Glass_Shelves = self.get_var("Glass Shelves")
        
        glass_shelf = common_parts.add_glass_shelf(self)
        
        glass_shelf.draw_as_hidden_line()
        glass_shelf.x_loc(value=0)
        glass_shelf.y_loc('Depth',[Depth])
        glass_shelf.z_loc('IF(Fill_Opening,((Height-(Glass_Thickness*Shelf_Qty))/(Shelf_Qty+1)),IF(Door_Type==2,Height-Insert_Height,0)+((Insert_Height-(Glass_Thickness*Shelf_Qty))/(Shelf_Qty+1)))',
                        [Fill_Opening,Height,Glass_Thickness,Shelf_Qty,Insert_Height,Door_Type])
        glass_shelf.x_rot(value = 0)
        glass_shelf.y_rot(value = 0)
        glass_shelf.z_rot(value = 0)
        glass_shelf.x_dim('Width',[Width])
        glass_shelf.y_dim('-Depth+.00635',[Depth])
        glass_shelf.z_dim('Glass_Thickness',[Glass_Thickness])
        glass_shelf.prompt('Hide','IF(Glass_Shelves==False,True,IF(Shelf_Qty==0,True,False))',[Shelf_Qty,Glass_Shelves])
        glass_shelf.prompt('Z Quantity','Shelf_Qty',[Shelf_Qty])
        glass_shelf.prompt('Z Offset','IF(Fill_Opening,((Height-(Glass_Thickness*Shelf_Qty))/(Shelf_Qty+1))+Glass_Thickness,((Insert_Height-(Glass_Thickness*Shelf_Qty))/(Shelf_Qty+1))+Glass_Thickness)',
                         [Fill_Opening,Height,Glass_Thickness,Shelf_Qty,Insert_Height])
        
    def draw(self):
        self.create_assembly()
        self.obj_bp.mv.export_as_subassembly = True
        
        props = props_closet.get_object_props(self.obj_bp)
        props.is_door_insert_bp = True

        self.add_common_doors_prompts()
        
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Height = self.get_var('dim_z','Height')
        Swing = self.get_var('Swing','Swing')
        LO = self.get_var("Left Overlay",'LO')
        RO = self.get_var("Right Overlay",'RO')
        Vertical_Gap = self.get_var("Vertical Gap",)
        Rotation = self.get_var("Door Rotation",'Rotation')
        Open = self.get_var("Open")
        double_door = self.get_var("Force Double Doors",'double_door')
        DD = self.get_var("Force Double Doors",'DD')
        left_swing = self.get_var("Use Left Swing",'left_swing')
        ST = self.get_var("Shelf Thickness", 'ST')
        Insert_Height = self.get_var("Insert Height")
        Fill_Opening = self.get_var("Fill Opening")
        DDAS = self.get_var("Double Door Auto Switch", 'DDAS')
        No_Pulls = self.get_var("No Pulls")
        Lock_Door = self.get_var("Lock Door")
        Lock_to_Panel = self.get_var("Lock to Panel")
        dt = self.get_var("Division Thickness", 'dt')
        ddl_offset = self.get_var("Double Door Lock Offset", 'ddl_offset')
        Front_Thickness = self.get_var("Front Thickness")
        Door_Gap = self.get_var("Door to Cabinet Gap",'Door_Gap')
        Door_Type = self.get_var("Door Type")
        Offset_For_Plant_On_Top = self.get_var("Offset For Plant On Top")
        Add_Striker = self.get_var("Add Striker")
        Striker_Depth = self.get_var("Striker Depth")
        Striker_Thickness = self.get_var("Striker Thickness")
        Glass_Shelves = self.get_var("Glass Shelves")
        Add_Stiles = self.get_var('Add Stiles')
        Stile_Qnty = self.get_var('Stile Quantity')
        Stile_z = self.get_var('Stile Location')
        Stile_Spacing = self.get_var('Stile Spacing')
        Shelf_Backing_Setback = self.get_var("Shelf Backing Setback")

        FO = self.get_var("Full Overlay",'FO')
        DDHOD = self.get_var("Double Door Half Overlay Difference", 'DDHOD')
        DDFOD = self.get_var("Double Door Full Overlay Difference", 'DDFOD')
        SDFOD = self.get_var("Single Door Full Overlay Difference", 'SDFOD')

        Top_KD = self.get_var("Top KD")
        Bottom_KD = self.get_var("Bottom KD")
        Pard_Has_Top_KD = self.get_var("Pard Has Top KD")
        Pard_Has_Bottom_KD = self.get_var("Pard Has Bottom KD")
        Placed_In_Invalid_Opening = self.get_var("Placed In Invalid Opening")
        Full_Overlay = self.get_var("Full Overlay")
        DDHOD = self.get_var("Double Door Half Overlay Difference", 'DDHOD')
        DDFOD = self.get_var("Double Door Full Overlay Difference", 'DDFOD')
        SDFOD = self.get_var("Single Door Full Overlay Difference", 'SDFOD')

        HBLC = self.get_var("Has Blind Left Corner",'HBLC')
        HBRC = self.get_var("Has Blind Right Corner",'HBRC')
        LBCD = self.get_var("Left Blind Corner Depth",'LBCD')
        RBCD = self.get_var("Right Blind Corner Depth",'RBCD')
        lbcd = self.get_prompt("Left Blind Corner Depth")

        self.prompt('Doors Backing Gap','Insert_Height+ST*2',[Insert_Height,ST])  

        sq = self.get_var("Shelf Quantity",'sq')
        sf1 = self.get_var("Shelf 1 Height",'sf1')
        sf2 = self.get_var("Shelf 2 Height",'sf2')
        sf3 = self.get_var("Shelf 3 Height",'sf3')
        sf4 = self.get_var("Shelf 4 Height",'sf4')
        sf5 = self.get_var("Shelf 5 Height",'sf5')
        sf6 = self.get_var("Shelf 6 Height",'sf6')
        sf7 = self.get_var("Shelf 7 Height",'sf7')
        sf8 = self.get_var("Shelf 8 Height",'sf8')
        sf9 = self.get_var("Shelf 9 Height",'sf9')
        sf10 = self.get_var("Shelf 10 Height",'sf10')
        sf11 = self.get_var("Shelf 11 Height",'sf11')
        sf12 = self.get_var("Shelf 12 Height",'sf12')
        sf13 = self.get_var("Shelf 13 Height",'sf13')
        sf14 = self.get_var("Shelf 14 Height",'sf14')
        sf15 = self.get_var("Shelf 15 Height",'sf15')

        self.prompt('Shelf Stack Height',
                    'sf1+IF(sq>1,sf2,0)+IF(sq>2,sf3,0)+IF(sq>3,sf4,0)+IF(sq>4,sf5,0)+IF(sq>5,sf6,0)+IF(sq>6,sf7,0)+IF(sq>7,sf8,0)+IF(sq>8,sf9,0)+IF(sq>9,sf10,0)+IF(sq>10,sf11,0)+IF(sq>11,sf12,0)+IF(sq>12,sf13,0)+IF(sq>13,sf14,0)+IF(sq>14,sf15,0)', # ? Change height to allow correct door heights
                    [sf1,sf2,sf3,sf4,sf5,sf6,sf7,sf8,sf9,sf10,sf11,sf12,sf13,sf14,sf15,sq])        
        
        #STRIKER
        striker = common_parts.add_door_striker(self)
        striker.x_loc(value = 0)
        striker.y_loc('Striker_Depth',[Striker_Depth])
        striker.z_loc('Height+Striker_Thickness',[Height, Striker_Thickness])
        striker.x_rot(value = 180)
        striker.y_rot(value = 0)
        striker.z_rot(value = 0)
        striker.x_dim('Width',[Width])
        striker.y_dim('Striker_Depth',[Striker_Depth])
        striker.z_dim('ST',[ST])
        striker.prompt('Hide','IF(Add_Striker,False,True)',[Add_Striker])      

        self.add_glass_shelves()
        self.add_shelves()
        
        #LEFT DOOR
        
        left_door = common_parts.add_door(self)
        left_door.set_name("Left Door")
        self.set_door_drivers(left_door)
        left_door.x_loc('IF(HBLC,LBCD-ST/4-INCH(0.375),IF(FO,-LO*2,-LO))',[LO,FO,HBLC,HBRC,ST,LBCD,Width])
        left_door.z_rot('radians(90)-radians(Open*Rotation)',[Open,Rotation])
        left_door.y_dim('IF(OR(HBLC,HBRC),IF(OR(DD,Width-IF(HBLC,LBCD,RBCD)+ST>DDAS),(Width-IF(HBLC,LBCD,RBCD)+ST)/2,(Width-IF(HBLC,LBCD,RBCD)+ST)+ST/6),IF(OR(DD,Width>DDAS), IF(FO,(Width+(ST*2)-DDFOD)/2,(Width+LO+RO)/2-DDHOD) ,IF(FO,Width+(ST*2)-SDFOD,Width+LO+RO))) *-1',[DDHOD,DDFOD,SDFOD,DD,DDAS,Width,LO,RO,Vertical_Gap,Swing,FO,ST,HBLC,HBRC,LBCD,RBCD])
        left_door.prompt('Hide','IF(OR(HBLC,HBRC),IF(OR(double_door,Width-IF(HBLC,LBCD,RBCD)+ST>DDAS,left_swing),False,True),IF(OR(double_door,Width>DDAS,left_swing),False,True))',[double_door,DDAS,left_swing,Width,HBLC,HBRC,LBCD,RBCD,ST])
        left_door.prompt('Door Type','Door_Type',[Door_Type])
        left_door.prompt('Door Swing','0',[])
        left_door.prompt('No Pulls','No_Pulls',[No_Pulls])
        left_door.prompt('CatNum','IF(OR(double_door,Width>DDAS),1005,1006)',[double_door,Width,DDAS])
        
        
        #LEFT PULL
        left_pull = common_parts.add_door_pull(self)
        self.set_pull_drivers(left_pull)
        left_pull.x_loc('IF(HBLC,LBCD-ST/4-INCH(0.375),-LO)',[LO,HBLC,Width,LBCD,ST,HBRC,RBCD,double_door,DDAS])
        left_pull.z_rot('IF(HBLC,radians(90)-radians(Open*Rotation),radians(90)-radians(Open*Rotation))',[Open,Rotation,HBLC])
        #left_pull.y_dim('IF(OR(double_door,Width>DDAS),(Width+LO+RO-Vertical_Gap)/2,(Width+LO+RO))*-1',[double_door,DDAS,Width,LO,RO,Vertical_Gap,Swing,ST,HBLC,HBRC,LBCD,RBCD])
        left_pull.y_dim('IF(OR(HBLC,HBRC),IF(OR(double_door,Width-IF(HBLC,LBCD,RBCD)+ST>DDAS),((Width-IF(HBLC,LBCD,RBCD))/2),(Width-(IF(HBLC,LBCD,RBCD)))),IF(OR(double_door,Width>DDAS),(Width+LO+RO-Vertical_Gap)/2,(Width+LO+RO)))*-1',[double_door,DDAS,Width,LO,RO,Vertical_Gap,Swing,ST,HBLC,HBRC,LBCD,RBCD])
        left_pull.prompt('Hide','IF(No_Pulls,True,IF(OR(HBLC,HBRC),IF(OR(double_door,Width-IF(HBLC,LBCD,RBCD)+ST>DDAS,left_swing),False,True),IF(OR(double_door,Width>DDAS,left_swing),False,True)))',[No_Pulls,double_door,DDAS,left_swing,Width,HBLC,HBRC,LBCD,RBCD,ST])
        
        #RIGHT DOOR
        right_door = common_parts.add_door(self)
        right_door.set_name("Right Door")
        self.set_door_drivers(right_door)
        right_door.x_loc('IF(HBRC,Width-RBCD+ST/4+INCH(0.375),IF(FO, Width+(RO*2), Width+RO))',[Width,RO,FO,HBLC,HBRC,RBCD,ST])
        right_door.z_rot('radians(90)+radians(Open*Rotation)',[Open,Rotation])
        right_door.y_dim('IF(OR(HBLC,HBRC),IF(OR(DD,Width-IF(HBLC,LBCD,RBCD)+ST>DDAS),(Width-IF(HBLC,LBCD,RBCD)+ST)/2,(Width-IF(HBLC,LBCD,RBCD)+ST)+ST/6),IF(OR(DD,Width>DDAS), IF(FO,(Width+(ST*2)-DDFOD)/2,(Width+LO+RO)/2-DDHOD) ,IF(FO,Width+(ST*2)-SDFOD,Width+LO+RO)))',[DDHOD,DDFOD,SDFOD,DD,DDAS,Width,LO,RO,Vertical_Gap,Swing,FO,ST,HBLC,HBRC,LBCD,RBCD])
        right_door.prompt('Hide','IF(OR(HBLC,HBRC),IF(OR(double_door,Width-IF(HBLC,LBCD,RBCD)+ST>DDAS),False,IF(left_swing,True,False)),IF(OR(double_door,Width>DDAS),False,IF(left_swing,True,False)))',[double_door,DDAS,Width,HBLC,HBRC,LBCD,RBCD,ST,left_swing])
        right_door.prompt('Door Type','Door_Type',[Door_Type])
        right_door.prompt('Door Swing','1',[])
        right_door.prompt('No Pulls','No_Pulls',[No_Pulls])
        right_door.prompt('CatNum','IF(OR(double_door,Width>DDAS),1005,1006)',[double_door,Width,DDAS])
        
        right_pull = common_parts.add_door_pull(self)
        self.set_pull_drivers(right_pull)
        #right_pull.x_loc('Width+RO',[Width,RO])
        right_pull.x_loc('IF(HBRC,Width-RBCD+ST/4+INCH(0.375),Width+RO)',[RO,HBRC,Width,RBCD,ST,HBRC,double_door,DDAS])
        right_pull.z_rot('radians(90)+radians(Open*Rotation)',[Open,Rotation])
        #right_pull.y_dim('IF(OR(double_door,Width>DDAS),(Width+LO+RO-Vertical_Gap)/2,(Width+LO+RO))',[double_door,DDAS,Width,LO,RO,Vertical_Gap,Swing])
        right_pull.y_dim('IF(OR(HBLC,HBRC),IF(OR(double_door,Width-IF(HBLC,LBCD,RBCD)+ST>DDAS),((Width-IF(HBLC,LBCD,RBCD))/2),(Width-IF(HBLC,LBCD,RBCD))),IF(OR(double_door,Width>DDAS),(Width+LO+RO-Vertical_Gap)/2,(Width+LO+RO)))',[double_door,DDAS,Width,LO,RO,Vertical_Gap,Swing,ST,HBLC,HBRC,LBCD,RBCD])
        #right_pull.prompt('Hide','IF(No_Pulls,True,IF(OR(double_door,Width>DDAS,left_swing==False),False,True))',[No_Pulls,double_door,DDAS,left_swing,Width])
        right_pull.prompt('Hide','IF(No_Pulls,True,IF(OR(HBLC,HBRC),IF(OR(double_door,Width-IF(HBLC,LBCD,RBCD)+ST>DDAS,left_swing==False),False,True),IF(OR(double_door,Width>DDAS,left_swing==False),False,True)))',[No_Pulls,double_door,DDAS,left_swing,Width,HBLC,HBRC,LBCD,RBCD,ST])
        
        #BOTTOM KD SHELF
        bottom_shelf = common_parts.add_shelf(self)
        bottom_shelf.x_loc('Width',[Width])
        bottom_shelf.y_loc('Depth-Shelf_Backing_Setback',[Depth,Shelf_Backing_Setback])
        bottom_shelf.z_loc('IF(Fill_Opening, 0, IF(Door_Type==2,Height-Insert_Height,0))', 
                    [Door_Type,Insert_Height,Height,ST,Fill_Opening])
        bottom_shelf.x_rot(value = 0)
        bottom_shelf.y_rot(value = 0)
        bottom_shelf.z_rot(value = 180)
        bottom_shelf.x_dim('Width',[Width])
        bottom_shelf.y_dim('Depth-Shelf_Backing_Setback',[Depth,Shelf_Backing_Setback])
        bottom_shelf.z_dim('-ST',[ST])
        bottom_shelf.prompt('Hide', "IF(Placed_In_Invalid_Opening,IF(Door_Type!=2,True,IF(Bottom_KD, False, True)),IF(OR(AND(Pard_Has_Bottom_KD,Door_Type!=2),AND(Pard_Has_Bottom_KD,Fill_Opening)), True, IF(Bottom_KD, False, True)))", [Bottom_KD,Pard_Has_Bottom_KD,Door_Type,Fill_Opening,Placed_In_Invalid_Opening])
        bottom_shelf.prompt('Is Locked Shelf',value = True)

        #TOP KD SHELF
        top_shelf = common_parts.add_shelf(self)
        top_shelf.x_loc('Width',[Width])
        top_shelf.y_loc('Depth-Shelf_Backing_Setback',[Depth,Shelf_Backing_Setback])
        top_shelf.z_loc('IF(Fill_Opening, Height + ST,IF(Door_Type==2,Height + ST,Insert_Height + ST))',
                    [Door_Type,Insert_Height,Height,ST, Fill_Opening])
        top_shelf.x_rot(value = 0)
        top_shelf.y_rot(value = 0)
        top_shelf.z_rot(value = 180)
        top_shelf.x_dim('Width',[Width])
        top_shelf.y_dim('Depth-Shelf_Backing_Setback',[Depth,Shelf_Backing_Setback])
        top_shelf.z_dim('-ST',[ST])
        top_shelf.prompt('Hide', "IF(Placed_In_Invalid_Opening,IF(Door_Type==2,True,IF(Top_KD, False, True)),IF(OR(AND(Pard_Has_Top_KD,Door_Type==2),AND(Pard_Has_Top_KD,Fill_Opening)), True, IF(Top_KD, False, True)))", [Top_KD, Pard_Has_Top_KD,Door_Type,Fill_Opening,Placed_In_Invalid_Opening])
        top_shelf.prompt('Is Locked Shelf',value = True)
        
        opening = common_parts.add_opening(self)
        opening.x_loc(value = 0)
        opening.y_loc(value = 0)
        opening.z_loc('IF(Door_Type==2,0,Insert_Height+ST)',[Door_Type,Insert_Height,ST])
        opening.x_rot(value = 0)
        opening.y_rot(value = 0)
        opening.z_rot(value = 0)
        opening.x_dim('IF(Fill_Opening,0,Width)',[Fill_Opening,Width])
        opening.y_dim('IF(Fill_Opening,0,Depth)',[Fill_Opening,Depth])
        opening.z_dim('IF(Fill_Opening,0,Height-Insert_Height-ST)',[Fill_Opening,Height,Insert_Height,ST])

        # LOCK
        door_lock = common_parts.add_lock(self)
        door_lock.x_loc('IF(OR(double_door,Width>DDAS),Width/2+ddl_offset,IF(left_swing,Width+IF(Lock_to_Panel,dt,-dt),IF(Lock_to_Panel,-dt,dt)))',
                        [Lock_to_Panel,left_swing,Width,double_door,dt,DDAS,ddl_offset])
        door_lock.y_loc('IF(OR(double_door,Width>DDAS),-Front_Thickness-Door_Gap,IF(Lock_to_Panel,Front_Thickness,-Front_Thickness-Door_Gap))',
                        [Lock_to_Panel,Door_Gap,Front_Thickness,dt,DDAS,double_door,Width])
        door_lock.y_rot('IF(OR(double_door,Width>DDAS),radians(90),IF(AND(left_swing,Lock_to_Panel==False),radians(180),0))',
                        [left_swing,double_door,Width,Lock_to_Panel,DDAS])
        door_lock.z_rot('IF(OR(double_door,Width>DDAS),0,IF(Lock_to_Panel==False,0,IF(left_swing,radians(90),radians(-90))))',
                        [Lock_to_Panel,left_swing,double_door,DDAS,Width])
        base_lock_z_location_formula = "IF(Fill_Opening,Height,Insert_Height)-INCH(1.5)"
        tall_lock_z_location_formula = "IF(Fill_Opening,Height/2,Insert_Height/2)-INCH(1.5)"
        upper_lock_z_location_formula = "IF(Fill_Opening,0,Height-Insert_Height)+INCH(1.5)"
        door_lock.z_loc('IF(Door_Type==0,' + base_lock_z_location_formula + ',IF(Door_Type==1,' + tall_lock_z_location_formula + ',' + upper_lock_z_location_formula + '))',
                        [Door_Type,Fill_Opening,Insert_Height,Height])
        door_lock.prompt('Hide', 'IF(Lock_Door==True,IF(Open>0,IF(Lock_to_Panel,False,True),False),True)',[Lock_Door,Open,Lock_to_Panel])
        door_lock.material('Chrome')        
        
        self.update()
        
class PROMPTS_Door_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".door_prompts"
    bl_label = "Door Prompts" 
    bl_description = "This shows all of the available door options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    assembly = None
    part = None

    tabs = bpy.props.EnumProperty(name="Tabs",
                        items=[('DOOR','Door Options','Options for the door'),
                               ('SHELVES','Shelf Options','Options for the shelves')],
                        default = 'DOOR')

    shelf_quantity = bpy.props.EnumProperty(name="Shelf Quantity",
                                   items=[('1',"1",'1'),
                                          ('2',"2",'2'),
                                          ('3',"3",'3'),
                                          ('4',"4",'4'),
                                          ('5',"5",'5'),
                                          ('6',"6",'6'),
                                          ('7',"7",'7'),
                                          ('8',"8",'8'),
                                          ('9',"9",'9'),
                                          ('10',"10",'10'),
                                          ('11',"11",'11'),
                                          ('12',"12",'12'),
                                          ('13',"13",'13'),
                                          ('14',"14",'14'),
                                          ('15',"15",'15')],
                                   default = '3')

    Shelf_1_Height = bpy.props.EnumProperty(name="Shelf 1 Height",
                                    items=common_lists.SHELF_IN_DOOR_HEIGHTS)
    
    Shelf_2_Height = bpy.props.EnumProperty(name="Shelf 2 Height",
                                    items=common_lists.SHELF_IN_DOOR_HEIGHTS)
    
    Shelf_3_Height = bpy.props.EnumProperty(name="Shelf 3 Height",
                                    items=common_lists.SHELF_IN_DOOR_HEIGHTS)
    
    Shelf_4_Height = bpy.props.EnumProperty(name="Shelf 4 Height",
                                    items=common_lists.SHELF_IN_DOOR_HEIGHTS)
    
    Shelf_5_Height = bpy.props.EnumProperty(name="Shelf 5 Height",
                                    items=common_lists.SHELF_IN_DOOR_HEIGHTS)
    
    Shelf_6_Height = bpy.props.EnumProperty(name="Shelf 6 Height",
                                    items=common_lists.SHELF_IN_DOOR_HEIGHTS)
    
    Shelf_7_Height = bpy.props.EnumProperty(name="Shelf 7 Height",
                                    items=common_lists.SHELF_IN_DOOR_HEIGHTS)
    
    Shelf_8_Height = bpy.props.EnumProperty(name="Shelf 8 Height",
                                    items=common_lists.SHELF_IN_DOOR_HEIGHTS)
    
    Shelf_9_Height = bpy.props.EnumProperty(name="Shelf 9 Height",
                                    items=common_lists.SHELF_IN_DOOR_HEIGHTS)
                                    
    Shelf_10_Height = bpy.props.EnumProperty(name="Shelf 10 Height",
                                    items=common_lists.SHELF_IN_DOOR_HEIGHTS)
                                    
    Shelf_11_Height = bpy.props.EnumProperty(name="Shelf 11 Height",
                                    items=common_lists.SHELF_IN_DOOR_HEIGHTS)
                                    
    Shelf_12_Height = bpy.props.EnumProperty(name="Shelf 12 Height",
                                    items=common_lists.SHELF_IN_DOOR_HEIGHTS)
                                    
    Shelf_13_Height = bpy.props.EnumProperty(name="Shelf 13 Height",
                                    items=common_lists.SHELF_IN_DOOR_HEIGHTS)
                                    
    Shelf_14_Height = bpy.props.EnumProperty(name="Shelf 14 Height",
                                    items=common_lists.SHELF_IN_DOOR_HEIGHTS)
                                    
    Shelf_15_Height = bpy.props.EnumProperty(name="Shelf 15 Height",
                                    items=common_lists.SHELF_IN_DOOR_HEIGHTS)
    
    plant_on_top_opening_height = bpy.props.EnumProperty(name="Height",
                                                 items=common_lists.PLANT_ON_TOP_OPENING_HEIGHTS)    
    
    door_opening_height = bpy.props.EnumProperty(name="Height",
                                                 items=common_lists.OPENING_HEIGHTS)  

    shelf_quantity_prompt = None 
    cur_shelf_height = None   

    @classmethod
    def poll(cls, context):
        return True
    
    def check(self, context):
        props = props_closet.get_scene_props()

        if self.shelf_quantity_prompt:
            self.shelf_quantity_prompt.QuantityValue = int(self.shelf_quantity)

        insert_height = self.assembly.get_prompt("Insert Height")
        carcass_height = self.assembly.obj_z.location.z
        fill_opening = self.assembly.get_prompt("Fill Opening")
        evenly_space_shelves = self.assembly.get_prompt("Evenly Space Shelves")
        prompts = [insert_height,fill_opening,evenly_space_shelves]
        
        for i in range(1,int(self.shelf_quantity)+1):
            shelf = self.assembly.get_prompt("Shelf " + str(i) + " Height")
            if shelf:
                if not shelf.equal:
                    exec("self.cur_shelf_height = float(self.Shelf_" + str(i) + "_Height)/1000")
                    #If Shelf was Just Moved
                    if(unit.meter_to_inch(shelf.value()) != unit.meter_to_inch(self.cur_shelf_height)):
                        
                        #Get the height of the previous shelves
                        total_shelf_height = 0
                        for ii in range (1,i+1):
                            exec("self.cur_shelf_height = float(self.Shelf_" + str(ii) + "_Height)/1000")
                            total_shelf_height = total_shelf_height + self.cur_shelf_height
                            #print(unit.meter_to_inch(total_shelf_height))

                        #Adjust All Shelves above shelf that was just moved to evenly space themselves in the remaining space
                        for iii in range(i+1,int(self.shelf_quantity)+1):
                            next_shelf = self.assembly.get_prompt("Shelf " + str(iii) + " Height")
                            if all(prompts):
                                if(not evenly_space_shelves.value()):
                                    if(fill_opening.value()):
                                        hole_count = math.ceil(((carcass_height-total_shelf_height)*1000)/32)
                                    else:
                                        hole_count = math.ceil(((insert_height.value()-total_shelf_height)*1000)/32)
                                    holes_per_shelf = round(hole_count/(int(self.shelf_quantity)+1-i))
                                    if(holes_per_shelf >=3):
                                        next_shelf.set_value(float(common_lists.SHELF_IN_DOOR_HEIGHTS[holes_per_shelf-3][0])/1000)
                                        exec("self.Shelf_" + str(iii) + "_Height = common_lists.SHELF_IN_DOOR_HEIGHTS[holes_per_shelf-3][0]")
                                    else:
                                        next_shelf.set_value(float(common_lists.SHELF_IN_DOOR_HEIGHTS[0][0])/1000)
                                        exec("self.Shelf_" + str(iii) + "_Height = common_lists.SHELF_IN_DOOR_HEIGHTS[0][0]")


                    exec("shelf.DistanceValue = unit.inch(float(self.Shelf_" + str(i) + "_Height) / 25.4)")  
                
                if all(prompts):
                    if(evenly_space_shelves.value()):
                        if(fill_opening.value()):
                            hole_count = math.ceil((carcass_height*1000)/32)
                        else:
                            hole_count = math.ceil((insert_height.value()*1000)/32)
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

        if props.closet_defaults.use_32mm_system:
            insert_height = self.assembly.get_prompt("Insert Height")
            door_type = self.assembly.get_prompt("Door Type")
            offset_for_plant_on_top = self.assembly.get_prompt("Offset For Plant On Top")
            if insert_height:
                if door_type.value() == 'Upper' and offset_for_plant_on_top.value():
                    insert_height.DistanceValue = unit.inch(float(self.plant_on_top_opening_height) / 25.4)
                else:
                    insert_height.DistanceValue = unit.inch(float(self.door_opening_height) / 25.4)
        
        lucite_doors = self.assembly.get_prompt('Lucite Doors')
        draw_type = 'TEXTURED'

        door_type = self.assembly.get_prompt("Door Type")
        fill_opening = self.assembly.get_prompt("Fill Opening").value()
        top_pard_KD = self.assembly.get_prompt("Pard Has Top KD")
        top_KD = self.assembly.get_prompt("Top KD")
        bottom_pard_KD = self.assembly.get_prompt("Pard Has Bottom KD")
        bottom_KD = self.assembly.get_prompt("Bottom KD")

        kd_prompts = [
            top_pard_KD,
            bottom_pard_KD,
            top_KD,
            bottom_KD
        ]
        closet_obj = None
        closet_assembly = None

        closet_obj = utils.get_parent_assembly_bp(self.assembly.obj_bp)
        if closet_obj.lm_closets.is_closet:
            closet_assembly = fd_types.Assembly(closet_obj)

        if all(kd_prompts):
            if(closet_assembly):
                if(closet_assembly.get_prompt("Remove Top Shelf " + self.assembly.obj_bp.mv.opening_name)):
                    does_opening_have_top_KD = closet_assembly.get_prompt("Remove Top Shelf " + self.assembly.obj_bp.mv.opening_name)
                    does_opening_have_bottom_KD = closet_assembly.get_prompt("Remove Bottom Hanging Shelf " + self.assembly.obj_bp.mv.opening_name)
                    if(fill_opening):
                        if(top_KD.value()):
                            does_opening_have_top_KD.set_value(True)
                            top_pard_KD.set_value(True)
                        else:
                            does_opening_have_top_KD.set_value(False)
                            top_pard_KD.set_value(False)

                        if(bottom_KD.value()):
                            does_opening_have_bottom_KD.set_value(True)
                            bottom_pard_KD.set_value(True)
                        else:
                            does_opening_have_bottom_KD.set_value(False)
                            bottom_pard_KD.set_value(False)
                    else:
                        if(door_type.value()=='Upper'):
                            if(top_KD.value()):
                                does_opening_have_top_KD.set_value(True)
                                top_pard_KD.set_value(True)
                            else:
                                does_opening_have_top_KD.set_value(False)
                                top_pard_KD.set_value(False)
                        else:
                            if(bottom_KD.value()):
                                does_opening_have_bottom_KD.set_value(True)
                                bottom_pard_KD.set_value(True)
                            else:
                                does_opening_have_bottom_KD.set_value(False)
                                bottom_pard_KD.set_value(False)
            else:
                placed_in_invalid_opening = self.assembly.get_prompt("Placed In Invalid Opening")
                placed_in_invalid_opening.set_value(True)
                if(fill_opening):
                    top_KD.set_value(False)
                    bottom_KD.set_value(False)
                elif(door_type.value()=='Upper'):
                    top_KD.set_value(False)
                else:
                    bottom_KD.set_value(False)
        
        
        self.assign_mirror_material(self.assembly.obj_bp)
  
        
        for child in self.assembly.obj_bp.children:
            if child.mv.is_cabinet_door:
                if not child.hide:
                    door_assembly = fd_types.Assembly(child)
                    door_style = door_assembly.get_prompt("Door Style")
                    is_slab_door = self.assembly.get_prompt("Is Slab Door")
                    has_center_rail = self.assembly.get_prompt("Has Center Rail")
                    prompts = [door_style,is_slab_door,has_center_rail]
                    if all(prompts):
                        if(door_style.value() == "Slab Door"):
                            is_slab_door.set_value(True)
                            has_center_rail.set_value(False)
                        else:
                            is_slab_door.set_value(False)

                for nchild in child.children:
                    if nchild.cabinetlib.type_mesh == 'CUTPART':
                        if lucite_doors.value():
                            nchild.cabinetlib.cutpart_name = "Lucite_Front"
                            nchild.cabinetlib.edgepart_name = "Lucite_Edges"
                            draw_type = 'WIRE'
                        else:
                            nchild.cabinetlib.cutpart_name = "Slab_Door"
                            nchild.cabinetlib.edgepart_name = "Door_Edges"
                        utils.assign_materials_from_pointers(nchild)
                        nchild.draw_type = draw_type
        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport
        bpy.ops.cabinetlib.update_scene_from_pointers()
        return True
    
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

    def execute(self, context):
        return {'FINISHED'}

    def set_properties_from_prompts(self):
        insert_height = self.assembly.get_prompt("Insert Height")
        door_type = self.assembly.get_prompt("Door Type")
        offset_for_plant_on_top = self.assembly.get_prompt("Offset For Plant On Top")

        self.shelf_quantity_prompt = self.assembly.get_prompt("Shelf Quantity")
        if self.shelf_quantity_prompt:
            self.shelf_quantity = str(self.shelf_quantity_prompt.QuantityValue)

        for i in range(1,16):
            shelf = self.assembly.get_prompt("Shelf " + str(i) + " Height")
            if shelf:
                value = round(shelf.value() * 1000,3)
                for index, height in enumerate(common_lists.SHELF_IN_DOOR_HEIGHTS):
                    if not value >= float(height[0]):
                        exec("self.Shelf_" + str(i) + "_Height = common_lists.SHELF_IN_DOOR_HEIGHTS[index - 1][0]")
                        break

        if insert_height:
            if door_type.value() == 'Upper' and offset_for_plant_on_top.value():
                value = round(insert_height.DistanceValue * 1000,3)
                for index, height in enumerate(common_lists.PLANT_ON_TOP_OPENING_HEIGHTS):
                    if not value >= float(height[0]):
                        self.plant_on_top_opening_height = common_lists.PLANT_ON_TOP_OPENING_HEIGHTS[index - 1][0]
                        break
            else:
                value = round(insert_height.DistanceValue * 1000,3)
                for index, height in enumerate(common_lists.OPENING_HEIGHTS):
                    if not value >= float(height[0]):
                        self.door_opening_height = common_lists.OPENING_HEIGHTS[index - 1][0]
                        break
        
    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj,'INSERT')
        self.assembly = fd_types.Assembly(obj_insert_bp)
        
        obj_assembly_bp = utils.get_assembly_bp(obj)
        self.part = fd_types.Assembly(obj_assembly_bp)
        
        door_type = self.assembly.get_prompt("Door Type")
        fill_opening = self.assembly.get_prompt("Fill Opening").value()

        top_pard_KD = self.assembly.get_prompt("Pard Has Top KD")
        top_KD = self.assembly.get_prompt("Top KD")
        bottom_pard_KD = self.assembly.get_prompt("Pard Has Bottom KD")
        bottom_KD = self.assembly.get_prompt("Bottom KD")

        closet_obj = None
        closet_assembly = None

        closet_obj = utils.get_parent_assembly_bp(self.assembly.obj_bp)
        if closet_obj.lm_closets.is_closet:
            closet_assembly = fd_types.Assembly(closet_obj)

        placed_in_invalid_opening = self.assembly.get_prompt("Placed In Invalid Opening")            

        if(closet_assembly):
            Blind_Corner_Left = closet_assembly.get_prompt("Blind Corner Left")
            Blind_Corner_Right = closet_assembly.get_prompt("Blind Corner Right")
            Blind_Left_Depth = closet_assembly.get_prompt("Blind Left Depth")
            Blind_Right_Depth = closet_assembly.get_prompt("Blind Right Depth")
            Has_Blind_Left_Corner = self.assembly.get_prompt("Has Blind Left Corner")                
            Has_Blind_Right_Corner = self.assembly.get_prompt("Has Blind Right Corner")
            Left_Blind_Corner_Depth = self.assembly.get_prompt("Left Blind Corner Depth")                
            Right_Blind_Corner_Depth = self.assembly.get_prompt("Right Blind Corner Depth")


            kd_prompts = [
                top_pard_KD,
                bottom_pard_KD,
                top_KD,
                bottom_KD
            ]       


            bcp_prompts = [
                Blind_Corner_Left,
                Blind_Corner_Right,
                Blind_Left_Depth,
                Blind_Right_Depth,
                Has_Blind_Left_Corner,
                Has_Blind_Right_Corner,
                Left_Blind_Corner_Depth,
                Right_Blind_Corner_Depth
            ]

            if all(kd_prompts):
                if(closet_assembly.get_prompt("Remove Top Shelf " + self.assembly.obj_bp.mv.opening_name)):
                    does_opening_have_top_KD = closet_assembly.get_prompt("Remove Top Shelf " + self.assembly.obj_bp.mv.opening_name).value()
                    does_opening_have_bottom_KD = closet_assembly.get_prompt("Remove Bottom Hanging Shelf " + self.assembly.obj_bp.mv.opening_name).value()
                    if(fill_opening):
                        if(does_opening_have_top_KD):
                            top_pard_KD.set_value(True)
                            top_KD.set_value(True)
                        else:
                            top_pard_KD.set_value(False)
                            top_KD.set_value(False)

                        if(does_opening_have_bottom_KD):
                            bottom_pard_KD.set_value(True)
                            bottom_KD.set_value(True)
                        else:
                            bottom_pard_KD.set_value(False)
                            bottom_KD.set_value(False)
                    else:
                        if(door_type.value()=='Upper'):
                            if(does_opening_have_top_KD):
                                top_pard_KD.set_value(True)
                                top_KD.set_value(True)
                            else:
                                top_pard_KD.set_value(False)
                                top_KD.set_value(False)
                        else:
                            if(does_opening_have_bottom_KD):
                                bottom_pard_KD.set_value(True)
                                bottom_KD.set_value(True)
                            else:
                                bottom_pard_KD.set_value(False)
                                bottom_KD.set_value(False)


            if(closet_assembly.get_prompt("Opening 1 Height")):
                opening_quantity = 0
                for i in range(1,10):
                    if(fd_types.Assembly(self.assembly.obj_bp.parent).get_prompt("Opening " + str(i) + " Height") == None):
                                    opening_quantity = i - 1
                                    break

                if all(bcp_prompts):
                    if(opening_quantity == 1):
                        if Blind_Corner_Left:
                            Has_Blind_Right_Corner.set_value(False)

                        elif Blind_Corner_Right:
                            Has_Blind_Right_Corner.set_value(True)
                            Has_Blind_Left_Corner.set_value(False)

                        else:
                            Has_Blind_Right_Corner.set_value(False)
                            Has_Blind_Left_Corner.set_value(False)

                    elif(self.assembly.obj_bp.mv.opening_name == '1'):
                        if Blind_Corner_Left:
                            Has_Blind_Left_Corner.set_value(True)
                        else:
                            Has_Blind_Left_Corner.set_value(False)

                    elif(self.assembly.obj_bp.mv.opening_name == str(opening_quantity)):

                        if Blind_Corner_Right:
                            Has_Blind_Right_Corner.set_value(True)
                        else:
                            Has_Blind_Right_Corner.set_value(False)

                    else:
                        Has_Blind_Left_Corner.set_value(False)
                        Has_Blind_Right_Corner.set_value(False)
                    Left_Blind_Corner_Depth.set_value(Blind_Left_Depth.value())
                    Right_Blind_Corner_Depth.set_value(Blind_Right_Depth.value())

        else:
            placed_in_invalid_opening.set_value(True)
            Has_Blind_Left_Corner = self.assembly.get_prompt("Has Blind Left Corner")                
            Has_Blind_Right_Corner = self.assembly.get_prompt("Has Blind Right Corner")
            Left_Blind_Corner_Depth = self.assembly.get_prompt("Left Blind Corner Depth")                
            Right_Blind_Corner_Depth = self.assembly.get_prompt("Right Blind Corner Depth")
            if(fill_opening):
                top_KD.set_value(False)
                bottom_KD.set_value(False)
            elif(door_type.value()=='Upper'):
                top_KD.set_value(False)
            else:
                bottom_KD.set_value(False)
            Has_Blind_Left_Corner.set_value(False)
            Has_Blind_Right_Corner.set_value(False)


        for child in self.assembly.obj_bp.children:
            if child.mv.is_cabinet_door:
                if not child.hide:
                    door_assembly = fd_types.Assembly(child)
                    door_style = door_assembly.get_prompt("Door Style")
                    is_slab_door = self.assembly.get_prompt("Is Slab Door")
                    has_center_rail = self.assembly.get_prompt("Has Center Rail")
                    prompts = [door_style,is_slab_door,has_center_rail]
                    if all(prompts):
                        if(door_style.value() == "Slab Door"):
                            is_slab_door.set_value(True)
                            has_center_rail.set_value(False)
                        else:
                            is_slab_door.set_value(False)
                
        self.set_properties_from_prompts()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=330)
        
    def is_glass_door(self):
        if "Glass" in self.part.obj_bp.mv.comment:
            return True
        else:
            return False
        
    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                props = props_closet.get_scene_props()
                
                door_type = self.assembly.get_prompt("Door Type")
                open_prompt = self.assembly.get_prompt("Open")
                pull_type = self.assembly.get_prompt('Pull Location')
                use_left_swing = self.assembly.get_prompt('Use Left Swing')
                force_double_door = self.assembly.get_prompt('Force Double Doors')
                lucite_doors = self.assembly.get_prompt('Lucite Doors')
                force_double_door = self.assembly.get_prompt('Force Double Doors')
                lucite_doors = self.assembly.get_prompt('Lucite Doors')    
                fill_opening = self.assembly.get_prompt('Fill Opening')       
                lock_door = self.assembly.get_prompt('Lock Door')   
                lock_to_panel = self.assembly.get_prompt('Lock to Panel')   
                insert_height = self.assembly.get_prompt("Insert Height")
                no_pulls = self.assembly.get_prompt("No Pulls")
                shelf_qty = self.assembly.get_prompt("Shelf Qty")
                offset_for_plant_on_top = self.assembly.get_prompt("Offset For Plant On Top") 
                add_striker = self.assembly.get_prompt("Add Striker")
                mid_rail = self.part.get_prompt("Mid Rail")
                glass_panel = self.part.get_prompt("Glass Panel")
                glass_style = self.part.get_prompt("Glass Style")
                use_mirror = self.assembly.get_prompt("Use Mirror")
                glass_shelves = self.assembly.get_prompt("Glass Shelves")
                glass_shelf_thickness = self.assembly.get_prompt("Glass Shelf Thickness")
                add_stiles = self.assembly.get_prompt("Add Stiles")
                stile_qnty = self.assembly.get_prompt("Stile Quantity")
                stile_z = self.assembly.get_prompt("Stile Location")
                stile_spacing = self.assembly.get_prompt("Stile Spacing")
                full_overlay = self.assembly.get_prompt("Full Overlay")
                top_KD = self.assembly.get_prompt("Top KD")
                bottom_KD = self.assembly.get_prompt("Bottom KD")
                placed_in_invalid_opening = self.assembly.get_prompt("Placed In Invalid Opening")       
                is_slab_door = self.assembly.get_prompt("Is Slab Door")
                has_center_rail = self.assembly.get_prompt("Has Center Rail")        
                center_rail_distance_from_center = self.assembly.get_prompt("Center Rail Distance From Center")
                shelf_quantity = self.assembly.get_prompt("Shelf Quantity")   
                evenly_space_shelves = self.assembly.get_prompt("Evenly Space Shelves") 
                add_shelves = self.assembly.get_prompt("Add Shelves")      

                box = layout.box()
                row = box.row()
                if add_shelves:
                    row.prop(self,'tabs',expand=True)

                if self.tabs == 'DOOR':
                    box.label("Opening Options:")
                    add_striker.draw_prompt(box)
                    row = box.row()
                    row.label("Fill Opening")
                    row.prop(fill_opening,'CheckBoxValue',text="") 
                    if fill_opening.value() != True:
                        row = box.row()
                        if props.closet_defaults.use_32mm_system:
                            #print(door_type.value(),offset_for_plant_on_top.value())
                            if door_type.value() == 'Upper' and offset_for_plant_on_top.value():
                                row.prop(self,'plant_on_top_opening_height',text="Opening Height") 
                            else:
                                row.prop(self,'door_opening_height',text="Opening Height") 
                        else:
                            insert_height.draw_prompt(row)
                    
                    row = box.row()
                    glass_shelves.draw_prompt(row)

                    if glass_shelves.value() == True:
                        row = box.row()
                        row.label("Glass Shelf Thickness:")
                        row = box.row()
                        glass_shelf_thickness.draw_prompt(row, text=" ")
                    
                    row = box.row()
                    if shelf_qty:
                        shelf_qty.draw_prompt(row)               
                    
                    box = layout.box()
                    box.label("Door Options:")
                    if door_type:
                        row = box.row()
                        door_type.draw_prompt(row)                       
                        if door_type.value() == 'Base':
                            pull_location = self.assembly.get_prompt('Base Pull Location')
                            pull_location.draw_prompt(box)
                        if door_type.value() == 'Tall':
                            pull_location = self.assembly.get_prompt('Tall Pull Location')
                            pull_location.draw_prompt(box)
                        if door_type.value() == 'Upper':
                            pull_location = self.assembly.get_prompt('Upper Pull Location')
                            pull_location.draw_prompt(box)              
                                       
                           
                    row = box.row()
                    row.label("Open Door")
                    row.prop(open_prompt,'PercentageValue',slider=True,text="")
                    # row = box.row()
                    # row.label("Lucite Doors")
                    # row.prop(lucite_doors,'CheckBoxValue',text="") 
                    #row = box.row()               
                    #row.label("Inset Front")
                    #row.prop(inset_front,'CheckBoxValue',text="")

                    if has_center_rail and is_slab_door and center_rail_distance_from_center:
                        if not is_slab_door.value():
                            row = box.row()
                            row.label("Center Rail")
                            row.prop(has_center_rail,'CheckBoxValue',text="")
                            if has_center_rail.value():
                                row = box.row()
                                row.label("Distance From Center")
                                row.prop(center_rail_distance_from_center,'DistanceValue',text="")

                    if top_KD and bottom_KD:
                        if(placed_in_invalid_opening and placed_in_invalid_opening.value()==False):
                            row = box.row()              
                            row.label("Top KD")
                            row.prop(top_KD,'CheckBoxValue',text="")
                            row = box.row()               
                            row.label("Bottom KD")
                            row.prop(bottom_KD,'CheckBoxValue',text="")
                        else:
                            if(fill_opening.value()==False):
                                if(door_type.value()=='Upper'):
                                    row = box.row()              
                                    row.label("Top KD")
                                    row.prop(top_KD,'CheckBoxValue',text="")
                                    row = box.row()               
                                    row.label("Bottom KD")
                                    row.prop(bottom_KD,'CheckBoxValue',text="")
                                else:
                                    row = box.row()              
                                    row.label("Top KD")
                                    row.prop(top_KD,'CheckBoxValue',text="")

                        row = box.row()
                        row.label("Force Double Door")
                        row.prop(force_double_door,'CheckBoxValue',text="")
                        row = box.row()
                        row.label("Left Swing")
                        row.prop(use_left_swing,'CheckBoxValue',text="")
                        row = box.row()
                        row.label("No Pulls")
                        row.prop(no_pulls,'CheckBoxValue',text="")        
                        row = box.row()
                        row.label("Lock Door")
                        row.prop(lock_door,'CheckBoxValue',text="")   
                        if lock_door.value() and force_double_door.value() == False and self.assembly.obj_x.location.x < unit.inch(24):             
                            row = box.row()
                            row.label("Lock to Panel")
                            row.prop(lock_to_panel,'CheckBoxValue',text="")
                        
                        if full_overlay:
                            row = box.row()
                            row.label("Full Overlay")
                            row.prop(full_overlay,'CheckBoxValue',text="") 
                
                        if mid_rail:
                            row = box.row()
                            row.label("Mid Rail")
                            row.prop(mid_rail, 'CheckBoxValue', text="")

                        if self.is_glass_door():
                            row = box.row()
                            use_mirror.draw_prompt(row)
                            
                        if glass_panel:
                            row = box.row()
                            row.label("Glass Panel")
                            row.prop(glass_panel, 'CheckBoxValue', text="")
                            if glass_panel.value() and glass_style:             
                                row = box.row()
                                glass_style.draw_prompt(row) 
                elif self.tabs == 'SHELVES':
                    row=box.row()
                    row.label("Add Shelves")
                    row.prop(add_shelves, 'CheckBoxValue', text="")
                    if(add_shelves):
                        if(add_shelves.value()):
                            if shelf_quantity:
                                col = box.column(align=True)
                                row = col.row()
                                row.label("Qty:")
                                row.prop(self,"shelf_quantity",expand=True)   
                                col.separator()  
                                row=box.row()
                                row.label("Evenly Space Shelves: ")
                                row.prop(evenly_space_shelves, 'CheckBoxValue', text="")
                                for i in range(1,shelf_quantity.value() + 1):
                                    shelf = self.assembly.get_prompt("Shelf " + str(i) + " Height")
                                    setback = self.assembly.get_prompt("Shelf " + str(i) + " Setback")
                                    if shelf:
                                        row = box.row()
                                        if(evenly_space_shelves.value()):
                                            row.label("Shelf " + str(i) + " Height:")
                                            row.label(str(math.ceil((shelf.value()*1000)/32)) +"H-" + str(round(unit.meter_to_active_unit(shelf.DistanceValue),3)) + '"')
                                        else:
                                            row.label("Shelf " + str(i) + " Height:")
                                            row.prop(self,'Shelf_' + str(i) + '_Height',text="")
                                    
                                    if setback:
                                        row = box.row()
                                        row.label("Shelf " + str(i) + " Setback")
                                        row.prop(setback,'DistanceValue',text="")   
        

class OPS_Doors_Drop(bpy.types.Operator):
    bl_idname = "closets.insert_doors_drop"
    bl_label = "Custom drag and drop for doors insert"

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
        #Clear  to avoid old/duplicate openings
        self.objects.clear()        
        insert_type = self.insert.obj_bp.mv.placement_type
        for obj in  bpy.context.scene.objects:
            #Check to avoid opening that is part of the dropped insert
            if utils.get_parent_assembly_bp(obj) == self.insert.obj_bp:
                continue

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
                    self.set_backing_top_gap(self.insert.obj_bp, selected_opening)
                    context.scene.objects.active = self.insert.obj_bp
                    closet_obj = None
                    closet_assembly = None
                    opening_width = None

                    closet_obj = utils.get_parent_assembly_bp(self.insert.obj_bp)
                    if closet_obj.lm_closets.is_closet:
                        closet_assembly = fd_types.Assembly(closet_obj)

                    if closet_assembly:
                        width = closet_assembly.get_prompt("Opening " + self.insert.obj_bp.mv.opening_name + " Width")
                        if(width):
                            opening_width = width.value()

                        if(closet_assembly.get_prompt("Remove Top Shelf " + self.insert.obj_bp.mv.opening_name)):
                            self.insert.get_prompt("Pard Has Top KD").set_value(closet_assembly.get_prompt("Remove Top Shelf " + self.insert.obj_bp.mv.opening_name).value())
                            self.insert.get_prompt("Pard Has Bottom KD").set_value(closet_assembly.get_prompt("Remove Bottom Hanging Shelf " + self.insert.obj_bp.mv.opening_name).value())
                            if(self.insert.get_prompt("Pard Has Top KD").value() == False and self.insert.get_prompt("Door Type").value()=='Upper'):
                                self.insert.get_prompt("Pard Has Top KD").set_value(True)
                                closet_assembly.get_prompt("Remove Top Shelf " + self.insert.obj_bp.mv.opening_name).set_value(True)

                        if(closet_assembly.get_prompt("Opening 1 Height")):
                            opening_quantity = 0
                            left_depth = 0
                            right_depth = 0
                            if(closet_assembly.get_prompt("Blind Corner Left Depth") and closet_assembly.get_prompt("Blind Corner Right Depth")):
                                left_depth = closet_assembly.get_prompt("Blind Corner Left Depth").value()
                                right_depth = closet_assembly.get_prompt("Blind Corner Right Depth").value()
                                for i in range(1,10):
                                    if(closet_assembly.get_prompt("Opening " + str(i) + " Height") == None):
                                        opening_quantity = (i - 1)
                                        break
                                if(opening_quantity == 1):
                                    if(closet_assembly.get_prompt("Blind Corner Left").value()):
                                        self.insert.get_prompt("Has Blind Left Corner").set_value(True)
                                        self.insert.get_prompt("Use Left Swing").set_value(True)
                                        opening_width = opening_width - left_depth + unit.inch(0.75)
                                    if(closet_assembly.get_prompt("Blind Corner Right").value()):
                                        self.insert.get_prompt("Has Blind Right Corner").set_value(True)
                                        opening_width = opening_width - right_depth + unit.inch(0.75)
                                elif(self.insert.obj_bp.mv.opening_name == '1'):
                                    if(closet_assembly.get_prompt("Blind Corner Left").value()):
                                        self.insert.get_prompt("Has Blind Left Corner").set_value(True)
                                        self.insert.get_prompt("Use Left Swing").set_value(True)
                                        opening_width = opening_width - left_depth + unit.inch(0.75)
                                elif(self.insert.obj_bp.mv.opening_name == str(opening_quantity)):
                                    if(closet_assembly.get_prompt("Blind Corner Right").value()):
                                        self.insert.get_prompt("Has Blind Right Corner").set_value(True)
                                        opening_width = opening_width - right_depth + unit.inch(0.75)
                                else:
                                    self.insert.get_prompt("Has Blind Left Corner").set_value(False)
                                    self.insert.get_prompt("Has Blind Right Corner").set_value(False)

                                self.insert.get_prompt("Left Blind Corner Depth").set_value(left_depth)
                                self.insert.get_prompt("Right Blind Corner Depth").set_value(right_depth)

                        if(opening_width >= unit.inch(21)): 
                                force_double_door = self.insert.get_prompt("Force Double Doors")
                                if(force_double_door):
                                    force_double_door.set_value(True)
                    else:
                        placed_in_invalid_opening = self.insert.get_prompt("Placed In Invalid Opening")
                        placed_in_invalid_opening.set_value(True)
                        self.insert.get_prompt("Has Blind Left Corner").set_value(False)
                        self.insert.get_prompt("Has Blind Right Corner").set_value(False)
                        self.insert.get_prompt("Left Blind Corner Depth").set_value(0)
                        self.insert.get_prompt("Right Blind Corner Depth").set_value(0)

                    # THIS NEEDS TO BE RUN TWICE TO AVOID RECAL ERRORS
                    utils.run_calculators(self.insert.obj_bp)
                    utils.run_calculators(self.insert.obj_bp)
                    # TOP LEVEL PRODUCT RECAL
                    utils.run_calculators(utils.get_parent_assembly_bp(self.insert.obj_bp))
                    utils.run_calculators(utils.get_parent_assembly_bp(self.insert.obj_bp))

                    bpy.context.window.cursor_set('DEFAULT')
                    
                    return {'FINISHED'}

            return {'RUNNING_MODAL'}

    def set_backing_top_gap(self, insert_bp, selected_opening):
        opening_name = selected_opening.obj_bp.mv.opening_name
        carcass_bp = utils.get_parent_assembly_bp(insert_bp)
        doors_assembly = fd_types.Assembly(insert_bp)        
        Doors_Backing_Gap = doors_assembly.get_var('Doors Backing Gap')

        for child in carcass_bp.children:
            if child.lm_closets.is_back_bp:
                if child.mv.opening_name == opening_name:
                    back_assembly = fd_types.Assembly(child)
                    top_insert_backing = back_assembly.get_prompt('Top Insert Backing')

                    if top_insert_backing:
                        back_assembly.prompt('Top Insert Backing', 'Doors_Backing_Gap', [Doors_Backing_Gap])

    def modal(self, context, event):
        context.area.tag_redraw()
        context.area.header_text_set(text=self.header_text)
        
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}
        
        if event.type in {'ESC','RIGHTMOUSE'}:
            self.cancel_drop(context,event)
            return {'FINISHED'}
        
        return self.insert_drop(context,event)


bpy.utils.register_class(PROMPTS_Door_Prompts)
bpy.utils.register_class(OPS_Doors_Drop)
