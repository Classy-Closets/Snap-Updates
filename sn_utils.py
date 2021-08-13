import os
import sys
import mathutils
import math
import random
import re
import inspect
from pathlib import Path

import bpy
from bpy_extras import view3d_utils
import bmesh
import bgl
import blf

from snap import sn_types
from snap import sn_paths
from snap import sn_unit


def get_object_icon(obj):
    if 'IS_BP_ASSEMBLY' in obj:
        return 'FILE_3D'
    if obj.type == 'MESH':
        return 'OUTLINER_OB_MESH'
    if obj.type == 'CURVE':
        return 'OUTLINER_OB_CURVE'
    if obj.type == 'FONT':
        return 'OUTLINER_OB_FONT'
    if obj.type == 'EMPTY':
        return 'OUTLINER_OB_EMPTY'
    if obj.type == 'LATTICE':
        return 'OUTLINER_OB_LATTICE'
    if obj.type == 'META':
        return 'OUTLINER_OB_META'
    if obj.type == 'LIGHT':
        return 'OUTLINER_OB_LIGHT'
    if obj.type == 'CAMERA':
        return 'OUTLINER_OB_CAMERA'
    if obj.type == 'SURFACE':
        return 'OUTLINER_OB_SURFACE'
    if obj.type == 'ARMATURE':
        return 'OUTLINER_OB_ARMATURE'
    if obj.type == 'SPEAKER':
        return 'OUTLINER_OB_SPEAKER'
    if obj.type == 'FORCE_FIELD':
        return 'OUTLINER_OB_FORCE_FIELD'
    if obj.type == 'GPENCIL':
        return 'OUTLINER_OB_GREASEPENCIL'
    if obj.type == 'LIGHT_PROBE':
        return 'OUTLINER_OB_LIGHTPROBE'


def get_assembly_bp(obj):
    if obj:
        if "IS_BP_ASSEMBLY" in obj:
            return obj
        elif obj.parent:
            return get_assembly_bp(obj.parent)


def get_drivers(obj):
    drivers = []
    if obj.animation_data:
        for driver in obj.animation_data.drivers:
            drivers.append(driver)

    if obj.data and obj.data.animation_data:
        for driver in obj.data.animation_data.drivers:
            drivers.append(driver)

    return drivers


def get_material(category, material_name):
    try:
        if material_name in bpy.data.materials:
            return bpy.data.materials[material_name]

        material_path = os.path.join(sn_paths.MATERIAL_DIR, category, material_name + ".blend")

        with bpy.data.libraries.load(material_path, False, False) as (data_from, data_to):
            for mat in data_from.materials:
                if mat == material_name:
                    data_to.materials = [mat]
                    break

        if len(data_to.materials) == 0:
            bpy.ops.snap.message_box(
                'INVOKE_DEFAULT',
                message="'{}' not found in library file: '{}'".format(material_name, material_name + ".blend"))
            return

        for mat in data_to.materials:
            return mat

    except OSError as os_err:
        print(os_err)
        bpy.ops.snap.message_box(
            'INVOKE_DEFAULT',
            message="Material file not found for: {}".format(material_name))


def get_part_thickness(obj):
    '''Backing should no longer be attached to a static spec group thickness
    however, material pointers are still needed so keeping cutpart 'Back' for now

    TODO: Allow for cutpart pointer thickness to be optional, in this case get_part_thickness
    will return actual part thickness
    '''
    if obj.parent:
        obj_props = obj.parent.sn_closets

        backing_parts = [
            obj_props.is_back_bp,
            obj_props.is_top_back_bp,
            obj_props.is_bottom_back_bp
        ]

        if any(backing_parts):
            for child in obj.parent.children:
                if 'obj_z' in child:
                    return math.fabs(child.location.z)

        if obj.get("IS_COVER_CLEAT"):
            cover_cleat = sn_types.Assembly(obj.parent)
            closet_materials = bpy.context.scene.closet_materials
            mat_sku = closet_materials.get_mat_sku(obj.parent, cover_cleat)
            mat_inventory_name = closet_materials.get_mat_inventory_name(sku=mat_sku)
            if(mat_inventory_name == "Oxford White" or mat_inventory_name == "Cabinet Almond" or mat_inventory_name == "Duraply Almond" or mat_inventory_name == "Duraply White"):
                return math.fabs(sn_unit.inch(0.38))
            else:
                return math.fabs(sn_unit.inch(0.75))

    if obj.snap.type_mesh == 'CUTPART':
        spec_group = bpy.context.scene.snap.spec_groups[obj.snap.spec_group_index]
        if obj.snap.cutpart_name in spec_group.cutparts:
            return spec_group.cutparts[obj.snap.cutpart_name].thickness
        else:
            if obj.parent:
                for child in obj.parent.children:
                    if 'obj_z' in child:
                        return math.fabs(child.location.z)

    if obj.snap.type_mesh in {'SOLIDSTOCK', 'BUYOUT'}:
        if obj.parent:
            for child in obj.parent.children:
                if 'obj_z' in child:
                    return math.fabs(child.location.z)

    if obj.snap.type_mesh == 'EDGEBANDING':
        for mod in obj.modifiers:
            if mod.type == 'SOLIDIFY':
                return mod.thickness

    return 0


def get_wall_bp(obj):
    if not obj:
        return None
    if "IS_BP_WALL" in obj:
        return obj
    elif obj.parent:
        return get_wall_bp(obj.parent)


def get_room_bp(obj):
    if not obj:
        return None
    if "IS_ROOM_BP" in obj:
        return obj
    elif obj.parent:
        return get_room_bp(obj.parent)


def get_cabinet_bp(obj):
    if not obj:
        return None
    if "IS_CABINET_BP" in obj:
        return obj
    elif obj.parent:
        return get_cabinet_bp(obj.parent)


def get_closet_bp(obj):
    if not obj:
        return None
    if "IS_BP_CLOSET" in obj or 'IS_BP_WINDOW' in obj or 'IS_BP_ENTRY_DOOR' in obj:
        return obj
    elif obj.parent:
        return get_closet_bp(obj.parent)


def get_carcass_bp(obj):
    if not obj:
        return None
    if "IS_CARCASS_BP" in obj:
        return obj
    elif obj.parent:
        return get_carcass_bp(obj.parent)


def get_appliance_bp(obj):
    if not obj:
        return None
    if "IS_APPLIANCE_BP" in obj:
        return obj
    elif obj.parent:
        return get_appliance_bp(obj.parent)


def get_range_bp(obj):
    if not obj:
        return None
    if "IS_RANGE_BP" in obj:
        return obj
    elif obj.parent:
        return get_range_bp(obj.parent)


def get_door_bp(obj):
    if not obj:
        return None
    if "IS_DOOR_BP" in obj:
        return obj
    elif obj.parent:
        return get_door_bp(obj.parent)

def get_entry_door_bp(obj):
    if not obj:
        return None
    if "IS_BP_ENTRY_DOOR" in obj:
        return obj
    elif obj.parent:
        return get_entry_door_bp(obj.parent)


def get_window_bp(obj):
    if not obj:
        return None
    if "IS_BP_WINDOW" in obj:
        return obj
    elif obj.parent:
        return get_window_bp(obj.parent)


def get_exterior_bp(obj):
    if not obj:
        return None
    if "IS_EXTERIOR_BP" in obj:
        return obj
    elif obj.parent:
        return get_exterior_bp(obj.parent)


def get_object(path):
    print(path)
    if os.path.exists(path):

        with bpy.data.libraries.load(path, False, False) as (data_from, data_to):
            data_to.objects = data_from.objects

        for obj in data_to.objects:
            return obj


