'''
This scripts converts door .blend files from version 1.2.x into the new version 2.x
using the new assembly class and markers for objects.

Please execute this script in the Blender console (e.g, from Text Editor)

or from WindowOS console:
    blender.exe --background --python ..\\scripts\\addons\\snap\\libraries\\closets\\assets\\door_converter.py
'''
import bpy
import os


def convert_to_new_door(context, path, door_path, door_name):
    # Please: configure the local path to the new SNaP-addon directory with Door Panels 
    target_path =\
        "C:/work/tmp/scripts/addons/snap/libraries/closets/assets/Door Panels/"
    save_path = os.path.join(target_path, door_path)
    if os.path.exists(save_path):
        return
    delete_objs(context)
    delete_orphan_data()
    with bpy.data.libraries.load(path, False, False) as (data_from, data_to):
        for collection in data_from.collections:
            data_to.collections = [collection]
            break
    for collection in data_to.collections:
        for obj in collection.objects:
            if "MESH" in obj.name:
                door_mesh = obj
            if "VPDIMX" in obj.name:
                obj_x = obj
            if "VPDIMY" in obj.name:
                obj_y = obj
            if "Y1" in obj.name:
                obj_y1 = obj
            if "Y2" in obj.name:
                obj_y2 = obj
    door = bpy.data.objects.new(door_name.split(".")[0], None)
    door["IS_BP_ASSEMBLY"] = True
    door["ID_PROMPT"] = 'sn_closets.door_prompts'
    door["PROMPT_ID"] = 'sn_assembly.show_properties'
    scene_collection = bpy.context.scene.collection
    scene = scene_collection.children['Collection']
    door_mesh.parent = door
    scene.objects.link(door_mesh)
    door_dim_z = door_mesh.dimensions.z

    obj_x.parent = door
    obj_x.name = "OBJ_X"
    obj_x["obj_x"] = True
    obj_x.empty_display_type = 'SPHERE'
    obj_x.empty_display_size = .1
    for i in range(3):
        obj_x.lock_location[i] = True
        obj_x.lock_rotation[i] = True
    obj_x.lock_location[0] = False
    scene.objects.link(obj_x)

    obj_y.parent = door
    obj_y.name = "OBJ_Y"
    obj_y["obj_y"] = True
    obj_y.empty_display_type = 'SPHERE'
    obj_y.empty_display_size = .1
    for i in range(3):
        obj_y.lock_location[i] = True
        obj_y.lock_rotation[i] = True
    obj_y.lock_location[1] = False
    scene.objects.link(obj_y)

    obj_y1.parent = door
    obj_y1.name = "Y1"
    obj_y1.empty_display_type = 'SPHERE'
    obj_y1.empty_display_size = .1
    for i in range(3):
        obj_y1.lock_location[i] = True
        obj_y1.lock_rotation[i] = True
    obj_y1.lock_location[1] = False
    scene.objects.link(obj_y1)

    obj_y2.parent = door
    obj_y2.name = "Y2"
    obj_y2.empty_display_type = 'SPHERE'
    obj_y2.empty_display_size = .1
    for i in range(3):
        obj_y2.lock_location[i] = True
        obj_y2.lock_rotation[i] = True
    obj_y2.lock_location[1] = False
    scene.objects.link(obj_y2)

    obj_z = bpy.data.objects.new("OBJ_Z", None)
    obj_z.parent = door
    obj_z.location = (0, 0, door_dim_z)
    obj_z["obj_z"] = True
    obj_z.empty_display_type = 'SINGLE_ARROW'
    obj_z.empty_display_size = .1
    for i in range(3):
        obj_z.lock_location[i] = True
        obj_z.lock_rotation[i] = True
    obj_z.lock_location[2] = False
    scene.objects.link(obj_z)

    obj_prompts = bpy.data.objects.new("OBJ_PROMPTS", None)
    obj_prompts.location = (0, 0, 0)
    obj_prompts.parent = door
    obj_prompts.empty_display_size = 0
    for i in range(3):
        obj_prompts.lock_location[i] = True
        obj_prompts.lock_rotation[i] = True
    obj_prompts["obj_prompts"] = True
    scene.objects.link(obj_prompts)

    door_mesh.vertex_groups.clear()

    vertex_x = []
    vertex_y1 = []
    vertex_y2 = []
    for mod in door_mesh.modifiers:
        if "VPDIMX" in mod.name:
            mod.object = obj_x
            mod.name = obj_x.name
            ver_index = mod.vertex_indices
            for item in ver_index:
                vertex_x.append(item)
        if "Y1" in mod.name:
            mod.object = obj_y1
            mod.name = obj_y1.name
            ver_index = mod.vertex_indices
            for item in ver_index:
                vertex_y1.append(item)
        if "Y2" in mod.name:
            mod.object = obj_y2
            mod.name = obj_y2.name
            ver_index = mod.vertex_indices
            for item in ver_index:
                vertex_y2.append(item)

    door_mesh.vertex_groups.new(name=obj_x.name)
    vgroup = door_mesh.vertex_groups[obj_x.name]
    vgroup.add(vertex_x, 1, 'ADD')

    door_mesh.vertex_groups.new(name=obj_y1.name)
    vgroup = door_mesh.vertex_groups[obj_y1.name]
    vgroup.add(vertex_y1, 1, 'ADD')

    door_mesh.vertex_groups.new(name=obj_y2.name)
    vgroup = door_mesh.vertex_groups[obj_y2.name]
    vgroup.add(vertex_y1, 1, 'ADD')

    scene.objects.link(door)

    bpy.ops.wm.save_as_mainfile(
        filepath=save_path,
        filter_blender=True,
        filter_backup=True,
        filter_python=True,
        compress=True)


def delete_orphan_data():
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)

    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

    for block in bpy.data.textures:
        if block.users == 0:
            bpy.data.textures.remove(block)

    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)


def delete_objs(context):
    scene = context.scene
    for obj in scene.objects:
        obj.select_set(True)
        mesh = obj.data
        if mesh:
            mesh.users
            mesh.user_clear()
            bpy.data.meshes.remove(mesh)
        try:
            objs = bpy.data.objects
            objs.remove(objs[obj.name], do_unlink=True)
        except Exception as e:
            print(e)
        bpy.ops.sn_object.delete(use_global=True)
        del obj
    if len(scene.objects) > 0:
        delete_objs(context)


if __name__ == "__main__":
    # Please: configure the local path to the old SNaP-addon directory with Door Panels 
    old_folder_path = "C:/work/repos/SNaP-Dev/SNaP/data/libraries/Library-Classy_Closets/Door Panels/" # Wood Doors/Bergamo Door.blend"
    for folder in os.listdir(old_folder_path):
        folder_path = os.path.join(old_folder_path, folder)
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            door_path = os.path.join(folder, file)
            convert_to_new_door(bpy.context, file_path, door_path, file)
