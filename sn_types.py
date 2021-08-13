import xml.etree.ElementTree as ET
import math
import bpy
from bpy.types import Operator
from snap import sn_utils, sn_unit, sn_props


class Variable():

    var_name = ""
    obj = None
    data_path = ""
    var_type = ""
    transform_space = 'WORLD_SPACE'
    transform_type = 'LOC_X'

    def __init__(self, obj, data_path, var_name, var_type='SINGLE_PROP',
                 transform_space='WORLD_SPACE', transform_type='LOC_X'):
        self.obj = obj
        self.data_path = data_path
        self.var_name = var_name
        self.var_type = var_type
        if var_type == 'TRANSFORMS':
            self.transform_space = transform_space
            self.transform_type = transform_type


class Assembly:
    coll = None
    obj_bp = None
    obj_x = None
    obj_y = None
    obj_z = None
    obj_prompts = None
    prompts = {}
    assembly_name = ""

    def __init__(self, obj_bp=None, filepath=""):
        if obj_bp:
            self.coll = bpy.context.collection
            self.obj_bp = obj_bp
            for child in obj_bp.children:
                if "obj_x" in child:
                    self.obj_x = child
                if "obj_y" in child:
                    self.obj_y = child
                if "obj_z" in child:
                    self.obj_z = child
                if "obj_prompts" in child:
                    self.obj_prompts = child

        if filepath:
            self.coll = bpy.data.scenes[0].collection

            with bpy.data.libraries.load(filepath, False, False) as (data_from, data_to):
                data_to.objects = data_from.objects

            for obj in data_to.objects:
                if "obj_bp" in obj and obj["obj_bp"]:
                    self.obj_bp = obj
                if "obj_x" in obj and obj["obj_x"]:
                    self.obj_x = obj
                if "obj_y" in obj and obj["obj_y"]:
                    self.obj_y = obj
                if "obj_z" in obj and obj["obj_z"]:
                    self.obj_z = obj
                if "obj_prompts" in obj and obj["obj_prompts"]:
                    self.obj_prompts = obj

                self.coll.objects.link(obj)

    def update_vector_groups(self):
        """
        This is used to add all of the vector groups to
        an assembly this should be called everytime a new object
        is added to an assembly.
        """
        vgroupslist = []
        objlist = []

        for child in self.obj_bp.children:
            if child.type == 'EMPTY' and 'obj_prompts' not in child:
                vgroupslist.append(child.name)
            if child.type == 'MESH':
                objlist.append(child)

        for obj in objlist:
            for vgroup in vgroupslist:
                if vgroup not in obj.vertex_groups:
                    obj.vertex_groups.new(name=vgroup)

    def create_assembly(self, assembly_name="New Assembly"):
        """
        This creates the basic structure for an assembly.
        This must be called first when creating an assembly from a script.
        """
        bpy.ops.object.select_all(action='DESELECT')

        self.coll = bpy.data.scenes[0].collection
        self.obj_bp = bpy.data.objects.new(assembly_name, None)

        self.obj_bp.location = (0, 0, 0)
        self.obj_bp["obj_bp"] = True
        self.obj_bp.empty_display_type = 'ARROWS'
        self.obj_bp.empty_display_size = .1
        self.coll.objects.link(self.obj_bp)
        self.obj_bp['IS_BP_ASSEMBLY'] = True

        self.obj_x = bpy.data.objects.new("OBJ_X", None)
        self.obj_x.location = (0, 0, 0)
        self.obj_x.parent = self.obj_bp
        self.obj_x["obj_x"] = True
        self.obj_x.empty_display_type = 'SPHERE'
        self.obj_x.empty_display_size = .1
        self.obj_x.lock_location[0] = False
        self.obj_x.lock_location[1] = True
        self.obj_x.lock_location[2] = True
        self.obj_x.lock_rotation[0] = True
        self.obj_x.lock_rotation[1] = True
        self.obj_x.lock_rotation[2] = True
        self.coll.objects.link(self.obj_x)

        self.obj_y = bpy.data.objects.new("OBJ_Y", None)
        self.obj_y.location = (0, 0, 0)
        self.obj_y.parent = self.obj_bp
        self.obj_y["obj_y"] = True
        self.obj_y.empty_display_type = 'SPHERE'
        self.obj_y.empty_display_size = .1
        self.obj_y.lock_location[0] = True
        self.obj_y.lock_location[1] = False
        self.obj_y.lock_location[2] = True
        self.obj_y.lock_rotation[0] = True
        self.obj_y.lock_rotation[1] = True
        self.obj_y.lock_rotation[2] = True
        self.coll.objects.link(self.obj_y)

        self.obj_z = bpy.data.objects.new("OBJ_Z", None)
        self.obj_z.location = (0, 0, 0)
        self.obj_z.parent = self.obj_bp
        self.obj_z["obj_z"] = True
        self.obj_z.empty_display_type = 'SINGLE_ARROW'
        self.obj_z.empty_display_size = .2
        self.obj_z.lock_location[0] = True
        self.obj_z.lock_location[1] = True
        self.obj_z.lock_location[2] = False
        self.obj_z.lock_rotation[0] = True
        self.obj_z.lock_rotation[1] = True
        self.obj_z.lock_rotation[2] = True
        self.coll.objects.link(self.obj_z)

        coll = bpy.data.scenes[0].collection
        self.obj_prompts = bpy.data.objects.new("OBJ_PROMPTS", None)
        self.obj_prompts.location = (0, 0, 0)
        self.obj_prompts.parent = self.obj_bp
        self.obj_prompts.empty_display_size = 0
        self.obj_prompts.lock_location[0] = True
        self.obj_prompts.lock_location[1] = True
        self.obj_prompts.lock_location[2] = True
        self.obj_prompts.lock_rotation[0] = True
        self.obj_prompts.lock_rotation[1] = True
        self.obj_prompts.lock_rotation[2] = True
        self.obj_prompts["obj_prompts"] = True
        coll.objects.link(self.obj_prompts)

    def create_cube(self, name="Cube", size=(0, 0, 0)):
        """ This will create a cube mesh and assign mesh hooks
        """
        # When assigning vertices to a hook
        # the transformation is made so the size must be 0
        obj_mesh = sn_utils.create_cube_mesh("Cube", size)
        self.add_object(obj_mesh)

        vgroup = obj_mesh.vertex_groups[self.obj_x.name]
        vgroup.add([2, 3, 6, 7], 1, 'ADD')

        vgroup = obj_mesh.vertex_groups[self.obj_y.name]
        vgroup.add([1, 2, 5, 6], 1, 'ADD')

        vgroup = obj_mesh.vertex_groups[self.obj_z.name]
        vgroup.add([4, 5, 6, 7], 1, 'ADD')

        hook = obj_mesh.modifiers.new('XHOOK', 'HOOK')
        hook.object = self.obj_x
        hook.vertex_indices_set([2, 3, 6, 7])

        hook = obj_mesh.modifiers.new('YHOOK', 'HOOK')
        hook.object = self.obj_y
        hook.vertex_indices_set([1, 2, 5, 6])

        hook = obj_mesh.modifiers.new('ZHOOK', 'HOOK')
        hook.object = self.obj_z
        hook.vertex_indices_set([4, 5, 6, 7])

        return obj_mesh

    def add_prompt(self, name, prompt_type, value, combobox_items=[], prompt_obj=None):
        if prompt_obj:
            prompt = prompt_obj.snap.add_prompt(prompt_type, name)
        else:
            prompt = self.obj_prompts.snap.add_prompt(prompt_type, name)

        prompt.set_value(value)
        if prompt_type == 'COMBOBOX':
            for item in combobox_items:
                i = prompt.combobox_items.add()
                i.name = item
        return prompt

    def add_opening(self):
        """
        Creates and adds an empty opening to this assembly and returns it as an Assembly.

        **Returns:** sn_types.Assembly
        """
        opening = Assembly()
        opening.create_assembly()
        opening.obj_bp.parent = self.obj_bp
        opening.obj_bp.snap.type_group = 'OPENING'
        opening.obj_bp.snap.name_object = "Opening"
        return opening

    def add_empty(self, obj_name):
        obj = bpy.data.objects.new(obj_name, None)
        self.add_object(obj)
        return obj

    def add_light(self, obj_name, light_type):
        light = bpy.data.lights.new(obj_name, light_type)
        obj = bpy.data.objects.new(obj_name, light)
        self.add_object(obj)
        return obj

    def add_object(self, obj):
        obj.location = (0, 0, 0)
        obj.parent = self.obj_bp
        col_objects = list(map(lambda a: a.name, self.coll.objects))
        if obj.name not in col_objects:
            self.coll.objects.link(obj)
        self.update_vector_groups()

    def add_prompt_obj(self, name):
        """
        Adds a prompt object to the assembly.
        Needed to avoid cyclic driver errors when using prompt variables in drivers of the same assembly.

        Parameters:
        name (str): Name for prompt object.

        Returns:
        bpy.types.Object: Prompt object.

        """

        ppt_obj = self.add_empty("OBJ_PROMPTS_{}".format(name))
        ppt_obj.location = (0, 0, 0)
        ppt_obj.empty_display_size = 0
        ppt_obj.lock_location[0] = True
        ppt_obj.lock_location[1] = True
        ppt_obj.lock_location[2] = True
        ppt_obj.lock_rotation[0] = True
        ppt_obj.lock_rotation[1] = True
        ppt_obj.lock_rotation[2] = True
        ppt_obj["obj_formula_prompts"] = True

        for coll in ppt_obj.users_collection:
            coll.objects.unlink(ppt_obj)
        m_coll = bpy.context.scene.collection
        m_coll.objects.link(ppt_obj)
        return ppt_obj

    def add_object_from_file(self, filepath):
        with bpy.data.libraries.load(filepath, False, False) as (data_from, data_to):
            data_to.objects = data_from.objects

        for obj in data_to.objects:
            self.coll.objects.link(obj)
            obj.parent = self.obj_bp
            return obj

    def add_assembly(self, assembly):
        if assembly.obj_bp is None:
            if hasattr(assembly, 'draw'):
                assembly.draw()
        assembly.obj_bp.location = (0, 0, 0)
        assembly.obj_bp.parent = self.obj_bp
        return assembly

    def hide_driver_patch(self):
        for obj in self.obj_bp.children:
            # we are adding this to allow manual hiding of object while
            # preserving the drivers
            if obj.type == 'MESH' and hasattr(obj, 'animation_data'):
                obj['hide_viewport'] = obj.hide_viewport
                driver = obj.animation_data.drivers.find('hide_viewport')
                if not driver:
                    return
                driver.expression = '({}) and '

    def add_assembly_from_file(self, filepath):
        with bpy.data.libraries.load(filepath, False, False) as (data_from, data_to):
            data_to.objects = data_from.objects

        obj_bp = None

        for obj in data_to.objects:
            if not obj.parent:
                obj_bp = obj
            self.coll.objects.link(obj)

        obj_bp.parent = self.obj_bp
        return obj_bp

    def set_name(self, name):
        self.obj_bp.name = name
        self.obj_bp.snap.name_object = name

    def get_formula_prompt(self, name):
        for child in self.obj_bp.children:
            if "obj_formula_prompts" in child:
                if name in child.snap.prompts:
                    return child.snap.prompts[name]

    def get_prompt(self, name):
        if self.obj_prompts:
            if name in self.obj_prompts.snap.prompts:
                return self.obj_prompts.snap.prompts[name]

            for calculator in self.obj_prompts.snap.calculators:
                if name in calculator.prompts:
                    return calculator.prompts[name]

            return self.get_formula_prompt(name)

    def get_calculator(self, name):
        if name in self.obj_prompts.snap.calculators:
            return self.obj_prompts.snap.calculators[name]

    def set_prompts(self):
        for key in self.prompts:
            if key in self.obj_prompts.snap.prompts:
                if key in self.obj_prompts.snap.prompts:
                    prompt = self.obj_prompts.snap.prompts[key]
                    prompt.set_value(self.prompts[key])

    def get_prompt_dict(self):
        prompt_dict = {}
        for prompt in self.obj_prompts.snap.prompts:
            prompt_dict[prompt.name] = prompt.get_value()
        return prompt_dict

    def loc_x(self, expression="", variables=[], value=0):
        if expression == "":
            self.obj_bp.location.x = value
        else:
            self.obj_bp.snap.loc_x(expression, variables)

    def loc_y(self, expression="", variables=[], value=0):
        if expression == "":
            self.obj_bp.location.y = value
        else:
            self.obj_bp.snap.loc_y(expression, variables)

    def loc_z(self, expression="", variables=[], value=0):
        if expression == "":
            self.obj_bp.location.z = value
        else:
            self.obj_bp.snap.loc_z(expression, variables)

    def rot_x(self, expression="", variables=[], value=0):
        if expression == "":
            self.obj_bp.rotation_euler.x = value
        else:
            self.obj_bp.snap.rot_x(expression, variables)

    def rot_y(self, expression="", variables=[], value=0):
        if expression == "":
            self.obj_bp.rotation_euler.y = value
        else:
            self.obj_bp.snap.rot_y(expression, variables)

    def rot_z(self, expression="", variables=[], value=0):
        if expression == "":
            self.obj_bp.rotation_euler.z = value
        else:
            self.obj_bp.snap.rot_z(expression, variables)

    def dim_x(self, expression="", variables=[], value=0):
        if expression == "":
            self.obj_x.location.x = value
        else:
            self.obj_x.snap.loc_x(expression, variables)

    def dim_y(self, expression="", variables=[], value=0):
        if expression == "":
            self.obj_y.location.y = value
        else:
            self.obj_y.snap.loc_y(expression, variables)

    def dim_z(self, expression="", variables=[], value=0):
        if expression == "":
            self.obj_z.location.z = value
        else:
            self.obj_z.snap.loc_z(expression, variables)

    def set_material_pointers(self, material_pointer_name, slot_name=""):
        """
        Sets every material slot for every mesh to the material_pointer_name.

        **Parameters:**

        * **material_pointer_name** (string, (never None)) - Name of the material pointer to assign.

        * **slot_name** (string, (optional)) - If not "" then the material_pointer_name will be assigned to the slot.

        **Returns:** None
        """
        for slot in self.obj_bp.snap.material_slots:
            if slot_name == "":
                slot.pointer_name = material_pointer_name
            elif slot_name == slot.name:
                slot.pointer_name = material_pointer_name
        for child in self.obj_bp.children:
            if child.type == 'MESH':
                if len(child.snap.material_slots) < 1:
                    bpy.ops.sn_material.add_material_pointers(object_name=child.name)
                for slot in child.snap.material_slots:
                    if slot_name == "":
                        slot.pointer_name = material_pointer_name
                    elif slot_name == slot.name:
                        slot.pointer_name = material_pointer_name

    def draw_as_hidden_line(self, bp=None):
        print('Note: Re-add draw_as_hidden_line')
        # if bp:
        #     for c in bp.children:
        #         if c.type == 'MESH':
        #             if 'IS_BP_ASSEMBLY' in c:
        #                 self.draw_as_hidden_line(bp=c)
        #             else:
        #                 for e in c.data.edges:
        #                     e.use_freestyle_mark = True
        #                 c.data.show_freestyle_edge_marks = True

        # else:
        #     for c in self.obj_bp.children:
        #         if c.type == 'MESH':
        #             if 'IS_BP_ASSEMBLY' in c:
        #                 self.draw_as_hidden_line(bp=c)
        #             else:
        #                 for e in c.data.edges:
        #                     e.use_freestyle_mark = True
        #                 c.data.show_freestyle_edge_marks = True

    def get_cage(self):
        """
        This gets the cage for an assembly. If the cage cannot be found
        then a new one is create and returned by the function.
        """
        for child in self.obj_bp.children:
            if child.get('IS_CAGE'):
                return child
        return self.build_cage()

    def build_cage(self):
        """
        This builds the cage object which is a cube that visually represents volume of the assembly.
        """
        if self.obj_bp and self.obj_x and self.obj_y and self.obj_z:
            self.obj_x.hide_viewport = False
            self.obj_y.hide_viewport = False
            self.obj_z.hide_viewport = False
            bpy.context.view_layer.update()

            size = (self.obj_x.location.x, self.obj_y.location.y, self.obj_z.location.z)
            obj_cage = sn_utils.create_cube_mesh('CAGE', size)
            obj_cage.snap.name_object = 'CAGE'
            obj_cage.location = (0, 0, 0)
            obj_cage.parent = self.obj_bp
            obj_cage['IS_CAGE'] = True
            obj_cage.snap.type = 'CAGE'

            sn_utils.create_vertex_group_for_hooks(obj_cage, [2, 3, 6, 7], 'X Dimension')
            sn_utils.create_vertex_group_for_hooks(obj_cage, [1, 2, 5, 6], 'Y Dimension')
            sn_utils.create_vertex_group_for_hooks(obj_cage, [4, 5, 6, 7], 'Z Dimension')
            sn_utils.hook_vertex_group_to_object(obj_cage, 'X Dimension', self.obj_x)
            sn_utils.hook_vertex_group_to_object(obj_cage, 'Y Dimension', self.obj_y)
            sn_utils.hook_vertex_group_to_object(obj_cage, 'Z Dimension', self.obj_z)

            self.obj_x.hide_viewport = True
            self.obj_y.hide_viewport = True
            self.obj_z.hide_viewport = True

            obj_cage.display_type = 'WIRE'
            obj_cage.hide_select = True
            obj_cage.hide_render = True
            obj_cage.lock_location = (True, True, True)
            obj_cage.lock_rotation = (True, True, True)
            obj_cage.cycles_visibility.camera = False
            obj_cage.cycles_visibility.diffuse = False
            obj_cage.cycles_visibility.glossy = False
            obj_cage.cycles_visibility.transmission = False
            obj_cage.cycles_visibility.shadow = False
            return obj_cage

    def calc_width(self):
        """
        Calculates the width of the group based on the rotation.
        Used to determine collisions for rotated groups.
        """
        return math.cos(self.obj_bp.rotation_euler.z) * self.obj_x.location.x

    def calc_depth(self):
        """
        Calculates the depth of the group based on the rotation. 
        Used to determine collisions for rotated groups.
        """
        if self.obj_bp.rotation_euler.z < 0:
            return math.fabs(self.obj_x.location.x)
        else:
            return math.fabs(self.obj_y.location.y)

    def calc_x(self):
        """
        Calculates the x location of the group based on the rotation.
        Used to determine collisions for rotated groups.
        """
        return math.sin(self.obj_bp.rotation_euler.z) * self.obj_y.location.y

    def has_height_collision(self, assembly):
        """
        Determines if this assembly will collide with the assembly that is passed in.

        **Parameters:**

        * **assembly** (Assembly, (never None)) - Assembly to test against.

        **Returns:** Bool
        """

        if self.obj_bp.matrix_world[2][3] > self.obj_z.matrix_world[2][3]:
            grp1_z_1 = self.obj_z.matrix_world[2][3]
            grp1_z_2 = self.obj_bp.matrix_world[2][3]
        else:
            grp1_z_1 = self.obj_bp.matrix_world[2][3]
            grp1_z_2 = self.obj_z.matrix_world[2][3]

        if assembly.obj_bp.matrix_world[2][3] > assembly.obj_z.matrix_world[2][3]:
            grp2_z_1 = assembly.obj_z.matrix_world[2][3]
            grp2_z_2 = assembly.obj_bp.matrix_world[2][3]
        else:
            grp2_z_1 = assembly.obj_bp.matrix_world[2][3]
            grp2_z_2 = assembly.obj_z.matrix_world[2][3]

        if grp1_z_1 >= grp2_z_1 and grp1_z_1 <= grp2_z_2:
            return True

        if grp1_z_2 >= grp2_z_1 and grp1_z_2 <= grp2_z_2:
            return True

        if grp2_z_1 >= grp1_z_1 and grp2_z_1 <= grp1_z_2:
            return True

        if grp2_z_2 >= grp1_z_1 and grp2_z_2 <= grp1_z_2:
            return True

    def has_width_collision(self, assembly):
        """
        Determines if this assembly will collide with the assembly that is passed in.

        **Parameters:**

        * **assembly** (Assembly, (never None)) - Assembly to test against.

        **Returns:** Bool
        """

        grp1_x_1 = self.obj_bp.matrix_world[0][3]
        grp1_x_2 = self.obj_x.matrix_world[0][3]

        grp2_x_1 = assembly.obj_bp.matrix_world[0][3]
        grp2_x_2 = assembly.obj_x.matrix_world[0][3]

        if grp1_x_1 >= grp2_x_1 and grp1_x_1 <= grp2_x_2:
            return True

        if grp1_x_1 <= grp2_x_1 and grp1_x_2 >= grp2_x_1:
            return True

    def get_collision_location(self, direction='LEFT'):
        wall = None
        if self.obj_bp.parent:
            wall = Wall(obj_bp=self.obj_bp.parent)
        if wall:
            list_obj_bp = wall.get_wall_groups()
            list_obj_left_bp = []
            list_obj_right_bp = []
            for index, obj_bp in enumerate(list_obj_bp):
                if obj_bp.name == self.obj_bp.name:
                    list_obj_left_bp = list_obj_bp[:index]
                    list_obj_right_bp = list_obj_bp[index + 1:]
                    break
            if direction == 'LEFT':
                list_obj_left_bp.reverse()
                for obj_bp in list_obj_left_bp:
                    prev_group = Assembly(obj_bp)
                    if self.has_height_collision(prev_group):
                        return obj_bp.location.x + prev_group.calc_width()

                # CHECK NEXT WALL
                left_wall = wall.get_connected_wall('LEFT')
                if left_wall:
                    wall_rot_z = wall.obj_bp.rotation_euler.z
                    left_wall_rot_z = left_wall.obj_bp.rotation_euler.z
                    rotation_difference = math.degrees(wall_rot_z) - math.degrees(left_wall_rot_z)
                    if rotation_difference < 0 or rotation_difference > 180:
                        list_obj_bp = left_wall.get_wall_groups()
                        for obj in list_obj_bp:
                            prev_group = Assembly(obj)
                            product_x = obj.location.x
                            product_width = prev_group.calc_width()
                            x_dist = left_wall.obj_x.location.x - (product_x + product_width)
                            product_depth = math.fabs(self.obj_y.location.y)
                            if x_dist <= product_depth:
                                if self.has_height_collision(prev_group):
                                    return prev_group.calc_depth()
                return 0

            if direction == 'RIGHT':
                for obj_bp in list_obj_right_bp:
                    next_group = Assembly(obj_bp)
                    if self.has_height_collision(next_group):
                        return obj_bp.location.x - next_group.calc_x()

                # CHECK NEXT WALL
                right_wall = wall.get_connected_wall('RIGHT')
                if right_wall:
                    wall_rot_z = wall.obj_bp.rotation_euler.z
                    right_wall_rot_z = right_wall.obj_bp.rotation_euler.z
                    rotation_difference = math.degrees(wall_rot_z) - math.degrees(right_wall_rot_z)
                    if rotation_difference > 0 or rotation_difference < -180:
                        list_obj_bp = right_wall.get_wall_groups()
                        for obj in list_obj_bp:
                            next_group = Assembly(obj)
                            product_x = obj.location.x
                            product_width = next_group.calc_width()
                            product_depth = math.fabs(self.obj_y.location.y)
                            if product_x <= product_depth:
                                if self.has_height_collision(next_group):
                                    wall_length = wall.obj_x.location.x
                                    product_depth = next_group.calc_depth()
                                    return wall_length - product_depth

                return wall.obj_x.location.x
        else:
            return 0

    def get_adjacent_assembly(self, direction='LEFT'):
        """
        Returns an adjacent assembly to this assembly on the same Wall in the direction given.
        **Parameters:**

        * **direction** (Enum in ['LEFT', 'RIGHT', 'ABOVE', 'BELOW'], (never None)) - Direction to check.

        **Returns:** Assembly
        """

        if self.obj_bp.parent:
            wall = Wall(obj_bp=self.obj_bp.parent)
        list_obj_bp = wall.get_wall_groups()
        list_obj_left_bp = []
        list_obj_right_bp = []

        list_obj_bp_z = wall.get_wall_groups(loc_sort='Z')
        list_obj_above_bp = []
        list_obj_below_bp = []

        for index, obj_bp in enumerate(list_obj_bp):
            if obj_bp.name == self.obj_bp.name:
                list_obj_left_bp = list_obj_bp[:index]
                list_obj_right_bp = list_obj_bp[index + 1:]
                break

        for index, obj_bp in enumerate(list_obj_bp_z):
            if obj_bp.name == self.obj_bp.name:
                list_obj_above_bp = list_obj_bp_z[index + 1:]
                list_obj_below_bp = list_obj_bp_z[:index]

        if direction == 'LEFT':
            list_obj_left_bp.reverse()
            for obj_bp in list_obj_left_bp:
                prev_group = Assembly(obj_bp)
                if self.has_height_collision(prev_group):
                    return Assembly(obj_bp)

        if direction == 'RIGHT':
            for obj_bp in list_obj_right_bp:
                next_group = Assembly(obj_bp)
                if self.has_height_collision(next_group):
                    return Assembly(obj_bp)

        if direction == 'ABOVE':
            for obj_bp in list_obj_above_bp:
                above_group = Assembly(obj_bp)
                if self.has_width_collision(above_group):
                    return Assembly(obj_bp)

        if direction == 'BELOW':
            for obj_bp in list_obj_below_bp:
                below_group = Assembly(obj_bp)
                if self.has_width_collision(below_group):
                    return Assembly(obj_bp)

    def lock_rot_and_scale(self, obj):
        obj.lock_rotation = (True, True, True)
        obj.lock_scale = (True, True, True)

    def set_child_properties(self, obj):
        obj["ID_PROMPT"] = self.obj_bp["ID_PROMPT"]
        if obj.type == 'MESH':
            self.lock_rot_and_scale(obj)
        for child in obj.children:
            self.set_child_properties(child)

    def update(self):
        if hasattr(self, "drop_id"):
            self.obj_bp["ID_DROP"] = self.drop_id
        if hasattr(self, "id_prompt"):
            self.obj_bp["ID_PROMPT"] = self.id_prompt
        if hasattr(self, "placement_type"):
            self.obj_bp.snap.placement_type = self.placement_type
        if self.assembly_name == "":
            self.set_name(sn_utils.get_product_class_name(self.__class__.__name__))
        else:
            self.set_name(self.assembly_name)
        self.obj_bp.snap.type_group = self.type_assembly
        self.obj_bp.snap.class_name = self.__class__.__name__
        self.set_prompts()
        for child in self.obj_bp.children:
            if child.type == 'MESH':
                self.lock_rot_and_scale(child)
            self.set_child_properties(child)