def assign_materials_from_pointers(obj):
    library = bpy.context.scene.snap
    spec_group = library.spec_groups[obj.snap.spec_group_index]

    # ASSIGN POINTERS TO MESH BASED ON MESH TYPE
    if obj.snap.type_mesh == 'CUTPART':

        if obj.snap.cutpart_name == 'Back':
            back_bp = obj.parent
            bp_props = back_bp.sn_closets

            if bp_props.use_unique_material:
                if bp_props.unique_mat_types == 'MELAMINE':
                    unique_mat_name = bp_props.unique_mat_mel
                if bp_props.unique_mat_types == 'TEXTURED_MELAMINE':
                    unique_mat_name = bp_props.unique_mat_tex_mel
                if bp_props.unique_mat_types == 'VENEER':
                    unique_mat_name = bp_props.unique_mat_veneer

                for slot in obj.snap.material_slots:
                    slot.category_name = "Closet Materials"
                    slot.item_name = unique_mat_name

        if spec_group:
            if obj.snap.cutpart_name in spec_group.cutparts:
                cutpart = spec_group.cutparts[obj.snap.cutpart_name]
                for index, slot in enumerate(obj.snap.material_slots):
                    if slot.name == 'Core':
                        slot.pointer_name = cutpart.core
                    elif slot.name in {'Top', 'Exterior'}:
                        slot.pointer_name = cutpart.top
                    elif slot.name in {'Bottom', 'Interior'}:
                        slot.pointer_name = cutpart.bottom
                    elif not obj.snap.use_multiple_edgeband_pointers:
                        if obj.snap.edgepart_name in spec_group.edgeparts:
                            edgepart = spec_group.edgeparts[obj.snap.edgepart_name]
                            slot.pointer_name = edgepart.material

                    if slot.pointer_name in spec_group.materials:
                        material_pointer = spec_group.materials[slot.pointer_name]
                        slot.category_name = material_pointer.category_name
                        slot.item_name = material_pointer.item_name

    elif obj.snap.type_mesh == 'EDGEBANDING':
        obj.show_bounds = False
        if spec_group:
            if obj.snap.edgepart_name in spec_group.edgeparts:
                edgepart = spec_group.edgeparts[obj.snap.edgepart_name]
                for index, slot in enumerate(obj.snap.material_slots):
                    slot.pointer_name = edgepart.material

                    if slot.pointer_name in spec_group.materials:
                        material_pointer = spec_group.materials[slot.pointer_name]
                        slot.category_name = material_pointer.category_name
                        slot.item_name = material_pointer.item_name

    elif obj.snap.type_mesh == 'MACHINING':
        # MAKE A SIMPLE BLACK MATERIAL FOR MACHINING
        for slot in obj.snap.material_slots:
            slot.category_name = "Plastics"
            slot.item_name = "Gloss Black Plastic"

    else:
        if spec_group:
            for index, slot in enumerate(obj.snap.material_slots):
                if slot.pointer_name in spec_group.materials:
                    material_pointer = spec_group.materials[slot.pointer_name]
                    slot.category_name = material_pointer.category_name
                    slot.item_name = material_pointer.item_name

    # RETRIEVE MATERIAL FROM CATEGORY NAME AND ITEM NAME AND ASSIGN TO SLOT
    for index, slot in enumerate(obj.snap.material_slots):
        if slot.item_name and slot.item_name != "None":
            material = get_material(slot.category_name, slot.item_name)

            if material:
                obj.material_slots[index].material = material

    obj.display_type = 'TEXTURED'


def object_has_driver(obj):
    if obj.animation_data:
        if len(obj.animation_data.drivers) > 0:
            return True


def draw_driver(layout, obj, driver):
    props = bpy.context.scene.snap
    col = layout.column(align=True)
    box = col.box()
    row = box.row()
    driver_name = driver.data_path
    if driver_name in {"location", "rotation_euler", "dimensions", "lock_scale", 'lock_location', 'lock_rotation'}:
        if driver.array_index == 0:
            driver_name = driver_name + " X"
        if driver.array_index == 1:
            driver_name = driver_name + " Y"
        if driver.array_index == 2:
            driver_name = driver_name + " Z"
    try:
        value = eval(
            'bpy.data.objects["' + obj.name + '"].' + driver.data_path)
    except Exception as ex:
        print(ex)
        value = eval(
            'bpy.data.objects["' + obj.name + '"].data.' + driver.data_path)
    if type(value).__name__ == 'str':
        row.label(text=driver_name + " = " + str(value), icon='AUTO')
    elif type(value).__name__ == 'float':
        row.label(text=driver_name + " = " + str(value), icon='AUTO')
    elif type(value).__name__ == 'int':
        row.label(text=driver_name + " = " + str(value), icon='AUTO')
    elif type(value).__name__ == 'bool':
        row.label(text=driver_name + " = " + str(value), icon='AUTO')
    elif type(value).__name__ == 'bpy_prop_array':
        row.label(text=driver_name + " = " + str(value[driver.array_index]), icon='AUTO')
    elif type(value).__name__ == 'Vector':
        row.label(text=driver_name + " = " + str(value[driver.array_index]), icon='AUTO')
    elif type(value).__name__ == 'Euler':
        row.label(text=driver_name + " = " + str(value[driver.array_index]), icon='AUTO')
    else:
        row.label(text=driver_name + " = " + str(type(value)), icon='AUTO')

    row = box.row(align=True)
    if driver.driver.is_valid:
        row.prop(driver.driver, "expression", text="",
                 expand=True, icon='DECORATE')
        if driver.mute:
            row.prop(driver, "mute", text="", icon='DECORATE')
        else:
            row.prop(driver, "mute", text="", icon='DECORATE')
    else:
        row.prop(driver.driver, "expression",
                 text="", expand=True, icon='ERROR')
        if driver.mute:
            row.prop(driver, "mute", text="", icon='DECORATE')
        else:
            row.prop(driver, "mute", text="", icon='DECORATE')

    box = col.box()
    row = box.row()
    row.label(text="Formula Variables:")
    row = box.row()
    row.prop(props, 'driver_override_object', text="", icon='DRIVER')
    obj_bp = get_assembly_bp(obj)
    if props.driver_override_object:
        override_obj_bp = get_assembly_bp(props.driver_override_object)
        assembly = sn_types.Assembly(obj_bp=override_obj_bp)
        if assembly.obj_prompts:
            props = row.operator(
                'sn_driver.get_vars_from_object', text=override_obj_bp.name, icon='DRIVER')
            props.object_name = obj.name
            props.var_object_name = assembly.obj_prompts.name
            props.data_path = driver.data_path
            props.array_index = driver.array_index
    elif obj_bp:
        assembly = sn_types.Assembly(obj_bp=obj_bp)
        props = row.operator('sn_driver.get_vars_from_object',
                             text=assembly.obj_bp.name, icon='DRIVER')
        props.object_name = obj.name
        props.var_object_name = assembly.obj_prompts.name
        props.data_path = driver.data_path
        props.array_index = driver.array_index
    else:
        props = row.operator('sn_driver.get_vars_from_object',
                             text=obj.name, icon='DRIVER')
        props.object_name = obj.name
        props.var_object_name = obj.name
        props.data_path = driver.data_path
        props.array_index = driver.array_index

    draw_driver_variables(box, obj, driver)


def draw_driver_variables(layout, obj, driver):
    for var in driver.driver.variables:
        col = layout.column()
        boxvar = col.box()
        row = boxvar.row(align=True)
        row.prop(var, "name", text="", icon='FORWARD')

        props = row.operator("sn_driver.remove_variable",
                             text="", icon='X', emboss=False)
        props.object_name = obj.name
        props.data_path = driver.data_path
        props.array_index = driver.array_index
        props.var_name = var.name

        for target in var.targets:
            if obj.snap.show_driver_debug_info:
                row = boxvar.row()
                row.prop(var, "type", text="")
                row = boxvar.row()
                row.prop(target, "id", text="")
                row = boxvar.row(align=True)
                row.prop(target, "data_path", text="", icon='ANIM_DATA')

            if target.id and target.data_path != "":
                value = eval(
                    'bpy.data.objects["' + target.id.name + '"]'"." + target.data_path)
            else:
                value = "ERROR#"
            row = boxvar.row()
            row.alignment = 'CENTER'
            if type(value).__name__ == 'str':
                row.label(text="Value: " + value)
            elif type(value).__name__ == 'float':
                row.label(text="Value: " + str(bpy.utils.units.to_string(
                    bpy.context.scene.unit_settings.system, 'LENGTH', value)))
            elif type(value).__name__ == 'int':
                row.label(text="Value: " + str(value))
            elif type(value).__name__ == 'bool':
                row.label(text="Value: " + str(value))


def hook_vertex_group_to_object(obj_mesh, vertex_group, obj_hook):
    bpy.ops.object.select_all(action='DESELECT')
    obj_hook.hide_set(False)
    obj_hook.hide_viewport = False
    obj_hook.hide_select = False
    obj_hook.select_set(True)
    obj_mesh.hide_set(False)
    obj_mesh.hide_select = False
    if vertex_group in obj_mesh.vertex_groups:
        vgroup = obj_mesh.vertex_groups[vertex_group]
        obj_mesh.vertex_groups.active_index = vgroup.index
        bpy.context.view_layer.objects.active = obj_mesh
        bpy.ops.sn_object.toggle_edit_mode(obj_name=obj_mesh.name)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        if obj_mesh.data.total_vert_sel > 0:
            bpy.ops.object.hook_add_selob()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.sn_object.toggle_edit_mode(obj_name=obj_mesh.name)


def flip_normals(assembly):
    for child in assembly.obj_bp.children:
        if child.type == 'MESH':
            for polygon in child.data.polygons:
                polygon.flip()
            child.data.update()


def apply_hook_modifiers(context, obj):
    obj.hide_set(False)
    obj.select_set(True)
    context.view_layer.objects.active = obj
    for mod in obj.modifiers:
        if mod.type == 'HOOK':
            bpy.ops.object.modifier_apply(modifier=mod.name)


def unwrap_obj(context, obj):
    context.view_layer.objects.active = obj
    apply_hook_modifiers(context, obj)

    mode = obj.mode
    if obj.mode == 'OBJECT':
        bpy.ops.object.editmode_toggle()

    bpy.ops.mesh.select_all(action='SELECT')
    # angle_limit should be in radians
    bpy.ops.uv.smart_project(
        angle_limit=1.15192)
    if mode == 'OBJECT':
        bpy.ops.object.editmode_toggle()

    bpy.ops.sn_assembly.connect_meshes_to_hooks_in_assembly(obj_name=obj.name)


