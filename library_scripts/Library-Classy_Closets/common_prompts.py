from mv import unit
from . import mv_closet_defaults as props_closet

def add_closet_carcass_prompts(assembly):
    props = props_closet.get_scene_props()
    defaults = props.closet_defaults    
    
    assembly.add_prompt(name="Left End Condition",prompt_type='COMBOBOX',items=['EP','WP','CP','OFF'],value=1,tab_index=1,columns=4)
    assembly.add_prompt(name="Right End Condition",prompt_type='COMBOBOX',items=['EP','WP','CP','OFF'],value=1,tab_index=1,columns=4)
    assembly.add_prompt(name="Shelf Gap",prompt_type='DISTANCE',value=0,tab_index=1)
    assembly.add_prompt(name="Left Side Wall Filler",prompt_type='DISTANCE',value=0.0,tab_index=1)
    assembly.add_prompt(name="Right Side Wall Filler",prompt_type='DISTANCE',value=0.0,tab_index=1)
    assembly.add_prompt(name="Left End Deduction",prompt_type='DISTANCE',value=0.0,tab_index=1)
    assembly.add_prompt(name="Right End Deduction",prompt_type='DISTANCE',value=0.0,tab_index=1)
    assembly.add_prompt(name="Toe Kick Height",prompt_type='DISTANCE',value=defaults.toe_kick_height,tab_index=1)
    assembly.add_prompt(name="Toe Kick Setback",prompt_type='DISTANCE',value=defaults.toe_kick_setback,tab_index=1)
    assembly.add_prompt(name="Add Backing",prompt_type='CHECKBOX',value=defaults.add_backing,tab_index=1)
    assembly.add_prompt(name="Add Hutch Backing",prompt_type='CHECKBOX',value=False,tab_index=1)
    assembly.add_prompt(name="Has Capping Bottom",prompt_type='CHECKBOX',value=False,tab_index=1)
    assembly.add_prompt(name="First Rear Notch Height",prompt_type='DISTANCE',value=defaults.rear_notch_height_1,tab_index=1)
    assembly.add_prompt(name="First Rear Notch Depth",prompt_type='DISTANCE',value=defaults.rear_notch_depth_1,tab_index=1)
    assembly.add_prompt(name="Second Rear Notch Height",prompt_type='DISTANCE',value=defaults.rear_notch_height_2,tab_index=1)
    assembly.add_prompt(name="Second Rear Notch Depth",prompt_type='DISTANCE',value=defaults.rear_notch_height_2,tab_index=1)
    assembly.add_prompt(name="Cut to Fit Amount",prompt_type='DISTANCE',value=unit.inch(4),tab_index=1)  
    assembly.add_prompt(name="Drilling Distance From Front",prompt_type='DISTANCE',value=defaults.panel_drilling_from_front,tab_index=1)
    assembly.add_prompt(name="Drilling Distance From Rear",prompt_type='DISTANCE',value=defaults.panel_drilling_from_rear,tab_index=1)
    assembly.add_prompt(name="Add Hanging Rail",prompt_type='CHECKBOX',value=defaults.add_hanging_rail,tab_index=1)
    assembly.add_prompt(name="Hanging Rail Distance From Top",prompt_type='DISTANCE',value=defaults.hanging_rail_distance_from_top,tab_index=1)
    assembly.add_prompt(name="Remove Top Shelf",prompt_type='CHECKBOX',value=defaults.remove_top_shelf,tab_index=1)
    assembly.add_prompt(name="Extend Left Side",prompt_type='CHECKBOX',value=False,tab_index=1)
    assembly.add_prompt(name="Extend Right Side",prompt_type='CHECKBOX',value=False,tab_index=1)
    assembly.add_prompt(name="Height Left Side",prompt_type='DISTANCE',value=0,tab_index=1)
    assembly.add_prompt(name="Height Right Side",prompt_type='DISTANCE',value=0,tab_index=1)
    assembly.add_prompt(name="Loc Left Side",prompt_type='DISTANCE',value=defaults.hanging_height,tab_index=1)
    assembly.add_prompt(name="Loc Right Side",prompt_type='DISTANCE',value=defaults.hanging_height,tab_index=1)
    assembly.add_prompt(name="Height To Add Mid Cleat",prompt_type='DISTANCE',value=defaults.height_to_add_mid_cleat,tab_index=1)
    assembly.add_prompt(name="Dog Ear Each",prompt_type='CHECKBOX',value=defaults.dog_ear_each,tab_index=1)
    assembly.add_prompt(name="Front Angle Height",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1) 
    assembly.add_prompt(name="Front Angle Depth",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)  
    assembly.add_prompt(name="Rear Angle Height",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)  
    assembly.add_prompt(name="Rear Angle Depth",prompt_type='DISTANCE',value=unit.inch(0),tab_index=1)   
    assembly.add_prompt(name="Cleat Height",prompt_type='DISTANCE',value=unit.inch(3.64),tab_index=1)
    assembly.add_prompt(name="Blind Corner Left",prompt_type='CHECKBOX',value=False,tab_index=1)
    assembly.add_prompt(name="Blind Corner Right",prompt_type='CHECKBOX',value=False,tab_index=1)
    assembly.add_prompt(name="Blind Corner Left Depth",prompt_type='DISTANCE',value=unit.inch(18),tab_index=1)
    assembly.add_prompt(name="Blind Corner Right Depth",prompt_type='DISTANCE',value=unit.inch(18),tab_index=1)       
    assembly.add_prompt(name="Opening Height Difference",prompt_type='DISTANCE',value=unit.inch(1.49),tab_index=1)
    assembly.add_prompt(name="Blind Corner Height Difference",prompt_type='DISTANCE',value=unit.inch(0.91),tab_index=1)


    #For adding individual opening prompts
    for i in range(1,assembly.opening_qty+1):
        assembly.add_prompt(name="CTF Opening " + str(i),
                            prompt_type='CHECKBOX',
                            value=False,
                            tab_index=1)
        
        assembly.add_prompt(name="Add " + str(i) + " Top Cleat",
                            prompt_type='CHECKBOX',
                            value=defaults.add_top_cleat,
                            tab_index=2)
        
        assembly.add_prompt(name="Add " + str(i) + " Bottom Cleat",
                            prompt_type='CHECKBOX',
                            value=defaults.add_bottom_cleat,
                            tab_index=2)
                    
        assembly.add_prompt(name="Cleat " + str(i) + " Location",
                            prompt_type='DISTANCE',
                            value=unit.inch(0),
                            tab_index=2)
        
        assembly.add_prompt(name="Remove Bottom Hanging Shelf " + str(i),
                            prompt_type='CHECKBOX',
                            value=props.closet_defaults.remove_bottom_hanging_shelf,
                            tab_index=1)
        
        assembly.add_prompt(name="Remove Top Shelf " + str(i),
                            prompt_type='CHECKBOX',
                            value=props.closet_defaults.remove_top_shelf,
                            tab_index=1)

        assembly.add_prompt(name="Top KD " + str(i) + ' Vertical Offset',
                            prompt_type='DISTANCE',
                            value=0,
                            tab_index=1)

    #For adding individual panel prompts
    for i in range(1,assembly.opening_qty+2):
        assembly.add_prompt(name="Dog Ear Partition " + str(i),
                            prompt_type='CHECKBOX',
                            value=False,
                            tab_index=1)
                    
        assembly.add_prompt(name="Front Angle " + str(i) + " Height",
                            prompt_type='DISTANCE',
                            value=defaults.angle_top_front_panel_height,
                            tab_index=2)    
                    
        assembly.add_prompt(name="Front Angle " + str(i) + " Depth",
                            prompt_type='DISTANCE',
                            value=defaults.angle_top_front_panel_depth,
                            tab_index=2)      
                    
        assembly.add_prompt(name="Rear Angle " + str(i) + " Height",
                            prompt_type='DISTANCE',
                            value=defaults.angle_top_rear_panel_height,
                            tab_index=2)
                    
        assembly.add_prompt(name="Rear Angle " + str(i) + " Depth",
                            prompt_type='DISTANCE',
                            value=defaults.angle_top_rear_panel_depth,
                            tab_index=2)   

    Left_End_Condition = assembly.get_var('Left End Condition')
    Right_End_Condition = assembly.get_var('Right End Condition')
    Left_Side_Thickness = assembly.get_var('Left Side Thickness')
    Right_Side_Thickness = assembly.get_var('Right Side Thickness')    
    Panel_Thickness = assembly.get_var('Panel Thickness')
    Left_Side_Wall_Filler = assembly.get_var('Left Side Wall Filler')
    Right_Side_Wall_Filler = assembly.get_var('Right Side Wall Filler')
    sgi = assembly.get_var('cabinetlib.spec_group_index','sgi')
    
    assembly.prompt("Left Side Thickness", 'IF(Left_End_Condition!=3,THICKNESS(sgi,"Panel"),0)',[Left_End_Condition,sgi])
    assembly.prompt("Right Side Thickness", 'IF(Right_End_Condition!=3,THICKNESS(sgi,"Panel"),0)',[Right_End_Condition,sgi])
    
    assembly.calculator_deduction("Left_Side_Thickness+Right_Side_Thickness+Panel_Thickness*(" + str(assembly.opening_qty) +"-1)+Left_Side_Wall_Filler+Right_Side_Wall_Filler",
                                 [Left_Side_Thickness,Right_Side_Thickness,Panel_Thickness,Left_Side_Wall_Filler,Right_Side_Wall_Filler])            
        
