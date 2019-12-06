import bpy
import math
from mv import fd_types, unit, utils
from . import cabinet_properties

def draw_carcass_options(carcass,layout):
    left_fin_end = carcass.get_prompt("Left Fin End")
    right_fin_end = carcass.get_prompt("Right Fin End")
    left_wall_filler = carcass.get_prompt("Left Side Wall Filler")
    right_wall_filler = carcass.get_prompt("Right Side Wall Filler")
    
    valance_height_top = carcass.get_prompt("Valance Height Top")
    toe_kick_height = carcass.get_prompt("Toe Kick Height")
    remove_bottom = carcass.get_prompt("Remove Bottom")
    remove_back = carcass.get_prompt("Remove Back")
    use_thick_back = carcass.get_prompt("Use Thick Back")
    use_nailers = carcass.get_prompt("Use Nailers")
    cabinet_depth_left = carcass.get_prompt("Cabinet Depth Left")
    cabinet_depth_right = carcass.get_prompt("Cabinet Depth Right")
    
    # SIDE OPTIONS:
    if left_wall_filler and right_wall_filler:
        col = layout.column(align=True)
        col.label("Side Options:")
        
        row = col.row()
        row.prop(left_wall_filler,'DistanceValue',text="Left Filler Amount")
        row.prop(left_fin_end,'CheckBoxValue',text="Left Fin End")
        
        row = col.row()
        row.prop(right_wall_filler,'DistanceValue',text="Right Filler Amount")
        row.prop(right_fin_end,'CheckBoxValue',text="Right Fin End")
    
    # CARCASS OPTIONS:
    col = layout.column(align=True)
    col.label("Carcass Options:")
    row = col.row()
    if use_thick_back:
        row.prop(use_thick_back,'CheckBoxValue',text="Use Thick Back")
    if use_nailers:
        row.prop(use_nailers,'CheckBoxValue',text="Use Nailers")
    if remove_bottom:
        row.prop(remove_bottom,'CheckBoxValue',text="Remove Bottom")
    if remove_back:
        row.prop(remove_back,'CheckBoxValue',text="Remove Back")
    if cabinet_depth_left:
        row = col.row()
        row.prop(cabinet_depth_left,'DistanceValue',text="Cabinet Depth Left")
        row.prop(cabinet_depth_right,'DistanceValue',text="Cabinet Depth Right")
    
    # TOE KICK OPTIONS
    if toe_kick_height:
        col = layout.column(align=True)
        toe_kick_setback = carcass.get_prompt("Toe Kick Setback")
        col.label("Toe Kick Options:")
        row = col.row()
        row.prop(toe_kick_height,'DistanceValue',text="Toe Kick Height")
        row.prop(toe_kick_setback,'DistanceValue',text="Toe Kick Setback")
        
    # VALANCE OPTIONS
    if valance_height_top:
        r_full_height = carcass.get_prompt("Right Side Full Height")
        l_full_height = carcass.get_prompt("Left Side Full Height")
        valance_each_unit = carcass.get_prompt("Valance Each Unit")
        
        col = layout.column(align=True)
        col.label("Valance Options:")
        door_valance_top = carcass.get_prompt("Door Valance Top")
        row = col.row()
        row.prop(valance_height_top,'DistanceValue',text="Valance Height Top")
        row.prop(door_valance_top,'CheckBoxValue',text="Door Valance Top")

        valance_height_bottom = carcass.get_prompt("Valance Height Bottom")
        
        if valance_height_bottom:
            door_valance_bottom = carcass.get_prompt("Door Valance Bottom")
            row = col.row()
            row.prop(valance_height_bottom,'DistanceValue',text="Valance Height Bottom")
            row.prop(door_valance_bottom,'CheckBoxValue',text="Door Valance Bottom")
        
        row = col.row()
        row.prop(l_full_height,'CheckBoxValue',text="Left Side Full Height")
        row.prop(r_full_height,'CheckBoxValue',text="Right Side Full Height")
        
        row = col.row()
        row.prop(valance_each_unit,'CheckBoxValue',text="Add Valance For Each Unit")

def draw_countertop_options(ctop,product,layout):
    Add_Backsplash = ctop.get_prompt("Add Backsplash")
    Add_Left_Backsplash = ctop.get_prompt("Add Left Backsplash")
    Add_Right_Backsplash = ctop.get_prompt("Add Right Backsplash")
    Countertop_Overhang_Front = product.get_prompt("Countertop Overhang Front")
    Countertop_Overhang_Back = product.get_prompt("Countertop Overhang Back")
    Countertop_Overhang_Left = product.get_prompt("Countertop Overhang Left")
    Countertop_Overhang_Right = product.get_prompt("Countertop Overhang Right")
    col = layout.column(align=True)
    col.label("Countertop Options:")
    
    if Add_Backsplash and Add_Left_Backsplash and Add_Right_Backsplash:
        row = col.row()
        row.label("Add Splash:")
        row.prop(Add_Backsplash,'CheckBoxValue',text="Back")
        row.prop(Add_Left_Backsplash,'CheckBoxValue',text="Left")
        row.prop(Add_Right_Backsplash,'CheckBoxValue',text="Right")
    
    if Countertop_Overhang_Front:
        row = col.row(align=True)
        row.label("Overhang:")
        row.prop(Countertop_Overhang_Front,'DistanceValue',text="Front")
        row.prop(Countertop_Overhang_Back,'DistanceValue',text="Back")
        row.prop(Countertop_Overhang_Left,'DistanceValue',text="Left")
        row.prop(Countertop_Overhang_Right,'DistanceValue',text="Right")

def draw_door_options(door,layout):
    box = layout.box()

    open_door = door.get_prompt('Open Door')
    door_swing = door.get_prompt('Door Swing')
    inset_front = door.get_prompt('Inset Front')
    
    half_overlay_top = door.get_prompt('Half Overlay Top')
    half_overlay_bottom = door.get_prompt('Half Overlay Bottom')
    half_overlay_left = door.get_prompt('Half Overlay Left')
    half_overlay_right = door.get_prompt('Half Overlay Right')
    
    row = box.row()
    row.label("Door Options:")
    
    if open_door:
        inset_front.draw_prompt(row,text="Inset Door",split_text=False)
        open_door.draw_prompt(row,split_text=False)
        
    if door_swing:
        row = box.row()
        door_swing.draw_prompt(row)
    
    if not inset_front.value():
        row = box.row()
        row.label("Half Overlays:")
        if half_overlay_top:
            half_overlay_top.draw_prompt(row,text="Top",split_text=False)
        if half_overlay_bottom:
            half_overlay_bottom.draw_prompt(row,text="Bottom",split_text=False)
        if half_overlay_left:
            half_overlay_left.draw_prompt(row,text="Left",split_text=False)
        if half_overlay_right:
            half_overlay_right.draw_prompt(row,text="Right",split_text=False)

def draw_drawer_options(drawers,layout):
    open_prompt = drawers.get_prompt("Open Drawers")
    inset_front = drawers.get_prompt("Inset Front")
    half_overlay_top = drawers.get_prompt("Half Overlay Top")
    half_overlay_bottom = drawers.get_prompt("Half Overlay Bottom")
    half_overlay_left = drawers.get_prompt("Half Overlay Left")
    half_overlay_right = drawers.get_prompt("Half Overlay Right")
    
    box = layout.box()
    row = box.row()
    row.label("Drawer Options:")

    if inset_front:
        row.prop(inset_front,'CheckBoxValue',text="Inset Drawer Front")

    if open_prompt:
        open_prompt.draw_prompt(row,split_text=False)
        
    if not inset_front.value():
        if half_overlay_top:
            col = box.column(align=True)
            row = col.row()
            row.label("Half Overlays:")
            row.prop(half_overlay_top,'CheckBoxValue',text="Top")
            row.prop(half_overlay_bottom,'CheckBoxValue',text="Bottom")
            row.prop(half_overlay_left,'CheckBoxValue',text="Left")
            row.prop(half_overlay_right,'CheckBoxValue',text="Right")
    
    if "Drawer Front 2 Height" in drawers.obj_bp.mv.PromptPage.COL_Prompt:
        for i in range(1,10):
            drawer_height = drawers.get_prompt("Drawer Front " + str(i) + " Height")
            if drawer_height:
                row = box.row()
                row.label("Drawer Front " + str(i) + " Height:")
                if drawer_height.equal:
                    row.label(str(unit.meter_to_active_unit(drawer_height.value())))
                    row.prop(drawer_height,'equal',text="")
                else:
                    row.prop(drawer_height,'DistanceValue',text="")
                    row.prop(drawer_height,'equal',text="")
            else:
                break