def add_bevel(assembly):
    for child in assembly.obj_bp.children:
        if child.type == 'MESH':
            bevel = child.modifiers.new('Bevel', 'BEVEL')
            bevel.width = .0005


def create_cube_mesh(name, size):

    verts = [(0.0, 0.0, 0.0),
             (0.0, size[1], 0.0),
             (size[0], size[1], 0.0),
             (size[0], 0.0, 0.0),
             (0.0, 0.0, size[2]),
             (0.0, size[1], size[2]),
             (size[0], size[1], size[2]),
             (size[0], 0.0, size[2]),
             ]

    faces = [(0, 1, 2, 3),
             (4, 7, 6, 5),
             (0, 4, 5, 1),
             (1, 5, 6, 2),
             (2, 6, 7, 3),
             (4, 0, 3, 7),
             ]

    return create_object_from_verts_and_faces(verts, faces, name)


def create_object_from_verts_and_faces(verts, faces, name):
    """
    Creates an object from Verties and Faces
    arg1: Verts List of tuples [(float,float,float)]
    arg2: Faces List of ints
    arg3: name of object

    RETURNS bpy.types.Object
    """
    mesh = bpy.data.meshes.new(name)

    bm = bmesh.new()

    for v_co in verts:
        bm.verts.new(v_co)

    for f_idx in faces:
        bm.verts.ensure_lookup_table()
        bm.faces.new([bm.verts[i] for i in f_idx])

    bm.to_mesh(mesh)

    mesh.update()

    obj_new = bpy.data.objects.new(mesh.name, mesh)
    bpy.context.scene.collection.objects.link(obj_new)

    return obj_new


def delete_obj_list(obj_list):
    bpy.ops.object.select_all(action='DESELECT')
    for obj in obj_list:
        if obj.animation_data:
            for driver in obj.animation_data.drivers:
                # TODO:
                # THESE DRIVERS MUST BE REMOVED TO DELETE OBJECTS
                if driver.data_path in {'hide', 'hide_select'}:
                    obj.driver_remove(driver.data_path)

        # TODO: FIGURE OUT IF THIS IS RIGHT
        if obj.name in bpy.context.view_layer.active_layer_collection.collection.objects:
            obj.parent = None
            obj.hide_select = False
            obj.hide_viewport = False
            obj.select_set(True)

            bpy.context.view_layer.active_layer_collection.collection.objects.unlink(
                obj)
            # bpy.context.scene.objects.unlink(obj)

    for obj in obj_list:
        bpy.data.objects.remove(obj, do_unlink=True)


def delete_object_and_children(obj_bp):
    obj_list = []
    obj_list.append(obj_bp)
    for child in obj_bp.children:
        if len(child.children) > 0:
            delete_object_and_children(child)
        else:
            obj_list.append(child)
    delete_obj_list(obj_list)


def calc_distance(point1, point2):
    """ This gets the distance between two points (X,Y,Z)
    """
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)


def floor_raycast(context, mx, my):
    '''
    This casts a ray into the 3D view and returns information based on what is under the mouse

    ARGS
    context (bpy.context) = current blender context
    mx (float) = 2D mouse x location
    my (float) = 2D mouse y location

    RETURNS tuple
    has_hit (boolean) - determines if an object is under the mouse
    snapped_location (tuple) - x,y,z location of location under mouse
    snapped_normal (tuple) - normal direction
    snapped_rotation (tuple) - rotation
    face_index (int) - face index under mouse
    object (bpy.types.Object) - Blender Object under mouse
    martix (float multi-dimensional array of 4 * 4 items in [-inf, inf]) - matrix of placement under mouse
    '''
    r = context.region
    rv3d = context.region_data
    coord = mx, my

    # get the ray from the viewport and mouse
    view_vector = view3d_utils.region_2d_to_vector_3d(r, rv3d, coord)
    ray_origin = view3d_utils.region_2d_to_origin_3d(r, rv3d, coord)
    # ray_target = ray_origin + (view_vector * 1000000000)
    ray_target = ray_origin + view_vector

    snapped_location = mathutils.geometry.intersect_line_plane(ray_origin, ray_target, (0, 0, 0), (0, 0, 1),
                                                               False)
    if snapped_location is not None:
        has_hit = True
        snapped_normal = mathutils.Vector((0, 0, 1))
        face_index = None
        object = None
        matrix = None
        snapped_rotation = snapped_normal.to_track_quat('Z', 'Y').to_euler()
        offset_rotation_amount = 0
        randomize_rotation_amount = 0
        randomize_rotation = False
        if randomize_rotation:
            randoffset = offset_rotation_amount + math.pi + (
                random.random() - 0.5) * randomize_rotation_amount
        else:
            randoffset = offset_rotation_amount + math.pi
        snapped_rotation.rotate_axis('Z', randoffset)

    return has_hit, snapped_location, snapped_normal, snapped_rotation, face_index, object, matrix


def get_selection_point(context, event, ray_max=10000.0, objects=None, floor=None, exclude_objects=[]):
    """Gets the point to place an object based on selection"""
    # get the context arguments
    scene = context.scene
    region = context.region
    rv3d = context.region_data
    coord = event.mouse_region_x, event.mouse_region_y
    # get the ray from the viewport and mouse
    view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
    ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
    ray_target = ray_origin + view_vector

    def visible_objects_and_duplis():
        """Loop over (object, matrix) pairs (mesh only)"""

        for obj in context.visible_objects:

            if objects:
                if obj in objects and obj not in exclude_objects:
                    yield (obj, obj.matrix_world.copy())

            else:
                if obj not in exclude_objects:
                    if floor is not None and obj == floor:
                        yield (obj, obj.matrix_world.copy())

    #                 if obj.display_type != 'WIRE':
                    if obj.type == 'MESH' and obj.hide_select is False:
                        yield (obj, obj.matrix_world.copy())

                    if obj.instance_type != 'NONE':
                        obj.dupli_list_create(scene)
                        for dob in obj.dupli_list:
                            obj_dupli = dob.object
                            if obj_dupli.type == 'MESH':
                                yield (obj_dupli, dob.matrix.copy())
            # TODO:
            # obj.dupli_list_clear()

    def obj_ray_cast(obj, matrix):
        """Wrapper for ray casting that moves the ray into object space"""
        try:
            # get the ray relative to the object
            matrix_inv = matrix.inverted()
            ray_origin_obj = matrix_inv @ ray_origin
            ray_target_obj = matrix_inv @ ray_target
            ray_direction_obj = ray_target_obj - ray_origin_obj

            # cast the ray
            success, location, normal, face_index = obj.ray_cast(
                ray_origin_obj, ray_direction_obj)

            if success:
                return location, normal, face_index
            else:
                return None, None, None
        except Exception as ex:
            print(ex)
            print("ERROR IN obj_ray_cast", obj)
            return None, None, None

    best_length_squared = ray_max * ray_max
    best_obj = None
    best_hit = (0, 0, 0)
    best_normal = (0, 0, 1)
    for obj, matrix in visible_objects_and_duplis():
        if obj.type == 'MESH':
            if obj.data:
                hit, normal, face_index = obj_ray_cast(obj, matrix)
                if hit is not None:
                    hit_world = matrix @ hit
                    length_squared = (hit_world - ray_origin).length_squared
                    if length_squared < best_length_squared:
                        best_hit = hit_world
                        best_length_squared = length_squared
                        best_obj = obj
                        best_normal = normal
                        if best_normal:
                            best_normal = best_obj.matrix_world.to_euler().to_matrix() @ mathutils.Vector(best_normal)
    return best_hit, best_obj, best_normal


def save_assembly(assembly, path):
    for obj in bpy.data.objects:
        obj.hide_set(False)
        obj.select_set(True)

        for slot in obj.material_slots:
            slot.material = None

    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat, do_unlink=True)

    for image in bpy.data.images:
        bpy.data.images.remove(image, do_unlink=True)

    path = os.path.join(path, assembly.category_name)
    if not os.path.exists(path):
        os.makedirs(path)
    assembly.set_name(assembly.assembly_name)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(
        path, assembly.assembly_name + ".blend"))


def update_file_browser_path(context, path):
    for area in context.screen.areas:
        if area.type == 'FILE_BROWSER':
            for space in area.spaces:
                if space.type == 'FILE_BROWSER':
                    params = space.params
                    params.directory = str.encode(path)
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


def register_library(name, lib_type, drop_id, icon, use_custom_icon):
    """ This registers a library with SNaP
    """
    snap = bpy.context.window_manager.snap
    if name not in snap.libraries:
        snap.add_library(
            name=name,
            lib_type=lib_type,
            drop_id=drop_id,
            icon=icon,
            use_custom_icon=use_custom_icon,
        )


def unregister_library(name):
    """ This unregisters a library with SNaP
    """
    snap = bpy.context.window_manager.snap
    snap.remove_library(name)


# -------OBJECT FUNCTIONS


