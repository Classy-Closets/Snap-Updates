import bpy
from mv import unit, fd_types, utils
from . import mv_closet_defaults as props_closet
from . import common_parts
from . import common_lists

def add_horizontal_cubbie_slots(part,insert):
    default_props = props_closet.get_scene_props().closet_defaults
    machining = default_props.machining_defaults   
        
    Part_Thickness = part.get_var('dim_z','Part_Thickness')
    Part_Length = part.get_var('dim_x','Part_Length')
    Part_Width = part.get_var('dim_y','Part_Width')
    Vertical_Quantity = insert.get_var('Vertical Quantity')

    for i in range(1, 15):
        opening_space_formula = "((Part_Length-(Part_Thickness*Vertical_Quantity))/(Vertical_Quantity+1))"
        qty_spacing = 'IF(' + str(i) + '>Vertical_Quantity,0,' + str(i) + ')+IF(' + str(i) + '>Vertical_Quantity,0,Part_Thickness*' + str(i - 1) + ')'

        first_notch = part.add_machine_token('Horz Cubbie Slot Notch ' + str(i),'3SIDEDNOTCH','5','1')
        first_notch[1].add_driver(first_notch[0],'is_disabled','IF(Vertical_Quantity>=' + str(i)  + ',False,True)',[Vertical_Quantity])
        first_notch[1].add_driver(first_notch[0],'dim_in_x',opening_space_formula + "*" + qty_spacing,[Part_Length,Part_Thickness,Vertical_Quantity])
        first_notch[1].add_driver(first_notch[0],'end_dim_in_x',"(" + opening_space_formula + "*" + qty_spacing + ")+Part_Thickness",[Part_Length,Part_Thickness,Vertical_Quantity])
        first_notch[1].add_driver(first_notch[0],'dim_in_y','(fabs(Part_Width)/2)+MILLIMETER(6)',[Part_Width])
        first_notch[1].add_driver(first_notch[0],'end_dim_in_y','(fabs(Part_Width)/2)+MILLIMETER(6)',[Part_Width])
        first_notch[1].add_driver(first_notch[0],'dim_in_z','fabs(Part_Thickness)',[Part_Thickness])
        first_notch[1].lead_in = machining.router_lead
        first_notch[1].tool_number = machining.tool_number

def add_vertical_cubbie_slots(part,insert):
    default_props = props_closet.get_scene_props().closet_defaults
    machining = default_props.machining_defaults   
        
    Part_Thickness = part.get_var('dim_z','Part_Thickness')
    Part_Length = part.get_var('dim_x','Part_Length')
    Part_Width = part.get_var('dim_y','Part_Width')
    Horizontal_Quantity = insert.get_var('Horizontal Quantity')

    for i in range(1, 15):
        opening_space_formula = "((fabs(Part_Length)-(fabs(Part_Thickness)*Horizontal_Quantity))/(Horizontal_Quantity+1))"
        qty_spacing = 'IF(' + str(i) + '>Horizontal_Quantity,0,' + str(i) + ')+IF(' + str(i) + '>Horizontal_Quantity,0,fabs(Part_Thickness)*' + str(i - 1) + ')'

        first_notch = part.add_machine_token('Vert Cubbie Slot Notch ' + str(i),'3SIDEDNOTCH','5','2')
        first_notch[1].add_driver(first_notch[0],'is_disabled','IF(Horizontal_Quantity>=' + str(i)  + ',False,True)',[Horizontal_Quantity])
        first_notch[1].add_driver(first_notch[0],'dim_in_x',opening_space_formula + "*" + qty_spacing,[Part_Length,Part_Thickness,Horizontal_Quantity])
        first_notch[1].add_driver(first_notch[0],'end_dim_in_x',"(" + opening_space_formula + "*" + qty_spacing + ")-Part_Thickness",[Part_Length,Part_Thickness,Horizontal_Quantity])
        first_notch[1].add_driver(first_notch[0],'dim_in_y','(fabs(Part_Width)/2)+MILLIMETER(6)',[Part_Width])
        first_notch[1].add_driver(first_notch[0],'end_dim_in_y','(fabs(Part_Width)/2)+MILLIMETER(6)',[Part_Width])
        first_notch[1].add_driver(first_notch[0],'dim_in_z','fabs(Part_Thickness)',[Part_Thickness])
        first_notch[1].lead_in = machining.router_lead
        first_notch[1].tool_number = machining.tool_number