def draw_interior_options(assembly,layout):
    adj_shelf_qty = assembly.get_prompt("Adj Shelf Qty")
    fix_shelf_qty = assembly.get_prompt("Fixed Shelf Qty")
    shelf_qty = assembly.get_prompt("Shelf Qty")
    shelf_setback = assembly.get_prompt("Shelf Setback")
    adj_shelf_setback = assembly.get_prompt("Adj Shelf Setback")
    fix_shelf_setback = assembly.get_prompt("Fixed Shelf Setback")
    div_qty_per_row = assembly.get_prompt("Divider Qty Per Row")
    division_qty = assembly.get_prompt("Division Qty")
    adj_shelf_rows = assembly.get_prompt("Adj Shelf Rows")
    fixed_shelf_rows = assembly.get_prompt("Fixed Shelf Rows")
    
    if shelf_qty:
        row = layout.row()
        shelf_qty.draw_prompt(row,split_text=False)    
    
    if shelf_setback:
        shelf_setback.draw_prompt(row,split_text=False)    
    
    if adj_shelf_qty:
        row = layout.row()
        adj_shelf_qty.draw_prompt(row,split_text=False)

    if adj_shelf_setback:
        adj_shelf_setback.draw_prompt(row,split_text=False)
        
    if fix_shelf_qty:
        row = layout.row()
        fix_shelf_qty.draw_prompt(row,split_text=False)

    if fix_shelf_setback:
        fix_shelf_setback.draw_prompt(row,split_text=False)
        
    if div_qty_per_row:
        row = layout.row()
        div_qty_per_row.draw_prompt(row,split_text=False)

    if division_qty:
        row = layout.row()
        division_qty.draw_prompt(row,split_text=False)

    if adj_shelf_rows:
        row = layout.row()
        adj_shelf_rows.draw_prompt(row,split_text=False)

    if fixed_shelf_rows:
        row = layout.row()
        fixed_shelf_rows.draw_prompt(row,split_text=False)

def draw_splitter_options(assembly,layout):
    if assembly.get_prompt("Opening 1 Height"):
        name = "Height"
    else:
        name = "Width"
        
    box = layout.box()
    
    for i in range(1,10):
        opening = assembly.get_prompt("Opening " + str(i) + " " + name)
        if opening:
            row = box.row()
            row.label("Opening " + str(i) + " " + name  + ":")
            if opening.equal:
                row.label(str(unit.meter_to_active_unit(opening.value())))
                row.prop(opening,'equal',text="")
            else:
                row.prop(opening,'DistanceValue',text="")
                row.prop(opening,'equal',text="")
        else:
            break