def create_chamfer_cube_mesh(name, size, l_depth, r_depth):

    verts = [(0.0, 0.0, 0.0),
             (0.0, size[1], 0.0),
             (l_depth, size[1], 0.0),
             (size[0], -r_depth, 0.0),
             (size[0], 0.0, 0.0),
             (0.0, 0.0, size[2]),
             (0.0, size[1], size[2]),
             (l_depth, size[1], size[2]),
             (size[0], -r_depth, size[2]),
             (size[0], 0.0, size[2]),
             ]

    faces = [(0, 1, 2, 3, 4),
             (5, 6, 7, 8, 9),
             (0, 1, 6, 5),
             (0, 4, 9, 5),
             (4, 3, 8, 9),
             (1, 2, 7, 6),
             (2, 3, 8, 7),
             ]

    return create_object_from_verts_and_faces(verts, faces, name)


def create_pie_cut_mesh(name, size, l_depth, r_depth):

    verts = [(0.0, 0.0, 0.0),
             (0.0, size[1], 0.0),
             (l_depth, size[1], 0.0),
             (l_depth, -r_depth, 0.0),
             (size[0], -r_depth, 0.0),
             (size[0], 0.0, 0.0),
             (0.0, 0.0, size[2]),
             (0.0, size[1], size[2]),
             (l_depth, size[1], size[2]),
             (l_depth, -r_depth, size[2]),
             (size[0], -r_depth, size[2]),
             (size[0], 0.0, size[2]),
             ]

    faces = [(0, 1, 2, 3, 4, 5),
             (6, 7, 8, 9, 10, 11),
             (0, 1, 7, 6),
             (0, 5, 11, 6),
             (5, 4, 10, 11),
             (1, 2, 8, 7),
             (2, 3, 9, 8),
             (3, 4, 10, 9),
             ]

    return create_object_from_verts_and_faces(verts, faces, name)


def create_floor_mesh(name, size):

    verts = [(0.0, 0.0, 0.0),
             (0.0, size[1], 0.0),
             (size[0], size[1], 0.0),
             (size[0], 0.0, 0.0),
             ]

    faces = [(0, 1, 2, 3),
             ]

    return create_object_from_verts_and_faces(verts, faces, name)


def create_single_vertex(name):

    verts = [(0, 0, 0)]

    return create_object_from_verts_and_faces(verts, [], name)


def copy_world_loc(source, target, offset=(0, 0, 0)):
    """ This function copies the source object's world location and applies it
        to the target object. Final target location can be adjusted
        with a location offset.
    """
    off_mtx = mathutils.Matrix.Translation(mathutils.Vector(offset))
    result_loc = (source.matrix_world @ off_mtx).to_translation()
    target.matrix_world.translation = result_loc


def copy_world_rot(source, target, offset=(0, 0, 0)):
    """ This function copies the source object's world rotation and applies it
        to the target object. Final target rotation can be adjusted
        with a rotation offset provided in degrees.
    """
    off_rad = [math.radians(o) for o in offset]
    off_mtx = mathutils.Euler(off_rad, source.rotation_mode).to_matrix()
    result_rot = source.matrix_world.to_3x3().normalized() @ off_mtx
    target.matrix_world @= result_rot.to_4x4()


def link_objects_to_scene(obj_bp, scene_collection):
    """ This Function links an object and all of it's children
        to the scene
    """
    obj_bp.display_type = 'WIRE'  # THIS IS NEEDED FOR DRAG AND DROP
    obj_bp.select_set(False)
    scene_collection.objects.link(obj_bp)
    if obj_bp.type == 'EMPTY':
        obj_bp.hide_set(True)
    for child in obj_bp.children:
        link_objects_to_scene(child, scene_collection)


def create_vertex_group_for_hooks(obj_mesh, vert_list, vgroupname):
    """ Adds a new vertex group to a mesh. If the group already exists
        Then no group is added. The second parameter allows you to assign
        verts to the vertex group.
        Arg1: bpy.data.Object | Mesh Object to operate on
        Arg2: [] of int | vertext indexs to assign to group
        Arg3: string | vertex group name
    """
    if vgroupname not in obj_mesh.vertex_groups:
        obj_mesh.vertex_groups.new(name=vgroupname)

    vgroup = obj_mesh.vertex_groups[vgroupname]
    vgroup.add(vert_list, 1, 'ADD')


def set_object_name(obj):
    """ This function sets the name of an object to make the outliner easier to navigate
    """
    counter = str(obj.snap.item_number)
    if obj.get('VPDIMX') or obj.get('VPDIMY') or obj.get('VPDIMZ'):
        obj.name = counter + '.' + obj.snap.type + '.' + \
            obj.parent.snap.name_object if obj.parent else obj.snap.name_object
    elif obj.get('IS_BP_ASSEMBLY'):
        if obj.snap.type_group in {'PRODUCT', 'INSERT', 'OPENING'}:
            obj.name = counter + '.' + obj.snap.type_group + '.' + obj.snap.name_object
        else:
            obj.name = counter + '.BPASSEMBLY.' + obj.snap.name_object
    elif obj.snap.type_mesh != 'NONE':
        obj.name = counter + '.' + obj.snap.type_mesh + '.' + \
            obj.parent.snap.name_object + '.' + obj.snap.name_object
    elif obj.snap.type in ['VISDIM_A', 'VISDIM_B']:
        obj.name = counter + '.DIMENSION.' + \
            obj.parent.snap.name_object + '.' + obj.snap.name_object
    else:

        obj.name = counter + '.' + obj.type + '.' + obj.snap.name_object


def get_child_objects(obj, obj_list=None):
    """ Returns: List of Objects
        Par1: obj - Object to collect all of the children from
        Par2: list - List of Objects to store all of the objects in
    """
    if not obj_list:
        obj_list = []
    if obj not in obj_list:
        obj_list.append(obj)
    for child in obj.children:
        obj_list.append(child)
        get_child_objects(child, obj_list)
    return obj_list


def get_material_name(obj):
    if obj.snap.type_mesh in {'CUTPART', 'EDGEBANDING'}:
        # IF snap.cutpart_material_name IS SET THEN RETURN THAT VALUE
        # THIS IS USED FOR USERS WHO WANT TO CONTROL THE NAME
        # OF THE MATERIAL THAT GETS EXPORTED
        if obj.snap.cutpart_material_name != "":
            return obj.snap.cutpart_material_name
        thickness = str(
            round(sn_unit.meter_to_active_unit(get_part_thickness(obj)), 4))
        core = ""
        exterior = ""
        interior = ""
        for sn_slot in obj.snap.material_slots:
            if sn_slot.name == 'Core':
                core = sn_slot.item_name
            if sn_slot.name in {'Top', 'Exterior'}:
                exterior = sn_slot.item_name
            if sn_slot.name in {'Bottom', 'Interior'}:
                interior = sn_slot.item_name

        return format_material_name(thickness, core, exterior, interior)

    if obj.snap.type_mesh == 'BUYOUT':

        if obj.snap.buyout_material_name != "":
            return obj.snap.buyout_material_name

        # THIS IS NEEDED FOR THE DOOR BUILDER LIBRARY
        # BECAUSE THE DOOR ASSEMBLY BP IS MARKED AS BUYOUT
        if obj.get('IS_BP_ASSEMBLY'):
            return obj.snap.name_object
        if obj.parent:
            return obj.parent.snap.name_object
        else:
            return obj.snap.name_object

    if obj.snap.type_mesh == 'SOLIDSTOCK':
        return obj.snap.solid_stock


def format_material_name(thickness, core, exterior, interior):
    if core == exterior:
        exterior = "-"

    if core == interior:
        interior = "-"

    return thickness + " " + core + " [" + exterior + "] [" + interior + "]"


def connect_objects_location(anchor_obj, obj):
    """ This function adds a copy location constraint to the obj
        add sets the target to the anchor_obj
    """
    constraint = obj.constraints.new('COPY_LOCATION')
    constraint.target = anchor_obj
    constraint.use_x = True
    constraint.use_y = True
    constraint.use_z = True


def get_edgebanding_thickness_from_pointer_name(pointer_name, spec_group):
    """ This function returns the thickness from an edge pointer
    """
    if pointer_name in spec_group.edgeparts:
        pointer = spec_group.edgeparts[pointer_name]
        thickness = round(sn_unit.meter_to_active_unit(pointer.thickness), 4)
        return thickness
    else:
        return 0


def get_edgebanding_name_from_pointer_name(pointer_name, spec_group):
    if pointer_name in spec_group.edgeparts:
        pointer = spec_group.edgeparts[pointer_name]
        thickness = str(round(sn_unit.meter_to_active_unit(pointer.thickness), 4))
        material = spec_group.materials[pointer.material].item_name
        if thickness + " " + material not in bpy.context.scene.snap.edgebanding:
            mat = bpy.context.scene.snap.edgebanding.add()
            mat.thickness = pointer.thickness
            mat.name = thickness + " " + material
        return thickness + " " + material
    else:
        return ""


def get_material_name_from_pointer(pointer, spec_group):
    thickness = str(round(sn_unit.meter_to_active_unit(pointer.thickness), 4))
    if pointer.core in spec_group.materials:
        core_material = spec_group.materials[pointer.core].item_name
    else:
        core_material = "NA"
    if pointer.top in spec_group.materials:
        top_material = spec_group.materials[pointer.top].item_name
    else:
        top_material = "NA"
    if pointer.bottom in spec_group.materials:
        bottom_material = spec_group.materials[pointer.bottom].item_name
    else:
        bottom_material = "NA"
    return format_material_name(thickness, core_material, top_material, bottom_material)

