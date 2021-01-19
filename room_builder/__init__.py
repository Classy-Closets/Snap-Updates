import bpy
from mv import fd_types, utils, unit
import math
from mathutils import Vector
import os
import inspect
from bpy.types import PropertyGroup, UIList, Panel, Operator
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       BoolVectorProperty,
                       PointerProperty,
                       CollectionProperty,
                       EnumProperty)

PAINT_LIBRARY_NAME = "Paint"
FLOORING_LIBRARY_NAME = "Flooring"
PAINT_CATEGORY_NAME = "Textured Wall Paint"
CARPET_CATEGORY_NAME = "Carpet"
TILE_CATEGORY_NAME = "Tile"
HARDWOOD_CATEGORY_NAME = "Wood Flooring"
MOLDING_ASSEMBLY = os.path.join(os.path.dirname(__file__), "Moldings", "assemblies", "molding.blend")
BASE_PRO_PATH = os.path.join(os.path.dirname(__file__), "Moldings", "profiles", "base")
CROWN_PRO_PATH = os.path.join(os.path.dirname(__file__), "Moldings", "profiles", "crown")

preview_collections = {}

def enum_carpet(self,context):
    if context is None:
        return []
    
    icon_dir = os.path.join(utils.get_library_dir("materials"),FLOORING_LIBRARY_NAME,CARPET_CATEGORY_NAME)
    pcoll = preview_collections["carpet"]
    return utils.get_image_enum_previews(icon_dir,pcoll)

def enum_wood_floor(self,context):
    if context is None:
        return []

    icon_dir = os.path.join(utils.get_library_dir("materials"),FLOORING_LIBRARY_NAME,HARDWOOD_CATEGORY_NAME)
    pcoll = preview_collections["wood_floor"]
    return utils.get_image_enum_previews(icon_dir,pcoll)

def enum_tile_floor(self,context):
    if context is None:
        return []

    icon_dir = os.path.join(utils.get_library_dir("materials"),FLOORING_LIBRARY_NAME,TILE_CATEGORY_NAME)
    pcoll = preview_collections["tile"]
    return utils.get_image_enum_previews(icon_dir,pcoll)

def enum_wall_material(self,context):
    if context is None:
        return []

    icon_dir = os.path.join(utils.get_library_dir("materials"),PAINT_LIBRARY_NAME,PAINT_CATEGORY_NAME)
    pcoll = preview_collections["paint"]
    return utils.get_image_enum_previews(icon_dir,pcoll)

def enum_base_molding(self,context):
    if context is None:
        return []

    icon_dir = os.path.join(os.path.dirname(__file__), "Moldings", "profiles","Base")
    pcoll = preview_collections["base molding"]
    return utils.get_image_enum_previews(icon_dir,pcoll)

def enum_crown_molding(self,context):
    if context is None:
        return []

    icon_dir = os.path.join(os.path.dirname(__file__), "Moldings", "profiles", "Crown")
    pcoll = preview_collections["crown molding"]
    return utils.get_image_enum_previews(icon_dir,pcoll)

def update_wall_index(self,context): 
    bpy.ops.object.select_all(action='DESELECT')
    wall = self.walls[self.wall_index]
    
    obj = bpy.data.objects[wall.bp_name]
    for child in obj.children:
        if child.type == 'MESH' and child.mv.type!= 'BPASSEMBLY':
            child.select = True
            context.scene.objects.active = child

def update_obstacle_index(self,context): 
    bpy.ops.object.select_all(action='DESELECT')
    wall = context.scene.fd_roombuilder.walls[context.scene.fd_roombuilder.wall_index]
    obstacle = wall.obstacles[wall.obstacle_index]
    
    obj = bpy.data.objects[obstacle.bp_name]
    for child in obj.children:
        if child.type == 'MESH' and child.mv.type!= 'BPASSEMBLY':
            child.hide_select = False
            child.select = True
            context.scene.objects.active = child 
           
def toggle_obstacle_hide(self, context):
    state = True if self.obstacle_hide == 'HIDE' else False
    
    for o in bpy.data.objects:
        if o.mv.type == 'OBSTACLE':
            obstacle = fd_types.Assembly(o)
            cage = obstacle.get_cage()
            cage.hide = state
                       
class Obstacle(PropertyGroup):
    
    bp_name = StringProperty("BP Name")
    base_point = StringProperty("Base Point")
    
bpy.utils.register_class(Obstacle)
    
class Wall(PropertyGroup):
    
    bp_name = StringProperty("BP Name")
    
    obstacle_index = IntProperty(name="ObstacleIndex",update=update_obstacle_index)
    obstacles = CollectionProperty(name="Obstacles",type=Obstacle)

    def add_obstacle(self,obstacle,base_point):
        obst = self.obstacles.add()
        obst.name = obstacle.obj_bp.mv.name_object
        obst.bp_name = obstacle.obj_bp.name
        obst.base_point = base_point
    
bpy.utils.register_class(Wall)