class PANEL_Cabinet_Options(bpy.types.Panel):
    """Panel to Store all of the Cabinet Options"""
    bl_id = cabinet_properties.LIBRARY_NAME_SPACE + "_Advanced_Cabinet_Options"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "Advanced Cabinet Options"
    bl_category = "SNaP"

    props = None

    def draw_header(self, context):
        layout = self.layout
        layout.label('',icon='BLANK1')

    def draw_molding_options(self,layout):
        molding_box = layout.box()
        row = molding_box.row(align=True)
        row.label("Moldings Options:")
        row = molding_box.row(align=True)
        row.prop(self.props,'expand_crown_molding',text="",icon='TRIA_DOWN' if self.props.expand_crown_molding else 'TRIA_RIGHT',emboss=False)
        row.label("Crown:")
        row.prop(self.props,'crown_molding_category',text="",icon='FILE_FOLDER')
        row.prop(self.props,'crown_molding',text="")
        row.operator(cabinet_properties.LIBRARY_NAME_SPACE + ".auto_add_molding",text="",icon='ZOOMIN').molding_type = 'Crown'
        row.operator(cabinet_properties.LIBRARY_NAME_SPACE + '.delete_molding',text="",icon='X').molding_type = 'Crown'
        if self.props.expand_crown_molding:
            row = molding_box.row()
            row.label(text="",icon='BLANK1')
            row.template_icon_view(self.props,"crown_molding",show_labels=True)
            
        row = molding_box.row(align=True)
        row.prop(self.props,'expand_base_molding',text="",icon='TRIA_DOWN' if self.props.expand_base_molding else 'TRIA_RIGHT',emboss=False)
        row.label("Base:")
        row.prop(self.props,'base_molding_category',text="",icon='FILE_FOLDER')
        row.prop(self.props,'base_molding',text="")
        row.operator(cabinet_properties.LIBRARY_NAME_SPACE + ".auto_add_molding",text="",icon='ZOOMIN').molding_type = 'Base'
        row.operator(cabinet_properties.LIBRARY_NAME_SPACE + '.delete_molding',text="",icon='X').molding_type = 'Base'
        if self.props.expand_base_molding:
            row = molding_box.row()
            row.label(text="",icon='BLANK1')
            row.template_icon_view(self.props,"base_molding",show_labels=True)
            
        row = molding_box.row(align=True)
        row.prop(self.props,'expand_light_rail_molding',text="",icon='TRIA_DOWN' if self.props.expand_light_rail_molding else 'TRIA_RIGHT',emboss=False)
        row.label("Light Rail:")
        row.prop(self.props,'light_rail_molding_category',text="",icon='FILE_FOLDER')
        row.prop(self.props,'light_rail_molding',text="")
        row.operator(cabinet_properties.LIBRARY_NAME_SPACE + ".auto_add_molding",text="",icon='ZOOMIN').molding_type = 'Light'
        row.operator(cabinet_properties.LIBRARY_NAME_SPACE + '.delete_molding',text="",icon='X').molding_type = 'Light'
        if self.props.expand_light_rail_molding:
            row = molding_box.row()
            row.label(text="",icon='BLANK1')
            row.template_icon_view(self.props,"light_rail_molding",show_labels=True)            
            
    def draw_hardware_options(self,layout):
        #IMPLEMENT CHANGING HINGES GLOBALLY
        #IMPLEMENT CHANGING DRAWER SLIDES GLOBALLY
        hardware_box = layout.box()
        hardware_box.label("Hardware Options:")
        
        row = hardware_box.row(align=True)
        row.prop(self.props,'expand_pull',text="",icon='TRIA_DOWN' if self.props.expand_pull else 'TRIA_RIGHT',emboss=False)
        row.label('Pulls:')
        row.prop(self.props,'pull_category',text="",icon='FILE_FOLDER')
        row.prop(self.props,'pull_name',text="")
        row.operator(cabinet_properties.LIBRARY_NAME_SPACE + '.update_pull_selection',text="",icon='FILE_REFRESH').update_all = True
        row.operator(cabinet_properties.LIBRARY_NAME_SPACE + '.update_pull_selection',text="",icon='MAN_TRANS').update_all = False
        if self.props.expand_pull:
            row = hardware_box.row()
            row.label(text="",icon='BLANK1')
            row.template_icon_view(self.props,"pull_name",show_labels=True)
            
    def draw_material_options(self,layout):
        #IMPLEMENT CHANGING ROD MATERIAL
        #IMPLEMENT CHANGING BASKET MATERIAL
        #IMPLEMENT CHANGING DRAWER BOX MATERIAL

        material_box = layout.box()
        row = material_box.row()
        row.label("Material Selection:")
        row.operator(cabinet_properties.LIBRARY_NAME_SPACE + '.update_material',text="Selection",icon='MAN_TRANS').selection_only = True
        row.operator(cabinet_properties.LIBRARY_NAME_SPACE + '.update_material',text="Update All",icon='FILE_REFRESH').selection_only = False
        
        row = material_box.row(align=True)
        row.prop(self.props,'expand_core_material',text="",icon='TRIA_DOWN' if self.props.expand_core_material else 'TRIA_RIGHT',emboss=False)
        row.label('Core:')
        row.prop(self.props,'core_material',text="")
        if self.props.expand_core_material:
            row = material_box.row()
            row.label(text="",icon='BLANK1')
            row.template_icon_view(self.props,"core_material",show_labels=True)
        
        row = material_box.row(align=True)
        row.prop(self.props,'expand_door_material',text="",icon='TRIA_DOWN' if self.props.expand_door_material else 'TRIA_RIGHT',emboss=False)
        row.label('Doors:')
        row.prop(self.props,'door_material_category',text="",icon='FILE_FOLDER')
        row.prop(self.props,'door_material',text="")
        if self.props.expand_door_material:
            row = material_box.row()
            row.label(text="",icon='BLANK1')
            row.template_icon_view(self.props,"door_material",show_labels=True)
        
        row = material_box.row(align=True)
        row.prop(self.props,'expand_exterior_material',text="",icon='TRIA_DOWN' if self.props.expand_exterior_material else 'TRIA_RIGHT',emboss=False)
        row.label('Exterior:')
        row.prop(self.props,'exterior_material_category',text="",icon='FILE_FOLDER')
        row.prop(self.props,'exterior_material',text="")
        if self.props.expand_exterior_material:
            row = material_box.row()
            row.label(text="",icon='BLANK1')
            row.template_icon_view(self.props,"exterior_material",show_labels=True)
        
        row = material_box.row(align=True)
        row.prop(self.props,'expand_interior_material',text="",icon='TRIA_DOWN' if self.props.expand_interior_material else 'TRIA_RIGHT',emboss=False)
        row.label('Interior:')
        row.prop(self.props,'interior_material_category',text="",icon='FILE_FOLDER')
        row.prop(self.props,'interior_material',text="")
        if self.props.expand_interior_material:
            row = material_box.row()
            row.label(text="",icon='BLANK1')
            row.template_icon_view(self.props,"interior_material",show_labels=True)
        
        row = material_box.row(align=True)
        row.prop(self.props,'expand_edge_material',text="",icon='TRIA_DOWN' if self.props.expand_edge_material else 'TRIA_RIGHT',emboss=False)
        row.label('Edges:')
        row.prop(self.props,'edge_material_category',text="",icon='FILE_FOLDER')
        row.prop(self.props,'edge_material',text="")
        if self.props.expand_edge_material:
            row = material_box.row()
            row.label(text="",icon='BLANK1')
            row.template_icon_view(self.props,"edge_material",show_labels=True)

    def draw_door_style_options(self,layout):
        door_style_box = layout.box()
        door_style_box.label("Door Options:")
        row = door_style_box.row(align=True)
        row.prop(self.props,'expand_door',text="",icon='TRIA_DOWN' if self.props.expand_door else 'TRIA_RIGHT',emboss=False)
        row.label("Doors:")
        row.prop(self.props,'door_category',text="",icon='FILE_FOLDER')
        row.prop(self.props,'door_style',text="")
        row.operator(cabinet_properties.LIBRARY_NAME_SPACE + '.update_door_selection',text="",icon='MAN_TRANS')
        if self.props.expand_door:
            row = door_style_box.row()
            row.label(text="",icon='BLANK1')
            row.template_icon_view(self.props,"door_style",show_labels=True)
        row = door_style_box.row(align=True)
        row.label("Applied Panel:")
        row.operator(cabinet_properties.LIBRARY_NAME_SPACE + '.place_applied_panel',text="Add Applied Panel",icon='MAN_TRANS')
        
    def draw_column_style_options(self,layout):
        columns_panel_box = layout.box()
        columns_panel_box.label("Columns Options:")
        
        row = columns_panel_box.row(align=True)    
        row.prop(self.props,'expand_column',text="",icon='TRIA_DOWN' if self.props.expand_column else 'TRIA_RIGHT',emboss=False)
        row.label('Columns:')
        row.prop(self.props,'column_category',text="",icon='FILE_FOLDER')
        row.prop(self.props,'column_style',text="")
        row.operator(cabinet_properties.LIBRARY_NAME_SPACE + '.update_column_selection',text="",icon='MAN_TRANS')
        if self.props.expand_column:
            row = columns_panel_box.row()
            row.label(text="",icon='BLANK1')
            row.template_icon_view(self.props,"column_style",show_labels=True)
            
    def draw_interior_defaults(self,layout):
        col = layout.column(align=True)
        
        box = col.box()
        
        box.label("Default Shelf Quantity:")
        row = box.row()
        row.label("Base Cabinets:")
        row.prop(self.props.interior_defaults,"base_adj_shelf_qty",text="Quantity")
        row = box.row()
        row.label("Tall Cabinets:")
        row.prop(self.props.interior_defaults,"tall_adj_shelf_qty",text="Quantity")
        row = box.row()
        row.label("Upper Cabinets:")
        row.prop(self.props.interior_defaults,"upper_adj_shelf_qty",text="Quantity")
        
        box = col.box()
        
        box.label("Default Shelf Setback:")
        row = box.row()
        row.label("Adjustable:")
        row.prop(self.props.interior_defaults,"adj_shelf_setback",text="Setback")
        row = box.row()
        row.label("Fixed:")
        row.prop(self.props.interior_defaults,"fixed_shelf_setback",text="Setback")
        
    def draw_exterior_defaults(self,layout):
        col = layout.column(align=True)
        
        box = col.box()
        box.label("Door & Drawer Defaults:")
        
        row = box.row(align=True)
        row.prop(self.props.exterior_defaults,"inset_door")
        row.prop(self.props.exterior_defaults,"no_pulls")
        
        row = box.row(align=True)
        row.prop(self.props.exterior_defaults,"use_buyout_drawer_boxes")
        row.prop(self.props.exterior_defaults,"horizontal_grain_on_drawer_fronts")        
        
        if not self.props.exterior_defaults.no_pulls:
            box = col.box()
            box.label("Pull Placement:")
            
            row = box.row(align=True)
            row.label("Base Doors:")
            row.prop(self.props.exterior_defaults,"base_pull_location",text="From Top of Door")
            
            row = box.row(align=True)
            row.label("Tall Doors:")
            row.prop(self.props.exterior_defaults,"tall_pull_location",text="From Bottom of Door")
            
            row = box.row(align=True)
            row.label("Upper Doors:")
            row.prop(self.props.exterior_defaults,"upper_pull_location",text="From Bottom of Door")
            
            row = box.row(align=True)
            row.label("Distance From Edge:")
            row.prop(self.props.exterior_defaults,"pull_from_edge",text="")
            
            row = box.row(align=True)
            row.prop(self.props.exterior_defaults,"center_pulls_on_drawers")
    
            if not self.props.exterior_defaults.center_pulls_on_drawers:
                row.prop(self.props.exterior_defaults,"drawer_pull_from_top",text="Distance From Top")
        
        box = col.box()
        box.label("Door & Drawer Reveals:")
        
        if self.props.exterior_defaults.inset_door:
            row = box.row(align=True)
            row.label("Inset Reveals:")
            row.prop(self.props.exterior_defaults,"inset_reveal",text="")
        else:
            row = box.row(align=True)
            row.label("Standard Reveals:")
            row.prop(self.props.exterior_defaults,"left_reveal",text="Left")
            row.prop(self.props.exterior_defaults,"right_reveal",text="Right")
            
            row = box.row(align=True)
            row.label("Base Door Reveals:")
            row.prop(self.props.exterior_defaults,"base_top_reveal",text="Top")
            row.prop(self.props.exterior_defaults,"base_bottom_reveal",text="Bottom")
            
            row = box.row(align=True)
            row.label("Tall Door Reveals:")
            row.prop(self.props.exterior_defaults,"tall_top_reveal",text="Top")
            row.prop(self.props.exterior_defaults,"tall_bottom_reveal",text="Bottom")
            
            row = box.row(align=True)
            row.label("Upper Door Reveals:")
            row.prop(self.props.exterior_defaults,"upper_top_reveal",text="Top")
            row.prop(self.props.exterior_defaults,"upper_bottom_reveal",text="Bottom")
            
        row = box.row(align=True)
        row.label("Vertical Gap:")
        row.prop(self.props.exterior_defaults,"vertical_gap",text="")
    
        row = box.row(align=True)
        row.label("Door To Cabinet Gap:")
        row.prop(self.props.exterior_defaults,"door_to_cabinet_gap",text="")
        
    def draw_carcass_defaults(self,layout):
        col = layout.column(align=True)

        box = col.box()
        row = box.row(align=True)
        row.label("Cabinet Back Options:")
        row = box.row(align=True)
        row.prop(self.props.carcass_defaults,"remove_back")
        row.prop(self.props.carcass_defaults,"use_nailers")
        row.prop(self.props.carcass_defaults,"use_thick_back")
        row = box.row(align=True)
        row.label("Nailer Width:")
        row.prop(self.props.carcass_defaults,"nailer_width",text="")
        row = box.row(align=True)
        row.label("Center Nailer Switch:")
        row.prop(self.props.carcass_defaults,"center_nailer_switch",text="")

        box = col.box()
        row = box.row(align=True)
        row.label("Cabinet Top Options:")
        row = box.row(align=True)
        row.prop(self.props.carcass_defaults,"use_full_tops")
        if not self.props.carcass_defaults.use_full_tops:
            row = box.row(align=True)
            row.label("Stretcher Width:")
            row.prop(self.props.carcass_defaults,"stretcher_width",text="")
        row = box.row(align=True)
        row.label("Sub Front Height:")
        row.prop(self.props.carcass_defaults,"sub_front_height",text="")
        
        box = col.box()
        row = box.row(align=True)
        row.label("Cabinet Side Options:")
        row = box.row(align=True)
        row.prop(self.props.carcass_defaults,"use_notched_sides")
        row.prop(self.props.carcass_defaults,"extend_sides_to_floor")
        
        box = col.box()
        row = box.row(align=True)
        row.label("Cabinet Valance Options:")
        row = box.row(align=True)
        row.label("Valance Height Top:")
        row.prop(self.props.carcass_defaults,"valance_height_top")
        row = box.row(align=True)
        row.label("Valance Height Bottom:")
        row.prop(self.props.carcass_defaults,"valance_height_bottom")
        row = box.row(align=True)
        row.prop(self.props.carcass_defaults,"door_valance_top")
        row.prop(self.props.carcass_defaults,"door_valance_bottom")
        row = box.row(align=True)
        row.prop(self.props.carcass_defaults,"valance_each_unit")
        
        box = col.box()
        row = box.row(align=True)
        row.label("Cabinet Base Assembly:")
        row = box.row(align=True)
        row.label("Toe Kick Height:")
        row.prop(self.props.carcass_defaults,"toe_kick_height")
        row = box.row(align=True)
        row.label("Toe Kick Setback:")
        row.prop(self.props.carcass_defaults,"toe_kick_setback")
        row = box.row(align=True)
        row.prop(self.props.carcass_defaults,"use_leg_levelers")
    
    def draw_cabinet_sizes(self,layout):

        col = layout.column(align=True)

        box = col.box()
        box.label("Standard Frameless Cabinet Sizes:")
        
        row = box.row(align=True)
        row.label("Base:")
        row.prop(self.props.size_defaults,"base_cabinet_height",text="Height")
        row.prop(self.props.size_defaults,"base_cabinet_depth",text="Depth")
        
        row = box.row(align=True)
        row.label("Tall:")
        row.prop(self.props.size_defaults,"tall_cabinet_height",text="Height")
        row.prop(self.props.size_defaults,"tall_cabinet_depth",text="Depth")
        
        row = box.row(align=True)
        row.label("Upper:")
        row.prop(self.props.size_defaults,"upper_cabinet_height",text="Height")
        row.prop(self.props.size_defaults,"upper_cabinet_depth",text="Depth")

        row = box.row(align=True)
        row.label("Sink:")
        row.prop(self.props.size_defaults,"sink_cabinet_height",text="Height")
        row.prop(self.props.size_defaults,"sink_cabinet_depth",text="Depth")
        
        row = box.row(align=True)
        row.label("Suspended:")
        row.prop(self.props.size_defaults,"suspended_cabinet_height",text="Height")
        row.prop(self.props.size_defaults,"suspended_cabinet_depth",text="Depth")
        
        row = box.row(align=True)
        row.label("1 Door Wide:")
        row.prop(self.props.size_defaults,"width_1_door",text="Width")
        
        row = box.row(align=True)
        row.label("2 Door Wide:")
        row.prop(self.props.size_defaults,"width_2_door",text="Width")
        
        row = box.row(align=True)
        row.label("Drawer Stack Width:")
        row.prop(self.props.size_defaults,"width_drawer",text="Width")
        
        box = col.box()
        box.label("Blind Cabinet Widths:")
        
        row = box.row(align=True)
        row.label('Base:')
        row.prop(self.props.size_defaults,"base_width_blind",text="Width")
        
        row = box.row(align=True)
        row.label('Tall:')
        row.prop(self.props.size_defaults,"tall_width_blind",text="Width")
        
        row = box.row(align=True)
        row.label('Upper:')
        row.prop(self.props.size_defaults,"upper_width_blind",text="Width")
        
        box = col.box()
        box.label("Inside Corner Cabinet Sizes:")
        row = box.row(align=True)
        row.label("Base:")
        row.prop(self.props.size_defaults,"base_inside_corner_size",text="")
        
        row = box.row(align=True)
        row.label("Upper:")
        row.prop(self.props.size_defaults,"upper_inside_corner_size",text="")
        
        box = col.box()
        box.label("Placement:")
        row = box.row(align=True)
        row.label("Height Above Floor:")
        row.prop(self.props.size_defaults,"height_above_floor",text="")
        
        box = col.box()
        box.label("Drawer Heights:")
        row = box.row(align=True)
        row.prop(self.props.size_defaults,"equal_drawer_stack_heights")
        if not self.props.size_defaults.equal_drawer_stack_heights:
            row.prop(self.props.size_defaults,"top_drawer_front_height")
    
    def draw(self, context):
        self.props = cabinet_properties.get_scene_props()
        layout = self.layout

        box = layout.box()
        row = box.row()
        row.prop(self.props,'main_tabs',expand=True)
        
        if self.props.main_tabs == 'DEFAULTS':
            col = box.column(align=True)
            box = col.box()
            row = box.row()
            row.prop(self.props,'defaults_tabs',expand=True)
            
            if self.props.defaults_tabs == 'SIZES':
                self.draw_cabinet_sizes(box)
            
            if self.props.defaults_tabs == 'CARCASS':
                self.draw_carcass_defaults(box)
            
            if self.props.defaults_tabs == 'EXTERIOR':
                self.draw_exterior_defaults(box)
                
            if self.props.defaults_tabs == 'INTERIOR':
                self.draw_interior_defaults(box)
            
        if self.props.main_tabs == 'MATERIALS':
            self.draw_material_options(box)
            
        if self.props.main_tabs == 'OPTIONS':
            col = box.column(align=True)
            self.draw_molding_options(col)
            self.draw_hardware_options(col)
            self.draw_door_style_options(col)
            self.draw_column_style_options(col)

