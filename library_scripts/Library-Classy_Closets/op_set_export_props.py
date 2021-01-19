import bpy
from snap_db.fd_2dviews import opengl_dim
from mv import fd_types, unit, utils
from . import mv_closet_defaults as props_closet

def part_is_not_hidden(part):
    hide = part.get_prompt("Hide")
    if hide:
        if hide.value():
            return False
        else:
            return True
    else:
        return True

def scene_assemblies(context):
    for obj in bpy.context.scene.objects:
        if obj.mv.type == 'BPASSEMBLY':
            assembly = fd_types.Assembly(obj)
            yield assembly

def get_wall_name(assembly):
    wall_bp = utils.get_wall_bp(assembly.obj_bp)
    if wall_bp:
        return wall_bp.mv.name_object
    else:
        return "NONE"

def get_walls():
    walls = []
    for obj in bpy.data.objects:
        wall_bp = utils.get_wall_bp(obj)
        if wall_bp and wall_bp not in walls:
            walls.append(wall_bp)
    walls.sort(key=lambda wall: wall.mv.name_object, reverse=False)
    return walls

def get_wall_products(bp):
    products = []
    for child in bp.children:
        props = props_closet.get_object_props(child)
        if props.is_closet:
            products.append(child)
    products.sort(key=lambda obj: obj.location.x, reverse=False)
    return products

def get_product_part(obj_bp):
    if obj_bp.mv.type == 'BPASSEMBLY':
        assembly = fd_types.Assembly(obj_bp)
        if part_is_not_hidden(assembly):
            return assembly

def get_product_parts(bp,part_list):
    part = get_product_part(bp)
    if part and part not in part_list:
        part_list.append(part)  
    for child in bp.children:
        get_product_parts(child,part_list)
    return part_list

def get_product_panels(product_list,index):
    last_opening = 0
    for i, product in enumerate(product_list):
        if i < index:
            assembly = fd_types.Assembly(product)
            last_opening_prompt = assembly.get_prompt("Last Opening")
            last_opening += last_opening_prompt.value() + 1
    return last_opening

def get_product_openings(product_list,index):
    last_opening = 0
    for i, product in enumerate(product_list):
        if i < index:
            assembly = fd_types.Assembly(product)
            last_opening_prompt = assembly.get_prompt("Last Opening")
            last_opening += last_opening_prompt.value()
    return last_opening

def set_part_section_numbers():
    walls = get_walls()
    for wall in walls:
        products = get_wall_products(wall)
        if products:
            products.sort(key=lambda product: product.location.x, reverse=False)
            for i, product in enumerate(products):
                product.mv.comment = wall.mv.name_object
                parts = get_product_parts(product,[])
                for part in parts:
                    if part.obj_bp.mv.opening_name != "":
                        opening_number = int(part.obj_bp.mv.opening_name)
                        props = props_closet.get_object_props(part.obj_bp)
                        if props.is_panel_bp:
                            part.obj_bp.mv.comment = str(opening_number + get_product_panels(products,i))
                        else:
                            part.obj_bp.mv.comment = str(opening_number + get_product_openings(products,i))

def set_manufacturing_material(obj):
    """ Sets the cutpart_material_name property so the materials
        get exported as the correct names.
    """
    cutpart_name = obj.cabinetlib.cutpart_name
    edgepart_name = obj.cabinetlib.edgepart_name
    
    edge_part_pointers = bpy.context.scene.mv.spec_groups[0].edgeparts
    cut_part_pointers = bpy.context.scene.mv.spec_groups[0].cutparts
    material_pointers = bpy.context.scene.mv.spec_groups[0].materials
    
    if cutpart_name in cut_part_pointers:
        pointer = cut_part_pointers[cutpart_name]
        material_name = material_pointers[pointer.core].item_name
        
        material_thickness = str(unit.meter_to_active_unit(pointer.thickness))
        
        obj.mv.cutpart_material_name = material_thickness + " " + material_name
        
    if edgepart_name in edge_part_pointers:
        pointer = edge_part_pointers[edgepart_name]
        material_name = material_pointers[pointer.material].item_name
        
        edgeband_thickness = str(unit.meter_to_active_unit(pointer.thickness))
        
        obj.mv.edgeband_material_name = edgeband_thickness + " " + material_name
        
def set_part_comment_2(part,description):
    part.obj_bp.mv.comment_2 = description
    for child in part.obj_bp.children:
        if child.cabinetlib.type_mesh == 'CUTPART':
            set_manufacturing_material(child)
            
class OPERATOR_Set_Export_Props(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".set_export_props"
    bl_label = "Set Export Props"
    bl_description = "This will assign the comments and material names"
    bl_options = {'UNDO'}
    
    def execute(self, context):
        set_part_section_numbers()
        
        for assembly in scene_assemblies(context):
            
            props = props_closet.get_object_props(assembly.obj_bp)
            
            if props.is_panel_bp:
                set_part_comment_2(assembly,"PANEL")
    
            if props.is_shelf_bp:
                set_part_comment_2(assembly,"SHELF")    
    
            if props.is_cleat_bp:
                set_part_comment_2(assembly,"CLEAT")        
    
            if props.is_toe_kick_bp:
                set_part_comment_2(assembly,"TOE KICK")         
    
            if props.is_shelf_lip_bp:
                set_part_comment_2(assembly,"SHELF LIP")           
                
            if props.is_deco_shelf_lip_bp:
                set_part_comment_2(assembly,"DECO SHELF LIP")       
                
            if props.is_divider_bp:
                set_part_comment_2(assembly,"DIVIDER")
                
            if props.is_back_bp:
                set_part_comment_2(assembly,"SHELF LIP")    
    
            if props.is_filler_bp:
                set_part_comment_2(assembly,"FILLER")          
    
            if props.is_fluted_filler_bp:
                set_part_comment_2(assembly,"FLUTED FILLER")  
    
            if props.is_drawer_side_bp:
                set_part_comment_2(assembly,"DRAWER SIDE")           
    
            if props.is_drawer_back_bp:
                set_part_comment_2(assembly,"DRAWER BACK")         
    
            if props.is_drawer_sub_front_bp:
                set_part_comment_2(assembly,"DRAWER SUB FRONT")       
    
            if props.is_drawer_bottom_bp:
                set_part_comment_2(assembly,"DRAWER BOTTOM")     
    
            if props.is_door_bp:
                set_part_comment_2(assembly,"DOOR")         
    
            if props.is_drawer_front_bp:
                set_part_comment_2(assembly,"DRAWER FRONT")          
    
            if props.is_hamper_front_bp:
                set_part_comment_2(assembly,"HAMPER FRONT")
                
        return {'FINISHED'}

bpy.utils.register_class(OPERATOR_Set_Export_Props)