class Part(Assembly):
    """
    Part Assembly.
    """

    def assign_material(self, slot_name, material_path, material_name):
        """
        Sets the every material slot for every mesh that matches the slot_name to the material_pointer_name.

        **Parameters:**

        * **slot_name** (string, (never None)) - Name of the snap.material_slot to assign material to.

        * **material_path** (string, (never None)) - File path to retrieve material from.

        * **material_name** (string, (never None)) - Material name.

        ***Returns:*** None
        """
        material = None

        if material_name in bpy.data.materials:
            material = bpy.data.materials[material_name]
        else:
            with bpy.data.libraries.load(material_path, False, False) as (data_from, data_to):
                for mat in data_from.materials:
                    if mat == material_name:
                        data_to.materials = [mat]
                        break

            for mat in data_to.materials:
                material = mat

        for child in self.obj_bp.children:
            for index, slot in enumerate(child.snap.material_slots):
                if slot.name == slot_name:
                    slot.material_path = material_path
                    slot.item_name = material_name
                    child.material_slots[index].material = material

    def material(self, material_pointer_name):
        """
        Sets every material slot for every mesh to the material_pointer_name.

        **Parameters:**

        * **material_pointer_name** (string, (never None)) - Name of the material pointer to assign.

        **Returns:** None
        """
        for slot in self.obj_bp.snap.material_slots:
            slot.pointer_name = material_pointer_name
        for child in self.obj_bp.children:
            if child.type == 'MESH':
                for slot in child.snap.material_slots:
                    slot.pointer_name = material_pointer_name

    def cutpart(self, cutpart_name):
        """
        Assigns every mesh cut part to the cutpart_name.

        **Parameters:**

        * **cutpart_name** (string, (never None)) - Name of the material pointer to assign.

        **Returns:** None
        """
        for child in self.obj_bp.children:
            if child.type == 'MESH' and child.snap.type_mesh == 'CUTPART':
                child.snap.cutpart_name = cutpart_name

    def solid_stock(self, solid_stock_name):
        """
        Assigns the every mesh solid stock to the solid_stock_name.

        **Parameters:**

        * **solid_stock_name** (string, (never None)) - Solid stock name to assign to obj.

        **Returns:** None
        """

        for child in self.obj_bp.children:
            if child.type == 'MESH' and child.snap.type_mesh == 'SOLIDSTOCK':
                child.snap.solid_stock = solid_stock_name

    def edgebanding(self, edgebanding_name, w1=False, l1=False, w2=False, l2=False):
        """
        Assigns every mesh cut part to the edgebanding_name.

        **Parameters:**

        * **edgebanding_name** (string, (never None)) - Name of the edgepart pointer to assign.

        * **w1** (bool, (optional, default=False)) - Determines if to edgeband width 1 of the part.

        * **w2** (bool, (optional, default=False)) - Determines if to edgeband width 2 of the part.

        * **l1** (bool, (optional, default=False)) - Determines if to edgeband length 1 of the part.

        * **l2** (bool, (optional, default=False)) - Determines if to edgeband length 2 of the part.

        **Returns:** None
        """

        for child in self.obj_bp.children:
            if child.type == 'MESH' and child.snap.type_mesh == 'EDGEBANDING':
                child.snap.edgepart_name = edgebanding_name
            if child.type == 'MESH' and child.snap.type_mesh == 'CUTPART':
                child.snap.edgepart_name = edgebanding_name
                if w1:
                    child.snap.edge_w1 = edgebanding_name
                if l1:
                    child.snap.edge_l1 = edgebanding_name
                if w2:
                    child.snap.edge_w2 = edgebanding_name
                if l2:
                    child.snap.edge_l2 = edgebanding_name

    def add_machine_token(self, machining_name, machining_type, machining_face, machining_edge="1"):
        """ Returns:tuple(bpy.types.Object,properties.Machining_Token) - adds a machine token
                                                                         to the first cutpart mesh

            machining_name:string - name of the machining token

            machining_name:string - type of machining token to add

            machining_face:string - face to add the machining token to

            machining_edge:string - edge to add the machining token to
        """
        for child in self.obj_bp.children:
            if child.snap.type_mesh == 'CUTPART':
                token = child.snap.mp.add_machine_token(
                    machining_name, machining_type, machining_face, machining_edge)
                return child, token

    def get_cutparts(self):
        """ Returns:list of bpy.types.Object - gets all mesh objects that are assigned as cutparts.
        """
        cutparts = []
        for child in self.obj_bp.children:
            if child.type == 'MESH' and child.snap.type_mesh == 'CUTPART':
                cutparts.append(child)
        return cutparts

    def machine_token(self, obj, token, token_property, expression, driver_vars, index=None):
        """ Returns:None - sets a driver for a machine token that is passed in.
        """
        data_path = ""
        for m_token in obj.snap.mp.machine_tokens:
            if m_token == token:
                if index:
                    data_path = 'snap.mp.machine_tokens.["' + token.name + \
                        '"].' + token_property + '[' + str(index) + ']'
                else:
                    data_path = 'snap.mp.machine_tokens.["' + \
                        token.name + '"].' + token_property
                obj.driver_add(data_path)

        if data_path != "":
            for var in driver_vars:
                if obj.animation_data:
                    for DR in obj.animation_data.drivers:
                        if data_path in DR.data_path:
                            new_var = DR.driver.variables.new()
                            new_var.name = var.var_name
                            new_var.targets[0].data_path = var.data_path
                            new_var.targets[0].id = var.obj
                            DR.driver.expression = expression
                            break
        else:
            print("Error: '{}' not found while setting expression '{}'".format(token.name, expression))


