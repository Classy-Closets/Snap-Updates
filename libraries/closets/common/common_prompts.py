from snap import sn_unit
from snap.libraries.closets import closet_props
from snap.libraries.closets import closet_utils
import bpy


def add_closet_carcass_prompts(assembly):
    scene_props = bpy.context.scene.sn_closets
    defaults = scene_props.closet_defaults

    assembly.add_prompt("Left End Condition", 'COMBOBOX', 1, ['EP', 'WP', 'CP', 'OFF'])
    assembly.add_prompt("Right End Condition", 'COMBOBOX', 1, ['EP', 'WP', 'CP', 'OFF'])
    assembly.add_prompt("Shelf Gap", 'DISTANCE', 0)
    assembly.add_prompt("Add Left Filler", 'CHECKBOX', False)
    assembly.add_prompt("Add Right Filler", 'CHECKBOX', False)
    assembly.add_prompt("Left Side Wall Filler", 'DISTANCE', 0.0)
    assembly.add_prompt("Right Side Wall Filler", 'DISTANCE', 0.0)
    assembly.add_prompt("Add Capping Left Filler", 'CHECKBOX', False)
    assembly.add_prompt("Add Capping Right Filler", 'CHECKBOX', False)
    assembly.add_prompt("Left Filler Setback Amount", 'DISTANCE', 0.0)
    assembly.add_prompt("Right Filler Setback Amount", 'DISTANCE', 0.0)
    assembly.add_prompt("Left End Deduction", 'DISTANCE', 0.0)
    assembly.add_prompt("Right End Deduction", 'DISTANCE', 0.0)
    assembly.add_prompt("Toe Kick Height", 'DISTANCE', defaults.toe_kick_height)
    assembly.add_prompt("Toe Kick Setback", 'DISTANCE', defaults.toe_kick_setback)
    assembly.add_prompt("Add Backing", 'CHECKBOX', defaults.add_backing)
    assembly.add_prompt("Add Hutch Backing", 'CHECKBOX', False)
    assembly.add_prompt("Has Capping Bottom", 'CHECKBOX', False)
    assembly.add_prompt("First Rear Notch Height", 'DISTANCE', defaults.rear_notch_height_1)
    assembly.add_prompt("First Rear Notch Depth", 'DISTANCE', defaults.rear_notch_depth_1)
    assembly.add_prompt("Second Rear Notch Height", 'DISTANCE', defaults.rear_notch_height_2)
    assembly.add_prompt("Second Rear Notch Depth", 'DISTANCE', defaults.rear_notch_height_2)
    assembly.add_prompt("Cut to Fit Amount", 'DISTANCE', sn_unit.inch(4))
    assembly.add_prompt("Drilling Distance From Front", 'DISTANCE', defaults.panel_drilling_from_front)
    assembly.add_prompt("Drilling Distance From Rear", 'DISTANCE', defaults.panel_drilling_from_rear)
    assembly.add_prompt("Add Hanging Rail", 'CHECKBOX', defaults.add_hanging_rail)
    assembly.add_prompt("Hanging Rail Distance From Top", 'DISTANCE', defaults.hanging_rail_distance_from_top)
    assembly.add_prompt("Remove Top Shelf", 'CHECKBOX', defaults.remove_top_shelf)
    assembly.add_prompt("Extend Left End Pard Forward", 'CHECKBOX', False)
    assembly.add_prompt("Extend Right End Pard Forward", 'CHECKBOX', False)
    assembly.add_prompt("Extend Left End Pard Down", 'CHECKBOX', False)
    assembly.add_prompt("Extend Right End Pard Down", 'CHECKBOX', False)
    assembly.add_prompt("Height Left Side", 'DISTANCE', 0)
    assembly.add_prompt("Height Right Side", 'DISTANCE', 0)
    assembly.add_prompt("Loc Left Side", 'DISTANCE', defaults.hanging_height)
    assembly.add_prompt("Loc Right Side", 'DISTANCE', defaults.hanging_height)
    assembly.add_prompt("Height To Add Mid Cleat", 'DISTANCE', defaults.height_to_add_mid_cleat)
    assembly.add_prompt("Capping Options", 'CHECKBOX', False)
    assembly.add_prompt("Edge Bottom of Filler", 'CHECKBOX', False)
    assembly.add_prompt("Edge Bottom of Left Filler", 'CHECKBOX', False)
    assembly.add_prompt("Edge Bottom of Right Filler", 'CHECKBOX', False)
    assembly.add_prompt("Dog Ear Active", 'CHECKBOX', defaults.dog_ear_active)
    assembly.add_prompt("Front Angle Height", 'DISTANCE', sn_unit.inch(0))
    assembly.add_prompt("Front Angle Depth", 'DISTANCE', defaults.panel_depth)
    assembly.add_prompt("Cleat Height", 'DISTANCE', sn_unit.inch(3.64))
    assembly.add_prompt("Blind Corner Left", 'CHECKBOX', False)
    assembly.add_prompt("Blind Corner Right", 'CHECKBOX', False)
    assembly.add_prompt("Blind Corner Left Depth", 'DISTANCE', sn_unit.inch(18))
    assembly.add_prompt("Blind Corner Right Depth", 'DISTANCE', sn_unit.inch(18))
    assembly.add_prompt("Opening Height Difference", 'DISTANCE', sn_unit.inch(1.49))
    assembly.add_prompt("Blind Corner Height Difference", 'DISTANCE', sn_unit.inch(0.91))

    # For adding individual opening prompts
    for i in range(1, assembly.opening_qty + 1):
        assembly.add_prompt("Add Full Back " + str(i), 'CHECKBOX', False)
        assembly.add_prompt("CTF Opening " + str(i), 'CHECKBOX', False)
        assembly.add_prompt("Add " + str(i) + " Top Cleat", 'CHECKBOX', defaults.add_top_cleat)
        assembly.add_prompt("Add " + str(i) + " Bottom Cleat", 'CHECKBOX', defaults.add_bottom_cleat)
        assembly.add_prompt("Use " + str(i) + " Custom Cleat Location", 'CHECKBOX', False)
        assembly.add_prompt("Cleat " + str(i) + " Location", 'DISTANCE', 0)
        assembly.add_prompt("Remove Bottom Hanging Shelf " + str(i),
                            'CHECKBOX',
                            defaults.remove_bottom_hanging_shelf)
        assembly.add_prompt("Remove Top Shelf " + str(i),
                            'CHECKBOX',
                            defaults.remove_top_shelf)
        assembly.add_prompt("Top KD " + str(i) + " Vertical Offset",
                            'DISTANCE',
                            0)

    # For adding individual panel prompts
    for i in range(1, assembly.opening_qty + 2):
        assembly.add_prompt("Dog Ear Partition " + str(i), 'CHECKBOX', False)
        assembly.add_prompt("Front Angle " + str(i) + " Height", 'DISTANCE', defaults.angle_top_front_panel_height)
        assembly.add_prompt("Front Angle " + str(i) + " Depth", 'DISTANCE', defaults.angle_top_front_panel_depth)

    # Add opening widths calculator
    calc_distance_obj = assembly.add_empty('Calc Distance Obj')
    calc_distance_obj.empty_display_size = .001

    calculator = assembly.obj_prompts.snap.add_calculator(
        "Opening Widths Calculator",
        calc_distance_obj)

    assembly.calculator = calculator
    Product_Width = assembly.obj_x.snap.get_var('location.x', 'Product_Width')
    Panel_Thickness = assembly.get_prompt('Panel Thickness').get_var('Panel_Thickness')
    Left_Side_Wall_Filler = assembly.get_prompt('Left Side Wall Filler').get_var('Left_Side_Wall_Filler')
    Right_Side_Wall_Filler = assembly.get_prompt('Right Side Wall Filler').get_var('Right_Side_Wall_Filler')

    calculator.set_total_distance(
        "Product_Width-Panel_Thickness*{}-Left_Side_Wall_Filler-Right_Side_Wall_Filler".format(str(assembly.opening_qty + 1)),
        [Product_Width, Panel_Thickness, Left_Side_Wall_Filler, Right_Side_Wall_Filler])


