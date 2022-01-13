import bpy
from snap import sn_types

def update_wall_index(self, context):
    bpy.ops.object.select_all(action='DESELECT')
    wall = self.walls[self.wall_index]
    obj = bpy.data.objects[wall.bp_name]

    for child in obj.children:
        if child.type == 'MESH' and child.get('IS_BP_ASSEMBLY') is None:
            child.select_set(True)
            context.view_layer.objects.active = child


def update_obstacle_index(self, context):
    bpy.ops.object.select_all(action='DESELECT')
    wall = context.scene.sn_roombuilder.walls[context.scene.sn_roombuilder.wall_index]
    obstacle = wall.obstacles[wall.obstacle_index]

    obj = bpy.data.objects[obstacle.bp_name]
    for child in obj.children:
        if child.type == 'MESH' and child.get('IS_BP_ASSEMBLY') is None:
            child.hide_select = False
            child.select_set(True)
            context.view_layer.objects.active = child


def toggle_objects_hide(self, context):
    state = True if self.obstacle_hide == 'HIDE' else False

    for o in bpy.context.scene.collection.children['Collection'].objects:
        if o.type == 'MESH':
            o.hide_viewport = state
