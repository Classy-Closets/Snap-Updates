import bpy

from snap import sn_types, sn_utils


CLOSET_LIB_NAME_SPACE = "sn_closets"


def part_is_not_hidden(part):
    ''' Returns bool
        Determines if part assembly is hidden
    '''
    hide = part.get_prompt("Hide")
    if hide:
        if hide.get_value():
            return False
        else:
            return True
    else:
        return True


def scene_parts(context):
    ''' Generator that Returns a List of all of the assemblies in the Scene
    '''
    for obj in bpy.context.scene.objects:
        if 'IS_BP_ASSEMBLY' in obj:
            part = sn_types.Part(obj)
            if part_is_not_hidden(part):
                yield part


def clear_temp_hardware():
    ''' Removes all temp objects that have been added to the scene
    '''
    temp_objects = []
    for obj in bpy.data.objects:
        obj_props = obj.sn_closets
        if obj_props.is_temp_hardware:
            temp_objects.append(obj)
    sn_utils.delete_obj_list(temp_objects)


def set_room_prop(name, value):
    properties = bpy.context.scene.sn_closets.project_properties
    if name in properties:
        prop = properties[name]
        prop.value = str(value)
    else:
        prop = properties.add()
        prop.name = name
        prop.value = str(value)
