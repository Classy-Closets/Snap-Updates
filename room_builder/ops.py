import os
import math
import time

import bpy
from bpy.types import Operator

from snap import sn_types
from snap import sn_unit
from snap import sn_utils
import mathutils

from bpy.props import (StringProperty,
                       BoolProperty,
                       FloatProperty,
                       EnumProperty)

BASE_PRO_PATH = os.path.join(os.path.dirname(__file__), "Moldings", "profiles", "base")
CROWN_PRO_PATH = os.path.join(os.path.dirname(__file__), "Moldings", "profiles", "crown")

PAINT_LIBRARY_NAME = "Paint"
FLOORING_LIBRARY_NAME = "Flooring"
PAINT_CATEGORY_NAME = "Textured Wall Paint"
CARPET_CATEGORY_NAME = "Carpet"

last_wall_idx = 1


class ROOM_BUILDER_OT_Collect_Walls(Operator):
    bl_idname = "sn_roombuilder.collect_walls"
    bl_label = "Collect Walls"

    bl_options = {'UNDO'}

    add_to_project: BoolProperty(name="Add to Selected Project", default=True)
    room_name: StringProperty(name="Room Name", default="New Room")

    @classmethod
    def poll(cls, context):
        return len(context.scene.sn_roombuilder.walls) < 1

    def check(self, context):
        return True

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        props = bpy.context.scene.sn_roombuilder

        wm = context.window_manager.sn_project
        if len(wm.projects) > 0:
            project = wm.projects[wm.project_index]
            box.prop(self, "add_to_project", text="Add to Active Project: {}".format(project.name))
        else:
            box.label(text='No Projects Exist. Room will not have a project')

        if self.add_to_project:
            box.prop(self, "room_name", text="Room Name")
            box.prop(props, "room_category", text="Room Category")

    def assign_floor_material(self, context, obj):
        props = context.scene.sn_roombuilder
        if props.floor_type == 'CARPET':
            material = sn_utils.get_material("Flooring - Carpet", props.carpet_material)
        if props.floor_type == 'WOOD':
            material = sn_utils.get_material("Flooring - Wood Flooring", props.wood_floor_material)
        if props.floor_type == 'TILE':
            material = sn_utils.get_material("Flooring - Tile", props.tile_material)
        if material:
            bpy.ops.sn_object.unwrap_mesh(object_name=obj.name)
            bpy.ops.sn_object.add_material_slot(object_name=obj.name)
            for i, mat in enumerate(obj.material_slots):
                mat.material = material

    def assign_wall_material(self, context, obj):

        props = context.scene.sn_roombuilder
        material = sn_utils.get_material("Textured Wall Paint", props.wall_material)
        if material:
            bpy.ops.sn_object.unwrap_mesh(object_name=obj.name)
            bpy.ops.sn_object.add_material_slot(object_name=obj.name)
            for i, mat in enumerate(obj.material_slots):
                mat.material = material

    def execute(self, context):
        global last_wall_idx
        props = context.scene.sn_roombuilder
        snap_props = context.scene.snap

        for old_wall in props.walls:
            props.walls.remove(0)

        bpy.ops.sn_object.draw_floor_plane()
        obj_floor = context.active_object
        obj_floor.name = "Floor"
        obj_floor.snap.name_object = "Floor"
        obj_floor.sn_roombuilder.is_floor = True
        self.assign_floor_material(context, obj_floor)

        bpy.ops.sn_object.draw_floor_plane()
        ceiling = context.active_object
        ceiling.name = 'Ceiling'
        ceiling.snap.name_object = "Ceiling"
        ceiling.location.z = snap_props.default_wall_height
        self.assign_wall_material(context, ceiling)
        ceiling.hide_viewport = True
        ceiling.sn_roombuilder.is_ceiling = True

        bpy.ops.sn_object.add_room_light()

        for obj in context.view_layer.objects:
            if obj.get('IS_BP_WALL'):
                wall = sn_types.Wall(obj_bp=obj)
                wall.obj_bp['ID_PROMPT'] = 'room_builder.wall_prompts'
                for child in wall.obj_bp.children:
                    child["ID_PROMPT"] = wall.obj_bp["ID_PROMPT"]
                self.assign_wall_material(context, wall.get_wall_mesh())
                wall = props.walls.add()
                wall.name = obj.snap.name_object
                wall.bp_name = obj.name
            if obj.sn_roombuilder.is_floor:
                floor = props.walls.add()
                floor.name = obj.snap.name_object
                floor.bp_name = obj.name
            if obj.sn_roombuilder.is_ceiling:
                ceiling = props.walls.add()
                ceiling.name = obj.snap.name_object
                ceiling.bp_name = obj.name

        if self.add_to_project:
            bpy.ops.project_manager.add_room(room_name=self.room_name, room_category=props.room_category)

        sn_utils.update_accordions_prompt()
        last_wall_idx = 1

        return {'FINISHED'}