class Shoe_Cubbies(fd_types.Assembly):
    """ This shoe cubby insert allows users to specify the quantity of vertical and horizontal dividers
        users can determine if the shoe cubbies are placed at the top, bottom, or if they should fill the entire opening
    """
    
    placement_type = "SPLITTER"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".shoe_cubbies"
    type_assembly = "INSERT"
    mirror_y = False

    def draw(self):
        self.create_assembly()
        
        self.add_tab("Shoe Cubby Options", 'VISIBLE')
        self.add_prompt(name="Cubby Placement",prompt_type='COMBOBOX',value=0,tab_index=0,items=['Bottom','Top','Fill'],columns=3)
        self.add_prompt(name="Horizontal Quantity",prompt_type='QUANTITY',value=2,tab_index=0)
        self.add_prompt(name="Vertical Quantity",prompt_type='QUANTITY',value=2,tab_index=0)
        self.add_prompt(name="Cubby Setback",prompt_type='DISTANCE',value=unit.inch(0.25),tab_index=0)
        self.add_prompt(name="Divider Thickness",prompt_type='DISTANCE',value=unit.inch(.25),tab_index=0)
        self.add_prompt(name="Shelf Thickness",prompt_type='DISTANCE',value=unit.inch(.75),tab_index=0)
        self.add_prompt(name="Vertical Spacing",prompt_type='DISTANCE',value=unit.inch(.25),tab_index=0)
        self.add_prompt(name="Horizontal Spacing",prompt_type='DISTANCE',value=unit.inch(.25),tab_index=0)
        self.add_prompt(name="Cubby Height",prompt_type='DISTANCE',value=unit.millimeter(557.276),tab_index=0)
        
        Width = self.get_var('dim_x','Width')
        Height = self.get_var('dim_z',"Height")
        Depth = self.get_var('dim_y',"Depth")
        Horizontal_Quantity = self.get_var("Horizontal Quantity")
        Vertical_Quantity = self.get_var("Vertical Quantity")
        Cubby_Setback = self.get_var("Cubby Setback")
        Cubby_Height = self.get_var("Cubby Height")
        Divider_Thickness = self.get_var("Divider Thickness")
        Shelf_Thickness = self.get_var("Shelf Thickness")
        Cubby_Placement = self.get_var("Cubby Placement")
        
        top_shelf = common_parts.add_shelf(self)
        top_shelf.prompt("Is Locked Shelf",value=True)
        top_shelf.x_loc(value = 0)
        top_shelf.y_loc(value = 0)
        top_shelf.z_loc('IF(Cubby_Placement==0,Cubby_Height+Shelf_Thickness,Height-Cubby_Height)',[Shelf_Thickness,Cubby_Placement,Cubby_Height,Height])
        top_shelf.x_rot(value = 0)
        top_shelf.y_rot(value = 0)
        top_shelf.z_rot(value = 0)
        top_shelf.x_dim('Width',[Width])
        top_shelf.y_dim('Depth',[Depth])
        top_shelf.z_dim('-Shelf_Thickness',[Shelf_Thickness])
        top_shelf.prompt('Hide','IF(Cubby_Placement==2,True,False)',[Cubby_Placement])

        opening = common_parts.add_opening(self)
        opening.x_loc(value = 0)
        opening.y_loc(value = 0)
        opening.z_loc('IF(Cubby_Placement==0,Cubby_Height+Shelf_Thickness,0)',[Cubby_Placement,Cubby_Height,Shelf_Thickness])
        opening.x_rot(value = 0)
        opening.y_rot(value = 0)
        opening.z_rot(value = 0)
        opening.x_dim('IF(Cubby_Placement==2,0,Width)',[Cubby_Placement,Width])
        opening.y_dim('IF(Cubby_Placement==2,0,Depth)',[Cubby_Placement,Depth])
        opening.z_dim('IF(Cubby_Placement==2,0,Height-Cubby_Height-Shelf_Thickness)',[Cubby_Placement,Height,Cubby_Height,Shelf_Thickness])

        for i in range(1,30):
            vert_spacing = "((Width-(Divider_Thickness*Vertical_Quantity))/(Vertical_Quantity+1))"
            vert_qty = 'IF(' + str(i) + '>Vertical_Quantity,0,' + str(i) + ')+IF(' + str(i) + '>Vertical_Quantity,0,Divider_Thickness*' + str(i - 1) + ')'
            
            vert = common_parts.add_divider(self)
            vert.set_name("Vertical Divider")
            vert.x_loc('(' + vert_spacing + ')*' + vert_qty,[Width,Divider_Thickness,Vertical_Quantity])
            vert.y_loc("Depth",[Depth])
            vert.z_loc('IF(Cubby_Placement==1,Height-Cubby_Height,0)',[Cubby_Placement,Height,Cubby_Height])
            vert.x_rot(value = 0)
            vert.y_rot(value = -90)
            vert.z_rot(value = 0)
            vert.x_dim("IF(Cubby_Placement==2,Height,Cubby_Height)",[Height,Cubby_Placement,Cubby_Height])
            vert.y_dim("(Depth*-1)+Cubby_Setback",[Depth,Cubby_Setback])
            vert.z_dim("-Divider_Thickness",[Divider_Thickness])
            vert.prompt('Hide','IF(' + str(i) + '>Vertical_Quantity,True,False)',[Vertical_Quantity])
            
            start_placement = "IF(Cubby_Placement==1,Height-Cubby_Height,0)"
            horz_spacing = "((IF(Cubby_Placement==2,Height,Cubby_Height)-(Divider_Thickness*Horizontal_Quantity))/(Horizontal_Quantity+1))"
            horz_qty = 'IF(' + str(i) + '>Horizontal_Quantity,0,' + str(i) + ')+IF(' + str(i) + '>Horizontal_Quantity,0,Divider_Thickness*' + str(i - 1) + ')'
            
            horz = common_parts.add_divider(self)
            horz.set_name("Horizontal Divider")
            horz.x_loc(value = 0)
            horz.y_loc("Depth",[Depth])
            horz.z_loc(start_placement + '+(' + horz_spacing + ')*' + horz_qty,[Cubby_Placement,Cubby_Height,Height,Divider_Thickness,Horizontal_Quantity])
            horz.x_rot(value = 0)
            horz.y_rot(value = 0)
            horz.z_rot(value = 0)
            horz.x_dim("Width",[Width])
            horz.y_dim("(Depth*-1)+Cubby_Setback",[Depth,Cubby_Setback])
            horz.z_dim("Divider_Thickness",[Divider_Thickness])
            horz.prompt('Hide','IF(' + str(i) + '>Horizontal_Quantity,True,False)',[Horizontal_Quantity])
            
        self.update()