def add_countertop_prompts(assembly,prompt_tab=0):
    assembly.add_prompt(name="Deck Overhang",prompt_type='DISTANCE',value=unit.inch(1.5),tab_index=prompt_tab)
    assembly.add_prompt(name="Side Deck Overhang",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=prompt_tab)
    
    assembly.add_prompt(name="Countertop Type",
                          prompt_type='COMBOBOX',
                          value=0,
                          tab_index=prompt_tab,
                          items=['Melamine',
                                 'HPL',
                                 'Granite'],
                          columns=3) #2
    
    assembly.add_prompt(name="Countertop Thickness",
                          prompt_type='COMBOBOX',
                          value=0,
                          tab_index=prompt_tab,
                          items=['.75',
                                 '1.0'],
                          columns=2)
    
    assembly.add_prompt(name="Edge Type",
                          prompt_type='COMBOBOX',
                          value=1,
                          tab_index=prompt_tab,
                          items=['Waterfall',
                                 'Flat Front',
                                 '180 Degree',
                                 'Alder Miter'],
                          columns=2)
     
    assembly.add_prompt(name="HPL Material Name",prompt_type='TEXT',value="",tab_index=prompt_tab)
    assembly.add_prompt(name="HPL Material Number",prompt_type='TEXT',value="",tab_index=prompt_tab)
    assembly.add_prompt(name="Deck Thickness",prompt_type='DISTANCE',value=unit.inch(1.5),tab_index=prompt_tab) #1.5
    
    Countertop_Type = assembly.get_var('Countertop Type')

    #assembly.prompt("Deck Thickness",'IF(Countertop_Type==2,INCH(.75),INCH(.75))',
    #                [Countertop_Type])