#---------PRODUCT: EXTERIOR PROMPTS

class PROMPTS_Door_Prompts(bpy.types.Operator):
    bl_idname = cabinet_properties.LIBRARY_NAME_SPACE + ".door_prompts"
    bl_label = "Door Prompts" 
    bl_description = "This shows all of the available door options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    assembly = None
    
    @classmethod
    def poll(cls, context):
        return True
        
    def check(self, context):
        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport
        return True
        
    def execute(self, context):
        return {'FINISHED'}

    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj,'INSERT')
        self.assembly = fd_types.Assembly(obj_insert_bp)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(500))
        
    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                draw_door_options(self.assembly,layout)


class PROMPTS_Drawer_Prompts(bpy.types.Operator):
    bl_idname = cabinet_properties.LIBRARY_NAME_SPACE + ".drawer_prompts"
    bl_label = "Drawer Prompts" 
    bl_description = "This shows all of the available drawer options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    assembly = None

    @classmethod
    def poll(cls, context):
        return True
        
    def check(self, context):
        utils.run_calculators(self.assembly.obj_bp)
        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport
        return True
        
    def execute(self, context):
        return {'FINISHED'}
        
    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj,'INSERT')
        self.assembly = fd_types.Assembly(obj_insert_bp)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(330))
    
    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                draw_drawer_options(self.assembly,layout)

        