# -------LIBRARY FUNCTIONS


def get_library_dir(lib_type=""):
    if lib_type == 'assemblies':
        if os.path.exists(bpy.context.window_manager.snap.assembly_library_path):
            return bpy.context.window_manager.snap.assembly_library_path
    if lib_type == 'objects':
        if os.path.exists(bpy.context.window_manager.snap.object_library_path):
            return bpy.context.window_manager.snap.object_library_path
    if lib_type == 'materials':
        if os.path.exists(bpy.context.window_manager.snap.material_library_path):
            return bpy.context.window_manager.snap.material_library_path
    if lib_type == 'worlds':
        if os.path.exists(bpy.context.window_manager.snap.world_library_path):
            return bpy.context.window_manager.snap.world_library_path

    # If no path is set get default path
    root_path = os.path.join(os.path.dirname(bpy.app.binary_path), "data")
    if lib_type == "":
        return root_path
    else:
        return os.path.join(root_path, lib_type)


def get_library_packages(context, only_external=False):
    """ Returns: List (of Strings)
    Adds FD Library Packages to PYTHON Path, and Returns list of package folder names.
    """
    packages = []
    path = Path(sn_paths.LIBRARY_ROOT)

    for folder in path.iterdir():
        if folder.is_dir():
            for file in folder.iterdir():
                if '__init__.py' in file.name:
                    path, folder_name = os.path.split(
                        os.path.normpath(sn_paths.CLOSET_ROOT))
                    sys.path.append(path)
                    packages.append(folder_name)
                    break

    return packages


def get_product_class(context, library_name, category_name, product_name):
    """ Returns: Object (Product Class)
    Gets the Product Class Base on active product library name
    """
    lib = context.window_manager.snap.lib_products[context.scene.snap.product_library_name]
    pkg = __import__(lib.package_name)

    for modname, modobj in inspect.getmembers(pkg):
        for name, obj in inspect.getmembers(modobj):
            if "PRODUCT_" in name and inspect.isclass(obj):
                product = obj()
                if product.assembly_name == "":
                    product.assembly_name = get_product_class_name(name)
                if product.library_name == library_name and \
                   product.category_name == category_name and \
                   product.assembly_name == product_name:
                    product.package_name = lib.package_name
                    product.module_name = modname
                    return product


def get_insert_class(context, library_name, category_name, insert_name):
    """ Returns: Object (Product Class)
    Gets the Product Class Base on active product library name
    """
    lib = context.window_manager.snap.lib_inserts[context.scene.snap.insert_library_name]
    pkg = __import__(lib.package_name)

    for modname, modobj in inspect.getmembers(pkg):
        for name, obj in inspect.getmembers(modobj):
            if "INSERT_" in name and inspect.isclass(obj):
                insert = obj()
                if insert.assembly_name == "":
                    insert.assembly_name = get_insert_class_name(name)
                if insert.library_name == library_name and \
                   insert.category_name == category_name and \
                   insert.assembly_name == insert_name:
                    insert.package_name = lib.package_name
                    insert.module_name = modname
                    return insert


def get_group(path):

    with bpy.data.libraries.load(path, False, False) as (data_from, data_to):
        for collection in data_from.collections:
            data_to.collections = [collection]
            break

    for collection in data_to.collections:
        """
        THIS IS A HACK
        In Blender 2.78a if an object has a reference to a shape key
        the object is not appended it is linked. If an object is linked
        it can cause errors trying to link duplicate objects into the scene. If a
        library is found on an object we make objects local.
        Unfortunetly we have to make 'ALL' local becuase selected objects doens't work
        when the linked object has hide_select turned on.
        """
        for obj in collection.objects:
            if obj.library:
                bpy.ops.object.make_local(type='ALL')
        """
        END HACK
        """
        obj_bp = get_assembly_bp(collection.objects[0])
        link_objects_to_scene(obj_bp, bpy.context.scene.collection)
        bpy.data.collections.remove(collection, do_unlink=True)
        return obj_bp


def get_product_class_name(class_name):
    name = class_name.replace("PRODUCT_", "")
    return name.replace("_", " ")


def get_insert_class_name(class_name):
    name = class_name.replace("INSERT_", "")
    return name.replace("_", " ")


def set_wireframe(obj, make_wire=True):
    obj.show_in_front = make_wire
    if make_wire:
        obj.display_type = 'WIRE'
    else:
        obj.display_type = 'TEXTURED'
        assign_materials_from_pointers(obj)
    for child in obj.children:
        set_wireframe(child, make_wire)


def get_curve_length(obj_curve):
    """
    This gets a curve objects length. This currently only calculates straight segments.
    """
    length = 0

    if obj_curve.type == 'CURVE':

        for spline in obj_curve.data.splines:
            for index, point in enumerate(spline.bezier_points):
                if len(spline.bezier_points) > index + 1:
                    length += calc_distance(point.co,
                                            spline.bezier_points[index + 1].co)

    return length

# -------ENUM FUNCTIONS


def create_image_preview_collection():
    col = bpy.utils.previews.new()
    col.my_previews_dir = ""
    col.my_previews = ()
    return col


def get_image_enum_previews(path, key, force_reload=False):
    """ Returns: ImagePreviewCollection
        Par1: path - The path to collect the images from
        Par2: key - The dictionary key the previews will be stored in
    """
    enum_items = []
    if len(key.my_previews) > 0:
        return key.my_previews

    if path and os.path.exists(path):
        image_paths = []
        for fn in os.listdir(path):
            if fn.lower().endswith(".png"):
                image_paths.append(fn)

        for i, name in enumerate(image_paths):
            filepath = os.path.join(path, name)
            thumb = key.load(filepath, filepath, 'IMAGE', force_reload)
            filename, ext = os.path.splitext(name)
            enum_items.append((filename, filename, filename, thumb.icon_id, i))

    key.my_previews = enum_items
    key.my_previews_dir = path
    return key.my_previews


def get_folder_enum_previews(path, key):
    """ Returns: ImagePreviewCollection
        Par1: path - The path to collect the folders from
        Par2: key - The dictionary key the previews will be stored in
    """
    enum_items = []
    if len(key.my_previews) > 0:
        return key.my_previews

    if path and os.path.exists(path):
        folders = []
        for fn in os.listdir(path):
            if os.path.isdir(os.path.join(path, fn)):
                folders.append(fn)

        for i, name in enumerate(folders):
            filepath = os.path.join(path, name)
            thumb = key.load(filepath, "", 'IMAGE')
            filename, ext = os.path.splitext(name)
            enum_items.append((filename, filename, filename, thumb.icon_id, i))

    key.my_previews = enum_items
    key.my_previews_dir = path
    return key.my_previews

# -------ASSEMBLY FUNCTIONS


def get_bp(obj, group_type):
    if obj:
        if obj.snap.type_group == group_type and obj.get('IS_BP_ASSEMBLY'):
            return obj
        else:
            if obj.parent:
                return get_bp(obj.parent, group_type)


def get_parent_assembly_bp(obj):
    """ This will get the top level group base point from the passed in object
    """
    if obj:
        if obj.parent:
            if 'IS_BP_ASSEMBLY' in obj.parent:
                return get_parent_assembly_bp(obj.parent)
            else:
                if 'IS_BP_WALL' in obj.parent and 'IS_BP_ASSEMBLY' in obj:
                    return obj
        else:
            if 'IS_BP_ASSEMBLY' in obj:
                return obj


def run_calculators(obj_bp):
    """ Runs all calculators for an assembly and all it's children assemblies
    """
    for calculator in obj_bp.snap.calculators:
        bpy.context.view_layer.update()
        calculator.calculate()

    for child in obj_bp.children:
        if child.get('IS_BP_ASSEMBLY'):
            run_calculators(child)


def set_property_id(obj, property_id):
    """ Returns:None - sets all of the property_id values for the assembly
                       and all of its children.
    """
    obj['ID_PROMPT'] = property_id
    for child in obj.children:
        set_property_id(child, property_id)


def get_insert_bp_list(obj_bp, insert_list):
    for child in obj_bp.children:
        if child.get('IS_BP_ASSEMBLY') and child.snap.type_group == 'INSERT':
            insert_list.append(child)
            get_insert_bp_list(child, insert_list)

    if len(insert_list) > 0:
        insert_list.sort(key=lambda obj: obj.location.z, reverse=True)
    return insert_list


def init_objects(obj_bp):
    """ This Function is used to init all of the objects in an assembly
            -Sets the names of the children
            -Sets the materials
    """
    # set_object_name(obj_bp)
    for child in obj_bp.children:
        # set_object_name(child)

        if child.type == 'EMPTY':
            child.hide_set(True)

        if child.type == 'MESH':
            assign_materials_from_pointers(child)

        if 'IS_VISDIM_A' in child:
            child.hide_set(True)
            for dim_child in child.children:
                dim_child.hide_set(True)

        if 'IS_BP_ASSEMBLY' in child:
            init_objects(child)
            child.hide_set(True)

        if 'use_as_bool_obj' in child:
            child.display_type = 'WIRE'