def add_countertop_prompts(assembly):
    assembly.add_prompt("Deck Overhang", 'DISTANCE', sn_unit.inch(1.5))
    assembly.add_prompt("Side Deck Overhang", 'DISTANCE', sn_unit.inch(0.75))
    assembly.add_prompt("Countertop Type", 'COMBOBOX', 0, ['Melamine', 'HPL', 'Granite'])
    assembly.add_prompt("Countertop Thickness", 'COMBOBOX', 0, ['.75', '1.0'])
    assembly.add_prompt("Edge Type", 'COMBOBOX', 1, ['Waterfall', 'Flat Front', '180 Degree', 'Alder Miter'])
    assembly.add_prompt("HPL Material Name", 'TEXT', "")
    assembly.add_prompt("HPL Material Number", 'TEXT', "")
    assembly.add_prompt("Deck Thickness", 'DISTANCE', sn_unit.inch(1.5))
    # Countertop_Type = assembly.get_prompt('Countertop Type').get_var('Countertop_Type')
    # deck_thickness = assembly.get_prompt("Deck Thickness")
    # deck_thickness.set_formula('IF(Countertop_Type==2,INCH(.75),INCH(1.5))', [Countertop_Type])


def add_front_overlay_prompts(assembly):
    """
    Requires add_thickness_prompts to be added
    """
    assembly.add_prompt("Top Overlay", "DISTANCE", True)
    assembly.add_prompt("Bottom Overlay", "DISTANCE", True)
    assembly.add_prompt("Left Overlay", "DISTANCE", True)
    assembly.add_prompt("Right Overlay", "DISTANCE", True)    
    assembly.add_prompt("Full Overlay", 'CHECKBOX', False)
    assembly.add_prompt("Top Reveal", 'DISTANCE', sn_unit.inch(0.125))
    assembly.add_prompt("Bottom Reveal", 'DISTANCE', sn_unit.inch(0.125))
    assembly.add_prompt("Left Reveal", 'DISTANCE', sn_unit.inch(0.125))
    assembly.add_prompt("Right Reveal", 'DISTANCE', sn_unit.inch(0.125))
    assembly.add_prompt("Vertical Gap", 'DISTANCE', sn_unit.inch(.125))
    assembly.add_prompt("Door to Cabinet Gap", 'DISTANCE', sn_unit.inch(0.01))
    assembly.add_prompt("Double Door Half Overlay Difference", 'DISTANCE', sn_unit.inch(0.09))
    assembly.add_prompt("Double Door Full Overlay Difference", 'DISTANCE', sn_unit.inch(0.375))
    assembly.add_prompt("Single Door Full Overlay Difference", 'DISTANCE', sn_unit.inch(0.25))

    overlay_prompts = assembly.add_empty("OBJ_PROMPTS_Overlays")
    overlay_prompts.empty_display_size = .01

    overlay_prompts.snap.add_prompt('CHECKBOX', "Inset Front")
    inset = overlay_prompts.snap.get_prompt('Inset Front').get_var('inset')

    hg_ppt = overlay_prompts.snap.add_prompt('DISTANCE', "Horizontal Gap")
    hg_ppt.set_value(sn_unit.inch(.1588))

    inset_reveal_ppt = overlay_prompts.snap.add_prompt('DISTANCE', "Inset Reveal")
    inset_reveal_ppt.set_value(sn_unit.inch(0.125))
    inset_reveal = inset_reveal_ppt.get_var('inset_reveal')

    true_width_ppt = overlay_prompts.snap.add_prompt("DISTANCE", "True Width Overlay")
    true_width_ppt.set_value(sn_unit.inch(0.58))
    two = true_width_ppt.get_var('two')

    true_height_ppt = overlay_prompts.snap.add_prompt("DISTANCE", "True Height Overlay")
    true_height_ppt.set_value(sn_unit.inch(0.58))
    tho = true_height_ppt.get_var('tho')

    half_overlay_top_ppt = overlay_prompts.snap.add_prompt('CHECKBOX', "Half Overlay Top")
    half_overlay_top_ppt.set_value(True)
    hot = half_overlay_top_ppt.get_var('hot')

    half_overlay_bottom_ppt = overlay_prompts.snap.add_prompt("CHECKBOX", 'Half Overlay Bottom')
    half_overlay_bottom_ppt.set_value(True)
    hob = half_overlay_bottom_ppt.get_var('hob')

    half_overlay_left_ppt = overlay_prompts.snap.add_prompt("CHECKBOX", 'Half Overlay Left')
    half_overlay_left_ppt.set_value(True)
    hol = half_overlay_left_ppt.get_var('hol')

    half_overlay_right_ppt = overlay_prompts.snap.add_prompt("CHECKBOX", 'Half Overlay Right')
    half_overlay_right_ppt.set_value(True)
    hor = half_overlay_right_ppt.get_var('hor')

    top_overlay = assembly.get_prompt("Top Overlay")
    top_overlay.set_formula(
        "IF(inset,-inset_reveal,IF(hot,tho/2,tho))",
        [inset, inset_reveal, hot, tho])

    bottom_overlay = assembly.get_prompt("Bottom Overlay")
    bottom_overlay.set_formula(
        "IF(inset,-inset_reveal,IF(hob,tho/2,tho))",
        [inset, inset_reveal, hob, tho])

    left_overlay = assembly.get_prompt("Left Overlay")
    left_overlay.set_formula(
        "IF(inset,-inset_reveal,IF(hol,two/2,two))",
        [inset, inset_reveal, hol, two])

    right_overlay = assembly.get_prompt("Right Overlay")
    right_overlay.set_formula(
        "IF(inset,-inset_reveal,IF(hor,two/2,two))",
        [inset, inset_reveal, hor, two])

    return overlay_prompts


