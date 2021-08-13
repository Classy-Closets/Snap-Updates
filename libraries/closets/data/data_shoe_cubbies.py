import bpy
from snap import sn_types, sn_unit, sn_utils
from snap import closet_props
from ..common import common_parts
from ..common import common_lists

def add_horizontal_cubbie_slots(part,insert):
    default_props = bpy.context.scene.sn_closets.closet_defaults
    machining = default_props.machining_defaults   
        
    Part_Thickness = part.obj_z.snap.get_var('location.z','Part_Thickness')
    Part_Length = part.obj_x.snap.get_var('location.x','Part_Length')
    Part_Width = part.obj_y.snap.get_var('location.y','Part_Width')
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
    default_props = bpy.context.scene.sn_closets.closet_defaults
    machining = default_props.machining_defaults   
        
    Part_Thickness = part.obj_z.snap.get_var('location.z','Part_Thickness')
    Part_Length = part.obj_x.snap.get_var('location.x','Part_Length')
    Part_Width = part.obj_y.snap.get_var('location.y','Part_Width')
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

class Shoe_Cubbies(sn_types.Assembly):
    """ This shoe cubby insert allows users to specify the quantity of vertical and horizontal dividers
        users can determine if the shoe cubbies are placed at the top, bottom, or if they should fill the entire opening
    """

    placement_type = "SPLITTER"
    property_id = "sn_closets.shoe_cubbies"
    type_assembly = "INSERT"
    mirror_y = False

    def draw(self):
        self.create_assembly()
        # we are adding a master hide for everything
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()

        self.add_tab("Shoe Cubby Options", 'VISIBLE')
        self.add_prompt("Cubby Placement", 'COMBOBOX', 0, ['Bottom', 'Top', 'Fill'])  # columns=3
        self.add_prompt("Horizontal Quantity", 'QUANTITY', 2)
        self.add_prompt("Vertical Quantity", 'QUANTITY', 2)
        self.add_prompt("Cubby Setback", 'DISTANCE', sn_unit.inch(0.25))
        self.add_prompt("Divider Thickness", 'DISTANCE', sn_unit.inch(.25))
        self.add_prompt("Shelf Thickness", 'DISTANCE', sn_unit.inch(.75))
        self.add_prompt("Vertical Spacing", 'DISTANCE', sn_unit.inch(.25))
        self.add_prompt("Horizontal Spacing", 'DISTANCE', sn_unit.inch(.25))
        self.add_prompt("Cubby Height", 'DISTANCE', sn_unit.millimeter(557.276))

        Width = self.obj_x.snap.get_var('location.x', 'Width')
        Height = self.obj_z.snap.get_var('location.z', 'Height')
        Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        Horizontal_Quantity = self.get_var("Horizontal Quantity")
        Vertical_Quantity = self.get_var("Vertical Quantity")
        Cubby_Setback = self.get_var("Cubby Setback")
        Cubby_Height = self.get_var("Cubby Height")
        Divider_Thickness = self.get_var("Divider Thickness")
        Shelf_Thickness = self.get_var("Shelf Thickness")
        Cubby_Placement = self.get_var("Cubby Placement")

        top_shelf = common_parts.add_shelf(self)
        top_shelf.prompt("Is Locked Shelf",value=True)
        top_shelf.loc_x(value = 0)
        top_shelf.loc_y(value = 0)
        top_shelf.loc_z('IF(Cubby_Placement==0,Cubby_Height+Shelf_Thickness,Height-Cubby_Height)',[Shelf_Thickness,Cubby_Placement,Cubby_Height,Height])
        top_shelf.rot_x(value = 0)
        top_shelf.rot_y(value = 0)
        top_shelf.rot_z(value = 0)
        top_shelf.dim_x('Width',[Width])
        top_shelf.dim_y('Depth',[Depth])
        top_shelf.dim_z('-Shelf_Thickness',[Shelf_Thickness])
        top_shelf.prompt('Hide','IF(Cubby_Placement==2,True,False)',[Cubby_Placement])

        opening = common_parts.add_opening(self)
        opening.loc_x(value = 0)
        opening.loc_y(value = 0)
        opening.loc_z('IF(Cubby_Placement==0,Cubby_Height+Shelf_Thickness,0)',[Cubby_Placement,Cubby_Height,Shelf_Thickness])
        opening.rot_x(value = 0)
        opening.rot_y(value = 0)
        opening.rot_z(value = 0)
        opening.dim_x('IF(Cubby_Placement==2,0,Width)',[Cubby_Placement,Width])
        opening.dim_y('IF(Cubby_Placement==2,0,Depth)',[Cubby_Placement,Depth])
        opening.dim_z('IF(Cubby_Placement==2,0,Height-Cubby_Height-Shelf_Thickness)',[Cubby_Placement,Height,Cubby_Height,Shelf_Thickness])

        for i in range(1,30):
            vert_spacing = "((Width-(Divider_Thickness*Vertical_Quantity))/(Vertical_Quantity+1))"
            vert_qty = 'IF(' + str(i) + '>Vertical_Quantity,0,' + str(i) + ')+IF(' + str(i) + '>Vertical_Quantity,0,Divider_Thickness*' + str(i - 1) + ')'
            
            vert = common_parts.add_divider(self)
            vert.set_name("Vertical Divider")
            vert.loc_x('(' + vert_spacing + ')*' + vert_qty,[Width,Divider_Thickness,Vertical_Quantity])
            vert.loc_y("Depth",[Depth])
            vert.loc_z('IF(Cubby_Placement==1,Height-Cubby_Height,0)',[Cubby_Placement,Height,Cubby_Height])
            vert.rot_x(value = 0)
            vert.rot_y(value = -90)
            vert.rot_z(value = 0)
            vert.dim_x("IF(Cubby_Placement==2,Height,Cubby_Height)",[Height,Cubby_Placement,Cubby_Height])
            vert.dim_y("(Depth*-1)+Cubby_Setback",[Depth,Cubby_Setback])
            vert.dim_z("-Divider_Thickness",[Divider_Thickness])
            vert.prompt('Hide','IF(' + str(i) + '>Vertical_Quantity,True,False)',[Vertical_Quantity])
            
            start_placement = "IF(Cubby_Placement==1,Height-Cubby_Height,0)"
            horz_spacing = "((IF(Cubby_Placement==2,Height,Cubby_Height)-(Divider_Thickness*Horizontal_Quantity))/(Horizontal_Quantity+1))"
            horz_qty = 'IF(' + str(i) + '>Horizontal_Quantity,0,' + str(i) + ')+IF(' + str(i) + '>Horizontal_Quantity,0,Divider_Thickness*' + str(i - 1) + ')'
            
            horz = common_parts.add_divider(self)
            horz.set_name("Horizontal Divider")
            horz.loc_x(value = 0)
            horz.loc_y("Depth",[Depth])
            horz.loc_z(start_placement + '+(' + horz_spacing + ')*' + horz_qty,[Cubby_Placement,Cubby_Height,Height,Divider_Thickness,Horizontal_Quantity])
            horz.rot_x(value = 0)
            horz.rot_y(value = 0)
            horz.rot_z(value = 0)
            horz.dim_x("Width",[Width])
            horz.dim_y("(Depth*-1)+Cubby_Setback",[Depth,Cubby_Setback])
            horz.dim_z("Divider_Thickness",[Divider_Thickness])
            horz.prompt('Hide','IF(' + str(i) + '>Horizontal_Quantity,True,False)',[Horizontal_Quantity])
            
        self.update()

