
import bpy
from bpy.types import Panel, UIList
from snap import sn_unit, sn_types
from snap.sn_unit import meter_to_active_unit


class ROOM_BUILDER_UL_walls(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if item.bp_name in context.view_layer.objects:
            wall_bp = context.view_layer.objects[item.bp_name]

            obstacle_count = len(item.obstacles)
            count_text = ""
            if obstacle_count > 0:
                count_text = "(" + str(obstacle_count) + ")"

            if wall_bp.sn_roombuilder.is_floor or wall_bp.sn_roombuilder.is_ceiling:
                layout.label(text="", icon='MESH_GRID')
                layout.label(text=item.name + "   " + count_text)
                area = round(meter_to_active_unit(wall_bp.dimensions.x) * meter_to_active_unit(wall_bp.dimensions.y))
                layout.label(text="Area: " + str(area))
                if wall_bp.hide_viewport:
                    layout.operator('sn_roombuilder.show_plane',
                                    text="",
                                    icon='RESTRICT_VIEW_ON',
                                    emboss=False).object_name = wall_bp.name
                else:
                    layout.operator('sn_roombuilder.hide_plane',
                                    text="",
                                    icon='RESTRICT_VIEW_OFF',
                                    emboss=False).object_name = wall_bp.name
            else:
                wall = sn_types.Wall(obj_bp=wall_bp)
                layout.label(text="", icon='SNAP_FACE')
                layout.label(text=item.name + "   " + count_text)

                # we need to round  and remove decimal zero, if it is a whole number
                numLen = round(sn_unit.meter_to_active_unit(wall.obj_x.location.x), 3)
                if int(numLen) == numLen:
                    numLen = int(numLen)

                layout.label(text="Length: " + str(numLen))
                wall_mesh = list(filter(lambda a: 'Wall' in a.name and a.type == 'MESH', wall_bp.children))[0]
                if wall_mesh.hide_viewport:
                    props = layout.operator('sn_roombuilder.hide_show_wall',
                                            text="",
                                            icon='RESTRICT_VIEW_ON',
                                            emboss=False)
                    props.wall_bp_name = wall_bp.name
                    props.hide = False
                else:
                    props = layout.operator('sn_roombuilder.hide_show_wall',
                                            text="",
                                            icon='RESTRICT_VIEW_OFF',
                                            emboss=False)
                    props.wall_bp_name = wall_bp.name
                    props.hide = True


class ROOM_BUILDER_UL_obstacles(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        wall = context.scene.sn_roombuilder.walls[context.scene.sn_roombuilder.wall_index]
        wall_obj = context.view_layer.objects[wall.bp_name]

        layout.label(text="", icon='PLUGIN')
        layout.label(text=item.name)

        if wall_obj.sn_roombuilder.is_floor or wall_obj.sn_roombuilder.is_ceiling:
            layout.operator('sn_roombuilder.add_floor_obstacle', text="", icon='INFO').obstacle_bp_name = item.bp_name
        else:
            layout.operator('sn_roombuilder.add_obstacle', text="", icon='INFO').obstacle_bp_name = item.bp_name

        layout.operator('sn_roombuilder.delete_obstacle', text="", icon='X').obstacle_bp_name = item.bp_name


class ROOM_BUILDER_PT_Room_Builder(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "Room Builder"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 1

    def draw_header(self, context):
        layout = self.layout
        layout.label(text='', icon='MOD_BUILD')

    def draw(self, context):
        layout = self.layout
        props = context.scene.sn_roombuilder
        props_snap = context.scene.snap

        main_box = layout.box()
        box = main_box.box()
        box.label(text='Room Setup:', icon='SNAP_PEEL_OBJECT')
        box.prop(props, 'room_type', text="Room Template")

        row = box.row(align=True)
        row.prop(props, 'floor_type', text="Floor", icon='FILE_FOLDER')

        if props.floor_type == 'CARPET':
            row.prop(props, 'carpet_material', text="")
        if props.floor_type == 'WOOD':
            row.prop(props, 'wood_floor_material', text="")
        if props.floor_type == 'TILE':
            row.prop(props, 'tile_material', text="")

        row = box.row(align=True)
        row.prop(props, 'paint_type', text="Walls", icon='FILE_FOLDER')
        row.prop(props, 'wall_material', text="")

        row = box.row()
        row.prop(props, 'add_base_molding', text="Include Base Molding:")

        if props.add_base_molding:
            row.prop(props, 'base_molding_height', text="")

        row = box.row()
        row.prop(props, 'add_crown_molding', text="Include Crown Molding:")

        if props.add_crown_molding:
            row.prop(props, 'crown_molding_height', text="")

        if props.room_type == 'SQUARE':
            row = box.row(align=True)
            row.prop(props, 'entry_door_type', text="Door", icon='FILE_FOLDER')

        row = box.row(align=True)
        row.prop(props_snap, 'default_wall_height', text="Ceiling Height")
        row.prop(props_snap, 'default_wall_depth')

        if props.room_type == 'CUSTOM':
            row = box.row()
            if len(bpy.data.objects) == 0:
                row.operator('sn_roombuilder.draw_walls', text="Draw Walls", icon='GREASEPENCIL')
            else:
                # we only want to show_draw walls while collect_walls has not been executed
                if not bpy.data.objects.get('Floor'):
                    row.operator('sn_roombuilder.draw_walls', text="Draw Walls", icon='GREASEPENCIL')
                else:
                    row.operator('sn_roombuilder.new_custom_room', text="Draw New Room", icon='GREASEPENCIL')
                
                row.operator('sn_roombuilder.collect_walls', icon='FILE_REFRESH')
                row.operator('sn_roombuilder.delete_room', text="Delete Room", icon='X')

            # Adds background image functionality. Unsure if we are going to use
            # self.draw_custom_room_options(layout, context)
        else:
            col = box.column()
            col.scale_y = 1.3
            if len(bpy.data.objects) > 0:
                col.operator('sn_roombuilder.delete_room', text="Delete Room", icon='X')
                col.operator('sn_roombuilder.new_room', text="New Room", icon='PLUS')
            else:
                col.operator('sn_roombuilder.build_room', text="Build Room", icon='SNAP_PEEL_OBJECT')

        if len(props.walls) > 0:
            box = main_box.box()
            row = box.row(align=True)
            row.label(text="Room Objects:", icon='SNAP_FACE')
            row.prop_enum(props, 'obstacle_hide', 'SHOW', icon='RESTRICT_VIEW_OFF', text="")
            row.prop_enum(props, 'obstacle_hide', 'HIDE', icon='RESTRICT_VIEW_ON', text="")

            box.template_list("ROOM_BUILDER_UL_walls", "", props, "walls", props, "wall_index", rows=len(props.walls))
            wall = props.walls[props.wall_index]
            if wall.bp_name in context.view_layer.objects:
                obj = context.view_layer.objects[wall.bp_name]
                if obj.sn_roombuilder.is_ceiling:
                    box.operator('sn_roombuilder.add_floor_obstacle', text="Add Obstacle To Ceiling", icon='PLUGIN')
                elif obj.sn_roombuilder.is_floor:
                    box.operator('sn_roombuilder.add_floor_obstacle', text="Add Obstacle To Floor", icon='PLUGIN')
                else:
                    box.operator('sn_roombuilder.add_obstacle', text="Add Obstacle To Wall", icon='PLUGIN')

                if len(wall.obstacles) > 0:
                    box.template_list("ROOM_BUILDER_UL_obstacles", "",
                                      wall,
                                      "obstacles",
                                      wall,
                                      "obstacle_index",
                                      rows=4)

    def draw_custom_room_options(self, layout, context):
        view = context.space_data
        use_multiview = context.scene.render.use_multiview

        mainbox = layout.box()
        mainbox.operator("view3d.background_image_add", text="Add Image", icon='ADD')

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
                        box.prop(bg, "draw_depth", expand=False, text="Draw Depth")
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
                    row.label(text="Image Opacity")
                    row.prop(bg, "opacity", slider=True, text="")

                    row = box.row()
                    row.label(text="Rotation:")
                    row.prop(bg, "rotation", text="")

                    row = box.row()
                    row.label(text="Location:")
                    row.prop(bg, "offset_x", text="X")
                    row.prop(bg, "offset_y", text="Y")

                    row = box.row()
                    row.label(text="Flip Image:")
                    row.prop(bg, "use_flip_x", text="Horizontally")
                    row.prop(bg, "use_flip_y", text="Vertically")

                    row = box.row()
                    row.prop(context.scene.sn_roombuilder, "background_image_scale", text="Known Dimension")
                    row.operator('sn_roombuilder.select_two_points', text="Select Two Points", icon='MAN_TRANS')

                    row = box.row()
                    row.label(text="Image Size:")
                    row.prop(bg, "size", text="")


classes = (
    ROOM_BUILDER_PT_Room_Builder,
    ROOM_BUILDER_UL_walls,
    ROOM_BUILDER_UL_obstacles,
)

register, unregister = bpy.utils.register_classes_factory(classes)
