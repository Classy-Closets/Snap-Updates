import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       BoolVectorProperty,
                       PointerProperty,
                       CollectionProperty,
                       EnumProperty)
import math
import snap_db
from mv import fd_types, unit, utils
from . import mv_closet_defaults as props_closet
from . import common_closet_utils
from . import classy_closets_materials

MACHINING_PROPERTY_NAMESPACE = "mv_closet_machining"

def get_machining_props():
    """ 
    This is a function to get access to all of the scene properties that are registered in this library
    """
    props = eval("bpy.context.scene." + MACHINING_PROPERTY_NAMESPACE)
    return props


class LIST_Mac_Scenes(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(item.name, icon='SCENE_DATA')

    def filter_items(self, context, data, propname):
        flt_flags = []
        flt_neworder = []
        scenes = getattr(data, propname)
        helper_funcs = bpy.types.UI_UL_list
        
        if not flt_flags:
            flt_flags = [self.bitflag_filter_item] * len(scenes)

        for i, scene in enumerate(scenes):
            if scene.mv.plan_view_scene or scene.mv.elevation_scene:
                flt_flags[i] &= ~self.bitflag_filter_item

        flt_neworder = helper_funcs.sort_items_by_name(scenes, "name")

        return flt_flags, flt_neworder


class OPERATOR_Prepare_Closet_For_Export(bpy.types.Operator):
    bl_idname = MACHINING_PROPERTY_NAMESPACE + ".prepare_closet_for_export"
    bl_label = "Prepare Closet for Export"
    bl_description = "This operator perpares all of the closet data in the scene for export to ERP. This adds any additional hardware references and machine tokens."

    def add_hardware(self,name,assembly):
        obj = utils.create_single_vertex(name)
        obj_props = props_closet.get_object_props(obj)
        obj_props.is_temp_hardware = True
        obj.cabinetlib.type_mesh = 'HARDWARE'
        obj.mv.name_object = name
        obj.parent = assembly.obj_bp
        return obj

    def get_product_from_part(self,part):
        product_bp = utils.get_bp(part.obj_bp,'PRODUCT')
        return fd_types.Assembly(product_bp)
    
    def get_hinge_qty(self,length):
        if length > unit.inch(48): 
            return 3
        else:
            return 2    
    
    def get_hinge_name(self):
        p = get_machining_props()
        options = props_closet.get_scene_props().closet_options

        return options.hinge_name
    
    def get_hinge_plate_name(self):
        p = get_machining_props()
        options = props_closet.get_scene_props().closet_options
        
        return "Mounting Plate (600)"
            
    def get_door_pull_name(self):
        options = props_closet.get_scene_props().closet_options
        if options.pull_name == '':
            return "Knob"
        return "Knob"
            
    def remove_machining_token(self,part,name):
        for child in part.obj_bp.children:
            if child.type == 'MESH':
                tokens = child.mv.mp.machine_tokens
                if name in tokens:
                    for index, token in enumerate(tokens):
                        if token.name == name:
                            tokens.remove(index)
                            break

    def add_associative_hinges(self,assembly):
        '''
            If drill for hinges is turned on then we need add hinges and hinge plates
            The names come from machining hinge_name, hinge_plate_name
            the property hinge_from_top_and_bottom and hinge minimum spacing is used
            to determine quantity.
        '''
        macp = get_machining_props()

        door_swing = assembly.get_prompt("Door Swing")
        door_length = assembly.obj_x.location.x
        door_width = assembly.obj_y.location.y # Used to determine swing negative values are left doors
        
        hinge_qty = self.get_hinge_qty(door_length)
        if door_swing.value() in {"Top","Bottom"}:
            spacing = (math.fabs(door_width) - (macp.hinge_location_from_top_and_bottom * 2)) / (hinge_qty - 1)
        else:
            spacing = (door_length - (macp.hinge_location_from_top_and_bottom * 2)) / (hinge_qty - 1)

        hole_qty = math.floor(unit.meter_to_millimeter(spacing) / 32)
        spacing_32mm = hole_qty * unit.millimeter(32)
        
        for i in range(0,hinge_qty):
            
            if door_swing.value() == 'Left' or door_swing.value() == 'Right':
            
                if macp.use_associative_hardware_for_hinges:
                    hinge = self.add_hardware(self.get_hinge_name(),assembly)
                    hinge.lm_closets.is_hinge = True
                    hinge.location.z = unit.inch(.1)
                    hinge.location.y = macp.hinge_cup_off_door_edge if door_width > 0 else -macp.hinge_cup_off_door_edge
                    hinge.location.x = macp.hinge_location_from_top_and_bottom + spacing_32mm*i
                    hinge.mv.associative_rotation = 270 if door_swing.value() == 'Left' else 90
                
                if macp.use_associative_hardware_for_hinge_plates:
                    plate = self.add_hardware(self.get_hinge_plate_name(),assembly)
                    plate.location.z = -macp.hinge_plate_inset_from_door
                    plate.location.y = 0
                    plate.location.x = macp.hinge_location_from_top_and_bottom + spacing_32mm*i
                    plate.mv.associative_rotation = 0
                    
            if door_swing.value() == 'Top':
                if macp.use_associative_hardware_for_hinges:
                    hinge = self.add_hardware(self.get_hinge_name(),assembly)
                    hinge.lm_closets.is_hinge = True
                    hinge.location.z = unit.inch(.1)
                    hinge.location.y = door_length - macp.hinge_cup_off_door_edge
                    hinge.location.x = macp.hinge_location_from_top_and_bottom + spacing_32mm*i
                    hinge.mv.associative_rotation = 180
                    
                if macp.use_associative_hardware_for_hinge_plates:
                    plate = self.add_hardware(self.get_hinge_plate_name(),assembly)
                    plate.location.z = -macp.hinge_plate_inset_from_door
                    plate.location.y = macp.hinge_location_from_top_and_bottom + spacing_32mm*i
                    plate.location.x = door_length
                    plate.mv.associative_rotation = 0
            
            if door_swing.value() == 'Bottom':
                if macp.use_associative_hardware_for_hinges:
                    hinge = self.add_hardware(self.get_hinge_name(),assembly)
                    hinge.lm_closets.is_hinge = True
                    hinge.location.z = unit.inch(.1)
                    hinge.location.y = (macp.hinge_location_from_top_and_bottom + spacing_32mm*i) *-1
                    hinge.location.x = macp.hinge_cup_off_door_edge
                    hinge.mv.associative_rotation = 0
                
                if macp.use_associative_hardware_for_hinge_plates:
                    plate = self.add_hardware(self.get_hinge_plate_name(),assembly)
                    plate.location.z = -macp.hinge_plate_inset_from_door
                    plate.location.y = (macp.hinge_location_from_top_and_bottom + spacing_32mm*i) *-1
                    plate.location.x = 0
                    plate.mv.associative_rotation = 0
    
    def add_door_pull_drilling(self,assembly):
        macp = get_machining_props()
        self.remove_machining_token(assembly, 'Pull Drilling')

        if macp.add_machining_for_pulls:
            no_pulls = assembly.get_prompt("No Pulls")
            
            if not no_pulls.value():
                door_type = assembly.get_prompt("Door Type")
                door_swing = assembly.get_prompt("Door Swing")
                obj, token = assembly.add_machine_token('Pull Drilling' ,'BORE','5')
                
                if door_type.value() == 'Base':
                    if door_swing.value() == 'Bottom':
                        token.dim_in_x = assembly.obj_x.location.x - macp.pull_location_on_base_upper_doors
                        token.end_dim_in_x  = assembly.obj_x.location.x - macp.pull_location_on_base_upper_doors
                    else:
                        token.dim_in_x = assembly.obj_x.location.x - macp.pull_location_on_base_upper_doors
                        token.end_dim_in_x  = assembly.obj_x.location.x - macp.pull_location_on_base_upper_doors - macp.door_pull_length
                elif door_type.value() == 'Upper':
                    token.dim_in_x = macp.pull_location_on_base_upper_doors
                    token.end_dim_in_x  = macp.pull_location_on_base_upper_doors + macp.door_pull_length
                elif door_type.value() == 'Tall':
                    token.dim_in_x = macp.pull_location_on_tall_doors + (macp.door_pull_length/2)
                    token.end_dim_in_x  = macp.pull_location_on_tall_doors - (macp.door_pull_length/2)
                    
                if door_swing.value() == 'Left':
                    token.dim_in_y = macp.pull_from_edge
                    token.end_dim_in_y = macp.pull_from_edge                    
                elif door_swing.value() == 'Right':
                    token.dim_in_y = math.fabs(assembly.obj_y.location.y) - macp.pull_from_edge
                    token.end_dim_in_y = math.fabs(assembly.obj_y.location.y) - macp.pull_from_edge
                else: #TOP AND BOTTOM SWING
                    token.dim_in_y = (math.fabs(assembly.obj_y.location.y)/2) - (macp.door_pull_length/2)
                    token.end_dim_in_y = (math.fabs(assembly.obj_y.location.y)/2) + (macp.door_pull_length/2)
                    
                token.dim_in_z = math.fabs(assembly.obj_z.location.z) + unit.inch(.1)
                token.face_bore_dia = macp.pull_bore_dia
                token.distance_between_holes = macp.door_pull_length

    def add_door_hinge_drilling(self, assembly):
        self.remove_machining_token(assembly, 'Door Hinge Drilling')
        obj, token = assembly.add_machine_token('Door Hinge Drilling' ,'BORE','6')

    def add_hamper_door_hinge_drilling(self, assembly):
        self.remove_machining_token(assembly, 'Hamper Door Hinge Drilling')
        obj, token = assembly.add_machine_token('Hamper Door Hinge Drilling' ,'BORE','6')

    def add_drawer_front_pull_drilling(self,assembly):
        macp = get_machining_props()
        self.remove_machining_token(assembly, 'Pull Drilling')

        print("PULL ASSEMBLY", assembly.obj_bp.name)
        
        if macp.add_machining_for_pulls:
            no_pulls = assembly.get_prompt("No Pulls")
            if not no_pulls.value():
                use_double_pulls = assembly.get_prompt("Use Double Pulls")
                center_pulls_on_drawers = assembly.get_prompt("Center Pulls on Drawers")
                drawer_pull_from_top = assembly.get_prompt("Drawer Pull From Top")
                
                obj, token = assembly.add_machine_token('Pull Drilling' ,'BORE','5')
                token.dim_in_x = (assembly.obj_y.location.y/2) - (macp.drawer_pull_length/2)
                token.end_dim_in_x  = (assembly.obj_y.location.y/2) + (macp.drawer_pull_length/2)
                
                if center_pulls_on_drawers.value():
                    token.dim_in_y = math.fabs(assembly.obj_x.location.x)/2
                    token.end_dim_in_y = math.fabs(assembly.obj_x.location.x)/2
                else:
                    token.dim_in_y = math.fabs(assembly.obj_x.location.x) - drawer_pull_from_top.value()
                    token.end_dim_in_y = math.fabs(assembly.obj_x.location.x) - drawer_pull_from_top.value()
                    
                token.distance_between_holes = macp.drawer_pull_length
                token.dim_in_z = math.fabs(assembly.obj_z.location.z) + unit.inch(.1)
                token.face_bore_dia = macp.pull_bore_dia
                
    def add_hamper_front_hinges(self,assembly):
        macp = get_machining_props()
        door_width = assembly.obj_y.location.y
        
        if macp.use_associative_hardware_for_hinges:
            hinge = self.add_hardware(self.get_hinge_name(),assembly)
            hinge.lm_closets.is_hinge = True
            hinge.location.z = unit.inch(.1)
            hinge.location.y = door_width + macp.hinge_location_from_top_and_bottom
            hinge.location.x = macp.hinge_cup_off_door_edge
            hinge.mv.associative_rotation = 0
        
            hinge = self.add_hardware(self.get_hinge_name(),assembly)
            hinge.lm_closets.is_hinge = True
            hinge.location.z = unit.inch(.1)
            hinge.location.y = - macp.hinge_location_from_top_and_bottom
            hinge.location.x = macp.hinge_cup_off_door_edge
            hinge.mv.associative_rotation = 0  
        
        if macp.use_associative_hardware_for_hinge_plates:
            plate = self.add_hardware(self.get_hinge_plate_name(),assembly)
            plate.location.z = -macp.hinge_plate_inset_from_door
            plate.location.y = - macp.hinge_location_from_top_and_bottom
            plate.location.x = 0
            plate.mv.associative_rotation = 0
        
            plate = self.add_hardware(self.get_hinge_plate_name(),assembly)
            plate.location.z = -macp.hinge_plate_inset_from_door
            plate.location.y = door_width + macp.hinge_location_from_top_and_bottom
            plate.location.x = 0
            plate.mv.associative_rotation = 0
        
    def add_hamper_front_pull_drilling(self,assembly):
        macp = get_machining_props()
        self.remove_machining_token(assembly, 'Pull Drilling')

        if macp.add_machining_for_pulls:

            obj, token = assembly.add_machine_token('Pull Drilling' ,'BORE','5')
            token.dim_in_x = assembly.obj_x.location.x - macp.pull_location_on_base_upper_doors
            token.end_dim_in_x  = assembly.obj_x.location.x - macp.pull_location_on_base_upper_doors            
            token.dim_in_y = (math.fabs(assembly.obj_y.location.y)/2) - (macp.door_pull_length/2)
            token.end_dim_in_y = (math.fabs(assembly.obj_y.location.y)/2) + (macp.door_pull_length/2)
            token.dim_in_z = math.fabs(assembly.obj_z.location.z) + unit.inch(.1)
            token.face_bore_dia = macp.pull_bore_dia
            token.distance_between_holes = macp.door_pull_length        
        
    def add_associative_pull(self,assembly):
        pull = self.add_hardware(self.get_door_pull_name(),assembly)
        pull.location.z = 0
        pull.location.y = 0
        pull.location.x = 0
        pull.mv.associative_rotation = 0

    def add_blind_corner_panel_drilling(self,assembly):
        macp = get_machining_props()
        self.remove_machining_token(assembly, 'System Holes Right Bottom Front')
        self.remove_machining_token(assembly, 'System Holes Right Bottom Rear')

        left = assembly.get_prompt("Is Left Blind Corner Panel")
        right = assembly.get_prompt("Is Right Blind Corner Panel")
        part_length = math.fabs(assembly.obj_x.location.x)
        part_width = math.fabs(assembly.obj_y.location.y)
        dim_to_front = macp.dim_to_front_system_hole
        dim_to_rear = macp.dim_to_rear_system_hole

        if left.value():
            obj, token = assembly.add_machine_token('System Holes Right Bottom Front','BORE','5')
            token.dim_in_x = part_length + unit.inch(0.455) - macp.dim_to_system_top_hole - macp.dim_between_holes
            token.dim_in_y = dim_to_front
            token.dim_in_z = macp.system_hole_bore_depth
            token.end_dim_in_x =  -unit.inch(0.455) + macp.dim_to_system_top_hole + macp.dim_between_holes
            token.end_dim_in_y = dim_to_front + part_width
            token.face_bore_dia = macp.system_hole_dia
            token.distance_between_holes = macp.dim_between_holes
            token.associative_dia = 0
            token.associative_depth = 0

        elif right.value():
            obj, token = assembly.add_machine_token('System Holes Left Bottom Front','BORE','6')
            token.dim_in_x = part_length + unit.inch(0.455) - macp.dim_to_system_top_hole - macp.dim_between_holes
            token.dim_in_y = part_width - dim_to_rear
            token.dim_in_z = macp.system_hole_bore_depth
            token.end_dim_in_x = -unit.inch(0.455) + macp.dim_to_system_top_hole + macp.dim_between_holes
            token.end_dim_in_y = part_width - dim_to_rear
            token.face_bore_dia = macp.system_hole_dia
            token.distance_between_holes = macp.dim_between_holes
            token.associative_dia = 0
            token.associative_depth = 0


    def add_panel_drilling(self,assembly):
        '''
            This should only be added if they have the option to always drill panels turned on.
            Required Panel Prompts - Previous Depth, Next Depth, 
                                     Previous Stop Drilling From Bottom, Previous Stop Drilling From Top
                                     Next Stop Drilling From Bottom, Next Stop Drilling From Top
        '''
        macp = get_machining_props()
        self.remove_machining_token(assembly, 'System Holes Right Bottom Front')
        self.remove_machining_token(assembly, 'System Holes Right Bottom Rear')
        self.remove_machining_token(assembly, 'System Holes Left Bottom Front')
        self.remove_machining_token(assembly, 'System Holes Left Bottom Rear')
        self.remove_machining_token(assembly, 'System Holes Right Top Front')
        self.remove_machining_token(assembly, 'System Holes Right Top Rear')
        self.remove_machining_token(assembly, 'System Holes Left Top Front')
        self.remove_machining_token(assembly, 'System Holes Left Top Rear')

        if macp.panel_drilling_type == '32MM':
            product = self.get_product_from_part(assembly)
            
            part_length = math.fabs(assembly.obj_x.location.x)
            part_width = math.fabs(assembly.obj_y.location.y)
            dim_to_front = macp.dim_to_front_system_hole
            dim_to_rear = macp.dim_to_rear_system_hole
            left_depth = assembly.get_prompt('Left Depth')
            right_depth = assembly.get_prompt('Right Depth')
            sdbl = assembly.get_prompt('Stop Drilling Bottom Left').value()
            sdtl = assembly.get_prompt('Stop Drilling Top Left').value()
            sdbr = assembly.get_prompt('Stop Drilling Bottom Right').value()
            sdtr = assembly.get_prompt('Stop Drilling Top Right').value()
            
            #ALWAYS DRILL BOTTOM
            if right_depth.value() > 0 or sdbr > 0:
                obj, token = assembly.add_machine_token('System Holes Right Bottom Front','BORE','5')
                token.dim_in_x = part_length - unit.millimeter(9.5)
                token.dim_in_y = dim_to_front + (part_width - right_depth.value())
                token.dim_in_z = macp.system_hole_bore_depth
                token.end_dim_in_x = unit.millimeter(9.5) if sdbr == 0 else sdbr
                token.end_dim_in_y = dim_to_front + (part_width - right_depth.value())
                token.face_bore_dia = macp.system_hole_dia
                token.distance_between_holes = unit.millimeter(32)
                token.associative_dia = 0
                token.associative_depth = 0
                
                obj, token = assembly.add_machine_token('System Holes Right Bottom Rear','BORE','5')
                token.dim_in_x = part_length - unit.millimeter(9.5)
                token.dim_in_y = part_width - dim_to_rear
                token.dim_in_z = macp.system_hole_bore_depth
                token.end_dim_in_x = unit.millimeter(9.5) if sdbr == 0 else sdbr
                token.end_dim_in_y = part_width - dim_to_rear
                token.face_bore_dia = macp.system_hole_dia
                token.distance_between_holes = unit.millimeter(32)
                token.associative_dia = 0
                token.associative_depth = 0

            if left_depth.value() > 0 or sdbl > 0 or sdbr > 0:
                obj, token = assembly.add_machine_token('System Holes Left Bottom Front','BORE','6')
                token.dim_in_x = part_length - unit.millimeter(9.5)
                token.dim_in_y = dim_to_front + (part_width - left_depth.value())
                token.dim_in_z = macp.system_hole_bore_depth
                token.end_dim_in_x = unit.millimeter(9.5) if sdbl == 0 else sdbl
                token.end_dim_in_y = dim_to_front + (part_width - left_depth.value())
                token.face_bore_dia = macp.system_hole_dia
                token.distance_between_holes = unit.millimeter(32)
                token.associative_dia = 0
                token.associative_depth = 0
                
                obj, token = assembly.add_machine_token('System Holes Left Bottom Rear','BORE','6')
                token.dim_in_x = part_length - unit.millimeter(9.5)
                token.dim_in_y = part_width - dim_to_rear
                token.dim_in_z = macp.system_hole_bore_depth
                token.end_dim_in_x = unit.millimeter(9.5) if sdbl == 0 else sdbl
                token.end_dim_in_y = part_width - dim_to_rear
                token.face_bore_dia = macp.system_hole_dia
                token.distance_between_holes = unit.millimeter(32)
                token.associative_dia = 0
                token.associative_depth = 0
                    
            #DRILL TOP IF STOP DRILLING IS FOUND
            if right_depth.value() > 0 and sdtr > 0:
                obj, token = assembly.add_machine_token('System Holes Right Top Front','BORE','5')
                token.dim_in_x = part_length - unit.millimeter(9.5)
                token.dim_in_y = dim_to_front + (part_width - right_depth.value())
                token.dim_in_z = macp.system_hole_bore_depth
                token.end_dim_in_x = part_length - sdtr
                token.end_dim_in_y = dim_to_front + (part_width - right_depth.value())
                token.face_bore_dia = macp.system_hole_dia
                token.distance_between_holes = unit.millimeter(32)
                token.associative_dia = 0
                token.associative_depth = 0
                
                obj, token = assembly.add_machine_token('System Holes Right Top Rear','BORE','5')
                token.dim_in_x = part_length - unit.millimeter(9.5)
                token.dim_in_y = part_width - dim_to_rear
                token.dim_in_z = macp.system_hole_bore_depth
                token.end_dim_in_x = part_length - sdtr
                token.end_dim_in_y = part_width - dim_to_rear
                token.face_bore_dia = macp.system_hole_dia
                token.distance_between_holes = unit.millimeter(32)
                token.associative_dia = 0
                token.associative_depth = 0
            
            if sdtl > 0 or sdtr > 0:
                
                if left_depth.value() != right_depth.value() and left_depth.value() > 0:
                    obj, token = assembly.add_machine_token('System Holes Left Top Front','BORE','6')
                    token.dim_in_x = part_length - unit.millimeter(9.5)
                    token.dim_in_y = dim_to_front + (part_width - left_depth.value())
                    token.dim_in_z = unit.millimeter(15)
                    token.end_dim_in_x = part_length - sdtl
                    token.end_dim_in_y = dim_to_front + (part_width - left_depth.value())
                    token.face_bore_dia = macp.system_hole_dia
                    token.distance_between_holes = unit.millimeter(32)
                    token.associative_dia = 0
                    token.associative_depth = 0
                    
                    obj, token = assembly.add_machine_token('System Holes Left Top Rear','BORE','6')
                    token.dim_in_x = part_length - unit.millimeter(9.5)
                    token.dim_in_y = part_width - dim_to_rear
                    token.dim_in_z = unit.millimeter(15)
                    token.end_dim_in_x = part_length - sdtl
                    token.end_dim_in_y = part_width - dim_to_rear
                    token.face_bore_dia = macp.system_hole_dia
                    token.distance_between_holes = unit.millimeter(32)
                    token.associative_dia = 0
                    token.associative_depth = 0
    
    def add_panel_routing(self,assembly):
        '''
            This adds the routing for panels for the hanging notch, base molding notch, top chamfers (rear and front)
            
            Required Panel Prompts
            
            Front_Angle_Height
            Front_Angle_Depth
            
            Rear_Angle_Height
            Rear_Angle_Depth
            
            First_Rear_Notch_Height
            First_Rear_Notch_Depth
            
            Second_Rear_Notch_Height
            Second_Rear_Notch_Depth
            
            Hanging_Notch_From_Top
            Hanging_Notch_Height
            Hanging_Notch_Depth
            
        '''
        macp = get_machining_props()
        product = self.get_product_from_part(assembly)
        self.remove_machining_token(assembly, 'First Rear Notch')
        self.remove_machining_token(assembly, 'Second Rear Notch')
        self.remove_machining_token(assembly, 'Front Chamfer')
        self.remove_machining_token(assembly, 'Rear Chamfer')
        
        if macp.include_routing_on_panels:
            
            loc_z = assembly.obj_bp.location.z
            panel_thickness = math.fabs(assembly.obj_z.location.z)
            First_Rear_Notch_Height = product.get_prompt('First Rear Notch Height')
            First_Rear_Notch_Depth = product.get_prompt('First Rear Notch Depth')
            Second_Rear_Notch_Height = product.get_prompt('Second Rear Notch Height')
            Second_Rear_Notch_Depth = product.get_prompt('Second Rear Notch Depth')
            
            if First_Rear_Notch_Height and First_Rear_Notch_Depth and Second_Rear_Notch_Height and Second_Rear_Notch_Depth:

                if First_Rear_Notch_Height.value() > 0 and loc_z < unit.inch(1):
                    obj, first_notch = assembly.add_machine_token('First Rear Notch' ,'CORNERNOTCH','5','3')
                    first_notch.dim_in_x = First_Rear_Notch_Height.value()
                    first_notch.dim_in_y = First_Rear_Notch_Depth.value()
                    first_notch.dim_in_z = panel_thickness
                    first_notch.lead_in = macp.router_lead
                    first_notch.tool_number = macp.tool_number
                
                if Second_Rear_Notch_Height.value() > 0 and loc_z < unit.inch(1):
                    obj, second_notch = assembly.add_machine_token('Second Rear Notch' ,'CORNERNOTCH','5','3')
                    second_notch.dim_in_x = Second_Rear_Notch_Height.value()
                    second_notch.dim_in_y = First_Rear_Notch_Depth.value() + Second_Rear_Notch_Depth.value()
                    second_notch.dim_in_z = panel_thickness
                    second_notch.lead_in = macp.router_lead
                    second_notch.tool_number = macp.tool_number
                    
            Front_Angle_Height = product.get_prompt('Front Angle Height')
            Front_Angle_Depth = product.get_prompt('Front Angle Depth')
            Rear_Angle_Height = product.get_prompt('Rear Angle Height')
            Rear_Angle_Depth = product.get_prompt('Rear Angle Depth')
            
            if Front_Angle_Depth and Front_Angle_Height and Rear_Angle_Height and Rear_Angle_Depth:
                
                if Front_Angle_Height.value() > 0:
                    obj, front_chamfer = assembly.add_machine_token('Front Chamfer' ,'CHAMFER','5','7')
                    front_chamfer.dim_in_x = Front_Angle_Height.value()
                    front_chamfer.dim_in_y = Front_Angle_Depth.value()
                    front_chamfer.dim_in_z = panel_thickness
                    front_chamfer.lead_in = macp.router_lead
                    front_chamfer.tool_number = macp.tool_number
                    
                if Rear_Angle_Height.value() > 0:
                    obj, rear_chamfer = assembly.add_machine_token('Rear Chamfer' ,'CHAMFER','5','5')
                    rear_chamfer.dim_in_x = Rear_Angle_Height.value()
                    rear_chamfer.dim_in_y = Rear_Angle_Depth.value()
                    rear_chamfer.dim_in_z = panel_thickness
                    rear_chamfer.lead_in = macp.router_lead
                    rear_chamfer.tool_number = macp.tool_number
    
    def add_shelf_and_rod_cleat_holes(self,assembly):
        macp = get_machining_props() 
        self.remove_machining_token(assembly, 'Shelf and Rod Holes')
        
        product_bp = utils.get_bp(assembly.obj_bp,'PRODUCT')
        if product_bp:
            product = fd_types.Assembly(product_bp)
            add_rod_holes = product.get_prompt("Add Rod")
            rod_placement = product.get_prompt("Hanging Rod Placement").value()
            rod_vertical_placement = product.get_prompt("Hanging Vertical Placement").value()

            if add_rod_holes and add_rod_holes.value():
                
                panel_length = math.fabs(assembly.obj_x.location.x)
                panel_width = math.fabs(assembly.obj_y.location.y)
                
                face = "6" if "Left" in assembly.obj_bp.mv.name_object else "5"
                
                obj, token = assembly.add_machine_token('Shelf and Rod Holes','BORE',face)
                token.dim_in_x = rod_placement
                token.dim_in_y = rod_vertical_placement - (unit.millimeter(32)/2)
                token.dim_in_z = unit.millimeter(15)
                token.face_bore_dia = macp.system_hole_dia
                token.end_dim_in_x = rod_placement
                token.end_dim_in_y = rod_vertical_placement + (unit.millimeter(32)/2)
                token.distance_between_holes = unit.millimeter(32)
                token.associative_dia = 0
                token.associative_depth = 0
    
    def add_shelf_and_rod_fe_machining(self,assembly):
        macp = get_machining_props()
        self.remove_machining_token(assembly, 'Shelf and Rod Holes')
        self.remove_machining_token(assembly, 'FE Chamfer')
        
        product_bp = utils.get_bp(assembly.obj_bp,'PRODUCT')
        if product_bp:
            product = fd_types.Assembly(product_bp)
            add_rod_holes = product.get_prompt("Add Rod")
            rod_placement = product.get_prompt("Hanging Rod Placement").value()
            rod_vertical_placement = product.get_prompt("Hanging Vertical Placement").value()
            left_depth = assembly.get_prompt("Left Depth").value()
            
            
            if add_rod_holes and add_rod_holes.value():
                
                panel_length = math.fabs(assembly.obj_x.location.x)
                panel_width = math.fabs(assembly.obj_y.location.y)
                panel_thickness = math.fabs(assembly.obj_z.location.z)
                
                face = "6" if "Left" in assembly.obj_bp.mv.name_object else "5"
                
                obj, token = assembly.add_machine_token('Shelf and Rod Holes','BORE',face)
                token.dim_in_x = rod_vertical_placement  - (unit.millimeter(32)/2)
                token.dim_in_y = panel_length - rod_placement
                token.dim_in_z = unit.millimeter(15)
                token.face_bore_dia = macp.system_hole_dia
                token.end_dim_in_x = rod_vertical_placement + (unit.millimeter(32)/2)
                token.end_dim_in_y = panel_length - rod_placement
                token.distance_between_holes = unit.millimeter(32)
                token.associative_dia = 0
                token.associative_depth = 0
                
                obj, front_chamfer = assembly.add_machine_token('FE Chamfer' ,'CHAMFER','5','7')
                front_chamfer.dim_in_x = panel_length - left_depth
                front_chamfer.dim_in_y = panel_width
                front_chamfer.dim_in_z = panel_thickness
                front_chamfer.lead_in = macp.router_lead
                front_chamfer.tool_number = macp.tool_number
    
    def add_panel_hanging_machining(self,assembly):
        macp = get_machining_props()        
        
        self.remove_machining_token(assembly, 'Hanging Notch')
        self.remove_machining_token(assembly, 'Hanging Hardware Drilling')
        
        if macp.include_routing_for_hanging_notch:
            panel_length = assembly.obj_x.location.x
            panel_thickness = math.fabs(assembly.obj_z.location.z)
            dim_from_top = macp.hanging_notch_dim_from_top_of_panel
            notch_length = macp.hanging_notch_length
            notch_depth = macp.hanging_notch_depth
            notch_routing_depth = macp.hanging_notch_routing_depth_on_end_panels
            is_right_end_panel = assembly.get_prompt("Is Right End Panel")
            is_left_end_panel = assembly.get_prompt("Is Left End Panel")

            if is_right_end_panel.value():
                face = '6'
            else:
                face = '5'
                
            obj, token = assembly.add_machine_token('Hanging Notch' ,'3SIDEDNOTCH',face,'2')
            token.dim_in_x = panel_length - dim_from_top
            token.end_dim_in_x = panel_length - dim_from_top - notch_length
            token.dim_in_y = notch_depth
            token.end_dim_in_y = notch_depth
            if is_right_end_panel.value() or is_left_end_panel.value():
                token.dim_in_z = notch_routing_depth
            else:
                token.dim_in_z = panel_thickness
            token.lead_in = macp.router_lead
            token.tool_number = macp.tool_number
            
        if macp.include_drilling_for_hanging_hardware:
            place_hanging_hardware_on_right = assembly.get_prompt("Place Hanging Hardware On Right")
            
            if place_hanging_hardware_on_right.value():
                face = '5'
            else:
                face = '6'

            dim_drilling_from_top = assembly.obj_x.location.x - macp.hanging_notch_dim_from_top_of_panel - macp.hanging_hardware_drilling_from_top_of_notch
                
            obj, token = assembly.add_machine_token('Hanging Hardware Drilling' ,'BORE',face)
            token.dim_in_x = dim_drilling_from_top
            token.end_dim_in_x  = dim_drilling_from_top
            token.dim_in_y = math.fabs(assembly.obj_y.location.y) - macp.hanging_hardware_first_drilling_hole_from_back_of_panel
            token.end_dim_in_y = math.fabs(assembly.obj_y.location.y) - macp.hanging_hardware_second_drilling_hole_from_back_of_panel
            token.dim_in_z = macp.hanging_hardware_drilling_depth
            token.face_bore_dia = macp.hanging_hardware_drilling_diameter
            token.distance_between_holes = macp.hanging_hardware_second_drilling_hole_from_back_of_panel - macp.hanging_hardware_first_drilling_hole_from_back_of_panel
    
    def add_drawer_wood_box_machining(self,assembly):
        macp = get_machining_props()
        
        self.remove_machining_token(assembly, 'Left Drilling')
        self.remove_machining_token(assembly, 'Right Drilling')        
        
        width = math.fabs(assembly.obj_y.location.y)
        
        if macp.wood_drawer_box_machining == 'DOWELS':

            obj, token = assembly.add_machine_token('Left Drilling' ,'CONST','3')
            token.dim_to_first_const_hole = unit.inch(1.25)
            token.dim_to_last_const_hole = width - unit.inch(1.25)
            token.edge_bore_depth = macp.dowel_bore_edge_depth
            token.edge_bore_dia = macp.dowel_bore_edge_dia
            token.face_bore_depth = macp.dowel_bore_face_depth
            token.face_bore_dia = macp.dowel_bore_face_dia
            token.distance_between_holes = macp.distance_between_holes_dowels

            obj, token = assembly.add_machine_token('Right Drilling' ,'CONST','4')
            token.dim_to_first_const_hole = unit.inch(1.25)
            token.dim_to_last_const_hole = width - unit.inch(1.25)
            token.edge_bore_depth = macp.dowel_bore_edge_depth
            token.edge_bore_dia = macp.dowel_bore_edge_dia
            token.face_bore_depth = macp.dowel_bore_face_depth
            token.face_bore_dia = macp.dowel_bore_face_dia
            token.distance_between_holes = macp.distance_between_holes_dowels
        
    def add_drawer_bottom_dado(self,assembly):
        macp = get_machining_props()
        
        self.remove_machining_token(assembly, 'Left Dado')
        self.remove_machining_token(assembly, 'Right Dado')
        self.remove_machining_token(assembly, 'Front Dado')
        self.remove_machining_token(assembly, 'Back Dado')
        
        if macp.route_dado_for_drawer_bottom:
            thickness = math.fabs(assembly.obj_z.location.z)
            
            tokens = []
            tokens.append(assembly.add_machine_token('Left Dado' ,'DADO','3'))
            tokens.append(assembly.add_machine_token('Right Dado' ,'DADO','4'))
            tokens.append(assembly.add_machine_token('Front Dado' ,'DADO','1'))
            tokens.append(assembly.add_machine_token('Back Dado' ,'DADO','2'))
            
            for token in tokens:
                token[1].lead_in = macp.router_lead
                token[1].lead_out = macp.router_lead
                token[1].beginning_depth = unit.inch(.25) + unit.inch(.01)
                token[1].double_pass = thickness + unit.inch(.1)
                token[1].panel_penetration = unit.inch(-.25)     
                token[1].tool_number = macp.tool_number
    
    def add_drawer_slide_machining_tokens(self,assembly):
        '''
            This adds associative SLIDE machine tokens to the left and right drawer sides
            The hole locations are determined based on the slide selection and the depth of the side
        '''
        pass
    
    def add_associative_hardware_for_hanging_rod_cups(self,assembly):
        '''
            This adds the associative hardware for the hanging rod cups currently we only have one hardware
            item in the material file called closet rod cup
        '''
        pass
    
    def add_slanted_shelf_machining(self,assembly):
        '''
            This adds the machining for slated shelf shelves
        '''
        macp = get_machining_props()
        self.remove_machining_token(assembly, 'Left Drilling')
        self.remove_machining_token(assembly, 'Right Drilling')
        self.remove_machining_token(assembly, 'Left Shelf Notch Routing')
        self.remove_machining_token(assembly, 'Right Shelf Notch Routing')   
             
        width = math.fabs(assembly.obj_y.location.y) 
        length = math.fabs(assembly.obj_x.location.x) 
        
        if macp.slanted_shoe_shelf_machining_type == 'ONLYDRILLREARCAMS':
            
            assembly.prompt('Shelf Pin Qty',value=2)
            assembly.prompt('Cam Qty',value=2)
            
            obj, token = assembly.add_machine_token('Left Drilling' ,'CAMLOCK','3')
            token.hole_locations[0] = width - macp.slanted_shoe_shelf_machining_distance_from_rear
            token.edge_bore_depth = macp.cam_bore_edge_depth
            token.edge_bore_dia = macp.cam_bore_edge_dia
            token.face_bore_depth = macp.cam_bore_face_depth
            token.face_bore_dia = macp.cam_bore_face_dia
            token.face_bore_depth_2 = macp.cam_depth
            token.face_bore_dia_2 = macp.cam_dia
            token.backset = macp.cam_backset
            token.cam_face = '5'
            
            obj, token = assembly.add_machine_token('Right Drilling' ,'CAMLOCK','4')
            token.hole_locations[0] = width - macp.slanted_shoe_shelf_machining_distance_from_rear
            token.edge_bore_depth = macp.cam_bore_edge_depth
            token.edge_bore_dia = macp.cam_bore_edge_dia
            token.face_bore_depth = macp.cam_bore_face_depth
            token.face_bore_dia = macp.cam_bore_face_dia
            token.face_bore_depth_2 = macp.cam_depth
            token.face_bore_dia_2 = macp.cam_dia
            token.backset = macp.cam_backset
            token.cam_face = '5'
            
        elif macp.slanted_shoe_shelf_machining_type == 'ROUTEREARNOTCH':
            
            assembly.prompt('Shelf Pin Qty',value=4)
            assembly.prompt('Cam Qty',value=0)            
            
            obj, token = assembly.add_machine_token('Right Shelf Notch Routing' ,'PLINE','5')
            token.tool_number = macp.tool_number
            token.tool_comp = "C"
            
            vector = token.vector_locations.add()
            vector.x_loc = length + macp.router_lead
            vector.y_loc = width - macp.slanted_shoe_shelf_machining_distance_from_rear
            vector.z_loc = 0
            
            vector = token.vector_locations.add()
            vector.x_loc = length + unit.inch(.01)
            vector.y_loc = width - macp.slanted_shoe_shelf_machining_distance_from_rear
            vector.z_loc = unit.inch(.125)
    
            vector = token.vector_locations.add()
            vector.x_loc = length - unit.inch(.5)
            vector.y_loc = width - macp.slanted_shoe_shelf_machining_distance_from_rear
            vector.z_loc = unit.inch(.125)           
            
            obj, token = assembly.add_machine_token('Left Shelf Notch Routing' ,'PLINE','5')
            token.tool_number = macp.tool_number
            token.tool_comp = "C"
            
            vector = token.vector_locations.add()
            vector.x_loc = -macp.router_lead
            vector.y_loc = width - macp.slanted_shoe_shelf_machining_distance_from_rear
            vector.z_loc = 0
            
            vector = token.vector_locations.add()
            vector.x_loc = -unit.inch(.01)
            vector.y_loc = width - macp.slanted_shoe_shelf_machining_distance_from_rear
            vector.z_loc = unit.inch(.125)            
    
            vector = token.vector_locations.add()
            vector.x_loc = unit.inch(.5)
            vector.y_loc = width - macp.slanted_shoe_shelf_machining_distance_from_rear
            vector.z_loc = unit.inch(.125)                     
    
    def add_lock_shelf_machining(self,assembly):
        '''
            This adds in the machining for locked shelves
            if use associative machining is turned on then either CAM or Dowel tokens will be added
            otherwise BORE tokens will be added.
            Is Locked Shelf
            Drill On Top
            Remove Left Holes
            Remove Right Holes
        '''
        macp = get_machining_props()
        self.remove_machining_token(assembly, 'Left Drilling')
        self.remove_machining_token(assembly, 'Right Drilling')
        
        is_lock_shelf = assembly.get_prompt("Is Locked Shelf")
        if is_lock_shelf and is_lock_shelf.value():        
        
            if macp.drill_cams_for_lock_shelves:
                width = math.fabs(assembly.obj_y.location.y)             
                drill_on_top = assembly.get_prompt("Drill On Top")
                remove_left_holes = assembly.get_prompt("Remove Left Holes")
                remove_right_holes = assembly.get_prompt("Remove Right Holes")                
                
                for i in range(0,4):
                    hardware = self.add_hardware("KD FITTING", assembly)
                    hardware.mv.comment_2 = "1015"
                
                if not remove_left_holes.value():
                    obj, token = assembly.add_machine_token('Left Drilling' ,'CAMLOCK','3')
                    token.hole_locations[0] = macp.dim_to_front_system_hole
                    token.hole_locations[1] = width - macp.dim_to_rear_system_hole
                    token.edge_bore_depth = macp.cam_bore_edge_depth
                    token.edge_bore_dia = macp.cam_bore_edge_dia
                    token.face_bore_depth = macp.cam_bore_face_depth
                    token.face_bore_dia = macp.cam_bore_face_dia
                    token.face_bore_depth_2 = macp.cam_depth
                    token.face_bore_dia_2 = macp.cam_dia
                    token.backset = macp.cam_backset
                    token.cam_face = '6' if drill_on_top.value() else '5'                    
                    
                if not remove_right_holes.value():
                    obj, token = assembly.add_machine_token('Right Drilling' ,'CAMLOCK','4')
                    token.hole_locations[0] = macp.dim_to_front_system_hole
                    token.hole_locations[1] = width - macp.dim_to_rear_system_hole
                    token.edge_bore_depth = macp.cam_bore_edge_depth
                    token.edge_bore_dia = macp.cam_bore_edge_dia
                    token.face_bore_depth = macp.cam_bore_face_depth
                    token.face_bore_dia = macp.cam_bore_face_dia
                    token.face_bore_depth_2 = macp.cam_depth
                    token.face_bore_dia_2 = macp.cam_dia
                    token.backset = macp.cam_backset
                    token.cam_face = '6' if drill_on_top.value() else '5'

    def add_toe_kick_machining(self,assembly):
        '''
            This adds in the machining for locked shelves
            if use associative machining is turned on then either CAM or Dowel tokens will be added
            otherwise BORE tokens will be added.
            Is Locked Shelf
            Drill On Top
            Remove Left Holes
            Remove Right Holes
        '''
        macp = get_machining_props()
        self.remove_machining_token(assembly, 'Left Drilling')
        self.remove_machining_token(assembly, 'Right Drilling')
        
        if macp.drill_cams_for_toe_kicks:
            
            width = math.fabs(assembly.obj_y.location.y)
            length = math.fabs(assembly.obj_x.location.x)

            obj, token = assembly.add_machine_token('Left Drilling' ,'CAMLOCK','3')
            token.hole_locations[0] = macp.dim_to_toe_kick_cam
            token.edge_bore_depth = macp.cam_bore_edge_depth
            token.edge_bore_dia = macp.cam_bore_edge_dia
            token.face_bore_depth = macp.cam_bore_face_depth
            token.face_bore_dia = macp.cam_bore_face_dia
            token.face_bore_depth_2 = macp.cam_depth
            token.face_bore_dia_2 = macp.cam_dia
            token.backset = macp.cam_backset
            token.cam_face = '5'

            obj, token = assembly.add_machine_token('Right Drilling' ,'CAMLOCK','4')
            token.hole_locations[0] = macp.dim_to_toe_kick_cam
            token.edge_bore_depth = macp.cam_bore_edge_depth
            token.edge_bore_dia = macp.cam_bore_edge_dia
            token.face_bore_depth = macp.cam_bore_face_depth
            token.face_bore_dia = macp.cam_bore_face_dia
            token.face_bore_depth_2 = macp.cam_depth
            token.face_bore_dia_2 = macp.cam_dia
            token.backset = macp.cam_backset
            token.cam_face = '5'
    
    def add_l_shelf_routing(self,assembly):
        '''
            This adds the routing for panels for the hanging notch, base molding notch, top chamfers (rear and front)
            
            Required Shelf Prompts
            
            Left Depth
            Right Depth
            
        '''
        macp = get_machining_props()
        self.remove_machining_token(assembly, 'L Shelf Notch')

        part_width = math.fabs(assembly.obj_y.location.y)
        part_length = math.fabs(assembly.obj_x.location.x)
        panel_thickness = math.fabs(assembly.obj_z.location.z)
        Left_Depth = assembly.get_prompt('Left Depth')
        Right_Depth = assembly.get_prompt('Right Depth')

        obj, second_notch = assembly.add_machine_token('L Shelf Notch' ,'CORNERNOTCH','5','7')
        second_notch.dim_in_x = part_length - Left_Depth.value()
        second_notch.dim_in_y = part_width - Right_Depth.value()
        second_notch.dim_in_z = panel_thickness
        second_notch.lead_in = macp.router_lead
        second_notch.tool_number = macp.tool_number
    
    def add_angle_shelf_chamfer(self,assembly):
        '''
            This adds the routing for panels for the hanging notch, base molding notch, top chamfers (rear and front)
            
            Required Shelf Prompts
            
            Left Depth
            Right Depth
            
        '''
        macp = get_machining_props()
        self.remove_machining_token(assembly, 'Shelf Chamfer')

        part_width = math.fabs(assembly.obj_y.location.y)
        part_length = math.fabs(assembly.obj_x.location.x)
        panel_thickness = math.fabs(assembly.obj_z.location.z)
        Left_Depth = assembly.get_prompt('Left Depth')
        Right_Depth = assembly.get_prompt('Right Depth')

        obj, second_notch = assembly.add_machine_token('Shelf Chamfer' ,'CHAMFER','5','7')
        second_notch.dim_in_x = part_length - Left_Depth.value()
        second_notch.dim_in_y = part_width - Right_Depth.value()
        second_notch.dim_in_z = panel_thickness
        second_notch.lead_in = macp.router_lead
        second_notch.tool_number = macp.tool_number
    
    def add_radius_shelf_routing(self,assembly):
        macp = get_machining_props()
        
        self.remove_machining_token(assembly, 'Radius Routing')
        
        obj, token = assembly.add_machine_token('Radius Routing' ,'PLINE','5')
        token.tool_number = macp.tool_number
        token.tool_comp = "R"
        
        width = math.fabs(assembly.obj_y.location.y) 
        length = math.fabs(assembly.obj_x.location.x)         
        panel_thickness = math.fabs(assembly.obj_z.location.z)
        
        vector = token.vector_locations.add()
        vector.x_loc = length + macp.router_lead
        vector.y_loc = width
        vector.z_loc = 0
        
        vector = token.vector_locations.add()
        vector.x_loc = length
        vector.y_loc = width
        vector.z_loc = panel_thickness   
        vector.bulge = .5
        
        vector = token.vector_locations.add()
        vector.x_loc = 0
        vector.y_loc = 0
        vector.z_loc = panel_thickness

        vector = token.vector_locations.add()
        vector.x_loc = macp.router_lead
        vector.y_loc = 0
        vector.z_loc = 0
    
    def add_slide_token(self,assembly):
        macp = get_machining_props()
        options = props_closet.get_scene_props().closet_options
        self.remove_machining_token(assembly, 'Slide Drilling')
        
        if macp.use_associative_hardware_for_slides:
        
            depth = assembly.obj_x.location.x
            
            if options.slide_name == 'Accuride Slides':
            
                obj, token = assembly.add_machine_token('Slide Drilling' ,'SLIDE','1')
                print(macp.drawer_slide_dim_from_bottom)
                token.dim_from_drawer_bottom = macp.drawer_slide_dim_from_bottom
                token.dim_to_first_hole = unit.inch(1.5817) if depth > unit.inch(1.5817) else 0
                token.dim_to_second_hole = unit.inch(6.6211) if depth > unit.inch(6.6211) else 0
                token.dim_to_third_hole = unit.inch(10.4006) if depth > unit.inch(10.4006) else 0
                token.dim_to_fourth_hole = unit.inch(15.44) if depth > unit.inch(15.44) else 0
                token.dim_to_fifth_hole = unit.inch(17.9596) if depth > unit.inch(17.9596) else 0
                token.face_bore_depth = macp.slide_face_bore_depth
                token.face_bore_dia = macp.slide_face_bore_dia
                token.drawer_slide_clearance = unit.inch(.5)
            
            elif options.slide_name == 'Blum Slides':
                
                obj, token = assembly.add_machine_token('Slide Drilling' ,'SLIDE','1')
                print(macp.drawer_slide_dim_from_bottom)                
                token.dim_from_drawer_bottom = macp.drawer_slide_dim_from_bottom
                token.dim_to_first_hole = unit.inch(1.5817) if depth > unit.inch(1.5817) else 0
                token.dim_to_second_hole = unit.inch(6.6211) if depth > unit.inch(6.6211) else 0
                token.dim_to_third_hole = unit.inch(10.4006) if depth > unit.inch(10.4006) else 0
                token.dim_to_fourth_hole = unit.inch(15.44) if depth > unit.inch(15.44) else 0
                token.dim_to_fifth_hole = unit.inch(17.9596) if depth > unit.inch(17.9596) else 0
                token.face_bore_depth = macp.slide_face_bore_depth
                token.face_bore_dia = macp.slide_face_bore_dia
                token.drawer_slide_clearance = unit.inch(.5)
                
            elif options.slide_name == 'Grass Slides':
                
                obj, token = assembly.add_machine_token('Slide Drilling' ,'SLIDE','1')
                print(macp.drawer_slide_dim_from_bottom)
                token.dim_from_drawer_bottom = macp.drawer_slide_dim_from_bottom
                token.dim_to_first_hole = unit.inch(1.5817) if depth > unit.inch(1.5817) else 0
                token.dim_to_second_hole = unit.inch(6.6211) if depth > unit.inch(6.6211) else 0
                token.dim_to_third_hole = unit.inch(10.4006) if depth > unit.inch(10.4006) else 0
                token.dim_to_fourth_hole = unit.inch(15.44) if depth > unit.inch(15.44) else 0
                token.dim_to_fifth_hole = unit.inch(17.9596) if depth > unit.inch(17.9596) else 0
                token.face_bore_depth = macp.slide_face_bore_depth
                token.face_bore_dia = macp.slide_face_bore_dia
                token.drawer_slide_clearance = unit.inch(.5)
    
    def update_drawer_machining(self,drawer_sides,drawer_backs,drawer_bottoms,drawer_fronts,drawer_boxes,drawer_stacks):
        macp = get_machining_props()
        defaults = props_closet.get_scene_props().closet_defaults
        options = props_closet.get_scene_props().closet_options
        box_type = options.box_type

        for drawer_stack in drawer_stacks:
            # change drawer top, bottom, and slide gap
            drawer_box_slide_gap = drawer_stack.get_prompt("Drawer Box Slide Gap")
            drawer_box_bottom_gap = drawer_stack.get_prompt("Drawer Box Bottom Gap")
            drawer_box_top_gap = drawer_stack.get_prompt("Drawer Box Top Gap")

            if box_type == 'MEL':
                
                drawer_box_slide_gap.set_value(unit.inch(1.05/2))
                drawer_box_top_gap.set_value(unit.inch(1.3782))            
                drawer_box_bottom_gap.set_value(unit.inch(0.8218))
                
            else: #DOVETAIL
                
                drawer_box_top_gap.set_value(unit.inch(0.6282))            
                drawer_box_bottom_gap.set_value(unit.inch(0.8218))                
                
                if "HBB" in options.dt_slide_name or "Mepla" in options.dt_slide_name:
                    drawer_box_slide_gap.set_value(unit.inch(.5))
                else:
                    drawer_box_slide_gap.set_value(unit.inch(.625/2))
                    
            
        for drawer_box in drawer_boxes:
            # change box prompts
            drawer_box_depth = drawer_box.obj_y.location.y
            drawer_box_height = drawer_box.obj_z.location.z
            use_dovetail_construction = drawer_box.get_prompt("Use Dovetail Construction")
            override_depth = drawer_box.get_prompt("Override Depth")            
            override_height = drawer_box.get_prompt("Override Height")  
            
            #OVERRIDE DRAWER BOX HEIGHT FOR SMALLER SIZES
            if drawer_box_height < unit.inch(1.5):
                override_height.set_value(unit.inch(1.62))
            elif drawer_box_height < unit.inch(2.75):
                override_height.set_value(unit.inch(2))
            else:
                override_height.set_value(0)
            
            if box_type == 'MEL':
                override_depth.set_value(0)
                use_dovetail_construction.set_value(False)
            else:  
                use_dovetail_construction.set_value(True)
                if "Undermount" in options.dt_slide_name:
                    if drawer_box_depth >= unit.inch(21):
                        override_depth.set_value(unit.inch(21))
                    elif drawer_box_depth >= unit.inch(18):
                        override_depth.set_value(unit.inch(18))
                    elif drawer_box_depth >= unit.inch(15):
                        override_depth.set_value(unit.inch(15))
                    elif drawer_box_depth >= unit.inch(12):
                        override_depth.set_value(unit.inch(12))
                    elif drawer_box_depth >= unit.inch(9):
                        override_depth.set_value(unit.inch(9))                        
                else:
                    override_depth.set_value(0)
                    
            if options.box_type == 'MEL':
                slide_name = options.mel_slide_name
            else:
                slide_name = options.dt_slide_name      
                      
                if slide_name == 'Mepla Partial Extension':
                    if drawer_box_depth >= unit.inch(22):
                        self.add_hardware("Mepla PE 22",drawer_box)
                    elif drawer_box_depth >= unit.inch(20):
                        self.add_hardware("Mepla PE 20",drawer_box)
                    elif drawer_box_depth >= unit.inch(18):
                        self.add_hardware("Mepla PE 18",drawer_box)
                    elif drawer_box_depth >= unit.inch(16):
                        self.add_hardware("Mepla PE 16",drawer_box)
                    elif drawer_box_depth >= unit.inch(14):
                        self.add_hardware("Mepla PE 14",drawer_box)
                    elif drawer_box_depth >= unit.inch(12):
                        self.add_hardware("Mepla PE 12",drawer_box) 
                    elif drawer_box_depth >= unit.inch(10):
                        self.add_hardware("Mepla PE 10",drawer_box)                         
                    else:
                        self.add_hardware("ERROR Drawer Too Small",drawer_box) 

                if slide_name == 'Mepla Full Extension':
                    if drawer_box_depth >= unit.inch(22):
                        self.add_hardware("Mepla FE 22",drawer_box)
                    elif drawer_box_depth >= unit.inch(20):
                        self.add_hardware("Mepla FE 20",drawer_box)
                    elif drawer_box_depth >= unit.inch(18):
                        self.add_hardware("Mepla FE 18",drawer_box)
                    elif drawer_box_depth >= unit.inch(16):
                        self.add_hardware("Mepla FE 16",drawer_box)
                    elif drawer_box_depth >= unit.inch(14):
                        self.add_hardware("Mepla FE 14",drawer_box)
                    elif drawer_box_depth >= unit.inch(12):
                        self.add_hardware("Mepla FE 12",drawer_box) 
                    elif drawer_box_depth >= unit.inch(10):
                        self.add_hardware("Mepla FE 10",drawer_box)                         
                    else:
                        self.add_hardware("ERROR Drawer Too Small",drawer_box) 
                        
                if slide_name == 'HBB':
                    if drawer_box_depth >= unit.inch(22):
                        self.add_hardware("HBB 22",drawer_box)
                    elif drawer_box_depth >= unit.inch(20):
                        self.add_hardware("HBB 20",drawer_box)
                    elif drawer_box_depth >= unit.inch(18):
                        self.add_hardware("HBB 18",drawer_box)
                    elif drawer_box_depth >= unit.inch(16):
                        self.add_hardware("HBB 16",drawer_box)
                    elif drawer_box_depth >= unit.inch(14):
                        self.add_hardware("HBB 14",drawer_box)
                    elif drawer_box_depth >= unit.inch(12):
                        self.add_hardware("HBB 12",drawer_box) 
                    elif drawer_box_depth >= unit.inch(10):
                        self.add_hardware("HBB 10",drawer_box)                         
                    else:
                        self.add_hardware("ERROR Drawer Too Small",drawer_box)                                            
                        
                if slide_name == 'Blum Undermount':
                    if drawer_box_depth >= unit.inch(21):
                        self.add_hardware("Blum 21",drawer_box)
                    elif drawer_box_depth >= unit.inch(18):
                        self.add_hardware("Blum 18",drawer_box)
                    elif drawer_box_depth >= unit.inch(15):
                        self.add_hardware("Blum 15",drawer_box)
                    elif drawer_box_depth >= unit.inch(12):
                        self.add_hardware("Blum 12",drawer_box) 
                    elif drawer_box_depth >= unit.inch(9):
                        self.add_hardware("Blum 9",drawer_box)                         
                    else:
                        self.add_hardware("ERROR Drawer Too Small",drawer_box) 
                        
                if slide_name == 'King Undermount':
                    if drawer_box_depth >= unit.inch(21):
                        self.add_hardware("King 21",drawer_box)
                    elif drawer_box_depth >= unit.inch(18):
                        self.add_hardware("King 18",drawer_box)
                    elif drawer_box_depth >= unit.inch(15):
                        self.add_hardware("King 15",drawer_box)
                    elif drawer_box_depth >= unit.inch(12):
                        self.add_hardware("King 12",drawer_box) 
                    elif drawer_box_depth >= unit.inch(9):
                        self.add_hardware("King 9",drawer_box)                         
                    else:
                        self.add_hardware("ERROR Drawer Too Small",drawer_box) 
                        
                if slide_name == 'Salice Undermount':
                    if drawer_box_depth >= unit.inch(21):
                        self.add_hardware("Salice 21",drawer_box)
                    elif drawer_box_depth >= unit.inch(18):
                        self.add_hardware("Salice 18",drawer_box)
                    elif drawer_box_depth >= unit.inch(15):
                        self.add_hardware("Salice 15",drawer_box)
                    elif drawer_box_depth >= unit.inch(12):
                        self.add_hardware("Salice 12",drawer_box) 
                    elif drawer_box_depth >= unit.inch(9):
                        self.add_hardware("Salice 9",drawer_box)                         
                    else:
                        self.add_hardware("ERROR Drawer Too Small",drawer_box)                                                 
                                             
                        
                                        
        for drawer_back in drawer_backs:

            pass
                
        for drawer_bottom in drawer_bottoms:
            # Add Routing and/or drilling for drawer systems
                        
            if box_type == 'MEL':
                drawer_bottom.cutpart('Drawer_Bottom')
                # self.set_manufacturing_material(drawer_bottom)
                
        for drawer_front in drawer_fronts:
            # Add Drilling for drawer systems
            pass
        
        for drawer_side in drawer_sides: # SET THIS LAST TO MAKE SURE SIZE IS CORRECT FOR HEIGHT OF DRAWER SYSTEM
            self.remove_machining_token(drawer_side, 'Slide Drilling')

            depth = math.fabs(drawer_side.obj_x.location.x)
            height = math.fabs(drawer_side.obj_y.location.y)     
            
            for child in drawer_side.obj_bp.children:
                
                if child.type == 'MESH':
                    child.cabinetlib.type_mesh = 'CUTPART'
                    child.mv.name_object = "Drawer Side"                    
                    # if options.box_type == 'MEL':
                    #     slide_name = options.mel_slide_name
                    # else:
                    #     slide_name = options.dt_slide_name

                    # slide_id = options.slide_name                    
                    # rows = snap_db.query_db(
                    #     "SELECT\
                    #         *\
                    #     FROM\
                    #         SlideTypes\
                    #     WHERE\
                    #         ItemTypeCode == '{}'\
                    #     ;".format(slide_id)
                    # )        

                    _, token = drawer_side.add_machine_token('Slide Drilling' ,'SLIDE','1')
                    token.drawer_slide_clearance = unit.inch(0.5)   
                    token.face_bore_depth = macp.slide_face_bore_depth
                    token.face_bore_dia = macp.slide_face_bore_dia                    

                    # for row in rows:
                    #     #obj, token = drawer_side.add_machine_token('Slide Drilling' ,'SLIDE','1')
                    #     token.dim_from_drawer_bottom = unit.inch(float(row[3]))
                    #     token.drawer_slide_clearance = unit.inch(0.5)   
                    #     token.face_bore_depth = macp.slide_face_bore_depth
                    #     token.face_bore_dia = macp.slide_face_bore_dia
                 
                    #     token.dim_to_first_hole = unit.inch(float(row[4]))
                    #     token.dim_to_second_hole = unit.inch(float(row[5]))
                    #     token.dim_to_third_hole = unit.inch(float(row[6]))
                    #     token.dim_to_fourth_hole = unit.inch(float(row[7]))
                    #     token.dim_to_fifth_hole = unit.inch(float(row[8]))
                    #
                    #rows.clear()                 

                    #Mepla Partial Extension                    
                    # if slide_name == 'Mepla Partial Extension':
                    #     obj, token = drawer_side.add_machine_token('Slide Drilling' ,'SLIDE','1')
                    #     token.dim_from_drawer_bottom = unit.inch(0.4378)  
                    #     token.drawer_slide_clearance = unit.inch(0.5)   
                    #     token.face_bore_depth = macp.slide_face_bore_depth
                    #     token.face_bore_dia = macp.slide_face_bore_dia
                 
                    #     token.dim_to_first_hole = unit.millimeter(37)    
                    #     if depth >= unit.inch(22):
                    #         token.dim_to_second_hole = unit.millimeter(517)
                    #     elif depth >= unit.inch(20):
                    #         token.dim_to_second_hole = unit.millimeter(485)
                    #     elif depth >= unit.inch(18):
                    #         token.dim_to_second_hole = unit.millimeter(389)
                    #     elif depth >= unit.inch(16):
                    #         token.dim_to_second_hole = unit.millimeter(357)
                    #     elif depth >= unit.inch(14):
                    #         token.dim_to_second_hole = unit.millimeter(325)
                    #     elif depth >= unit.inch(12):
                    #         token.dim_to_second_hole = unit.millimeter(261)  
                    #     else:
                    #         token.dim_to_second_hole = unit.millimeter(165)      

                    #Mepla Full Extension                    
                    # if slide_name == 'Mepla Full Extension':
                    #     obj, token = drawer_side.add_machine_token('Slide Drilling' ,'SLIDE','1')
                    #     token.dim_from_drawer_bottom = unit.inch(1.6977)  
                    #     token.drawer_slide_clearance = unit.inch(0.5)   
                    #     token.face_bore_depth = macp.slide_face_bore_depth
                    #     token.face_bore_dia = macp.slide_face_bore_dia
                 
                    #     token.dim_to_first_hole = unit.millimeter(37)    
                    #     if depth >= unit.inch(22):
                    #         token.dim_to_second_hole = unit.millimeter(517)
                    #     elif depth >= unit.inch(20):
                    #         token.dim_to_second_hole = unit.millimeter(485)
                    #     elif depth >= unit.inch(18):
                    #         token.dim_to_second_hole = unit.millimeter(389)
                    #     elif depth >= unit.inch(16):
                    #         token.dim_to_second_hole = unit.millimeter(357)
                    #     elif depth >= unit.inch(14):
                    #         token.dim_to_second_hole = unit.millimeter(325)
                    #     elif depth >= unit.inch(12):
                    #         token.dim_to_second_hole = unit.millimeter(261)  
                    #     else:
                    #         token.dim_to_second_hole = unit.millimeter(165)                             
                    
                    #HBB                    
                    # if slide_name == 'HBB':
                    #     obj, token = drawer_side.add_machine_token('Slide Drilling' ,'SLIDE','1')
                    #     token.dim_from_drawer_bottom = unit.inch(1.6977)  
                    #     token.drawer_slide_clearance = unit.inch(0.5)   
                    #     token.face_bore_depth = macp.slide_face_bore_depth
                    #     token.face_bore_dia = macp.slide_face_bore_dia
                 
                    #     token.dim_to_first_hole = unit.millimeter(37)    
                    #     if depth >= unit.inch(22):
                    #         token.dim_to_second_hole = unit.millimeter(485)
                    #     elif depth >= unit.inch(20):
                    #         token.dim_to_second_hole = unit.millimeter(485)
                    #     elif depth >= unit.inch(18):
                    #         token.dim_to_second_hole = unit.millimeter(389)
                    #     elif depth >= unit.inch(16):
                    #         token.dim_to_second_hole = unit.millimeter(357)
                    #     elif depth >= unit.inch(14):
                    #         token.dim_to_second_hole = unit.millimeter(261)
                    #     elif depth >= unit.inch(12):
                    #         token.dim_to_second_hole = unit.millimeter(261)  
                    #     else:
                    #         token.dim_to_second_hole = unit.millimeter(165)  
                    
                    #Salice Undermount                   
                    # if slide_name == 'Salice Undermount':
                    #     obj, token = drawer_side.add_machine_token('Slide Drilling' ,'SLIDE','1')
                    #     token.dim_from_drawer_bottom = unit.inch(0.4378)  
                    #     token.drawer_slide_clearance = unit.inch(0.625/2)   
                    #     token.face_bore_depth = macp.slide_face_bore_depth
                    #     token.face_bore_dia = macp.slide_face_bore_dia
                 
                    #     token.dim_to_first_hole = unit.millimeter(37)    
                    #     if depth >= unit.inch(21):
                    #         token.dim_to_second_hole = unit.millimeter(517)
                    #     elif depth >= unit.inch(18):
                    #         token.dim_to_second_hole = unit.millimeter(453)
                    #     elif depth >= unit.inch(15):
                    #         token.dim_to_second_hole = unit.millimeter(357)
                    #     elif depth >= unit.inch(12):
                    #         token.dim_to_second_hole = unit.millimeter(325)
                    #     else:
                    #         token.dim_to_second_hole = unit.millimeter(229)                               

                    #Blum Undermount                   
                    # if slide_name == 'Blum Undermount':
                    #     obj, token = drawer_side.add_machine_token('Slide Drilling' ,'SLIDE','1')
                    #     token.dim_from_drawer_bottom = unit.inch(0.4378)  
                    #     token.drawer_slide_clearance = unit.inch(0.625/2)   
                    #     token.face_bore_depth = macp.slide_face_bore_depth
                    #     token.face_bore_dia = macp.slide_face_bore_dia
                 
                    #     token.dim_to_first_hole = unit.millimeter(37)    
                    #     if depth >= unit.inch(21):
                    #         token.dim_to_second_hole = unit.millimeter(517)
                    #     elif depth >= unit.inch(18):
                    #         token.dim_to_second_hole = unit.millimeter(453)
                    #     elif depth >= unit.inch(15):
                    #         token.dim_to_second_hole = unit.millimeter(357)
                    #     elif depth >= unit.inch(12):
                    #         token.dim_to_second_hole = unit.millimeter(261)
                    #     else:
                    #         token.dim_to_second_hole = unit.millimeter(229)   

                    #King Undermount                   
                    # if slide_name == 'King Undermount':
                    #     obj, token = drawer_side.add_machine_token('Slide Drilling' ,'SLIDE','1')
                    #     token.dim_from_drawer_bottom = unit.inch(0.4378)  
                    #     token.drawer_slide_clearance = unit.inch(0.625/2)   
                    #     token.face_bore_depth = macp.slide_face_bore_depth
                    #     token.face_bore_dia = macp.slide_face_bore_dia
                 
                    #     token.dim_to_first_hole = unit.millimeter(37)    
                    #     if depth >= unit.inch(21):
                    #         token.dim_to_second_hole = unit.millimeter(517)
                    #     elif depth >= unit.inch(18):
                    #         token.dim_to_second_hole = unit.millimeter(453)
                    #     elif depth >= unit.inch(15):
                    #         token.dim_to_second_hole = unit.millimeter(357)
                    #     elif depth >= unit.inch(12):
                    #         token.dim_to_second_hole = unit.millimeter(278)
                    #     else:
                    #         token.dim_to_second_hole = unit.millimeter(229)  

    def set_manufacturing_material(self,assembly):
        """ Sets the cutpart_material_name property so the materials
            get exported as the correct names.
        """
        for child in assembly.obj_bp.children:
            if child.cabinetlib.type_mesh == 'CUTPART':
                cutpart_name = child.cabinetlib.cutpart_name
                edgepart_name = child.cabinetlib.edgepart_name
                
                edge_part_pointers = bpy.context.scene.mv.spec_groups[0].edgeparts
                cut_part_pointers = bpy.context.scene.mv.spec_groups[0].cutparts
                material_pointers = bpy.context.scene.mv.spec_groups[0].materials
                
                if cutpart_name in cut_part_pointers:
                    pointer = cut_part_pointers[cutpart_name]
                    material_name = material_pointers[pointer.core].item_name
                    
                    material_thickness = str(round(unit.meter_to_active_unit(pointer.thickness),4))
                    
                    child.mv.cutpart_material_name = material_thickness + " " + material_name
                    
                if edgepart_name in edge_part_pointers:
                    pointer = edge_part_pointers[edgepart_name]
                    material_name = material_pointers[pointer.material].item_name
                    
                    edgeband_thickness = str(round(unit.meter_to_active_unit(pointer.thickness),4))
                    
                    child.mv.edgeband_material_name = edgeband_thickness + " " + material_name    
    
    def set_section_number(self,assembly):
        """
            Set Section Number for Assembly
            This collects the products on a wall and loops through the
            products increasing the count of the number of openings found.
            Then assigns the number to comment 2 of the part
            
            This can only be set for parts that have a integer assigned for the mv.opening_name property
        """
        wall_bp = utils.get_wall_bp(assembly.obj_bp)
        product_bp = utils.get_bp(assembly.obj_bp,'PRODUCT')
        if wall_bp:
            products = self.get_wall_products(wall_bp)
            adjusted_opening_number = 0
            for product in products:
                if product == product_bp:
                    assembly.obj_bp.mv.comment_2 = str(int(round(float(product.mv.opening_name),0)) + adjusted_opening_number)
                    break
                else:
                    adjusted_opening_number += int(round(float(product.mv.opening_name),0))
    
    def get_wall_products(self,wall_bp):
        """
            Get Sorted List of Products on a Wall
        """
        products = []
        for child in wall_bp.children:
            props = props_closet.get_object_props(child)       
            if props.is_closet:
                child.mv.comment = wall_bp.mv.name_object
                products.append(child)
        products.sort(key=lambda obj: obj.location.x, reverse=False)
        return products

    def get_product_panels(self,product_bp,panel_list):
        """
            Get Sorted List of Panels in a product
        """
        for child in product_bp.children:
            props = props_closet.get_object_props(child)
            if props.is_panel_bp:
                assembly = fd_types.Assembly(child)
                if common_closet_utils.part_is_not_hidden(assembly):
                    panel_list.append(child)
            self.get_product_panels(child, panel_list)   
        panel_list.sort(key=lambda obj: obj.location.x, reverse=False)
        return panel_list

    def get_wall_panels(self,wall_bp):
        """
            Get Sorted List of Panels for a wall
            Returns List of Base Points
        """
        wall_panels = []
        products = self.get_wall_products(wall_bp)
        for product in products:
            product_panel_list = self.get_product_panels(product,[])
            for product_panel in product_panel_list:
                wall_panels.append(product_panel)
        return wall_panels

    def set_manufacturing_prompts(self,assembly):
        macp = get_machining_props()
        
        #Needed for the slide machine token
        drawer_box_slide_gap = assembly.get_prompt("Drawer Box Slide Gap")
        if drawer_box_slide_gap:
            drawer_box_slide_gap.set_value(macp.drawer_slide_gap)
            assembly.obj_bp.location = assembly.obj_bp.location
            
    def get_adj_panels(self,insert_bp):
        product_bp = utils.get_bp(insert_bp,'PRODUCT')
        panels = self.get_product_panels(product_bp,[])
        right_panel_bp = None
        left_panel_bp = None
        for i , panel in enumerate(panels):
            if insert_bp.location.x < panel.location.x:
                right_panel_bp = panel
                left_panel_bp = panels[i-1]
                break
            
        left_panel = fd_types.Assembly(left_panel_bp)
        right_panel = fd_types.Assembly(right_panel_bp)
        return left_panel, right_panel
            
    def update_panel_prompts_for_drawer_stack(self,drawer_stack):
        left_panel, right_panel = self.get_adj_panels(drawer_stack.obj_bp)
        
        drawer_stack_height = drawer_stack.get_prompt("Drawer Stack Height")
        stop_drilling_bottom_right = left_panel.get_prompt("Stop Drilling Bottom Right")
        stop_drilling_top_right = left_panel.get_prompt("Stop Drilling Top Right")
        stop_drilling_bottom_left = right_panel.get_prompt("Stop Drilling Bottom Left")
        stop_drilling_top_left = right_panel.get_prompt("Stop Drilling Top Left")
                    
        dist_from_top = drawer_stack.obj_z.location.z - drawer_stack_height.value()
                    
        stop_drilling_bottom_left.set_value(unit.inch(.01))
        stop_drilling_bottom_right.set_value(unit.inch(.01))
        stop_drilling_top_left.set_value(dist_from_top + unit.millimeter(32))
        stop_drilling_top_right.set_value(dist_from_top + unit.millimeter(32))
        
    def add_panel_drilling_for_middle_hanging_rods(self,hanging_rod):
        macp = get_machining_props()
        insert_bp = utils.get_bp(hanging_rod.obj_bp,'INSERT')
        if insert_bp:
            left_panel, right_panel = self.get_adj_panels(insert_bp)
            self.remove_machining_token(left_panel, 'System Holes Mid')
            self.remove_machining_token(right_panel, 'System Holes Mid')        
            props = get_machining_props()
                        
            set_back = hanging_rod.get_prompt("Hanging Rod Setback")
            
            if set_back and set_back.value() > props.dim_to_front_system_hole:
    
                obj, token = left_panel.add_machine_token('System Holes Mid','BORE','5')
                token.dim_in_x = unit.millimeter(9.5)
                token.dim_in_y = set_back.value()
                token.dim_in_z = props.system_hole_bore_depth
                token.face_bore_dia = macp.system_hole_dia
                token.end_dim_in_x = left_panel.obj_x.location.x - unit.millimeter(9.5)
                token.end_dim_in_y = set_back.value()
                token.distance_between_holes = unit.millimeter(32)
                token.associative_dia = 0
                token.associative_depth = 0
                
                obj, token = right_panel.add_machine_token('System Holes Mid','BORE','5')
                token.dim_in_x = unit.millimeter(9.5)
                token.dim_in_y = set_back.value()
                token.dim_in_z = props.system_hole_bore_depth
                token.face_bore_dia = macp.system_hole_dia
                token.end_dim_in_x = right_panel.obj_x.location.x - unit.millimeter(9.5)
                token.end_dim_in_y = set_back.value()
                token.distance_between_holes = unit.millimeter(32)
                token.associative_dia = 0
                token.associative_depth = 0
                        
    def execute(self, context):
        common_closet_utils.clear_temp_hardware()
        mac_props = get_machining_props()
        
        #COLLECT DRAWER PARTS TO UPDATE MACHINING AND PROMPTS
        #BASED ON DRAWER SELECTION
        drawer_sides = []
        drawer_boxes = []
        drawer_stacks = []
        drawer_fronts = []
        drawer_bottoms = []
        drawer_backs = []
        drawer_sub_fronts = []
        panels = []

            
        #SET PANEL NUMBER
        # for wall_bp in common_closet_utils.scene_walls(context):
        #     panels = self.get_wall_panels(wall_bp) #GET SORTED LIST OF PANELS
        #     for i , panel_bp in enumerate(panels):
        #         panel_bp.mv.opening_name = str(i + 1)
        #         panel_bp.mv.comment_2 = str(i + 1)
                
        for assembly in common_closet_utils.scene_parts(context):
            
            props = props_closet.get_object_props(assembly.obj_bp)
            
            # self.set_manufacturing_material(assembly)
            self.set_manufacturing_prompts(assembly)
            
            #PANELS
            if props.is_panel_bp:
                panels.append(assembly)
            else:
                pass
                # if assembly.obj_bp.mv.opening_name != "":
                #     self.set_section_number(assembly)

            if props.is_blind_corner_panel_bp:
                self.add_blind_corner_panel_drilling(assembly)
            
            #DOORS
            if props.is_door_bp:
                self.add_associative_hinges(assembly)
                self.add_door_pull_drilling(assembly)
                self.add_door_hinge_drilling(assembly)
                
            if props.is_hamper_front_bp:
                self.add_hamper_front_hinges(assembly)
                self.add_hamper_front_pull_drilling(assembly)
                self.add_hamper_door_hinge_drilling(assembly)
                
            if props.is_ironing_board_door_front_bp:
                self.add_hamper_front_hinges(assembly)
                self.add_hamper_front_pull_drilling(assembly)                
                
            if props.is_drawer_front_bp:
                drawer_fronts.append(assembly)
                self.add_drawer_front_pull_drilling(assembly)
                
            #CAM MACHINING
            if props.is_shelf_bp:
                self.add_lock_shelf_machining(assembly)
                
            if props.is_toe_kick_bp:
                self.add_toe_kick_machining(assembly)
            
            if props.is_slanted_shelf_bp:
                self.add_slanted_shelf_machining(assembly)            
            
            #CORNER MACHINING
            if props.is_l_shelf_bp:
                self.add_l_shelf_routing(assembly)            

            if props.is_angle_shelf_bp:
                self.add_angle_shelf_chamfer(assembly)
            
            if props.is_radius_shelf_bp:
                self.add_radius_shelf_routing(assembly)
            
            #DRAWERS
            if props.is_drawer_box_bp:
                drawer_boxes.append(assembly)
            
            if props.is_drawer_stack_bp:
                drawer_stacks.append(assembly)
                self.update_panel_prompts_for_drawer_stack(assembly)
                            
            if props.is_drawer_side_bp:
                drawer_sides.append(assembly)
                # self.add_slide_token(assembly)
                    
            if props.is_drawer_sub_front_bp:
                drawer_sub_fronts.append(assembly)
                # self.add_drawer_wood_box_machining(assembly)
                    
            if props.is_drawer_bottom_bp:
                drawer_bottoms.append(assembly)
                # self.add_drawer_bottom_dado(assembly)
                
            if props.is_drawer_back_bp:
                drawer_backs.append(assembly)                
                
            #FIXED SHELF AND ROD PRODUCT
            if props.is_shelf_and_rod_cleat_bp:
                self.add_shelf_and_rod_cleat_holes(assembly)
            if props.is_shelf_and_rod_fe_cleat_bp:
                self.add_shelf_and_rod_fe_machining(assembly)
            
            if props.is_hanging_rod:
                self.add_panel_drilling_for_middle_hanging_rods(assembly)
                
        for panel in panels:
            self.add_panel_drilling(panel)
            self.add_panel_routing(panel)        
            self.add_panel_hanging_machining(panel)             

        #SEND IN ALL DRAWER PARTS FOUND TO ADD INFORMATION FOR DRAWER SYSTEMS
        self.update_drawer_machining(drawer_sides, drawer_backs, drawer_bottoms, drawer_fronts, drawer_boxes, drawer_stacks)
        
        #UPDATE ALL MATERIAL THICKNESSES
        bpy.ops.cabinetlib.update_scene_from_pointers()
        
        return {'FINISHED'}


class PROPS_Machining_Defaults(bpy.types.PropertyGroup):
    
    machining_tabs = EnumProperty(name="Machining Tabs",
                                  items=[('MAIN',"Main",'Main Settings'),
                                         ('HARDWARE',"Hardware",'Hardware Machining Settings')])            
    
    #MAIN SETTINGS
    auto_machine_on_save = BoolProperty(name="Auto Apply Machining On Save",
                                        default=True,
                                        description="Automatically apply machining on save")    
    
    panel_drilling_type = EnumProperty(name="Panel Drilling Type",
                                       items=[('NONE',"None",'No Drilling (This is used if you want to use associative drilling)'),
                                              ('32MM',"32mm System",'Drill all Panels in 32mm increments')],default='32MM')      
    
    drill_cams_for_lock_shelves = BoolProperty(name="Route Cams for Lock Shelves",
                                                description="Check this box to drill cams for lock shelves",
                                                default=False)
    
    drill_cams_for_toe_kicks = BoolProperty(name="Route Cams for Toe Kicks",
                                            description="Check this box to drill cams for toe kicks",
                                            default=False)    
    
    lock_shelf_machining_type = EnumProperty(name="Lock Shelf Machining Type",
                                       items=[('NONE',"None",'No Drilling'),
                                              ('ASSOCIATIVECAMS',"Associative Cams",'This will drill Cam holes in the shelf and the associative panel drilling'),
                                              ('ONLYDRILLCAMHOLES',"Only Drill Cam Holes",'Only Drill Cam Holes')])  
    
    adj_shelf_machining_type = EnumProperty(name="Adjustable Shelf Machining Type",
                                            items=[('NONE',"None",'No Drilling'),
                                                   ('DRILLINDIVIUAL',"Drill Holes for Each Shelf",'Drill Holes for Each Shelf'),
                                                   ('DRILLALL',"Drill Holes for Entire Opening",'This will drill holes for the entire opening')])      
    
    toe_kick_machining_type = EnumProperty(name="Toe Kick Machining Type",
                                           items=[('NONE',"None",'No Drilling'),
                                                  ('ASSOCIATIVECAMS',"Associative Cams",'This will drill Cam holes in the toe kick and the associative panel drilling'),
                                                  ('ONLYDRILLCAMHOLES',"Only Drill Cam Holes",'This only drills the holes for the cams')])
    
    slanted_shoe_shelf_machining_type = EnumProperty(name="Slanted Shoe Shelf Machining Type",
                                                     items=[('NONE',"None",'No Drilling'),
                                                            ('ONLYDRILLREARCAMS',"Only Drill Rear Cams",'This will only drill rear cams in the shelf'),
                                                            ('ROUTEREARNOTCH',"Route Rear Notch",'This will route a notch in the back of the panel for the shelf pin to sit in.')])      
    
    slanted_shoe_shelf_machining_distance_from_rear = FloatProperty(name="Dim To Rear System Hole",
                                                                    description="Enter the distance from the back of the slanted shoe shelf to add the machining.",
                                                                    default=unit.inch(1.5),unit='LENGTH')
    
    wood_drawer_box_machining = EnumProperty(name="Wood Drawer Box Machining",
                                             items=[('NONE',"None",'No Drilling'),
                                                    ('DOWELS',"Dowels",'This will include holes for dowels to connect the front and back to sides')])      
    
    route_dado_for_drawer_bottom = BoolProperty(name="Route Dado for Drawer Bottom",
                                                description="Check this box to route the drawer sub front, back, and sides for the bottom dado",
                                                default=False)
    
    include_routes_for_interlocking_cubbies = BoolProperty(name="Include Routes for Interlocking Cubbies",
                                                description="Check this box to include routes for interlocking cubbies",
                                                default=True)
    
    include_routing_on_panels = BoolProperty(name="Include Routing Operations on Panels",
                                             description="Check this box to include routing operations on panels",
                                             default=True)
    
    dim_between_holes = FloatProperty(
        name="Dim Between System Holes",
        description="Enter the distance between system holes.",
        default=unit.millimeter(32),
        unit='LENGTH'
        )

    dim_to_front_system_hole = FloatProperty(
        name="Dim To First System Hole",
        description="Enter the distance from the front of the part to center of the front system hole.",
        default=unit.millimeter(37),
        unit='LENGTH'
        )
    
    dim_to_rear_system_hole = FloatProperty(
        name="Dim To Rear System Hole",
        description="Enter the distance from the back of the part to center of the rear system hole.",
        default=unit.millimeter(37),
        unit='LENGTH'
        )

    dim_to_system_top_hole = FloatProperty(
        name="Dim To First System Hole",
        description="Enter the distance from the top of the part to center of the top system hole.",
        default=unit.millimeter(9.5),
        unit='LENGTH'
        )

    dim_to_system_bottom_hole = FloatProperty(
        name="Dim To First System Hole",
        description="Enter the distance from the bottom of the part to center of the bottom system hole.",
        default=unit.millimeter(9.5),
        unit='LENGTH'
        ) 
    
    dim_to_toe_kick_cam = FloatProperty(name="Dim To Toe Kick Cam",
                                            description="Enter the distance top of the toe kick to place the cam hole.",
                                            default=unit.inch(1.25),unit='LENGTH')    
    
    #HANGING NOTCH SETTING
    
    include_routing_for_hanging_notch = BoolProperty(name="Include Routing for Hanging Notch",
                                             description="Check this box to include routing for hanging notch",
                                             default=False)    
    
    include_drilling_for_hanging_hardware = BoolProperty(name="Include Drilling for Hanging Hardware",
                                             description="Check this box to include drilling for the hanging hardware",
                                             default=False)      
    
    hanging_notch_dim_from_top_of_panel = FloatProperty(name="Hanging Notch Dim From Top of Panel",
                                            description="Enter the distance from the top of the panel to the start of the hanging notch.",
                                            default=unit.inch(6),unit='LENGTH')    
    
    hanging_notch_length = FloatProperty(name="Hanging Notch Length",
                                            description="Enter the length of the hanging notch",
                                            default=unit.inch(2.125),unit='LENGTH')
    
    hanging_notch_depth = FloatProperty(name="Hanging Notch Depth",
                                            description="Enter the depth of the hanging notch",
                                            default=unit.inch(.5),unit='LENGTH')    
    
    hanging_notch_routing_depth_on_end_panels = FloatProperty(name="Hanging Notch Routing Depth on End Panels",
                                            description="Enter the routing depth on end panels",
                                            default=unit.inch(.5625),unit='LENGTH')       
    
    hanging_hardware_drilling_from_top_of_notch = FloatProperty(name="Hanging Hardware Drilling from Top of Notch",
                                            description="Enter the location to add the drilling from the top of the hanging notch",
                                            default=unit.inch(1),unit='LENGTH')
    
    hanging_hardware_first_drilling_hole_from_back_of_panel = FloatProperty(name="Hanging Hardware First Drilling Hole from Back of Panel",
                                            description="Enter the location to add the first hole drilling from the from the back of the panel",
                                            default=unit.inch(1.25),unit='LENGTH')         
    
    hanging_hardware_second_drilling_hole_from_back_of_panel = FloatProperty(name="Hanging Hardware Second Drilling Hole from Back of Panel",
                                            description="Enter the location to add the second hole drilling from the from the back of the panel",
                                            default=unit.inch(2.5),unit='LENGTH')      
    
    hanging_hardware_drilling_diameter = FloatProperty(name="Hanging Hardware Drilling Diameter",
                                            description="Enter hanging hardware drilling diameter (ENTER VALUE IN MILLIMETERS)",
                                            default=5)
    
    hanging_hardware_drilling_depth = FloatProperty(name="Hanging Hardware Drilling Depth",
                                            description="Enter hanging hardware drilling depth",
                                            default=unit.inch(.5),unit='LENGTH')    
    
    #CAM HOLE SETTINGS
    cam_bore_face_depth = FloatProperty(name="Cam Bore Face Depth",
                                        description="Enter the face drilling depth for cams. This is the depth to drill on the associated panel.",
                                        default=unit.inch(.5),unit='LENGTH')    
    
    cam_bore_edge_depth = FloatProperty(name="Cam Bore Edge Depth",
                                        description="Enter the edge drilling depth for cams.",
                                        default=unit.inch(.5),unit='LENGTH')        
    
    cam_dia = FloatProperty(name="Cam Dia",
                            description="Enter the face drilling dia for the cam. This is the drilling on the shelf for the cam. ENTER VALUE IN MILLIMETERS",
                            default=20)      
    
    cam_depth = FloatProperty(name="Cam Depth",
                              description="Enter the face drilling depth for the cam. This is the drilling on the shelf for the cam.",
                              default=unit.inch(.625),unit='LENGTH')          
    
    cam_backset = FloatProperty(name="Cam Backset",
                              description="Enter the distance from the edge of the shelf to the center of the cam placement",
                              default=unit.inch(.5),unit='LENGTH')       
    
    cam_bore_face_dia = FloatProperty(name="Cam Bore Face Dia",
                                      description="Enter the face drilling dia for cam holes. This is the drilling on the associated panel. ENTER VALUE IN MILLIMETERS",
                                      default=5)
    
    cam_bore_edge_dia = FloatProperty(name="Cam Bore Edge Dia",
                                      description="Enter the edge drilling dia for dowel holes. ENTER VALUE IN MILLIMETERS",
                                      default=5)
    
    #SYSTEM HOLE SETTINGS
    system_hole_bore_depth = FloatProperty(name="System Hole Bore Depth",
                                           description="Enter the drilling depth for the system holes",
                                           default=unit.inch(.5),
                                           unit='LENGTH')
    
    system_hole_dia = FloatProperty(name="System Hole Dia",
        description="Enter the drilling dia for the system holes.",
        default=unit.inch(0.197),
        unit='LENGTH',
        precision=3
        )  
    
    #DOWEL SETTINGS
    dowel_bore_face_depth = FloatProperty(name="Dowel Bore Face Depth",
                                          default=unit.inch(.5),unit='LENGTH')    
    
    dowel_bore_edge_depth = FloatProperty(name="Dowel Bore Edge Depth",
                                          default=unit.inch(.5),unit='LENGTH')        
    
    dowel_bore_face_dia = FloatProperty(name="Dowel Bore Face Dia",
                                        description="Enter the face drilling dia for dowel holes. ENTER VALUE IN MILLIMETERS",
                                        default=5)     
    
    dowel_bore_edge_dia = FloatProperty(name="Dowel Bore Edge Dia",
                                        description="Enter the edge drilling dia for dowel holes. ENTER VALUE IN MILLIMETERS",
                                        default=5)       
    
    distance_between_holes_dowels = FloatProperty(name="Distance Between Holes Dowels",
                                                  description="Enter the distance between holes for cams. Or Enter 0 to use only two cams",
                                                  default=unit.inch(.5))        
    
    #ROUTING SETTINGS
    tool_number = StringProperty(name="Tool Number",
                                 description="Enter the tool number that you want to use for routing operations. This should match a tool number assigned in your primary toolfile.",
                                 default="101")

    router_lead = FloatProperty(name="Router Lead",default=unit.inch(.25),unit='LENGTH')

    #ASSOCIATIVE HARDWARE
    use_associative_hardware_for_hinges = BoolProperty(name="Use Associative Hardware for Hinges",
                                                       description="Check this box to add associative hardware for hinges",
                                                       default=True)
    
    use_associative_hardware_for_hinge_plates = BoolProperty(name="Use Associative Hardware for Hinge Plates",
                                                       description="Check this box to add associative hardware for hinge plates",
                                                       default=True)    
    
    use_associative_hardware_for_locks = BoolProperty(name="Use Associative Hardware for Locks",
                                                       description="Check this box to add associative hardware for locks",
                                                       default=True)           

    use_associative_hardware_for_closet_rod_cups = BoolProperty(name="Use Associative Hardware for Closet Rod Cups",
                                                       description="Check this box to add associative hardware for closet rod cups",
                                                       default=True)   

    use_associative_hardware_for_slides = BoolProperty(name="Use Associative Hardware for Slides",
                                                       description="Check this box to add associative hardware for drawer slides",
                                                       default=True)   

    hinge_cup_off_door_edge = FloatProperty(name="Hinge Cup Off Door Edge",default=unit.inch(.9252),unit='LENGTH')
     
    hinge_plate_inset_from_door = FloatProperty(name="Hinge Plate Inset From Door",default=unit.inch(1.4567),unit='LENGTH')

    hinge_location_from_top_and_bottom = FloatProperty(name="Hinge Location From Top and Bottom",default=unit.inch(3),unit='LENGTH')
    
    #PULLS
    add_machining_for_pulls = BoolProperty(name="Add Machining For Pulls",
                                           description="Check this box to add machining for pulls",
                                           default=True)     

    pull_from_edge = FloatProperty(name="Pull From Edge",
                               description="Enter the horizontal distance from the edge of the door",
                               default=unit.inch(2),unit='LENGTH')
    
    pull_location_on_base_upper_doors = FloatProperty(name="Pull Location for Base and Upper Doors",
                                                      description="Enter the vertical distance from the edge of the door",
                                                      default=unit.inch(2),unit='LENGTH')
    
    pull_location_on_tall_doors = FloatProperty(name="Pull Location on Tall Doors",
                                                description="Enter the distance from the bottom of the door to the center of the pull on tall doors",
                                                default=unit.inch(40),unit='LENGTH')
    
    door_pull_length = FloatProperty(name="Door Pull Length",
                                     description="Enter in the distance between holes for drilling for pulls on doors. (Enter 0 for Knobs)",
                                     default=unit.inch(3),unit='LENGTH')
    
    drawer_pull_length = FloatProperty(name="Drawer Pull Length",
                                       description="Enter in the distance between holes for drilling for pulls on drawer fronts. (Enter 0 for Knobs)",
                                       default=unit.inch(3),unit='LENGTH')
    
    pull_bore_dia = FloatProperty(name="Pull Bore Dia",
                                  description="Enter the face drilling dia for pull hardware holes. ENTER VALUE IN MILLIMETERS",
                                  default=5)    
    
    #SLIDE SETTINGS
    slide_face_bore_depth = FloatProperty(name="Slide Face Bore Depth",default=unit.inch(.5511),unit='LENGTH')
     
    slide_face_bore_dia = FloatProperty(name="Slide Face Bore Dia",
                                        description="Enter the face drilling dia for drawer slide holes. ENTER VALUE IN MILLIMETERS",
                                        default=5)
     
    drawer_slide_dim_from_bottom = FloatProperty(name="Drawer Slide Dim From Bottom",default=unit.inch(.5),unit='LENGTH')
    
    drawer_slide_gap = FloatProperty(name="Drawer Slide Gap",default=unit.inch(.5),unit='LENGTH')
    
    def draw(self,layout):
        main_box = layout.box()

        row = main_box.row()
        row.scale_y = 1.3
        row.operator(MACHINING_PROPERTY_NAMESPACE + ".prepare_closet_for_export",icon='FILE_TICK')
        row.prop(self,'auto_machine_on_save',text="Auto Apply on Save")
        
        main_col = main_box.column(align=True)
        
        row = main_col.row(align=True)
        row.scale_y = 1.1
        row.prop_enum(self, "machining_tabs", 'MAIN', icon='PREFERENCES', text="Machining")
        #row.prop_enum(self, "machining_tabs", 'HARDWARE', icon='PREFERENCES', text="Hardware") 
        # row.prop_enum(self, "machining_tabs", '2D', icon='PREFERENCES', text="2D") 
        
        if self.machining_tabs == 'MAIN':
            box = main_col.box()
            col = box.column()
            col.label("System Hole Drilling:")
            col.prop(self,'panel_drilling_type',text="Panel")

            if self.panel_drilling_type != 'NONE':
                row = col.row(align=True)
                row.label("Hole Locations:")
                row.prop(self,'dim_to_front_system_hole',text="Dim from Front")
                row.prop(self,'dim_to_rear_system_hole',text="Dim from Rear")
                row = col.row(align=True)
                row.label("Drilling Info:")
                row.prop(self,'system_hole_bore_depth',text="Drill Depth")
                row.prop(self,'system_hole_dia',text="Drill Diameter")

            box = main_col.box()
            box.template_list(
                "LIST_Mac_Scenes", 
                " ",
                bpy.data, 
                "scenes", 
                bpy.context.window_manager.mv, 
                "elevation_scene_index"
            )           
 
            # box = main_col.box()
            # box.label("Cam Drilling:")
            # box.prop(self,'drill_cams_for_lock_shelves',text="Lock Shelf")
            # box.prop(self,'drill_cams_for_toe_kicks',text="Toe Kick")
            
            # if self.drill_cams_for_toe_kicks:
            #     row = box.row(align=True)
            #     row.label("Toe Kick Cam Location:") 
            #     row.prop(self,'dim_to_toe_kick_cam',text="From Top")               

            # if self.drill_cams_for_lock_shelves or self.drill_cams_for_toe_kicks:
            #     row = box.row(align=True)
            #     row.label("Cam Distance from Shelf Edge:")
            #     row.prop(self,'cam_backset',text="From Edge") 
            #     row = box.row(align=True)
            #     row.label("Cam Diameter:")
            #     row.prop(self,'cam_dia',text='Dia')                
            #     row = box.row(align=True)
            #     row.label("Diameter")
            #     row.prop(self,'cam_bore_face_dia',text="Face")
            #     row.prop(self,'cam_bore_edge_dia',text="Edge")
            #     row = box.row(align=True)
            #     row.label("Depth")
            #     row.prop(self,'cam_bore_face_depth',text="Face")
            #     row.prop(self,'cam_bore_edge_depth',text="Edge")
            
            # box = main_col.box()
            # col = box.column()
            # col.label("Drawer Box Machining:")        
            # row = col.row()
            # row.prop(self,'wood_drawer_box_machining',text="Drawer Box")
            # row = col.row()
            # row.prop(self,'route_dado_for_drawer_bottom')
            
            # box = main_col.box()
            # col = box.column()
            # col.label("Slanted Shoe Shelf Machining:")
            # col.prop(self,'slanted_shoe_shelf_machining_type',text="Slanted Shelf")            
            # if self.slanted_shoe_shelf_machining_type != 'NONE':
            #     row = col.row()
            #     row.label("Machining Distance From Rear")
            #     row.prop(self,'slanted_shoe_shelf_machining_distance_from_rear',text="")
            # box = main_col.box()
            # col = box.column()
            # col.label("Routing:")
            
            # row = box.row()
            # row.prop(self,'tool_number')
            # row = box.row()
            # row.label("Router Lead")
            # row.prop(self,'router_lead',text="")
            
        if self.machining_tabs == 'HARDWARE':
            hardware_box = main_col.box()
            col = hardware_box.column()
            col.label("Hanging Notch Machining:")  
            col.prop(self,'include_routing_for_hanging_notch')  
            
            if self.include_routing_for_hanging_notch:
                row = col.row()
                row.label("Notch Location")
                row.prop(self,'hanging_notch_dim_from_top_of_panel',text="Dim From Top of Panel")
                row = col.row(align=True)
                row.label("Notch Size")
                row.prop(self,'hanging_notch_length',text="Length")
                row.prop(self,'hanging_notch_depth',text="Width")
                row = col.row()
                row.label("Route Depth")
                row.prop(self,'hanging_notch_routing_depth_on_end_panels',text="Only for End Panels")
                          
            col.prop(self,'include_drilling_for_hanging_hardware')  
                          
            if self.include_drilling_for_hanging_hardware:
                row = col.row()
                row.label("Drilling Location From Top")
                row.prop(self,'hanging_hardware_drilling_from_top_of_notch',text="Dim From Top of Notch")
                row = col.row()
                row.label("Drilling Location From Rear")
                row.prop(self,'hanging_hardware_first_drilling_hole_from_back_of_panel',text="First Hole")  
                row = col.row()
                row.label(" ")
                row.prop(self,'hanging_hardware_second_drilling_hole_from_back_of_panel',text="Second Hole")                
                row = col.row(align=True)
                row.label("Drilling")
                row.prop(self,'hanging_hardware_drilling_diameter',text="Dia")
                row.prop(self,'hanging_hardware_drilling_depth',text="Depth")
                
            hardware_box = main_col.box()
            col = hardware_box.column()
            col.label("Drawer Slides:")
            col.prop(self,'use_associative_hardware_for_slides',text="Add Associative Drilling for Drawer Slides")    
            if self.use_associative_hardware_for_slides:
                row = col.row()
                row.label("Drawer Slide Gap:")
                row.prop(self,'drawer_slide_gap',text="")
                row = col.row()
                row.label("Dim from Bottom of Drawer:")
                row.prop(self,'drawer_slide_dim_from_bottom',text="")
                row = col.row(align=True)
                row.label("Drilling:")
                row.prop(self,'slide_face_bore_depth',text="Depth")
                row.prop(self,'slide_face_bore_dia',text="Dia")
            #Use Closet Defaults, Enter in Name, Use Lookup
            
            hardware_box = main_col.box()
            col = hardware_box.column()
            col.label("Add Associative Hinge Hardware:")
            row = col.row()
            row.prop(self,'use_associative_hardware_for_hinges',text="Hinges")
            row.prop(self,'use_associative_hardware_for_hinge_plates',text="Hinge Plates")
            if self.use_associative_hardware_for_hinges:
                row = col.row()
                row.label("Hinge Cup Off Door Edge:")
                row.prop(self,'hinge_cup_off_door_edge',text="")
            if self.use_associative_hardware_for_hinge_plates:
                row = col.row()
                row.label("Hinge Plate Inset from Door:")
                row.prop(self,'hinge_plate_inset_from_door',text="")
            if self.use_associative_hardware_for_hinge_plates or self.use_associative_hardware_for_hinges:
                row = col.row()
                row.label("Hinge Location:")
                row.prop(self,'hinge_location_from_top_and_bottom',text="From Top and Bottom")     
                
            #Use Closet Defaults, Enter in Name, Use Lookup
            hardware_box = main_col.box()
            col = hardware_box.column()
            col.label("Add Drilling For Pulls:")
            col.prop(self,'add_machining_for_pulls',text="Pulls")
            if self.add_machining_for_pulls:
                row = col.row()
                row.label("Door Pull Length:")
                row.prop(self,'door_pull_length',text="")
                row = col.row()
                row.label("Drawer Pull Length:")                
                row.prop(self,'drawer_pull_length',text="")
            #Use Closet Defaults, Enter in Name, Use Lookup
            #Add Non associative drilling, hole dia, pull length drilling
            
            # hardware_box = main_col.box()
            # hardware_box.label("Locks:")            
            # hardware_box.prop(self,'use_associative_hardware_for_locks',text="Locks")

            #Use Closet Defaults, Enter in Name, Use Lookup
            #Add Non associative drilling, hole dia, pull length drilling
            
            # hardware_box = main_col.box()
            # hardware_box.label("Closet Rod Cups:")
            # hardware_box.prop(self,'use_associative_hardware_for_closet_rod_cups',text="Closet Rod Cups")

            #Use Closet Defaults, Enter in Name, Use Lookup
            #Add Non associative drilling, hole dia, pull length drilling
        
        #if self.machining_tabs == 'MATERIALS':
            #Cutpart Part Naming: (AUTO) Thickness then material name,  Use Lookup
            #Solid Stock Naming; (AUTO) Name then Color , Use Lookup
            #Buyout Naming; (AUTO) Name, Use Lookup
        
        # if self.machining_tabs == '2D':
        #     plan_box = main_col.box()
        #     plan_box.label("Plan View:")
        #     plan_box.prop(self,'use_associative_hardware_for_slides',text="Add Panel Names")
        #     plan_box.prop(self,'use_associative_hardware_for_slides',text="Add Section Widths")
        #     plan_box.prop(self,'use_associative_hardware_for_slides',text="Add Section Names")
        #     plan_box = main_col.box()
        #     plan_box.label("Elevation View:")
        #     plan_box.prop(self,'use_associative_hardware_for_slides',text="Add Section Widths")
        #     plan_box.prop(self,'use_associative_hardware_for_slides',text="Add Section Heights")
        #     plan_box.prop(self,'use_associative_hardware_for_slides',text="Add Doors Front Heights")        
        #     plan_box.prop(self,'use_associative_hardware_for_slides',text="Add Drawer Front Heights")   
        #     plan_box.prop(self,'use_associative_hardware_for_slides',text="Add Hanging Rod Locations")  
        #     plan_box.prop(self,'use_associative_hardware_for_slides',text="Add Hamper Annotations") 
        #     plan_box.prop(self,'use_associative_hardware_for_slides',text="Add Ironing Board Annotations") 
        #     plan_box.prop(self,'use_associative_hardware_for_slides',text="Add Wall Heights") 


class PANEL_Closet_Machining_Setup(bpy.types.Panel):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + "Closet_Machining_Setup"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "Closet Machining Setup"
    bl_category = "SNaP"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        debug_mode = context.user_preferences.addons["snap_db"].preferences.debug_mode
        
        if snap_db.DEV_TOOLS_AVAILABLE and debug_mode:
            return True
        else:
            return False
    
    def draw_header(self, context):
        layout = self.layout
        layout.label('',icon='BLANK1')    

    def draw(self, context):
        props = get_machining_props()
        props.draw(self.layout)


# REGISTER CLASSES
bpy.utils.register_class(PROPS_Machining_Defaults)
bpy.utils.register_class(OPERATOR_Prepare_Closet_For_Export)
bpy.utils.register_class(PANEL_Closet_Machining_Setup)
bpy.utils.register_class(LIST_Mac_Scenes)
exec("bpy.types.Scene." + MACHINING_PROPERTY_NAMESPACE + "= PointerProperty(type = PROPS_Machining_Defaults)")


# AUTO CALL OPERATOR ON SAVE
@bpy.app.handlers.persistent
def assign_machining(scene=None):
    if not bpy.app.background:
        props = get_machining_props()
        if props.auto_machine_on_save:
            exec("bpy.ops." + MACHINING_PROPERTY_NAMESPACE + ".prepare_closet_for_export()")
            
bpy.app.handlers.save_pre.append(assign_machining)