class Material_Pointer():

    name = ""
    category_name = ""
    item_name = ""

    def __init__(self, library_path):
        self.category_name = library_path[0]
        self.item_name = library_path[1]


class Cutpart_Pointer():

    name = ""
    thickness = 0.0
    core = ""
    top = ""
    bottom = ""
    mv_pointer_name = ""

    def __init__(self, thickness, core, top, bottom, mv_pointer_name=""):
        self.thickness = thickness
        self.core = core
        self.top = top
        self.bottom = bottom
        self.mv_pointer_name = mv_pointer_name


class Edgepart_Pointer():

    name = ""
    thickness = 0.0
    material = ""
    mv_pointer_name = ""

    def __init__(self, thickness, material, mv_pointer_name=""):
        self.thickness = thickness
        self.material = material
        self.mv_pointer_name = mv_pointer_name


class Wall(Assembly):

    def __init__(self, wall_thickness=None, wall_height=None, obj_bp=None):
        if obj_bp:
            super().__init__(obj_bp=obj_bp)

        if wall_height and wall_thickness:
            self.wall_thickness = wall_thickness
            self.wall_height = wall_height

    def draw_wall(self):
        self.create_assembly("Wall")

        self.obj_bp["IS_BP_WALL"] = True

        self.obj_bp.snap.name_object = 'Wall'
        self.obj_bp['type'] = 'Wall'
        self.obj_x.location.x = sn_unit.inch(120)
        self.obj_y.location.y = self.wall_thickness
        self.obj_z.location.z = self.wall_height
        size = (0, 0, 0)

        obj_mesh = sn_utils.create_cube_mesh("Wall Mesh", size)
        obj_mesh.snap.is_wall_mesh = True
        self.add_object(obj_mesh)
        left_angle_empty = self.add_empty("Left Angle")
        right_angle_empty = self.add_empty("Right Angle")

        # Hooks
        vgroup = obj_mesh.vertex_groups[left_angle_empty.name]
        vgroup.add([1, 5], 1, 'ADD')
        vgroup = obj_mesh.vertex_groups[right_angle_empty.name]
        vgroup.add([2, 6], 1, 'ADD')
        vgroup = obj_mesh.vertex_groups[self.obj_x.name]
        vgroup.add([3, 7], 1, 'ADD')
        vgroup = obj_mesh.vertex_groups[self.obj_z.name]
        vgroup.add([4, 5, 6, 7], 1, 'ADD')

        hook = obj_mesh.modifiers.new('XHOOK', 'HOOK')
        hook.object = self.obj_x
        hook.vertex_indices_set([3, 7])
        hook = obj_mesh.modifiers.new('LEFTANGLE', 'HOOK')
        hook.object = left_angle_empty
        hook.vertex_indices_set([1, 5])
        hook = obj_mesh.modifiers.new('RIGHTANGLE', 'HOOK')
        hook.object = right_angle_empty
        hook.vertex_indices_set([2, 6])
        hook = obj_mesh.modifiers.new('ZHOOK', 'HOOK')
        hook.object = self.obj_z
        hook.vertex_indices_set([4, 5, 6, 7])

        # Drivers
        length = self.obj_x.snap.get_var('location.x', 'length')
        wall_thickness = self.obj_y.snap.get_var('location.y', 'wall_thickness')

        left_angle = self.add_prompt("Left Angle", 'ANGLE', 0)
        right_angle = self.add_prompt("Right Angle", 'ANGLE', 0)

        left_angle_var = left_angle.get_var('left_angle_var')
        right_angle_var = right_angle.get_var('right_angle_var')

        left_angle_empty.snap.loc_x(
            'tan(left_angle_var)*wall_thickness',
            [left_angle_var, wall_thickness])

        left_angle_empty.snap.loc_y('wall_thickness', [wall_thickness])

        right_angle_empty.snap.loc_x(
            'length+tan(right_angle_var)*wall_thickness',
            [length, right_angle_var, wall_thickness])

        right_angle_empty.snap.loc_y('wall_thickness', [wall_thickness])

    def get_wall_mesh(self):
        for child in self.obj_bp.children:
            if child.type == 'MESH' and len(child.data.vertices) != 1:
                return child

    def refresh_hook_modifiers(self):
        for child in self.obj_bp.children:
            if child.type == 'MESH':
                bpy.ops.sn_object.apply_hook_modifiers(object_name=child.name)
                bpy.ops.sn_assembly.connect_meshes_to_hooks_in_assembly(obj_name=child.name)

    def get_wall_groups(self, loc_sort='X'):
        """ This returns a sorted list of all of the groups base points
            parented to the wall
        """
        list_obj_bp = []
        for child in self.obj_bp.children:
            if child.get('IS_BP_ASSEMBLY'):
                list_obj_bp.append(child)
        if loc_sort == 'X':
            list_obj_bp.sort(key=lambda obj: obj.location.x, reverse=False)
        if loc_sort == 'Y':
            list_obj_bp.sort(key=lambda obj: obj.location.y, reverse=False)
        if loc_sort == 'Z':
            list_obj_bp.sort(key=lambda obj: obj.location.z, reverse=False)
        return list_obj_bp

    def get_connected_wall(self, direction):
        if direction == 'LEFT':
            for con in self.obj_bp.constraints:
                if con.type == 'COPY_LOCATION':
                    if con.target:
                        return Wall(obj_bp=con.target.parent)

        if direction == 'RIGHT':
            for obj in bpy.data.objects:
                if obj.get('IS_BP_WALL'):
                    next_wall = Wall(obj_bp=obj)
                    for con in next_wall.obj_bp.constraints:
                        if con.type == 'COPY_LOCATION':
                            if con.target == self.obj_x:
                                return next_wall


