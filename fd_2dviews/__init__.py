# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import psutil
import time
import os
import math
from . import report_2d_drawings
from . import operators
from . import opengl_dim
from mv import utils, fd_types, unit
from bpy.props import BoolProperty, EnumProperty
import bpy
bl_info = {
    "name": "2D Views",
    "author": "Ryan Montes",
    "version": (1, 0, 0),
    "blender": (2, 7, 0),
    "location": "Tools Shelf",
    "description": "This add-on creates a UI to generate 2D Views",
    "warning": "",
    "wiki_url": "",
    "category": "SNaP"
}


class WM_PROPERTIES_2d_views(bpy.types.PropertyGroup):

    expand_options = bpy.props.BoolProperty(name="Expand Dimension Options",
                                            description="Expands Dimension Options Box",
                                            default=True)

    page_layout_setting = EnumProperty(name="Page Layout Settings",
                                       items=[
                                           ('PLAN+1ELVS', "Plan and elevations",
                                            'Plan on top plus three elevations (U-Shaped)'),
                                           ('3ELVS', 'Three per page',
                                               'Three elevations per page'),
                                           ('2ELVS', "Two per page",
                                               'Two elevations per page'),
                                           ('SINGLE', "One per page",
                                               'One elevation per page'),
                                       ],
                                       default='SINGLE')

    paper_size = EnumProperty(name="Paper Size",
                              items=[
                                  ('ELEVENSEVENTEEN', '11x17',
                                   'US Ledger Paper - 11 x 17 inches - ANSI B'),
                                  ('LEGAL', 'Legal',
                                   'US Legal Paper - 8.5 x 14 inches'),
                                  ('LETTER', 'Letter',
                                   'US Letter Paper - 8.5 x 11 inches')
                              ],
                              default='LEGAL')


bpy.utils.register_class(WM_PROPERTIES_2d_views)