class ROOM_BUILDER_OT_draw_walls(Operator):
    bl_idname = "sn_roombuilder.draw_walls"
    bl_label = "Draw Walls"

    filepath: StringProperty(name="Filepath", default="Error")
    obj_bp_name: StringProperty(name="Obj Base Point Name")

    drawing_plane = None

    current_wall = None
    previous_wall = None

    starting_point = (0, 0, 0)

    assembly = None
    obj = None
    exclude_objects = []
    obj_wall_meshes = []

    typed_value = ""
    header_text = "(Esc, Right Click) = Cancel Command  :  (Left Click) = Place Wall"

    def char_from_number(self, number):
        ASCII_START = 97
        if number > 27 or number <= 0:
            return
        alphabet = [chr(ASCII_START + i).upper() for i in range(0, 26)]
        character = alphabet[number - 1]
        return character

    def set_type_value(self, event):
        if event.value == 'PRESS':
            if event.type == "ONE" or event.type == "NUMPAD_1":
                self.typed_value += "1"
            if event.type == "TWO" or event.type == "NUMPAD_2":
                self.typed_value += "2"
            if event.type == "THREE" or event.type == "NUMPAD_3":
                self.typed_value += "3"
            if event.type == "FOUR" or event.type == "NUMPAD_4":
                self.typed_value += "4"
            if event.type == "FIVE" or event.type == "NUMPAD_5":
                self.typed_value += "5"
            if event.type == "SIX" or event.type == "NUMPAD_6":
                self.typed_value += "6"
            if event.type == "SEVEN" or event.type == "NUMPAD_7":
                self.typed_value += "7"
            if event.type == "EIGHT" or event.type == "NUMPAD_8":
                self.typed_value += "8"
            if event.type == "NINE" or event.type == "NUMPAD_9":
                self.typed_value += "9"
            if event.type == "ZERO" or event.type == "NUMPAD_0":
                self.typed_value += "0"
            if event.type == "PERIOD" or event.type == "NUMPAD_PERIOD":
                last_value = self.typed_value[-1:]
                if last_value != ".":
                    self.typed_value += "."
            if event.type == 'BACK_SPACE':
                if self.typed_value != "":
                    self.typed_value = self.typed_value[:-1]

    def reset_properties(self):
        self.drawing_plane = None
        self.current_wall = None
        self.previous_wall = None
        self.starting_point = (0, 0, 0)
        self.assembly = None
        self.obj = None
        self.exclude_objects = []
        self.obj_wall_meshes = []
        self.typed_value = ''

    def get_previous_wall(self):
        # this function assumes that wall base points all have the same name
        objects = bpy.context.view_layer.objects
        wall_empties = list(filter(lambda a: a.get('IS_BP_WALL'), objects))
        if len(wall_empties) > 1:
            walls_sorted = sorted(wall_empties, key=lambda a: a.name)
            last_wall_bp = walls_sorted[-1]
            self.previous_wall = sn_types.Wall(obj_bp=last_wall_bp)

    def execute(self, context):
        self.reset_properties()
        self.create_drawing_plane(context)
        self.create_wall()
        self.get_previous_wall()
        if self.previous_wall:
            self.connect_walls()
            self.starting_point = list(self.previous_wall.obj_x.matrix_world.translation)
        context.window_manager.modal_handler_add(self)
        context.area.tag_redraw()
        return {'RUNNING_MODAL'}

    def create_wall(self):
        global last_wall_idx
        scene_props = bpy.context.scene.snap
        directory, file = os.path.split(self.filepath)
        filename, ext = os.path.splitext(file)
        wall = None
        wall = sn_types.Wall(scene_props.default_wall_depth,
                             scene_props.default_wall_height)
        wall.draw_wall()

        wall.obj_bp['ID_PROMPT'] = 'room_builder.wall_prompts'
        for child in wall.obj_bp.children:
            child["ID_PROMPT"] = wall.obj_bp["ID_PROMPT"]
        wall_letter = self.char_from_number(last_wall_idx)
        wall.set_name("Wall")
        wall.obj_bp.snap.name_object = f'Wall {wall_letter}'
        last_wall_idx += 1
        if self.current_wall:
            self.previous_wall = self.current_wall
        self.current_wall = wall
        self.current_wall.obj_x.location.x = 0
        self.set_child_properties(self.current_wall.obj_bp)

    def connect_walls(self):
        constraint_obj = self.previous_wall.obj_x
        constraint = self.current_wall.obj_bp.constraints.new('COPY_LOCATION')
        constraint.target = constraint_obj
        constraint.use_x = True
        constraint.use_y = True
        constraint.use_z = True
        constraint_obj.snap.connected_object = self.current_wall.obj_bp

    def set_child_properties(self, obj):
        if obj.type == 'EMPTY':
            obj.hide_viewport = True
        if obj.type == 'MESH':
            obj.display_type = 'WIRE'
        if obj.name != self.drawing_plane.name:
            self.exclude_objects.append(obj)
        for child in obj.children:
            self.set_child_properties(child)

    def set_placed_properties(self, obj):
        if obj.type == 'MESH':
            obj.display_type = 'TEXTURED'
            self.obj_wall_meshes.append(obj)
        for child in obj.children:
            self.set_placed_properties(child)

    def create_drawing_plane(self, context):
        bpy.ops.mesh.primitive_plane_add()
        plane = context.active_object
        plane.location = (0, 0, 0)
        self.drawing_plane = context.active_object
        self.drawing_plane.display_type = 'WIRE'
        self.drawing_plane.dimensions = (100, 100, 1)

    def modal(self, context, event):
        self.set_type_value(event)
        wall_length_text = str(sn_unit.meter_to_active_unit(round(self.current_wall.obj_x.location.x, 4)))
        wall_length_unit = '"' if context.scene.unit_settings.system == 'IMPERIAL' else 'mm'
        context.area.header_text_set(
            text=self.header_text + '   (Current Wall Length = ' + wall_length_text + wall_length_unit + ')')
        context.area.tag_redraw()
        self.mouse_x = event.mouse_x
        self.mouse_y = event.mouse_y

        selected_point, selected_obj, _ = sn_utils.get_selection_point(
            context, event, exclude_objects=self.exclude_objects)

        self.position_object(selected_point, selected_obj)
        self.set_end_angles()

        if self.event_is_place_first_point(event):
            self.starting_point = (selected_point[0],
                                   selected_point[1],
                                   selected_point[2])
            return {'RUNNING_MODAL'}

        if self.event_is_place_next_point(event):
            self.set_placed_properties(self.current_wall.obj_bp)
            self.create_wall()
            self.connect_walls()
            self.typed_value = ''
            self.starting_point = (selected_point[0],
                                   selected_point[1],
                                   selected_point[2])
            return {'RUNNING_MODAL'}

        if self.event_is_cancel_command(event):
            global last_wall_idx
            last_wall_idx -= 1
            return self.cancel_drop(context)

        if self.event_is_pass_through(event):
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}

    def event_is_place_next_point(self, event):
        if self.starting_point == ():
            return False
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            return True
        elif event.type == 'NUMPAD_ENTER' and event.value == 'PRESS':
            return True
        elif event.type == 'RET' and event.value == 'PRESS':
            return True
        else:
            return False

    def event_is_place_first_point(self, event):
        if self.starting_point != ():
            return False
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            return True
        elif event.type == 'NUMPAD_ENTER' and event.value == 'PRESS':
            return True
        elif event.type == 'RET' and event.value == 'PRESS':
            return True
        else:
            return False

    def event_is_cancel_command(self, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            return True
        else:
            return False

    def event_is_pass_through(self, event):
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return True
        else:
            return False

    def set_end_angles(self):
        if self.previous_wall and self.current_wall:
            left_angle = self.current_wall.get_prompt("Left Angle")
            prev_right_angle = self.previous_wall.get_prompt("Right Angle")

            prev_rot = round(math.degrees(self.previous_wall.obj_bp.rotation_euler.z), 0)
            rot = round(math.degrees(self.current_wall.obj_bp.rotation_euler.z), 0)
            diff = int(math.fabs(rot - prev_rot))
            if diff == 0 or diff == 180:
                left_angle.set_value(0)
                prev_right_angle.set_value(0)
            else:
                left_angle.set_value((rot - prev_rot) / 2)
                prev_right_angle.set_value((prev_rot - rot) / 2)

            self.current_wall.obj_prompts.location = self.current_wall.obj_prompts.location
            self.previous_wall.obj_prompts.location = self.previous_wall.obj_prompts.location

    def position_object(self, selected_point, selected_obj):
        if self.starting_point == ():
            self.current_wall.obj_bp.location = selected_point
        else:
            x = selected_point[0] - self.starting_point[0]
            y = selected_point[1] - self.starting_point[1]
            parent_rot = self.current_wall.obj_bp.parent.rotation_euler.z if self.current_wall.obj_bp.parent else 0
            if math.fabs(x) > math.fabs(y):
                if x > 0:
                    self.current_wall.obj_bp.rotation_euler.z = math.radians(0) + parent_rot
                else:
                    self.current_wall.obj_bp.rotation_euler.z = math.radians(180) + parent_rot
                if self.typed_value == "":
                    self.current_wall.obj_x.location.x = math.fabs(x)
                else:
                    value = eval(self.typed_value)
                    if bpy.context.scene.unit_settings.system == 'METRIC':
                        self.current_wall.obj_x.location.x = sn_unit.millimeter(float(value))
                    else:
                        self.current_wall.obj_x.location.x = sn_unit.inch(float(value))

            if math.fabs(y) > math.fabs(x):
                if y > 0:
                    self.current_wall.obj_bp.rotation_euler.z = math.radians(90) + parent_rot
                else:
                    self.current_wall.obj_bp.rotation_euler.z = math.radians(-90) + parent_rot
                if self.typed_value == "":
                    self.current_wall.obj_x.location.x = math.fabs(y)
                else:
                    value = eval(self.typed_value)
                    if bpy.context.scene.unit_settings.system == 'METRIC':
                        self.current_wall.obj_x.location.x = sn_unit.millimeter(float(value))
                    else:
                        self.current_wall.obj_x.location.x = sn_unit.inch(float(value))

    def hide_empties(self, obj):
        for child in obj.children:
            if child.type == 'EMPTY':
                child.hide_viewport = True

    def cancel_drop(self, context):
        context.area.header_text_set(None)
        if self.previous_wall:
            prev_right_angle = self.previous_wall.get_prompt("Right Angle")
            prev_right_angle.set_value(0)

        start_time = time.time()
        for obj in self.obj_wall_meshes:
            if not obj.hide_viewport:
                sn_utils.unwrap_obj(context, obj)
            self.hide_empties(obj.parent)
        print("Wall Unwrap: Draw Time --- %s seconds ---" % (time.time() - start_time))

        obj_list = []
        obj_list.append(self.drawing_plane)
        obj_list.append(self.current_wall.obj_bp)
        for child in self.current_wall.obj_bp.children:
            obj_list.append(child)
        sn_utils.delete_obj_list(obj_list)
        return {'CANCELLED'}


class ROOM_BUILDER_OT_Add_Obstacle(Operator):
    bl_idname = "sn_roombuilder.add_obstacle"
    bl_label = "Add Obstacle"
    bl_options = {'UNDO'}

    obstacle_bp_name: StringProperty(name="Obstacle BP Name",
                                     description="Pass the base point name to reposition an existing obstacle",
                                     default="")

    base_point: EnumProperty(name="Base Point",
                             items=[('TOP_LEFT', "Top Left", 'Top Left of Wall'),
                                    ('TOP_RIGHT', "Top Right", 'Top Right of Wall'),
                                    ('BOTTOM_LEFT', "Bottom Left", 'Bottom Left of Wall'),
                                    ('BOTTOM_RIGHT', "Bottom_Right", 'Bottom Right of Wall')],
                             default='BOTTOM_LEFT')

    obstacle_name: StringProperty(name="Obstacle Name",
                                  description="Enter the Name of the Obstacle",
                                  default="New Obstacle")

    obstacle_width: FloatProperty(name="Obstacle Width",
                                  description="Enter the Width of the Obstacle",
                                  default=sn_unit.inch(3),
                                  unit='LENGTH',
                                  precision=4)

    obstacle_height: FloatProperty(name="Obstacle Height",
                                   description="Enter the Height of the Obstacle",
                                   default=sn_unit.inch(4),
                                   unit='LENGTH',
                                   precision=4)

    obstacle_depth: FloatProperty(name="Obstacle Depth",
                                  description="Enter the Depth of the Obstacle",
                                  default=sn_unit.inch(1),
                                  unit='LENGTH',
                                  precision=4)

    x_location: FloatProperty(name="X Location",
                              description="Enter the X Location of the Obstacle",
                              default=sn_unit.inch(0),
                              unit='LENGTH',
                              precision=4)

    z_location: FloatProperty(name="Z Location",
                              description="Enter the Z Location of the Obstacle",
                              default=sn_unit.inch(0),
                              unit='LENGTH',
                              precision=4)

    dim_x_loc_offset: FloatProperty(name="Dimension X Location Offset",
                                    description="Enter X location dimension offset from wall",
                                    default=sn_unit.inch(6.0),
                                    unit='LENGTH',
                                    precision=4)

    dim_z_loc_offset: FloatProperty(name="Dimension Z Location Offset",
                                    description="Enter Z location dimension offset from wall",
                                    default=sn_unit.inch(9.0),
                                    unit='LENGTH',
                                    precision=4)

    obstacle = None
    dim_x_loc = None
    dim_z_loc = None
    dim_label = None
    wall = None
    wall_item = None
    click_ok = False
    modify_existing = False

    def check(self, context):
        if self.obstacle and self.wall:

            self.obstacle.obj_z.location.z = self.obstacle_height
            self.obstacle.obj_x.location.x = self.obstacle_width
            self.obstacle.obj_y.location.y = -self.obstacle_depth
            self.obstacle.obj_bp.location.y = 0

            if self.base_point == 'TOP_LEFT':
                self.obstacle.obj_bp.location.x = self.x_location
                self.obstacle.obj_bp.location.z = self.wall.obj_z.location.z - self.z_location - self.obstacle_height

                self.dim_x_loc.start_x(value=-self.obstacle.obj_bp.location.x)
                self.dim_x_loc.end_x(value=self.obstacle.obj_bp.location.x)
                self.dim_x_loc.start_z(value=(self.wall.obj_z.location.z
                                              - self.obstacle.obj_bp.location.z
                                              + self.dim_x_loc_offset))

                self.dim_z_loc.start_x(value=-self.obstacle.obj_bp.location.x - self.dim_z_loc_offset)
                self.dim_z_loc.start_z(value=self.wall.obj_z.location.z - self.obstacle.obj_bp.location.z)
                self.dim_z_loc.end_z(value=-(self.wall.obj_z.location.z
                                             - self.obstacle.obj_bp.location.z
                                             - self.obstacle_height))

            if self.base_point == 'TOP_RIGHT':
                self.obstacle.obj_bp.location.x = self.wall.obj_x.location.x - self.x_location - self.obstacle_width
                self.obstacle.obj_bp.location.z = self.wall.obj_z.location.z - self.z_location - self.obstacle_height

                self.dim_x_loc.start_x(value=self.obstacle_width)
                self.dim_x_loc.end_x(value=self.wall.obj_x.location.x
                                     - self.obstacle.obj_bp.location.x
                                     - self.obstacle_width)
                self.dim_x_loc.start_z(value=self.wall.obj_z.location.z
                                       - self.obstacle.obj_bp.location.z
                                       + self.dim_x_loc_offset)

                self.dim_z_loc.start_x(value=self.wall.obj_x.location.x
                                       - self.obstacle.obj_bp.location.x
                                       + self.dim_z_loc_offset)
                self.dim_z_loc.start_z(value=self.wall.obj_z.location.z - self.obstacle.obj_bp.location.z)
                self.dim_z_loc.end_z(value=-(self.wall.obj_z.location.z
                                     - self.obstacle.obj_bp.location.z
                                     - self.obstacle_height))

            if self.base_point == 'BOTTOM_LEFT':
                self.obstacle.obj_bp.location.x = self.x_location
                self.obstacle.obj_bp.location.z = self.z_location

                self.dim_x_loc.start_x(value=-self.obstacle.obj_bp.location.x)
                self.dim_x_loc.end_x(value=self.obstacle.obj_bp.location.x)
                self.dim_x_loc.start_z(value=-self.obstacle.obj_bp.location.z - self.dim_x_loc_offset)

                self.dim_z_loc.start_x(value=-self.obstacle.obj_bp.location.x - self.dim_z_loc_offset)
                self.dim_z_loc.start_z(value=0)
                self.dim_z_loc.end_z(value=-self.obstacle.obj_bp.location.z)                

            if self.base_point == 'BOTTOM_RIGHT':
                self.obstacle.obj_bp.location.x = self.wall.obj_x.location.x - self.x_location - self.obstacle_width
                self.obstacle.obj_bp.location.z = self.z_location

                self.dim_x_loc.start_x(value=self.obstacle_width)
                self.dim_x_loc.end_x(value=self.wall.obj_x.location.x
                                     - self.obstacle.obj_bp.location.x
                                     - self.obstacle_width)
                self.dim_x_loc.start_z(value=-self.obstacle.obj_bp.location.z - self.dim_x_loc_offset)

                self.dim_z_loc.start_x(value=self.wall.obj_x.location.x
                                       - self.obstacle.obj_bp.location.x
                                       + self.dim_z_loc_offset)
                self.dim_z_loc.start_z(value=0)
                self.dim_z_loc.end_z(value=-self.obstacle.obj_bp.location.z)

        return True

    def cancel(self, context):
        self.set_draw_type(bpy.context, 'TEXTURED')

        if not self.modify_existing:
            sn_utils.delete_object_and_children(self.obstacle.obj_bp)
        else:
            for obstacle in self.wall_item.obstacles:
                if obstacle.bp_name == self.obstacle_bp_name:
                    obstacle.base_point = self.base_point

            self.cage.show_in_front = False
            self.cage.display_type = 'TEXTURED'

    def set_draw_type(self, context, draw_type='WIRE'):
        for obj in context.scene.view_layers[0].objects:
            if obj.get('IS_CAGE'):
                continue
            if obj.parent:
                if obj.parent.name == self.wall.obj_bp.name:
                    pass
                else:
                    obj.display_type = draw_type
        if self.obstacle:
            for child in self.obstacle.obj_bp.children:
                child.display_type = 'WIRE'

    def invoke(self, context, event):
        wm = context.window_manager
        if bpy.context.scene.name != bpy.data.scenes[0].name:
            bpy.ops.snap.message_box(
                'INVOKE_DEFAULT',
                message="You can only create objects in the main scene")
            return {'CANCELLED'}
        self.click_ok = False
        self.modify_existing = False if self.obstacle_bp_name == "" else True

        self.wall_item = context.scene.sn_roombuilder.walls[context.scene.sn_roombuilder.wall_index]
        wall_bp = context.scene.view_layers[0].objects[self.wall_item.bp_name]
        self.wall = sn_types.Wall(obj_bp=wall_bp)
        self.wall.obj_bp['ID_PROMPT'] = 'room_builder.wall_prompts'
        for child in self.wall.obj_bp.children:
            child["ID_PROMPT"] = self.wall.obj_bp["ID_PROMPT"]
        self.set_draw_type(context)

        self.obstacle_height = sn_unit.inch(4)
        self.obstacle_width = sn_unit.inch(3)
        self.x_location = 0
        self.z_location = 0

        if self.modify_existing:
            if self.obstacle_bp_name in context.scene.view_layers[0].objects:
                for obstacle in self.wall_item.obstacles:
                    if obstacle.bp_name == self.obstacle_bp_name:
                        self.base_point = obstacle.base_point
                        self.obstacle_name = obstacle.name

                obj_bp = context.scene.view_layers[0].objects[self.obstacle_bp_name]
                self.obstacle = sn_types.Assembly(obj_bp=obj_bp)
                self.obstacle_height = self.obstacle.obj_z.location.z
                self.obstacle_width = self.obstacle.obj_x.location.x
                self.obstacle_depth = math.fabs(self.obstacle.obj_y.location.y)

                if self.base_point == 'TOP_LEFT':
                    self.x_location = self.obstacle.obj_bp.location.x
                    self.z_location = (self.wall.obj_z.location.z
                                       - self.obstacle.obj_bp.location.z
                                       - self.obstacle_height)
                if self.base_point == 'TOP_RIGHT':
                    self.x_location = self.wall.obj_x.location.x - self.obstacle.obj_bp.location.x - self.obstacle_width
                    self.z_location = (self.wall.obj_z.location.z
                                       - self.obstacle.obj_bp.location.z
                                       - self.obstacle_height)
                if self.base_point == 'BOTTOM_LEFT':
                    self.x_location = self.obstacle.obj_bp.location.x
                    self.z_location = self.obstacle.obj_bp.location.z
                if self.base_point == 'BOTTOM_RIGHT':
                    self.x_location = self.wall.obj_x.location.x - self.obstacle.obj_bp.location.x - self.obstacle_width
                    self.z_location = self.obstacle.obj_bp.location.z

                sn_utils.delete_object_and_children(obj_bp)

        self.obstacle = sn_types.Assembly()
        self.obstacle.create_assembly()
        self.obstacle.obj_bp['IS_OBSTACLE'] = True
        cage = self.obstacle.get_cage()
        cage.select_set(True)
        cage.show_in_front = True
        self.cage = cage
        self.obstacle.obj_x.hide_viewport = True
        self.obstacle.obj_y.hide_viewport = True
        self.obstacle.obj_z.hide_viewport = True
        self.obstacle.obj_bp.parent = self.wall.obj_bp
        self.obstacle.obj_x.location.x = self.obstacle_width
        self.obstacle.obj_y.location.y = self.wall.obj_y.location.y + sn_unit.inch(2)
        self.obstacle.obj_z.location.z = self.obstacle_height
        self.obstacle.obj_bp.location.y = 0
        self.obstacle.draw_as_hidden_line()

        Width = self.obstacle.obj_x.snap.get_var('location.x', 'Width')

        self.dim_label = sn_types.Dimension()
        self.dim_label.parent(self.obstacle.obj_bp)
        self.dim_label.start_z(value=sn_unit.inch(.5))
        self.dim_label.start_x('Width/2', [Width])
        self.dim_label.set_label(self.obstacle_name)

        self.dim_x_loc = sn_types.Dimension()
        self.dim_x_loc.parent(self.obstacle.obj_bp)

        self.dim_z_loc = sn_types.Dimension()
        self.dim_z_loc.parent(self.obstacle.obj_bp)

        if self.modify_existing:
            self.obstacle.obj_bp.name = self.obstacle_bp_name

        self.check(context)

        return wm.invoke_props_dialog(self, width=400)

    def execute(self, context):
        self.click_ok = True
        self.dim_label.set_label(self.obstacle_name)

        if not self.modify_existing:
            self.obstacle.obj_bp.snap.name_object = self.obstacle_name
            str_obstacle_index = str(len(self.wall_item.obstacles))
            obj_type = sn_utils.get_class_type(self.obstacle.obj_bp)

            self.obstacle.obj_bp.name = "{}.{}.{}".format(obj_type,
                                                          str_obstacle_index,
                                                          self.obstacle_name)

            self.wall_item.add_obstacle(self.obstacle, self.base_point)

        else:
            for obstacle in self.wall_item.obstacles:
                if obstacle.bp_name == self.obstacle_bp_name:
                    obstacle.name = self.obstacle_name
                    old_name = self.obstacle.obj_bp.name.split(".")[-1]
                    new_name = self.obstacle.obj_bp.name.replace(old_name, self.obstacle_name)
                    self.obstacle.obj_bp.name = new_name
                    obstacle.bp_name = self.obstacle.obj_bp.name
                    obstacle.base_point = self.base_point

        self.obstacle_name = "New Obstacle"
        self.obstacle_bp_name = ""
        self.set_draw_type(bpy.context, 'TEXTURED')
        self.cage.show_in_front = False
        self.cage.display_type = 'TEXTURED'

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()

        box.prop(self, "obstacle_name")

        col = box.column(align=False)

        row = col.row(align=True)
        row.prop_enum(self, "base_point", 'TOP_LEFT', icon='TRIA_LEFT', text="Top Left")
        row.prop_enum(self, "base_point", 'TOP_RIGHT', icon='TRIA_RIGHT', text="Top Right")
        row = col.row(align=True)
        row.prop_enum(self, "base_point", 'BOTTOM_LEFT', icon='TRIA_LEFT', text="Bottom Left")
        row.prop_enum(self, "base_point", 'BOTTOM_RIGHT', icon='TRIA_RIGHT', text="Bottom Right")

        row = col.row()
        row.label(text="Obstacle Width:")
        row.prop(self, "obstacle_width", text="")

        row = col.row()
        row.label(text="Obstacle Height:")
        row.prop(self, "obstacle_height", text="")

        row = col.row()
        row.label(text="Obstacle Depth:")
        row.prop(self, "obstacle_depth", text="")

        row = col.row()
        row.label(text="Obstacle X Location:")
        row.prop(self, "x_location", text="")

        row = col.row()
        row.label(text="Obstacle Z Location:")
        row.prop(self, "z_location", text="")


class ROOM_BUILDER_OT_Add_Floor_Obstacle(Operator):
    bl_idname = "sn_roombuilder.add_floor_obstacle"
    bl_label = "Add Floor or Ceiling Obstacle"

    bl_options = {'UNDO'}

    obstacle_bp_name: StringProperty(name="Obstacle BP Name",
                                     description="Pass the base point name to reposition an existing obstacle",
                                     default="")

    base_point: EnumProperty(name="Base Point",
                             items=[('FRONT_LEFT', "Front Left", 'Front Left of Room'),
                                    ('FRONT_RIGHT', "Front Right", 'Front Right of Room'),
                                    ('BACK_LEFT', "Back Left", 'Back Left of Room'),
                                    ('BACK_RIGHT', "Back", 'Back Right of Room')],
                             default='FRONT_LEFT')

    obstacle_name: StringProperty(name="Obstacle Name",
                                  description="Enter the Name of the Obstacle",
                                  default="New Obstacle")

    obstacle_width: FloatProperty(name="Obstacle Width",
                                  description="Enter the Width of the Obstacle",
                                  default=sn_unit.inch(3),
                                  unit='LENGTH',
                                  precision=4)

    obstacle_depth: FloatProperty(name="Obstacle Depth",
                                  description="Enter the Depth of the Obstacle",
                                  default=sn_unit.inch(4),
                                  unit='LENGTH',
                                  precision=4)

    obstacle_height: FloatProperty(name="Obstacle Height",
                                   description="Enter the Height of the Obstacle",
                                   default=sn_unit.inch(1),
                                   unit='LENGTH',
                                   precision=4)

    x_location: FloatProperty(name="X Location",
                              description="Enter the X Location of the Obstacle",
                              default=sn_unit.inch(0),
                              unit='LENGTH',
                              precision=4)

    y_location: FloatProperty(name="Y Location",
                              description="Enter the Y Location of the Obstacle",
                              default=sn_unit.inch(0),
                              unit='LENGTH',
                              precision=4)

    obstacle = None
    dim_label = None
    plane = None
    wall_item = None
    click_ok = False
    modify_existing = False

    def check(self, context):
        if self.obstacle and self.plane:

            self.obstacle.obj_bp.location.z = 0
            self.obstacle.obj_y.location.y = self.obstacle_depth
            self.obstacle.obj_x.location.x = self.obstacle_width
            if self.plane.sn_roombuilder.is_ceiling:
                self.obstacle.obj_z.location.z = -self.obstacle_height
            else:
                self.obstacle.obj_z.location.z = self.obstacle_height

            if self.base_point == 'FRONT_LEFT':
                self.obstacle.obj_bp.location.x = self.x_location
                self.obstacle.obj_bp.location.y = self.y_location
            if self.base_point == 'FRONT_RIGHT':
                self.obstacle.obj_bp.location.x = self.plane.dimensions.x - self.x_location - self.obstacle_width
                self.obstacle.obj_bp.location.y = self.y_location
            if self.base_point == 'BACK_LEFT':
                self.obstacle.obj_bp.location.x = self.x_location
                self.obstacle.obj_bp.location.y = self.plane.dimensions.y - self.y_location - self.obstacle_depth
            if self.base_point == 'BACK_RIGHT':
                self.obstacle.obj_bp.location.x = self.plane.dimensions.x - self.x_location - self.obstacle_width
                self.obstacle.obj_bp.location.y = self.plane.dimensions.y - self.y_location - self.obstacle_depth

        return True

    def cancel(self, context):
        self.set_draw_type(bpy.context, 'TEXTURED')

        if not self.click_ok:
            if not self.modify_existing:
                sn_utils.delete_object_and_children(self.obstacle.obj_bp)
            else:
                for obstacle in self.wall_item.obstacles:
                    if obstacle.bp_name == self.obstacle_bp_name:
                        obstacle.base_point = self.base_point

        self.cage.show_in_front = False
        self.cage.display_type = 'TEXTURED'

    def set_draw_type(self, context, draw_type='WIRE'):
        for obj in context.view_layer.objects:
            if obj.get('IS_CAGE'):
                continue

            if obj.parent:
                if obj.parent.name == self.plane.name:
                    pass
                else:
                    obj.display_type = draw_type
        if self.obstacle:
            for child in self.obstacle.obj_bp.children:
                child.display_type = 'WIRE'

    def invoke(self, context, event):
        wm = context.window_manager
        self.click_ok = False
        self.modify_existing = False if self.obstacle_bp_name == "" else True

        self.wall_item = context.scene.sn_roombuilder.walls[context.scene.sn_roombuilder.wall_index]
        self.plane = context.view_layer.objects[self.wall_item.bp_name]
        self.set_draw_type(context)

        if self.modify_existing:
            if self.obstacle_bp_name in context.view_layer.objects:
                for obstacle in self.wall_item.obstacles:
                    if obstacle.bp_name == self.obstacle_bp_name:
                        self.base_point = obstacle.base_point
                        self.obstacle_name = obstacle.name

                obj_bp = context.view_layer.objects[self.obstacle_bp_name]
                self.obstacle = sn_types.Assembly(obj_bp=obj_bp)
                if self.plane.sn_roombuilder.is_ceiling:
                    self.obstacle_height = -self.obstacle.obj_z.location.z
                else:
                    self.obstacle_height = self.obstacle.obj_z.location.z
                self.obstacle_width = self.obstacle.obj_x.location.x
                self.obstacle_depth = self.obstacle.obj_y.location.y

                if self.base_point == 'FRONT_LEFT':
                    self.x_location = self.obstacle.obj_bp.location.x
                    self.y_location = self.obstacle.obj_bp.location.y
                if self.base_point == 'FRONT_RIGHT':
                    self.x_location = self.plane.dimensions.x - self.obstacle.obj_bp.location.x - self.obstacle_width
                    self.y_location = self.obstacle.obj_bp.location.y
                if self.base_point == 'BACK_LEFT':
                    self.x_location = self.x_location
                    self.y_location = self.plane.dimensions.y - self.obstacle.obj_bp.location.y - self.obstacle_depth
                if self.base_point == 'BACK_RIGHT':
                    self.x_location = self.plane.dimensions.x - self.obstacle.obj_bp.location.x - self.obstacle_width
                    self.y_location = self.plane.dimensions.y - self.obstacle.obj_bp.location.y - self.obstacle_depth

                sn_utils.delete_object_and_children(obj_bp)

        self.obstacle = sn_types.Assembly()
        self.obstacle.create_assembly()
        self.obstacle.obj_bp['IS_OBSTACLE'] = True
        cage = self.obstacle.get_cage()
        cage.select_set(True)
        cage.show_in_front = True
        self.cage = cage
        self.obstacle.obj_x.hide_viewport = True
        self.obstacle.obj_y.hide_viewport = True
        self.obstacle.obj_z.hide_viewport = True

        self.obstacle.obj_bp.parent = self.plane
        self.obstacle.obj_x.location.x = self.obstacle_width
        self.obstacle.obj_y.location.y = self.obstacle_depth
        if self.plane.sn_roombuilder.is_ceiling:
            self.obstacle.obj_z.location.z = -self.obstacle_height
        else:
            self.obstacle.obj_z.location.z = self.obstacle_height
        self.obstacle.obj_bp.location.y = self.y_location

        Width = self.obstacle.obj_x.snap.get_var('location.x', 'Width')

        self.dim_label = sn_types.Dimension()
        self.dim_label.parent(self.obstacle.obj_bp)
        self.dim_label.start_z(value=sn_unit.inch(.5))
        self.dim_label.start_x('Width/2', [Width])
        self.dim_label.set_label(self.obstacle_name)

        self.dim_x_loc = sn_types.Dimension()
        self.dim_x_loc.parent(self.obstacle.obj_bp)

        self.dim_z_loc = sn_types.Dimension()
        self.dim_z_loc.parent(self.obstacle.obj_bp)

        if self.modify_existing:
            self.obstacle.obj_bp.name = self.obstacle_bp_name

        self.check(context)

        return wm.invoke_props_dialog(self, width=400)

    def execute(self, context):
        self.click_ok = True
        self.dim_label.set_label(self.obstacle_name)

        if not self.modify_existing:
            self.obstacle.obj_bp.snap.name_object = self.obstacle_name
            str_obstacle_index = str(len(self.wall_item.obstacles))
            obj_type = sn_utils.get_class_type(self.obstacle.obj_bp)

            self.obstacle.obj_bp.name = "{}.{}.{}".format(obj_type,
                                                          str_obstacle_index,
                                                          self.obstacle_name)

            self.wall_item.add_obstacle(self.obstacle, self.base_point)

        else:

            for obstacle in self.wall_item.obstacles:
                if obstacle.bp_name == self.obstacle_bp_name:
                    obstacle.name = self.obstacle_name
                    old_name = self.obstacle.obj_bp.name.split(".")[-1]
                    new_name = self.obstacle.obj_bp.name.replace(old_name, self.obstacle_name)
                    self.obstacle.obj_bp.name = new_name
                    obstacle.bp_name = self.obstacle.obj_bp.name
                    obstacle.base_point = self.base_point

        self.obstacle_name = "New Obstacle"

        self.obstacle_bp_name = ""
        self.set_draw_type(bpy.context, 'TEXTURED')
        self.cage.show_in_front = False
        self.cage.display_type = 'TEXTURED'

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()

        box.prop(self, "obstacle_name")

        col = box.column(align=False)

        row = col.row(align=True)
        row.prop_enum(self, "base_point", 'BACK_LEFT', icon='TRIA_LEFT', text="Back Left")

        row.prop_enum(self, "base_point", 'BACK_RIGHT', icon='TRIA_RIGHT', text="Back Right")

        row = col.row(align=True)
        row.prop_enum(self, "base_point", 'FRONT_LEFT', icon='TRIA_LEFT', text="Front Left")

        row.prop_enum(self, "base_point", 'FRONT_RIGHT', icon='TRIA_RIGHT', text="Front Right")

        row = col.row()
        row.label(text="Obstacle Width:")
        row.prop(self, "obstacle_width", text="")

        row = col.row()
        row.label(text="Obstacle Height:")
        row.prop(self, "obstacle_height", text="")

        row = col.row()
        row.label(text="Obstacle Depth:")
        row.prop(self, "obstacle_depth", text="")

        row = col.row()
        row.label(text="Obstacle X Location:")
        row.prop(self, "x_location", text="")

        row = col.row()
        row.label(text="Obstacle Y Location:")
        row.prop(self, "y_location", text="")


class ROOM_BUILDER_OT_Build_Room(Operator):
    bl_idname = "sn_roombuilder.build_room"
    bl_label = "Build Room"

    bl_options = {'UNDO'}

    room_name: StringProperty(name="Room Name", default="New Room")

    add_to_project: BoolProperty(name="Add to Selected Project", default=True)

    back_wall_length: FloatProperty(name="Back Wall Length",
                                    description="Enter the Back Wall Length",
                                    default=sn_unit.inch(120),
                                    unit='LENGTH',
                                    precision=4)

    side_wall_length: FloatProperty(name="Side Wall Length",
                                    description="Enter the Side Wall Length",
                                    default=sn_unit.inch(120),
                                    unit='LENGTH',
                                    precision=4)

    left_return_length: FloatProperty(name="Left Return Length",
                                      description="Enter the Left Return Wall Length",
                                      default=sn_unit.inch(25),
                                      unit='LENGTH',
                                      precision=4)

    right_return_length: FloatProperty(name="Right Return Length",
                                       description="Enter the Right Return Wall Length",
                                       default=sn_unit.inch(25),
                                       unit='LENGTH',
                                       precision=4)

    wall_height: FloatProperty(name="Wall Height",
                               description="Enter the Wall Height",
                               default=sn_unit.inch(108),
                               unit='LENGTH',
                               precision=4)

    wall_thickness: FloatProperty(name="Wall Thickness",
                                  description="Enter the Wall Thickness",
                                  default=sn_unit.inch(4),
                                  unit='LENGTH',
                                  precision=4)

    opening_height: FloatProperty(name="Opening Height",
                                  description="Enter the Height of the Opening",
                                  default=sn_unit.inch(83),
                                  unit='LENGTH',
                                  precision=4)

    obstacle = None
    left_side_wall = None
    back_wall = None
    entry_wall = None
    right_side_wall = None
    door = None
    base_molding = None
    base_molding_pro = None
    crown_molding = None
    crown_molding_pro = None

    wall_mesh_objs = []

    floor = None

    clicked_ok = False

    props = None

    def check(self, context):
        self.update_wall_properties(context)
        self.set_camera_position(context)
        return True

    def set_camera_position(self, context):
        view3d = context.space_data.region_3d
        if sn_unit.meter_to_active_unit(self.back_wall_length) / 17 < 7:
            distance = 7
        elif sn_unit.meter_to_active_unit(self.back_wall_length) / 17 > 12:
            distance = 12
        else:
            distance = sn_unit.meter_to_active_unit(self.back_wall_length) / 17
        view3d.view_distance = distance
        view3d.view_location = (self.back_wall_length / 2, self.side_wall_length, 0)
        view3d.view_rotation = (.8416, .4984, -.1004, -.1824)

    def set_molding_points(self, curve, points):
        spline = curve.data.splines.new('BEZIER')
        spline.bezier_points.add(count=len(points) - 1)

        for i, point in enumerate(points):
            curve.data.splines[0].bezier_points[i].co = point

        bpy.context.view_layer.objects.active = curve

        bpy.ops.object.editmode_toggle()
        bpy.ops.curve.select_all(action='SELECT')
        bpy.ops.curve.handle_type_set(type='VECTOR')
        bpy.ops.object.editmode_toggle()

    def update_square_room(self):
        self.left_side_wall.obj_z.location.z = self.wall_height
        self.left_side_wall.obj_y.location.y = self.wall_thickness
        self.left_side_wall.obj_x.location.x = self.side_wall_length
        self.left_side_wall.obj_bp.snap.name_object = "Wall A"

        self.back_wall.obj_z.location.z = self.wall_height
        self.back_wall.obj_y.location.y = self.wall_thickness
        self.back_wall.obj_x.location.x = self.back_wall_length
        self.back_wall.obj_bp.snap.name_object = "Wall B"

        self.right_side_wall.obj_z.location.z = self.wall_height
        self.right_side_wall.obj_y.location.y = self.wall_thickness
        self.right_side_wall.obj_x.location.x = self.side_wall_length
        self.right_side_wall.obj_bp.snap.name_object = "Wall C"

        self.entry_wall.obj_z.location.z = self.wall_height
        self.entry_wall.obj_y.location.y = self.wall_thickness
        self.entry_wall.obj_x.location.x = self.back_wall_length
        self.entry_wall.obj_bp.snap.name_object = "Wall D"

        self.door.obj_bp.location.x = self.right_return_length
        self.door.obj_x.location.x = self.back_wall_length - self.right_return_length - self.left_return_length
        self.door.obj_y.location.y = self.wall_thickness + sn_unit.inch(.01)
        self.door.obj_z.location.z = self.opening_height

        self.left_side_wall.obj_z.hide_viewport = True
        self.left_side_wall.obj_y.hide_viewport = True
        self.left_side_wall.obj_x.hide_viewport = True
        self.back_wall.obj_z.hide_viewport = True
        self.back_wall.obj_y.hide_viewport = True
        self.back_wall.obj_x.hide_viewport = True
        self.right_side_wall.obj_z.hide_viewport = True
        self.right_side_wall.obj_y.hide_viewport = True
        self.right_side_wall.obj_x.hide_viewport = True
        self.entry_wall.obj_z.hide_viewport = True
        self.entry_wall.obj_y.hide_viewport = True
        self.entry_wall.obj_x.hide_viewport = True
        self.door.obj_z.hide_viewport = True
        self.door.obj_y.hide_viewport = True
        self.door.obj_x.hide_viewport = True

    def update_single_wall(self):
        self.back_wall.obj_z.location.z = self.wall_height
        self.back_wall.obj_y.location.y = self.wall_thickness
        self.back_wall.obj_x.location.x = self.back_wall_length
        self.back_wall.obj_bp.snap.name_object = "Wall A"

        self.back_wall.obj_z.hide_viewport = True
        self.back_wall.obj_y.hide_viewport = True
        self.back_wall.obj_x.hide_viewport = True

    def update_l_shape_wall(self):
        self.back_wall.obj_z.location.z = self.wall_height
        self.back_wall.obj_y.location.y = self.wall_thickness
        self.back_wall.obj_x.location.x = self.back_wall_length
        self.back_wall.obj_bp.snap.name_object = "Wall B"

        self.left_side_wall.obj_z.location.z = self.wall_height
        self.left_side_wall.obj_y.location.y = self.wall_thickness
        self.left_side_wall.obj_x.location.x = self.left_return_length
        self.left_side_wall.obj_bp.snap.name_object = "Wall A"

        self.left_side_wall.obj_z.hide_viewport = True
        self.left_side_wall.obj_y.hide_viewport = True
        self.left_side_wall.obj_x.hide_viewport = True

        self.back_wall.obj_z.hide_viewport = True
        self.back_wall.obj_y.hide_viewport = True
        self.back_wall.obj_x.hide_viewport = True

    def update_u_shape_wall(self):
        self.left_side_wall.obj_z.location.z = self.wall_height
        self.left_side_wall.obj_y.location.y = self.wall_thickness
        self.left_side_wall.obj_x.location.x = self.left_return_length
        self.left_side_wall.obj_bp.snap.name_object = "Wall A"

        self.back_wall.obj_z.location.z = self.wall_height
        self.back_wall.obj_y.location.y = self.wall_thickness
        self.back_wall.obj_x.location.x = self.back_wall_length
        self.back_wall.obj_bp.snap.name_object = "Wall B"

        self.right_side_wall.obj_z.location.z = self.wall_height
        self.right_side_wall.obj_y.location.y = self.wall_thickness
        self.right_side_wall.obj_x.location.x = self.right_return_length
        self.right_side_wall.obj_bp.snap.name_object = "Wall C"

        self.left_side_wall.obj_z.hide_viewport = True
        self.left_side_wall.obj_y.hide_viewport = True
        self.left_side_wall.obj_x.hide_viewport = True
        self.back_wall.obj_z.hide_viewport = True
        self.back_wall.obj_y.hide_viewport = True
        self.back_wall.obj_x.hide_viewport = True
        self.right_side_wall.obj_z.hide_viewport = True
        self.right_side_wall.obj_y.hide_viewport = True
        self.right_side_wall.obj_x.hide_viewport = True

    def update_wall_properties(self, context):
        if self.props.room_type == 'SQUARE':
            self.update_square_room()
        if self.props.room_type == 'LSHAPE':
            self.update_l_shape_wall()
        if self.props.room_type == 'USHAPE':
            self.update_u_shape_wall()
        if self.props.room_type == 'SINGLE':
            self.update_single_wall()

    def create_wall(self, context):
        wall = sn_types.Wall(self.wall_thickness, self.wall_height)
        wall.draw_wall()
        wall.obj_bp['ID_PROMPT'] = 'room_builder.wall_prompts'
        for child in wall.obj_bp.children:
            child["ID_PROMPT"] = wall.obj_bp["ID_PROMPT"]
        # wall.create_wall()
        # wall.build_wall_mesh()
        # wall.obj_bp.location = (0,0,0)

        return wall

    def build_sqaure_room(self, context):
        self.left_side_wall = self.create_wall(context)
        self.left_side_wall.obj_bp.rotation_euler.z = math.radians(90)
        self.back_wall = self.create_wall(context)
        self.right_side_wall = self.create_wall(context)
        self.right_side_wall.obj_bp.rotation_euler.z = math.radians(-90)
        self.entry_wall = self.create_wall(context)
        self.entry_wall.obj_bp.rotation_euler.z = math.radians(180)

        back_wall = self.back_wall.get_wall_mesh()
        self.wall_mesh_objs.append(back_wall)
        back_wall.data.vertices[1].co[0] -= self.wall_thickness

        back_wall.data.vertices[2].co[0] += self.wall_thickness

        back_wall.data.vertices[5].co[0] -= self.wall_thickness

        back_wall.data.vertices[6].co[0] += self.wall_thickness

        left_side_wall = self.left_side_wall.get_wall_mesh()
        self.wall_mesh_objs.append(left_side_wall)
        left_side_wall.data.vertices[1].co[0] -= self.wall_thickness

        left_side_wall.data.vertices[2].co[0] += self.wall_thickness

        left_side_wall.data.vertices[5].co[0] -= self.wall_thickness

        left_side_wall.data.vertices[6].co[0] += self.wall_thickness

        right_side_wall = self.right_side_wall.get_wall_mesh()
        self.wall_mesh_objs.append(right_side_wall)
        right_side_wall.data.vertices[1].co[0] -= self.wall_thickness

        right_side_wall.data.vertices[2].co[0] += self.wall_thickness

        right_side_wall.data.vertices[5].co[0] -= self.wall_thickness

        right_side_wall.data.vertices[6].co[0] += self.wall_thickness

        entry_wall = self.entry_wall.get_wall_mesh()
        self.wall_mesh_objs.append(entry_wall)
        entry_wall.data.vertices[1].co[0] -= self.wall_thickness

        entry_wall.data.vertices[2].co[0] += self.wall_thickness

        entry_wall.data.vertices[5].co[0] -= self.wall_thickness

        entry_wall.data.vertices[6].co[0] += self.wall_thickness
        bp = sn_utils.get_group(os.path.join(os.path.dirname(__file__),
                                             "Entry Doors",
                                             self.props.entry_door_fn[self.props.entry_door_type]))
        self.door = sn_types.Assembly(obj_bp=bp)
        self.door.obj_bp['dont_export'] = True
        self.door.obj_bp['property_id'] = "lm_entry_doors.entry_door_prompts"
        self.door.obj_bp['mirror_y'] = False
        self.door.obj_bp['type_group'] = 'PRODUCT'
        self.door.obj_bp['product_type'] = "Entry Door"
        self.door.obj_bp['door_type'] = self.props.entry_door_type
        self.door.obj_bp.parent = self.entry_wall.obj_bp
        # FIX
        # self.door.draw_as_hidden_line()
        objs = sn_utils.get_child_objects(self.door.obj_bp)

        for obj_bool in objs:
            obj_bool.display_type = 'TEXTURED'
            obj_bool['property_id'] = "lm_entry_doors.entry_door_prompts"
            if obj_bool.get('use_as_bool_obj'):
                mod = entry_wall.modifiers.new(obj_bool.name, 'BOOLEAN')
                mod.object = obj_bool
                mod.operation = 'DIFFERENCE'

        sn_utils.connect_objects_location(self.left_side_wall.obj_x, self.back_wall.obj_bp)
        sn_utils.connect_objects_location(self.back_wall.obj_x, self.right_side_wall.obj_bp)
        sn_utils.connect_objects_location(self.right_side_wall.obj_x, self.entry_wall.obj_bp)

    def build_single_wall(self, context):
        self.back_wall = self.create_wall(context)

    def build_l_shape_room(self, context):
        self.left_side_wall = self.create_wall(context)
        self.left_side_wall.obj_bp.rotation_euler.z = math.radians(90)
        self.back_wall = self.create_wall(context)

        back_wall = self.back_wall.get_wall_mesh()
        self.wall_mesh_objs.append(back_wall)
        back_wall.data.vertices[1].co[0] -= self.wall_thickness

        back_wall.data.vertices[5].co[0] -= self.wall_thickness

        left_side_wall = self.left_side_wall.get_wall_mesh()
        self.wall_mesh_objs.append(left_side_wall)
        left_side_wall.data.vertices[2].co[0] += self.wall_thickness

        left_side_wall.data.vertices[6].co[0] += self.wall_thickness

        sn_utils.connect_objects_location(self.left_side_wall.obj_x, self.back_wall.obj_bp)

    def build_u_shape_room(self, context):
        self.left_side_wall = self.create_wall(context)
        self.left_side_wall.obj_bp.rotation_euler.z = math.radians(90)
        self.back_wall = self.create_wall(context)
        self.right_side_wall = self.create_wall(context)
        self.right_side_wall.obj_bp.rotation_euler.z = math.radians(-90)

        back_wall = self.back_wall.get_wall_mesh()
        self.wall_mesh_objs.append(back_wall)
        back_wall.data.vertices[1].co[0] -= self.wall_thickness

        back_wall.data.vertices[2].co[0] += self.wall_thickness

        back_wall.data.vertices[5].co[0] -= self.wall_thickness

        back_wall.data.vertices[6].co[0] += self.wall_thickness

        left_side_wall = self.left_side_wall.get_wall_mesh()
        self.wall_mesh_objs.append(left_side_wall)
        left_side_wall.data.vertices[2].co[0] += self.wall_thickness

        left_side_wall.data.vertices[6].co[0] += self.wall_thickness

        right_side_wall = self.right_side_wall.get_wall_mesh()
        self.wall_mesh_objs.append(right_side_wall)
        right_side_wall.data.vertices[1].co[0] -= self.wall_thickness

        right_side_wall.data.vertices[5].co[0] -= self.wall_thickness

        sn_utils.connect_objects_location(self.left_side_wall.obj_x, self.back_wall.obj_bp)
        sn_utils.connect_objects_location(self.back_wall.obj_x, self.right_side_wall.obj_bp)

    def add_molding(self, molding_type, wall, points):
        bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=False)
        obj_curve = bpy.context.active_object
        obj_curve.modifiers.new("Edge Split", type='EDGE_SPLIT')
        obj_curve.data.splines.clear()

        # obj_curve.data.show_handles = False
        obj_curve.snap.type_mesh = 'SOLIDSTOCK'
        obj_curve.parent = wall.obj_bp

        bpy.ops.sn_object.add_material_slot(object_name=obj_curve.name)
        bpy.ops.sn_material.sync_material_slots(object_name=obj_curve.name)
        obj_curve.snap.material_slots[0].pointer_name = "Molding"
        obj_curve.data.dimensions = '2D'
        sn_utils.assign_materials_from_pointers(obj_curve)

        if molding_type == "base":
            actualHeight = self.base_molding_pro.dimensions.y
            desiredHeight = self.props.base_molding_height
            scale_factor = desiredHeight / actualHeight
            obj_curve.scale.z = scale_factor

            obj_curve.location = (0, 0, 0)
            obj_curve.data.bevel_object = self.base_molding_pro
            if hasattr(obj_curve.data, 'bevel_mode'):
                obj_curve.data.bevel_mode = 'OBJECT'
            obj_curve.snap.name_object = wall.obj_bp.snap.name_object + " Base Molding"
            obj_curve.name = wall.obj_bp.snap.name_object + " Base Molding"
            obj_curve['solid_stock'] = self.base_molding_pro.name
            self.set_molding_points(obj_curve, points)

        elif molding_type == "crown":

            actualHeight = self.crown_molding_pro.dimensions.y
            desiredHeight = self.props.crown_molding_height
            scale_factor = desiredHeight / actualHeight
            obj_curve.scale.z = scale_factor

            obj_curve.location = (0, 0, self.wall_height)
            obj_curve.data.bevel_object = self.crown_molding_pro
            if hasattr(obj_curve.data, 'bevel_mode'):
                obj_curve.data.bevel_mode = 'OBJECT'
            obj_curve.snap.name_object = wall.obj_bp.snap.name_object + " Crown Molding"
            obj_curve.name = wall.obj_bp.snap.name_object + " Crown Molding"
            obj_curve['solid_stock'] = self.crown_molding_pro.name
            self.set_molding_points(obj_curve, points)
        obj_curve['ID_PROMPT'] = 'sn_roombuilder.molding_prompts'
        return obj_curve

    def add_molding_to_room(self, molding_type='crown'):
        if self.left_side_wall:
            points = [(0, 0, 0), (self.left_side_wall.obj_x.location.x, 0, 0)]
            self.add_molding(molding_type=molding_type, wall=self.left_side_wall, points=points)

        if self.back_wall:
            points = [(0, 0, 0), (self.back_wall.obj_x.location.x, 0, 0)]
            self.add_molding(molding_type=molding_type, wall=self.back_wall, points=points)

        if self.right_side_wall:
            points = [(0, 0, 0), (self.right_side_wall.obj_x.location.x, 0, 0)]
            self.add_molding(molding_type=molding_type, wall=self.right_side_wall, points=points)

        if self.entry_wall:
            if molding_type == 'base':
                # If the base molding is being added we need to wrap around the entry way.
                # This currently only works for the square room.
                products = self.entry_wall.get_wall_groups()
                entry_door = sn_types.Assembly(obj_bp=products[0])
                points = [(0, 0, 0), (entry_door.obj_bp.location.x, 0, 0)]
                self.add_molding(molding_type=molding_type, wall=self.entry_wall, points=points)

                points = [(entry_door.obj_bp.location.x + entry_door.obj_x.location.x, 0, 0),
                          (self.entry_wall.obj_x.location.x, 0, 0)]
                self.add_molding(molding_type=molding_type, wall=self.entry_wall, points=points)
            else:
                points = [(0, 0, 0), (self.entry_wall.obj_x.location.x, 0, 0)]
                self.add_molding(molding_type=molding_type, wall=self.entry_wall, points=points)

    def invoke(self, context, event):
        self.wall_mesh_objs = []
        sn_utils.delete_obj_list(bpy.data.objects)

        self.props = bpy.context.scene.sn_roombuilder

        for old_wall in self.props.walls:
            self.props.walls.remove(0)

        self.wall_height = context.scene.snap.default_wall_height
        self.wall_thickness = context.scene.snap.default_wall_depth

        objects = bpy.data.objects

        if self.props.add_base_molding:
            if self.props.base_molding in objects:
                self.base_molding_pro = objects[self.props.base_molding]
            else:
                self.base_molding_pro = sn_utils.get_object(os.path.join(BASE_PRO_PATH,
                                                                         self.props.base_molding + ".blend"))

        if self.props.add_crown_molding:
            if self.props.crown_molding in objects:
                self.crown_molding_pro = objects[self.props.crown_molding]
            else:

                self.crown_molding_pro = sn_utils.get_object(os.path.join(CROWN_PRO_PATH,
                                                                          self.props.crown_molding + ".blend"))

        if self.props.room_type == 'SQUARE':
            self.build_sqaure_room(context)
        if self.props.room_type == 'LSHAPE':
            self.build_l_shape_room(context)
        if self.props.room_type == 'USHAPE':
            self.build_u_shape_room(context)
        if self.props.room_type == 'SINGLE':
            self.build_single_wall(context)

        self.update_wall_properties(context)
        sn_utils.update_accordions_prompt()
        self.set_camera_position(context)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)

    def finished(self):
        # Do not create room if room category not selected
        if self.props.room_category == 'Please Select':
            bpy.ops.sn_roombuilder.delete_room()
            message = "Room not created: Category not Selected"
            return bpy.ops.snap.message_box('INVOKE_DEFAULT', message=message)

        # FIX MESH SIZE FOR EDITING AFTER ROOM CREATION
        for mesh in self.wall_mesh_objs:
            bpy.ops.sn_assembly.connect_meshes_to_hooks_in_assembly(obj_name=mesh.name)

        # HIDE EMPTIES AFTER CONNECTING HOOKS
        for obj in bpy.context.view_layer.objects:
            if obj.type == 'EMPTY':
                obj.hide_viewport = True

        if self.props.add_base_molding:
            self.add_molding_to_room(molding_type="base")

        if self.props.add_crown_molding:
            self.add_molding_to_room(molding_type="crown")

        bpy.ops.sn_roombuilder.collect_walls(add_to_project=False)

        if self.add_to_project:
            bpy.ops.project_manager.add_room(room_name=self.room_name, room_category=self.props.room_category)
            bpy.context.scene.sn_roombuilder.room_name = self.room_name

    def cancel(self, context):
        bpy.ops.sn_roombuilder.delete_room()

    def execute(self, context):
        self.finished()
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()

        wm = context.window_manager.sn_project
        if len(wm.projects) > 0:
            project = wm.projects[wm.project_index]
            box.prop(self, "add_to_project", text="Add to Active Project: {}".format(project.name))

            if self.add_to_project:
                box.prop(self, "room_name", text="Room Name")

        row = box.row()
        row.prop(self.props, "room_category", text="Room Category")

        if(self.props.room_category != "Please Select"):

            if self.props.room_type == 'SQUARE':

                row = box.row()
                row.label(text="Room Length:")
                row.prop(self, "back_wall_length", text="")

                row = box.row()
                row.label(text="Room Depth:")
                row.prop(self, "side_wall_length", text="")

                row = box.row()
                row.label(text='Return Walls:')
                row.prop(self, "left_return_length", text="Left")
                row.prop(self, "right_return_length", text='Right')

                row = box.row()
                row.label(text="Opening Height:")
                row.prop(self, "opening_height", text="")

            if self.props.room_type == 'SINGLE':
                row = box.row()
                row.label(text="Wall Length:")
                row.prop(self, "back_wall_length", text="")

            if self.props.room_type == 'LSHAPE':
                row = box.row()
                row.label(text="Back Wall Length:")
                row.prop(self, "back_wall_length", text="")

                row = box.row()
                row.label(text="Left Wall Length:")
                row.prop(self, "left_return_length", text="")

            if self.props.room_type == 'USHAPE':
                row = box.row()
                row.label(text="Back Wall Length:")
                row.prop(self, "back_wall_length", text="")

                row = box.row()
                row.label(text="Left Wall Length:")
                row.prop(self, "left_return_length", text="")

                row = box.row()
                row.label(text="Right Wall Length:")
                row.prop(self, "right_return_length", text="")