class PROMPTS_Shoe_Cubbies(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".shoe_cubbies"
    bl_label = "Shoe Cubbies Prompts" 
    bl_description = "This shows all of the available shoe cubby options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    cubby_height = bpy.props.EnumProperty(name="Cubby Height",
                                          items=common_lists.OPENING_HEIGHTS,
                                          default = '557.276')     
    
    assembly = None
    
    vertical_opening_space = 0
    horizontal_opening_space = 0
    
    @classmethod
    def poll(cls, context):
        return True
        
    def check(self, context):
        props = props_closet.get_scene_props()
        if props.closet_defaults.use_32mm_system:
            cubby_height = self.assembly.get_prompt("Cubby Height")
            if cubby_height:
                cubby_height.DistanceValue = unit.inch(float(self.cubby_height) / 25.4)

        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport
        return True
        
    def execute(self, context):
        return {'FINISHED'}

    def set_properties_from_prompts(self):
        cubby_height = self.assembly.get_prompt("Cubby Height")
        if cubby_height:
            value = round(cubby_height.DistanceValue * 1000,2)
            for index, height in enumerate(common_lists.OPENING_HEIGHTS):
                if not value >= float(height[0]):
                    self.cubby_height = common_lists.OPENING_HEIGHTS[index - 1][0]
                    break

    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj,'INSERT')
        self.assembly = fd_types.Assembly(obj_insert_bp)
        self.set_properties_from_prompts()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(330))
        
    def draw(self, context):
        props = props_closet.get_scene_props()
        
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                box = layout.box()
                
                cubby_placement = self.assembly.get_prompt("Cubby Placement")
                cubby_height = self.assembly.get_prompt("Cubby Height")
                
                vert_qty = self.assembly.get_prompt("Vertical Quantity")
                horz_qty = self.assembly.get_prompt("Horizontal Quantity")
                setback = self.assembly.get_prompt("Cubby Setback")
                divider_thickness = self.assembly.get_prompt("Divider Thickness")
                
                cubby_placement.draw_prompt(box)
                
                if props.closet_defaults.use_32mm_system:   
                    box.prop(self,'cubby_height')
                else:
                    cubby_height.draw_prompt(box)
                box.prop(vert_qty,'QuantityValue',text="Vertical Quantity")
                box.prop(horz_qty,'QuantityValue',text="Horizontal Quantity")
                box.prop(setback,'DistanceValue',text="Setback Amount")
                
                height = self.assembly.obj_z.location.z
                width = self.assembly.obj_x.location.x
                v_qty = vert_qty.QuantityValue
                h_qty = horz_qty.QuantityValue
                
                vertical_opening = (height - (divider_thickness.DistanceValue*h_qty))/(h_qty+1)
                horizontal_opening = (width - (divider_thickness.DistanceValue*v_qty))/(v_qty+1)
                
                box.label("Shoe Cubby Vertical Opening Space: " + str(unit.meter_to_active_unit(vertical_opening)) + '"')
                box.label("Shoe Cubby Horizontal Opening Space: " + str(unit.meter_to_active_unit(horizontal_opening)) + '"')

bpy.utils.register_class(PROMPTS_Shoe_Cubbies)