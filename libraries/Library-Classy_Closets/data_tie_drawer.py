import bpy
from os import path
from mv import fd_types, unit, utils
from . import mv_closet_defaults as props_closet
from . import common_parts
from . import common_prompts
from . import data_pull_hardware
import math

class Tie_Drawer_Box(fd_types.Assembly):
    
    type_assembly = "NONE"
    mirror_y = False
    
    def draw(self):
        self.create_assembly()
        
        self.add_tab(name='Drawer Box Options',tab_type='VISIBLE')
        self.add_prompt(name="Drawer Part Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
        self.add_prompt(name="Division Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
        self.add_prompt(name="Hide",prompt_type='CHECKBOX',value=False,tab_index=0)
        
        Drawer_Width = self.get_var('dim_x','Drawer_Width')
        Drawer_Depth = self.get_var('dim_y','Drawer_Depth')
        Drawer_Height = self.get_var('dim_z','Drawer_Height')
        Drawer_Part_Thickness = self.get_var('Drawer Part Thickness')
        Division_Thickness = self.get_var('Division Thickness')
        Hide = self.get_var('Hide')
        
        top = common_parts.add_panel(self)
        top.set_name("Tie Drawer Top")
        top.x_loc('Drawer_Width',[Drawer_Width])
        top.y_loc(value = 0)
        top.z_loc('Drawer_Height',[Drawer_Height])
        top.x_rot(value = 0)
        top.y_rot(value = 0)
        top.z_rot(value = 90)
        top.x_dim('Drawer_Depth',[Drawer_Depth])
        top.y_dim('Drawer_Width',[Drawer_Width])
        top.z_dim('-Drawer_Part_Thickness',[Drawer_Part_Thickness])
        top.prompt('Hide', "Hide", [Hide])

        bottom = common_parts.add_panel(self)
        bottom.set_name("Tie Drawer Bottom")
        bottom.x_loc('Drawer_Width',[Drawer_Width])
        bottom.y_loc(value = 0)
        bottom.z_loc(value = 0)
        bottom.x_rot(value = 0)
        bottom.y_rot(value = 0)
        bottom.z_rot(value = 90)
        bottom.x_dim('Drawer_Depth',[Drawer_Depth])
        bottom.y_dim('Drawer_Width',[Drawer_Width])
        bottom.z_dim('Drawer_Part_Thickness',[Drawer_Part_Thickness])
        bottom.prompt('Hide', "Hide", [Hide])

        front = common_parts.add_panel(self)
        front.set_name("Tie Drawer Sub Front")
        front.x_loc('Drawer_Width',[Drawer_Width])
        front.y_loc(value = 0)
        front.z_loc('Drawer_Part_Thickness',[Drawer_Part_Thickness])
        front.x_rot(value = 90)
        front.y_rot(value = -90)
        front.z_rot(value = 0)
        front.x_dim('Drawer_Height-(Drawer_Part_Thickness*2)',[Drawer_Height,Drawer_Part_Thickness])
        front.y_dim('Drawer_Width',[Drawer_Width])
        front.z_dim('-Drawer_Part_Thickness',[Drawer_Part_Thickness])
        front.prompt('Hide', "Hide", [Hide])
        
        back = common_parts.add_back(self)
        back.set_name("Tie Drawer Back")
        back.x_loc('Drawer_Width',[Drawer_Width])
        back.y_loc('Drawer_Depth',[Drawer_Depth])
        back.z_loc('Drawer_Part_Thickness',[Drawer_Part_Thickness])
        back.x_rot(value = 90)
        back.y_rot(value = -90)
        back.z_rot(value = 0)
        back.x_dim('Drawer_Height-(Drawer_Part_Thickness*2)',[Drawer_Height,Drawer_Part_Thickness])
        back.y_dim('Drawer_Width',[Drawer_Width])
        back.z_dim('Drawer_Part_Thickness',[Drawer_Part_Thickness])
        back.prompt('Hide', "Hide", [Hide])

        division = common_parts.add_panel(self)
        division.set_name("Tie Drawer Division")
        division.x_loc('(Drawer_Width/2)-(Drawer_Part_Thickness/2)',[Drawer_Width,Drawer_Part_Thickness])
        division.y_loc('Drawer_Part_Thickness',[Drawer_Part_Thickness])
        division.z_loc('Drawer_Height-Drawer_Part_Thickness',[Drawer_Height,Drawer_Part_Thickness])
        division.x_rot(value = 90)
        division.y_rot(value = 90)
        division.z_rot(value = 90)
        division.x_dim('Drawer_Height-(Drawer_Part_Thickness*2)',[Drawer_Height,Drawer_Part_Thickness])
        division.y_dim('Drawer_Depth-(Drawer_Part_Thickness*2)',[Drawer_Depth,Drawer_Part_Thickness])
        division.z_dim('Division_Thickness',[Division_Thickness])
        division.prompt('Hide', "Hide", [Hide])
        
        self.update()
        
        
class Tie_Drawer(fd_types.Assembly):
    # 1. How should these be placed. 
    #    opening split first then indvidually placed or a double insert placed in opening.
    
    # 2. What are the avilable opening heights these go into.
    #    If placing a double can that only go into a certian height opening.
    
    property_id = props_closet.LIBRARY_NAME_SPACE + ".tie_drawer_prompts"
    placement_type = "SPLITTER"
    type_assembly = "INSERT"
    mirror_y = False
    
    top_drawer = False
    
    def add_common_prompts(self):
        self.add_tab(name='Tie Drawer Options',tab_type='VISIBLE')
        self.add_tab(name='Formulas',tab_type='HIDDEN')
    
        self.add_prompt(name="No Pulls",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Place Pull At Bottom",prompt_type='CHECKBOX',value=self.top_drawer,tab_index=0)
        self.add_prompt(name="Rotate Pull",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Drawer Pull From Top",prompt_type='DISTANCE',value=unit.inch(1.5),tab_index=0)
        self.add_prompt(name="Pull Double Max Span",prompt_type='DISTANCE',value=unit.inch(30),tab_index=0)
        self.add_prompt(name="Lock From Top",prompt_type='DISTANCE',value=unit.inch(1.0),tab_index=0)
        self.add_prompt(name="Lock Drawer",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Inset Front",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Open",prompt_type='PERCENTAGE',value=0,tab_index=0)
        self.add_prompt(name="Drawer Content",prompt_type='COMBOBOX',items=['None','2 Tie Rack','2 Belt Rack','Tie and Belt Rack'],value=0,tab_index=0)
        self.add_prompt(name="Add Top Drawer",prompt_type='CHECKBOX',value=True,tab_index=0)
        self.add_prompt(name="Add Bottom Drawer",prompt_type='CHECKBOX',value=True,tab_index=0)
        self.add_prompt(name="Remove Bottom Shelf",prompt_type='CHECKBOX',value=False,tab_index=0)

        self.add_prompt(name="Half Overlay Top",prompt_type='CHECKBOX',value=True,tab_index=0)
        self.add_prompt(name="Half Overlay Bottom",prompt_type='CHECKBOX',value=True,tab_index=0)
        self.add_prompt(name="Half Overlay Left",prompt_type='CHECKBOX',value=True,tab_index=0)
        self.add_prompt(name="Half Overlay Right",prompt_type='CHECKBOX',value=True,tab_index=0)
        self.add_prompt(name="Top Reveal",prompt_type='DISTANCE',value=unit.inch(0.125),tab_index=0)
        self.add_prompt(name="Bottom Reveal",prompt_type='DISTANCE',value=unit.inch(0.0),tab_index=0)
        self.add_prompt(name="Left Reveal",prompt_type='DISTANCE',value=unit.inch(0.0625),tab_index=0)
        self.add_prompt(name="Right Reveal",prompt_type='DISTANCE',value=unit.inch(0.0625),tab_index=0)
        self.add_prompt(name="Inset Reveal",prompt_type='DISTANCE',value=unit.inch(0.125),tab_index=0) 
        self.add_prompt(name="Horizontal Gap",prompt_type='DISTANCE',value=unit.inch(0.125),tab_index=0)
        self.add_prompt(name="Door to Cabinet Gap",prompt_type='DISTANCE',value=unit.inch(0.125),tab_index=0)   
        self.add_prompt(name="Drawer Box Top Gap",prompt_type='DISTANCE',value=unit.inch(0.5),tab_index=0)
        self.add_prompt(name="Drawer Box Bottom Gap",prompt_type='DISTANCE',value=unit.inch(0.5),tab_index=0)
        self.add_prompt(name="Drawer Box Slide Gap",prompt_type='DISTANCE',value=unit.inch(0.5),tab_index=0)
        self.add_prompt(name="Drawer Box Rear Gap",prompt_type='DISTANCE',value=unit.inch(0.5),tab_index=0)
        
        self.add_prompt(name="Left Side Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
        self.add_prompt(name="Right Side Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
        self.add_prompt(name="Top Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
        self.add_prompt(name="Bottom Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
        self.add_prompt(name="Back Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
        self.add_prompt(name="Front Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
        self.add_prompt(name="Division Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
        self.add_prompt(name="Top Overlay",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Bottom Overlay",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Left Overlay",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Right Overlay",prompt_type='DISTANCE',value=0,tab_index=1)
        self.add_prompt(name="Accessories Offset",prompt_type='DISTANCE',value=unit.inch(3.3),tab_index=1)
        self.add_prompt(name="Center Divider Offset",prompt_type='DISTANCE',value=unit.inch(.38),tab_index=1)
        self.add_prompt(name="Rack Offset",prompt_type='DISTANCE',value=unit.inch(0.45),tab_index=1)
        self.add_prompt(name="Shelf Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
        
        common_prompts.add_front_overlay_prompts(self)
        common_prompts.add_thickness_prompts(self)

    def get_assemblies(self,name,index=1):
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z',"Height")
        Depth = self.get_var('dim_y',"Depth")
        Left_Overlay = self.get_var("Left Overlay")
        Right_Overlay = self.get_var("Right Overlay")
        Top_Overlay = self.get_var("Top Overlay")
        Bottom_Overlay = self.get_var("Bottom Overlay")
        Drawer_Box_Slide_Gap = self.get_var("Drawer Box Slide Gap")
        Door_to_Cabinet_Gap = self.get_var("Door to Cabinet Gap")
        Front_Thickness = self.get_var("Front Thickness")
        Drawer_Box_Rear_Gap = self.get_var("Drawer Box Rear Gap")
        Drawer_Box_Top_Gap = self.get_var("Drawer Box Top Gap")
        Drawer_Box_Bottom_Gap = self.get_var("Drawer Box Bottom Gap")
        Place_Pull_At_Bottom = self.get_var("Place Pull At Bottom")
        Rotate_Pull = self.get_var("Rotate Pull")
        Drawer_Pull_From_Top = self.get_var("Drawer Pull From Top")
        Open = self.get_var("Open")
        Inset_Front = self.get_var("Inset Front")
        Remove_Bottom_Shelf = self.get_var("Remove Bottom Shelf")
        Add_Top_Drawer = self.get_var("Add Top Drawer")
        Add_Bottom_Drawer = self.get_var("Add Bottom Drawer")
        Shelf_Thickness = self.get_var("Shelf Thickness")
        
        mid_shelf = common_parts.add_shelf(self)
        mid_shelf.x_loc(value = 0)
        mid_shelf.y_loc(value = 0)
        mid_shelf.z_loc('(Height/2)-(Shelf_Thickness/2)',[Height,Shelf_Thickness])
        mid_shelf.x_rot(value = 0)
        mid_shelf.y_rot(value = 0)
        mid_shelf.z_rot(value = 0)
        mid_shelf.x_dim('Width',[Width])
        mid_shelf.y_dim('Depth',[Depth])
        mid_shelf.z_dim('Shelf_Thickness',[Shelf_Thickness])
        
        bot_shelf = common_parts.add_shelf(self)
        bot_shelf.x_loc(value = 0)
        bot_shelf.y_loc(value = 0)
        bot_shelf.z_loc('-Shelf_Thickness',[Shelf_Thickness])
        bot_shelf.x_rot(value = 0)
        bot_shelf.y_rot(value = 0)
        bot_shelf.z_rot(value = 0)
        bot_shelf.x_dim('Width',[Width])
        bot_shelf.y_dim('Depth',[Depth])
        bot_shelf.z_dim('Shelf_Thickness',[Shelf_Thickness])
        bot_shelf.prompt('Hide', "IF(Remove_Bottom_Shelf,True,False)", [Remove_Bottom_Shelf])        
    
#--------TOP DRAWER
        front = common_parts.add_panel(self)
        front.set_name("Tie Drawer Front")
        front.x_loc('-Left_Overlay',[Left_Overlay])
        front.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(Depth*Open)/' + str(index),[Door_to_Cabinet_Gap,Depth,Open,Inset_Front,Front_Thickness])
        front.z_loc('(Height/2)',[Height,Bottom_Overlay])
        front.x_rot(value = 90)
        front.y_rot(value = 0)
        front.z_rot(value = 0)
        front.x_dim('Width+Left_Overlay+Right_Overlay',[Width,Left_Overlay,Right_Overlay])
        front.y_dim('(Height/2)+Top_Overlay',[Height,Top_Overlay,Bottom_Overlay])
        front.z_dim('Front_Thickness',[Front_Thickness])
        front.prompt('Hide', "IF(Add_Top_Drawer,False,True)", [Add_Top_Drawer])

        drawer = Tie_Drawer_Box()
        drawer.draw()
        drawer.obj_bp.parent = self.obj_bp
        drawer.set_name(name + " Drawer Box")
        drawer.x_loc('Drawer_Box_Slide_Gap',[Drawer_Box_Slide_Gap])
        drawer.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(Depth*Open)/' + str(index),[Door_to_Cabinet_Gap,Depth,Open,Inset_Front,Front_Thickness])
        drawer.z_loc('(Height/2)+Drawer_Box_Bottom_Gap',[Height,Drawer_Box_Bottom_Gap])
        drawer.x_rot(value = 0)
        drawer.y_rot(value = 0)
        drawer.z_rot(value = 0)
        drawer.x_dim('Width-(Drawer_Box_Slide_Gap*2)',[Width,Drawer_Box_Slide_Gap])
        drawer.y_dim('Depth-Drawer_Box_Rear_Gap',[Depth,Drawer_Box_Rear_Gap])
        drawer.z_dim('(Height/2)-Drawer_Box_Top_Gap-Drawer_Box_Bottom_Gap',[Height,Drawer_Box_Top_Gap,Drawer_Box_Bottom_Gap])
        drawer.prompt('Hide', "IF(Add_Top_Drawer,False,True)", [Add_Top_Drawer])

        pull = common_parts.add_drawer_pull(self)
        pull.set_name("Drawer Pull")
        Pull_Length = pull.get_var("Pull Length")
        pull.x_loc('-Left_Overlay',[Left_Overlay])
        pull.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(Depth*Open)/' + str(index),[Door_to_Cabinet_Gap,Depth,Open,Inset_Front,Front_Thickness])
        pull.z_loc('(Height/2)+Bottom_Overlay+INCH(1)',[Height,Bottom_Overlay])
        pull.x_rot(value = 90)
        pull.y_rot(value = 0)
        pull.z_rot(value = 0)
        pull.x_dim('Width+Left_Overlay+Right_Overlay',[Width,Left_Overlay,Right_Overlay])
        pull.y_dim('(Height/2)+Top_Overlay',[Height,Top_Overlay,Bottom_Overlay])
        pull.z_dim('Front_Thickness',[Front_Thickness])
        pull.prompt("Pull X Location",'(Height/2)-Drawer_Pull_From_Top-IF(Rotate_Pull,Pull_Length/2,0)',
                    [Rotate_Pull,Pull_Length,Place_Pull_At_Bottom,Height,Drawer_Pull_From_Top])
        pull.prompt("Pull Z Location",'(Width/2)+Right_Overlay',[Width,Right_Overlay])
        pull.prompt("Pull Rotation",'IF(Rotate_Pull,radians(90),0)',[Rotate_Pull])
        pull.prompt('Hide', "IF(Add_Top_Drawer,False,True)", [Add_Top_Drawer])        

#-------BOTTOM DRAWER 
        
        front = common_parts.add_panel(self)
        front.set_name("Tie Drawer Front")
        front.x_loc('-Left_Overlay',[Left_Overlay])
        front.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(Depth*Open)/' + str(index),[Door_to_Cabinet_Gap,Depth,Open,Inset_Front,Front_Thickness])
        front.z_loc('-Bottom_Overlay', [Bottom_Overlay])
        front.x_rot(value = 90)
        front.y_rot(value = 0)
        front.z_rot(value = 0)
        front.x_dim('Width+Left_Overlay+Right_Overlay',[Width,Left_Overlay,Right_Overlay])
        front.y_dim('(Height/2)+Top_Overlay',[Height,Top_Overlay,Bottom_Overlay])
        front.z_dim('Front_Thickness',[Front_Thickness])
        front.prompt('Hide', "IF(Add_Bottom_Drawer,False,True)", [Add_Bottom_Drawer])

        drawer = Tie_Drawer_Box()
        drawer.draw()
        drawer.obj_bp.parent = self.obj_bp
        drawer.set_name(name + " Drawer Box")
        drawer.x_loc('Drawer_Box_Slide_Gap',[Drawer_Box_Slide_Gap])
        drawer.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(Depth*Open)/' + str(index),[Door_to_Cabinet_Gap,Depth,Open,Inset_Front,Front_Thickness])
        drawer.z_loc('Drawer_Box_Bottom_Gap',[Drawer_Box_Bottom_Gap])
        drawer.x_rot(value = 0)
        drawer.y_rot(value = 0)
        drawer.z_rot(value = 0)
        drawer.x_dim('Width-(Drawer_Box_Slide_Gap*2)',[Width,Drawer_Box_Slide_Gap])
        drawer.y_dim('Depth-Drawer_Box_Rear_Gap',[Depth,Drawer_Box_Rear_Gap])
        drawer.z_dim('(Height/2)-Drawer_Box_Top_Gap-Drawer_Box_Bottom_Gap',[Height,Drawer_Box_Top_Gap,Drawer_Box_Bottom_Gap])
        drawer.prompt('Hide', "IF(Add_Bottom_Drawer,False,True)", [Add_Bottom_Drawer])

        pull = common_parts.add_drawer_pull(self)
        pull.set_name("Drawer Pull")
        Pull_Length = pull.get_var("Pull Length")
        pull.x_loc('-Left_Overlay',[Left_Overlay])
        pull.y_loc('IF(Inset_Front,Front_Thickness,-Door_to_Cabinet_Gap)-(Depth*Open)/' + str(index),[Door_to_Cabinet_Gap,Depth,Open,Inset_Front,Front_Thickness])
        pull.z_loc('-Bottom_Overlay-INCH(1)',[Bottom_Overlay])
        pull.x_rot(value = 90)
        pull.y_rot(value = 0)
        pull.z_rot(value = 0)
        pull.x_dim('Width+Left_Overlay+Right_Overlay',[Width,Left_Overlay,Right_Overlay])
        pull.y_dim('(Height/2)',[Height,Top_Overlay,Bottom_Overlay])
        pull.z_dim('Front_Thickness',[Front_Thickness])
        pull.prompt("Pull X Location",'IF(Place_Pull_At_Bottom,(Height/2)-Drawer_Pull_From_Top-IF(Rotate_Pull,Pull_Length/2,0),Drawer_Pull_From_Top+IF(Rotate_Pull,Pull_Length/2,0))',
                    [Rotate_Pull,Pull_Length,Place_Pull_At_Bottom,Height,Drawer_Pull_From_Top])
        pull.prompt("Pull Z Location",'(Width/2)+Right_Overlay',[Width,Right_Overlay])
        pull.prompt("Pull Rotation",'IF(Rotate_Pull,radians(90),0)',[Rotate_Pull])
        pull.prompt('Hide', "IF(Add_Bottom_Drawer,False,True)", [Add_Bottom_Drawer])
                                                     
    def draw(self):
        self.create_assembly()
        
        self.add_common_prompts()
        
        self.get_assemblies("Top")
        
        self.update()     
        
        
class PROMPTS_Tie_Drawer_Prompts(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".tie_drawer_prompts"
    bl_label = "Tie Drawer Prompts" 
    bl_description = "This shows all of the available tie drawer options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    assembly = None
    
    @classmethod
    def poll(cls, context):
        return True
        
    def execute(self, context):
        return {'FINISHED'}
        
    def check(self, context):
        return True

    def set_properties_from_prompts(self):
        pass
        
    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj,'INSERT')
        self.assembly = fd_types.Assembly(obj_insert_bp)
        self.set_properties_from_prompts()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(330))
    
    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                open_drawer = self.assembly.get_prompt('Open')
                Add_Top_Drawer = self.assembly.get_prompt('Add Top Drawer')
                Add_Bottom_Drawer = self.assembly.get_prompt('Add Bottom Drawer')
                Remove_Bottom_Shelf = self.assembly.get_prompt('Remove Bottom Shelf')
                rotate_pull = self.assembly.get_prompt('Rotate Pull')
                box = layout.box()
                row = box.row()
                row.prop(open_drawer,'PercentageValue',text="Open") 
                row = box.row()
                Add_Top_Drawer.draw_prompt(row)
                row = box.row()
                Add_Bottom_Drawer.draw_prompt(row)  
                row = box.row()
                rotate_pull.draw_prompt(row) 
                row = box.row()
                Remove_Bottom_Shelf.draw_prompt(row)      

bpy.utils.register_class(PROMPTS_Tie_Drawer_Prompts)           