class PANEL_2d_views(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "2D Views"
    bl_category = "SNaP"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        layout = self.layout
        layout.label('', icon='ALIGN')

    def draw_dim_options(self, context, layout):
        scene = context.scene
        dim_props = scene.mv.opengl_dim
        sys_units = scene.unit_settings.system
        box = layout.box()

        row = box.row()

        if dim_props.gl_dim_units == 'AUTO':
            row.label("Units:" +
                      "                    (" +
                      sys_units.title() +
                      ")")
        else:
            row.label("Units:")

        row.prop(dim_props, 'gl_dim_units', text="")

        row = box.row()
        row.label("Arrow Type:")
        row.prop(dim_props, 'gl_arrow_type', text="")
        row = box.row()
        row.label("Color:")
        row.prop(dim_props, 'gl_default_color', text="")
        row = box.row()

        if dim_props.gl_dim_units in ('INCH', 'FEET') or dim_props.gl_dim_units == 'AUTO' and sys_units == 'IMPERIAL':
            row.label("Round to the nearest:")
            row.prop(dim_props, 'gl_imperial_rd_factor', text="")
            row = box.row()
            row.label("Number format:")
            row.prop(dim_props, 'gl_number_format', text="")

        else:
            row.label("Precision:")
            row.prop(dim_props, 'gl_precision', text="")

        row = box.row()
        row.label("Text Size:")
        row.prop(dim_props, 'gl_font_size', text="")
        row = box.row()
        row.label("Arrow Size:")
        row.prop(dim_props, 'gl_arrow_size', text="")

    def draw(self, context):
        props = context.window_manager.views_2d
        fd_wm = context.window_manager.mv

        layout = self.layout
        scene = context.scene
        panel_box = layout.box()

        # ----
        col = panel_box.column(align=True)
        col.prop(fd_wm, 'use_opengl_dimensions',
                 text='{}able Dimensions'.format(
                     "Dis" if fd_wm.use_opengl_dimensions else "En"),
                 icon='VISIBLE_IPO_OFF' if fd_wm.use_opengl_dimensions else 'VISIBLE_IPO_ON',
                 toggle=True)

        row = col.row(align=True)
        row.operator('fd_2d_views.add_dimension',
                     text='Add Dimension', icon='CURVE_NCURVE')
        row.operator('fd_2d_views.add_annotation',
                     text='Add Annotation', icon='ZOOMIN')

        row = col.row(align=True)
        row.operator("fd_2d_views.toggle_dimension_handles",
                     text="Show Dimension Handles", icon='OUTLINER_OB_EMPTY').turn_on = True
        row.operator("fd_2d_views.toggle_dimension_handles",
                     text="Hide Dimension Handles", icon='OUTLINER_OB_EMPTY').turn_on = False

        row = col.row(align=True)
        row.operator('fd_2d_views.dimension_interface',
                     text='Dimension Options', icon='SCRIPTWIN')
        # ----

#         options_box = panel_box.box()
#         row = options_box.row(align=True)
#         row.prop(props, 'expand_options', icon='TRIA_DOWN' if props.expand_options else 'TRIA_RIGHT', icon_only=True, emboss=False)
#         row.label("Dimension Options", icon='SCRIPTWIN')
#
#         if props.expand_options:
#             self.draw_dim_options(context, options_box)

        row = panel_box.row(align=True)
        row.scale_y = 1.3

        elv_scenes = []
        for scene in bpy.data.scenes:
            if scene.mv.elevation_scene:
                elv_scenes.append(scene)

        if len(elv_scenes) < 1:
            row.operator("fd_2d_views.genereate_2d_views",
                         text="Prepare 2D Views", icon='RENDERLAYERS')
        else:
            row.operator("fd_2d_views.genereate_2d_views",
                         text="", icon='FILE_REFRESH')
            row.operator("fd_2d_views.create_new_view", text="", icon='ZOOMIN')
            row.operator("2dviews.render_2d_views",
                         text="Render Selected Scenes", icon='RENDER_REGION')
            row.menu('MENU_elevation_scene_options',
                     text="", icon='DOWNARROW_HLT')
            panel_box.template_list("LIST_scenes",
                                    " ",
                                    bpy.data,
                                    "scenes",
                                    bpy.context.window_manager.mv,
                                    "elevation_scene_index")

        image_views = context.window_manager.mv.image_views

        if len(image_views) > 0:
            panel_box.label("Image Views", icon='RENDERLAYERS')
            row = panel_box.row()
            row.template_list("LIST_2d_images", " ", context.window_manager.mv,
                              "image_views", context.window_manager.mv, "image_view_index")
            col = row.column(align=True)
            col.operator('fd_2d_views.move_2d_image_item',
                         text="", icon='TRIA_UP').direction = 'UP'
            col.operator('fd_2d_views.move_2d_image_item', text="",
                         icon='TRIA_DOWN').direction = 'DOWN'
            row = panel_box.row(align=True)
            row.prop(props, 'page_layout_setting', "Elevations layout")
            paper_row = panel_box.row(align=True)
            paper_row.prop(props, 'paper_size', "Paper Size")
            panel_box.menu('MENU_2dview_reports', icon='FILE_BLANK')
#             panel_box.operator('2dviews.create_pdf',text="Create PDF",icon='FILE_BLANK')


class MENU_2dview_reports(bpy.types.Menu):
    bl_label = "2D Reports"

    """
    Report Templates are added to this menu
    """

    def draw(self, context):
        layout = self.layout


class MENU_elevation_scene_options(bpy.types.Menu):
    bl_label = "Elevation Scene Options"

    def draw(self, context):
        layout = self.layout
        layout.operator("fd_general.select_all_elevation_scenes",
                        text="Select All", icon='CHECKBOX_HLT').select_all = True
        layout.operator("fd_general.select_all_elevation_scenes",
                        text="Deselect All", icon='CHECKBOX_DEHLT').select_all = False
        layout.separator()
        layout.operator('fd_general.project_info',
                        text="View Project Info", icon='INFO')
        layout.operator("2dviews.create_snap_shot",
                        text="Create Snap Shot", icon='SCENE')
        layout.operator("fd_2d_views.append_to_view",
                        text="Append to View", icon='ZOOMIN')
        layout.separator()
        layout.operator("fd_scene.clear_2d_views",
                        text="Clear All 2D Views", icon='X')


class LIST_scenes(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        if item.mv.plan_view_scene or item.mv.elevation_scene:
            layout.label(item.mv.name_scene, icon='RENDER_REGION')
            layout.prop(item.mv, 'render_type_2d_view', text="")
            layout.prop(item.mv, 'elevation_selected', text="")
        else:
            layout.label(item.name, icon='SCENE_DATA')

    def filter_items(self, context, data, propname):
        flt_flags = []
        flt_neworder = []
        scenes = getattr(data, propname)
        helper_funcs = bpy.types.UI_UL_list

        if not flt_flags:
            flt_flags = [self.bitflag_filter_item] * len(scenes)

        for i, scene in enumerate(scenes):
            if scene.lm_closets.is_drill_scene:
                flt_flags[i] &= ~self.bitflag_filter_item

        flt_neworder = helper_funcs.sort_items_by_name(scenes, "name")

        return flt_flags, flt_neworder


class LIST_2d_images(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        layout.label(item.name, icon='RENDER_RESULT')
        layout.operator('2dviews.view_image', text="",
                        icon='RESTRICT_VIEW_OFF', emboss=False).image_name = item.name
        layout.operator('2dviews.delete_image', text="",
                        icon='X', emboss=False).image_name = item.name


class OPERATOR_move_image_list_item(bpy.types.Operator):
    bl_idname = "fd_2d_views.move_2d_image_item"
    bl_label = "Move an item in the 2D image list"

    direction = bpy.props.EnumProperty(items=(('UP', 'Up', "Move Item Up"),
                                              ('DOWN', 'Down', "Move Item Down")))

    @classmethod
    def poll(self, context):
        return len(bpy.context.window_manager.mv.image_views) > 0

    def execute(self, context):
        wm = context.window_manager.mv
        img_list = wm.image_views
        crt_index = wm.image_view_index
        list_length = len(wm.image_views) - 1
        move_to_index = crt_index - 1 if self.direction == 'UP' else crt_index + 1

        if self.direction == 'UP' and crt_index == 0 or self.direction == 'DOWN' and crt_index == list_length:
            return {'FINISHED'}
        else:
            img_list.move(crt_index, move_to_index)
            wm.image_view_index = move_to_index

        return{'FINISHED'}


class OPERATOR_create_new_view(bpy.types.Operator):
    bl_idname = "fd_2d_views.create_new_view"
    bl_label = "Create New 2d View"
    bl_description = "Create New 2d View"
    bl_options = {'UNDO'}

    view_name = bpy.props.StringProperty(name="View Name",
                                         description="Name for New View",
                                         default="")

    view_products = []

    def invoke(self, context, event):
        wm = context.window_manager
        self.view_products.clear()

        # For now only products are selected, could include walls or other objects
        for obj in context.selected_objects:
            product_bp = utils.get_bp(obj, 'PRODUCT')

            if product_bp and product_bp not in self.view_products:
                self.view_products.append(product_bp)

        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.prop(self, 'view_name', text="View Name")
        box.label("Selected Products:")
        prod_box = box.box()

        if len(self.view_products) > 0:
            for obj in self.view_products:
                row = prod_box.row()
                row.label(obj.mv.name_object, icon='OUTLINER_OB_LATTICE')

        else:
            row = prod_box.row()
            row.label("No Products Selected!", icon='ERROR')
            warn_box = box.box()
            row = warn_box.row()
            row.label("Create Empty View?", icon='QUESTION')

    def execute(self, context):
        packed_bps = [{"name": obj_bp.name, "obj_name": obj_bp.mv.name_object}
                      for obj_bp in self.view_products]
        bpy.ops.fd_2d_views.genereate_2d_views('INVOKE_DEFAULT',
                                               use_single_scene=True,
                                               single_scene_name=self.view_name,
                                               single_scene_objs=packed_bps)
        return {'FINISHED'}


class OPERATOR_append_to_view_OLD(bpy.types.Operator):
    bl_idname = "fd_2d_views.append_to_view"
    bl_label = "Append Product to 2d View"
    bl_description = "Append Product to 2d View"
    bl_options = {'UNDO'}

    products = []

    def invoke(self, context, event):
        wm = context.window_manager
        self.products.clear()

        # For now only products are selected, could include walls or other objects
        for obj in context.selected_objects:
            product_bp = utils.get_bp(obj, 'PRODUCT')

            if product_bp and product_bp not in self.products:
                self.products.append(product_bp)

        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label("Selected Products:")
        prod_box = box.box()

        if len(self.products) > 0:
            for obj in self.products:
                row = prod_box.row()
                row.label(obj.mv.name_object, icon='OUTLINER_OB_LATTICE')

        else:
            row = prod_box.row()
            row.label("No Products Selected!", icon='ERROR')
            warn_box = box.box()
            row = warn_box.row()
            row.label("Nothing to Append.", icon='ERROR')

    def link_dims_to_scene(self, scene, obj_bp):
        for child in obj_bp.children:
            if child not in self.ignore_obj_list:
                if child.mv.type in ('VISDIM_A', 'VISDIM_B'):
                    scene.objects.link(child)
                if len(child.children) > 0:
                    self.link_dims_to_scene(scene, child)

    def group_children(self, grp, obj):
        if obj.mv.type != 'CAGE':
            grp.objects.link(obj)
        for child in obj.children:
            if len(child.children) > 0:
                if child.mv.type == 'OBSTACLE':
                    for cc in child.children:
                        if cc.mv.type == 'CAGE':
                            cc.hide_render = False
                            grp.objects.link(cc)
                else:
                    self.group_children(grp, child)
            else:
                if not child.mv.is_wall_mesh:
                    if child.mv.type != 'CAGE':
                        grp.objects.link(child)
        return grp

    def execute(self, context):
        if len(self.products) < 1:
            return {'FINISHED'}

        for scene in bpy.data.scenes:
            if scene.mv.elevation_selected:
                grp = bpy.data.groups[scene.name]
                for prod in self.products:
                    self.group_children(grp, prod)

        return {'FINISHED'}


class single_scene_objs(bpy.types.PropertyGroup):
    obj_name = bpy.props.StringProperty(name="Object Name")


bpy.utils.register_class(single_scene_objs)


class OPERATOR_append_to_view(bpy.types.Operator):
    bl_idname = "fd_2d_views.append_to_view"
    bl_label = "Append Product to 2d View"
    bl_description = "Append Product to 2d View"
    bl_options = {'UNDO'}

    products = []

    objects = []

    scenes = bpy.props.CollectionProperty(type=single_scene_objs,
                                          name="Objects for Single Scene",
                                          description="Objects to Include When Creating a Single View")

    scene_index = bpy.props.IntProperty(name="Scene Index")

    def invoke(self, context, event):
        wm = context.window_manager
        self.products.clear()
        self.objects.clear()

        for i in self.scenes:
            self.scenes.remove(0)

        for scene in bpy.data.scenes:
            scene_col = self.scenes.add()
            scene_col.name = scene.name

        for obj in context.selected_objects:
            product_bp = utils.get_bp(obj, 'PRODUCT')

            if product_bp and product_bp not in self.products:
                self.products.append(product_bp)

        if len(self.products) == 0:
            for obj in context.selected_objects:
                self.objects.append(obj)

        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label("Selected View to Append To:")
        box.template_list("LIST_2d_images", " ", self,
                          "scenes", self, "scene_index")

        if len(self.products) > 0:
            box.label("Selected Products:")
            prod_box = box.box()
            for obj in self.products:
                row = prod_box.row()
                row.label(obj.mv.name_object, icon='OUTLINER_OB_LATTICE')
        else:
            if len(self.objects) > 0:
                box.label("Selected Objects:")
                prod_box = box.box()
                for obj in self.objects:
                    row = prod_box.row()
                    row.label(obj.name, icon='OBJECT_DATA')
            else:
                warn_box = box.box()
                row = warn_box.row()
                row.label("Nothing to Append.", icon='ERROR')

    def link_children_to_scene(self, scene, obj_bp):
        scene.objects.link(obj_bp)
        for child in obj_bp.children:
            self.link_children_to_scene(scene, child)

    def execute(self, context):
        scene = bpy.data.scenes[self.scene_index]

        for product in self.products:
            self.link_children_to_scene(scene, product)

        print("OBJS", self.objects)

        for obj in self.objects:
            print('LINK', obj, scene)
            self.link_children_to_scene(scene, obj)

        return {'FINISHED'}


class OPERATOR_genereate_2d_views(bpy.types.Operator):
    bl_idname = "fd_2d_views.genereate_2d_views"
    bl_label = "Generate 2d Views"
    bl_description = "Generates 2D Views"
    bl_options = {'UNDO'}

    VISIBLE_LINESET_NAME = "Visible Lines"
    HIDDEN_LINESET_NAME = "Hidden Lines"
    ENV_2D_NAME = "2D Environment"
    HIDDEN_LINE_DASH_PX = 5
    HIDDEN_LINE_GAP_PX = 5

    ev_pad = bpy.props.FloatProperty(name="Elevation View Padding",
                                     default=0.75)

    pv_pad = bpy.props.FloatProperty(name="Plan View Padding",
                                     default=1.5)

    main_scene = None

    ignore_obj_list = []

    hashmarks = []

    use_single_scene = bpy.props.BoolProperty(name="Use for Creating Single View",
                                              default=False)

    single_scene_name = bpy.props.StringProperty(name="Single Scene Name")

    single_scene_objs = bpy.props.CollectionProperty(type=single_scene_objs,
                                                     name="Objects for Single Scene",
                                                     description="Objects to Include When Creating a Single View")

#     orphan_products = []
    def get_object_global_location(self, obj):
        return obj.matrix_world * obj.data.vertices[0].co

    def to_inch(self, measure):
        return round(measure / unit.inch(1), 2)

    def to_inch_str(self, measure):
        return str(self.to_inch(measure))

    def to_inch_lbl(self, measure):
        return self.to_inch_str(measure) + "\""

    def list_mode(self, lst):
        return max(set(lst), key=lst.count)

    def get_world(self):
        if self.ENV_2D_NAME in bpy.data.worlds:
            return bpy.data.worlds[self.ENV_2D_NAME]
        else:
            world = bpy.data.worlds.new(self.ENV_2D_NAME)
            world.horizon_color = (1.0, 1.0, 1.0)
            return world

    def create_linestyles(self):
        linestyles = bpy.data.linestyles
        linestyles.new(self.VISIBLE_LINESET_NAME)
        linestyles[self.VISIBLE_LINESET_NAME].use_chaining = False

        hidden_linestyle = linestyles.new(self.HIDDEN_LINESET_NAME)
        hidden_linestyle.use_dashed_line = True
        hidden_linestyle.dash1 = self.HIDDEN_LINE_DASH_PX
        hidden_linestyle.dash2 = self.HIDDEN_LINE_DASH_PX
        hidden_linestyle.dash3 = self.HIDDEN_LINE_DASH_PX
        hidden_linestyle.gap1 = self.HIDDEN_LINE_GAP_PX
        hidden_linestyle.gap2 = self.HIDDEN_LINE_GAP_PX
        hidden_linestyle.gap3 = self.HIDDEN_LINE_GAP_PX

    def create_linesets(self, scene):
        f_settings = scene.render.layers[0].freestyle_settings
        linestyles = bpy.data.linestyles
        # groups = bpy.data.groups
        if 'FS Hidden Exclude' not in bpy.data.groups:
            fs_hidden_exclude_grp = bpy.data.groups.new('FS Hidden Exclude')
        else:
            fs_hidden_exclude_grp = bpy.data.groups['FS Hidden Exclude']

        f_settings.linesets.new(
            self.VISIBLE_LINESET_NAME).linestyle = linestyles[self.VISIBLE_LINESET_NAME]

        hidden_lineset = f_settings.linesets.new(self.HIDDEN_LINESET_NAME)
        hidden_lineset.linestyle = linestyles[self.HIDDEN_LINESET_NAME]

        hidden_lineset.select_by_visibility = True
        hidden_lineset.visibility = 'HIDDEN'
        hidden_lineset.select_by_edge_types = True
        hidden_lineset.select_by_face_marks = False
        hidden_lineset.select_by_group = True
        hidden_lineset.select_by_image_border = False

        hidden_lineset.select_silhouette = False
        hidden_lineset.select_border = False
        hidden_lineset.select_contour = True
        hidden_lineset.select_suggestive_contour = False
        hidden_lineset.select_ridge_valley = False
        hidden_lineset.select_crease = False
        hidden_lineset.select_edge_mark = True
        hidden_lineset.select_external_contour = False
        hidden_lineset.select_material_boundary = False

        # Group settings - used to exclude objects from hidden lines
        hidden_lineset.group = fs_hidden_exclude_grp
        hidden_lineset.group_negation = 'EXCLUSIVE'

    def clear_unused_linestyles(self):
        for linestyle in bpy.data.linestyles:
            if linestyle.users == 0:
                bpy.data.linestyles.remove(linestyle)

    def create_camera(self, scene):
        camera_data = bpy.data.cameras.new(scene.name)
        camera_obj = bpy.data.objects.new(
            name=scene.name, object_data=camera_data)
        scene.objects.link(camera_obj)
        scene.camera = camera_obj
        camera_obj.data.type = 'ORTHO'
        scene.render.resolution_y = 1280
        scene.mv.ui.render_type_tabs = 'NPR'
        scene.world = self.get_world()
        scene.render.display_mode = 'NONE'
        scene.render.use_lock_interface = True
        scene.render.image_settings.file_format = 'JPEG'

        return camera_obj

    def link_dims_to_scene(self, scene, obj_bp):
        for child in obj_bp.children:
            if child not in self.ignore_obj_list:
                if child.mv.type in ('VISDIM_A', 'VISDIM_B'):
                    scene.objects.link(child)
                if len(child.children) > 0:
                    self.link_dims_to_scene(scene, child)

    def link_desired_dims_to_scene(self, scene, obj_bp):
        for child in obj_bp.children:
            if child not in self.ignore_obj_list:
                if child.mv.type == 'VISDIM_A':
                    obj_parent = child.parent
                    if 'hanging' not in obj_parent.name.lower():
                        scene.objects.link(child)
                if child.mv.type == 'VISDIM_B':
                    obj_grandpa = child.parent.parent
                    if 'hanging' not in obj_grandpa.name.lower():
                        scene.objects.link(child)
                if len(child.children) > 0:
                    self.link_desired_dims_to_scene(scene, child)

    def group_children(self, grp, obj):
        if obj.mv.type != 'CAGE' and obj not in self.ignore_obj_list:
            grp.objects.link(obj)
        for child in obj.children:
            if len(child.children) > 0:
                if child.mv.type == 'OBSTACLE':
                    for cc in child.children:
                        if cc.mv.type == 'CAGE':
                            cc.hide_render = False
                            grp.objects.link(cc)
                else:
                    self.group_children(grp, child)
            else:
                #                 if not child.mv.is_wall_mesh:
                if child.mv.type != 'CAGE' and obj not in self.ignore_obj_list:
                    grp.objects.link(child)
        return grp

    def create_new_scene(self, context, grp, obj_bp):
        bpy.ops.scene.new('INVOKE_DEFAULT', type='EMPTY')
        new_scene = context.scene
        new_scene.name = grp.name
        new_scene.mv.name_scene = "Product - " + \
            obj_bp.mv.name_object if obj_bp.mv.type == 'BPASSEMBLY' else obj_bp.mv.name_object
        new_scene.mv.elevation_img_name = obj_bp.name
        new_scene.mv.plan_view_scene = False
        new_scene.mv.elevation_scene = True
        self.create_linesets(new_scene)

        return new_scene

    def add_text(self, context, assembly):
        bpy.ops.object.text_add()
        text = context.active_object
        text.parent = assembly.obj_bp
        text.location.x = unit.inch(-2)
        text.location.z = unit.inch(-10)
        text.rotation_euler.x = math.radians(90)
        text.data.size = .1
        text.data.body = assembly.obj_bp.mv.name_object
        text.data.align_x = 'RIGHT'
        text.data.font = self.font

    # Its to figure out if has variable children
    variable_sections_list = []

    def has_variable_descendants(self, item):
        if item.mv.opening_name:
            carcass_bp = utils.get_parent_assembly_bp(item)
            carcass_assembly = fd_types.Assembly(carcass_bp)
            variable_section = carcass_assembly.get_prompt(
                "CTF Opening {}".format(item.mv.opening_name)).value()
            if variable_section:
                self.variable_sections_list.append(item.mv.opening_name)
        if len(item.children) > 0:
            for i in item.children:
                self.has_variable_descendants(i)

    def wall_width_dimension(self, assembly):
        dim = fd_types.Dimension()
        dim.parent(assembly.obj_bp)
        dim.start_y(value=assembly.obj_y.location.y)
        dim.start_z(value=assembly.obj_z.location.z + unit.inch(4))
        dim.end_x(value=assembly.obj_x.location.x)
        dim.set_label(self.to_inch_str(assembly.obj_x.location.x) + "\"")

    def wall_height_dimension(self, context, item):
        dim = fd_types.Dimension()
        dim.parent(item.parent)
        dim.start_x(value=0 - unit.inch(9))
        dim.start_y(value=0 - unit.inch(9))
        dim.start_z(value=0)
        dim.end_z(value=item.dimensions[2])
        wall_height = self.to_inch_lbl(item.dimensions[2])
        dim.set_label(" ")
        bpy.ops.object.text_add()
        text = context.active_object
        text.parent = item
        text.rotation_euler.x = math.radians(0)
        text.rotation_euler.y = math.radians(-90)
        text.rotation_euler.z = math.radians(90)
        text.location.x = unit.inch(-10)
        text.location.y = 0
        text.location.z = (item.dimensions[2] / 2)
        text.data.align_x = 'CENTER'
        text.data.size = .1
        text.data.body = wall_height
        text.data.font = self.font

    def variable_opening_label(self, context, item):
        for n_item in item.children:
            if 'OPENING' in n_item.name:
                self.has_variable_descendants(n_item)
                variable_sections = set(self.variable_sections_list)
                self.variable_sections_list = []
                if len(variable_sections) > 0:
                    section_width = 0
                    for k_item in n_item.children:
                        if k_item.mv.type == 'VPDIMX':
                            section_width = k_item.location[0]
                    dim = fd_types.Dimension()
                    dim.parent(n_item)
                    dim.start_x(value=section_width / 2)
                    dim.start_y(value=section_width / 2)
                    dim.start_z(value=unit.inch(-7) +
                                (n_item.location[2] / -1))
                    dim.set_label("Var.")

    def parallel_partition_dimension(self, context, item):
        for n_item in item.children:
            if n_item.lm_closets.is_panel_bp:
                for k_item in n_item.children:
                    if "cutpart" in k_item.name.lower() and not k_item.hide:
                        line_offset = 1.5
                        label = self.to_inch_str(k_item.dimensions[0])
                        bpy.ops.object.text_add()
                        text = context.active_object
                        text.parent = k_item
                        text.rotation_euler.x = math.radians(90)
                        text.rotation_euler.y = math.radians(0)
                        text.rotation_euler.z = math.radians(0)
                        text.location.x = ((k_item.dimensions[0] / 2))
                        text.location.y = 0
                        text.location.z = unit.inch(line_offset)
                        text.data.align_x = 'CENTER'
                        text.data.size = .07
                        text.data.body = label
                        text.data.font = self.font_bold

    def toe_kick_dimension(self, context, item, assembly):
        for n_item in item.children:
            if 'toe' in n_item.name.lower():
                for k_item in n_item.children:
                    if k_item.mv.type == 'VPDIMZ':
                        label = str(
                            round(k_item.location[2] / unit.inch(1), 2)) + "\""
                        dim = fd_types.Dimension()
                        dim.parent(assembly.obj_bp)
                        dim.start_x(value=0 - unit.inch(2))
                        dim.start_y(value=0)
                        dim.start_z(value=0)
                        dim.end_z(value=k_item.location[2])
                        dim.set_label(" ")
                        bpy.ops.object.text_add()
                        text = context.active_object
                        text.parent = assembly.obj_bp
                        text.rotation_euler.x = math.radians(90)
                        text.rotation_euler.y = math.radians(0)
                        text.rotation_euler.z = math.radians(0)
                        text.location.x = 0 - unit.inch(5)
                        text.location.y = 0
                        text.location.z = k_item.location[2] / \
                            2 - unit.inch(0.5)
                        text.data.align_x = 'CENTER'
                        text.data.size = .07
                        text.data.body = label
                        text.data.font = self.font

    def fullback_labeling(self, context, item):
        for n_item in item.children:
            if 'backing' in n_item.name.lower():
                show_fullback = False
                label = ""
                fullback_dimensions = object
                offset = -2
                for k_item in n_item.children:
                    if 'cutpart' in k_item.name.lower() and not k_item.hide:
                        show_fullback = True
                        fullback_dimensions = k_item.dimensions
                if show_fullback:
                    full_back_size = abs(self.to_inch(fullback_dimensions[2]))
                    if full_back_size == 0.25:
                        label = ["F/B", "1/4"]
                    if full_back_size == 0.75:
                        label = ["F/B", "3/4"]
                    for lbl in label:
                        offset += 1
                        bpy.ops.object.text_add()
                        text = context.active_object
                        text.parent = n_item
                        text.rotation_euler.x = math.radians(180)
                        text.rotation_euler.y = math.radians(0)
                        text.rotation_euler.z = math.radians(90)
                        text.location.x = (
                            (fullback_dimensions[0] / 2) + (unit.inch(2) * offset))
                        text.location.y = ((fullback_dimensions[1] / 2))
                        text.location.z = 0
                        text.data.align_x = 'CENTER'
                        text.data.size = .07
                        text.data.body = lbl
                        text.data.font = self.font_bold

    def arrayed_shelf_dimension(self, context, cutpart, shelf_bp):
        setback = 0.25
        shelves_qtt = cutpart.modifiers["ZQuantity"].count
        shelves_offset = cutpart.modifiers[
            "ZQuantity"].constant_offset_displace[2]
        section_depth = self.to_inch(
            shelf_bp.location[1])
        shelf_depth = self.to_inch(
            cutpart.dimensions[1])
        depth_part_diff = abs(
            section_depth - shelf_depth)
        label = self.to_inch_lbl(
            cutpart.dimensions[1])
        rotation = (0, math.radians(45), 0)
        width = cutpart.dimensions[0]
        if depth_part_diff != setback and depth_part_diff != 0.0:
            for i in range(shelves_qtt):
                z_offset = shelves_offset + (shelves_offset *
                                             (i - 1))
                location = (width/2,
                            0,
                            unit.inch(2.12) + z_offset)
                hashmark = self.draw_hashmark(context,
                                              cutpart,
                                              location=location,
                                              rotation=rotation,
                                              length=unit.inch(6))
                dim = fd_types.Dimension()
                dim.parent(hashmark)
                dim.start_x(value=0)
                dim.start_y(value=0)
                dim.start_z(value=unit.inch(5))
                dim.set_label(label)

    def arrayed_shelves_door_inserts(self, context, item):
        if 'INSERT' in item.name and 'doors' in item.name.lower():
            for k_item in item.children:
                if k_item.lm_closets.is_shelf_bp:
                    for x_item in k_item.children:
                        part_name = x_item.name.lower()
                        if 'cutpart' in part_name and not x_item.hide:
                            self.arrayed_shelf_dimension(
                                context, x_item, k_item)

    def arrayed_hangs_inserts(self, context, item):
        if 'INSERT' in item.name and 'hang' in item.name.lower():
            for k_item in item.children:
                if k_item.lm_closets.is_shelf_bp:
                    for x_item in k_item.children:
                        part_name = x_item.name.lower()
                        if 'cutpart' in part_name and not x_item.hide:
                            self.arrayed_shelf_dimension(
                                context, x_item, k_item)

    def arrayed_hamper_doors_inserts(self, context, item):
        if 'INSERT' in item.name and 'hamper' in item.name.lower():
            for k_item in item.children:
                if 'INSERT' in k_item.name and 'doors' in k_item.name.lower():
                    for x_item in k_item.children:
                        if x_item.lm_closets.is_shelf_bp:
                            for y_item in x_item.children:
                                part_name = y_item.name.lower()
                                if 'cutpart' in part_name and not y_item.hide:
                                    self.arrayed_shelf_dimension(
                                        context, y_item, x_item)

    def arrayed_shelves_section_depth_dimension(self, context, item):
        if 'hanging' in item.name.lower():
            for n_item in item.children:
                self.arrayed_shelves_door_inserts(context, n_item)
                self.arrayed_hangs_inserts(context, n_item)
                self.arrayed_hamper_doors_inserts(context, n_item)

    def topshelf_exposed_dim(self, context, parent, location, rotation):
        mark = self.draw_hashmark(context, parent,
                                  location=location,
                                  rotation=rotation,
                                  length=unit.inch(3))
        dim = fd_types.Dimension()
        dim.parent(mark)
        dim.start_x(value=0)
        dim.start_y(value=0)
        dim.start_z(value=unit.inch(-4))
        dim.set_label("Exp.")

    def ctop_exposed_dim(self, context, parent, location, rotation):
        mark = self.draw_hashmark(context, parent,
                                  location=location,
                                  rotation=rotation,
                                  length=unit.inch(3))
        dim = fd_types.Dimension()
        dim.parent(mark)
        dim.start_x(value=0)
        dim.start_y(value=0)
        dim.start_z(value=unit.inch(4))
        dim.set_label("Exp.")

    def topshelf_exposed_label(self, context, item):
        for n_item in item.children:
            if n_item.lm_closets.is_closet_top_bp:
                for k_item in n_item.children:
                    for x_item in k_item.children:
                        if 'cutpart' in x_item.name.lower():
                            z_offset = (
                                x_item.dimensions[2] + unit.inch(1.06)) * -1
                            # Left Edgeband
                            if x_item.mv.edge_w1 != '':
                                location = (unit.inch(-1.06), 0, z_offset)
                                rotation = (0, math.radians(45), 0)
                                self.topshelf_exposed_dim(context,
                                                          x_item,
                                                          location,
                                                          rotation)
                            # Right Edgeband
                            if x_item.mv.edge_w2 != '':
                                offset = x_item.dimensions[0]
                                location = (unit.inch(1.06) + offset,
                                            0, z_offset)
                                rotation = (0, math.radians(-45), 0)
                                self.topshelf_exposed_dim(context,
                                                          x_item,
                                                          location,
                                                          rotation)
                            # Back Edgeband
                            if x_item.mv.edge_l2 != '':
                                offset = x_item.dimensions[0] / 2
                                location = (unit.inch(-1.06) + offset,
                                            0, z_offset)
                                rotation = (0, math.radians(45), 0)
                                self.topshelf_exposed_dim(context,
                                                          x_item,
                                                          location,
                                                          rotation)

    def topshelf_hashmark(self, context, item):
        for n_item in item.children:
            if n_item.lm_closets.is_closet_top_bp:
                for k_item in n_item.children:
                    if k_item.mv.type == 'BPASSEMBLY':
                        ts_assembly = fd_types.Assembly(k_item)
                        ts_width = ts_assembly.obj_x.location.x
                        ts_depth = ts_assembly.obj_y.location.y
                        ts_height = ts_assembly.obj_z.location.z
                        offset = ts_width / 2
                        location = (unit.inch(
                            1.06) + offset, 0, unit.inch(-1.06) + ts_height)
                        rotation = (0, math.radians(-45), 0)
                        hashmark = self.draw_hashmark(context, k_item,
                                                      location=location,
                                                      rotation=rotation,
                                                      length=unit.inch(3))
                        dim = fd_types.Dimension()
                        dim.parent(hashmark)
                        dim.start_x(value=0)
                        dim.start_y(value=0)
                        dim.start_z(value=unit.inch(-4))
                        dim.set_label(self.to_inch_lbl(ts_depth))

    def chk_shelf_cutpart(self, context, cutpart, shelf_bp):
        setback = 0.25
        shelf_depth = self.to_inch(
            shelf_bp.location[1])
        shelf_cutpart = self.to_inch(
            cutpart.dimensions[1])
        depth_part_diff = abs(
            shelf_depth - shelf_cutpart)
        if depth_part_diff != setback and depth_part_diff != 0.0:
            return True
        else:
            return False

    def shelf_non_std_dimension(self, context, cutpart, shelf_bp):
        setback = 0.25
        shelf_depth = self.to_inch(shelf_bp.location[1])
        shelf_cutpart = self.to_inch(cutpart.dimensions[1])
        width = cutpart.dimensions[0]
        depth_part_diff = abs(shelf_depth - shelf_cutpart)
        location = ((width / 2),
                    0,
                    unit.inch(2.12))
        rotation = (0, math.radians(45), 0)
        label = ""
        if depth_part_diff != setback and depth_part_diff != 0.0:
            label = self.to_inch_lbl(cutpart.dimensions[1])
        else:
            label = self.to_inch_lbl(shelf_bp.location[1])
        hashmark = self.draw_hashmark(context,
                                      cutpart,
                                      location=location,
                                      rotation=rotation,
                                      length=unit.inch(6))
        dim = fd_types.Dimension()
        dim.parent(hashmark)
        dim.start_x(value=0)
        dim.start_y(value=0)
        dim.start_z(value=unit.inch(5))
        dim.set_label(label)

    def valances(self, context, item):
        for candidate in item.children:
            product = 'product' in candidate.name.lower()
            valance = 'valance' in candidate.name.lower()
            if product and valance:
                valance_assembly = fd_types.Assembly(candidate)
                width = valance_assembly.obj_x.location.x
                height = valance_assembly.get_prompt(
                    "Molding Height").value()
                location = valance_assembly.get_prompt(
                    "Molding Location").value()
                x_offset = width / 2 + unit.inch(0.68)
                z_offset = (abs(height) + abs(location) + unit.inch(0.68)) * -1
                hashmark_location = (x_offset,
                                     0,
                                     z_offset)
                rotation = (math.radians(135), 0, math.radians(90))
                label = "Valance " + self.to_inch_lbl(abs(height))
                hashmark = self.draw_hashmark(context,
                                              candidate,
                                              location=hashmark_location,
                                              rotation=rotation,
                                              length=unit.inch(2))
                dim = fd_types.Dimension()
                dim.parent(hashmark)
                dim.start_x(value=0)
                dim.start_y(value=0)
                dim.start_z(value=unit.inch(4))
                dim.set_label(label)

    def light_rails(self, context, item):
        for candidate in item.children:
            product = 'product' in candidate.name.lower()
            light = 'light' in candidate.name.lower()
            rail = 'rail' in candidate.name.lower()
            if product and light and rail:
                light_rail_assembly = fd_types.Assembly(candidate)
                width = light_rail_assembly.obj_x.location.x
                height = light_rail_assembly.get_prompt(
                    "Molding Height").value()
                location = light_rail_assembly.get_prompt(
                    "Molding Location").value()
                x_offset = width / 2 + unit.inch(0.68)
                z_offset = (abs(height) + abs(location) + unit.inch(0.68)) * -1
                hashmark_location = (x_offset,
                                     0,
                                     z_offset)
                rotation = (math.radians(135), 0, math.radians(90))
                label = "Light Rails " + self.to_inch_lbl(abs(height))
                hashmark = self.draw_hashmark(context,
                                              candidate,
                                              location=hashmark_location,
                                              rotation=rotation,
                                              length=unit.inch(2))
                dim = fd_types.Dimension()
                dim.parent(hashmark)
                dim.start_x(value=0)
                dim.start_y(value=0)
                dim.start_z(value=unit.inch(4))
                dim.set_label(label)

    def flat_crown(self, context, item):
        for candidate in item.children:
            candidate_name = candidate.name.lower()
            product = 'product' in candidate_name
            flat = 'flat' in candidate_name
            crown = 'crown' in candidate_name
            if product and flat and crown:
                crown_assembly = fd_types.Assembly(candidate)
                width = crown_assembly.obj_x.location.x
                crown_m_height = crown_assembly.get_prompt("Molding Height")
                crown_height = crown_m_height.value()
                y_offset = crown_height
                x_offset = width / 2
                location = (unit.inch(2.12) + x_offset,
                            0,
                            unit.inch(2.12) + y_offset)
                rotation = (0, math.radians(45), 0)
                label = "Flat Crown " + self.to_inch_lbl(crown_height)
                hashmark = self.draw_hashmark(context,
                                              candidate,
                                              location=location,
                                              rotation=rotation,
                                              length=unit.inch(6))
                dim = fd_types.Dimension()
                dim.parent(hashmark)
                dim.start_x(value=0)
                dim.start_y(value=0)
                dim.start_z(value=unit.inch(5))
                dim.set_label(label)

    def slanted_shoes_shelf(self, context, item):
        for candidate in item.children:
            candidate_name = candidate.name.lower()
            insert = 'insert' in candidate_name
            slanted = 'slanted' in candidate_name
            shoe = 'shoe' in candidate_name
            shelf = 'shelf' in candidate_name
            if insert and slanted and shoe and shelf:
                sss_assembly = fd_types.Assembly(candidate)
                #
                shelf_lip_prompt = sss_assembly.get_prompt("Shelf Lip Type")
                shelf_qty_prompt = sss_assembly.get_prompt("Adj Shelf Qty")
                shelf_offset_prompt = sss_assembly.get_prompt(
                    "Distance Between Shelves")
                shelf_lip = shelf_lip_prompt.value()
                shelf_offset = float(shelf_offset_prompt.value())
                shelf_qty = int(shelf_qty_prompt.value())
                #
                z_offset = (shelf_qty - 1) * shelf_offset
                width = sss_assembly.obj_x.location.x
                x_offset = width / 2
                label = "SSS " + shelf_lip + " Lip"
                location = (unit.inch(2.12) + x_offset,
                            0,
                            unit.inch(2.12) + z_offset)
                rotation = (0, math.radians(45), 0)
                hashmark = self.draw_hashmark(context,
                                              candidate,
                                              location=location,
                                              rotation=rotation,
                                              length=unit.inch(6))
                dim = fd_types.Dimension()
                dim.parent(hashmark)
                dim.start_x(value=0)
                dim.start_y(value=0)
                dim.start_z(value=unit.inch(5))
                dim.set_label(label)

    def add_glass_cutpart_dim(self, context, assembly, cutpart, thickness):
        setback = 0.25
        section_depth = self.to_inch(
            assembly.location[1])
        shelf_depth = self.to_inch(
            cutpart.dimensions[1])
        depth_part_diff = abs(
            section_depth - shelf_depth)
        shelves_qtt = cutpart.modifiers["ZQuantity"].count
        shelves_offset = cutpart.modifiers[
            "ZQuantity"].constant_offset_displace[2]
        width = cutpart.dimensions[0]
        # For cutparts that differs from the section depth minus setback (0.25)
        if depth_part_diff != setback and depth_part_diff != 0.0:
            label = self.to_inch_lbl(
                cutpart.dimensions[1])
        else:
            label = self.to_inch_lbl(
                assembly.location[1])
        label += " Glass "
        label += thickness
        for i in range(shelves_qtt):
            z_offset = shelves_offset + (shelves_offset *
                                         (i - 1))
            location = (width/2,
                        0,
                        unit.inch(2.12) + z_offset)
            rotation = (0, math.radians(45), 0)
            hashmark = self.draw_hashmark(context,
                                          cutpart,
                                          location=location,
                                          rotation=rotation,
                                          length=unit.inch(6))
            dim = fd_types.Dimension()
            dim.parent(hashmark)
            dim.start_x(value=0)
            dim.start_y(value=0)
            dim.start_z(value=unit.inch(5))
            dim.set_label(label)

    def glass_shelves(self, context, item):
        for candidate in item.children:
            candidate_lowername = candidate.name.lower()
            insert = 'insert' in candidate_lowername
            shelves = 'shelves' in candidate_lowername
            glass = 'glass' in candidate_lowername
            if insert and shelves and glass:
                insert_assembly = fd_types.Assembly(candidate)
                glass_prompt = insert_assembly.get_prompt(
                    "Glass Shelf Thickness")
                glass_thickness = glass_prompt.value()
                for assem_candidate in candidate.children:
                    if assem_candidate.lm_closets.is_glass_shelf_bp:
                        for cutpart_candidate in assem_candidate.children:
                            if 'cutpart' in cutpart_candidate.name.lower():
                                self.add_glass_cutpart_dim(context,
                                                           assem_candidate,
                                                           cutpart_candidate,
                                                           glass_thickness)

    def non_standard_shelves_dimensions(self, context, item):
        # We add dimensions for shelves that differs
        # from the section depth + default cutpart (1/4")
        for n_item in item.children:
            item_is_top_bp = n_item.lm_closets.is_closet_top_bp
            item_is_shelf = 'shelf' in n_item.name.lower()
            item_is_insert = 'INSERT' in n_item.name

            if item_is_insert and item_is_shelf and not item_is_top_bp:
                shelves = []
                for k_item in n_item.children:
                    if k_item.lm_closets.is_shelf_bp:
                        for x_item in k_item.children:
                            if 'cutpart' in x_item.name.lower():
                                shelves.append(self.chk_shelf_cutpart(context,
                                                                      x_item,
                                                                      k_item))
                if any(shelves):
                    for k_item in n_item.children:
                        if k_item.lm_closets.is_shelf_bp:
                            for x_item in k_item.children:
                                if 'cutpart' in x_item.name.lower():
                                    self.shelf_non_std_dimension(context,
                                                                 x_item,
                                                                 k_item)

    def section_depths(self, context, assembly):
        wall = assembly.obj_bp.children
        candidates = [item for item in wall if item.mv.type == 'BPASSEMBLY']
        n_openings = [[item for item in obj.children if 'OPENING' in item.name]
                      for obj in candidates]
        for openings in n_openings:
            for opening in openings:
                opening_assembly = fd_types.Assembly(opening)
                depth = opening_assembly.obj_y.location.y
                hashmark = self.draw_hashmark(context, opening,
                                              location=(
                                                  unit.inch(2.12),
                                                  0,
                                                  unit.inch(2.12)),
                                              rotation=(
                                                  0, math.radians(45), 0),
                                              length=unit.inch(6))
                dim = fd_types.Dimension()
                dim.parent(hashmark)
                dim.start_x(value=0)
                dim.start_y(value=0)
                dim.start_z(value=unit.inch(5))
                dim.set_label(self.to_inch_str(depth) + "\"")

    def widths_uppers_and_lowers(self, context, assembly):
        lower_offset = unit.inch(-3)
        upper_offset = unit.inch(15)
        #
        wall = assembly.obj_bp.children
        hanging_openings_lengths = []
        restricted_openings = []
        offset_openings = []
        # Selecting the openings at the wall, using a nested list - n_openings
        candidates = [item for item in wall if item.mv.type == 'BPASSEMBLY']
        n_openings = [[item for item in obj.children if 'OPENING' in item.name]
                      for obj in candidates]
        hanging_openings_lengths.append(len(n_openings))
        if len(n_openings) > 1 and len(set(hanging_openings_lengths)) == 1:
            column_openings = zip(*n_openings)
            for column in column_openings:
                opening_widths = []
                opening_heights = []
                global_heights = []
                if len(column) == 2:
                    for item in column:
                        item_assembly = fd_types.Assembly(item)
                        opening_widths.append(self.to_inch(
                            item_assembly.obj_x.location.x))
                        opening_heights.append(self.to_inch(
                            item_assembly.obj_z.location.z))
                        gl_height = self.get_object_global_location(item)[2]
                        global_heights.append(self.to_inch(gl_height))
                        offset_openings.append(item)
                width_query = len(set(opening_widths)) == 1
                global_heights_query = len(set(global_heights)) != 1
                if width_query and global_heights_query:
                    restricted_openings.append(column[1])

        for openings in n_openings:
            for opening in openings:
                depth = 0
                opening_assembly = fd_types.Assembly(opening)
                # skip unwanted dimensions
                if opening in restricted_openings:
                    continue
                if opening not in offset_openings:
                    depth += opening_assembly.obj_y.location.y
                width = opening_assembly.obj_x.location.x
                width_str = str(round(width / unit.inch(1), 2)) + "\""
                global_opening_height = self.get_object_global_location(
                    opening)[2]
                parent_assembly = fd_types.Assembly(opening.parent)
                parent_height = parent_assembly.obj_z.location.z
                vertical_placement = (opening.location[2] / -1) + lower_offset
                if global_opening_height >= parent_height / 2:
                    vertical_placement += (parent_height + upper_offset)
                dim = fd_types.Dimension()
                dim.parent(opening)
                dim.start_x(value=width/2)
                dim.start_y(value=depth)
                dim.start_z(value=vertical_placement)
                dim.set_label(width_str)
                self.ignore_obj_list.append(dim.anchor)
                self.ignore_obj_list.append(dim.end_point)

    def apply_planview_opening_tag(self, wall_assembly,
                                   context, opening, tags, parent):
        text_height = .1
        tags.sort(key=lambda x: x[1])
        text_rotation = math.radians(0)
        wall_assembly_bp = fd_types.Assembly(wall_assembly.obj_bp)
        wall_angle = round(math.degrees(
            wall_assembly_bp.obj_bp.rotation_euler[2]))
        if wall_angle == 180:
            text_rotation = math.radians(180)
            tags.reverse()
        opng_assembly = fd_types.Assembly(opening)
        pos_x = opng_assembly.obj_x.location.x
        pos_y = opng_assembly.obj_y.location.y
        parent_height = parent.location[2]
        for index, tag in enumerate(tags):
            loc_y = ((index + 1) * (pos_y / (len(tags) + 1)))
            bpy.ops.object.text_add()
            text = context.active_object
            text.parent = parent
            text.rotation_euler.x = math.radians(0)
            text.rotation_euler.y = math.radians(0)
            text.rotation_euler.z = text_rotation
            text.location.x = pos_x / 2
            text.location.y = loc_y - unit.inch(1)
            text.location.z = 0 - parent_height
            text.data.align_x = 'CENTER'
            text.data.size = text_height
            text.data.body = tag[0]
            text.data.font = self.font

    def get_hang_shelves_count(self, assembly):
        shelves_dict = {}
        shelves_dict["dust"] = 0
        hang_assembly = fd_types.Assembly(assembly)
        top_dust_shelf = hang_assembly.get_prompt("Add Top Shelf").value()
        bottom_dust_shelf = hang_assembly.get_prompt(
            "Add Bottom Shelf").value()
        top_shelves = hang_assembly.get_prompt(
            "Add Shelves In Top Section").value()
        middle_shelves = hang_assembly.get_prompt(
            'Add Shelves In Middle Section').value()
        bottom_shelves = hang_assembly.get_prompt(
            'Add Shelves In Bottom Section').value()
        if top_shelves:
            shelves_dict["top"] = hang_assembly.get_prompt(
                "Top Shelf Quantity").value()
        else:
            shelves_dict["top"] = 0
        if middle_shelves:
            shelves_dict["middle"] = hang_assembly.get_prompt(
                "Middle Shelf Quantity").value()
        else:
            shelves_dict["middle"] = 0
        if bottom_shelves:
            shelves_dict["bottom"] = hang_assembly.get_prompt(
                "Bottom Shelf Quantity").value()
        else:
            shelves_dict["bottom"] = 0
        if top_dust_shelf:
            shelves_dict["dust"] += 1
        if bottom_dust_shelf:
            shelves_dict["dust"] += 1
        return shelves_dict

    def get_glass_shelves_count(self, assembly):
        glass_sh_assembly = fd_types.Assembly(assembly)
        sh_qty = glass_sh_assembly.get_prompt("Shelf Qty").value()
        return str(sh_qty)

    def get_sss_count(self, assembly):
        sss_assembly = fd_types.Assembly(assembly)
        sh_qty = sss_assembly.get_prompt("Adj Shelf Qty").value()
        return str(sh_qty)

    def get_shelf_stack_count(self, assembly):
        assemblies = [
            item for item in assembly.children if item.lm_closets.is_shelf_bp]
        return (len(assemblies))

    def get_door_count(self, assembly):
        door_count = 0
        for obj in assembly.children:
            if 'left' in obj.name.lower():
                for d_obj in obj.children:
                    if 'cutpart' in d_obj.name.lower() and not d_obj.hide:
                        door_count += 1
            if 'right' in obj.name.lower():
                for d_obj in obj.children:
                    if 'cutpart' in d_obj.name.lower() and not d_obj.hide:
                        door_count += 1
        return door_count

    def get_drawer_count(self, assembly):
        drawers_assembly = fd_types.Assembly(assembly)
        drawers_qty = drawers_assembly.get_prompt("Drawer Quantity").value()
        # It's needed to count minus one drawer to get the correct
        # drawers count over it's prompt.
        drawers_qty -= 1
        return str(drawers_qty)

    def get_assembly_tag(self, assemblies, opening):
        opening_assembly = fd_types.Assembly(opening)
        opening_assembly_height = opening_assembly.obj_z.location.z
        has_any_hang = False
        tags = []
        shelf_count = 0
        for assembly in assemblies:
            shelves_dict = {}
            name = assembly.name.lower()
            gloc_height = self.get_object_global_location(assembly)[2]
            gloc_inches = self.to_inch(abs(gloc_height))
            # Hangs
            if 'hang' in name:
                shelves_dict = self.get_hang_shelves_count(assembly)
                has_any_hang = True
            if 'hang' and 'double' in name:
                tags.append(('DH', gloc_inches))
                shelf_count += shelves_dict["dust"]
            elif 'hang' and 'long' in name:
                tags.append(('LH', gloc_inches))
                shelf_count += shelves_dict["dust"]
            elif 'hang' and 'medium' in name:
                tags.append(('MH', gloc_inches))
                shelf_count += shelves_dict["dust"]
                shelf_count += shelves_dict["top"]
            elif 'hang' and 'short' in name:
                tags.append(('SH', gloc_inches))
                shelf_count += shelves_dict["dust"]
                shelf_count += shelves_dict["middle"]
            # Hampers
            elif 'hamper' in name:
                tags.append(('Hamp.', gloc_inches))
            # Shelves
            elif 'glass' in name:
                qty = self.get_glass_shelves_count(assembly)
                tag = qty + ' Glass Shlvs'
                tags.append((tag, gloc_inches))
            elif 'shelf' in name and 'slanted' not in name:
                qty = self.get_shelf_stack_count(assembly)
                shelf_count += qty
            elif 'slanted' and 'shoe' and 'shelf' in name:
                qty = self.get_sss_count(assembly)
                tag = qty + ' SSS'
                tags.append((tag, gloc_inches))
            # Doors
            elif 'doors' in name:
                tag = ()
                door_assy = fd_types.Assembly(assembly)
                door_height = door_assy.obj_z.location.z
                qty = self.get_door_count(assembly)
                shf_pmt = fd_types.Assembly(assembly).get_prompt('Add Shelves')
                shf_qty = fd_types.Assembly(
                    assembly).get_prompt('Shelf Quantity')
                bot_kd = fd_types.Assembly(assembly).get_prompt('Bottom KD')
                door_type = fd_types.Assembly(
                    assembly).get_prompt('Door Type').value()
                hang_presumption = door_height > (opening_assembly_height / 2)
                # HACK we are presuming once there is a tall door and it is
                #      higher than the middle of respective opening, the hang
                #      is behind the door
                if hang_presumption and door_type == "Tall":
                    shelf_count -= 1
                if bot_kd:
                    if bot_kd.value():
                        shelf_count += 1
                if shf_pmt:
                    if shf_pmt.value():
                        shelf_count += shf_qty.value()
                if qty == 1:
                    tag = ('1 Door', gloc_inches)
                else:
                    tag = ('2 Doors', gloc_inches)
                tags.append(tag)
            # Drawers
            elif 'drawer' in name:
                qty = self.get_drawer_count(assembly)
                tag = qty + ' Drws.'
                tags.append((tag, gloc_inches))
        if shelf_count > 1:
            shelf_tag = str(shelf_count) + " Shlvs."
            tags.append((shelf_tag, 0.0))
        elif shelf_count > 0:
            shelf_tag = str(shelf_count) + " Shelf"
            tags.append((shelf_tag, 0.0))
        return tags

    def find_matching_inserts(self, context, hanging_opening, location):
        matches = []
        for child in hanging_opening.children:
            if 'insert' in child.name.lower():
                measure = self.to_inch(child.location[0])
                if measure == location:
                    matches.append(child)
                    for nested in child.children:
                        if 'insert' in nested.name.lower():
                            matches.append(nested)
        return matches

    def group_openings_by_euclidean_distance(self, tags_dict, wall_angle):
        positions_dict = {}
        groups = []
        group_max_distance = unit.inch(5)
        skip_on_merge = []
        # Fetch the global position of each opening, it will be compared in
        # X-axis later
        for opening, value in tags_dict.items():
            # Depending on wall angle, our "X-axis" is diferent.
            if wall_angle == 0:
                opng_x_pos = self.get_object_global_location(opening)[0]
                continue
            if wall_angle > 0:
                opng_x_pos = self.get_object_global_location(
                    opening)[0] * math.sin(wall_angle)
                continue
            if wall_angle < 0:
                opng_x_pos = self.get_object_global_location(
                    opening)[1] * math.cos(wall_angle)
                continue
            positions_dict[opening] = opng_x_pos
        # Now compare each opening with all others to find matching groups
        for opening, x_pos in positions_dict.items():
            for key, position in positions_dict.items():
                # get euclidean distance
                distance = abs(x_pos - position)
                # compare to get the ones that matters
                if opening != key and distance < group_max_distance:
                    local_group = []
                    local_group.append(opening.name)
                    local_group.append(key.name)
                    local_group.sort()
                    groups.append(local_group)
        results = list(set(tuple(sorted(group)) for group in groups))
        if len(groups) > 0:
            grouped_dict = {}
            for result in results:
                group_body = []
                heights = []
                openings = list(result)
                for opening in openings:
                    blender_obj = bpy.data.objects[opening]
                    global_height = self.get_object_global_location(
                        blender_obj)[2]
                    global_height_val = self.to_inch(global_height)
                    for tag in tags_dict[blender_obj][0]:
                        group_body.append(tag)
                    heights.append((blender_obj, global_height_val))
                    skip_on_merge.append(blender_obj.name)
                heights.sort(key=lambda x: x[1])
                desired_blender_obj = heights[0][0]
                associated_obj = tags_dict[desired_blender_obj][1]
                grouped_dict[desired_blender_obj] = (
                    group_body, associated_obj)
            skip_on_merge = list(set(skip_on_merge))
            for key, value in tags_dict.items():
                if key.name not in skip_on_merge:
                    grouped_dict[key] = value
            return grouped_dict
        return tags_dict

    def plan_view_products_labels(self, context, wall_assembly):
        tags_dict = {}
        wall = wall_assembly.obj_bp.children
        wall_angle = round(math.degrees(
            wall_assembly.obj_bp.rotation_euler[2]))
        for item in wall:
            if item.mv.type == 'BPASSEMBLY':
                for opening in item.children:
                    if 'OPENING' in opening.name:
                        opng_position = self.to_inch(opening.location[0])
                        matches = self.find_matching_inserts(context,
                                                             item,
                                                             opng_position)
                        if (len(matches) > 0):
                            tags = self.get_assembly_tag(matches, opening)
                            tags_dict[opening] = (tags, matches)
        grouped = self.group_openings_by_euclidean_distance(
            tags_dict, wall_angle)
        for opening, value in grouped.items():
            tags = value[0]
            parent = value[1][0]
            self.apply_planview_opening_tag(wall_assembly, context, opening,
                                            tags,
                                            parent)

    def countertop_hashmark(self, context, item):
        material_name = ""
        for n_item in item.children:
            if n_item.lm_closets.is_counter_top_insert_bp:
                ctop_assembly = fd_types.Assembly(n_item)
                width = abs(ctop_assembly.obj_x.location.x)
                counter_top_width = 0
                counter_top_depth = 0
                counter_top_height = 0
                # n_item is at CTOP INSERT level
                for k_item in n_item.children:
                    for x_item in k_item.children:
                        if not x_item.hide and 'hashmark' not in x_item.name.lower():
                            # HACK to display the material correctly
                            # Until the context materials get fixed
                            if 'hpl' in x_item.name.lower():
                                material_name = "HPL"
                            elif 'melamine' in x_item.name.lower():
                                material_name = "Mel."
                            elif 'granite' in x_item.name.lower():
                                material_name = "Gran."
                            for sibling in x_item.parent.children:
                                if sibling.mv.type == 'VPDIMX':
                                    counter_top_width = abs(
                                        sibling.location[0])
                                if sibling.mv.type == 'VPDIMY':
                                    counter_top_depth = abs(
                                        sibling.location[1])
                                if sibling.mv.type == 'VPDIMZ':
                                    counter_top_height = abs(
                                        sibling.location[2])
                context_material = material_name
                material = ""
                if not None:
                    material += context_material
                material += " "
                for spec_group in context.scene.mv.spec_groups:
                    material += spec_group.materials["Countertop_Surface"].item_name
                x_offset = width / 2
                z_offset = counter_top_height + unit.inch(1.06)
                location = (unit.inch(1.06) + x_offset, 0, z_offset)
                rotation = (0, math.radians(45), 0)
                hashmark = self.draw_hashmark(context, n_item, location,
                                              rotation,
                                              length=unit.inch(3))
                counter_top_width_str = self.to_inch_lbl(counter_top_width)
                counter_top_depth_str = self.to_inch_lbl(counter_top_depth)
                counter_top_height_str = self.to_inch_lbl(
                    counter_top_height)
                # Countertop Dimensions
                label = (material + " C.T. " + counter_top_width_str +
                         " x " + counter_top_depth_str)
                ctop_dim = fd_types.Dimension()
                ctop_dim.parent(hashmark)
                ctop_dim.start_x(value=unit.inch(-2.12))
                ctop_dim.start_y(value=0)
                ctop_dim.start_z(value=unit.inch(3))
                ctop_dim.set_label(label)

    def countertop_exposed_label(self, context, item):
        for n_item in item.children:
            if n_item.lm_closets.is_counter_top_insert_bp:
                ctop_assembly = fd_types.Assembly(n_item)
                ctop_exposed_left = ctop_assembly.get_prompt("Exposed Left")
                ctop_exposed_right = ctop_assembly.get_prompt("Exposed Right")
                ctop_exposed_back = ctop_assembly.get_prompt("Exposed Back")
                extended_left = ctop_assembly.get_prompt("Extend Left Amount")
                extended_right = ctop_assembly.get_prompt(
                    "Extend Right Amount")
                width = abs(ctop_assembly.obj_x.location.x)
                counter_top_height = 0
                # n_item is at CTOP INSERT level
                for k_item in n_item.children:
                    for x_item in k_item.children:
                        if not x_item.hide and 'hashmark' not in x_item.name.lower():
                            for sibling in x_item.parent.children:
                                if sibling.mv.type == 'VPDIMZ':
                                    counter_top_height = abs(
                                        sibling.location[2])
                z_offset = counter_top_height + unit.inch(1.06)
                if ctop_exposed_left.value() is True:
                    extension = 0
                    if extended_left is not None:
                        extension = extended_left.value()
                    offset = 0 - extension
                    location = (unit.inch(-1.06) + offset, 0, z_offset)
                    rotation = (0, math.radians(-45), 0)
                    self.ctop_exposed_dim(context, n_item, location, rotation)
                if ctop_exposed_right.value() is True:
                    extension = 0
                    if extended_right is not None:
                        extension = extended_right.value()
                    offset = width + extension
                    location = (unit.inch(1.06) + offset, 0, z_offset)
                    rotation = (0, math.radians(45), 0)
                    self.ctop_exposed_dim(context, n_item, location, rotation)
                if ctop_exposed_back.value() is True:
                    offset = width / 4
                    location = (unit.inch(-1.06) + offset, 0, z_offset)
                    rotation = (0, math.radians(-45), 0)
                    self.ctop_exposed_dim(context, n_item, location, rotation)

    def file_drawer_labeling(self, context, item):
        for n_item in item.children:
            if n_item.lm_closets.is_drawer_stack_bp:
                for k_item in n_item.children:
                    if k_item.lm_closets.is_drawer_box_bp:
                        rails = {}
                        drawer_width = 0
                        for f_item in k_item.children:
                            if f_item.mv.type == 'VPDIMX':
                                drawer_width = f_item.location[0]
                            if 'rail' in f_item.name.lower():
                                for v_item in f_item.children:
                                    if 'cutpart' in v_item.name.lower() and not v_item.hide:
                                        if 'left' in v_item.name.lower():
                                            rails["left"] = self.to_inch(
                                                f_item.location[0])
                                            rails["type"] = "front_back"
                                            rails["dim_parent"] = f_item
                                        if 'right' in v_item.name.lower():
                                            rails["right"] = self.to_inch(
                                                f_item.location[0])
                                            rails["type"] = "front_back"
                                        if 'front' in v_item.name.lower():
                                            rails["front"] = self.to_inch(
                                                f_item.location[1])
                                            rails["type"] = "lateral"
                                            rails["dim_parent"] = f_item
                                        if 'back' in v_item.name.lower():
                                            rails["back"] = self.to_inch(
                                                f_item.location[1])
                                            rails["type"] = "lateral"
                        if len(rails) > 0:
                            file_rail_thickness = 0.5
                            letter_size = 12
                            legal_size = 15
                            label = []
                            if (rails["type"] == "lateral"):
                                label.append("FILE")
                                bottom_line = "LAT "
                                if rails["back"] - rails["front"] - file_rail_thickness == letter_size:
                                    bottom_line += "Letter"
                                elif rails["back"] - rails["front"] - file_rail_thickness == legal_size:
                                    bottom_line += "Legal"
                                label.append(bottom_line)
                            if (rails["type"] == "front_back"):
                                label.append("FILE")
                                bottom_line = "F2B "
                                if rails["right"] - rails["left"] - file_rail_thickness == letter_size:
                                    bottom_line += "Letter"
                                elif rails["right"] - rails["left"] - file_rail_thickness == legal_size:
                                    bottom_line += "Legal"
                                label.append(bottom_line)
                            count = len(label)
                            for l in label:
                                dim = fd_types.Dimension()
                                dim.parent(rails["dim_parent"])
                                dim.start_x(value=(drawer_width / 2) -
                                            unit.inch(file_rail_thickness * 2))
                                dim.start_y(value=(drawer_width / 2) -
                                            unit.inch(file_rail_thickness * 2))
                                dim.start_z(
                                    value=(unit.inch(3) * count) - unit.inch(2))
                                dim.set_label(l)
                                count -= 1

    def add_filler_labeling(self, context, item):
        for child in item.children:
            if 'filler' in child.name.lower():
                for cc in child.children:
                    if 'cutpart' in cc.name.lower() and not cc.hide:
                        filler_assy = fd_types.Assembly(child)
                        filler_measure = filler_assy.obj_y.location.y
                        filler_amount = self.to_inch_lbl(abs(filler_measure))
                        z_offset = child.location[2] + unit.inch(3)
                        # Filler Measure
                        # NOTE to change Z-position change X values
                        #      to change X-position change Y values
                        filler_dim = fd_types.Dimension()
                        filler_dim.parent(child)
                        filler_dim.start_x(value=0 - z_offset)
                        filler_dim.start_y(value=filler_measure / 2)
                        filler_dim.start_z(value=0)
                        filler_dim.set_label(filler_amount)
                        # Filler Label
                        filler_lbl = fd_types.Dimension()
                        filler_lbl.parent(child)
                        filler_lbl.start_x(value=0 - z_offset - unit.inch(3))
                        filler_lbl.start_y(value=filler_measure / 2)
                        filler_lbl.start_z(value=0)
                        filler_lbl.set_label("Filler")

    def build_height_dimension(self, context, assembly):
        for item in assembly.obj_bp.children:
            if 'hanging' in item.name.lower():
                offset = unit.inch(-5)
                countertop_height = 0
                ctop_thickness = 0
                topshelf_thickness = 0
                hanging_height = 0
                for n_item in item.children:
                    if n_item.mv.type == 'VPDIMZ':
                        hanging_height = abs(n_item.location[2])

                    if n_item.lm_closets.is_counter_top_insert_bp:
                        countertop_height = n_item.location[2]
                        for k_item in n_item.children:
                            for x_item in k_item.children:
                                if not x_item.hide:
                                    ctop_thickness = abs(x_item.dimensions[2])

                    if n_item.lm_closets.is_closet_top_bp:
                        for k_item in n_item.children:
                            if k_item.mv.type == 'BPASSEMBLY':
                                for f_item in k_item.children:
                                    if f_item.mv.type == 'VPDIMZ':
                                        topshelf_thickness = abs(
                                            f_item.location[2])
                hanging = hanging_height > 0
                ctop = ctop_thickness == 0
                tshelf = topshelf_thickness == 0
                if hanging and ctop and tshelf:
                    dim = fd_types.Dimension()
                    dim.parent(assembly.obj_bp)
                    dim.start_x(value=offset)
                    dim.start_y(value=offset)
                    dim.start_z(value=0)
                    dim.end_z(value=hanging_height)
                    label = self.to_inch_lbl(hanging_height)
                    dim.set_label(" ")
                    bpy.ops.object.text_add()
                    text = context.active_object
                    text.parent = assembly.obj_bp
                    text.rotation_euler.x = math.radians(0)
                    text.rotation_euler.y = math.radians(-90)
                    text.rotation_euler.z = math.radians(90)
                    text.location.x = offset - unit.inch(1)
                    text.location.y = 0
                    text.location.z = ((hanging_height / 2))
                    text.data.align_x = 'CENTER'
                    text.data.size = .1
                    text.data.body = label
                    text.data.font = self.font
                elif ctop_thickness > 0:
                    dim = fd_types.Dimension()
                    dim.parent(assembly.obj_bp)
                    dim.start_x(value=offset)
                    dim.start_y(value=offset)
                    dim.start_z(value=0)
                    dim.end_z(value=countertop_height + ctop_thickness)
                    label = self.to_inch_lbl(
                        (countertop_height + ctop_thickness))
                    dim.set_label(" ")
                    bpy.ops.object.text_add()
                    text = context.active_object
                    text.parent = assembly.obj_bp
                    text.rotation_euler.x = math.radians(0)
                    text.rotation_euler.y = math.radians(-90)
                    text.rotation_euler.z = math.radians(90)
                    text.location.x = offset - unit.inch(1)
                    text.location.y = 0
                    text.location.z = (
                        (countertop_height + ctop_thickness) / 2)
                    text.data.align_x = 'CENTER'
                    text.data.size = .1
                    text.data.body = label
                    text.data.font = self.font
                elif topshelf_thickness > 0:
                    dim = fd_types.Dimension()
                    dim.parent(assembly.obj_bp)
                    dim.start_x(value=offset)
                    dim.start_y(value=offset)
                    dim.start_z(value=0)
                    dim.end_z(value=hanging_height + topshelf_thickness)
                    label = self.to_inch_lbl(
                        (hanging_height + topshelf_thickness))
                    dim.set_label(" ")
                    bpy.ops.object.text_add()
                    text = context.active_object
                    text.parent = assembly.obj_bp
                    text.rotation_euler.x = math.radians(0)
                    text.rotation_euler.y = math.radians(-90)
                    text.rotation_euler.z = math.radians(90)
                    text.location.x = offset - unit.inch(1)
                    text.location.y = 0
                    text.location.z = (
                        (hanging_height + topshelf_thickness) / 2)
                    text.data.align_x = 'CENTER'
                    text.data.size = .1
                    text.data.body = label
                    text.data.font = self.font

    def draw_hashmark(self, context, parent,
                      location=(unit.inch(1.06), 0, unit.inch(1.06)),
                      rotation=(0, math.radians(45), 0),
                      length=unit.inch(3)):
        # The following creates a Poly NURBS curve that looks like a dash/line
        # Create a curve and define its rendering settings
        hashmark_n = 'Hashmark'
        line = bpy.data.curves.new(hashmark_n, 'CURVE')
        line.dimensions = '3D'
        line.fill_mode = 'HALF'
        line.bevel_resolution = 0
        line.bevel_depth = unit.inch(0.1)

        # Create a straight line spline for the curve and adjust its points' properties
        spline = line.splines.new(type='POLY')
        spline.points.add(1)
        spline.points[0].co = (0, 0, -0.5 * length, 1)
        spline.points[1].co = (0, 0, 0.5 * length, 1)
        spline.points[0].tilt = math.radians(90)
        spline.points[1].tilt = math.radians(90)

        # Create the hashmark object that contains the curve and spline data
        hashmark_obj = bpy.data.objects.new(hashmark_n, line)
        hashmark_obj.parent = parent
        hashmark_obj.location = location
        hashmark_obj.rotation_euler = rotation
        context.scene.objects.link(hashmark_obj)
        self.hashmarks.append(hashmark_obj)
        return hashmark_obj

    def plan_view_hashmarks(self, context, obj, mk_length=9, mk_offset=3.18):
        width, depth, height = 0, 0, 0
        wall_assembly = fd_types.Assembly(obj)
        wall_angle = round(obj.rotation_euler[2], 4)
        label_rotation = (math.radians(
            90), math.radians(135), math.radians(-90))
        label_offset = unit.inch(-7)

        if context.scene.fd_roombuilder.room_type == 'CUSTOM':
            for item in wall_assembly.obj_bp.children:
                if item.mv.is_wall_mesh:
                    width = item.dimensions[0]
                    depth = item.dimensions[1]
                    height = item.dimensions[2]
            location = ((width + unit.inch((mk_offset))),
                        (depth + unit.inch(mk_offset)), height)
            rotation = (math.radians(135), math.radians(90), 0)
            label_rotation = (math.radians(90), math.radians(270),
                              math.radians(-90))
            if wall_angle == round(math.radians(0), 4):  # ok
                location = ((width + unit.inch((mk_offset))),
                            (depth + unit.inch(mk_offset)), height)
                rotation = (math.radians(135), math.radians(90), 0)
                label_rotation = (math.radians(90), math.radians(135),
                                  math.radians(-90))
            elif wall_angle == round(math.radians(90), 4):  # ok
                location = ((width + unit.inch((mk_offset))),
                            (depth + unit.inch(mk_offset)), height)
                rotation = (math.radians(135), math.radians(90), 0)
                label_rotation = (math.radians(
                    90), math.radians(225), math.radians(-90))
            elif wall_angle == round(math.radians(-90), 4):  # ok
                location = ((width + depth - unit.inch((mk_offset))),
                            (depth + unit.inch(mk_offset)), height)
                rotation = (math.radians(135), math.radians(90), 0)
                label_rotation = (math.radians(
                    90), math.radians(45), math.radians(270))
                label_offset = unit.inch(-9)
            elif wall_angle == round(math.radians(180), 4):  # ok
                location = ((width + unit.inch((mk_offset))),
                            (depth + unit.inch(mk_offset)), height)
                rotation = (math.radians(-225),
                            math.radians(90), 0)
                label_rotation = (math.radians(
                    90), math.radians(315), math.radians(270))
                label_offset = unit.inch(-9)
        else:
            width = wall_assembly.obj_x.location.x
            depth = wall_assembly.obj_y.location.y
            height = wall_assembly.obj_z.location.z
            location = ((width + depth + unit.inch((mk_offset))),
                        (depth + unit.inch(mk_offset)), height)
            rotation = (math.radians(135),
                        math.radians(90), 0)
            if wall_angle == round(math.radians(0), 4):
                label_rotation = (math.radians(
                    90), math.radians(135), math.radians(270))
            elif wall_angle == round(math.radians(90), 4):
                label_rotation = (math.radians(
                    90), math.radians(225), math.radians(270))
            elif wall_angle == round(math.radians(-90), 4):
                label_rotation = (math.radians(
                    90), math.radians(45), math.radians(270))
                label_offset = unit.inch(-9)
            elif wall_angle == round(math.radians(180), 4):
                label_rotation = (math.radians(
                    90), math.radians(-45), math.radians(270))
                label_offset = unit.inch(-9)

        hashmark = self.draw_hashmark(
            context, obj, location, rotation, length=unit.inch(mk_length))
        label = str(round(height / unit.inch(1))) + "\""
        bpy.ops.object.text_add()
        text = context.active_object
        text.parent = hashmark
        text.rotation_euler = label_rotation
        text.location.x = 0
        text.location.y = 0
        text.location.z = label_offset
        text.data.align_x = 'CENTER'
        text.data.size = .1
        text.data.body = str(label)
        text.data.font = self.font
        hashmark.hide = True
        if len(hashmark.children) > 0:
            hashmark.children[0].hide = True

        return hashmark, height

    def create_plan_view_scene(self, context):
        bpy.ops.scene.new('INVOKE_DEFAULT', type='EMPTY')
        pv_scene = context.scene
        pv_scene.name = "Plan View"
        pv_scene.mv.name_scene = "Plan View"
        pv_scene.mv.plan_view_scene = True
        self.create_linesets(pv_scene)
        hashmark_heights = {}
        hashmark_length = 9
        hashmark_offset = 3.18
        grp = bpy.data.groups.new("Plan View")
        custom_room = False
        for obj in self.main_scene.objects:
            # Add Floor and Ceiling Obstacles to Plan View
            if obj.mv.type == 'OBSTACLE':
                pv_scene.objects.link(obj)
                for child in obj.children:
                    child.hide_render = False
                    pv_scene.objects.link(child)

            if obj.mv.type == 'BPWALL':
                pv_scene.objects.link(obj)
                # Only link all of the wall meshes

                hashmark, height = self.plan_view_hashmarks(
                    context, obj, hashmark_length, hashmark_offset)
                hashmark_heights[hashmark.name] = round(height, 2)

                for child in obj.children:
                    if child.mv.is_wall_mesh:
                        child.select = True
                        pv_scene.objects.link(child)
                        grp.objects.link(child)

                wall = fd_types.Wall(obj_bp=obj)

                self.plan_view_products_labels(context, wall)

                # Add countertop cutparts to plan view
                for child in obj.children:
                    for item in child.children:
                        if item.lm_closets.is_counter_top_insert_bp:
                            for c in item.children:
                                for cc in c.children:
                                    if not cc.hide:
                                        cube_dims = cc.dimensions
                                        altered_dims = (cube_dims[0] + unit.inch(0.06),
                                                        cube_dims[1],
                                                        cube_dims[2])
                                        parent_assy = fd_types.Assembly(c)
                                        x_loc = 0 - unit.inch(0.03)
                                        y_loc = parent_assy.obj_y.location.y
                                        z_loc = cc.parent.parent.location[2] * -1
                                        ctop_mesh = utils.create_cube_mesh(
                                            cc.name, altered_dims)
                                        ctop_mesh.parent = cc.parent
                                        ctop_mesh.location = (x_loc,
                                                              y_loc,
                                                              z_loc)
                                        ctop_mesh.rotation_euler = cc.rotation_euler
                                        ctop_mesh.mv.type = 'CAGE'

                if wall.obj_bp and wall.obj_x and wall.obj_y and wall.obj_z:

                    wall_angles = wall.obj_bp.rotation_euler
                    wall_z_angle = round(math.degrees(wall_angles[2]))
                    is_straight_angle = (wall_z_angle == 180)
                    is_btwn_right_square = wall_z_angle > 90 and wall_z_angle < 180

                    wall_label = self.to_inch_str(wall.obj_x.location.x) + "\""
                    dim = fd_types.Dimension()
                    dim.parent(wall.obj_bp)
                    dim.start_y(value=unit.inch(4) + wall.obj_y.location.y)
                    dim.start_z(value=wall.obj_z.location.z + unit.inch(8))
                    dim.end_x(value=wall.obj_x.location.x)
                    dim.set_label(" ")
                    bpy.ops.object.text_add()
                    text = context.active_object
                    text.parent = wall.obj_bp
                    text.location = (wall.obj_x.location.x/2,
                                     unit.inch(12),
                                     wall.obj_z.location.z)
                    if is_straight_angle:
                        text.rotation_euler = wall.obj_bp.rotation_euler
                        text.location.y = unit.inch(15)
                    if is_btwn_right_square:
                        text.rotation_euler[2] = math.radians(180)
                        text.location.y = unit.inch(15)
                    text.data.size = .1
                    text.data.body = wall_label
                    text.data.align_x = 'CENTER'
                    text.data.font = self.font

                    self.ignore_obj_list.append(dim.anchor)
                    self.ignore_obj_list.append(dim.end_point)

                    bpy.ops.object.text_add()
                    text = context.active_object
                    text.parent = wall.obj_bp
                    text.location = (wall.obj_x.location.x/2,
                                     unit.inch(1.5), wall.obj_z.location.z)
                    text.data.size = .1
                    text.data.body = wall.obj_bp.mv.name_object
                    text.data.align_x = 'CENTER'
                    text.data.font = self.font

                    obj_bps = wall.get_wall_groups()
                    # Create Cubes for all products
                    for obj_bp in obj_bps:
                        if obj_bp.mv.plan_draw_id != "":
                            eval('bpy.ops.' + obj_bp.mv.plan_draw_id +
                                 '(object_name=obj_bp.name)')

                        else:
                            assembly = fd_types.Assembly(obj_bp)
                            assembly_mesh = utils.create_cube_mesh(assembly.obj_bp.mv.name_object,
                                                                   (assembly.obj_x.location.x,
                                                                    assembly.obj_y.location.y,
                                                                    assembly.obj_z.location.z))
                            assembly_mesh.parent = wall.obj_bp
                            assembly_mesh.location = assembly.obj_bp.location
                            assembly_mesh.rotation_euler = assembly.obj_bp.rotation_euler
                            assembly_mesh.mv.type = 'CAGE'
                            distance = unit.inch(14)
                            distance += wall.obj_y.location.y

                            dim = fd_types.Dimension()
                            dim.parent(assembly_mesh)
                            dim.start_y(value=distance)
                            dim.start_z(value=0)
                            dim.end_x(value=assembly.obj_x.location.x)

                            self.ignore_obj_list.append(dim.anchor)
                            self.ignore_obj_list.append(dim.end_point)

                    if wall and wall.get_wall_mesh():
                        wall.get_wall_mesh().select = True

        show_all_hashmarks = False
        first_hashmark_str = list(sorted(hashmark_heights.keys()))[:1][0]
        first_hashmark = bpy.data.objects[str(first_hashmark_str)]
        first_hashmark.hide = False
        if len(first_hashmark.children) > 0:
            first_hashmark.children[0].hide = False

        hashmark_heights_mode = self.list_mode(list(hashmark_heights.values()))

        for key, value in hashmark_heights.items():
            if value != hashmark_heights_mode:
                show_all_hashmarks = True

        for item in hashmark_heights:
            if item in bpy.data.objects and not show_all_hashmarks:
                hashmark = bpy.data.objects[str(item)]
                if hashmark.hide:
                    bpy.data.objects.remove(hashmark, do_unlink=True)
            elif show_all_hashmarks:
                hashmark = bpy.data.objects[str(item)]
                hashmark.hide = False
                if len(hashmark.children) > 0:
                    hashmark.children[0].hide = False

        if custom_room and show_all_hashmarks:
            hashmarks_dict = {}
            counter = 0
            hashmarks = list(sorted(hashmark_heights.keys()))
            for item in hashmarks:
                hashmark = bpy.data.objects[str(item)]
                if not hashmark.hide and item in bpy.data.objects:
                    wall = fd_types.Assembly(hashmark.parent)
                    hashmarks_dict[counter] = {
                        "hashmark": hashmark.name,
                        "rotation": round(math.degrees(
                            hashmark.parent.rotation_euler[2])),
                        "wall_depth": wall.obj_y.location.y
                    }
                    counter += 1
            for i in range(len(hashmarks_dict)):
                hashmark_offset_inches = hashmark_offset * unit.inch(1)
                turn_angle = 0
                if i + 1 in hashmarks_dict.keys():
                    hashmark = bpy.data.objects[hashmarks_dict[i]["hashmark"]]
                    current_angle = hashmarks_dict[i]["rotation"]
                    next_one_angle = hashmarks_dict[i + 1]["rotation"]
                    turn_angle = current_angle - next_one_angle
                    wall_depth = hashmarks_dict[i]["wall_depth"]
                    dim_offset = (hashmark_offset_inches * 2) + wall_depth
                    cyl_angle_offset = math.radians(-270)
                    text_angle_offset = math.radians(90)
                    children = hashmark.children
                    if (turn_angle < 0 and turn_angle >= -90):
                        hashmark.location[0] -= dim_offset
                        hashmark.rotation_euler[0] -= cyl_angle_offset
                        if len(children) > 0:
                            children[0].rotation_euler[1] += text_angle_offset
                    if current_angle == 180 and next_one_angle < 0:
                        hashmark.location[0] -= dim_offset
                        hashmark.rotation_euler[0] -= math.radians(90)
                        if len(children) > 0:
                            children[0].rotation_euler[1] += math.radians(90)

        camera = self.create_camera(pv_scene)
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.view3d.camera_to_view_selected()
        camera.data.ortho_scale += self.pv_pad

    def unlink_cleats(self, context):
        # ungrouping objects we do not want to be rendered.
        for obj in bpy.data.objects:
            cutpart = 'cutpart' in obj.name.lower()
            cleat = 'cleat' in obj.name.lower()
            if cleat and cutpart:
                obj.select = True
                bpy.ops.group.objects_remove_all()

    def create_elv_view_scene(self, context, assembly):
        if assembly.obj_bp and assembly.obj_x and assembly.obj_y and assembly.obj_z:
            grp = bpy.data.groups.new(assembly.obj_bp.mv.name_object)
            new_scene = self.create_new_scene(context, grp, assembly.obj_bp)

            self.group_children(grp, assembly.obj_bp)
#             wall_mesh = utils.create_cube_mesh(assembly.obj_bp.mv.name_object,
#                                                (assembly.obj_x.location.x,
#                                                 assembly.obj_y.location.y,
#                                                 assembly.obj_z.location.z))
#
#             wall_mesh.parent = assembly.obj_bp
#             grp.objects.link(wall_mesh)

            instance = bpy.data.objects.new(
                assembly.obj_bp.mv.name_object + " " + "Instance", None)
            new_scene.objects.link(instance)
            instance.dupli_type = 'GROUP'
            instance.dupli_group = grp

            # Add partitions to the dimension ignore list so
            # it won't be linked to the scene "automatically"
            #
            # It also get rid of the hang height dimension
            self.ignore_obj_list.append(assembly.obj_bp)
            for item in assembly.obj_bp.children:
                if item.mv.type == "BPASSEMBLY":
                    for n_item in item.children:
                        if 'partition' in n_item.name.lower():
                            self.ignore_obj_list.append(n_item)
                if item.mv.type == 'VISDIM_A':
                    self.ignore_obj_list.append(item)

            self.link_desired_dims_to_scene(new_scene, assembly.obj_bp)
            self.widths_uppers_and_lowers(context, assembly)
            self.add_text(context, assembly)
            self.wall_width_dimension(assembly)
            self.build_height_dimension(context, assembly)
            self.section_depths(context, assembly)

            for item in assembly.obj_bp.children:
                self.arrayed_shelves_section_depth_dimension(context, item)
                if item.mv.is_wall_mesh:
                    self.wall_height_dimension(context, item)
                # Hanging Opening Item Level.
                if item.mv.type == "BPASSEMBLY":
                    self.flat_crown(context, item)
                    self.slanted_shoes_shelf(context, item)
                    self.glass_shelves(context, item)
                    self.valances(context, item)
                    self.light_rails(context, item)
                    self.non_standard_shelves_dimensions(context, item)
                    self.topshelf_hashmark(context, item)
                    self.topshelf_exposed_label(context, item)
                    self.variable_opening_label(context, item)
                    self.parallel_partition_dimension(context, item)
                    self.toe_kick_dimension(context, item, assembly)
                    self.fullback_labeling(context, item)
                    self.countertop_hashmark(context, item)
                    self.countertop_exposed_label(context, item)
                    self.file_drawer_labeling(context, item)
                    self.add_filler_labeling(context, item)

            camera = self.create_camera(new_scene)
            camera.rotation_euler.x = math.radians(90.0)
            camera.rotation_euler.z = assembly.obj_bp.rotation_euler.z
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.view3d.camera_to_view_selected()
            camera.data.ortho_scale += self.pv_pad
            instance.hide_select = True
            bpy.ops.object.select_all(action='DESELECT')

    def create_single_elv_view(self, context):
        grp = bpy.data.groups.new(self.single_scene_name)

        bpy.ops.scene.new('INVOKE_DEFAULT', type='EMPTY')
        new_scene = context.scene
        new_scene.name = grp.name
        new_scene.mv.name_scene = self.single_scene_name
        new_scene.mv.elevation_img_name = self.single_scene_name
        new_scene.mv.plan_view_scene = False
        new_scene.mv.elevation_scene = True
        self.create_linesets(new_scene)

        for item in self.single_scene_objs:
            obj = bpy.data.objects[item.name]
            self.group_children(grp, obj)
            self.link_dims_to_scene(new_scene, obj)

        instance = bpy.data.objects.new(
            self.single_scene_name + " " + "Instance", None)
        new_scene.objects.link(instance)
        instance.dupli_type = 'GROUP'
        instance.dupli_group = grp

        new_scene.world = self.main_scene.world
        # ----------------------------------------------------------------------------------------

        # self.link_dims_to_scene(new_scene, assembly.obj_bp)

        # Skip for now
        # self.add_text(context, assembly)

        camera = self.create_camera(new_scene)
        camera.rotation_euler.x = math.radians(90.0)
        # camera.rotation_euler.z = assembly.obj_bp.rotation_euler.z
        bpy.ops.object.select_all(action='SELECT')
        # wall_mesh.select = True
        bpy.ops.view3d.camera_to_view_selected()
        camera.data.ortho_scale += self.pv_pad

    # Will add assemblies that must not show as hidden line to a list
    def exclude_fs_hidden(self):
        objects = bpy.data.objects
        exclude_objs = []

        # Find top and bottom KD shelves by looking for expression in drivers
        # used to remove top or bottom shelves
        shelves = [obj for obj in objects if obj.lm_closets.is_shelf_bp]
        for s in shelves:
            for d in s.animation_data.drivers:
                exp = d.driver.expression
                rem_top_str = 'Remove_Top_Shelf'
                rem_bot_str = 'Remove_Bottom_Hanging_Shelf'
                top_kd_str = 'Top_KD'
                bot_kd_str = 'Bottom_KD'
                if (rem_top_str in exp or
                    rem_bot_str in exp or
                    top_kd_str in exp or
                        bot_kd_str in exp):
                    exclude_objs.append(s)

        # Find vertical panels
        panels = [obj for obj in objects if obj.lm_closets.is_panel_bp or
                  obj.lm_closets.is_blind_corner_panel_bp]
        for p in panels:
            exclude_objs.append(p)

        # Find drawer structures
        drawers = [obj for obj in objects if obj.lm_closets.is_drawer_box_bp
                   or obj.lm_closets.is_drawer_side_bp
                   or obj.lm_closets.is_drawer_back_bp
                   or obj.lm_closets.is_drawer_sub_front_bp
                   or obj.lm_closets.is_drawer_bottom_bp]
        for d in drawers:
            exclude_objs.append(d)

        # Find toe kicks
        tks = [obj for obj in objects if obj.lm_closets.is_toe_kick_end_cap_bp
               or obj.lm_closets.is_toe_kick_stringer_bp]
        for t in tks:
            exclude_objs.append(t)

        # Find backings
        backs = [obj for obj in objects if obj.lm_closets.is_back_bp or
                 obj.lm_closets.is_top_back_bp or
                 obj.lm_closets.is_bottom_back_bp or
                 obj.lm_closets.is_hutch_back_bp or
                 obj.lm_closets.is_drawer_back_bp]
        for b in backs:
            exclude_objs.append(b)

        return exclude_objs

    def execute(self, context):
        context.window_manager.mv.use_opengl_dimensions = True
        self.font = opengl_dim.get_custom_font()
        self.font_bold = opengl_dim.get_custom_font_bold()
        self.create_linestyles()
        self.main_scene = context.scene
        context.scene.name = "_Main"

        if self.use_single_scene:
            self.create_single_elv_view(context)

        else:
            for obj in bpy.data.objects:
                if obj.type == 'CURVE' and 'hashmark' in obj.name.lower():
                    bpy.data.objects.remove(obj, do_unlink=True)
            for obj in bpy.data.objects:
                no_users = obj.users == 0
                parent = obj.parent
                ctop = 'countertop' in obj.name.lower()
                cutpart = 'cutpart' in obj.name.lower()
                try:
                    partition = 'partition' in parent.name.lower()
                except AttributeError:
                    partition = False
                try:
                    wall = 'wall' in parent.name.lower()
                except AttributeError:
                    wall = False
                font = obj.type == 'FONT'
                if no_users and cutpart and ctop:
                    bpy.data.objects.remove(obj, do_unlink=True)
                if no_users and font and partition:
                    obj.hide = True
                    obj.hide_render = True
                if no_users and font and wall:
                    obj.hide = True
                    obj.hide_render = True

            bpy.ops.fd_scene.clear_2d_views()

            self.create_plan_view_scene(context)

            for obj in self.main_scene.objects:
                if obj.mv.type == 'BPWALL':
                    wall = fd_types.Wall(obj_bp=obj)
                    if len(wall.get_wall_groups()) > 0:
                        self.create_elv_view_scene(context, wall)

        self.clear_unused_linestyles()
        bpy.context.screen.scene = self.main_scene
        wm = context.window_manager.mv
        wm.elevation_scene_index = 0
        bpy.ops.object.select_all(action='DESELECT')
        self.unlink_cleats(context)
        bpy.ops.object.select_all(action='DESELECT')

        # Add objects to freestyle hidden line exclusion group
        fs_exclude_grp = bpy.data.groups['FS Hidden Exclude']
        fs_exclude_objs = self.exclude_fs_hidden()
        for item in fs_exclude_objs:
            for c in item.children:
                if c.type == 'MESH' and c.name not in fs_exclude_grp.objects:
                    fs_exclude_grp.objects.link(c)

        return {'FINISHED'}


class OPERATOR_render_2d_views(bpy.types.Operator):
    bl_idname = "2dviews.render_2d_views"
    bl_label = "Render 2D Views"
    bl_description = "Renders 2d Scenes"

    r = 0
    g = 0
    b = 0
    a = 0

    def check_file(self, path):

        while not os.path.exists(path + ".jpg"):
            time.sleep(0.1)

        p = psutil.Process()
        open_files = []

        for p in p.open_files():
            open_files.append(p.path)

        if path in open_files:
            print(path, "is in", open_files)
            print("File is still open!")

            self.check_file(path)

        else:
            return True

    def save_dim_color(self, color):
        self.r = color[0]
        self.g = color[1]
        self.b = color[2]
        self.a = color[3]

    def reset_dim_color(self, context):
        context.scene.mv.opengl_dim.gl_default_color[0] = self.r
        context.scene.mv.opengl_dim.gl_default_color[1] = self.g
        context.scene.mv.opengl_dim.gl_default_color[2] = self.b
        context.scene.mv.opengl_dim.gl_default_color[3] = self.a

    def render_scene(self, context, scene):
        context.screen.scene = scene
        objects = bpy.data.objects
        # Fix glitch where vertical dividers render as diagonal lines
        # Previous solution used a remesh modifier
        # Will remove that and replace it with a Triangulate modifier
        mod_rm_name = 'Remesh'
        mod_tri_name = 'Triangulate'
        for obj in objects:
            if obj.type == 'MESH' and '.Part' in obj.name:
                if mod_rm_name in obj.modifiers:
                    obj.modifiers.remove(obj.modifiers.get(mod_rm_name))
                if mod_tri_name not in obj.modifiers:
                    mod_tri = obj.modifiers.new(mod_tri_name, 'TRIANGULATE')
                    mod_tri.quad_method = 'SHORTEST_DIAGONAL'
                    mod_tri.ngon_method = 'BEAUTY'

        self.save_dim_color(scene.mv.opengl_dim.gl_default_color)

        scene.mv.opengl_dim.gl_default_color = (0.1, 0.1, 0.1, 1.0)
        rd = scene.render
        rl = rd.layers.active
        rd.filepath = bpy.app.tempdir
        rd.filepath += scene.name

        freestyle_settings = rl.freestyle_settings
        rd.use_freestyle = True
        rd.image_settings.file_format = 'JPEG'
        rd.line_thickness = 0.75
        rd.resolution_percentage = 100
        rl.use_solid = False
        rl.use_pass_combined = True
        rl.use_pass_z = False
        freestyle_settings.crease_angle = 2.617994

#         file_format = scene.render.image_settings.file_format.lower()

        if scene.mv.render_type_2d_view == 'GREYSCALE':
            rd.engine = 'BLENDER_RENDER'
        else:
            rd.engine = 'CYCLES'

        # Setup for rendering 3D text labels without Freestyle
        # Create RenderLayer to contain Label objects
        if 'Labels' not in scene.render.layers:
            labels_rl = rd.layers.new('Labels')
            # Make Labels render layer include only layer 1
            labels_rl.layers = [i == 1 for i in range(len(labels_rl.layers))]
        elif 'Labels' in scene.render.layers:
            labels_rl = scene.render.layers['Labels']

        # Exclude layer 1 from rendering in main RenderLayer
        rl.layers[1] = False

        # Make sure layers 0 and 1 are visible
        scene.layers[0] = True
        scene.layers[1] = True

        # Add all the text and curve objects in the scene only to layer 1
        scene_labels = [obj for obj in scene.objects if obj.type ==
                        'FONT' or obj.type == 'CURVE']
        for label in scene_labels:
            label.layers = [i == 1 for i in range(len(label.layers))]

        # Composite 2D View Freestyle layer and Labels layer
        # Start by enabling use of nodes and removing default nodes
        scene.use_nodes = True
        tree = scene.node_tree

        for node in tree.nodes:
            tree.nodes.remove(node)

        # Create nodes needed to overlay 3D text on Freestyle layer
        view2d_rl_node = tree.nodes.new(type='CompositorNodeRLayers')
        view2d_rl_node.layer = rl.name

        labels_rl_node = tree.nodes.new(type='CompositorNodeRLayers')
        labels_rl_node.layer = labels_rl.name

        mix_node = tree.nodes.new(type='CompositorNodeMixRGB')
        mix_node.blend_type = 'MULTIPLY'

        comp_node = tree.nodes.new(type='CompositorNodeComposite')
        comp_node.use_alpha = False

        # Connect nodes
        tree.links.new(view2d_rl_node.outputs['Image'], mix_node.inputs[1])
        tree.links.new(labels_rl_node.outputs['Image'], mix_node.inputs[2])
        tree.links.new(mix_node.outputs['Image'], comp_node.inputs['Image'])

        # Render composite
        bpy.ops.render.render('INVOKE_DEFAULT', write_still=True)
        img_path = bpy.path.abspath(scene.render.filepath)
        self.check_file(img_path)

        img_result = opengl_dim.render_opengl(self, context)

        image_view = context.window_manager.mv.image_views.add()
        image_view.name = img_result.name
        image_view.image_name = img_result.name

        if scene.mv.plan_view_scene:
            image_view.is_plan_view = True

        if scene.mv.elevation_scene:
            image_view.is_elv_view = True

            # Clear and deactivate nodes to prevent conflicts with other rendering methods
            for node in tree.nodes:
                tree.nodes.remove(node)
            scene.use_nodes = False

        self.reset_dim_color(context)

    def execute(self, context):
        file_path = bpy.app.tempdir if bpy.data.filepath == "" else os.path.dirname(
            bpy.data.filepath)

        # HACK: YOU HAVE TO SET THE CURRENT SCENE TO RENDER JPEG BECAUSE
        # OF REPORTS LAB AND BLENDER LIMITATIONS. :(
        rd = context.scene.render
        rd.image_settings.file_format = 'JPEG'

        current_scene = context.screen.scene

        for scene in bpy.data.scenes:
            if scene.mv.elevation_selected:
                self.render_scene(context, scene)

        context.screen.scene = current_scene

        return {'FINISHED'}


class OPERATOR_view_image(bpy.types.Operator):
    bl_idname = "2dviews.view_image"
    bl_label = "View Image"
    bl_description = "Opens the image editor to view the 2D view."

    image_name = bpy.props.StringProperty(name="Object Name",
                                          description="This is the readable name of the object")

    def execute(self, context):
        bpy.ops.fd_general.open_new_window(space_type='IMAGE_EDITOR')
        image_view = context.window_manager.mv.image_views[self.image_name]

        override = context.copy()
        areas = context.screen.areas

        for area in areas:
            for space in area.spaces:
                if space.type == 'IMAGE_EDITOR':
                    override['space'] = space
                    for image in bpy.data.images:
                        if image.name == image_view.image_name:
                            space.image = image

            for region in area.regions:
                if region.type == 'WINDOW':
                    override['region'] = region

        override['window'] = context.window
        override['area'] = context.area
        bpy.ops.image.view_all(override, fit_view=True)

        return {'FINISHED'}


class OPERATOR_delete_image(bpy.types.Operator):
    bl_idname = "2dviews.delete_image"
    bl_label = "View Image"
    bl_description = "Delete the Image"

    image_name = bpy.props.StringProperty(name="Object Name",
                                          description="This is the readable name of the object")

    def execute(self, context):
        for index, iv in enumerate(context.window_manager.mv.image_views):
            if iv.name == self.image_name:
                context.window_manager.mv.image_views.remove(index)

        for image in bpy.data.images:
            if image.name == self.image_name:
                bpy.data.images.remove(image)
                break

        return {'FINISHED'}


class OPERATOR_create_snap_shot(bpy.types.Operator):
    bl_idname = "2dviews.create_snap_shot"
    bl_label = "Create New View"
    bl_description = "Renders 2d Scenes"

    def execute(self, context):
        bpy.ops.view3d.toolshelf()
        context.area.header_text_set(
            text="Position view then LEFT CLICK to take screen shot. ESC to Cancel.")
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def get_file_path(self):
        counter = 1
        while os.path.exists(os.path.join(bpy.app.tempdir, "View " + str(counter) + ".png")):
            counter += 1
        return os.path.join(bpy.app.tempdir, "View " + str(counter) + ".png")

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}

        if event.type in {'ESC', 'RIGHTMOUSE'}:
            context.area.header_text_set()
            bpy.ops.view3d.toolshelf()
            return {'FINISHED'}

        if event.type in {'LEFTMOUSE'}:
            context.area.header_text_set(" ")
            file_path = self.get_file_path()
            # The PDF writter can only use JPEG images
            context.scene.render.image_settings.file_format = 'JPEG'
            bpy.ops.screen.screenshot(filepath=file_path, full=False)
            bpy.ops.view3d.toolshelf()
            context.area.header_text_set()
            image = bpy.data.images.load(file_path)
            image_view = context.window_manager.mv.image_views.add()
            image_view.name = os.path.splitext(image.name)[0]
            image_view.image_name = image.name

            return {'FINISHED'}

        return {'RUNNING_MODAL'}


def register():
    bpy.types.WindowManager.views_2d = bpy.props.PointerProperty(
        type=WM_PROPERTIES_2d_views)

    bpy.utils.register_class(PANEL_2d_views)
    bpy.utils.register_class(LIST_scenes)
    bpy.utils.register_class(LIST_2d_images)
    bpy.utils.register_class(MENU_2dview_reports)
    bpy.utils.register_class(MENU_elevation_scene_options)
    bpy.utils.register_class(OPERATOR_genereate_2d_views)
    bpy.utils.register_class(OPERATOR_render_2d_views)
    bpy.utils.register_class(OPERATOR_view_image)
    bpy.utils.register_class(OPERATOR_delete_image)
    bpy.utils.register_class(OPERATOR_create_new_view)
    bpy.utils.register_class(OPERATOR_append_to_view)
    bpy.utils.register_class(OPERATOR_create_snap_shot)

    bpy.utils.register_class(OPERATOR_move_image_list_item)

    operators.register()
    report_2d_drawings.register()


def unregister():
    bpy.utils.unregister_class(PANEL_2d_views)
    bpy.utils.unregister_class(LIST_scenes)
    bpy.utils.unregister_class(LIST_2d_images)
    bpy.utils.unregister_class(MENU_2dview_reports)
    bpy.utils.unregister_class(MENU_elevation_scene_options)
    bpy.utils.unregister_class(OPERATOR_genereate_2d_views)
    bpy.utils.unregister_class(OPERATOR_render_2d_views)
    bpy.utils.unregister_class(OPERATOR_view_image)
    bpy.utils.unregister_class(OPERATOR_delete_image)
    bpy.utils.unregister_class(OPERATOR_create_new_view)
    bpy.utils.unregister_class(OPERATOR_append_to_view)
    bpy.utils.unregister_class(OPERATOR_create_snap_shot)

    bpy.utils.unregister_class(OPERATOR_move_image_list_item)

    operators.unregister()
    report_2d_drawings.unregister()


if __name__ == "__main__":
    register()