def add_front_overlay_prompts(assembly):
    #Requires add_thickness_prompts to be added
    
    assembly.add_prompt(name="Inset Front",prompt_type='CHECKBOX',value=False,tab_index=0)
    assembly.add_prompt(name="Half Overlay Top",prompt_type='CHECKBOX',value=True,tab_index=0)
    assembly.add_prompt(name="Half Overlay Bottom",prompt_type='CHECKBOX',value=True,tab_index=0)
    assembly.add_prompt(name="Half Overlay Left",prompt_type='CHECKBOX',value=True,tab_index=0)
    assembly.add_prompt(name="Half Overlay Right",prompt_type='CHECKBOX',value=True,tab_index=0)
    assembly.add_prompt(name="Full Overlay",prompt_type='CHECKBOX',value=False,tab_index=0)
    assembly.add_prompt(name="Top Reveal",prompt_type='DISTANCE',value=unit.inch(0.125),tab_index=0)
    assembly.add_prompt(name="Bottom Reveal",prompt_type='DISTANCE',value=unit.inch(0.125),tab_index=0)
    assembly.add_prompt(name="Left Reveal",prompt_type='DISTANCE',value=unit.inch(0.125),tab_index=0)
    assembly.add_prompt(name="Right Reveal",prompt_type='DISTANCE',value=unit.inch(0.125),tab_index=0)
    assembly.add_prompt(name="Inset Reveal",prompt_type='DISTANCE',value=unit.inch(0.125),tab_index=0) 
    assembly.add_prompt(name="Horizontal Gap",prompt_type='DISTANCE',value=unit.inch(.1588),tab_index=0)
    assembly.add_prompt(name="Vertical Gap",prompt_type='DISTANCE',value=unit.inch(.125),tab_index=0)
    assembly.add_prompt(name="Door to Cabinet Gap",prompt_type='DISTANCE',value=unit.inch(0.01),tab_index=0)
    assembly.add_prompt(name="True Width Overlay",prompt_type='DISTANCE',value=unit.inch(0.58),tab_index=0)
    assembly.add_prompt(name="True Height Overlay",prompt_type='DISTANCE',value=unit.inch(0.58),tab_index=0)
    assembly.add_prompt(name="Double Door Half Overlay Difference",prompt_type='DISTANCE',value=unit.inch(0.09),tab_index=0)
    assembly.add_prompt(name="Double Door Full Overlay Difference",prompt_type='DISTANCE',value=unit.inch(0.375),tab_index=0)
    assembly.add_prompt(name="Single Door Full Overlay Difference",prompt_type='DISTANCE',value=unit.inch(0.25),tab_index=0)      
    
    assembly.add_prompt(name="Top Overlay",prompt_type='DISTANCE',value=0,tab_index=0)
    assembly.add_prompt(name="Bottom Overlay",prompt_type='DISTANCE',value=0,tab_index=0)
    assembly.add_prompt(name="Left Overlay",prompt_type='DISTANCE',value=0,tab_index=0)
    assembly.add_prompt(name="Right Overlay",prompt_type='DISTANCE',value=0,tab_index=0)
    
    inset = assembly.get_var('Inset Front','inset')
    inset_reveal = assembly.get_var('Inset Reveal','inset_reveal')
    lst = assembly.get_var('Left Side Thickness','lst')
    rst = assembly.get_var('Right Side Thickness','rst')
    tt = assembly.get_var('Top Thickness','tt')
    bt = assembly.get_var('Bottom Thickness','bt')
    hot = assembly.get_var("Half Overlay Top",'hot')
    hob = assembly.get_var("Half Overlay Bottom",'hob')
    hol = assembly.get_var("Half Overlay Left",'hol')
    hor = assembly.get_var("Half Overlay Right",'hor')  
    tr = assembly.get_var("Top Reveal",'tr')
    br = assembly.get_var("Bottom Reveal",'br')
    lr = assembly.get_var("Left Reveal",'lr')
    rr = assembly.get_var("Right Reveal",'rr')
    two = assembly.get_var("True Width Overlay",'two')
    tho = assembly.get_var("True Height Overlay",'tho')
    
    assembly.prompt("Top Overlay","IF(inset,-inset_reveal,IF(hot,tho/2,tho))",
                    [inset,inset_reveal,hot,tho])

    #assembly.prompt("Top Overlay","IF(inset,-inset_reveal,IF(hot,(tt/2)-(tr/2),tt-tr))",
                    #[inset,inset_reveal,hot,tt,tr])
    
    assembly.prompt("Bottom Overlay","IF(inset,-inset_reveal,IF(hob,tho/2,tho))",
                    [inset,inset_reveal,hob,tho])

    #assembly.prompt("Bottom Overlay","IF(inset,-inset_reveal,IF(hob,(bt/2)-(br/2),bt-br))",
                    #[inset,inset_reveal,hob,bt,br])
    
    assembly.prompt("Left Overlay","IF(inset,-inset_reveal,IF(hol,two/2,two))",
                    [inset,inset_reveal,hol,two])

    #assembly.prompt("Left Overlay","IF(inset,-inset_reveal,IF(hol,(lst/2)-(lr/2),lst-lr))",
                    #[inset,inset_reveal,hol,lst,lr])
    
    assembly.prompt("Right Overlay","IF(inset,-inset_reveal,IF(hor,two/2,two))",
                    [inset,inset_reveal,hor,two])

    #assembly.prompt("Right Overlay","IF(inset,-inset_reveal,IF(hor,(rst/2)-(rr/2),rst-rr))",
                    #[inset,inset_reveal,hor,rst,rr])  
    