def render_assembly(assembly, path):

    area = math.fabs(assembly.obj_x.location.x) + math.fabs(
        assembly.obj_y.location.y) + math.fabs(assembly.obj_z.location.z)

    if area == 0:
        # This is used for products that have a base point at the center (faucets)
        # It would be better to develop a way to create a cube that boarders
        # all of the objects and not look to the assembly size.
        rendering_space = sn_unit.inch(0)
    else:
        rendering_space = sn_unit.inch(5)

    render_box = create_cube_mesh("Render Box", (assembly.obj_x.location.x + rendering_space,
                                                 assembly.obj_y.location.y - rendering_space,
                                                 assembly.obj_z.location.z + rendering_space))

    render_box.location.x = assembly.obj_bp.location.x - (rendering_space / 2)
    render_box.location.y = assembly.obj_bp.location.y + (rendering_space / 2)
    render_box.location.z = assembly.obj_bp.location.z - (rendering_space / 2)

    render_box.select_set(True)

    for child in get_child_objects(assembly.obj_bp):
        child.select_set(True)

    bpy.ops.view3d.camera_to_view_selected()
    delete_obj_list([render_box])

    init_objects(assembly.obj_bp)

    render = bpy.context.scene.render
    render.use_file_extension = True
    render.filepath = path
    bpy.ops.render.render(write_still=True)


def replace_assembly(old_assembly, new_assembly):
    ''' replace the old_assembly with the new_assembly
    '''
    new_assembly.obj_bp.snap.name_object = old_assembly.obj_bp.snap.name_object
    new_assembly.obj_bp.parent = old_assembly.obj_bp.parent
    new_assembly.obj_bp.location = old_assembly.obj_bp.location
    new_assembly.obj_bp.rotation_euler = old_assembly.obj_bp.rotation_euler

    copy_drivers(old_assembly.obj_bp, new_assembly.obj_bp)
    copy_prompt_drivers(old_assembly.obj_bp, new_assembly.obj_bp)
    copy_drivers(old_assembly.obj_x, new_assembly.obj_x)
    copy_drivers(old_assembly.obj_y, new_assembly.obj_y)
    copy_drivers(old_assembly.obj_z, new_assembly.obj_z)
    # Go though all siblings and check if the assembly
    # is being referenced in any other drivers.
    search_obj = old_assembly.obj_bp.parent if old_assembly.obj_bp.parent else None
    if search_obj:
        for obj in search_obj.children:
            if obj.animation_data:
                for driver in obj.animation_data.drivers:
                    for var in driver.driver.variables:
                        for target in var.targets:
                            if target.id.name == old_assembly.obj_bp.name:
                                target.id = new_assembly.obj_bp
                            if target.id.name == old_assembly.obj_x.name:
                                target.id = new_assembly.obj_x
                            if target.id.name == old_assembly.obj_y.name:
                                target.id = new_assembly.obj_y
                            if target.id.name == old_assembly.obj_z.name:
                                target.id = new_assembly.obj_z

# -------INTERFACE FUNCTIONS


def get_prop_dialog_width(width):
    """ This function returns the width of a property dialog box in pixels
        This is needed to fix scaling issues with 4k monitors
        TODO: test if this works on the linux and apple OS
    """
    import ctypes
    screen_resolution_width = ctypes.windll.user32.GetSystemMetrics(0)
    if screen_resolution_width > 3000:  # There is probably a beter way to check if the monitor is 4K
        return width * 2
    else:
        return width


def get_file_browser_path(context):
    for area in context.screen.areas:
        if area.type == 'FILE_BROWSER':
            for space in area.spaces:
                if space.type == 'FILE_BROWSER':
                    params = space.params
                    return params.directory


def update_file_browser_space(context, path):
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
    bpy.ops.file.next()  # REFRESH FILEBROWSER INTERFACE


def get_selected_file_from_file_browser(context):
    # THIS IS USED BY THE CABINET LIBRARY
    window = context.window
    for area in window.screen.areas:
        if area.type == 'FILE_BROWSER':
            for space in area.spaces:
                if space.type == 'FILE_BROWSER':
                    return os.path.join(space.params.directory, space.params.filename)


def draw_object_info(layout, obj):
    box = layout.box()
    row = box.row()
    row.prop(obj, 'name')
    if obj.type in {'MESH', 'CURVE', 'LATTICE', 'TEXT'}:
        row.operator('fd_object.toggle_edit_mode', text="",
                     icon='EDITMODE_HLT').object_name = obj.name

    has_hook_modifier = False
    for mod in obj.modifiers:
        if mod.type == 'HOOK':
            has_hook_modifier = True

    has_shape_keys = False
    if obj.type == 'MESH':
        if obj.data.shape_keys:
            if len(obj.data.shape_keys.key_blocks) > 0:
                has_shape_keys = True

    if has_hook_modifier or has_shape_keys:
        row = box.row()
        col = row.column(align=True)
        col.label(text="Dimension")
        col.label(text=
            "X: " + str(round(sn_unit.meter_to_active_unit(obj.dimensions.x), 4)))
        col.label(text=
            "Y: " + str(round(sn_unit.meter_to_active_unit(obj.dimensions.y), 4)))
        col.label(text=
            "Z: " + str(round(sn_unit.meter_to_active_unit(obj.dimensions.z), 4)))
        col = row.column(align=True)
        col.label(text="Location")
        col.label(text="X: " + str(round(sn_unit.meter_to_active_unit(obj.location.x), 4)))
        col.label(text="Y: " + str(round(sn_unit.meter_to_active_unit(obj.location.y), 4)))
        col.label(text="Z: " + str(round(sn_unit.meter_to_active_unit(obj.location.z), 4)))
        col = row.column(align=True)
        col.label(text="Rotation")
        col.label(text="X: " + str(round(math.degrees(obj.rotation_euler.x), 4)))
        col.label(text="Y: " + str(round(math.degrees(obj.rotation_euler.y), 4)))
        col.label(text="Z: " + str(round(math.degrees(obj.rotation_euler.z), 4)))
        if has_hook_modifier:
            box.operator("fd_object.apply_hook_modifiers",
                         icon='HOOK').object_name = obj.name
        if has_shape_keys:
            box.operator("fd_object.apply_shape_keys",
                         icon='SHAPEKEY_DATA').object_name = obj.name
    else:
        if obj.type not in {'EMPTY', 'CAMERA', 'LAMP'}:
            box.label(text='Dimensions:')
            col = box.column(align=True)
            # X
            row = col.row(align=True)
            row.prop(obj, "lock_scale", index=0, text="")
            if obj.lock_scale[0]:
                row.label(text=
                    "X: " + str(round(sn_unit.meter_to_active_unit(obj.dimensions.x), 4)))
            else:
                row.prop(obj, "dimensions", index=0, text="X")
            # Y
            row = col.row(align=True)
            row.prop(obj, "lock_scale", index=1, text="")
            if obj.lock_scale[1]:
                row.label(text=
                    "Y: " + str(round(sn_unit.meter_to_active_unit(obj.dimensions.y), 4)))
            else:
                row.prop(obj, "dimensions", index=1, text="Y")
            # Z
            row = col.row(align=True)
            row.prop(obj, "lock_scale", index=2, text="")
            if obj.lock_scale[2]:
                row.label(text=
                    "Z: " + str(round(sn_unit.meter_to_active_unit(obj.dimensions.z), 4)))
            else:
                row.prop(obj, "dimensions", index=2, text="Z")

        col1 = box.row()
        if obj:
            col2 = col1.split()
            col = col2.column(align=True)
            col.label(text='Location:')
            # X
            row = col.row(align=True)
            row.prop(obj, "lock_location", index=0, text="")
            if obj.lock_location[0]:
                row.label(text=
                    "X: " + str(round(sn_unit.meter_to_active_unit(obj.location.x), 4)))
            else:
                row.prop(obj, "location", index=0, text="X")
            # Y
            row = col.row(align=True)
            row.prop(obj, "lock_location", index=1, text="")
            if obj.lock_location[1]:
                row.label(text=
                    "Y: " + str(round(sn_unit.meter_to_active_unit(obj.location.y), 4)))
            else:
                row.prop(obj, "location", index=1, text="Y")
            # Z
            row = col.row(align=True)
            row.prop(obj, "lock_location", index=2, text="")
            if obj.lock_location[2]:
                row.label(text=
                    "Z: " + str(round(sn_unit.meter_to_active_unit(obj.location.z), 4)))
            else:
                row.prop(obj, "location", index=2, text="Z")

            col2 = col1.split()
            col = col2.column(align=True)
            col.label(text='Rotation:')
            # X
            row = col.row(align=True)
            row.prop(obj, "lock_rotation", index=0, text="")
            if obj.lock_rotation[0]:
                row.label(text=
                    "X: " + str(round(math.degrees(obj.rotation_euler.x), 4)))
            else:
                row.prop(obj, "rotation_euler", index=0, text="X")
            # Y
            row = col.row(align=True)
            row.prop(obj, "lock_rotation", index=1, text="")
            if obj.lock_rotation[1]:
                row.label(text=
                    "Y: " + str(round(math.degrees(obj.rotation_euler.y), 4)))
            else:
                row.prop(obj, "rotation_euler", index=1, text="Y")
            # Z
            row = col.row(align=True)
            row.prop(obj, "lock_rotation", index=2, text="")
            if obj.lock_rotation[2]:
                row.label(text=
                    "Y: " + str(round(math.degrees(obj.rotation_euler.z), 4)))
            else:
                row.prop(obj, "rotation_euler", index=2, text="Z")

    row = box.row()
    row.prop(obj.snap, 'comment')