class Dimension():
    anchor = None
    end_point = None
    label = ""
    opengl_dim = None

    def __init__(self, line_only=False):
        scene = bpy.context.scene
        self.create_anchor()
        self.create_end_point()

        self.opengl_dim = self.anchor.snap.opengl_dim
        self.opengl_dim.gl_label = scene.snap.opengl_dim.gl_label
        self.opengl_dim.gl_font_size = scene.snap.opengl_dim.gl_font_size
        self.opengl_dim.line_only = line_only

    def create_anchor(self):
        context = bpy.context
        bpy.ops.object.add(type='EMPTY')
        self.anchor = context.object
        self.anchor.location = (0, 0, 0)
        self.anchor['IS_VISDIM_A'] = True
        self.anchor.snap.name_object = "Anchor"
        self.anchor.empty_display_type = 'SPHERE'
        self.anchor.empty_display_size = sn_unit.inch(1)

    def create_end_point(self):
        context = bpy.context
        bpy.ops.object.add(type='EMPTY')
        self.end_point = context.object
        self.end_point.location = (0, 0, 0)
        self.end_point['IS_VISDIM_B'] = True
        self.end_point.snap.name_object = "End Point"
        self.end_point.parent = self.anchor
        self.end_point.rotation_euler.z = math.radians(-90)
        self.end_point.empty_display_type = 'PLAIN_AXES'
        self.end_point.empty_display_size = sn_unit.inch(2)

    def parent(self, obj_bp):
        self.anchor.parent = obj_bp

    def start_x(self, expression="", driver_vars=[], value=0):
        if expression == "":
            self.anchor.location.x = value
        else:
            driver = self.anchor.driver_add('location', 0)
            sn_props.add_driver_variables(driver, driver_vars)
            driver.driver.expression = expression

    def start_y(self, expression="", driver_vars=[], value=0):
        if expression == "":
            self.anchor.location.y = value
        else:
            driver = self.anchor.driver_add('location', 1)
            sn_props.add_driver_variables(driver, driver_vars)
            driver.driver.expression = expression

    def start_z(self, expression="", driver_vars=[], value=0):
        if expression == "":
            self.anchor.location.z = value
        else:
            driver = self.anchor.driver_add('location', 2)
            sn_props.add_driver_variables(driver, driver_vars)
            driver.driver.expression = expression

    def end_x(self, expression="", driver_vars=[], value=0):
        if expression == "":
            self.end_point.location.x = value
        else:
            driver = self.end_point.driver_add('location', 0)
            sn_props.add_driver_variables(driver, driver_vars)
            driver.driver.expression = expression

    def end_y(self, expression="", driver_vars=[], value=0):
        if expression == "":
            self.end_point.location.y = value
        else:
            driver = self.end_point.driver_add('location', 1)
            sn_props.add_driver_variables(driver, driver_vars)
            driver.driver.expression = expression

    def end_z(self, expression="", driver_vars=[], value=0):
        if expression == "":
            self.end_point.location.z = value
        else:
            driver = self.end_point.driver_add('location', 2)
            sn_props.add_driver_variables(driver, driver_vars)
            driver.driver.expression = expression

    def hide(self, expression="", driver_vars=[], value=True):
        if expression == "":
            self.opengl_dim.hide = value
        else:
            driver = self.anchor.driver_add('snap.opengl_dim.hide')
            sn_props.add_driver_variables(driver, driver_vars)
            driver.driver.expression = expression

    def set_color(self, expression="", driver_vars=[], value=0):
        if expression == "":
            self.opengl_dim.gl_color = value
        else:
            driver = self.anchor.driver_add('snap.opengl_dim.gl_color')
            sn_props.add_driver_variables(driver, driver_vars)
            driver.driver.expression = expression

    def set_label(self, text, new_line=False):
        if new_line:
            self.opengl_dim.gl_label = " | " + text
        else:
            self.opengl_dim.gl_label = text

    def set_vertical_line_txt_pos(self, pos=''):
        assert pos in ('LEFT', 'RIGHT'), "Invalid arg - '{}'".format(pos)
        self.opengl_dim.v_line_text_placement = pos

    def set_horizontal_line_txt_pos(self, pos=''):
        assert pos in ('TOP', 'BOTTOM'), "Invalid arg - '{}'".format(pos)
        self.opengl_dim.h_line_text_placement = pos

    def set_text_offset_x(self, expression="", driver_vars=[], value=0):
        if expression == "":
            self.opengl_dim.gl_text_x = value
        else:
            driver = self.anchor.driver_add('cabinetlib.opengl_dim.gl_text_x')
            sn_props.add_driver_variables(driver, driver_vars)
            driver.driver.expression = expression

    def set_text_offset_y(self, expression="", driver_vars=[], value=0):
        if expression == "":
            self.opengl_dim.gl_text_y = value
        else:
            driver = self.anchor.driver_add('cabinetlib.opengl_dim.gl_text_y')
            sn_props.add_driver_variables(driver, driver_vars)
            driver.driver.expression = expression


