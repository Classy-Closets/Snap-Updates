import bpy
from os import path
from mv import fd_types, unit, utils
from . import mv_closet_defaults as props_closet
from . import common_parts
from . import common_prompts
from . import common_lists

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
            door_height = unit.millimeter(716.95)
        
        self.add_prompt(name="Fill Opening",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Insert Height",prompt_type='DISTANCE',value=door_height,tab_index=0)
        self.add_prompt(name="Offset For Plant On Top",prompt_type='CHECKBOX',value=defaults.use_plant_on_top,tab_index=0)
        self.add_prompt(name="Add Striker",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Striker Depth",prompt_type='DISTANCE',value=self.striker_depth,tab_index=0)
        self.add_prompt(name="Striker Thickness",prompt_type='DISTANCE',value=self.striker_thickness,tab_index=0)
        self.add_prompt(name="Use Mirror",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Glass Shelves",prompt_type='CHECKBOX',value=False,tab_index=0)
        
        self.add_prompt(name="Shelf Qty",
                        prompt_type='QUANTITY',
                        value=0,
                        tab_index=0)
        
        self.add_prompt(name="Shelf Setback",
                        prompt_type='DISTANCE',
                        value=0,
                        tab_index=0)
        
        sgi = self.get_var('cabinetlib.spec_group_index','sgi')
        
        self.prompt('Front Thickness','THICKNESS(sgi,"Slab_Door")',[sgi])
    
    def set_door_drivers(self,assembly):
        Height = self.get_var('dim_z','Height')
        Inset = self.get_var("Inset Front",'Inset')
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
        
        assembly.y_loc('IF(Inset,Front_Thickness,-Door_Gap)',[Inset,Door_Gap,Front_Thickness])
        assembly.z_loc('IF(Door_Type==2,IF(Fill_Opening,0,Height-Insert_Height)+IF(OR(eba==0,Inset),-Bottom_Overlay,-eba-Bottom_Thickness),IF(OR(eba==0,Inset),-Bottom_Overlay,-eba-Bottom_Thickness))',
                       [Fill_Opening,Door_Type,Height,Insert_Height,Inset,eba,Bottom_Thickness,Bottom_Overlay])
        assembly.x_rot(value = 0)
        assembly.y_rot(value = -90)
        assembly.x_dim('IF(Fill_Opening,Height,Insert_Height)+IF(OR(eta==0,Inset),Top_Overlay,Top_Thickness+eta)+IF(OR(eba==0,Inset),Bottom_Overlay,Bottom_Thickness+eba)',
                       [Fill_Opening,Insert_Height,Inset,Height,Top_Overlay,Bottom_Overlay,eta,eba,Top_Thickness,Bottom_Thickness])
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
        Shelf_Qty = self.get_var("Shelf Qty")
        Shelf_Setback = self.get_var("Shelf Setback")
        Shelf_Thickness = self.get_var("Shelf Thickness")
        Insert_Height = self.get_var("Insert Height")
        Fill_Opening = self.get_var("Fill Opening")
        Door_Type = self.get_var("Door Type")
        Glass_Shelves = self.get_var("Glass Shelves")
        
        adj_shelf = common_parts.add_shelf(self)
        
        Is_Locked_Shelf = adj_shelf.get_var('Is Locked Shelf')
        Adj_Shelf_Setback = adj_shelf.get_var('Adj Shelf Setback')
        Locked_Shelf_Setback = adj_shelf.get_var('Locked Shelf Setback')
        Adj_Shelf_Clip_Gap = adj_shelf.get_var('Adj Shelf Clip Gap')        
        
        adj_shelf.draw_as_hidden_line()
        adj_shelf.x_loc('IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap)',[Adj_Shelf_Clip_Gap,Is_Locked_Shelf])
        adj_shelf.y_loc('Depth',[Depth])
        adj_shelf.z_loc('IF(Fill_Opening,((Height-(Shelf_Thickness*Shelf_Qty))/(Shelf_Qty+1)),IF(Door_Type==2,Height-Insert_Height,0)+((Insert_Height-(Shelf_Thickness*Shelf_Qty))/(Shelf_Qty+1)))',
                        [Fill_Opening,Height,Shelf_Thickness,Shelf_Qty,Insert_Height,Door_Type])
        adj_shelf.x_rot(value = 0)
        adj_shelf.y_rot(value = 0)
        adj_shelf.z_rot(value = 0)
        adj_shelf.x_dim('Width-IF(Is_Locked_Shelf,0,Adj_Shelf_Clip_Gap*2)',[Width,Is_Locked_Shelf,Adj_Shelf_Clip_Gap])
        adj_shelf.y_dim('-Depth+IF(Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback)',[Depth,Is_Locked_Shelf,Locked_Shelf_Setback,Adj_Shelf_Setback])
        adj_shelf.z_dim('Shelf_Thickness',[Shelf_Thickness])
        adj_shelf.prompt('Hide','IF(Glass_Shelves,True,IF(Shelf_Qty==0,True,False))',[Shelf_Qty,Glass_Shelves])
        adj_shelf.prompt('Z Quantity','Shelf_Qty',[Shelf_Qty])
        adj_shelf.prompt('Z Offset','IF(Fill_Opening,((Height-(Shelf_Thickness*Shelf_Qty))/(Shelf_Qty+1))+Shelf_Thickness,((Insert_Height-(Shelf_Thickness*Shelf_Qty))/(Shelf_Qty+1))+Shelf_Thickness)',
                         [Fill_Opening,Height,Shelf_Thickness,Shelf_Qty,Insert_Height])

    def add_glass_shelves(self):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z','Height')
        Depth = self.get_var('dim_y','Depth')
        Shelf_Qty = self.get_var("Shelf Qty")
        Shelf_Setback = self.get_var("Shelf Setback")
        Shelf_Thickness = self.get_var("Shelf Thickness")
        Insert_Height = self.get_var("Insert Height")
        Fill_Opening = self.get_var("Fill Opening")
        Door_Type = self.get_var("Door Type")
        Glass_Shelves = self.get_var("Glass Shelves")
        
        adj_shelf = common_parts.add_glass_shelf(self)
        
        Is_Locked_Shelf = adj_shelf.get_var('Is Locked Shelf')
        Adj_Shelf_Setback = adj_shelf.get_var('Adj Shelf Setback')
        Locked_Shelf_Setback = adj_shelf.get_var('Locked Shelf Setback')
        Adj_Shelf_Clip_Gap = adj_shelf.get_var('Adj Shelf Clip Gap')        
        
        adj_shelf.draw_as_hidden_line()
        adj_shelf.x_loc(value = 0)
        adj_shelf.y_loc('Depth',[Depth])
        adj_shelf.z_loc('IF(Fill_Opening,((Height-(Shelf_Thickness*Shelf_Qty))/(Shelf_Qty+1)),IF(Door_Type==2,Height-Insert_Height,0)+((Insert_Height-(Shelf_Thickness*Shelf_Qty))/(Shelf_Qty+1)))',
                        [Fill_Opening,Height,Shelf_Thickness,Shelf_Qty,Insert_Height,Door_Type])
        adj_shelf.x_rot(value = 0)
        adj_shelf.y_rot(value = 0)
        adj_shelf.z_rot(value = 0)
        adj_shelf.x_dim('Width',[Width])
        adj_shelf.y_dim('-Depth+.00635',[Depth])
        adj_shelf.z_dim('Shelf_Thickness-.0127',[Shelf_Thickness])
        adj_shelf.prompt('Hide','IF(Glass_Shelves==False,True,IF(Shelf_Qty==0,True,False))',[Shelf_Qty,Glass_Shelves])
        adj_shelf.prompt('Z Quantity','Shelf_Qty',[Shelf_Qty])
        adj_shelf.prompt('Z Offset','IF(Fill_Opening,((Height-(Shelf_Thickness*Shelf_Qty))/(Shelf_Qty+1))+Shelf_Thickness,((Insert_Height-(Shelf_Thickness*Shelf_Qty))/(Shelf_Qty+1))+Shelf_Thickness)',
                         [Fill_Opening,Height,Shelf_Thickness,Shelf_Qty,Insert_Height])
        
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
        Left_Overlay = self.get_var("Left Overlay")
        Right_Overlay = self.get_var("Right Overlay")
        Vertical_Gap = self.get_var("Vertical Gap",)
        Rotation = self.get_var("Door Rotation",'Rotation')
        Open = self.get_var("Open")
        double_door = self.get_var("Force Double Doors",'double_door')
        left_swing = self.get_var("Use Left Swing",'left_swing')
        Shelf_Thickness = self.get_var("Shelf Thickness")
        Insert_Height = self.get_var("Insert Height")
        Fill_Opening = self.get_var("Fill Opening")
        Double_Door_Auto_Switch = self.get_var("Double Door Auto Switch")
        No_Pulls = self.get_var("No Pulls")
        Inset = self.get_var("Inset Front",'Inset')
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
        striker.z_dim('Shelf_Thickness',[Shelf_Thickness])
        striker.prompt('Hide','IF(Add_Striker,False,True)',[Add_Striker])      

        self.add_glass_shelves()
        self.add_shelves()
        
        #LEFT DOOR
        left_door = common_parts.add_door(self)
        left_door.set_name("Left Door")
        self.set_door_drivers(left_door)
        left_door.x_loc('-Left_Overlay',[Left_Overlay])
        left_door.z_rot('radians(90)-radians(Open*Rotation)',[Open,Rotation])
        left_door.y_dim('IF(OR(double_door,Width>Double_Door_Auto_Switch),(Width+Left_Overlay+Right_Overlay-Vertical_Gap)/2,(Width+Left_Overlay+Right_Overlay))*-1',[double_door,Double_Door_Auto_Switch,Width,Left_Overlay,Right_Overlay,Vertical_Gap,Swing])
        left_door.prompt('Hide','IF(OR(double_door,Width>Double_Door_Auto_Switch,left_swing),False,True)',[double_door,Double_Door_Auto_Switch,left_swing,Width])
        left_door.prompt('Door Type','Door_Type',[Door_Type])
        left_door.prompt('Door Swing','0',[])
        left_door.prompt('No Pulls','No_Pulls',[No_Pulls])
        left_door.prompt('CatNum','IF(OR(double_door,Width>Double_Door_Auto_Switch),1005,1006)',[double_door,Width,Double_Door_Auto_Switch])
        
        #LEFT PULL
        left_pull = common_parts.add_door_pull(self)
        self.set_pull_drivers(left_pull)
        left_pull.x_loc('-Left_Overlay',[Left_Overlay])
        left_pull.z_rot('radians(90)-radians(Open*Rotation)',[Open,Rotation])
        left_pull.y_dim('IF(OR(double_door,Width>Double_Door_Auto_Switch),(Width+Left_Overlay+Right_Overlay-Vertical_Gap)/2,(Width+Left_Overlay+Right_Overlay))*-1',[double_door,Double_Door_Auto_Switch,Width,Left_Overlay,Right_Overlay,Vertical_Gap,Swing])
        left_pull.prompt('Hide','IF(No_Pulls,True,IF(OR(double_door,Width>Double_Door_Auto_Switch,left_swing),False,True))',[No_Pulls,double_door,Double_Door_Auto_Switch,left_swing,Width])
        
        #RIGHT DOOR
        right_door = common_parts.add_door(self)
        right_door.set_name("Right Door")
        self.set_door_drivers(right_door)
        right_door.x_loc('Width+Right_Overlay',[Width,Right_Overlay])
        right_door.z_rot('radians(90)+radians(Open*Rotation)',[Open,Rotation])
        right_door.y_dim('IF(OR(double_door,Width>Double_Door_Auto_Switch),(Width+Left_Overlay+Right_Overlay-Vertical_Gap)/2,(Width+Left_Overlay+Right_Overlay))',[double_door,Double_Door_Auto_Switch,Width,Left_Overlay,Right_Overlay,Vertical_Gap,Swing])
        right_door.prompt('Hide','IF(OR(double_door,Width>Double_Door_Auto_Switch,left_swing==False),False,True)',[double_door,Double_Door_Auto_Switch,left_swing,Width])
        right_door.prompt('Door Type','Door_Type',[Door_Type])
        right_door.prompt('Door Swing','1',[])
        right_door.prompt('No Pulls','No_Pulls',[No_Pulls])
        right_door.prompt('CatNum','IF(OR(double_door,Width>Double_Door_Auto_Switch),1005,1006)',[double_door,Width,Double_Door_Auto_Switch])
        
        #RIGHT PULL
        right_pull = common_parts.add_door_pull(self)
        self.set_pull_drivers(right_pull)
        right_pull.x_loc('Width+Right_Overlay',[Width,Right_Overlay])
        right_pull.z_rot('radians(90)+radians(Open*Rotation)',[Open,Rotation])
        right_pull.y_dim('IF(OR(double_door,Width>Double_Door_Auto_Switch),(Width+Left_Overlay+Right_Overlay-Vertical_Gap)/2,(Width+Left_Overlay+Right_Overlay))',[double_door,Double_Door_Auto_Switch,Width,Left_Overlay,Right_Overlay,Vertical_Gap,Swing])
        right_pull.prompt('Hide','IF(No_Pulls,True,IF(OR(double_door,Width>Double_Door_Auto_Switch,left_swing==False),False,True))',[No_Pulls,double_door,Double_Door_Auto_Switch,left_swing,Width])
        
        shelf = common_parts.add_shelf(self)
        shelf.x_loc('Width',[Width])
        shelf.y_loc('Depth',[Depth])
        shelf.z_loc('IF(Door_Type==2,Height-Insert_Height,Insert_Height+Shelf_Thickness)',
                    [Door_Type,Insert_Height,Height,Shelf_Thickness])
        shelf.x_rot(value = 0)
        shelf.y_rot(value = 0)
        shelf.z_rot(value = 180)
        shelf.x_dim('Width',[Width])
        shelf.y_dim('Depth',[Depth])
        shelf.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        shelf.prompt('Hide','IF(Fill_Opening,True,False)',[Fill_Opening])
        shelf.prompt('Is Locked Shelf',value = True)
        
        opening = common_parts.add_opening(self)
        opening.x_loc(value = 0)
        opening.y_loc(value = 0)
        opening.z_loc('IF(Door_Type==2,0,Insert_Height+Shelf_Thickness)',[Door_Type,Insert_Height,Shelf_Thickness])
        opening.x_rot(value = 0)
        opening.y_rot(value = 0)
        opening.z_rot(value = 0)
        opening.x_dim('IF(Fill_Opening,0,Width)',[Fill_Opening,Width])
        opening.y_dim('IF(Fill_Opening,0,Depth)',[Fill_Opening,Depth])
        opening.z_dim('IF(Fill_Opening,0,Height-Insert_Height-Shelf_Thickness)',[Fill_Opening,Height,Insert_Height,Shelf_Thickness])

        # LOCK
        door_lock = common_parts.add_lock(self)
        door_lock.x_loc('IF(OR(double_door,Width>Double_Door_Auto_Switch),Width/2+ddl_offset,IF(left_swing,Width+IF(Lock_to_Panel,dt,-dt),IF(Lock_to_Panel,-dt,dt)))',
                        [Lock_to_Panel,left_swing,Width,double_door,dt,Double_Door_Auto_Switch,ddl_offset])
        door_lock.y_loc('IF(OR(double_door,Width>Double_Door_Auto_Switch),IF(Inset,0,-Front_Thickness-Door_Gap),IF(Lock_to_Panel,Front_Thickness,IF(Inset,0,-Front_Thickness-Door_Gap)))',
                        [Lock_to_Panel,Inset,Door_Gap,Front_Thickness,dt,Double_Door_Auto_Switch,double_door,Width])
        door_lock.y_rot('IF(OR(double_door,Width>Double_Door_Auto_Switch),radians(90),IF(AND(left_swing,Lock_to_Panel==False),radians(180),0))',
                        [left_swing,double_door,Width,Lock_to_Panel,Double_Door_Auto_Switch])
        door_lock.z_rot('IF(OR(double_door,Width>Double_Door_Auto_Switch),0,IF(Lock_to_Panel==False,0,IF(left_swing,radians(90),radians(-90))))',
                        [Lock_to_Panel,left_swing,double_door,Double_Door_Auto_Switch,Width])
        base_lock_z_location_formula = "IF(Fill_Opening,Height,Insert_Height)-INCH(1.5)"
        tall_lock_z_location_formula = "IF(Fill_Opening,Height/2,Insert_Height/2)-INCH(1.5)"
        upper_lock_z_location_formula = "IF(Fill_Opening,0,Height-Insert_Height)+INCH(1.5)"
        door_lock.z_loc('IF(Door_Type==0,' + base_lock_z_location_formula + ',IF(Door_Type==1,' + tall_lock_z_location_formula + ',' + upper_lock_z_location_formula + '))',
                        [Door_Type,Fill_Opening,Insert_Height,Inset,Height])
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
    
    plant_on_top_opening_height = bpy.props.EnumProperty(name="Height",
                                                 items=common_lists.PLANT_ON_TOP_OPENING_HEIGHTS)    
    
    door_opening_height = bpy.props.EnumProperty(name="Height",
                                                 items=common_lists.OPENING_HEIGHTS)    

    

    @classmethod
    def poll(cls, context):
        return True
    
    def check(self, context):
        props = props_closet.get_scene_props()
        
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
        
        
        self.assign_mirror_material(self.assembly.obj_bp)
  
        
        for child in self.assembly.obj_bp.children:
            if child.mv.is_cabinet_door:
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
        if insert_height:
            if door_type.value() == 'Upper' and offset_for_plant_on_top.value():
                value = round(insert_height.DistanceValue * 1000,2)
                for index, height in enumerate(common_lists.PLANT_ON_TOP_OPENING_HEIGHTS):
                    if not value >= float(height[0]):
                        self.plant_on_top_opening_height = common_lists.PLANT_ON_TOP_OPENING_HEIGHTS[index - 1][0]
                        break
            else:
                value = round(insert_height.DistanceValue * 1000,2)
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
                inset_front = self.assembly.get_prompt('Inset Front')
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
                add_stiles = self.assembly.get_prompt("Add Stiles")
                stile_qnty = self.assembly.get_prompt("Stile Quantity")
                stile_z = self.assembly.get_prompt("Stile Location")
                stile_spacing = self.assembly.get_prompt("Stile Spacing")
                
                
                box = layout.box()
                box.label("Opening Options:")
                add_striker.draw_prompt(box)
                row = box.row()
                row.label("Fill Opening")
                row.prop(fill_opening,'CheckBoxValue',text="") 
                if fill_opening.value() != True:
                    row = box.row()
                    if props.closet_defaults.use_32mm_system:
                        print(door_type.value(),offset_for_plant_on_top.value())
                        if door_type.value() == 'Upper' and offset_for_plant_on_top.value():
                            row.prop(self,'plant_on_top_opening_height',text="Opening Height") 
                        else:
                            row.prop(self,'door_opening_height',text="Opening Height") 
                    else:
                        insert_height.draw_prompt(row)
                
                row = box.row()
                glass_shelves.draw_prompt(row)
                
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
#                 row = box.row()
#                 row.label("Lucite Doors")
#                 row.prop(lucite_doors,'CheckBoxValue',text="") 
                row = box.row()               
                row.label("Inset Front")
                row.prop(inset_front,'CheckBoxValue',text="")
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
        
bpy.utils.register_class(PROMPTS_Door_Prompts)        
        