class ROOM_BUILDER_OT_Delete_Obstacle(Operator):
    bl_idname = "sn_roombuilder.delete_obstacle"
    bl_label = "Delete Obstacle"
    bl_options = {'UNDO'}

    obstacle_bp_name: StringProperty(name="Obstacle BP Name",
                                     description="Pass the base point name to reposition an existing obstacle",
                                     default="")

    def execute(self, context):
        props = bpy.context.scene.sn_roombuilder
        wall = props.walls[props.wall_index]

        for index, obstacle in enumerate(wall.obstacles):
            if obstacle.bp_name == self.obstacle_bp_name:
                wall.obstacles.remove(index)

        obj_bp = context.view_layer.objects[self.obstacle_bp_name]

        sn_utils.delete_object_and_children(obj_bp)
        return {'FINISHED'}


class ROOM_BUILDER_OT_Hide_Plane(Operator):
    bl_idname = "sn_roombuilder.hide_plane"
    bl_label = "Hide Plane"

    object_name: StringProperty("Object Name", default="")

    def execute(self, context):
        if self.object_name in context.view_layer.objects:
            obj = context.view_layer.objects[self.object_name]
        else:
            obj = context.active_object

        children = sn_utils.get_child_objects(obj)

        for child in children:
            child.hide_viewport = True

        obj.hide_viewport = True

        return {'FINISHED'}