def add_pull_prompts(assembly):
    props = bpy.context.scene.sn_closets

    assembly.add_prompt("Open", 'PERCENTAGE', 0)
    assembly.add_prompt("No Pulls", 'CHECKBOX', props.closet_defaults.no_pulls)
    assembly.add_prompt("Pull Rotation", 'ANGLE', 0)
    assembly.add_prompt("Pull Length", 'DISTANCE', 0)


def add_door_pull_prompts(assembly):
    assembly.add_prompt("Pull From Edge", 'DISTANCE', sn_unit.inch(1.5))
    assembly.add_prompt("Base Pull Location", 'DISTANCE', sn_unit.inch(2))
    assembly.add_prompt("Tall Pull Location", 'DISTANCE', sn_unit.inch(40))
    assembly.add_prompt("Upper Pull Location", 'DISTANCE', sn_unit.inch(2))


def add_door_prompts(assembly):
    props = bpy.context.scene.sn_closets

    assembly.add_prompt("Door Type", 'COMBOBOX', 0, ['Base', 'Tall', 'Upper'])
    assembly.add_prompt("Door Rotation", 'ANGLE', 120)
    assembly.add_prompt("Use Left Swing", 'CHECKBOX', False)
    assembly.add_prompt("Force Double Doors", 'CHECKBOX', False)
    assembly.add_prompt("Double Door Auto Switch", 'DISTANCE', props.closet_defaults.double_door_auto_switch)
    assembly.add_prompt("Lucite Doors", 'CHECKBOX', False)


