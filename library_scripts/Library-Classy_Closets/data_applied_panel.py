import bpy
from mv import fd_types, unit, utils
from . import mv_closet_defaults as props_closet
from . import common_parts

class Applied_Panel(fd_types.Assembly):
    
    type_assembly = "PRODUCT"
    property_id = props_closet.LIBRARY_NAME_SPACE + ".applied_panel"
    plan_draw_id = props_closet.LIBRARY_NAME_SPACE + '.draw_plan'
    
    opening_qty = 4
    
    is_hanging = False
    
    def __init__(self):
        pass
    
    def add_prompt_options(self):
        self.add_prompt(name="Panel Quantity",prompt_type='COMBOBOX',items=["1","2","3","4"],value=0,tab_index=0,columns=4)
        self.add_prompt(name="Bottom Offset",prompt_type='DISTANCE',value=0,tab_index=0)  
        self.add_prompt(name="Top Offset",prompt_type='DISTANCE',value=0,tab_index=0) 
        self.add_prompt(name="Left Offset",prompt_type='DISTANCE',value=0,tab_index=0) 
        self.add_prompt(name="Right Offset",prompt_type='DISTANCE',value=0,tab_index=0) 
    
    def add_calculator_prompts(self):
        pq = self.get_var('Panel Quantity','pq')
        Bottom_Offset = self.get_var('Bottom Offset')
        Top_Offset = self.get_var('Top Offset')
        
        for i in range(1,5):
            self.add_prompt(name="Panel " + str(i) + " Height",prompt_type='DISTANCE',value=0,equal=True,tab_index=2)
            self.add_prompt(name="Panel " + str(i) + " Left Offset",prompt_type='DISTANCE',value=0,equal=True,tab_index=0)
            self.add_prompt(name="Panel " + str(i) + " Right Offset",prompt_type='DISTANCE',value=0,equal=True,tab_index=0)
            #When using calculators we have to move the tab index if not being used in calculator
            driver = self.obj_bp.driver_add('mv.PromptPage.COL_Prompt["Panel ' + str(i) + ' Height"].TabIndex')
            utils.add_variables_to_driver(driver,[pq])
            driver.driver.expression = "IF(pq>=" + str(i - 1) + ",1,2)"         

        self.calculator_deduction("Top_Offset+Bottom_Offset",[Top_Offset,Bottom_Offset]) 
    
    def add_panels(self):
        Height = self.get_var('dim_z','Height')
        Width = self.get_var('dim_x','Width')
        Depth = self.get_var('dim_y','Depth')
        Top_Offset = self.get_var('Top Offset')
        Left_Offset = self.get_var('Left Offset')
        Right_Offset = self.get_var('Right Offset')             
        pq = self.get_var('Panel Quantity','pq')
        
        prev_panel_empty = None

        for i in range(1,5):
            
            panel_left_offset = self.get_var('Panel ' + str(i) + " Left Offset",'panel_left_offset')
            panel_right_offset = self.get_var('Panel ' + str(i) + " Right Offset",'panel_right_offset')
            ph = self.get_var('Panel ' + str(i) + " Height",'ph')
            
            panel_empty = self.add_empty()
            panel_empty.set_name("Panel Height Z " + str(i))
            if prev_panel_empty:
                prev_drawer_z_loc = prev_panel_empty.get_var('loc_z','prev_drawer_z_loc')
                panel_empty.z_loc('prev_drawer_z_loc-ph',[prev_drawer_z_loc,ph])
            else:
                panel_empty.z_loc('Height-Top_Offset-ph',[Height,Top_Offset,ph])                
                
            panel_z_loc = panel_empty.get_var('loc_z','panel_z_loc')
            
            panel = common_parts.add_door(self)
            panel.x_loc('Left_Offset+panel_left_offset',[Left_Offset,panel_left_offset])
            panel.y_loc(value = 0)
            panel.z_loc('panel_z_loc',[panel_z_loc])
            panel.x_rot(value = 0)
            panel.y_rot(value = -90)
            panel.z_rot(value = 90)
            panel.x_dim('ph',[ph])
            panel.y_dim('-Width+(Left_Offset+Right_Offset)+(panel_left_offset+panel_right_offset)',[Width,Left_Offset,Right_Offset,panel_left_offset,panel_right_offset])
            panel.z_dim('-Depth',[Depth])
            panel.prompt("Hide",'IF(pq>=' + str(i-1) + ',False,True)',[pq])
            
            prev_panel_empty = panel_empty
            
    def draw(self):
        self.create_assembly()
        
        self.add_tab(name='Panel Options',tab_type='VISIBLE')
        self.add_tab(name='Panel Heights',tab_type='CALCULATOR',calc_type="ZDIM")
        self.add_prompt_options()
        self.add_calculator_prompts()
        self.add_panels()
        
        self.update()
        
class PROMPTS_Applied_Panel(fd_types.Prompts_Interface):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".applied_panel"
    bl_label = "Applied Panel Prompts"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name",
                                           description="Stores the Base Point Object Name \
                                           so the object can be retrieved from the database.")
    
    width = bpy.props.FloatProperty(name="Width",unit='LENGTH',precision=4)
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
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(500))
        
    def get_number_of_equal_heights(self):
        number_of_equal_heights = 0
        panel_quantity = self.product.get_prompt("Panel Quantity")
        
        for i in range(1,int(panel_quantity.value()) + 1):
            height = self.product.get_prompt("Panel " + str(i) + " Height")
            if height:
                number_of_equal_heights += 1 if height.equal else 0
            else:
                break
            
        return number_of_equal_heights
        
    def draw(self, context):
        """ This is where you draw the interface """
        layout = self.layout
        layout.label(self.product.obj_bp.mv.name_object)
        self.draw_product_size(layout)
        
        top_offset = self.product.get_prompt("Top Offset")
        bottom_offset = self.product.get_prompt("Bottom Offset")
        left_offset = self.product.get_prompt("Left Offset")
        right_offset = self.product.get_prompt("Right Offset")
        
        box = layout.box()
        box.label("Panel Offsets")
        
        row = box.row()
        top_offset.draw_prompt(row)
        bottom_offset.draw_prompt(row)
        row = box.row()
        left_offset.draw_prompt(row)
        right_offset.draw_prompt(row)
        
        box = layout.box()
        box.label("Panel Quantities and Sizes")
        
        panel_quantity = self.product.get_prompt("Panel Quantity")
        panel_quantity.draw_prompt(box)
        
        for i in range(1,int(panel_quantity.value()) + 1):
            panel_height = self.product.get_prompt("Panel " + str(i) + " Height")
            panel_left_offset = self.product.get_prompt("Panel " + str(i) + " Left Offset")
            panel_right_offset = self.product.get_prompt("Panel " + str(i) + " Right Offset")
            
            row = box.row()
            if panel_height.equal == False:
                row.prop(panel_height,'equal',text="")
            else:            
                if self.get_number_of_equal_heights() != 1:
                    row.prop(panel_height,'equal',text="")
                else:
                    row.label("",icon='BLANK1')
            
            if panel_height.equal:
                row.label("Panel " + str(i) + " Height:")
                row.label(str(round(unit.meter_to_active_unit(panel_height.value()),2)))
            else:
                row.label("Panel " + str(i) + " Height:")
                row.prop(panel_height,'DistanceValue',text="")
                
            row.label("Offsets:")
            panel_left_offset.draw_prompt(row,split_text=False,text="Left")
            panel_right_offset.draw_prompt(row,split_text=False,text="Right")
        
bpy.utils.register_class(PROMPTS_Applied_Panel)