class ROOM_BUILDER_OT_Hide_Show_Wall(Operator):
    bl_idname = "sn_roombuilder.hide_show_wall"
    bl_label = "Hide Wall"

    wall_bp_name: StringProperty("Wall BP Name", default="")

    hide: BoolProperty("Hide", default=False)

    def execute(self, context):

        obj = context.view_layer.objects[self.wall_bp_name]

        wall_bp = sn_utils.get_wall_bp(obj)

        children = sn_utils.get_child_objects(wall_bp)

        for child in children:
            if child.get('IS_CAGE'):
                continue
            if child.type == 'EMPTY':
                if child.get('obj_prompts'):
                    prompt = child.snap.get_prompt('Hide')
                    if prompt:
                        prompt.set_value(self.hide)
                continue
            
            child.hide_viewport = self.hide

        wall_bp.hide_viewport = self.hide

        return {'FINISHED'}


class ROOM_BUILDER_OT_Delete_Room(Operator):
    bl_idname = "sn_roombuilder.delete_room"
    bl_label = "Delete Room"

    delete_room_file: BoolProperty(name="Delete Room File", default=False)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)

    def execute(self, context):
        if self.delete_room_file:
            bpy.ops.project_manager.delete_room("EXEC_DEFAULT")
            bpy.ops.wm.read_homefile()
        else:
            sn_utils.delete_obj_list(bpy.data.objects)
            props = context.scene.sn_roombuilder

            for old_wall in props.walls:
                props.walls.remove(0)

        return {'FINISHED'}

    def draw(self, context):
        wm = context.window_manager.sn_project
        layout = self.layout
        box = layout.box()
        if wm.current_file_project:
            box.label(text="Project: " + wm.current_file_project)
        if wm.current_file_room:
            box.label(text="Room: " + wm.current_file_room)
        box.label(text="Are you sure you want to delete this room?")