class Line(Dimension):
    length = 0
    rotation = (0, 0, 0)
    axis = 'Z'
    width = 2

    def __init__(self, length=length, rotation=rotation, axis=axis,
                 width=width):
        self.create_anchor()
        self.create_end_point()
        self.set_length(length, axis)
        self.set_rotation(rotation)
        self.opengl_dim = self.anchor.snap.opengl_dim
        self.opengl_dim.line_only = True
        self.opengl_dim.gl_width = width

    def set_length(self, length, axis):
        length_axis = [length * (a == axis) for a in ('X', 'Y', 'Z')]
        self.end_point.location = length_axis

    def set_rotation(self, rotation):
        self.anchor.rotation_euler = [math.radians(r) for r in rotation]


class MV_XML():

    tree = None

    def __init__(self):
        pass

    def create_tree(self):
        root = ET.Element('Root', {'Application': 'Microvellum', 'ApplicationVersion': '7.0'})
        self.tree = ET.ElementTree(root)
        return root

    def add_element(self, root, elm_name, attrib_name=""):
        if attrib_name == "":
            elm = ET.Element(elm_name)
        else:
            elm = ET.Element(elm_name, {'Name': attrib_name})
        root.append(elm)
        return elm

    def add_element_with_text(self, root, elm_name, text):
        field = ET.Element(elm_name)
        field.text = text
        root.append(field)

    def format_xml_file(self, path):
        """ This makes the xml file readable as a txt doc.
            For some reason the xml.toprettyxml() function
            adds extra blank lines. This makes the xml file
            unreadable. This function just removes
            all of the blank lines.
            arg1: path to xml file
        """
        from xml.dom.minidom import parse

        xml = parse(path)
        pretty_xml = xml.toprettyxml()

        file = open(path, 'w')
        file.write(pretty_xml)
        file.close()

        cleaned_lines = []
        with open(path, "r") as f:
            lines = f.readlines()
            for l in lines:
                l.strip()
                if "<" in l:
                    cleaned_lines.append(l)

        with open(path, "w") as f:
            f.writelines(cleaned_lines)

    def write(self, path):
        with open(path, 'w', encoding='utf-8') as file:
            self.tree.write(file, encoding='unicode')


