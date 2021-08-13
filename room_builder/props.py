import bpy

from bpy.types import PropertyGroup
from bpy.props import (
    StringProperty,
    BoolProperty,
    IntProperty,
    FloatProperty,
    PointerProperty,
    CollectionProperty,
    EnumProperty)

from snap import sn_unit
from . import image_enums
from .room_builder_main import (update_obstacle_index,
                                update_wall_index,
                                toggle_obstacle_hide)


def set_view_port(self, context):
    if self.room_type == 'CUSTOM':
        bpy.ops.view3d.view_axis(type='TOP')


def update_floor_mat(self, context):
    bpy.ops.sn_roombuilder.update_floor_material()


def update_wall_mat(self, context):
    bpy.ops.sn_roombuilder.update_wall_material()


class Obstacle(PropertyGroup):
    bp_name: StringProperty("BP Name")
    base_point: StringProperty("Base Point")


class Wall(PropertyGroup):
    bp_name: StringProperty("BP Name")
    obstacle_index: IntProperty(name="ObstacleIndex", update=update_obstacle_index)
    obstacles: CollectionProperty(name="Obstacles", type=Obstacle)

    def add_obstacle(self, obstacle, base_point):
        obst = self.obstacles.add()
        obst.name = obstacle.obj_bp.snap.name_object
        obst.bp_name = obstacle.obj_bp.name
        obst.base_point = base_point


class Scene_Props(PropertyGroup):
    room_name: StringProperty(name="Room Name")
    room_type: EnumProperty(
        name="Room Type",
        items=[
            ("CUSTOM", "Custom Room", "Custom Room"),
            ("SINGLE", "Single Wall", "Single Wall"),
            ("LSHAPE", "L Shape", "L Shape Room"),
            ("USHAPE", "U Shape", "U Shape Room"),
            ("SQUARE", "Square Room", "Sqaure Room")],
        default="SQUARE",
        update=set_view_port)

    wall_index: IntProperty(name="Wall Index", update=update_wall_index)

    walls: CollectionProperty(name="Walls", type=Wall)

    wall_thickness: FloatProperty(name="Wall Thickness", default=sn_unit.inch(6), subtype='DISTANCE')
    wall_height: FloatProperty(name="Wall Height", default=sn_unit.inch(108), subtype='DISTANCE')

    background_image_scale: FloatProperty(
        name="Backgroud Image Scale",
        description="Property used to set the scale properly for background images.",
        unit='LENGTH')

    floor_type: EnumProperty(
        name="Floor Type",
        items=[
            ('CARPET', "Carpet", 'Carpet'),
            ('TILE', "Tile", 'Tile'),
            ('WOOD', "Wood Floor", 'Wood Floor')],
        default='CARPET',
        update=update_floor_mat)

    paint_type: EnumProperty(
        name="Paint Type",
        items=[('TEXTURED', "Paint", 'Textured Paint')],
        default='TEXTURED')

    entry_door_type: EnumProperty(
        name="Door Type",
        items=[
            ('OPEN', 'Open Entry Way', 'Open Entry Way'),
            ('SINGLE', 'Single Door', 'Single Door'),
            ('DOUBLE', 'Double Door', 'Double Door'),
            ('POCKET', 'Pocket Door', 'Pocket Door'),
            ('POCKET_DOUBLE', 'Pocket Double Door', 'Pocket Double Door'),
            ('SLIDING', 'Sliding Door', 'Sliding Door'),
            ('BIFOLD', 'Bi-Fold Door', 'Bi-Fold Door'),
            ('BIFOLD_DOUBLE', 'Bi-Fold Double Door', 'Bi-Fold Double Door')],
        default='OPEN')

    entry_door_fn = {'OPEN': "Entry Door Frame.blend",
                     'SINGLE': "Single Door.blend",
                     'DOUBLE': "Double Door.blend",
                     'POCKET': "Pocket Door.blend",
                     'POCKET_DOUBLE': "Pocket Double Door.blend",
                     'SLIDING': "Sliding Door.blend",
                     'BIFOLD': "Bi-Fold Door.blend",
                     'BIFOLD_DOUBLE': "Bi-Fold Double Door.blend"}

    obstacle_hide: EnumProperty(name="Hide Obstacles",
                                items=[('SHOW', 'Show Obstacles', 'Show Obstacles'),
                                       ('HIDE', 'Hide Obstacles', 'Hide Obstacles')],
                                default='SHOW',
                                update=toggle_obstacle_hide)

    carpet_material: EnumProperty(name="Carpet Material", items=image_enums.enum_carpet, update=update_floor_mat)
    wood_floor_material: EnumProperty(name="Wood Floor Material", items=image_enums.enum_wood_floor, update=update_floor_mat)
    tile_material: EnumProperty(name="Tile Material", items=image_enums.enum_tile_floor, update=update_floor_mat)
    wall_material: EnumProperty(name="Wall Material", items=image_enums.enum_wall_material, update=update_wall_mat)

    base_molding: EnumProperty(name="Base Molding", items=image_enums.enum_base_molding)
    crown_molding: EnumProperty(name="Crown Molding", items=image_enums.enum_crown_molding)

    add_base_molding: BoolProperty(name="Add Base Molding", default=False)
    base_molding_height: FloatProperty(name="Height of the base molding", default=0.05715, unit='LENGTH', precision=4)

    add_crown_molding: BoolProperty(name="Add Crown Molding", default=False)
    crown_molding_height: FloatProperty(name="Height of crown molding", default=0.08255, unit='LENGTH', precision=4)

    room_category: EnumProperty(name="Room Category",
                                description="Select the Category of the Room",
                                items=[("Please Select",
                                        "REQUIRED Please Select a Category",
                                        "Please Select a Category"),
                                       ("41110", "Closet", "Closet"),
                                       ("41120", "Entertainment Center", "Entertainment Center"),
                                       ("41130", "Garage", "Garage"),
                                       ("41140", "Home Office", "Home Office"),
                                       ("41150", "Laundry", "Laundry"),
                                       ("41160", "Mud Room", "Mud Room"),
                                       ("41170", "Pantry", "Pantry"),
                                       ("41210", "Kitchen", "Kitchen"),
                                       ("41220", "Bathroom", "Bathroom"),
                                       ("41230", "Reface", "Reface"),
                                       ("41240", "Remodel", "Remodel"),
                                       ("41250", "Stone", "Stone")])

    @classmethod
    def register(cls):
        bpy.types.Scene.sn_roombuilder = PointerProperty(
            name="SNaP Room Builder Scene Properties",
            description="SNaP Room Scene Object Properties",
            type=cls,
        )

    @classmethod
    def unregister(cls):
        del bpy.types.Scene.sn_roombuilder


class Object_Props(PropertyGroup):
    is_floor: BoolProperty(name="Is Floor")
    is_ceiling: BoolProperty(name="Is Ceiling")

    @classmethod
    def register(cls):
        bpy.types.Object.sn_roombuilder = PointerProperty(
            name="SNaP Room Builder Object Properties",
            description="SNaP Room Builder Object Properties",
            type=cls,
        )

    @classmethod
    def unregister(cls):
        del bpy.types.Object.sn_roombuilder


classes = (
    Obstacle,
    Wall,
    Scene_Props,
    Object_Props)

register, unregister = bpy.utils.register_classes_factory(classes)