class ROOM_BUILDER_OT_draw_new_room(Operator):
    bl_idname = "sn_roombuilder.new_custom_room"
    bl_label = 'Draw New Custom Room'

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)

    def execute(self, context):
        bpy.ops.sn_roombuilder.delete_room()
        bpy.ops.sn_roombuilder.draw_walls()
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        col = box.column()

        col.label(text="Creating a new room will clear the current room from the scene.")

        col.label(text="Are you sure you want to delete the existing room?")


class ROOM_BUILDER_OT_New_Room(Operator):
    bl_idname = "sn_roombuilder.new_room"
    bl_label = "New Room"

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)

    def execute(self, context):
        bpy.ops.sn_roombuilder.delete_room()
        bpy.ops.sn_roombuilder.build_room('INVOKE_DEFAULT')
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        col = box.column()

        col.label(text="Creating a new room will clear the current room from the scene.")

        col.label(text="Are you sure you want to delete the existing room?")


class ROOM_BUILDER_OT_Show_Plane(Operator):
    bl_idname = "sn_roombuilder.show_plane"
    bl_label = "Show Plane"

    object_name: StringProperty("Object Name", default="")

    def execute(self, context):
        if self.object_name in context.view_layer.objects:
            obj = context.view_layer.objects[self.object_name]
        else:
            obj = context.active_object

        children = sn_utils.get_child_objects(obj)

        for child in children:
            if child.type != 'EMPTY':
                child.hide_viewport = False

        obj.hide_viewport = False

        return {'FINISHED'}