class PROMPTS_Shelf_Prompts(bpy.types.Operator):
    bl_idname = cabinet_properties.LIBRARY_NAME_SPACE + ".interior_prompts"
    bl_label = "Shelf Prompts" 
    bl_description = "This shows all of the available shelf options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    adj_shelf_qty = bpy.props.IntProperty(name="Adjustable Shelf Quantity",min=0,max=5)
    fix_shelf_qty = bpy.props.IntProperty(name="Fixed Shelf Quantity",min=0,max=5)
    
    adj_shelf_qty_prompt = None
    fix_shelf_qty_prompt = None
    
    assembly = None

    def check(self, context):
        utils.run_calculators(self.assembly.obj_bp)
        self.assembly.obj_bp.location = self.assembly.obj_bp.location # Redraw Viewport
        return True
        
    def execute(self, context):
        return {'FINISHED'}

    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj,'INSERT')
        self.assembly = fd_types.Assembly(obj_insert_bp)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(330))
        
    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                draw_interior_options(self.assembly,layout)

#---------PRODUCT: SPLITTER PROMPTS

class PROMPTS_Splitter_Prompts(bpy.types.Operator):
    bl_idname = cabinet_properties.LIBRARY_NAME_SPACE + ".splitter_prompts"
    bl_label = "Splitter Prompts" 
    bl_description = "This shows all of the available splitter options"
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    assembly = None

    def check(self, context):
        utils.run_calculators(self.assembly.obj_bp)
        return True
        
    def execute(self, context):
        if self.assembly.obj_bp:
            if self.assembly.obj_bp.name in context.scene.objects:
                utils.run_calculators(self.assembly.obj_bp)
        return {'FINISHED'}
        
    def invoke(self,context,event):
        obj = bpy.data.objects[self.object_name]
        obj_insert_bp = utils.get_bp(obj,'INSERT')
        self.assembly = fd_types.Assembly(obj_insert_bp)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(330))

    def draw(self, context):
        layout = self.layout
        if self.assembly.obj_bp:
            draw_splitter_options(self.assembly,layout)

#---------PRODUCT: COLUMN PROMPTS

class PROMPTS_Column_Prompts(fd_types.Prompts_Interface):
    bl_idname = cabinet_properties.LIBRARY_NAME_SPACE + ".column_prompts"
    bl_label = "Column Prompts"
    bl_options = {'UNDO'}
    object_name = bpy.props.StringProperty(name="Object Name")

    width = bpy.props.FloatProperty(name="Width",unit='LENGTH',precision=4)
    height = bpy.props.FloatProperty(name="Height",unit='LENGTH',precision=4)
    depth = bpy.props.FloatProperty(name="Depth",unit='LENGTH',precision=4)

    product = None
    Left_End_Assembly = None
    Right_End_Assembly = None
    Standalone_Assembly = None
    Column_Detail_prompt = None
    
    def check(self, context):
        self.update_product_size()
        return True

    def execute(self, context):
        # This gets called when the OK button is clicked
        return {'FINISHED'}

    def invoke(self,context,event):
        # This gets called first and is used as an init call
        self.product = self.get_product()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(480))
    
    def draw(self, context):
        layout = self.layout
        if self.product.obj_bp:
            if self.product.obj_bp.name in context.scene.objects:
                box = layout.box()

                split = box.split(percentage=.8)
                split.label(self.product.obj_bp.mv.name_object + " | " + self.product.obj_bp.cabinetlib.spec_group_name,icon='LATTICE_DATA')
                split.menu('MENU_Current_Cabinet_Menu',text="Menu",icon='DOWNARROW_HLT')

                Extend_Left_End = self.product.get_prompt("Extend Left End")
                Extend_Right_End = self.product.get_prompt("Extend Right End")
                Panel_Depth = self.product.get_prompt("Panel Depth")

                self.draw_product_size(box)
                col = box.column(align=True)
                col.label("Basic Column Options:")
                row = col.row()
                row.prop(Extend_Left_End,'CheckBoxValue',text="Extend Left End")
                row.prop(Extend_Right_End,'CheckBoxValue',text="Extend Right End")
                row = col.row()
                row.prop(Panel_Depth,'DistanceValue',text="Panel Depth")

class PROMPTS_Angled_Column_Prompts(fd_types.Prompts_Interface):
    bl_idname = cabinet_properties.LIBRARY_NAME_SPACE + ".angled_column_prompts"
    bl_label = "Angled Column Prompts"
    bl_options = {'UNDO'}
    object_name = bpy.props.StringProperty(name="Object Name")

    width = bpy.props.FloatProperty(name="Width",unit='LENGTH',precision=4)
    height = bpy.props.FloatProperty(name="Height",unit='LENGTH',precision=4)
    depth = bpy.props.FloatProperty(name="Depth",unit='LENGTH',precision=4)

    product = None
    Left_End_Assembly = None
    Right_End_Assembly = None
    Standalone_Assembly = None
    Column_Detail_prompt = None
    
    def check(self, context):
        self.update_product_size()
        return True

    def execute(self, context):
        # This gets called when the OK button is clicked
        return {'FINISHED'}

    def invoke(self,context,event):
        # This gets called first and is used as an init call
        self.product = self.get_product()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(480))
    
    def draw(self, context):
        layout = self.layout
        if self.product.obj_bp:
            if self.product.obj_bp.name in context.scene.objects:
                box = layout.box()

                split = box.split(percentage=.8)
                split.label(self.product.obj_bp.mv.name_object + " | " + self.product.obj_bp.cabinetlib.spec_group_name,icon='LATTICE_DATA')
                split.menu('MENU_Current_Cabinet_Menu',text="Menu",icon='DOWNARROW_HLT')

                self.draw_product_size(box)


#---------PRODUCT: CABINET PROMPTS

