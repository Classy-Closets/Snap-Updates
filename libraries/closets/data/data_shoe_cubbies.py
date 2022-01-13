import bpy
from snap import sn_types, sn_unit, sn_utils
from ..common import common_parts
from ..common import common_lists
import math
from bpy.props import EnumProperty, StringProperty

def add_horizontal_cubbie_slots(part,insert):
    default_props = bpy.context.scene.sn_closets.closet_defaults
    machining = default_props.machining_defaults   
        
    Part_Thickness = part.obj_z.snap.get_var('location.z','Part_Thickness')
    Part_Length = part.obj_x.snap.get_var('location.x','Part_Length')
    Part_Width = part.obj_y.snap.get_var('location.y','Part_Width')
    Vertical_Quantity = insert.get_prompt('Vertical Quantity').get_var()

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
    Horizontal_Quantity = insert.get_prompt('Horizontal Quantity').get_var()

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
    show_in_library = True
    category_name = "Products - Shelves"
    id_prompt = 'sn_closets.shoe_cubbies'

    vert_dividers = []
    horz_dividers = []

    def __init__(self, obj_bp=None):
        super().__init__(obj_bp=obj_bp)
        self.vert_dividers = []
        self.horz_dividers = []
        self.get_vert_dividers()
        self.get_horz_dividers()
        self.get_driver_vars()

    def get_driver_vars(self):
        self.Width = self.obj_x.snap.get_var('location.x', 'Width')
        self.Height = self.obj_z.snap.get_var('location.z', 'Height')
        self.Depth = self.obj_y.snap.get_var('location.y', 'Depth')
        self.Cubby_Setback = self.get_prompt("Cubby Setback").get_var()
        self.Cubby_Height = self.get_prompt("Cubby Height").get_var()
        self.Divider_Thickness = self.get_prompt("Divider Thickness").get_var()
        self.Cubby_Placement = self.get_prompt("Cubby Placement").get_var()

    def get_vert_dividers(self):
        for child in self.obj_bp.children:
            if child.get("IS_BP_VERT_DIV"):
                div = sn_types.Assembly(child)
                self.vert_dividers.append(div)

    def get_horz_dividers(self):
        for child in self.obj_bp.children:
            if child.get("IS_BP_HORZ_DIV"):
                div = sn_types.Assembly(child)
                self.horz_dividers.append(div)

    def add_vert_dividers(self, qty=2):
        for i in range(1, qty + 1):
            vert = common_parts.add_divider(self)
            vert.obj_bp["IS_BP_VERT_DIV"] = True
            self.vert_dividers.append(vert)
            vert.set_name("Vertical Divider")

            vert.loc_x(
                "((Width-(Divider_Thickness*{}))/({}+1))*{}+Divider_Thickness*{}".format(
                    qty, qty, i, str(i - 1), str(i - 1)),
                [self.Width, self.Divider_Thickness])
            vert.loc_y("Depth", [self.Depth])
            vert.loc_z(
                'IF(Cubby_Placement==1,Height-Cubby_Height,0)', [self.Cubby_Placement, self.Height, self.Cubby_Height])

            vert.rot_y(value=math.radians(-90))

            vert.dim_x(
                "IF(Cubby_Placement==2,Height,Cubby_Height)", [self.Height, self.Cubby_Placement, self.Cubby_Height])
            vert.dim_y("(Depth*-1)+Cubby_Setback", [self.Depth, self.Cubby_Setback])
            vert.dim_z("-Divider_Thickness", [self.Divider_Thickness])

    def add_horz_dividers(self, qty=2):
        for i in range(1, qty + 1):
            start_placement = "IF(Cubby_Placement==1,Height-Cubby_Height,0)"
            horz_spacing = "((IF(Cubby_Placement==2,Height,Cubby_Height)-(Divider_Thickness*{}))/({}+1))".format(qty, qty)
            horz_qty = 'IF({}>{},0,{})+IF({}>{},0,Divider_Thickness*{})'.format(str(i), str(qty), str(i), str(i), str(qty), str(i - 1))

            horz = common_parts.add_divider(self)
            horz.obj_bp["IS_BP_HORZ_DIV"] = True
            self.horz_dividers.append(horz)
            horz.set_name("Horizontal Divider")
            horz.loc_y("Depth", [self.Depth])
            horz.loc_z("{}+{}*{}".format(start_placement, horz_spacing, horz_qty), [self.Cubby_Placement, self.Cubby_Height, self.Height, self.Divider_Thickness])

            horz.dim_x("Width", [self.Width])
            horz.dim_y("(Depth*-1)+Cubby_Setback", [self.Depth, self.Cubby_Setback])
            horz.dim_z("Divider_Thickness", [self.Divider_Thickness])

    def draw(self):
        self.create_assembly()
        # we are adding a master hide for everything
        hide_prompt = self.add_prompt('Hide', 'CHECKBOX', False)
        self.hide_var = hide_prompt.get_var()

        self.add_prompt("Cubby Placement", 'COMBOBOX', 0, ['Bottom', 'Top', 'Fill'])  # columns=3
        self.add_prompt("Horizontal Quantity", 'QUANTITY', 2)
        self.add_prompt("Vertical Quantity", 'QUANTITY', 2)
        self.add_prompt("Cubby Setback", 'DISTANCE', sn_unit.inch(0.25))
        self.add_prompt("Divider Thickness", 'DISTANCE', sn_unit.inch(.25))
        self.add_prompt("Shelf Thickness", 'DISTANCE', sn_unit.inch(.75))
        self.add_prompt("Vertical Spacing", 'DISTANCE', sn_unit.inch(.25))
        self.add_prompt("Horizontal Spacing", 'DISTANCE', sn_unit.inch(.25))
        self.add_prompt("Cubby Height", 'DISTANCE', sn_unit.millimeter(557.276))

        self.get_driver_vars()
        Shelf_Thickness = self.get_prompt("Shelf Thickness").get_var()

        top_shelf = common_parts.add_shelf(self)
        top_shelf.get_prompt("Is Locked Shelf").set_value(True)
        top_shelf.loc_z(
            'IF(Cubby_Placement==0,Cubby_Height+Shelf_Thickness,Height-Cubby_Height)',
            [Shelf_Thickness, self.Cubby_Placement, self.Cubby_Height, self.Height])
        top_shelf.dim_x('Width', [self.Width])
        top_shelf.dim_y('Depth', [self.Depth])
        top_shelf.dim_z('-Shelf_Thickness', [Shelf_Thickness])
        top_shelf.get_prompt('Hide').set_formula('IF(Cubby_Placement==2,True,False)', [self.Cubby_Placement])

        opening = common_parts.add_opening(self)
        opening.loc_z(
            'IF(Cubby_Placement==0,Cubby_Height+Shelf_Thickness,0)',
            [self.Cubby_Placement, self.Cubby_Height, Shelf_Thickness])
        opening.dim_x('IF(Cubby_Placement==2,0,Width)', [self.Cubby_Placement, self.Width])
        opening.dim_y('IF(Cubby_Placement==2,0,Depth)', [self.Cubby_Placement, self.Depth])
        opening.dim_z(
            'IF(Cubby_Placement==2,0,Height-Cubby_Height-Shelf_Thickness)',
            [self.Cubby_Placement, self.Height, self.Cubby_Height, Shelf_Thickness])

        self.add_vert_dividers()
        self.add_horz_dividers()
        self.obj_bp["ID_PROMPT"] = self.id_prompt
        self.update()