def add_pull_prompts(assembly):
    props = props_closet.get_scene_props()
    
    assembly.add_prompt(name="Open",prompt_type='PERCENTAGE',value=0,tab_index=0)
    assembly.add_prompt(name="No Pulls",prompt_type='CHECKBOX',value=props.closet_defaults.no_pulls,tab_index=0)
    assembly.add_prompt(name="Pull Rotation",prompt_type='ANGLE',value=0,tab_index=0)
    assembly.add_prompt(name="Pull Length",prompt_type='DISTANCE',value=0,tab_index=1)
    
def add_door_pull_prompts(assembly):
    assembly.add_prompt(name="Pull From Edge",prompt_type='DISTANCE',value=unit.inch(1.5),tab_index=0)
    assembly.add_prompt(name="Base Pull Location",prompt_type='DISTANCE',value=unit.inch(2),tab_index=0)
    assembly.add_prompt(name="Tall Pull Location",prompt_type='DISTANCE',value=unit.inch(40),tab_index=0)
    assembly.add_prompt(name="Upper Pull Location",prompt_type='DISTANCE',value=unit.inch(2),tab_index=0)
    
def add_door_prompts(assembly):
    props = props_closet.get_scene_props()
    
    assembly.add_prompt(name="Door Type",prompt_type='COMBOBOX',value=0,tab_index=0,items=['Base','Tall','Upper'],columns=3)
    assembly.add_prompt(name="Door Rotation",prompt_type='ANGLE',value=120,tab_index=0)
    assembly.add_prompt(name="Use Left Swing",prompt_type='CHECKBOX',value=False,tab_index=0)
    assembly.add_prompt(name="Force Double Doors",prompt_type='CHECKBOX',value=False,tab_index=0)
    assembly.add_prompt(name="Double Door Auto Switch",prompt_type='DISTANCE',value=props.closet_defaults.double_door_auto_switch,tab_index=0)
    assembly.add_prompt(name="Lucite Doors",prompt_type='CHECKBOX',value=False,tab_index=0)
    