class PROMPTS_Frameless_Cabinet_Prompts(fd_types.Prompts_Interface):
    bl_idname = cabinet_properties.LIBRARY_NAME_SPACE + ".frameless_cabinet_prompts"
    bl_label = "Frameless Cabinet Prompts" 
    bl_options = {'UNDO'}
    
    object_name = bpy.props.StringProperty(name="Object Name")
    
    width = bpy.props.FloatProperty(name="Width",unit='LENGTH',precision=4)
    height = bpy.props.FloatProperty(name="Height",unit='LENGTH',precision=4)
    depth = bpy.props.FloatProperty(name="Depth",unit='LENGTH',precision=4)

    product_tabs = bpy.props.EnumProperty(name="Door Swing",items=[('CARCASS',"Carcass","Carcass Options"),
                                                                   ('EXTERIOR',"Exterior","Exterior Options"),
                                                                   ('INTERIOR',"Interior","Interior Options"),
                                                                   ('SPLITTER',"Openings","Openings Options")])

    door_rotation = bpy.props.FloatProperty(name="Door Rotation",subtype='ANGLE',min=0,max=math.radians(120))
    
    door_swing = bpy.props.EnumProperty(name="Door Swing",items=[('Left Swing',"Left Swing","Left Swing"),
                                                                 ('Right Swing',"Right Swing","Right Swing")])
    
    product = None
    
    open_door_prompts = []
    
    show_exterior_options = False
    show_interior_options = False
    show_splitter_options = False

    carcass = None
    exterior = None
    interior = None
    counter_top = None
    
    doors = []
    drawers = []
    splitters = []
    interiors = []
    
    inserts = []

    def check(self, context):
        self.update_product_size()
        return True

    def execute(self, context):
        utils.run_calculators(self.product.obj_bp)
        return {'FINISHED'}

    def invoke(self,context,event):
        self.doors = []
        self.drawers = []
        self.splitters = []
        self.interiors = []
        
        self.product = self.get_product()
        self.inserts = utils.get_insert_bp_list(self.product.obj_bp,[])
        for insert in self.inserts:
            
            if "Carcass Options" in insert.mv.PromptPage.COL_MainTab:
                self.carcass = fd_types.Assembly(insert)
                
            if "Countertop Options" in insert.mv.PromptPage.COL_MainTab:
                self.counter_top = fd_types.Assembly(insert)
                
            if "Door Options" in insert.mv.PromptPage.COL_MainTab:
                self.show_exterior_options = True
                if insert not in self.doors:
                    self.doors.append(insert)
                
            if "Drawer Options" in insert.mv.PromptPage.COL_MainTab:
                self.show_exterior_options = True
                if insert not in self.drawers:
                    self.drawers.append(insert)
                
            if "Interior Options" in insert.mv.PromptPage.COL_MainTab:
                self.show_interior_options = True
                if insert not in self.interiors:
                    self.interiors.append(insert)
                    
            if "Opening Heights" in insert.mv.PromptPage.COL_MainTab:
                self.show_splitter_options = True
                if insert not in self.splitters:
                    self.splitters.append(insert)
                    
            if "Opening Widths" in insert.mv.PromptPage.COL_MainTab:
                self.show_splitter_options = True
                if insert not in self.splitters:
                    self.splitters.append(insert)
                
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(500))
            
    def draw_carcass_prompts(self,layout):
        if self.carcass:
            draw_carcass_options(self.carcass, layout)
            
        if self.counter_top:
            draw_countertop_options(self.counter_top, self.product, layout)
        
    def draw_door_prompts(self,layout):
        for door_bp in self.doors:
            door = fd_types.Assembly(door_bp)
            draw_door_options(door, layout)
        
    def draw_drawer_prompts(self,layout):
        for drawer_bp in self.drawers:
            drawer = fd_types.Assembly(drawer_bp)
            draw_drawer_options(drawer, layout)

    def draw_interior_prompts(self,layout):
        for interior_bp in self.interiors:
            interior = fd_types.Assembly(interior_bp)
            draw_interior_options(interior, layout)

    def draw_splitter_prompts(self,layout):
        for splitter_bp in self.splitters:
            splitter = fd_types.Assembly(splitter_bp)
            draw_splitter_options(splitter, layout)

    def draw(self, context):
        layout = self.layout
        if self.product.obj_bp:
            if self.product.obj_bp.name in context.scene.objects:
                box = layout.box()
                
                split = box.split(percentage=.8)
                split.label(self.product.obj_bp.mv.name_object + " | " + self.product.obj_bp.cabinetlib.spec_group_name,icon='LATTICE_DATA')
                split.menu('MENU_Current_Cabinet_Menu',text="Menu",icon='DOWNARROW_HLT')
                
                self.draw_product_size(box)
                
                prompt_box = box.box()
                row = prompt_box.row(align=True)
                row.prop_enum(self, "product_tabs", 'CARCASS') 
                if self.show_exterior_options:
                    row.prop_enum(self, "product_tabs", 'EXTERIOR') 
                if self.show_interior_options:
                    row.prop_enum(self, "product_tabs", 'INTERIOR') 
                if self.show_splitter_options:
                    row.prop_enum(self, "product_tabs", 'SPLITTER') 

                if self.product_tabs == 'CARCASS':
                    self.draw_carcass_prompts(prompt_box)
                if self.product_tabs == 'EXTERIOR':
                    self.draw_door_prompts(prompt_box)
                    self.draw_drawer_prompts(prompt_box)
                if self.product_tabs == 'INTERIOR':
                    self.draw_interior_prompts(prompt_box)
                if self.product_tabs == 'SPLITTER':
                    self.draw_splitter_prompts(prompt_box)
      
class PROMPTS_Face_Frame_Cabinet_Prompts(fd_types.Prompts_Interface):
    bl_idname = cabinet_properties.LIBRARY_NAME_SPACE + ".face_frame_cabinet_prompts"
    bl_label = "Face Frame Cabinet Prompts" 
    bl_options = {'UNDO'}
         
    object_name = bpy.props.StringProperty(name="Object Name")
     
    width = bpy.props.FloatProperty(name="Width",unit='LENGTH',precision=4)
    height = bpy.props.FloatProperty(name="Height",unit='LENGTH',precision=4)
    depth = bpy.props.FloatProperty(name="Depth",unit='LENGTH',precision=4)
 
    product_tabs = bpy.props.EnumProperty(name="Door Swing",items=[('CARCASS',"Carcass","Carcass Options"),
                                                         ('EXTERIOR',"Exterior","Exterior Options"),
                                                         ('INTERIOR',"Interior","Interior Options"),
                                                         ('SPLITTER',"Openings","Openings Options"),
                                                         ('FACEFRAME',"Face Frame","Face Frame Options")])
 
    door_rotation = bpy.props.FloatProperty(name="Door Rotation",subtype='ANGLE',min=0,max=math.radians(120))
     
    door_swing = bpy.props.EnumProperty(name="Door Swing",items=[('Left Swing',"Left Swing","Left Swing"),
                                                       ('Right Swing',"Right Swing","Right Swing")])
     
    product = None
     
    open_door_prompt = None
     
    open_door_prompts = []
     
    inserts = []
     
    show_exterior_options = False
    show_interior_options = False
    show_splitter_options = False

    def check(self, context):
        self.update_product_size()
        return True
 
    def execute(self, context):
        utils.run_calculators(self.product.obj_bp)
        return {'FINISHED'}
 
    def invoke(self,context,event):
        self.open_door_prompts = []
        self.product = self.get_product()
        self.inserts = utils.get_insert_bp_list(self.product.obj_bp,[])
        for insert in self.inserts:
            if "Door Options" in insert.mv.PromptPage.COL_MainTab:
                door = fd_types.Assembly(insert)
                door_rotation = door.get_prompt("Door Rotation")
                if door_rotation:
                    self.open_door_prompts.append(door_rotation)
                    self.door_rotation = door_rotation.value()
                self.show_exterior_options = True
            if "Drawer Options" in insert.mv.PromptPage.COL_MainTab:
                self.show_exterior_options = True
            if "Interior Options" in insert.mv.PromptPage.COL_MainTab:
                self.show_interior_options = True
            if "Opening Heights" in insert.mv.PromptPage.COL_MainTab:
                self.show_splitter_options = True
            if "Opening Widths" in insert.mv.PromptPage.COL_MainTab:
                self.show_splitter_options = True
 
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=utils.get_prop_dialog_width(500))
 
    def draw_carcass_prompts(self,layout):
        for insert in self.inserts:
            if "Carcass Options" in insert.mv.PromptPage.COL_MainTab:
                carcass = fd_types.Assembly(insert)
                left_fin_end = carcass.get_prompt("Left Fin End")
                right_fin_end = carcass.get_prompt("Right Fin End")