class ROOM_BUILDER_OT_Select_Two_Points(Operator):
    bl_idname = "sn_roombuilder.select_two_points"
    bl_label = "Select Two Points"
    bl_options = {'UNDO'}

    # # READONLY
    drawing_plane = None

    first_point = (0, 0, 0)
    second_point = (0, 0, 0)

    header_text = "Select the First Point"

    def cancel_drop(self, context, event):
        context.window.cursor_set('DEFAULT')
        sn_utils.delete_obj_list([self.drawing_plane])
        return {'FINISHED'}

    def finished(self):
        bpy.context.area.header_text_set()

    def event_is_cancel(self, event):
        if event.type == 'RIGHTMOUSE' and event.value == 'PRESS':
            return True
        elif event.type == 'ESC' and event.value == 'PRESS':
            return True
        else:
            return False

    def modal(self, context, event):
        context.window.cursor_set('PAINT_BRUSH')
        context.area.tag_redraw()
        # Pass in Drawing Plane
        selected_point, selected_obj, _ = sn_utils.get_selection_point(context,
                                                                    event,
                                                                    objects=[self.drawing_plane]
                                                                    )
        bpy.ops.object.select_all(action='DESELECT')
        if selected_obj:
            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                if self.first_point != (0, 0, 0):
                    self.second_point = selected_point

                    distance = sn_utils.calc_distance(self.first_point, self.second_point)

                    diff = context.scene.sn_roombuilder.background_image_scale / distance

                    view = context.space_data
                    for bg in view.background_images:
                        bg_size = bg.size
                        bg.size = bg_size * diff
                    return self.cancel_drop(context, event)
                else:
                    self.first_point = selected_point

        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}

        if self.event_is_cancel(event):
            return self.cancel_drop(context, event)

        return {'RUNNING_MODAL'}

    def execute(self, context):
        self.first_point = (0, 0, 0)
        self.second_point = (0, 0, 0)
        bpy.ops.mesh.primitive_plane_add()
        plane = context.active_object
        plane.location = (0, 0, 0)
        self.drawing_plane = context.active_object
        self.drawing_plane.draw_type = 'WIRE'
        self.drawing_plane.dimensions = (100, 100, 1)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class ROOM_BUILDER_OT_update_floor_material(Operator):
    bl_idname = "sn_roombuilder.update_floor_material"
    bl_label = "Update Floor Material"
    bl_options = {'UNDO'}

    def execute(self, context):
        props = context.scene.sn_roombuilder
        for obj in context.view_layer.objects:
            if obj.sn_roombuilder.is_floor:
                if props.floor_type == 'CARPET':
                    material = sn_utils.get_material("Flooring - Carpet", props.carpet_material)
                if props.floor_type == 'WOOD':
                    material = sn_utils.get_material("Flooring - Wood Flooring", props.wood_floor_material)
                if props.floor_type == 'TILE':
                    material = sn_utils.get_material("Flooring - Tile", props.tile_material)
                if material:
                    for i, mat in enumerate(obj.material_slots):
                        mat.material = material
        return {'FINISHED'}