def draw_object_data(layout, obj):

    if obj.type == 'MESH':
        obj_bp = get_assembly_bp(obj)
        obj_wall_bp = get_wall_bp(obj)
        box = layout.box()
        row = box.row()
        row.label(text="Vertex Groups:")
        row.operator("object.vertex_group_add", icon='ZOOMIN', text="")
        row.operator("object.vertex_group_remove",
                     icon='ZOOMOUT', text="").all = False
        box.template_list("FD_UL_vgroups", "", obj, "vertex_groups",
                          obj.vertex_groups, "active_index", rows=3)
        if len(obj.vertex_groups) > 0:
            if obj.mode == 'EDIT':
                row = box.row()
                sub = row.row(align=True)
                sub.operator("object.vertex_group_assign", text="Assign")
                sub.operator("object.vertex_group_remove_from", text="Remove")
                sub = row.row(align=True)
                sub.operator("fd_object.vertex_group_select",
                             text="Select").object_name = obj.name
                sub.separator()
                sub.operator("fd_object.clear_vertex_groups",
                             text="Clear All").object_name = obj.name
            else:
                group = obj.vertex_groups.active
                if obj_bp or obj_wall_bp:
                    box.operator("fd_assembly.connect_meshes_to_hooks_in_assembly",
                                 text="Connect Hooks", icon='HOOK').object_name = obj.name
                else:
                    box.prop(group, 'name')

        key = obj.data.shape_keys
        kb = obj.active_shape_key

        box = layout.box()
        row = box.row()
        row.label(text="Shape Keys:")
        row.operator("object.shape_key_add", icon='ZOOMIN',
                     text="").from_mix = False
        row.operator("object.shape_key_remove",
                     icon='ZOOMOUT', text="").all = False
        box.template_list("MESH_UL_shape_keys", "", key,
                          "key_blocks", obj, "active_shape_key_index", rows=3)
        if kb and obj.active_shape_key_index != 0:
            box.prop(kb, 'name')
            if obj.mode != 'EDIT':
                row = box.row()
                row.prop(kb, "value")

    if obj.type == 'EMPTY':
        box = layout.box()
        box.label(text="Empty Data", icon='FONT_DATA')
        box.prop(obj, 'empty_draw_type', text='Draw Type')
        box.prop(obj, 'empty_draw_size')

    if obj.type == 'CURVE':
        box = layout.box()
        box.label(text="Curve Data", icon='CURVE_DATA')
        curve = obj.data
        box.prop(curve, "dimensions")
        box.prop(curve, "bevel_object")
        box.prop(curve, "bevel_depth")
        box.prop(curve, "extrude")
        box.prop(curve, "use_fill_caps")
        box.prop(curve.splines[0], "use_cyclic_u")

    if obj.type == 'FONT':
        text = obj.data
        box = layout.box()
        row = box.row()
        row.label(text="Font Data:")
        if obj.mode == 'OBJECT':
            row.operator("fd_object.toggle_edit_mode", text="Edit Text",
                         icon='OUTLINER_DATA_FONT').object_name = obj.name
        else:
            row.operator("fd_object.toggle_edit_mode", text="Exit Edit Mode",
                         icon='OUTLINER_DATA_FONT').object_name = obj.name
        row = box.row()
        row.template_ID(text, "font", open="font.open", unlink="font.unlink")
        row = box.row()
        row.label(text="Text Size:")
        row.prop(text, "size", text="")
        row = box.row()
        row.prop(text, "align")

        box = layout.box()
        row = box.row()
        row.label(text="3D Font:")
        row = box.row()
        row.prop(text, "extrude")
        row = box.row()
        row.prop(text, "bevel_depth")

    if obj.type == 'LAMP':
        box = layout.box()
        lamp = obj.data
        clamp = lamp.cycles
        cscene = bpy.context.scene.cycles

        emissionNode = None
        mathNode = None

        if "Emission" in lamp.node_tree.nodes:
            emissionNode = lamp.node_tree.nodes["Emission"]
        if "Math" in lamp.node_tree.nodes:
            mathNode = lamp.node_tree.nodes["Math"]

        type_box = box.box()
        type_box.label(text="Lamp Type:")
        row = type_box.row()
        row.prop(lamp, "type", expand=True)

        if lamp.type in {'POINT', 'SUN', 'SPOT'}:
            type_box.prop(lamp, "shadow_soft_size", text="Shadow Size")
        elif lamp.type == 'AREA':
            type_box.prop(lamp, "shape", text="")
            sub = type_box.column(align=True)

            if lamp.shape == 'SQUARE':
                sub.prop(lamp, "size")
            elif lamp.shape == 'RECTANGLE':
                sub.prop(lamp, "size", text="Size X")
                sub.prop(lamp, "size_y", text="Size Y")

        if cscene.progressive == 'BRANCHED_PATH':
            type_box.prop(clamp, "samples")

        if lamp.type == 'HEMI':
            type_box.label(text="Not supported, interpreted as sun lamp")

        options_box = box.box()
        options_box.label(text="Lamp Options:")
        if emissionNode:
            row = options_box.row()
            split = row.split(percentage=0.3)
            split.label(text="Lamp Color:")
            split.prop(emissionNode.inputs[0], "default_value", text="")

        row = options_box.row()
        split = row.split(percentage=0.3)
        split.label(text="Lamp Strength:")
        if mathNode:
            split.prop(mathNode.inputs[0], "default_value", text="")
        else:
            split.prop(emissionNode.inputs[1], "default_value", text="")

        row = options_box.row()
        split = row.split(percentage=0.4)
        split.prop(clamp, "cast_shadow", text="Cast Shadows")
        split.prop(clamp, "use_multiple_importance_sampling")

    if obj.type == 'CAMERA':
        box = layout.box()
        cam = obj.data
        ccam = cam.cycles
        scene = bpy.context.scene
        rd = scene.render

        box.label(text="Camera Options:")
        cam_opt_box_1 = box.box()
        row = cam_opt_box_1.row(align=True)
        row.label(text="Render Size:", icon='STICKY_UVS_VERT')
        row.prop(rd, "resolution_x", text="X")
        row.prop(rd, "resolution_y", text="Y")
        cam_opt_box_1.prop(cam, "type", expand=False, text="Camera Type")
        split = cam_opt_box_1.split()
        col = split.column()
        if cam.type == 'PERSP':
            row = col.row()
            if cam.lens_unit == 'MILLIMETERS':
                row.prop(cam, "lens")
            elif cam.lens_unit == 'FOV':
                row.prop(cam, "angle")
            row.prop(cam, "lens_unit", text="")

        if cam.type == 'ORTHO':
            col.prop(cam, "ortho_scale")

        if cam.type == 'PANO':
            engine = bpy.context.scene.render.engine
            if engine == 'CYCLES':
                ccam = cam.cycles
                col.prop(ccam, "panorama_type", text="Panorama Type")
                if ccam.panorama_type == 'FISHEYE_EQUIDISTANT':
                    col.prop(ccam, "fisheye_fov")
                elif ccam.panorama_type == 'FISHEYE_EQUISOLID':
                    row = col.row()
                    row.prop(ccam, "fisheye_lens", text="Lens")
                    row.prop(ccam, "fisheye_fov")
            elif engine == 'BLENDER_RENDER':
                row = col.row()
                if cam.lens_unit == 'MILLIMETERS':
                    row.prop(cam, "lens")
                elif cam.lens_unit == 'FOV':
                    row.prop(cam, "angle")
                row.prop(cam, "lens_unit", text="")

        row = cam_opt_box_1.row()
        split = row.split()
        col = split.column()
        col.prop(cam, "clip_start", text="Clipping Start")
        col.prop(cam, "clip_end", text="Clipping End")
        col = row.column()
        col.prop(bpy.context.scene.render, "film_transparent", text="Transparent Film")
        col.prop(bpy.context.space_data, "lock_camera")

# -------DRIVER FUNCTIONS


def get_driver(obj, data_path, array_index):
    if obj.animation_data:
        for DR in obj.animation_data.drivers:
            if DR.data_path == data_path and DR.array_index == array_index:
                return DR


def copy_drivers(obj, obj_target):
    """ This Function copies all drivers from obj
        To obj_target. This doesn't include prompt drivers
    """
    obj_target.location = obj.location
    obj_target.rotation_euler = obj.rotation_euler
    if obj.animation_data:
        for driver in obj.animation_data.drivers:
            newdriver = None
            try:
                newdriver = obj_target.driver_add(driver.data_path, driver.array_index)
            except Exception:
                try:
                    newdriver = obj_target.driver_add(driver.data_path)
                except Exception:
                    print("Unable to Copy Prompt Driver", driver.data_path)
            if newdriver:
                newdriver.driver.expression = driver.driver.expression
                newdriver.driver.type = driver.driver.type
                for var in driver.driver.variables:
                    if var.name not in newdriver.driver.variables:
                        newvar = newdriver.driver.variables.new()
                        newvar.name = var.name
                        newvar.type = var.type
                        for index, target in enumerate(var.targets):
                            newtarget = newvar.targets[index]
                            if target.id is obj:
                                newtarget.id = obj_target  # CHECK SELF REFERENCE FOR PROMPTS
                            else:
                                newtarget.id = target.id
                            newtarget.transform_space = target.transform_space
                            newtarget.transform_type = target.transform_type
                            newtarget.data_path = target.data_path