class PROMPTS_Shoe_Cubbies(bpy.types.Operator):
    bl_idname = "sn_closets.shoe_cubbies"
    bl_label = "Shoe Cubbies Prompts" 
    bl_description = "This shows all of the available shoe cubby options"
    bl_options = {'UNDO'}
    
    object_name: StringProperty(name="Object Name")
    
    cubby_height: EnumProperty(name="Cubby Height",
                                          items=common_lists.OPENING_HEIGHTS,
                                          default = '557.276')     
    
    assembly = None
    
    vertical_opening_space = 0
    horizontal_opening_space = 0
    
    @classmethod
    def poll(cls, context):
        return True
        
    def check(self, context):
        props = bpy.context.scene.sn_closets
        if props.closet_defaults.use_32mm_system:
            cubby_height = self.assembly.get_prompt("Cubby Height")
            if cubby_height:
                cubby_height.set_value(sn_unit.inch(float(self.cubby_height) / 25.4))

        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport
        return True
        
    def execute(self, context):
        return {'FINISHED'}

    def set_properties_from_prompts(self):
        cubby_height = self.assembly.get_prompt("Cubby Height")
        if cubby_height:
            value = round(cubby_height.distance_value * 1000,2)
            for index, height in enumerate(common_lists.OPENING_HEIGHTS):
                if not value >= float(height[0]):
                    self.cubby_height = common_lists.OPENING_HEIGHTS[index - 1][0]
                    break

    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = sn_utils.get_bp(obj,'INSERT')
        self.assembly = sn_types.Assembly(obj_insert_bp)
        self.set_properties_from_prompts()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=sn_utils.get_prop_dialog_width(330))
        
    def draw(self, context):
        props = bpy.context.scene.sn_closets
        
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
                box.prop(vert_qty,'quantity_value',text="Vertical Quantity")
                box.prop(horz_qty,'quantity_value',text="Horizontal Quantity")
                box.prop(setback,'distance_value',text="Setback Amount")
                
                height = self.assembly.obj_z.location.z
                width = self.assembly.obj_x.location.x
                v_qty = vert_qty.get_value()
                h_qty = horz_qty.get_value()
                
                vertical_opening = (height - (divider_thickness.distance_value*h_qty))/(h_qty+1)
                horizontal_opening = (width - (divider_thickness.distance_value*v_qty))/(v_qty+1)
                
                box.label("Shoe Cubby Vertical Opening Space: " + str(sn_unit.meter_to_active_unit(vertical_opening)) + '"')
                box.label("Shoe Cubby Horizontal Opening Space: " + str(sn_unit.meter_to_active_unit(horizontal_opening)) + '"')

bpy.utils.register_class(PROMPTS_Shoe_Cubbies)