class ROOM_BUILDER_OT_update_wall_material(Operator):
    bl_idname = "sn_roombuilder.update_wall_material"
    bl_label = "Update Wall Material"
    bl_options = {'UNDO'}

    def get_walls(self, context):
        for obj in context.view_layer.objects:
            if obj.snap.is_wall_mesh:
                yield obj

    def execute(self, context):
        props = context.scene.sn_roombuilder
        for obj in self.get_walls(context):
            material = sn_utils.get_material("Textured Wall Paint", props.wall_material)
            if material:
                for i, mat in enumerate(obj.material_slots):
                    mat.material = material
        return {'FINISHED'}


class PROMPTS_Molding(bpy.types.Operator):
    bl_idname= 'sn_roombuilder.molding_prompts'
    bl_label = 'Molding Prompts'
    bl_options = {'UNDO'}


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        self.obj = bpy.context.active_object
        if 'Base' in self.obj.name:
            self.type = 'Base Molding'
        elif 'Crown' in self.obj.name:
            self.type = 'Crown Molding'
        else:
            raise Exception('unknown type of molding selected')
        return wm.invoke_popup(self, width=480)

    def draw(self, context):
        layout = self.layout
        props = context.scene.sn_roombuilder

        box = layout
        col = box.column(align=True)
        row = col.row(align=True)
        box.label(text='Molding Height')
        if 'Crown' in self.obj.snap.name_object:
            box.prop(props, 'crown_molding_height')
        else:
            box.prop(props, 'base_molding_height')

    def check(self, context):
        props = context.scene.sn_roombuilder

        if self.type == 'Crown Molding':
            for obj in bpy.data.objects:
                if 'Crown' in obj.snap.name_object:
                    obj.dimensions.z = props.crown_molding_height
        else:
            for obj in bpy.data.objects:
                if 'Base' in obj.snap.name_object:
                    obj.dimensions.z = props.base_molding_height
        return True