def copy_prompt_drivers(obj, obj_target):
    """
    This Function copies all drivers that are assigned to prompts from obj to obj_target.
    """
    if obj.animation_data:
        for driver in obj.animation_data.drivers:
            if 'mv.PromptPage' in driver.data_path:
                for prompt in obj_target.snap.PromptPage.COL_Prompt:
                    newdriver = None
                    if prompt.name in driver.data_path:
                        newdriver = None
                        try:
                            newdriver = obj_target.driver_add(
                                driver.data_path, driver.array_index)
                        except Exception:
                            try:
                                newdriver = obj_target.driver_add(
                                    driver.data_path)
                            except Exception:
                                print("Unable to Copy Prompt Driver",
                                      driver.data_path)
                    if newdriver:
                        newdriver.driver.expression = driver.driver.expression
                        newdriver.driver.type = driver.driver.type
                        for var in driver.driver.variables:
                            if var.name not in newdriver.driver.variables:
                                newvar = newdriver.driver.variables.new()
                                newvar.name = var.name
                                newvar.type = var.type
                                for index, target in enumerate(var.targets):
                                    newtarget = newvar.targets[index]
                                    if target.id is obj:
                                        newtarget.id = obj_target  # CHECK SELF REFERENCE FOR PROMPTS
                                    else:
                                        newtarget.id = target.id
                                    newtarget.transform_space = target.transform_space
                                    newtarget.transform_type = target.transform_type
                                    newtarget.data_path = target.data_path


def add_driver_variables(driver, variables):
    for var in variables:
        new_var = driver.driver.variables.new()
        new_var.type = 'SINGLE_PROP'
        new_var.name = var.name
        new_var.targets[0].data_path = var.data_path
        new_var.targets[0].id = var.obj


def copy_assembly_drivers(template_assembly, copy_assembly):
    copy_drivers(template_assembly.obj_bp, copy_assembly.obj_bp)
    copy_drivers(template_assembly.obj_x, copy_assembly.obj_x)
    copy_drivers(template_assembly.obj_y, copy_assembly.obj_y)
    copy_drivers(template_assembly.obj_z, copy_assembly.obj_z)
    copy_prompt_drivers(template_assembly.obj_bp, copy_assembly.obj_bp)


def draw_driver_expression(layout, driver):
    row = layout.row(align=True)
    row.prop(driver.driver, 'show_debug_info', text="", icon='OOPS')
    if driver.driver.is_valid:
        row.prop(driver.driver, "expression", text="",
                 expand=True, icon='FILE_TICK')
        if driver.mute:
            row.prop(driver, "mute", text="", icon='OUTLINER_DATA_SPEAKER')
        else:
            row.prop(driver, "mute", text="", icon='OUTLINER_OB_SPEAKER')
    else:
        row.prop(driver.driver, "expression",
                 text="", expand=True, icon='ERROR')
        if driver.mute:
            row.prop(driver, "mute", text="", icon='OUTLINER_DATA_SPEAKER')
        else:
            row.prop(driver, "mute", text="", icon='OUTLINER_OB_SPEAKER')


def draw_add_variable_operators(layout, object_name, data_path, array_index):
    # GLOBAL PROMPT
    obj = bpy.data.objects[object_name]
    obj_bp = get_assembly_bp(obj)
    box = layout.box()
    box.label("Quick Variables", icon='DRIVER')
    row = box.row()
    if obj_bp:
        props = row.operator('fd_driver.get_vars_from_object',
                             text="Group Variables", icon='DRIVER')
        props.object_name = object_name
        props.var_object_name = obj_bp.name
        props.data_path = data_path
        props.array_index = array_index


def draw_callback_px(self, context):
    font_id = 0  # XXX, need to find out how best to get this.

    offset = 10
    text_height = 10
    text_length = int(len(self.mouse_text) * 7.3)

    if self.header_text != "":
        blf.size(font_id, 17, 72)
        text_w, text_h = blf.dimensions(font_id, self.header_text)
        blf.position(
            font_id,
            context.area.width / 2 - text_w / 2, context.area.height - 50,
            0)
        blf.draw(font_id, self.header_text)

    # 50% alpha, 2 pixel width line
    if self.mouse_text != "":
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glColor4f(0.0, 0.0, 0.0, 0.5)
        bgl.glLineWidth(10)

        bgl.glBegin(bgl.GL_LINE_STRIP)
        bgl.glVertex2i(self.mouse_loc[0] - offset - 5, self.mouse_loc[1] + offset)
        bgl.glVertex2i(
            self.mouse_loc[0] + text_length - offset,
            self.mouse_loc[1] + offset)
        bgl.glVertex2i(
            self.mouse_loc[0] + text_length - offset,
            self.mouse_loc[1] + offset + text_height)
        bgl.glVertex2i(self.mouse_loc[0] - offset - 5,
                       self.mouse_loc[1] + offset + text_height)
        bgl.glEnd()

        bgl.glColor4f(1.0, 1.0, 1.0, 1.0)
        blf.position(
            font_id, self.mouse_loc[0] - offset, self.mouse_loc[1] + offset, 0)
        blf.size(font_id, 15, 72)
        blf.draw(font_id, self.mouse_text)

    # restore opengl defaults
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)


def get_class_type(cls):
    keys = cls.keys()
    # I want to find all matches, to make sure no multiples
    matches = []
    for key in keys:
        if re.fullmatch('IS_[A-Z]+', key) is not None:
            matches.append(key[3:])

    if len(matches) > 1:
        raise Exception('class has multiple IS_* attributes')

    return matches[0]


def draw_assembly_transform(context, layout, assembly, include={'DIM', 'ROT', 'LOC'}):
    unit_system = context.scene.unit_settings.system
    scene_props = context.scene.snap

    layout.prop(assembly.obj_bp, 'name')
    if 'DIM' in include:
        col = layout.column(align=True)
        col.label(text="Dimensions:")
        row1 = col.row(align=True)
        row1.prop(assembly.obj_x, 'lock_location', index=0, text="")
        if assembly.obj_x.lock_location[0]:
            x = math.fabs(assembly.obj_x.location.x)
            value = str(bpy.utils.units.to_string(unit_system, 'LENGTH', x))
            row1.label(text='X: ' + value)
        else:
            row1.prop(assembly.obj_x, 'location', index=0, text="X")
            row1.prop(assembly.obj_x, 'hide_viewport', text="")

        row1 = col.row(align=True)
        row1.prop(assembly.obj_y, 'lock_location', index=1, text="")
        if assembly.obj_y.lock_location[1]:
            y = math.fabs(assembly.obj_y.location.y)
            value = str(bpy.utils.units.to_string(unit_system, 'LENGTH', y))
            row1.label(text='Y: ' + value)
        else:
            row1.prop(assembly.obj_y, 'location', index=1, text="Y")
            row1.prop(assembly.obj_y, 'hide_viewport', text="")

        row1 = col.row(align=True)
        row1.prop(assembly.obj_z, 'lock_location', index=2, text="")
        if assembly.obj_z.lock_location[2]:
            z = math.fabs(assembly.obj_z.location.z)
            value = str(bpy.utils.units.to_string(unit_system, 'LENGTH', z))
            row1.label(text='Z: ' + value)
        else:
            row1.prop(assembly.obj_z, 'location', index=2, text="Z")
            row1.prop(assembly.obj_z, 'hide_viewport', text="")

    s_col = layout.column()

    if 'ROT' in include and 'LOC' in include:
        s_col = s_col.split()
    if 'LOC' in include:
        s_col.prop(assembly.obj_bp, 'location')
    if 'ROT' in include:
        s_col.prop(assembly.obj_bp, 'rotation_euler', text="Rotation")

def draw_enum(self, layout, enum_name, title, item_num):
    row = layout.box()
    row.label(text=title)
    row = row.split(factor=1/item_num, align=True)
    for i in range(item_num):
        row.prop_enum(self, enum_name, str(i))

def update_accordions_prompt():
    walls_sum = 0
    walls = [obj for obj in bpy.data.objects if obj.get('IS_BP_WALL')]
    walls_len = [sn_types.Assembly(obj).obj_x.location.x for obj in walls]
    for wall in walls:
        walls_sum += sn_types.Assembly(wall).obj_x.location.x
    longest_wall_inches = math.ceil(sn_unit.meter_to_inch(max(walls_len)))
    walls_qty = len(walls)
    acc_props = bpy.context.scene.snap.accordion_view
    acc_props.break_width = math.ceil(sn_unit.meter_to_inch(walls_sum))
    acc_props.intermediate_space = longest_wall_inches
    acc_props.intermediate_qty = walls_qty