class Prompts_Interface(Operator):

    calculators = []

    def get_product(self):
        obj = bpy.data.objects[bpy.context.object.name]
        obj_product_bp = sn_utils.get_bp(obj, 'PRODUCT')
        product = Assembly(obj_product_bp)
        self.depth = math.fabs(product.obj_y.location.y)
        self.height = math.fabs(product.obj_z.location.z)
        self.width = math.fabs(product.obj_x.location.x)
        return product

    def get_insert(self):
        obj = bpy.data.objects[bpy.context.object.name]
        obj_product_bp = sn_utils.get_bp(obj, 'INSERT')
        insert = Assembly(obj_product_bp)
        return insert

    def draw_product_size(self, layout, alt_height="", use_rot_z=True):
        box = layout.box()
        row = box.row()

        col = row.column(align=True)
        row1 = col.row(align=True)
        if sn_utils.object_has_driver(self.product.obj_x):
            row1.label(text='Width: ' + str(round(sn_unit.meter_to_active_unit(math.fabs(self.product.obj_x.location.x)), 3)))
        else:
            row1.label(text='Width:')
            row1.prop(self, 'width', text="")

        row1 = col.row(align=True)
        if sn_utils.object_has_driver(self.product.obj_z):
            row1.label(text='Height: ' + str(round(sn_unit.meter_to_active_unit(math.fabs(self.product.obj_z.location.z)), 3)))
        else:
            row1.label(text='Height:')

            if alt_height == "":
                row1.prop(self, 'height', text="")
            else:
                row1.prop(self, alt_height, text="")

        row1 = col.row(align=True)
        if sn_utils.object_has_driver(self.product.obj_y):
            row1.label(text='Depth: ' + str(round(sn_unit.meter_to_active_unit(math.fabs(self.product.obj_y.location.y)), 3)))
        else:
            row1.label(text='Depth:')
            row1.prop(self, 'depth', text="")

        col = row.column(align=True)
        col.label(text="Location X:")
        col.label(text="Location Y:")
        col.label(text="Location Z:")

        col = row.column(align=True)
        col.prop(self.product.obj_bp, 'location', text="")

        if use_rot_z:
            row = box.row()
            row.label(text='Rotation Z:')
            row.prop(self.product.obj_bp, 'rotation_euler', index=2, text="")

    def draw_product_position(self, layout, plane=""):
        row = layout.row()
        box = row.box()
        col = box.column(align=True)

        row = col.row(align=True)
        row.label(text='Location:')

        if "x" in plane.lower() or plane == "":
            row1 = col.row(align=True)
            row1.label(text='X:')
            row1.prop(self.product.obj_bp, 'location', index=0, text="")

        if "y" in plane.lower() or plane == "":
            row2 = col.row(align=True)
            row2.label(text='Y:')
            row2.prop(self.product.obj_bp, 'location', index=1, text="")

        if "z" in plane.lower() or plane == "":
            row3 = col.row(align=True)
            row3.label(text='Z:')
            row3.prop(self.product.obj_bp, 'location', index=2, text="")

    def draw_product_rotation(self, layout, plane=""):
        row = layout.row()
        box = row.box()
        col = box.column(align=True)

        row = col.row(align=True)
        row.label(text='Rotation:')

        if "x" not in plane.lower() or plane == "":
            row1 = col.row(align=True)
            row1.label(text='X:')
            row1.prop(self.product.obj_bp, 'rotation_euler', index=0, text="")

        if "y" not in plane.lower() or plane == "":
            row2 = col.row(align=True)
            row2.label(text='Y:')
            row2.prop(self.product.obj_bp, 'rotation_euler', index=1, text="")

        if "z" not in plane.lower() or plane == "":
            row3 = col.row(align=True)
            row3.label(text='Z:')
            row3.prop(self.product.obj_bp, 'rotation_euler', index=2, text="")

    def draw_product_dimensions(self, layout):
        row = layout.row()
        box = row.box()
        col = box.column(align=True)

        row = col.row(align=True)
        row.label(text='Dimensions:')

        row1 = col.row(align=True)
        row1.label(text='X:')
        row1.prop(self.product.obj_bp, 'dimensions', index=0, text="")

        row2 = col.row(align=True)
        row2.label(text='Y:')
        row2.prop(self.product.obj_bp, 'dimensions', index=1, text="")

        row3 = col.row(align=True)
        row3.label(text='Z:')
        row3.prop(self.product.obj_bp, 'dimensions', index=2, text="")

    def update_product_size(self):
        self.product.obj_x.location.x = self.width

        if 'IS_MIRROR' in self.product.obj_y:
            self.product.obj_y.location.y = -self.depth
        else:
            self.product.obj_y.location.y = self.depth

        if 'IS_MIRROR' in self.product.obj_z:
            self.product.obj_z.location.z = -self.height
        else:
            self.product.obj_z.location.z = self.height

        sn_utils.run_calculators(self.product.obj_bp)

    def get_calculators(self, obj):
        for cal in obj.snap.calculators:
            self.calculators.append(cal)
        for child in obj.children:
            self.get_calculators(child)

    def run_calculators(self, obj):
        self.get_calculators(obj)
        for calculator in self.calculators:
            bpy.context.view_layer.update()
            calculator.calculate()