class PROMPTS_OT_Wall(bpy.types.Operator):
    bl_idname = "room_builder.wall_prompts"
    bl_label = "Assembly Properties"
    bl_description = "This show the assembly properties"
    bl_options = {'UNDO'}

    assembly = None

    def check(self, context):
        for child in self.assembly.obj_bp.children:
            child["ID_PROMPT"] = self.assembly.obj_bp["ID_PROMPT"]
        return True

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        assembly_bp = sn_utils.get_assembly_bp(context.object)
        self.assembly = sn_types.Assembly(assembly_bp)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        sn_utils.draw_assembly_transform(context, layout, self.assembly, include={'ROT', 'DIM'})


classes = (
    ROOM_BUILDER_OT_draw_walls,
    ROOM_BUILDER_OT_Hide_Show_Wall,
    ROOM_BUILDER_OT_Add_Obstacle,
    ROOM_BUILDER_OT_Add_Floor_Obstacle,
    ROOM_BUILDER_OT_Build_Room,
    ROOM_BUILDER_OT_Delete_Room,
    ROOM_BUILDER_OT_New_Room,
    ROOM_BUILDER_OT_Delete_Obstacle,
    ROOM_BUILDER_OT_Hide_Plane,
    ROOM_BUILDER_OT_Show_Plane,
    ROOM_BUILDER_OT_Select_Two_Points,
    ROOM_BUILDER_OT_Collect_Walls,
    ROOM_BUILDER_OT_update_floor_material,
    ROOM_BUILDER_OT_update_wall_material,
    PROMPTS_Molding,
    PROMPTS_OT_Wall,
    ROOM_BUILDER_OT_draw_new_room
)

register, unregister = bpy.utils.register_classes_factory(classes)