class Scene_Props(PropertyGroup):
    
    room_type = EnumProperty(name="Room Type",
                             items=[('CUSTOM',"Custom Room",'Custom Room'),
                                    ('SINGLE',"Single Wall",'Single Wall'),
                                    ('LSHAPE',"L Shape",'L Shape Room'),
                                    ('USHAPE',"U Shape",'U Shape Room'),
                                    ('SQUARE',"Square Room",'Sqaure Room')],
                             default='SQUARE')
    
    wall_index = IntProperty(name="Wall Index",update=update_wall_index)
    
    walls = CollectionProperty(name="Walls",type=Wall)

    background_image_scale = FloatProperty(name="Backgroud Image Scale",
                                           description="Property used to set the scale properly for background images.",
                                           unit='LENGTH')
    
    floor_type = EnumProperty(name="Floor Type",
                             items=[('CARPET',"Carpet",'Carpet'),
                                    ('TILE',"Tile",'Tile'),
                                    ('WOOD',"Wood Floor",'Wood Floor')],
                             default='CARPET')
    
    paint_type = EnumProperty(name="Paint Type",
                              items=[('TEXTURED',"Paint",'Textured Paint')],
                              default='TEXTURED')
    
    entry_door_type = EnumProperty(name="Door Type",
                                   items=[('OPEN', 'Open Entry Way', 'Open Entry Way'),
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
    
    obstacle_hide = EnumProperty(name="Hide Obstacles",
                                 items=[('SHOW', 'Show Obstacles', 'Show Obstacles'),
                                        ('HIDE', 'Hide Obstacles', 'Hide Obstacles')],
                                 default='SHOW',
                                 update=toggle_obstacle_hide)
    
    carpet_material = EnumProperty(name="Carpet Material",items=enum_carpet)
    wood_floor_material = EnumProperty(name="Wood Floor Material",items=enum_wood_floor)
    tile_material = EnumProperty(name="Tile Material",items=enum_tile_floor)
    wall_material = EnumProperty(name="Wall Material",items=enum_wall_material)

    base_molding = EnumProperty(name="Base Molding", items=enum_base_molding)
    crown_molding = EnumProperty(name="Crown Molding", items=enum_crown_molding)
    
    add_base_molding = BoolProperty(name="Add Base Molding",default = False)
    add_crown_molding = BoolProperty(name="Add Crown Molding",default = False)  

    room_category = EnumProperty(name="Room Category",
                                description="Select the Category of the Room",
                                items=[("Please Select","REQUIRED Please Select a Category","Please Select a Category"),
                                       ("41110","Closet","Closet"),
                                       ("41120","Entertainment Center","Entertainment Center"),
                                       ("41130","Garage","Garage"),
                                       ("41140","Home Office","Home Office"),
                                       ("41150","Laundry","Laundry"),
                                       ("41160","Mud Room","Mud Room"),
                                       ("41170","Pantry","Pantry"),
                                       ("41210","Kitchen","Kitchen"),
                                       ("41220","Bathroom","Bathroom"),
                                       ("41230","Reface","Reface"),
                                       ("41240","Remodel","Remodel"),
                                       ("41250","Stone","Stone")])  
    
class Object_Props(PropertyGroup):
    
    is_floor = BoolProperty(name="Is Floor")
    is_ceiling = BoolProperty(name="Is Ceiling")

class PANEL_Room_Builder(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "Room Builder"
    bl_category = "SNaP"
    
    def draw_header(self, context):
        layout = self.layout
        layout.label('',icon='MOD_BUILD')
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.fd_roombuilder
        mv = context.scene.mv

        main_box = layout.box()
        box = main_box.box()
        box.label('Room Setup:',icon='SNAP_PEEL_OBJECT')
        box.prop(props,'room_type',text="Room Template")

        row = box.row(align=True)
        row.prop(props,'floor_type',text="Floor",icon='FILE_FOLDER')
        if props.floor_type == 'CARPET':
            row.prop(props,'carpet_material',text="")
        if props.floor_type == 'WOOD':
            row.prop(props,'wood_floor_material',text="")
        if props.floor_type == 'TILE':
            row.prop(props,'tile_material',text="")
        row = box.row(align=True)
        row.prop(props,'paint_type',text="Walls",icon='FILE_FOLDER')
        row.prop(props,'wall_material',text="")
        
        row = box.row()
        row.prop(props, 'add_base_molding',text="Include Base Molding:")
        
        if props.add_base_molding:
            row.prop(props, 'base_molding', text="")
        
        row = box.row()
        row.prop(props, 'add_crown_molding', text="Include Crown Molding:")        
        
        if props.add_crown_molding:
            row.prop(props, 'crown_molding', text="")

        if props.room_type == 'SQUARE':
            row = box.row(align=True)
            row.prop(props, 'entry_door_type', text="Door", icon='FILE_FOLDER')                                            

        row = box.row(align=True)
        row.prop(mv,'default_wall_height')
        row.prop(mv,'default_wall_depth')

        if props.room_type == 'CUSTOM':
            row = box.row()
            row.operator('fd_assembly.draw_wall',text="Draw Walls",icon='GREASEPENCIL')
            row.operator('fd_roombuilder.collect_walls',icon='FILE_REFRESH')
            self.draw_custom_room_options(layout,context)
        else:
            col = box.column()
            col.scale_y = 1.3
            if len(bpy.data.objects) > 0:
                col.operator('fd_roombuilder.delete_room',text="Delete Room",icon='X')
                col.operator('fd_roombuilder.new_room',text="New Room",icon='PLUS')
            else:
                col.operator('fd_roombuilder.build_room',text="Build Room",icon='SNAP_PEEL_OBJECT')

        if len(props.walls) > 0:
            # box = main_box.box()
            # row = box.row(align=True)
            #row.prop(props, "room_category",text="Room Category")
            #row.prop_enum(self.props, 'room_category',text="Room Category")

            box = main_box.box()
            row = box.row(align=True)
            row.label("Room Objects:",icon='SNAP_FACE')
            row.prop_enum(props, 'obstacle_hide', 'SHOW', icon='RESTRICT_VIEW_OFF', text="")
            row.prop_enum(props, 'obstacle_hide', 'HIDE', icon='RESTRICT_VIEW_ON', text="")
            
            box.template_list("FD_UL_walls", "", props, "walls", props, "wall_index", rows=len(props.walls))
            wall = props.walls[props.wall_index]
            if wall.bp_name in context.scene.objects:
                obj = context.scene.objects[wall.bp_name]
                if obj.fd_roombuilder.is_ceiling:
                    box.operator('fd_roombuilder.add_floor_obstacle',text="Add Obstacle To Ceiling",icon='PLUG')
                elif obj.fd_roombuilder.is_floor:
                    box.operator('fd_roombuilder.add_floor_obstacle',text="Add Obstacle To Floor",icon='PLUG')
                else:
                    box.operator('fd_roombuilder.add_obstacle',text="Add Obstacle To Wall",icon='PLUG')
                
                if len(wall.obstacles) > 0:
                    box.template_list("FD_UL_obstacles", "", wall, "obstacles", wall, "obstacle_index", rows=4)

    def draw_custom_room_options(self,layout,context):
        view = context.space_data
        use_multiview = context.scene.render.use_multiview

        mainbox = layout.box()
        mainbox.operator("view3d.background_image_add", text="Add Image",icon='ZOOMIN')

        for i, bg in enumerate(view.background_images):
            layout.active = view.show_background_images
            box = mainbox.box()
            row = box.row(align=True)
            row.prop(bg, "show_expanded", text="", emboss=False)
            if bg.source == 'IMAGE' and bg.image:
                row.prop(bg.image, "name", text="", emboss=False)
            elif bg.source == 'MOVIE_CLIP' and bg.clip:
                row.prop(bg.clip, "name", text="", emboss=False)
            else:
                row.label(text="Select an Image with the open button")

            if bg.show_background_image:
                row.prop(bg, "show_background_image", text="", emboss=False, icon='RESTRICT_VIEW_OFF')
            else:
                row.prop(bg, "show_background_image", text="", emboss=False, icon='RESTRICT_VIEW_ON')

            row.operator("view3d.background_image_remove", text="", emboss=False, icon='X').index = i

            if bg.show_expanded:
                
                has_bg = False
                if bg.source == 'IMAGE':
                    row = box.row()
                    row.template_ID(bg, "image", open="image.open")
                    
                    if bg.image is not None:
                        box.prop(bg, "view_axis", text="Display View")
                        box.prop(bg, "draw_depth", expand=False,text="Draw Depth")
                        has_bg = True

                        if use_multiview and bg.view_axis in {'CAMERA', 'ALL'}:
                            box.prop(bg.image, "use_multiview")

                            column = box.column()
                            column.active = bg.image.use_multiview

                            column.label(text="Views Format:")
                            column.row().prop(bg.image, "views_format", expand=True)

                elif bg.source == 'MOVIE_CLIP':
                    box.prop(bg, "use_camera_clip")

                    column = box.column()
                    column.active = not bg.use_camera_clip
                    column.template_ID(bg, "clip", open="clip.open")

                    if bg.clip:
                        column.template_movieclip(bg, "clip", compact=True)

                    if bg.use_camera_clip or bg.clip:
                        has_bg = True

                    column = box.column()
                    column.active = has_bg
                    column.prop(bg.clip_user, "proxy_render_size", text="")
                    column.prop(bg.clip_user, "use_render_undistorted")

                if has_bg:
                    row = box.row()
                    row.label("Image Opacity")
                    row.prop(bg, "opacity", slider=True,text="")

                    row = box.row()
                    row.label("Rotation:")
                    row.prop(bg, "rotation",text="")

                    row = box.row()
                    row.label("Location:")
                    row.prop(bg, "offset_x", text="X")
                    row.prop(bg, "offset_y", text="Y")

                    row = box.row()
                    row.label("Flip Image:")
                    row.prop(bg, "use_flip_x",text="Horizontally")
                    row.prop(bg, "use_flip_y",text="Vertically")

                    row = box.row()
                    row.prop(context.scene.fd_roombuilder, "background_image_scale", text="Known Dimension")
                    row.operator('fd_roombuilder.select_two_points',text="Select Two Points",icon='MAN_TRANS')

                    row = box.row()
                    row.label("Image Size:")
                    row.prop(bg, "size",text="")

class FD_UL_walls(UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if item.bp_name in context.scene.objects:
            wall_bp = context.scene.objects[item.bp_name]
            
            obstacle_count = len(item.obstacles)
            count_text = ""
            if obstacle_count > 0:
                count_text = "(" + str(obstacle_count) + ")"
            
            if wall_bp.fd_roombuilder.is_floor or wall_bp.fd_roombuilder.is_ceiling:
                layout.label(text="",icon='MESH_GRID')
                layout.label(text=item.name + "   " + count_text)
                layout.label("Area: " + str(unit.meter_to_active_unit(wall_bp.dimensions.x) * unit.meter_to_active_unit(wall_bp.dimensions.y)))
                if wall_bp.hide:
                    layout.operator('fd_roombuilder.show_plane',text="",icon='RESTRICT_VIEW_ON',emboss=False).object_name = wall_bp.name
                else:
                    layout.operator('fd_roombuilder.hide_plane',text="",icon='RESTRICT_VIEW_OFF',emboss=False).object_name = wall_bp.name
            else:
                wall = fd_types.Wall(wall_bp)
                layout.label(text="",icon='SNAP_FACE')
                layout.label(text=item.name + "   " + count_text)
                layout.label("Length: " + str(unit.meter_to_active_unit(wall.obj_x.location.x)))
                if wall.obj_bp.hide:
                    props = layout.operator('fd_roombuilder.hide_show_wall',text="",icon='RESTRICT_VIEW_ON',emboss=False)
                    props.wall_bp_name = wall_bp.name
                    props.hide = False
                else:
                    props = layout.operator('fd_roombuilder.hide_show_wall',text="",icon='RESTRICT_VIEW_OFF',emboss=False)
                    props.wall_bp_name = wall_bp.name
                    props.hide = True
                    
class FD_UL_obstacles(UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        wall = context.scene.fd_roombuilder.walls[context.scene.fd_roombuilder.wall_index]
        wall_obj = context.scene.objects[wall.bp_name]

        layout.label(text="",icon='PLUG')
        layout.label(text=item.name)
                
        if wall_obj.fd_roombuilder.is_floor or wall_obj.fd_roombuilder.is_ceiling:
            layout.operator('fd_roombuilder.add_floor_obstacle',text="",icon='INFO').obstacle_bp_name = item.bp_name
        else:
            layout.operator('fd_roombuilder.add_obstacle',text="",icon='INFO').obstacle_bp_name = item.bp_name
             
        layout.operator('fd_roombuilder.delete_obstacle',text="",icon='X').obstacle_bp_name = item.bp_name
        
class OPERATOR_Draw_Walls(Operator):        
    bl_idname = "fd_roombuilder.draw_walls"
    bl_label = "Custom Room - Draw Walls" 
    bl_options = {'UNDO'}
    
    def execute(self, context):
        utils.delete_obj_list(bpy.data.objects)
        props = context.scene.fd_roombuilder
        
        for old_wall in props.walls:
            props.walls.remove(0)      
        
        bpy.ops.fd_assembly.draw_wall()
        return {'FINISHED'}
        
class OPERATOR_Add_Obstacle(Operator):
    bl_idname = "fd_roombuilder.add_obstacle"
    bl_label = "Add Obstacle" 
    bl_options = {'UNDO'}

    obstacle_bp_name = StringProperty(name="Obstacle BP Name",
                                      description="Pass the base point name to reposition an existing obstacle",
                                      default="")

    base_point = EnumProperty(name="Base Point",
                             items=[('TOP_LEFT',"Top Left",'Top Left of Wall'),
                                    ('TOP_RIGHT',"Top Right",'Top Right of Wall'),
                                    ('BOTTOM_LEFT',"Bottom Left",'Bottom Left of Wall'),
                                    ('BOTTOM_RIGHT',"Bottom_Right",'Bottom Right of Wall')],
                             default = 'BOTTOM_LEFT')

    obstacle_name = StringProperty(name="Obstacle Name",
                                   description="Enter the Name of the Obstacle",
                                   default="New Obstacle")

    obstacle_width = FloatProperty(name="Obstacle Width",
                                   description="Enter the Width of the Obstacle",
                                   default=unit.inch(3),
                                   unit='LENGTH',
                                   precision=4)

    obstacle_height = FloatProperty(name="Obstacle Height",
                                    description="Enter the Height of the Obstacle",
                                    default=unit.inch(4),
                                    unit='LENGTH',
                                    precision=4)

    obstacle_depth = FloatProperty(name="Obstacle Depth",
                                    description="Enter the Depth of the Obstacle",
                                    default=unit.inch(1),
                                    unit='LENGTH',
                                    precision=4)

    x_location = FloatProperty(name="X Location",
                               description="Enter the X Location of the Obstacle",
                               default=unit.inch(0),
                               unit='LENGTH',
                               precision=4)

    z_location = FloatProperty(name="Z Location",
                               description="Enter the Z Location of the Obstacle",
                               default=unit.inch(0),
                               unit='LENGTH',
                               precision=4)
    
    dim_x_loc_offset = FloatProperty(name="Dimension X Location Offset",
                                     description="Enter X location dimension offset from wall",
                                     default=unit.inch(6.0),
                                     unit='LENGTH',
                                     precision=4)    

    dim_z_loc_offset = FloatProperty(name="Dimension Z Location Offset",
                                     description="Enter Z location dimension offset from wall",
                                     default=unit.inch(9.0),
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
                self.dim_x_loc.start_z(value=self.wall.obj_z.location.z - self.obstacle.obj_bp.location.z + self.dim_x_loc_offset)
                
                self.dim_z_loc.start_x(value=-self.obstacle.obj_bp.location.x - self.dim_z_loc_offset)
                self.dim_z_loc.start_z(value=self.wall.obj_z.location.z - self.obstacle.obj_bp.location.z)
                self.dim_z_loc.end_z(value=-(self.wall.obj_z.location.z - self.obstacle.obj_bp.location.z - self.obstacle_height))
                
            if self.base_point == 'TOP_RIGHT':
                self.obstacle.obj_bp.location.x = self.wall.obj_x.location.x - self.x_location - self.obstacle_width
                self.obstacle.obj_bp.location.z = self.wall.obj_z.location.z - self.z_location - self.obstacle_height
                
                self.dim_x_loc.start_x(value=self.obstacle_width)
                self.dim_x_loc.end_x(value=self.wall.obj_x.location.x - self.obstacle.obj_bp.location.x - self.obstacle_width)
                self.dim_x_loc.start_z(value=self.wall.obj_z.location.z - self.obstacle.obj_bp.location.z + self.dim_x_loc_offset)
                
                self.dim_z_loc.start_x(value=self.wall.obj_x.location.x - self.obstacle.obj_bp.location.x + self.dim_z_loc_offset)
                self.dim_z_loc.start_z(value=self.wall.obj_z.location.z - self.obstacle.obj_bp.location.z)
                self.dim_z_loc.end_z(value=-(self.wall.obj_z.location.z - self.obstacle.obj_bp.location.z - self.obstacle_height))
                
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
                self.dim_x_loc.end_x(value= self.wall.obj_x.location.x - self.obstacle.obj_bp.location.x - self.obstacle_width)
                self.dim_x_loc.start_z(value=-self.obstacle.obj_bp.location.z - self.dim_x_loc_offset)
                
                self.dim_z_loc.start_x(value=self.wall.obj_x.location.x - self.obstacle.obj_bp.location.x + self.dim_z_loc_offset)
                self.dim_z_loc.start_z(value=0)
                self.dim_z_loc.end_z(value=-self.obstacle.obj_bp.location.z)

        return True
    
    def __del__(self):
        self.set_draw_type(bpy.context, 'TEXTURED')

        if self.click_ok == False:
            if not self.modify_existing:
                utils.delete_object_and_children(self.obstacle.obj_bp)
            else:
                for obstacle in self.wall_item.obstacles:
                    if obstacle.bp_name == self.obstacle_bp_name:
                        obstacle.base_point = self.base_point                
        
    def set_draw_type(self, context, draw_type='WIRE'):
        for obj in context.scene.objects:
            if obj.mv.type == 'CAGE':
                continue            
            if obj.parent:
                if obj.parent.name == self.wall.obj_bp.name:
                    pass
                else:
                    obj.draw_type = draw_type
        if self.obstacle:
            for child in self.obstacle.obj_bp.children:
                child.draw_type = 'WIRE'
    
    def invoke(self, context, event):
        wm = context.window_manager
        self.click_ok = False
        self.modify_existing = False if self.obstacle_bp_name == "" else True
        
        self.wall_item = context.scene.fd_roombuilder.walls[context.scene.fd_roombuilder.wall_index]
        wall_bp = context.scene.objects[self.wall_item.bp_name]
        self.wall = fd_types.Wall(wall_bp)
        self.set_draw_type(context)
        
        self.obstacle_height = unit.inch(4)
        self.obstacle_width = unit.inch(3)
        self.x_location = 0
        self.z_location = 0
        
        if self.modify_existing:
            if self.obstacle_bp_name in context.scene.objects:
                for obstacle in self.wall_item.obstacles:
                    if obstacle.bp_name == self.obstacle_bp_name:
                        self.base_point = obstacle.base_point
                        self.obstacle_name = obstacle.name
                 
                obj_bp = context.scene.objects[self.obstacle_bp_name]
                self.obstacle = fd_types.Assembly(obj_bp)
                self.obstacle_height = self.obstacle.obj_z.location.z
                self.obstacle_width = self.obstacle.obj_x.location.x
                self.obstacle_depth = math.fabs(self.obstacle.obj_y.location.y)
                
                if self.base_point == 'TOP_LEFT':
                    self.x_location = self.obstacle.obj_bp.location.x
                    self.z_location = self.wall.obj_z.location.z - self.obstacle.obj_bp.location.z - self.obstacle_height
                if self.base_point == 'TOP_RIGHT':
                    self.x_location = self.wall.obj_x.location.x - self.obstacle.obj_bp.location.x - self.obstacle_width
                    self.z_location = self.wall.obj_z.location.z - self.obstacle.obj_bp.location.z - self.obstacle_height
                if self.base_point == 'BOTTOM_LEFT':
                    self.x_location = self.obstacle.obj_bp.location.x
                    self.z_location = self.obstacle.obj_bp.location.z
                if self.base_point == 'BOTTOM_RIGHT':
                    self.x_location = self.wall.obj_x.location.x - self.obstacle.obj_bp.location.x - self.obstacle_width
                    self.z_location = self.obstacle.obj_bp.location.z
                    
                utils.delete_object_and_children(obj_bp)
            
        self.obstacle = fd_types.Assembly()
        self.obstacle.create_assembly()
        self.obstacle.obj_bp.mv.type = 'OBSTACLE'
        cage = self.obstacle.get_cage()
        cage.select = True
        cage.show_x_ray = True
        self.obstacle.obj_x.hide = True
        self.obstacle.obj_y.hide = True
        self.obstacle.obj_z.hide = True
        self.obstacle.obj_bp.parent = self.wall.obj_bp
        self.obstacle.obj_x.location.x = self.obstacle_width
        self.obstacle.obj_y.location.y = self.wall.obj_y.location.y + unit.inch(2)
        self.obstacle.obj_z.location.z = self.obstacle_height
        self.obstacle.obj_bp.location.y = 0
        self.obstacle.draw_as_hidden_line()
        
        Width = self.obstacle.get_var('dim_x','Width')
        
        self.dim_label = fd_types.Dimension()
        self.dim_label.parent(self.obstacle.obj_bp)
        self.dim_label.start_z(value = unit.inch(.5))
        self.dim_label.start_x('Width/2',[Width])
        self.dim_label.set_label(self.obstacle_name)        
        
        self.dim_x_loc = fd_types.Dimension()
        self.dim_x_loc.parent(self.obstacle.obj_bp)
        
        self.dim_z_loc = fd_types.Dimension()
        self.dim_z_loc.parent(self.obstacle.obj_bp)       
        
        if self.modify_existing:
            self.obstacle.obj_bp.name = self.obstacle_bp_name
            
        self.check(context)
        
        return wm.invoke_props_dialog(self, width=400)
    
    def execute(self, context):
        self.click_ok = True
        self.dim_label.set_label(self.obstacle_name)
        
        if not self.modify_existing:
            self.obstacle.obj_bp.mv.name_object = self.obstacle_name
            str_obstacle_index = str(len(self.wall_item.obstacles))
            self.obstacle.obj_bp.name = "{}.{}.{}".format(self.obstacle.obj_bp.mv.type,
                                                           str_obstacle_index,
                                                           self.obstacle_name)

            self.wall_item.add_obstacle(self.obstacle,self.base_point)
            
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

        return {'FINISHED'}
        
    def draw(self,context):
        layout = self.layout
        box = layout.box()

        box.prop(self,"obstacle_name")
        
        col = box.column(align=False)
        
        row = col.row(align=True)
        row.prop_enum(self, "base_point", 'TOP_LEFT', icon='TRIA_LEFT', text="Top Left") 
        row.prop_enum(self, "base_point", 'TOP_RIGHT', icon='TRIA_RIGHT', text="Top Right") 
        row = col.row(align=True)
        row.prop_enum(self, "base_point", 'BOTTOM_LEFT', icon='TRIA_LEFT', text="Bottom Left") 
        row.prop_enum(self, "base_point", 'BOTTOM_RIGHT', icon='TRIA_RIGHT', text="Bottom Right")   
        
        row = col.row()
        row.label("Obstacle Width:")
        row.prop(self,"obstacle_width",text="")
        
        row = col.row()
        row.label("Obstacle Height:")
        row.prop(self,"obstacle_height",text="")
        
        row = col.row()
        row.label("Obstacle Depth:")
        row.prop(self,"obstacle_depth",text="")        
        
        row = col.row()
        row.label("Obstacle X Location:")
        row.prop(self,"x_location",text="")
        
        row = col.row()
        row.label("Obstacle Z Location:")
        row.prop(self,"z_location",text="")


class OPERATOR_Add_Floor_Obstacle(Operator):
    bl_idname = "fd_roombuilder.add_floor_obstacle"
    bl_label = "Add Floor or Ceiling Obstacle" 
    bl_options = {'UNDO'}

    obstacle_bp_name = StringProperty(name="Obstacle BP Name",
                                      description="Pass the base point name to reposition an existing obstacle",
                                      default="")

    base_point = EnumProperty(name="Base Point",
                             items=[('FRONT_LEFT',"Front Left",'Front Left of Room'),
                                    ('FRONT_RIGHT',"Front Right",'Front Right of Room'),
                                    ('BACK_LEFT',"Back Left",'Back Left of Room'),
                                    ('BACK_RIGHT',"Back",'Back Right of Room')],
                             default = 'FRONT_LEFT')

    obstacle_name = StringProperty(name="Obstacle Name",
                                   description="Enter the Name of the Obstacle",
                                   default="New Obstacle")

    obstacle_width = FloatProperty(name="Obstacle Width",
                                   description="Enter the Width of the Obstacle",
                                   default=unit.inch(3),
                                   unit='LENGTH',
                                   precision=4)

    obstacle_depth = FloatProperty(name="Obstacle Depth",
                                   description="Enter the Depth of the Obstacle",
                                   default=unit.inch(4),
                                   unit='LENGTH',
                                   precision=4)

    obstacle_height = FloatProperty(name="Obstacle Height",
                                   description="Enter the Height of the Obstacle",
                                   default=unit.inch(1),
                                   unit='LENGTH',
                                   precision=4)

    x_location = FloatProperty(name="X Location",
                               description="Enter the X Location of the Obstacle",
                               default=unit.inch(0),
                               unit='LENGTH',
                               precision=4)

    y_location = FloatProperty(name="Y Location",
                               description="Enter the Y Location of the Obstacle",
                               default=unit.inch(0),
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
            if self.plane.fd_roombuilder.is_ceiling:
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
    
    def __del__(self):
        self.set_draw_type(bpy.context, 'TEXTURED')

        if self.click_ok == False:
            if not self.modify_existing:
                utils.delete_object_and_children(self.obstacle.obj_bp)
            else:
                for obstacle in self.wall_item.obstacles:
                    if obstacle.bp_name == self.obstacle_bp_name:
                        obstacle.base_point = self.base_point
        
    def set_draw_type(self, context, draw_type='WIRE'):
        for obj in context.scene.objects:
            if obj.mv.type == 'CAGE':
                continue            
            if obj.parent:
                if obj.parent.name == self.plane.name:
                    pass
                else:
                    obj.draw_type = draw_type
        if self.obstacle:
            for child in self.obstacle.obj_bp.children:
                child.draw_type = 'WIRE'
    
    def invoke(self, context, event):
        wm = context.window_manager
        self.click_ok = False
        self.modify_existing = False if self.obstacle_bp_name == "" else True
        
        self.wall_item = context.scene.fd_roombuilder.walls[context.scene.fd_roombuilder.wall_index]
        self.plane = context.scene.objects[self.wall_item.bp_name]
        self.set_draw_type(context)

        if self.modify_existing:
            if self.obstacle_bp_name in context.scene.objects:
                for obstacle in self.wall_item.obstacles:
                    if obstacle.bp_name == self.obstacle_bp_name:
                        self.base_point = obstacle.base_point
                        self.obstacle_name = obstacle.name
                 
                obj_bp = context.scene.objects[self.obstacle_bp_name]
                self.obstacle = fd_types.Assembly(obj_bp)
                if self.plane.fd_roombuilder.is_ceiling:
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
                    
                utils.delete_object_and_children(obj_bp)
            
        self.obstacle = fd_types.Assembly()
        self.obstacle.create_assembly()
        self.obstacle.obj_bp.mv.type = 'OBSTACLE'
        cage = self.obstacle.get_cage()
        cage.select = True
        cage.show_x_ray = True
        self.obstacle.obj_x.hide = True
        self.obstacle.obj_y.hide = True
        self.obstacle.obj_z.hide = True
        
        self.obstacle.obj_bp.parent = self.plane
        self.obstacle.obj_x.location.x = self.obstacle_width
        self.obstacle.obj_y.location.y = self.obstacle_depth
        if self.plane.fd_roombuilder.is_ceiling:
            self.obstacle.obj_z.location.z = -self.obstacle_height
        else:
            self.obstacle.obj_z.location.z = self.obstacle_height
        self.obstacle.obj_bp.location.y = self.y_location
        
        Width = self.obstacle.get_var('dim_x','Width')
        
        self.dim_label = fd_types.Dimension()
        self.dim_label.parent(self.obstacle.obj_bp)
        self.dim_label.start_z(value = unit.inch(.5))
        self.dim_label.start_x('Width/2',[Width])
        self.dim_label.set_label(self.obstacle_name)        
        
        self.dim_x_loc = fd_types.Dimension()
        self.dim_x_loc.parent(self.obstacle.obj_bp)
        
        self.dim_z_loc = fd_types.Dimension()
        self.dim_z_loc.parent(self.obstacle.obj_bp)       
        
        if self.modify_existing:
            self.obstacle.obj_bp.name = self.obstacle_bp_name
            
        self.check(context)
        
        return wm.invoke_props_dialog(self, width=400)
    
    def execute(self, context):
        self.click_ok = True
        self.dim_label.set_label(self.obstacle_name)
        
        if not self.modify_existing:
            self.obstacle.obj_bp.mv.name_object = self.obstacle_name
            str_obstacle_index = str(len(self.wall_item.obstacles))
            self.obstacle.obj_bp.name = "{}.{}.{}".format(self.obstacle.obj_bp.mv.type,
                                                           str_obstacle_index,
                                                           self.obstacle_name)

            self.wall_item.add_obstacle(self.obstacle,self.base_point)
            
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

        return {'FINISHED'}
        
    def draw(self,context):
        layout = self.layout
        box = layout.box()

        box.prop(self,"obstacle_name")
        
        col = box.column(align=False)
        
        row = col.row(align=True)
        row.prop_enum(self, "base_point", 'BACK_LEFT', icon='TRIA_LEFT', text="Back Left") 
        row.prop_enum(self, "base_point", 'BACK_RIGHT', icon='TRIA_RIGHT', text="Back Right")   
        row = col.row(align=True)
        row.prop_enum(self, "base_point", 'FRONT_LEFT', icon='TRIA_LEFT', text="Front Left") 
        row.prop_enum(self, "base_point", 'FRONT_RIGHT', icon='TRIA_RIGHT', text="Front Right")   
        
        row = col.row()
        row.label("Obstacle Width:")
        row.prop(self,"obstacle_width",text="")
        
        row = col.row()
        row.label("Obstacle Height:")
        row.prop(self,"obstacle_height",text="")        
        
        row = col.row()
        row.label("Obstacle Depth:")
        row.prop(self,"obstacle_depth",text="")
        
        row = col.row()
        row.label("Obstacle X Location:")
        row.prop(self,"x_location",text="")
        
        row = col.row()
        row.label("Obstacle Y Location:")
        row.prop(self,"y_location",text="")


class OPERATOR_Build_Room(Operator):
    bl_idname = "fd_roombuilder.build_room"
    bl_label = "Build Room" 
    bl_options = {'UNDO'}

    room_name = StringProperty(name="Room Name", default="New Room")

    add_to_project = BoolProperty(name="Add to Selected Project", default=True)

    back_wall_length = FloatProperty(name="Back Wall Length",
                                     description="Enter the Back Wall Length",
                                     default=unit.inch(120),
                                     unit='LENGTH',
                                     precision=4)

    side_wall_length = FloatProperty(name="Side Wall Length",
                                     description="Enter the Side Wall Length",
                                     default=unit.inch(120),
                                     unit='LENGTH',
                                     precision=4)
    
    left_return_length = FloatProperty(name="Left Return Length",
                                       description="Enter the Left Return Wall Length",
                                       default=unit.inch(25),
                                       unit='LENGTH',
                                       precision=4)
    
    right_return_length = FloatProperty(name="Right Return Length",
                                       description="Enter the Right Return Wall Length",
                                       default=unit.inch(25),
                                       unit='LENGTH',
                                       precision=4)
    
    wall_height = FloatProperty(name="Wall Height",
                                description="Enter the Wall Height",
                                default=unit.inch(108),
                                unit='LENGTH',
                                precision=4)
    
    wall_thickness = FloatProperty(name="Wall Thickness",
                                   description="Enter the Wall Thickness",
                                   default=unit.inch(4),
                                   unit='LENGTH',
                                   precision=4)
    
    opening_height = FloatProperty(name="Opening Height",
                                   description="Enter the Height of the Opening",
                                   default=unit.inch(83),
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
    
    def set_camera_position(self,context):
        view3d = context.space_data.region_3d
        if unit.meter_to_active_unit(self.back_wall_length) / 17 < 7:
            distance = 7
        elif unit.meter_to_active_unit(self.back_wall_length) / 17 > 12:
            distance = 12
        else:
            distance = unit.meter_to_active_unit(self.back_wall_length) / 17
        view3d.view_distance = distance
        view3d.view_location = (self.back_wall_length/2,self.side_wall_length,0)
        view3d.view_rotation = (.8416,.4984,-.1004,-.1824)
    
    def set_molding_points(self, curve, points):
        spline = curve.data.splines.new('BEZIER')
        spline.bezier_points.add(count=len(points) - 1)        
        
        for i, point in enumerate(points):
            curve.data.splines[0].bezier_points[i].co = point
        
        bpy.context.scene.objects.active = curve 
        bpy.ops.object.editmode_toggle()
        bpy.ops.curve.select_all(action='SELECT')
        bpy.ops.curve.handle_type_set(type='VECTOR')
        bpy.ops.object.editmode_toggle()

    def update_square_room(self):
        self.left_side_wall.obj_z.location.z = self.wall_height
        self.left_side_wall.obj_y.location.y = self.wall_thickness
        self.left_side_wall.obj_x.location.x = self.side_wall_length
        self.left_side_wall.obj_bp.mv.name_object = "Wall A"
        
        self.back_wall.obj_z.location.z = self.wall_height
        self.back_wall.obj_y.location.y = self.wall_thickness
        self.back_wall.obj_x.location.x = self.back_wall_length
        self.back_wall.obj_bp.mv.name_object = "Wall B"
        
        self.right_side_wall.obj_z.location.z = self.wall_height
        self.right_side_wall.obj_y.location.y = self.wall_thickness
        self.right_side_wall.obj_x.location.x = self.side_wall_length
        self.right_side_wall.obj_bp.mv.name_object = "Wall C"
        
        self.entry_wall.obj_z.location.z = self.wall_height
        self.entry_wall.obj_y.location.y = self.wall_thickness
        self.entry_wall.obj_x.location.x = self.back_wall_length
        self.entry_wall.obj_bp.mv.name_object = "Wall D"
        
        self.door.obj_bp.location.x = self.right_return_length
        self.door.obj_x.location.x = self.back_wall_length - self.right_return_length - self.left_return_length
        self.door.obj_y.location.y = self.wall_thickness + unit.inch(.01)
        self.door.obj_z.location.z = self.opening_height

        self.left_side_wall.obj_z.hide = True
        self.left_side_wall.obj_y.hide = True
        self.left_side_wall.obj_x.hide = True
        self.back_wall.obj_z.hide = True
        self.back_wall.obj_y.hide = True
        self.back_wall.obj_x.hide = True
        self.right_side_wall.obj_z.hide = True
        self.right_side_wall.obj_y.hide = True
        self.right_side_wall.obj_x.hide = True
        self.entry_wall.obj_z.hide = True
        self.entry_wall.obj_y.hide = True
        self.entry_wall.obj_x.hide = True
        self.door.obj_z.hide = True
        self.door.obj_y.hide = True
        self.door.obj_x.hide = True
    
    def update_single_wall(self):
        self.back_wall.obj_z.location.z = self.wall_height
        self.back_wall.obj_y.location.y = self.wall_thickness
        self.back_wall.obj_x.location.x = self.back_wall_length
        self.back_wall.obj_bp.mv.name_object = "Wall A"
    
        self.back_wall.obj_z.hide = True
        self.back_wall.obj_y.hide = True
        self.back_wall.obj_x.hide = True
    
    def update_l_shape_wall(self):
        self.back_wall.obj_z.location.z = self.wall_height
        self.back_wall.obj_y.location.y = self.wall_thickness
        self.back_wall.obj_x.location.x = self.back_wall_length
        self.back_wall.obj_bp.mv.name_object = "Wall B"
    
        self.left_side_wall.obj_z.location.z = self.wall_height
        self.left_side_wall.obj_y.location.y = self.wall_thickness
        self.left_side_wall.obj_x.location.x = self.left_return_length
        self.left_side_wall.obj_bp.mv.name_object = "Wall A"

        self.left_side_wall.obj_z.hide = True
        self.left_side_wall.obj_y.hide = True
        self.left_side_wall.obj_x.hide = True
    
        self.back_wall.obj_z.hide = True
        self.back_wall.obj_y.hide = True
        self.back_wall.obj_x.hide = True
        
    def update_u_shape_wall(self):
        self.left_side_wall.obj_z.location.z = self.wall_height
        self.left_side_wall.obj_y.location.y = self.wall_thickness
        self.left_side_wall.obj_x.location.x = self.left_return_length
        self.left_side_wall.obj_bp.mv.name_object = "Wall A"
        
        self.back_wall.obj_z.location.z = self.wall_height
        self.back_wall.obj_y.location.y = self.wall_thickness
        self.back_wall.obj_x.location.x = self.back_wall_length
        self.back_wall.obj_bp.mv.name_object = "Wall B"
        
        self.right_side_wall.obj_z.location.z = self.wall_height
        self.right_side_wall.obj_y.location.y = self.wall_thickness
        self.right_side_wall.obj_x.location.x = self.right_return_length
        self.right_side_wall.obj_bp.mv.name_object = "Wall C"
    
        self.left_side_wall.obj_z.hide = True
        self.left_side_wall.obj_y.hide = True
        self.left_side_wall.obj_x.hide = True
        self.back_wall.obj_z.hide = True
        self.back_wall.obj_y.hide = True
        self.back_wall.obj_x.hide = True
        self.right_side_wall.obj_z.hide = True
        self.right_side_wall.obj_y.hide = True
        self.right_side_wall.obj_x.hide = True
    
    def update_wall_properties(self,context):
        if self.props.room_type == 'SQUARE':
            self.update_square_room()
        if self.props.room_type == 'LSHAPE':
            self.update_l_shape_wall()
        if self.props.room_type == 'USHAPE':
            self.update_u_shape_wall()
        if self.props.room_type == 'SINGLE':
            self.update_single_wall()
        
    def create_wall(self,context):
        wall = fd_types.Wall()
        wall.create_wall()
        wall.build_wall_mesh()
        wall.obj_bp.location = (0,0,0)
        return wall
    
    def build_sqaure_room(self,context):
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
        
        bp = utils.get_group(os.path.join(os.path.dirname(__file__),
                                          "Entry Doors",
                                          self.props.entry_door_fn[self.props.entry_door_type]))
        
        self.door = fd_types.Assembly(bp)
        self.door.obj_bp.mv.dont_export = True
        self.door.obj_bp.mv.property_id = "lm_entry_doors.entry_door_prompts"
        self.door.obj_bp.mv.mirror_y = False
        self.door.obj_bp.mv.type_group = 'PRODUCT'
        self.door.obj_bp.mv.product_type = "Entry Door"
        self.door.obj_bp.parent = self.entry_wall.obj_bp
        self.door.draw_as_hidden_line()
        objs = utils.get_child_objects(self.door.obj_bp)
        
        for obj_bool in objs:
            obj_bool.draw_type = 'TEXTURED'
            obj_bool.mv.property_id = "lm_entry_doors.entry_door_prompts"
            if obj_bool.mv.use_as_bool_obj:
                mod = entry_wall.modifiers.new(obj_bool.name,'BOOLEAN')
                mod.object = obj_bool
                mod.operation = 'DIFFERENCE'
        
        utils.connect_objects_location(self.left_side_wall.obj_x,self.back_wall.obj_bp)
        utils.connect_objects_location(self.back_wall.obj_x,self.right_side_wall.obj_bp)
        utils.connect_objects_location(self.right_side_wall.obj_x,self.entry_wall.obj_bp)
        
    def build_single_wall(self,context):
        self.back_wall = self.create_wall(context)
        
    def build_l_shape_room(self,context):
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

        utils.connect_objects_location(self.left_side_wall.obj_x,self.back_wall.obj_bp)
        
    def build_u_shape_room(self,context):
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
        
        utils.connect_objects_location(self.left_side_wall.obj_x,self.back_wall.obj_bp)
        utils.connect_objects_location(self.back_wall.obj_x,self.right_side_wall.obj_bp)
        
    def add_molding(self, molding_type, wall, points):
        bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=False)
        obj_curve = bpy.context.active_object
        obj_curve.modifiers.new("Edge Split",type='EDGE_SPLIT')
        obj_curve.data.splines.clear()
        obj_curve.data.show_handles = False
        obj_curve.cabinetlib.type_mesh = 'SOLIDSTOCK'
        obj_curve.parent = wall.obj_bp
        
        bpy.ops.fd_object.add_material_slot(object_name=obj_curve.name)
        bpy.ops.cabinetlib.sync_material_slots(object_name=obj_curve.name)
        obj_curve.cabinetlib.material_slots[0].pointer_name = "Molding"
        obj_curve.data.dimensions = '2D'
        utils.assign_materials_from_pointers(obj_curve)  
        
        if molding_type == "base":
            obj_curve.location = (0, 0, 0)
            obj_curve.data.bevel_object = self.base_molding_pro
            obj_curve.mv.name_object = wall.obj_bp.mv.name_object + " Base Molding"
            obj_curve.name = wall.obj_bp.mv.name_object + " Base Molding"
            obj_curve.mv.solid_stock = self.base_molding_pro.name
            self.set_molding_points(obj_curve,points)
            
        elif molding_type == "crown":
            pro_height = self.crown_molding_pro.dimensions.y
            obj_curve.location = (0, 0, self.wall_height - pro_height)
            obj_curve.data.bevel_object = self.crown_molding_pro
            obj_curve.mv.name_object = wall.obj_bp.mv.name_object + " Crown Molding"
            obj_curve.name = wall.obj_bp.mv.name_object + " Crown Molding"
            obj_curve.mv.solid_stock = self.crown_molding_pro.name
            self.set_molding_points(obj_curve,points)

        return obj_curve

    def add_molding_to_room(self,molding_type='crown'):
        if self.left_side_wall:
            points = [(0,0,0),(self.left_side_wall.obj_x.location.x,0,0)]
            self.add_molding(molding_type=molding_type,wall=self.left_side_wall,points=points)
            
        if self.back_wall:
            points = [(0,0,0),(self.back_wall.obj_x.location.x,0,0)]
            self.add_molding(molding_type=molding_type,wall=self.back_wall,points=points)
            
        if self.right_side_wall:
            points = [(0,0,0),(self.right_side_wall.obj_x.location.x,0,0)]
            self.add_molding(molding_type=molding_type,wall=self.right_side_wall,points=points)
            
        if self.entry_wall:
            if molding_type == 'base':
                # If the base molding is being added we need to wrap around the entry way.
                # This currently only works for the square room.
                products = self.entry_wall.get_wall_groups()
                entry_door = fd_types.Assembly(products[0])
                points = [(0,0,0),(entry_door.obj_bp.location.x,0,0)]
                self.add_molding(molding_type=molding_type,wall=self.entry_wall,points=points)
                
                points = [(entry_door.obj_bp.location.x + entry_door.obj_x.location.x,0,0),
                          (self.entry_wall.obj_x.location.x,0,0)]
                self.add_molding(molding_type=molding_type,wall=self.entry_wall,points=points)
            else:
                points = [(0,0,0),(self.entry_wall.obj_x.location.x,0,0)]
                self.add_molding(molding_type=molding_type,wall=self.entry_wall,points=points)
        
    def invoke(self,context,event):
        self.wall_mesh_objs = []
        utils.delete_obj_list(bpy.data.objects)
        
        self.props = bpy.context.scene.fd_roombuilder
        
        for old_wall in self.props.walls:
            self.props.walls.remove(0)
        
        self.wall_height = context.scene.mv.default_wall_height
        self.wall_thickness = context.scene.mv.default_wall_depth
        
        objects = bpy.data.objects
        
        if self.props.add_base_molding:
            if self.props.base_molding in objects:
                self.base_molding_pro = objects[self.props.base_molding]
            else:
                self.base_molding_pro = utils.get_object(os.path.join(BASE_PRO_PATH, self.props.base_molding + ".blend"))
                
        if self.props.add_crown_molding:
            if self.props.crown_molding in objects:
                self.crown_molding_pro = objects[self.props.crown_molding]
            else:  
                self.crown_molding_pro = utils.get_object(os.path.join(CROWN_PRO_PATH, self.props.crown_molding + ".blend"))
                
        if self.props.room_type == 'SQUARE':
            self.build_sqaure_room(context)
        if self.props.room_type == 'LSHAPE':
            self.build_l_shape_room(context)
        if self.props.room_type == 'USHAPE':
            self.build_u_shape_room(context)
        if self.props.room_type == 'SINGLE':
            self.build_single_wall(context)
        
        self.update_wall_properties(context)
        self.set_camera_position(context)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)

    def execute(self, context):
        self.clicked_ok = True

        # Do not create room if room category not selected
        if self.props.room_category == 'Please Select':
            self.clear_room_objects()
            message = "Room not created: Category not Selected"
            return bpy.ops.snap.message_box('INVOKE_DEFAULT', message=message)

        #FIX MESH SIZE FOR EDITING AFTER ROOM CREATION
        for mesh in self.wall_mesh_objs:
            bpy.ops.fd_assembly.connect_meshes_to_hooks_in_assembly(object_name = mesh.name)
        
        #HIDE EMPTIES AFTER CONNECTING HOOKS
        for obj in bpy.context.scene.objects:
            if obj.type == 'EMPTY':
                obj.hide = True
        
        if self.props.add_base_molding:
            self.add_molding_to_room(molding_type="base")
            
        if self.props.add_crown_molding:
            self.add_molding_to_room(molding_type="crown")
        
        bpy.ops.fd_roombuilder.collect_walls()         
        
        if 'fd_projects' in bpy.context.user_preferences.addons.keys():
            if self.add_to_project:
                bpy.ops.project.add_room(room_name=self.room_name, room_category=self.props.room_category)

        return {'FINISHED'}

    def clear_room_objects(self):
        del_objs = []

        if self.left_side_wall:
            utils.delete_object_and_children(self.left_side_wall.obj_bp)
        if self.back_wall:
            utils.delete_object_and_children(self.back_wall.obj_bp)
        if self.entry_wall:
            utils.delete_object_and_children(self.entry_wall.obj_bp)
        if self.right_side_wall:
            utils.delete_object_and_children(self.right_side_wall.obj_bp)
        if self.door:
            utils.delete_object_and_children(self.door.obj_bp)
        if self.base_molding_pro:
            del_objs.append(self.base_molding_pro)
        if self.crown_molding_pro:
            del_objs.append(self.crown_molding_pro)
        for obj in self.wall_mesh_objs:
            del_objs.append(obj)
        if self.floor:
            del_objs.append(self.floor)

        utils.delete_obj_list(del_objs)

    def __del__(self):
        if not self.clicked_ok:
            self.clear_room_objects()          

    def draw(self,context):
        layout = self.layout
        box = layout.box()

        if 'fd_projects' in bpy.context.user_preferences.addons.keys():
            wm = context.window_manager.fd_project
            project = wm.projects[wm.project_index]
            box.prop(self, "add_to_project", text="Add to Active Project: {}".format(project.name))

            if self.add_to_project:
                box.prop(self, "room_name", text="Room Name")
                
        row = box.row()
        #row.prop_enum(self.props, 'room_category','Please Select',text="Room Category")
        row.prop(self.props, "room_category",text="Room Category")

        if(self.props.room_category != "Please Select"):
            if self.props.room_type == 'SQUARE':
            
                row = box.row()
                row.label("Room Length:")
                row.prop(self,"back_wall_length",text="")
                
                row = box.row()
                row.label("Room Depth:")
                row.prop(self,"side_wall_length",text="")
                
                row = box.row()
                row.label('Return Walls:')
                row.prop(self,"left_return_length",text="Left")
                row.prop(self,"right_return_length",text='Right')
                
                row = box.row()
                row.label("Opening Height:")
                row.prop(self,"opening_height",text="")
                
            if self.props.room_type == 'SINGLE':
                row = box.row()
                row.label("Wall Length:")
                row.prop(self,"back_wall_length",text="")
            
            if self.props.room_type == 'LSHAPE':
                row = box.row()
                row.label("Back Wall Length:")
                row.prop(self,"back_wall_length",text="")
                
                row = box.row()
                row.label("Left Wall Length:")
                row.prop(self,"left_return_length",text="")
            
            if self.props.room_type == 'USHAPE':
                row = box.row()
                row.label("Back Wall Length:")
                row.prop(self,"back_wall_length",text="")
                
                row = box.row()
                row.label("Left Wall Length:")
                row.prop(self,"left_return_length",text="")
            
                row = box.row()
                row.label("Right Wall Length:")
                row.prop(self,"right_return_length",text="")
        
class OPERATOR_Collect_Walls(Operator):
    bl_idname = "fd_roombuilder.collect_walls"
    bl_label = "Collect Walls" 
    bl_options = {'UNDO'}

    add_to_project = BoolProperty(name="Add to Selected Project")
    room_name = StringProperty(name="Room Name", default="New Room")

#     floor = None

    @classmethod
    def poll(cls, context):
        return len(context.scene.fd_roombuilder.walls) < 1

    def check(self, context):
        return True

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row = box.row()
        props = context.scene.fd_roombuilder

        if 'fd_projects' in bpy.context.user_preferences.addons.keys():
            wm = context.window_manager.fd_project
            project = wm.projects[wm.project_index]
            box.prop(self, "add_to_project", text="Add to Active Project: {}".format(project.name))

            if self.add_to_project:
                row.prop(self, "room_name", text="Room Name")
                row = box.row()
                row.prop(props, "room_category",text="Room Category")

    def assign_floor_material(self,context,obj):
        props = context.scene.fd_roombuilder
        if props.floor_type == 'CARPET':
            material = utils.get_material((FLOORING_LIBRARY_NAME,CARPET_CATEGORY_NAME),props.carpet_material)
        if props.floor_type == 'WOOD':    
            material = utils.get_material((FLOORING_LIBRARY_NAME,HARDWOOD_CATEGORY_NAME),props.wood_floor_material)
        if props.floor_type == 'TILE':
            material = utils.get_material((FLOORING_LIBRARY_NAME,TILE_CATEGORY_NAME),props.tile_material)
        if material:
            bpy.ops.fd_object.unwrap_mesh(object_name=obj.name)
            bpy.ops.fd_object.add_material_slot(object_name=obj.name)
            for i, mat in enumerate(obj.material_slots):
                mat.material = material

    def assign_wall_material(self,context,obj):
        props = context.scene.fd_roombuilder
        material = utils.get_material((PAINT_LIBRARY_NAME,PAINT_CATEGORY_NAME),props.wall_material)
        if material:
            bpy.ops.fd_object.unwrap_mesh(object_name=obj.name)
            bpy.ops.fd_object.add_material_slot(object_name=obj.name)
            for i, mat in enumerate(obj.material_slots):
                mat.material = material
                
    def execute(self, context):
        props = context.scene.fd_roombuilder
        mv = context.scene.mv
        
        for old_wall in props.walls:
            props.walls.remove(0)
        
        bpy.ops.fd_object.draw_floor_plane()
        obj_floor = context.active_object
        obj_floor.name = "Floor"
        obj_floor.mv.name_object = "Floor"
        obj_floor.fd_roombuilder.is_floor = True
        self.assign_floor_material(context,obj_floor)
        
        bpy.ops.fd_object.draw_floor_plane()
        ceiling = context.active_object
        ceiling.name = 'Ceiling'
        ceiling.mv.name_object = "Ceiling"
        ceiling.location.z = mv.default_wall_height
        ceiling.hide = True
        ceiling.fd_roombuilder.is_ceiling = True
        
        bpy.ops.fd_object.add_room_lamp()
        
        for obj in context.scene.objects:
            if obj.mv.type == 'BPWALL':
                wall = fd_types.Wall(obj)
                self.assign_wall_material(context, wall.get_wall_mesh())
                wall = props.walls.add()
                wall.name = obj.mv.name_object
                wall.bp_name = obj.name
            if obj.fd_roombuilder.is_floor:
                floor = props.walls.add()
                floor.name = obj.mv.name_object
                floor.bp_name = obj.name
            if obj.fd_roombuilder.is_ceiling:
                ceiling = props.walls.add()
                ceiling.name = obj.mv.name_object
                ceiling.bp_name = obj.name

        if 'fd_projects' in bpy.context.user_preferences.addons.keys():
            if self.add_to_project:
                bpy.ops.project.add_room(room_name=self.room_name, room_category = props.room_category)          

        return {'FINISHED'}
        
class OPERATOR_Delete_Obstacle(Operator):
    bl_idname = "fd_roombuilder.delete_obstacle"
    bl_label = "Delete Obstacle" 
    bl_options = {'UNDO'}

    obstacle_bp_name = StringProperty(name="Obstacle BP Name",
                                      description="Pass the base point name to reposition an existing obstacle",
                                      default="")

    def execute(self, context):
        props = bpy.context.scene.fd_roombuilder
        wall = props.walls[props.wall_index]
        
        for index, obstacle in enumerate(wall.obstacles):
            if obstacle.bp_name == self.obstacle_bp_name:
                wall.obstacles.remove(index)
            
        obj_bp = context.scene.objects[self.obstacle_bp_name]
        
        utils.delete_object_and_children(obj_bp)
        return {'FINISHED'}

class OPERATOR_Hide_Plane(Operator):
    bl_idname = "fd_roombuilder.hide_plane"
    bl_label = "Hide Plane"
    
    object_name = StringProperty("Object Name",default="")
    
    def execute(self, context):
        if self.object_name in context.scene.objects:
            obj = context.scene.objects[self.object_name]
        else:
            obj = context.active_object

        children = utils.get_child_objects(obj)
        
        for child in children:
            child.hide = True
        
        obj.hide = True
        
        return {'FINISHED'}

class OPERATOR_Hide_Show_Wall(Operator):
    bl_idname = "fd_roombuilder.hide_show_wall"
    bl_label = "Hide Wall"
    
    wall_bp_name = StringProperty("Wall BP Name",default="")
    
    hide = BoolProperty("Hide",default=False)
    
    def execute(self, context):
        # This assumes that layer 1 is the layer you have everything on
        # Layer 2 is the layer we are placing the hidden objects on
        # This is kind of a hack there might be a better way to do this.
        # But we cannot hide objects on a wall becuase many hide properties
        # are driven my python drivers and after the scene recalcs hidden objects
        # are shown again.
        hide_layers = (False,True,False,False,False,False,False,False,False,False,
                       False,False,False,False,False,False,False,False,False,False)
        
        visible_layers = (True,False,False,False,False,False,False,False,False,False,
                          False,False,False,False,False,False,False,False,False,False)        
        
        obj = context.scene.objects[self.wall_bp_name]
        
        wall_bp = utils.get_wall_bp(obj)
        
        children = utils.get_child_objects(wall_bp)
        
        for child in children:
            if self.hide:
                child.layers = hide_layers
            else:
                child.layers = visible_layers
            
        wall_bp.hide = self.hide
        
        return {'FINISHED'}

class OPERATOR_Delete_Room(Operator):
    bl_idname = "fd_roombuilder.delete_room"
    bl_label = "Delete Room"

    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)

    def execute(self, context):
        utils.delete_obj_list(bpy.data.objects)
        
        props = context.scene.fd_roombuilder
        
        for old_wall in props.walls:
            props.walls.remove(0)        
            
        return {'FINISHED'}

    def draw(self,context):
        layout = self.layout
        box = layout.box()
        box.label("Are you sure you want to delete the room?")

class OPERATOR_New_Room(Operator):
    bl_idname = "fd_roombuilder.new_room"
    bl_label = "New Room"

    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)

    def execute(self, context):
        bpy.ops.fd_roombuilder.delete_room()
        bpy.ops.fd_roombuilder.build_room('INVOKE_DEFAULT')
            
        return {'FINISHED'}

    def draw(self,context):
        layout = self.layout
        box = layout.box()
        col = box.column()

        col.label("Creating a new room will clear the current room from the scene.")        
        col.label("Are you sure you want to delete the existing room?")        

class OPERATOR_Show_Plane(Operator):
    bl_idname = "fd_roombuilder.show_plane"
    bl_label = "Show Plane"
    
    object_name = StringProperty("Object Name",default="")
    
    def execute(self, context):
        if self.object_name in context.scene.objects:
            obj = context.scene.objects[self.object_name]
        else:
            obj = context.active_object

        children = utils.get_child_objects(obj)
        
        for child in children:
            if child.type != 'EMPTY':
                child.hide = False
        
        obj.hide = False
        
        return {'FINISHED'}

class OPERATOR_Select_Two_Points(Operator):
    bl_idname = "fd_roombuilder.select_two_points"
    bl_label = "Select Two Points"
    bl_options = {'UNDO'}
    
    #READONLY
    drawing_plane = None

    first_point = (0,0,0)
    second_point = (0,0,0)
    
    header_text = "Select the First Point"
    
    def cancel_drop(self,context,event):
        context.window.cursor_set('DEFAULT')
        utils.delete_obj_list([self.drawing_plane])
        return {'FINISHED'}
        
    def __del__(self):
        bpy.context.area.header_text_set()
        
    def event_is_cancel(self,event):
        if event.type == 'RIGHTMOUSE' and event.value == 'PRESS':
            return True
        elif event.type == 'ESC' and event.value == 'PRESS':
            return True
        else:
            return False
            
    def modal(self, context, event):
        context.window.cursor_set('PAINT_BRUSH')
        context.area.tag_redraw()
        selected_point, selected_obj = utils.get_selection_point(context,event,objects=[self.drawing_plane]) #Pass in Drawing Plane
        bpy.ops.object.select_all(action='DESELECT')
        if selected_obj:
            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                if self.first_point != (0,0,0):
                    self.second_point = selected_point
                    
                    distance = utils.calc_distance(self.first_point,self.second_point)
                    
                    diff = context.scene.fd_roombuilder.background_image_scale / distance

                    view = context.space_data
                    for bg in view.background_images:
                        bg_size = bg.size
                        bg.size = bg_size*diff
                    return self.cancel_drop(context,event)
                else:
                    self.first_point = selected_point

        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}
            
        if self.event_is_cancel(event):
            return self.cancel_drop(context,event)
            
        return {'RUNNING_MODAL'}
        
    def execute(self,context):
        self.first_point = (0,0,0)
        self.second_point = (0,0,0)
        bpy.ops.mesh.primitive_plane_add()
        plane = context.active_object
        plane.location = (0,0,0)
        self.drawing_plane = context.active_object
        self.drawing_plane.draw_type = 'WIRE'
        self.drawing_plane.dimensions = (100,100,1)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    
def register():
    bpy.utils.register_class(Scene_Props)
    bpy.types.Scene.fd_roombuilder = PointerProperty(type = Scene_Props)
    bpy.utils.register_class(Object_Props)
    bpy.types.Object.fd_roombuilder = PointerProperty(type = Object_Props)
    
    bpy.utils.register_class(PANEL_Room_Builder)
    bpy.utils.register_class(FD_UL_walls)
    bpy.utils.register_class(FD_UL_obstacles)
    
    bpy.utils.register_class(OPERATOR_Draw_Walls)
    bpy.utils.register_class(OPERATOR_Hide_Show_Wall)
    bpy.utils.register_class(OPERATOR_Add_Obstacle)
    bpy.utils.register_class(OPERATOR_Add_Floor_Obstacle)
    bpy.utils.register_class(OPERATOR_Build_Room)
    bpy.utils.register_class(OPERATOR_Delete_Room)
    bpy.utils.register_class(OPERATOR_New_Room)
    bpy.utils.register_class(OPERATOR_Collect_Walls)
    bpy.utils.register_class(OPERATOR_Delete_Obstacle)
    bpy.utils.register_class(OPERATOR_Hide_Plane)
    bpy.utils.register_class(OPERATOR_Show_Plane)
    bpy.utils.register_class(OPERATOR_Select_Two_Points)

    carpet_coll = bpy.utils.previews.new()
    carpet_coll.my_previews_dir = ""
    carpet_coll.my_previews = ()

    wood_floor_coll = bpy.utils.previews.new()
    wood_floor_coll.my_previews_dir = ""
    wood_floor_coll.my_previews = ()

    tile_floor_coll = bpy.utils.previews.new()
    tile_floor_coll.my_previews_dir = ""
    tile_floor_coll.my_previews = ()

    paint_coll = bpy.utils.previews.new()
    paint_coll.my_previews_dir = ""
    paint_coll.my_previews = ()
    
    base_molding_coll = bpy.utils.previews.new()
    base_molding_coll.my_previews_dir = ""
    base_molding_coll.my_previews = ()
    
    crown_molding_coll = bpy.utils.previews.new()
    crown_molding_coll.my_previews_dir = ""
    crown_molding_coll.my_previews = ()         
    
    preview_collections["carpet"] = carpet_coll
    preview_collections["wood_floor"] = wood_floor_coll
    preview_collections["tile"] = tile_floor_coll
    preview_collections["paint"] = paint_coll
    preview_collections["base molding"] = base_molding_coll
    preview_collections["crown molding"] = crown_molding_coll

def unregister():
    bpy.utils.unregister_class(Scene_Props)
    del bpy.types.Scene.fd_roombuilder
    bpy.utils.unregister_class(Object_Props)
    del bpy.types.Object.fd_roombuilder
    
    bpy.utils.unregister_class(PANEL_Room_Builder)
    bpy.utils.unregister_class(FD_UL_walls)
    bpy.utils.unregister_class(FD_UL_obstacles)
    
    bpy.utils.unregister_class(OPERATOR_Draw_Walls)
    bpy.utils.unregister_class(OPERATOR_Hide_Show_Wall)
    bpy.utils.unregister_class(OPERATOR_Add_Obstacle)
    bpy.utils.unregister_class(OPERATOR_Add_Floor_Obstacle)
    bpy.utils.unregister_class(OPERATOR_Build_Room)
    bpy.utils.unregister_class(OPERATOR_Delete_Room)
    bpy.utils.unregister_class(OPERATOR_New_Room)
    bpy.utils.unregister_class(OPERATOR_Collect_Walls)
    bpy.utils.unregister_class(OPERATOR_Delete_Obstacle)
    bpy.utils.unregister_class(OPERATOR_Hide_Plane)
    bpy.utils.unregister_class(OPERATOR_Show_Plane)
    bpy.utils.unregister_class(OPERATOR_Select_Two_Points)
