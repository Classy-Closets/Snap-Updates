'''
Utility Functions
'''

import bpy
import os
from mv import utils
import snap_db

def update_file_browser_space(context,path):
    """ This function refreshes the file browser space
        with the path that is passed in
    """
    for area in context.screen.areas:
        if area.type == 'FILE_BROWSER':
            for space in area.spaces:
                if space.type == 'FILE_BROWSER':
                    params = space.params
                    params.directory = path
                    if not context.screen.show_fullscreen:
                        params.use_filter = True
                        params.display_type = 'THUMBNAIL'
                        params.use_filter_movie = False
                        params.use_filter_script = False
                        params.use_filter_sound = False
                        params.use_filter_text = False
                        params.use_filter_font = False
                        params.use_filter_folder = False
                        params.use_filter_blender = False
                        params.use_filter_image = True


def get_material(folders,material_name):
    if material_name in bpy.data.materials:
        return bpy.data.materials[material_name]
    
    #Make sure no folders are blank
    for folder in folders:
        if folder == "":
            return None
    
    search_dirs = []

    #Main materials folder 'data/materials'
    main_mats_dir = utils.get_library_dir("materials")

    for folder in folders:
        main_mats_dir = os.path.join(main_mats_dir,folder)

    search_dirs.append(main_mats_dir)

    #Materials folder in 'snap_db'
    search_dirs.append(snap_db.MATERIALS_DIR)

    material = None

    for search_directory in search_dirs:
        if os.path.isdir(search_directory):
            files = os.listdir(search_directory)
            possible_files = []
            # Add the blend file with the same name to the list first so it is searched first
            if material_name + ".blend" in files:
                possible_files.append(os.path.join(search_directory,material_name + ".blend"))
            
            for file in files:
                blendname, ext = os.path.splitext(file)
                if ext == ".blend":
                    possible_files.append(os.path.join(search_directory,file))
                    
            for file in possible_files:
                with bpy.data.libraries.load(file, False, False) as (data_from, data_to):
                    for mat in data_from.materials:
                        if mat == material_name:
                            data_to.materials = [mat]
                            break
        
                for mat in data_to.materials:
                    material = mat
    
    return material


def assign_materials_from_pointers(obj):
    library = bpy.context.scene.mv
    spec_group = library.spec_groups[obj.cabinetlib.spec_group_index]

    #ASSIGN POINTERS TO MESH BASED ON MESH TYPE
    if obj.cabinetlib.type_mesh == 'CUTPART':

        if obj.cabinetlib.cutpart_name == 'Back':
            back_bp = obj.parent
            bp_props = back_bp.lm_closets

            if bp_props.use_unique_material:
                if bp_props.unique_mat_types == 'MELAMINE':
                    unique_mat_name = bp_props.unique_mat_mel
                if bp_props.unique_mat_types == 'TEXTURED_MELAMINE':
                    unique_mat_name = bp_props.unique_mat_tex_mel
                if bp_props.unique_mat_types == 'VENEER':
                    unique_mat_name = bp_props.unique_mat_veneer
                
                for slot in obj.cabinetlib.material_slots:
                    slot.library_name = "Cabinet Materials"
                    slot.category_name = "Classy Closets"
                    slot.item_name = unique_mat_name
        
        if spec_group:
            if obj.cabinetlib.cutpart_name in spec_group.cutparts:
                cutpart = spec_group.cutparts[obj.cabinetlib.cutpart_name]
                for index, slot in enumerate(obj.cabinetlib.material_slots):
                    if slot.name == 'Core':
                        slot.pointer_name = cutpart.core
                    elif slot.name in {'Top','Exterior'}:
                        slot.pointer_name = cutpart.top
                    elif slot.name in {'Bottom','Interior'}:
                        slot.pointer_name = cutpart.bottom
                    else:
                        if not obj.mv.use_multiple_edgeband_pointers:
                            if obj.cabinetlib.edgepart_name in spec_group.edgeparts:
                                edgepart = spec_group.edgeparts[obj.cabinetlib.edgepart_name]
                                slot.pointer_name = edgepart.material
                        else:
                            pass
                            #print('SLOT NAME',slot.pointer_name)

                    if slot.pointer_name in spec_group.materials:
                        material_pointer = spec_group.materials[slot.pointer_name]
                        slot.library_name = material_pointer.library_name
                        slot.category_name = material_pointer.category_name
                        slot.item_name = material_pointer.item_name

    elif obj.cabinetlib.type_mesh == 'EDGEBANDING':
        obj.show_bounds = False
        if spec_group:
            if obj.cabinetlib.edgepart_name in spec_group.edgeparts:
                edgepart = spec_group.edgeparts[obj.cabinetlib.edgepart_name]
                for index, slot in enumerate(obj.cabinetlib.material_slots):
                    slot.pointer_name = edgepart.material

                    if slot.pointer_name in spec_group.materials:
                        material_pointer = spec_group.materials[slot.pointer_name]
                        slot.library_name = material_pointer.library_name
                        slot.category_name = material_pointer.category_name
                        slot.item_name = material_pointer.item_name

    elif obj.cabinetlib.type_mesh == 'MACHINING':
        # MAKE A SIMPLE BLACK MATERIAL FOR MACHINING
        for slot in obj.cabinetlib.material_slots:
            slot.library_name = "Plastics"
            slot.category_name = "Melamine"
            slot.item_name = "Gloss Black Plastic"
            
    else:
        if spec_group:
            for index, slot in enumerate(obj.cabinetlib.material_slots):
                if slot.pointer_name in spec_group.materials:
                    material_pointer = spec_group.materials[slot.pointer_name]
                    slot.library_name = material_pointer.library_name
                    slot.category_name = material_pointer.category_name
                    slot.item_name = material_pointer.item_name

    #RETRIEVE MATERIAL FROM CATEGORY NAME AND ITEM NAME AND ASSIGN TO SLOT
    for index, slot in enumerate(obj.cabinetlib.material_slots):
        material = get_material((slot.library_name,slot.category_name),slot.item_name)
        if material:
            obj.material_slots[index].material = material
        else:
            print("MATERIAL NOT FOUND",slot.library_name,slot.category_name,slot.item_name,obj.mv.name_object)

    #MAKE SURE OBJECT IS TEXTURED
    if obj.mv.type == 'CAGE':
        obj.draw_type = 'WIRE'
    else:
        obj.draw_type = 'TEXTURED'


def save_assembly(assembly,path):
    for obj in bpy.data.objects:
        obj.hide = False
        obj.select = True
        
        for slot in obj.material_slots:
            slot.material = None
      
    bpy.ops.group.create(name=assembly.assembly_name)

    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat, do_unlink=True)
        
    for image in bpy.data.images:
        bpy.data.images.remove(image, do_unlink=True)    

    path = os.path.join(path,assembly.category_name)
    if not os.path.exists(path): os.makedirs(path)
    assembly.set_name(assembly.assembly_name)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(path,assembly.assembly_name + ".blend"))
            
            