class PROMPTS_Shoe_Cubbies(sn_types.Prompts_Interface):
    bl_idname = "sn_closets.shoe_cubbies"
    bl_label = "Shoe Cubbies Prompts" 
    bl_description = "This shows all of the available shoe cubby options"
    bl_options = {'UNDO'}

    cubby_placement: EnumProperty(name="Cubby Placement",
                                  items=(
                                      ('0', 'Bottom', 'Bottom'),
                                      ('1', 'Top', 'Top'),
                                      ('2', 'Fill', 'Fill'),
                                  ))

    cubby_height: EnumProperty(name="Cubby Height",
                                items=common_lists.OPENING_HEIGHTS,
                                default = '557.276')     
    
    assembly = None
    
    vertical_opening_space = 0
    horizontal_opening_space = 0
    
    @classmethod
    def poll(cls, context):
        return True
        
    def update_vert_divs(self):
        vert_qty = self.assembly.get_prompt("Vertical Quantity")
        vert_qty_changed = len(self.assembly.vert_dividers) != int(vert_qty.get_value())

        if vert_qty_changed:
            for assembly in self.assembly.vert_dividers:
                sn_utils.delete_object_and_children(assembly.obj_bp)
            self.assembly.vert_dividers.clear()
            self.assembly.add_vert_dividers(qty=int(vert_qty.get_value()))

        self.assembly.update()

    def update_horz_divs(self):
        horz_qty = self.assembly.get_prompt("Horizontal Quantity")
        horz_qty_changed = len(self.assembly.horz_dividers) != int(horz_qty.get_value())

        if horz_qty_changed:
            for assembly in self.assembly.horz_dividers:
                sn_utils.delete_object_and_children(assembly.obj_bp)
            self.assembly.horz_dividers.clear()
            self.assembly.add_horz_dividers(qty=int(horz_qty.get_value()))

    def check(self, context):
        self.update_vert_divs()
        self.update_horz_divs()

        props = bpy.context.scene.sn_closets
        if props.closet_defaults.use_32mm_system:
            cubby_height = self.assembly.get_prompt("Cubby Height")
            if cubby_height:
                cubby_height.set_value(sn_unit.inch(float(self.cubby_height) / 25.4))

        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport
        self.assembly.get_prompt('Cubby Placement').set_value(int(self.cubby_placement))
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
        obj = bpy.data.objects[context.object.name]
        obj_insert_bp = sn_utils.get_bp(obj,'INSERT')
        self.assembly = Shoe_Cubbies(obj_insert_bp)
        self.set_properties_from_prompts()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=sn_utils.get_prop_dialog_width(330))
        
    def draw(self, context):
        props = bpy.context.scene.sn_closets
        
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                box = layout.box()
                
                
                cubby_height = self.assembly.get_prompt("Cubby Height")
                
                vert_qty = self.assembly.get_prompt("Vertical Quantity")
                horz_qty = self.assembly.get_prompt("Horizontal Quantity")
                setback = self.assembly.get_prompt("Cubby Setback")
                divider_thickness = self.assembly.get_prompt("Divider Thickness")
                
                box.prop(self,'cubby_placement', expand=True)
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
                
                box.label(text="Shoe Cubby Vertical Opening Space: " + str(sn_unit.meter_to_active_unit(vertical_opening)) + '"')
                box.label(text="Shoe Cubby Horizontal Opening Space: " + str(sn_unit.meter_to_active_unit(horizontal_opening)) + '"')

bpy.utils.register_class(PROMPTS_Shoe_Cubbies)