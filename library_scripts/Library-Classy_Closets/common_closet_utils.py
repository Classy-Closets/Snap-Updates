import bpy
from . import mv_closet_defaults as props_closet
from mv import fd_types, utils

def part_is_not_hidden(part):
    ''' Returns bool
        Determines if part assembly is hidden
    '''    
    hide = part.get_prompt("Hide")
    if hide:
        if hide.value():
            return False
        else:
            return True
    else:
        return True

def clear_temp_objects():
    ''' Removes all temp objects that have been added to the scene
    '''
    temp_objects = []
    for obj in bpy.data.objects:
        obj_props = props_closet.get_object_props(obj)
        if obj_props.is_temp_obj:
            temp_objects.append(obj)
    utils.delete_obj_list(temp_objects)

def clear_temp_hardware():
    ''' Removes all temp objects that have been added to the scene
    '''
    temp_objects = []
    for obj in bpy.data.objects:
        obj_props = props_closet.get_object_props(obj)
        if obj_props.is_temp_hardware :
            temp_objects.append(obj)
    utils.delete_obj_list(temp_objects)    
  
def scene_walls(context):
    ''' Generator that Returns a List of all of the wall base point objects
    '''
    for obj in context.scene.objects:
        if obj.mv.type == 'BPWALL':
            yield obj

def closet_products(context):
    ''' Generator that Returns a List of all of the Closet Products in the Scene
    '''
    for obj in context.scene.objects:
        obj_props = props_closet.get_object_props(obj)
        if obj_props.is_closet:
            yield fd_types.Assembly(obj)            
            
def scene_assemblies(context):
    ''' Generator that Returns a List of all of the assemblies in the Scene
    '''    
    for obj in bpy.context.scene.objects:
        if obj.mv.type == 'BPASSEMBLY':
            assembly = fd_types.Assembly(obj)
            if part_is_not_hidden(assembly):
                yield assembly            
            
def scene_parts(context):
    ''' Generator that Returns a List of all of the assemblies in the Scene
    '''    
    for obj in bpy.context.scene.objects:
        if obj.mv.type == 'BPASSEMBLY':
            part = fd_types.Part(obj)
            if part_is_not_hidden(part):
                yield part
            
def remove_machining_tokens(assembly):
    ''' Removes all of the machining tokens assigned to an assembly
    '''  
    for child in assembly.obj_bp.children:
        child.mv.mp.machine_tokens.clear()
            
def set_room_prop(name,value):
    ''' Sets a location level property to export to MV ERP
    '''
    properties = bpy.context.scene.mv.project_properties
    if name in properties:
        prop = properties[name]
        prop.value = str(value)
    else:
        prop = properties.add()
        prop.name = name
        prop.value = str(value)
        