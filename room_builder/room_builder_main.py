import bpy

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


def toggle_obstacle_hide(self, context):
    state = True if self.obstacle_hide == 'HIDE' else False

    for o in bpy.data.objects:
        if o.get('IS_OBSTACLE'):
            obstacle = sn_types.Assembly(obj_bp=o)
            cage = obstacle.get_cage()
            cage.hide_viewport = state