def add_door_lock_prompts(assembly):
    assembly.add_prompt("Lock to Panel", 'CHECKBOX', False)
    assembly.add_prompt("Lock Door", 'CHECKBOX', False)
    assembly.add_prompt("Double Door Lock Offset", 'DISTANCE', sn_unit.inch(0.8))


def add_drawer_pull_prompts(assembly):
    assembly.add_prompt("Use Double Pulls", 'CHECKBOX', False)
    assembly.add_prompt("Center Pulls on Drawers", 'CHECKBOX', False)
    assembly.add_prompt("Drawer Pull From Top", 'DISTANCE', sn_unit.inch(2.5))


def add_drawer_box_prompts(assembly):
    props = bpy.context.scene.sn_closets
    defaults = props.closet_defaults

    assembly.add_prompt("Drawer Box Top Gap", 'DISTANCE', defaults.drawer_box_top_gap)
    assembly.add_prompt("Drawer Box Bottom Gap", 'DISTANCE', defaults.drawer_box_bottom_gap)
    assembly.add_prompt("Drawer Box Slide Gap", 'DISTANCE', defaults.drawer_box_slide_gap)
    assembly.add_prompt("Drawer Box Rear Gap", 'DISTANCE', defaults.drawer_box_rear_gap)


def add_toe_kick_prompts(assembly, prompt_tab=0):
    props = bpy.context.scene.sn_closets
    assembly.add_prompt("Toe Kick Height", 'DISTANCE', props.closet_defaults.toe_kick_height)  # export=True
    assembly.add_prompt("Toe Kick Setback", 'DISTANCE', props.closet_defaults.toe_kick_setback)  # export=True


def add_thickness_prompts(assembly):
    assembly.add_prompt("Panel Thickness", 'DISTANCE', sn_unit.inch(0.75))
    assembly.add_prompt("Front Thickness", 'DISTANCE', sn_unit.inch(0.75))
    assembly.add_prompt("Left Side Thickness", 'DISTANCE', sn_unit.inch(0.75))
    assembly.add_prompt("Right Side Thickness", 'DISTANCE', sn_unit.inch(0.75))
    assembly.add_prompt("Top Thickness", 'DISTANCE', sn_unit.inch(0.75))
    assembly.add_prompt("Bottom Thickness", 'DISTANCE', sn_unit.inch(0.75))
    assembly.add_prompt("Back Thickness", 'DISTANCE', sn_unit.inch(0.25))
    assembly.add_prompt("Shelf Thickness", 'DISTANCE', sn_unit.inch(0.75))
    assembly.add_prompt("Division Thickness", 'DISTANCE', sn_unit.inch(0.75))
    assembly.add_prompt("Toe Kick Thickness", 'DISTANCE', sn_unit.inch(0.75))
    assembly.add_prompt("Cleat Thickness", 'DISTANCE', sn_unit.inch(0.75))