def add_door_lock_prompts(assembly):
    assembly.add_prompt(name="Lock to Panel",prompt_type='CHECKBOX',value=False,tab_index=0)
    assembly.add_prompt(name="Lock Door",prompt_type='CHECKBOX',value=False,tab_index=0)
    assembly.add_prompt(name="Double Door Lock Offset", prompt_type='DISTANCE', value=unit.inch(0.8), tab_index=1)
    
def add_drawer_pull_prompts(assembly):
    assembly.add_prompt(name="Use Double Pulls",prompt_type='CHECKBOX',value=False,tab_index=0)
    assembly.add_prompt(name="Center Pulls on Drawers",prompt_type='CHECKBOX',value=False,tab_index=0)
    assembly.add_prompt(name="Drawer Pull From Top",prompt_type='DISTANCE',value=unit.inch(2.5),tab_index=0)
        
def add_drawer_box_prompts(assembly):
    props = props_closet.get_scene_props()
    defaults = props.closet_defaults
    
    assembly.add_prompt(name="Drawer Box Top Gap",prompt_type='DISTANCE',value=defaults.drawer_box_top_gap,tab_index=0)
    assembly.add_prompt(name="Drawer Box Bottom Gap",prompt_type='DISTANCE',value=defaults.drawer_box_bottom_gap,tab_index=0)
    assembly.add_prompt(name="Drawer Box Slide Gap",prompt_type='DISTANCE',value=defaults.drawer_box_slide_gap,tab_index=0)
    assembly.add_prompt(name="Drawer Box Rear Gap",prompt_type='DISTANCE',value=defaults.drawer_box_rear_gap,tab_index=0)    

def add_toe_kick_prompts(assembly,prompt_tab=0):
    props = props_closet.get_scene_props()
    assembly.add_prompt(name="Toe Kick Height",prompt_type='DISTANCE',value=props.closet_defaults.toe_kick_height,tab_index=prompt_tab,export=True)
    assembly.add_prompt(name="Toe Kick Setback",prompt_type='DISTANCE',value=props.closet_defaults.toe_kick_setback,tab_index=prompt_tab,export=True)

def add_thickness_prompts(assembly):
    assembly.add_prompt(name="Panel Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
    assembly.add_prompt(name="Front Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
    assembly.add_prompt(name="Left Side Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
    assembly.add_prompt(name="Right Side Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
    assembly.add_prompt(name="Top Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
    assembly.add_prompt(name="Bottom Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
    assembly.add_prompt(name="Back Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
    assembly.add_prompt(name="Shelf Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
    assembly.add_prompt(name="Division Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
    assembly.add_prompt(name="Toe Kick Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
    assembly.add_prompt(name="Cleat Thickness",prompt_type='DISTANCE',value=unit.inch(0.75),tab_index=1)
    
    #FORMULAS TO REFERENCE SPEC GROUP THICKNESS
    sgi = assembly.get_var('cabinetlib.spec_group_index','sgi')
    assembly.prompt('Panel Thickness','THICKNESS(sgi,"Panel")',[sgi])
    assembly.prompt('Front Thickness','THICKNESS(sgi,"Slab_Door")',[sgi])
    assembly.prompt('Top Thickness','THICKNESS(sgi,"Shelf")',[sgi])
    assembly.prompt('Bottom Thickness','THICKNESS(sgi,"Shelf")',[sgi])
    assembly.prompt('Back Thickness','THICKNESS(sgi,"Back")',[sgi])
    assembly.prompt('Shelf Thickness','THICKNESS(sgi,"Shelf")',[sgi])
    assembly.prompt('Division Thickness','THICKNESS(sgi,"Panel")',[sgi])
    assembly.prompt('Toe Kick Thickness','THICKNESS(sgi,"Toe_Kick")',[sgi])
    assembly.prompt('Cleat Thickness','THICKNESS(sgi,"Cleat")',[sgi])
    