#                 left_wall_filler = carcass.get_prompt("Left Side Wall Filler")
#                 right_wall_filler = carcass.get_prompt("Right Side Wall Filler")
                 
                toe_kick_height = carcass.get_prompt("Toe Kick Height")
                remove_bottom = carcass.get_prompt("Remove Bottom")
                remove_back = carcass.get_prompt("Remove Back")
                use_thick_back = carcass.get_prompt("Use Thick Back")
                use_nailers = carcass.get_prompt("Use Nailers")
                cabinet_depth_left = carcass.get_prompt("Cabinet Depth Left")
                cabinet_depth_right = carcass.get_prompt("Cabinet Depth Right")
                 
                # SIDE OPTIONS:
                col = layout.column(align=True)
                col.label("Side Options:")
                row = col.row()
                row.prop(left_fin_end,'CheckBoxValue',text="Left Fin End")
                row.prop(right_fin_end,'CheckBoxValue',text="Right Fin End")
                 
                # CARCASS OPTIONS:
                col = layout.column(align=True)
                col.label("Carcass Options:")
                row = col.row()
                if use_thick_back:
                    row.prop(use_thick_back,'CheckBoxValue',text="Use Thick Back")
                if use_nailers:
                    row.prop(use_nailers,'CheckBoxValue',text="Use Nailers")
                if remove_bottom:
                    row.prop(remove_bottom,'CheckBoxValue',text="Remove Bottom")
                if remove_back:
                    row.prop(remove_back,'CheckBoxValue',text="Remove Back")
                if cabinet_depth_left:
                    row = col.row()
                    row.prop(cabinet_depth_left,'DistanceValue',text="Cabinet Depth Left")
                    row.prop(cabinet_depth_right,'DistanceValue',text="Cabinet Depth Right")
                 
                # TOE KICK OPTIONS
                if toe_kick_height:
                    col = layout.column(align=True)
                    toe_kick_setback = carcass.get_prompt("Toe Kick Setback")
                    col.label("Toe Kick Options:")
                    row = col.row()
                    row.prop(toe_kick_height,'DistanceValue',text="Toe Kick Height")
                    row.prop(toe_kick_setback,'DistanceValue',text="Toe Kick Setback")
                     
            if "Countertop Options" in insert.mv.PromptPage.COL_MainTab:
                ctop = fd_types.Assembly(insert)
                Add_Backsplash = ctop.get_prompt("Add Backsplash")
                Add_Left_Backsplash = ctop.get_prompt("Add Left Backsplash")
                Add_Right_Backsplash = ctop.get_prompt("Add Right Backsplash")
                Countertop_Overhang_Front = self.product.get_prompt("Countertop Overhang Front")
                Countertop_Overhang_Back = self.product.get_prompt("Countertop Overhang Back")
                Countertop_Overhang_Left = self.product.get_prompt("Countertop Overhang Left")
                Countertop_Overhang_Right = self.product.get_prompt("Countertop Overhang Right")
                col = layout.column(align=True)
                col.label("Countertop Options:")
                
                if Add_Backsplash and Add_Left_Backsplash and Add_Right_Backsplash:
                    row = col.row()
                    row.label("Add Splash:")
                    row.prop(Add_Backsplash,'CheckBoxValue',text="Back")
                    row.prop(Add_Left_Backsplash,'CheckBoxValue',text="Left")
                    row.prop(Add_Right_Backsplash,'CheckBoxValue',text="Right")
                
                if Countertop_Overhang_Front:
                    row = col.row(align=True)
                    row.label("Overhang:")
                    row.prop(Countertop_Overhang_Front,'DistanceValue',text="Front")
                    row.prop(Countertop_Overhang_Back,'DistanceValue',text="Back")
                    row.prop(Countertop_Overhang_Left,'DistanceValue',text="Left")
                    row.prop(Countertop_Overhang_Right,'DistanceValue',text="Right")
                     
    def draw_door_prompts(self,layout):
        for insert in self.inserts:
            if "Door Options" in insert.mv.PromptPage.COL_MainTab:
                 
                #TODO make pie cut door insert rot z for door open
                if "Pie Cut" not in insert.mv.name_object:
                    row = layout.row()
                    row.label("Open")
                    row.prop(self,'door_rotation',text="",slider=True)
                    break
             
        for insert in self.inserts:
            if "Door Options" in insert.mv.PromptPage.COL_MainTab:
                box = layout.box()
                col = box.column(align=True)
                col.label(insert.mv.name_object + " Options:")
                door = fd_types.Assembly(insert)
                left_swing = door.get_prompt("Left Swing")
                inset_front = door.get_prompt("Inset Front")
                 
                row = col.row()
                row.label("Inset Door")
                row.prop(inset_front,'CheckBoxValue',text="")
 
                if left_swing:
                    row = col.row()
                    row.label("Left Door Swing")
                    row.prop(left_swing,'CheckBoxValue',text="")
         
    def draw_drawer_prompts(self,layout):
        for insert_bp in self.inserts:
            if "Drawer Options" in insert_bp.mv.PromptPage.COL_MainTab:
                insert = fd_types.Assembly(insert_bp)
                open_prompt = insert.get_prompt("Open")
                 
                if open_prompt:
                    row = layout.row()
                    row.label("Open Drawer")
                    row.prop(open_prompt,"PercentageValue",text="")
                 
                box = layout.box()
                col = box.column(align=True)
                row = col.row()
                row.label(insert_bp.mv.name_object + " Options:")
                 
                inset_front = insert.get_prompt("Inset Front")
                half_overlay_top = insert.get_prompt("Half Overlay Top")
                 
                if inset_front:
                    row.prop(inset_front,'CheckBoxValue',text="Inset Front")
                     
                if half_overlay_top:
                    half_overlay_bottom = insert.get_prompt("Half Overlay Bottom")
                    half_overlay_left = insert.get_prompt("Half Overlay Left")
                    half_overlay_right = insert.get_prompt("Half Overlay Right")
                    row = col.row()
                    row.label("Half Overlays:")
                    row.prop(half_overlay_top,'CheckBoxValue',text="Top")
                    row.prop(half_overlay_bottom,'CheckBoxValue',text="Bottom")
                    row.prop(half_overlay_left,'CheckBoxValue',text="Left")
                    row.prop(half_overlay_right,'CheckBoxValue',text="Right")
                 
            if "Drawer Heights" in insert_bp.mv.PromptPage.COL_MainTab:
                insert = fd_types.Assembly(insert_bp)
                drawer_height_1 = insert.get_prompt("Top Drawer Height")
                drawer_height_2 = insert.get_prompt("Second Drawer Height")
                drawer_height_3 = insert.get_prompt("Third Drawer Height")
                drawer_height_4 = insert.get_prompt("Bottom Drawer Height")
                 
                if drawer_height_1:
                    row = box.row()
                    row.label("Drawer 1 Height:")
                    if drawer_height_1.equal:
                        row.label(str(unit.meter_to_active_unit(drawer_height_1.DistanceValue)))
                        row.prop(drawer_height_1,'equal',text="")
                    else:
                        row.prop(drawer_height_1,'DistanceValue',text="")
                        row.prop(drawer_height_1,'equal',text="")
                 
                if drawer_height_2:
                    row = box.row()
                    row.label("Drawer 2 Height:")
                    if drawer_height_2.equal:
                        row.label(str(unit.meter_to_active_unit(drawer_height_2.DistanceValue)))
                        row.prop(drawer_height_2,'equal',text="")
                    else:
                        row.prop(drawer_height_2,'DistanceValue',text="")
                        row.prop(drawer_height_2,'equal',text="")
                 
                if drawer_height_3:
                    row = box.row()
                    row.label("Drawer 3 Height:")
                    if drawer_height_3.equal:
                        row.label(str(unit.meter_to_active_unit(drawer_height_3.DistanceValue)))
                        row.prop(drawer_height_3,'equal',text="")
                    else:
                        row.prop(drawer_height_3,'DistanceValue',text="")
                        row.prop(drawer_height_3,'equal',text="")
                 
                if drawer_height_4:
                    row = box.row()
                    row.label("Drawer 4 Height:")
                    if drawer_height_4.equal:
                        row.label(str(unit.meter_to_active_unit(drawer_height_4.DistanceValue)))
                        row.prop(drawer_height_4,'equal',text="")
                    else:
                        row.prop(drawer_height_4,'DistanceValue',text="")
                        row.prop(drawer_height_4,'equal',text="")
         
    def draw_face_frame_options(self,layout):
        top_rail_width = self.product.get_prompt("Top Rail Width")
        bottom_rail_width = self.product.get_prompt("Bottom Rail Width")
        left_stile_width = self.product.get_prompt("Left Stile Width")
        right_stile_width = self.product.get_prompt("Right Stile Width")
         
        if top_rail_width:
            box = layout.box()
            box.label("Face Frame Options:")
            row = box.row()
            row.prop(top_rail_width,"DistanceValue",text="Top Rail Width") 
            row.prop(bottom_rail_width,"DistanceValue",text="Bottom Rail Width") 
            row = box.row()
            row.prop(left_stile_width,"DistanceValue",text="Left Stile Width") 
            row.prop(right_stile_width,"DistanceValue",text="Right Stile Width") 
             
    def draw_interior_prompts(self,layout):
        for insert in self.inserts:
            if "Interior Options" in insert.mv.PromptPage.COL_MainTab:
                box = layout.box()
                col = box.column(align=True)
                col.label("Interior Options:")
                carcass = fd_types.Assembly(insert)
                adj_shelf_qty = carcass.get_prompt("Adj Shelf Qty")
                fix_shelf_qty = carcass.get_prompt("Fixed Shelf Qty")
                div_qty_per_row = carcass.get_prompt("Divider Qty Per Row")
                division_qty = carcass.get_prompt("Division Qty")
                adj_shelf_rows = carcass.get_prompt("Adj Shelf Rows")
                fixed_shelf_rows = carcass.get_prompt("Fixed Shelf Rows")
                 
                if adj_shelf_qty:
                    row = col.row()
                    row.label("Adjustable Shelf Qty")
                    row.prop(adj_shelf_qty,'QuantityValue',text="")
         
                    row.label("Fixed Shelf Qty")
                    row.prop(fix_shelf_qty,'QuantityValue',text="")
                     
                if div_qty_per_row:
                    row = col.row()
                    row.label("Divider Qty Per Row")
                    row.prop(div_qty_per_row,'QuantityValue',text="")
                 
                if division_qty:
                    row = col.row()
                    row.label("Division Qty")
                    row.prop(division_qty,'QuantityValue',text="")
                 
                if adj_shelf_rows:
                    row = col.row()
                    row.label("Adjustable Shelf Rows")
                    row.prop(adj_shelf_rows,'QuantityValue',text="")
                     
                    row.label("Fixed Shelf Rows")
                    row.prop(fixed_shelf_rows,'QuantityValue',text="")
         
    def draw_splitter_prompts(self,layout):
        for insert in self.inserts:
            if "Opening Heights" in insert.mv.PromptPage.COL_MainTab:
                box = layout.box()
                col = box.column(align=True)
                col.label("Splitter Options:")
                splitter = fd_types.Assembly(insert)
                opening_1 = splitter.get_prompt("Opening 1 Height")
                opening_2 = splitter.get_prompt("Opening 2 Height")
                opening_3 = splitter.get_prompt("Opening 3 Height")
                opening_4 = splitter.get_prompt("Opening 4 Height")
                 
                if opening_1:
                    row = col.row()
                    row.label("Opening 1 Height:")
                    if opening_1.equal:
                        row.label(str(unit.meter_to_active_unit(opening_1.DistanceValue)))
                        row.prop(opening_1,'equal',text="")
                    else:
                        row.prop(opening_1,'DistanceValue',text="")
                        row.prop(opening_1,'equal',text="")
                if opening_2:
                    row = col.row()
                    row.label("Opening 2 Height:")
                    if opening_2.equal:
                        row.label(str(unit.meter_to_active_unit(opening_2.DistanceValue)))
                        row.prop(opening_2,'equal',text="")
                    else:
                        row.prop(opening_2,'DistanceValue',text="")
                        row.prop(opening_2,'equal',text="")
                if opening_3:
                    row = col.row()
                    row.label("Opening 3 Height:")
                    if opening_3.equal:
                        row.label(str(unit.meter_to_active_unit(opening_3.DistanceValue)))
                        row.prop(opening_3,'equal',text="")
                    else:
                        row.prop(opening_3,'DistanceValue',text="")
                        row.prop(opening_3,'equal',text="")
                if opening_4:
                    row = col.row()
                    row.label("Opening 4 Height:")
                    if opening_4.equal:
                        row.label(str(unit.meter_to_active_unit(opening_4.DistanceValue)))
                        row.prop(opening_4,'equal',text="")
                    else:
                        row.prop(opening_4,'DistanceValue',text="")
                        row.prop(opening_4,'equal',text="")
         
    def draw(self, context):
        layout = self.layout
        if self.product.obj_bp:
            if self.product.obj_bp.name in context.scene.objects:
                box = layout.box()
                  
                split = box.split(percentage=.8)
                split.label(self.product.obj_bp.mv.name_object + " | " + self.product.obj_bp.cabinetlib.spec_group_name,icon='LATTICE_DATA')
                split.menu('MENU_Current_Cabinet_Menu',text="Menu",icon='DOWNARROW_HLT')
                
                self.draw_product_size(box)
                
                prompt_box = box.box()
                row = prompt_box.row(align=True)
                row.prop_enum(self, "product_tabs", 'CARCASS') 
                if self.show_exterior_options:
                    row.prop_enum(self, "product_tabs", 'EXTERIOR') 
                if self.show_interior_options:
                    row.prop_enum(self, "product_tabs", 'INTERIOR') 
                if self.show_splitter_options:
                    row.prop_enum(self, "product_tabs", 'SPLITTER') 
                row.prop_enum(self, "product_tabs", 'FACEFRAME') 
                if self.product_tabs == 'CARCASS':
                    self.draw_carcass_prompts(prompt_box)
                if self.product_tabs == 'FACEFRAME':
                    self.draw_face_frame_options(prompt_box)
                if self.product_tabs == 'EXTERIOR':
                    self.draw_door_prompts(prompt_box)
                    self.draw_drawer_prompts(prompt_box)
                if self.product_tabs == 'INTERIOR':
                    self.draw_interior_prompts(prompt_box)
                if self.product_tabs == 'SPLITTER':
                    self.draw_splitter_prompts(prompt_box)      

bpy.utils.register_class(PANEL_Cabinet_Options)
bpy.utils.register_class(PROMPTS_Door_Prompts)
bpy.utils.register_class(PROMPTS_Drawer_Prompts)
bpy.utils.register_class(PROMPTS_Shelf_Prompts)
bpy.utils.register_class(PROMPTS_Splitter_Prompts)
bpy.utils.register_class(PROMPTS_Column_Prompts)
bpy.utils.register_class(PROMPTS_Angled_Column_Prompts)
bpy.utils.register_class(PROMPTS_Frameless_Cabinet_Prompts)
bpy.utils.register_class(PROMPTS_Face_Frame_Cabinet_Prompts)
    