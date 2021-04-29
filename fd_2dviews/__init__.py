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
import mathutils
import string
import random
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


def spread(arg):
    ret = []
    for i in arg:
        ret.extend(i) if isinstance(i, list) else ret.append(i)
    return ret


def get_dimension_props():
    dimprops = None
    if hasattr(bpy.context, 'scene'):
        dimprops = eval("bpy.context.scene.mv_closet_dimensions")
    return dimprops


class WM_PROPERTIES_2d_views(bpy.types.PropertyGroup):

    default_page_options = [('PLAN+1ELVS', "Plan and elevations",
                             'Plan on top plus three elevations (U-Shaped)'),
                            ('3ELVS', 'Three per page',
                                'Three elevations per page'),
                            ('2ELVS', "Two per page",
                                'Two elevations per page'),
                            ('SINGLE', "One per page",
                                'One elevation per page'),
                            ]

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
    
    accordions_layout_setting = EnumProperty(name="Page Layout Settings",
                                             items=[
                                                 ('2_ACCORD', "Two Accordions per page",
                                                  'Two accordions per page'),
                                                 ('1_ACCORD', "One Accordion per page",
                                                  'One accordion per page'),
                                                 ('PLAN+1ACCORDS', "Plan and Accordions",
                                                  'Plan on top plus accordions (U-Shaped)'),
                                                 ('PLAN+1ELVS', "Plan and elevations",
                                                  'Plan on top plus three elevations (U-Shaped)'),
                                                 ('3ELVS', 'Three per page',
                                                  'Three elevations per page'),
                                                 ('2ELVS', "Two per page",
                                                  'Two elevations per page'),
                                                 ('SINGLE', "One per page",
                                                  'One elevation per page'),
                                                   ],default='2_ACCORD')

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

        # options_box = panel_box.box()
        # row = options_box.row(align=True)
        # row.prop(props, 'expand_options', icon='TRIA_DOWN' if props.expand_options else 'TRIA_RIGHT', icon_only=True, emboss=False)
        # row.label("Dimension Options", icon='SCRIPTWIN')

        # if props.expand_options:
        #     self.draw_dim_options(context, options_box)

        row = panel_box.row(align=True)
        row.scale_y = 1.3

        elv_scenes = []
        for scene in bpy.data.scenes:
            if scene.mv.elevation_scene:
                elv_scenes.append(scene)

        # col = panel_box.column(align=True)
        # col.prop(fd_wm, 'render_dimensions',
        #          text='{} Dimensions'.format(
        #              "Render" if fd_wm.render_dimensions else "Do not Render"),
        #          icon='SCRIPTWIN',
        #          toggle=False)

        if len(elv_scenes) < 1:
            # TODO remove if it works on Closet 2D Setup
            # row.label("Include Accordion Views: ")
            # col = panel_box.column(align=True)
            # row = col.row(align=True)
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
            dimprops = get_dimension_props()
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
            if dimprops.include_accordions:
                row.prop(props, 'accordions_layout_setting', "Accordions layout")
            elif not dimprops.include_accordions:
                row.prop(props, 'page_layout_setting', "Elevations layout")
            paper_row = panel_box.row(align=True)
            paper_row.prop(props, 'paper_size', "Paper Size")
            panel_box.menu('MENU_2dview_reports', icon='FILE_BLANK')
            # panel_box.operator('2dviews.create_pdf',text="Create PDF",icon='FILE_BLANK')


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

        main_accordion = 'Z_Main Accordion' in item.mv.name_scene
        if (item.mv.plan_view_scene or item.mv.elevation_scene) and not main_accordion:
            layout.label(item.mv.name_scene, icon='RENDER_REGION')
            layout.prop(item.mv, 'render_type_2d_view', text="")
            layout.prop(item.mv, 'elevation_selected', text="")
        elif not item.mv.plan_view_scene and not item.mv.elevation_scene:
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

    axes = ('X', 'Y', 'Z')

    use_single_scene = bpy.props.BoolProperty(name="Use for Creating Single View",
                                              default=False)

    single_scene_name = bpy.props.StringProperty(name="Single Scene Name")

    single_scene_objs = bpy.props.CollectionProperty(type=single_scene_objs,
                                                     name="Objects for Single Scene",
                                                     description="Objects to Include When Creating a Single View")

    # orphan_products = []
    def get_object_global_location(self, obj):
        return obj.matrix_world * obj.data.vertices[0].co

    def to_inch(self, measure, prec=2):
        if prec > 0:
            return round(measure / unit.inch(1), prec)
        else:
            return round(measure / unit.inch(1))

    def to_inch_str(self, measure, prec=2):
        return str(self.to_inch(measure, prec))

    def to_inch_lbl(self, measure, prec=2):
        return self.to_inch_str(measure, prec) + "\""

    def list_mode(self, lst):
        return max(set(lst), key=lst.count)

    def get_world(self):
        if self.ENV_2D_NAME in bpy.data.worlds:
            return bpy.data.worlds[self.ENV_2D_NAME]
        else:
            world = bpy.data.worlds.new(self.ENV_2D_NAME)
            world.horizon_color = (1.0, 1.0, 1.0)
            return world

    def copy_world_loc(self, source, target, offset=(0, 0, 0)):
        off_mtx = mathutils.Matrix.Translation(mathutils.Vector(offset))
        result_loc = (source.matrix_world * off_mtx).to_translation()
        target.matrix_world.translation = result_loc

    def copy_world_rot(self, source, target, offset=(0, 0, 0)):
        off_rad = [math.radians(o) for o in offset]
        off_mtx = mathutils.Euler(off_rad, source.rotation_mode).to_matrix()
        result_rot = source.matrix_world.to_3x3().normalized() * off_mtx
        target.matrix_world *= result_rot.to_4x4()

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

        icons_linestyle = linestyles.new('Icons Linestyle')
        icons_linestyle.use_chaining = False
        icons_linestyle.color = (0.5, 0.5, 0.5)

    def create_linesets(self, scene):
        f_settings = scene.render.layers[0].freestyle_settings
        linestyles = bpy.data.linestyles
        # groups = bpy.data.groups
        if 'FS Hidden Exclude' not in bpy.data.groups:
            fs_hidden_exclude_grp = bpy.data.groups.new('FS Hidden Exclude')
        else:
            fs_hidden_exclude_grp = bpy.data.groups['FS Hidden Exclude']
        if 'Icons' not in bpy.data.groups:
            icons_grp = bpy.data.groups.new('Icons')
        else:
            icons_grp = bpy.data.groups['Icons']

        icons_lineset = f_settings.linesets.new('Icons Lines')
        icons_lineset.linestyle = linestyles['Icons Linestyle']

        icons_lineset.select_by_visibility = False
        icons_lineset.select_by_edge_types = False
        icons_lineset.select_by_face_marks = False
        icons_lineset.select_by_group = True
        icons_lineset.select_by_image_border = True
        icons_lineset.group = icons_grp
        icons_lineset.group_negation = 'INCLUSIVE'

        f_settings.linesets.new(
            self.VISIBLE_LINESET_NAME).linestyle = linestyles[self.VISIBLE_LINESET_NAME]

        hidden_lineset = f_settings.linesets.new(self.HIDDEN_LINESET_NAME)
        hidden_lineset.linestyle = linestyles[self.HIDDEN_LINESET_NAME]

        hidden_lineset.select_by_visibility = True
        hidden_lineset.visibility = 'HIDDEN'
        hidden_lineset.select_by_edge_types = True
        hidden_lineset.select_by_face_marks = False
        hidden_lineset.select_by_group = True
        hidden_lineset.select_by_image_border = True

        hidden_lineset.select_silhouette = True
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

    def draw_curve(self, name, points, curve_type, closed=False, fill=False):
        # Create curve
        curve = bpy.data.curves.new(name, 'CURVE')
        curve.dimensions = '2D'
        curve.extrude = 0.001
        if fill:
            curve.fill_mode = 'BOTH'
        else:
            curve.fill_mode = 'NONE'
        # Create spline for curve
        spline = curve.splines.new(type=curve_type)
        spline.points.add(len(points)-1)
        if curve_type == 'NURBS':
            spline.use_bezier_u = True
            spline.resolution_u = 8
        if closed:
            spline.use_cyclic_u = True
        for i, p in enumerate(points):
            spline.points[i].co = list(p) + [1]

        # Create object
        obj = bpy.data.objects.new(name, curve)
        return obj

    def move_curve(self, curve, vector):
        loc_vec = mathutils.Vector(vector)
        loc_mtx = mathutils.Matrix.Translation(loc_vec)
        curve.data.transform(loc_mtx)

    def flip_curve(self, curve, axis):
        scale_vec = [a == axis for a in self.axes]
        scale_mtx = mathutils.Matrix.Scale(-1, 4, scale_vec)
        curve.data.transform(scale_mtx)

    def draw_rectangle(self, name, width, height, off_x, off_y, fill=False):
        rect_points = [(off_x, off_y, 0),
                       (off_x, height + off_y, 0),
                       (width + off_x, height + off_y, 0),
                       (width + off_x, off_y, 0)]
        rect_obj = self.draw_curve(name, rect_points, 'POLY', True, fill)
        return rect_obj

    def draw_door_swing_icon(self, width, depth):
        door_n = 'ICON.CURVE.Door'
        swing_n = 'ICON.CURVE.Swing'
        door_crv = self.draw_rectangle(door_n, depth, width, 0, 0, True)
        swing_crv_pts = [(depth, width, 0),
                         (width * 0.9, width * 0.9, 0),
                         (width, 0, 0)]
        swing_crv = self.draw_curve(swing_n, swing_crv_pts, 'NURBS')
        return [door_crv, swing_crv]

    def pv_swing_door_icons(self, context, entry_door, wall):
        if 'Icons' not in bpy.data.groups:
            icons_grp = bpy.data.groups.new('Icons')
        else:
            icons_grp = bpy.data.groups['Icons']

        depth = unit.inch(2)
        wall_assy = fd_types.Assembly(wall)
        entry_assy = fd_types.Assembly(entry_door)
        entry_w = entry_assy.obj_x.location.x
        wall_d = wall_assy.obj_y.location.y
        pmt_rev = entry_assy.get_prompt('Reverse Swing')
        pmt_side = entry_assy.get_prompt('Door Swing')

        # Create the empty that will contain the icon shapes
        icon_obj_n = 'ICON.{}'.format(entry_door.mv.class_name)
        icon_obj = bpy.data.objects.new(icon_obj_n, None)
        icon_obj.empty_draw_size = unit.inch(1)
        icon_obj.empty_draw_type = 'SPHERE'
        icon_obj.mv.type = 'VISDIM_A'
        icon_obj.parent = entry_door
        context.scene.objects.link(icon_obj)
        sgl_entry = pmt_rev and pmt_side
        dbl_entry = pmt_rev and not pmt_side
        icon_crvs = []

        if dbl_entry:
            swing_rev = pmt_rev.value()
            icon_crvs = self.draw_door_swing_icon(entry_w * 0.5, depth)
            crvs_mirror = self.draw_door_swing_icon(entry_w * 0.5, depth)
            for c in crvs_mirror:
                self.flip_curve(c, 'X')
                self.move_curve(c, (entry_w, 0, 0))
                icon_crvs.append(c)
            if swing_rev:
                icon_obj.rotation_euler.x = math.radians(180)
            else:
                icon_obj.location.y = wall_d

        elif sgl_entry:
            swing_rev = pmt_rev.value()
            swing_side = pmt_side.value()[0]
            icon_crvs = self.draw_door_swing_icon(entry_w, depth)
            if swing_side == 'R' and swing_rev:
                icon_obj.location.x = entry_w
                icon_obj.rotation_euler.z = math.radians(180)

            elif swing_side == 'R' and not swing_rev:
                icon_obj.location.x = entry_w
                icon_obj.location.y = wall_d
                icon_obj.rotation_euler.y = math.radians(180)

            elif swing_side == 'L' and swing_rev:
                icon_obj.rotation_euler.x = math.radians(180)

            elif swing_side == 'L' and not swing_rev:
                icon_obj.location.y = wall_d

        for c in icon_crvs:
            msh = c.to_mesh(context.scene, False, 'PREVIEW')
            obj = bpy.data.objects.new(c.name, msh)
            obj.mv.type = 'CAGE'
            obj.parent = icon_obj
            context.scene.objects.link(obj)
            icons_grp.objects.link(obj)
            bpy.data.curves.remove(c.data, do_unlink=True)
            bpy.data.objects.remove(c, do_unlink=True)

    def link_dims_to_scene(self, scene, obj_bp):
        for child in obj_bp.children:
            if child not in self.ignore_obj_list:
                self.has_render_comment(child)
                if child.mv.type in ('VISDIM_A', 'VISDIM_B'):
                    scene.objects.link(child)
                if len(child.children) > 0:
                    self.link_dims_to_scene(scene, child)

    def has_render_comment(self, obj):
        if obj.mv.comment == "render":
            return True
        return False

    def get_hierarchy(self, obj):
        yield obj
        if len(obj.children) > 0:
            for c in obj.children:
                yield from self.get_hierarchy(c)

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

    def link_tagged_dims_to_scene(self, scene, obj_bp):
        for child in obj_bp.children:
            comment = self.has_render_comment(child)
            if 'hashmark' in child.name.lower():
                scene.objects.link(child)
            if child not in self.ignore_obj_list or comment:
                if child.mv.type == 'VISDIM_A':
                    obj_parent = child.parent
                    if 'hanging' not in obj_parent.name.lower():
                        scene.objects.link(child)
                if child.mv.type == 'VISDIM_B':
                    obj_grandpa = child.parent.parent
                    if 'hanging' not in obj_grandpa.name.lower():
                        scene.objects.link(child)
                if len(child.children) > 0:
                    self.link_tagged_dims_to_scene(scene, child)
            if 'LABEL' in child.name:
                scene.objects.link(child)
                
    def link_desired_dims_to_scene(self, scene, obj_bp):
        for child in obj_bp.children:
            comment = self.has_render_comment(child)
            if 'hashmark' in child.name.lower():
                scene.objects.link(child)
            if child not in self.ignore_obj_list or comment:
                if child.mv.type == 'VISDIM_A':
                    obj_parent = child.parent
                    if 'hanging' not in obj_parent.name.lower():
                        scene.objects.link(child)
                if child.mv.type == 'VISDIM_B':
                    obj_grandpa = child.parent.parent
                    if 'hanging' not in obj_grandpa.name.lower():
                        scene.objects.link(child)
                if len(child.children) > 0:
                    self.link_tagged_dims_to_scene(scene, child)
            if 'LABEL' in child.name:
                scene.objects.link(child)

    def link_custom_entities_to_scene(self, scene, obj_bp):
        for child in obj_bp.children:
            if 'PARTHGT' in child.name:
                if child.name not in scene.objects:
                    scene.objects.link(child)
            # if 'DBJWLR' in child.name:
            #     scene.objects.link(child)
            # if 'LOCK' in child.name:
            #     scene.objects.link(child)
            if len(child.children) > 0:
                self.link_custom_entities_to_scene(scene, child)

    def group_children(self, grp, obj):
        is_cage = obj.mv.type != 'CAGE'
        ignore = self.ignore_obj_list
        group_list = [item for item in grp.objects]
        not_empty_group = len(group_list) > 0
        if is_cage and obj not in ignore and not_empty_group and obj not in group_list:
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
                if (child.mv.type != 'CAGE' and obj not in self.ignore_obj_list
                    and child.name not in grp.objects):
                        grp.objects.link(child)
        return grp

    def add_children_to_ignore(self, obj):
        if obj not in self.ignore_obj_list:
            self.ignore_obj_list.append(obj)
        if (len(obj.children) > 0):
            for child in obj.children:
                if child not in self.ignore_obj_list:
                    self.add_children_to_ignore(child)

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

    def random_string(self, length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.sample(letters, length))
        return result_str

    def apply_build_height_label(self, context, wall_bp, 
                                 position, multiplier, wall_offset):
        offset = unit.inch(-7) + (unit.inch(-4) * multiplier)
        dim = fd_types.Dimension()
        dim.parent = wall_bp
        dim.start_x(value=offset + wall_offset)
        dim.start_y(value=offset + wall_offset)
        dim.start_z(value=0)
        dim.end_z(value=position)
        label = self.to_inch_lbl(position)
        dim.set_label(" ")
        bpy.ops.object.text_add()
        text = context.active_object
        text.parent = wall_bp
        text.rotation_euler.x = math.radians(0)
        text.rotation_euler.y = math.radians(-90)
        text.rotation_euler.z = math.radians(90)
        text.location.x = offset - unit.inch(1)
        text.location.y = 0
        text.location.z = ((position / 2))
        text.data.align_x = 'CENTER'
        text.data.size = .1
        text.data.body = label
        text.data.font = self.font

    def build_height_accordion_view(self, context, wall_bp, offset):
        build_height_dims_list = []
        for item in wall_bp.children:
            if 'hanging' in item.name.lower():
                build_height_dim = 0
                countertop_height = 0
                ctop_thickness = 0
                topshelf_thickness = 0
                hanging_height = fd_types.Assembly(item).obj_z.location.z
                for n_item in item.children:
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
                    build_height_dim = hanging_height
                elif ctop_thickness > 0:
                    build_height_dim = (countertop_height + ctop_thickness)
                elif topshelf_thickness > 0:
                    build_height_dim = (hanging_height + topshelf_thickness)
                build_height_dims_list.append(build_height_dim)
        build_height_dims_list = list(set(build_height_dims_list))
        build_height_dims_list = sorted(build_height_dims_list)
        for i, value in enumerate(build_height_dims_list):
            self.apply_build_height_label(context, wall_bp, value, i, offset)
        dims_offset = (unit.inch(-4) * len(build_height_dims_list))
        max_offset = unit.inch(-7) + dims_offset
        return max_offset

    def ceiling_height_accordion_view(self, context, item, 
                                 bheight_offset, dim_offset):
        dim = fd_types.Dimension()
        dim.parent = item.parent
        dim.start_x(value=unit.inch(-1) + bheight_offset + dim_offset)
        dim.start_y(value=unit.inch(-1) + bheight_offset + dim_offset)
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
        text.location.x = unit.inch(-2) + bheight_offset
        text.location.y = 0
        text.location.z = (item.dimensions[2] / 2)
        text.data.align_x = 'CENTER'
        text.data.size = .1
        text.data.body = wall_height
        text.data.font = self.font

    def wall_width_dimension_accordion_view(self, wall_bp):
        assembly = fd_types.Assembly(wall_bp)
        # has_entry = any('Entry' in c.mv.class_name for c in wall_bp.children)
        # if not has_entry:
        random_str = self.random_string(4)
        dim = fd_types.Dimension()
        dim.anchor.name = "WallDimAnchor_" + random_str
        dim.end_point.name = "WallDimEndPoint_" + random_str
        label = self.to_inch_lbl(assembly.obj_x.location.x)
        dim.parent(wall_bp)
        dim.start_y(value=assembly.obj_y.location.y)
        dim.start_z(value=assembly.obj_z.location.z + unit.inch(4))
        dim.end_x(value=assembly.obj_x.location.x)
        dim.set_label(label)
        return dim

    def max_object_width(self, measures):
        if len(measures) > 0:
            return max(measures, key=lambda tup: tup[0])
        return None

    def obj_at_min_loc_x(self, measures):
        return min(measures, key=lambda tup: tup[2])

    def create_acordion_scene(self, context, grp):
        bpy.ops.scene.new('INVOKE_DEFAULT', type='EMPTY')
        new_scene = context.scene
        new_scene.name = grp.name
        new_scene.mv.name_scene = grp.name
        new_scene.mv.elevation_img_name = grp.name
        new_scene.mv.plan_view_scene = False
        new_scene.mv.elevation_scene = True
        self.create_linesets(new_scene)

        return new_scene

    def divide_walls_to_acordions(self, walls, wall_break=330):
        walls_data = []
        wall_length_sum = 0
        for wall in walls:
            curr_wall_length = fd_types.Assembly(wall).obj_x.location.x
            wall_length_sum += self.to_inch(curr_wall_length)
            walls_data.append((self.to_inch(curr_wall_length), wall))
        acordions = []
        if wall_break >= wall_length_sum:
            acordions.append(walls)
        elif wall_break < wall_length_sum:
            current_break = wall_break
            division = []
            for wall in walls_data:
                wall_length, actual_wall = wall
                if wall_length <= current_break:
                    division.append(actual_wall)
                    current_break -= wall_length
                elif wall_length > current_break:
                    current_break = wall_break
                    acordions.append(division)
                    division = []
                    division.append(actual_wall)
                    current_break -= wall_length
            if len(division) > 0:
                acordions.append(division)
        return acordions

    def get_acordion_indexes(self, walls, acordions):
        indexed_acordions = []
        for acordion in acordions:
            indexed_acordion = []
            for item in acordion:
                index = walls.index(item)
                indexed_acordion.append(index)
            indexed_acordions.append(indexed_acordion)
        return indexed_acordions

    def corner_formation(self, context, cross_sections, 
                         strict_corner_objects, walls):
        # Check for colisions only if we have Corner Shelves or L-shelves
        cross_idx_exclusions = []
        if len(strict_corner_objects) > 0:
            first_wall = walls[1]
            last_wall = walls[-1]
            for corner, corner_obj in enumerate(strict_corner_objects):
                corner_pos, corner_orgn_wall, corner_tgt_wall, cn_parts, is_cross = corner_obj
                for cross, cs_section in enumerate(cross_sections):
                    cs_pos, cs_orgn_wall, cs_tgt_wall, cs_parts, is_cross = cs_section
                    if cs_pos == corner_pos and cs_tgt_wall == corner_tgt_wall:
                        cross_idx_exclusions.append(cross)
                    elif cs_tgt_wall == last_wall and corner_orgn_wall == first_wall:
                        cross_idx_exclusions.append(cross)
            cross_idx_exclusions = sorted(list(set(cross_idx_exclusions)))
            for corner in strict_corner_objects:
                cross_sections.append(corner)

        for i, cross_section in enumerate(cross_sections):
            if i in cross_idx_exclusions:
                continue
            position, origin_wall, target_wall, parts_list, is_cross = cross_section
            partitions = []
            inserts = []
            grp = bpy.data.groups.new("Joint_Grp")
            empty_obj_location = (0, 0, 0)
            empty_obj_rotation = (0, 0, math.radians(-90))
            target_wall_assy = fd_types.Assembly(target_wall)
            target_wall_width = target_wall_assy.obj_x.location.x
            # Colect parts objects into a group to add to joint object
            for part in parts_list:
                part_assy = fd_types.Assembly(part)
                partition_qry = 'partition' in part.name.lower()
                insert_qry = 'insert' in part.name.lower()
                if partition_qry:
                    partition_width = abs(part_assy.obj_y.location.y)
                    part_height = abs(part_assy.obj_x.location.x)
                    loc_x = part.location[0]
                    partition = (partition_width, part_height, loc_x, part)
                    partitions.append(partition)
                if insert_qry:
                    insert_width = abs(part_assy.obj_x.location.x)
                    insert_height = abs(part_assy.obj_y.location.y)
                    loc_x = part.location[0]
                    insert = (insert_width, insert_height, loc_x, part)
                    inserts.append(insert)
                self.group_children(grp, part)
                # self.add_children_to_ignore(part)
            # set the object target location based on origin cross section
            # positioning
            if position == "last":
                max_partition_width = self.max_object_width(partitions)[0]
                if max_partition_width is None:
                    continue
                empty_obj_location = (max_partition_width, 0, 0)
            elif position == "first" and not is_cross:
                for part in parts_list:
                    grp.objects.link(part)
                    for obj in part.children:
                        if obj.name not in grp.objects:
                            grp.objects.link(obj)
                empty_obj_location = (target_wall_width, 0, 0)
            elif position == "first" and is_cross:
                min_loc_x_obj = self.obj_at_min_loc_x(partitions)[3]
                min_loc_x_assy = fd_types.Assembly(min_loc_x_obj)
                partition_width = abs(min_loc_x_assy.obj_y.location.y)
                partition_height = abs(min_loc_x_assy.obj_x.location.x)
                empty_obj_location = (partition_width, 0, 0)
                dimensions = (partition_height,
                              partition_width,
                              unit.inch(0.75))
                # Add Occlusion only for
                # Cross Sections at last opening position
                largest_insert = self.max_object_width(inserts)
                if largest_insert is None:
                    continue
                oclusion_offset = largest_insert[0] + unit.inch(2)
                largest_insert_obj = largest_insert[3]
                location = (oclusion_offset,
                            (partition_width * -1),
                            (partition_height * -1)
                            )
                rotation = (0, math.radians(-90), 0)
                oclusion = self.add_oclusion_partition(
                    context, dimensions, location,
                    rotation, largest_insert_obj
                )
                self.group_children(grp, oclusion)
                # self.add_children_to_ignore(oclusion)
                empty_obj_location = (target_wall_width, 0, 0)
            for obj in grp.objects:
                if 'hashmark' in obj.name.lower():
                    grp.objects.unlink(obj)
            instance_name = "Joint " + str(i) + " Instance"
            instance = bpy.data.objects.new(instance_name, None)
            instance.dupli_type = 'GROUP'
            instance.dupli_group = grp
            instance.parent = target_wall
            instance.location = empty_obj_location
            instance.rotation_euler = empty_obj_rotation
            bpy.context.scene.objects.link(instance)

    def create_main_acordion_scene(self, context,
                                   mesh_data_dict, cross_sections):
        walls_length = 0
        walls_heights = []
        bpy.ops.scene.new('INVOKE_DEFAULT', type='LINK_OBJECT_DATA')
        new_scene = context.scene
        new_objects_dict = {}
        translated_cs_parts = []
        strict_corner_objects = []
        # Build the Dictionary of objects/meshes
        for obj in new_scene.objects:
            if obj.data is not None:
                new_objects_dict[obj.data.name] = obj
        new_scene_walls = [
            obj for obj in new_scene.objects if obj.mv.type == "BPWALL"]
        # Get corner/l-shelves
        for wall_idx, wall in enumerate(new_scene_walls):
            for child in wall.children:
                is_cross = False
                corner_shelves = 'corner shelves' in child.name.lower()
                l_shelves = 'l shelves' in child.name.lower()
                if corner_shelves or l_shelves:
                    corner_parts = []
                    corner_parts.append(child)
                    current_wall = new_scene_walls[wall_idx]
                    previous_wall = new_scene_walls[wall_idx-1]
                    strict_corner_objects.append(
                        ("first", current_wall, 
                         previous_wall, corner_parts, is_cross)
                    )
        for section in cross_sections:
            position, origin_wall, target_wall, parts_list = section
            is_cross = True
            trslt_parts_list = []
            origin_mesh = mesh_data_dict[origin_wall.name]
            trslt_origin_wall = new_objects_dict[origin_mesh]
            target_mesh = mesh_data_dict[target_wall.name]
            trslt_target_wall = new_objects_dict[target_mesh]
            for part in parts_list:
                if not hasattr(part, 'name'):
                    continue
                oclusion = 'oclusion' in part.name.lower()
                mesh = mesh_data_dict.get(part.name)
                if mesh is not None and not oclusion:
                    trslt_part = new_objects_dict[mesh]
                    trslt_parts_list.append(trslt_part)
            translated_section = (position,
                                  trslt_origin_wall,
                                  trslt_target_wall,
                                  trslt_parts_list,
                                  is_cross)
            translated_cs_parts.append(translated_section)
        self.corner_formation(context, translated_cs_parts,
                              strict_corner_objects, new_scene_walls)
        for obj in new_scene_walls:
            obj.rotation_euler.z = 0
            wall_assy = fd_types.Assembly(obj)
            walls_length += wall_assy.obj_x.location.x
            walls_heights.append(wall_assy.obj_z.location.z)
        new_scene.name = "Z_Main Accordion"
        new_scene.mv.name_scene = "Z_Main Accordion"
        new_scene.mv.elevation_img_name = "Z_Main Accordion"
        new_scene.mv.plan_view_scene = False
        new_scene.mv.elevation_scene = True
        self.create_linesets(new_scene)
        camera = self.create_camera(new_scene)
        camera.rotation_euler.x = math.radians(90.0)
        camera.rotation_euler.z = 0
        new_scene.mv.opengl_dim.gl_font_size = 18
        new_scene.render.pixel_aspect_x = 1.0
        new_scene.render.pixel_aspect_y = 1.0
        new_scene.render.resolution_x = 900
        new_scene.render.resolution_y = 450
        new_scene.render.resolution_percentage = 100
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.view3d.camera_to_view_selected()
        max_height = max(walls_heights)
        proportion = round((walls_length / max_height), 2)
        camera.data.ortho_scale += proportion
        bpy.ops.object.select_all(action='DESELECT')
        return new_scene

    def create_acordion_scenes(self, context, mesh_data_dict, cross_sections):
        acordion_counter = 1
        scene_objects = context.scene.objects
        walls = [
            obj for obj in scene_objects if obj.mv.type == "BPWALL"]
        acordions = self.divide_walls_to_acordions(walls, wall_break=330)
        indexes = self.get_acordion_indexes(walls, acordions)
        main_acordion_scene = self.create_main_acordion_scene(
            context, mesh_data_dict, cross_sections)
        new_scene_walls = [
            obj for obj in main_acordion_scene.objects if obj.mv.type == "BPWALL"]
        new_scene_walls_widths = []
        for new_wall in new_scene_walls:
            wall_assy = fd_types.Assembly(new_wall)
            width = wall_assy.obj_x.location.x
            new_scene_walls_widths.append(width)
        bpy.context.screen.scene = bpy.data.scenes['Z_Main Accordion']
        for i in range(len(acordions)):
            walls_length = 0
            walls_heights = []
            grp_name = "Accordion " + str(acordion_counter)
            grp = bpy.data.groups.new(grp_name)
            new_scene = self.create_acordion_scene(context, grp)
            for j, wall in enumerate(new_scene_walls):
                desired_indexes = indexes[i]
                wall.rotation_euler.z = 0
                if j in desired_indexes:
                    wall_assy = fd_types.Assembly(wall)
                    walls_length += wall_assy.obj_x.location.x
                    walls_heights.append(wall_assy.obj_z.location.z)
                    self.group_children(grp, wall)
                    for obj in grp.objects:
                        # CS Oclusion
                        hashmark = 'hashmark' in obj.name.lower()
                        cs_olcusion = 'cs oclusion' in obj.name.lower()
                        if hashmark or cs_olcusion:
                            grp.objects.unlink(obj)
                    # Remove wall width, height and build dimensions
                    for obj in wall.children:
                        dim_anchor = obj.mv.type == "VISDIM_A"
                        build_height = obj.type == 'FONT'
                        hashmark = 'hashmark' in obj.name.lower()
                        wall_mesh = 'mesh' in obj.name.lower()
                        if dim_anchor or build_height or hashmark:
                            bpy.data.objects.remove(obj, do_unlink=True)
                        if wall_mesh:
                            for n_obj in obj.children:
                                wall_height = n_obj.type == 'FONT'
                                if wall_height:
                                    bpy.data.objects.remove(n_obj,
                                                            do_unlink=True)
            instance_name = "Accordion Instance " + str(acordion_counter)
            instance = bpy.data.objects.new(instance_name, None)
            new_scene.objects.link(instance)
            instance.dupli_type = 'GROUP'
            instance.dupli_group = grp
            camera = self.create_camera(new_scene)
            camera.rotation_euler.x = math.radians(90.0)
            camera.rotation_euler.z = 0
            new_scene.mv.opengl_dim.gl_font_size = 16
            new_scene.render.pixel_aspect_x = 1.0
            new_scene.render.pixel_aspect_y = 1.0
            new_scene.render.resolution_x = 1800
            new_scene.render.resolution_y = 900
            new_scene.render.resolution_percentage = 100
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.view3d.camera_to_view_selected()
            max_height = max(walls_heights)
            proportion = round((walls_length / max_height), 2)
            camera.data.ortho_scale += proportion
            instance.hide_select = True
            bpy.ops.object.select_all(action='DESELECT')
            acordion_counter += 1
        bpy.context.screen.scene = bpy.data.scenes['_Main']

    def blind_corner_panel_labels(self, context, item):
        bcps = []
        opns = []

        for n_item in item.children:
            assy = fd_types.Assembly(n_item)
            hide = assy.get_prompt('Hide')
            is_bcp = n_item.lm_closets.is_blind_corner_panel_bp
            if is_bcp and hide and not hide.value():
                bcps.append(assy)
            elif n_item.mv.type_group == 'OPENING':
                opns.append(assy)

        for bcp in bcps:
            is_l_bcp = bcp.get_prompt('Is Left Blind Corner Panel')
            is_r_bcp = bcp.get_prompt('Is Right Blind Corner Panel')
            bcp_x = bcp.obj_bp.location[0]
            bcp_y = bcp.obj_bp.location[1]
            bcp_z = bcp.obj_bp.location[2]
            bcp_w = bcp.obj_y.location[1]
            bcp_h = bcp.obj_x.location[0]
            bcp_d = bcp.obj_z.location[2]

            bcp_str = '%s BCP' % self.to_inch_lbl(bcp_w)
            bcp_lbl_x = bcp_h * 0.55
            bcp_lbl_y = bcp_w * 0.5
            bcp_lbl_loc = (bcp_lbl_x, bcp_lbl_y, 0)
            bcp_lbl = fd_types.Dimension()
            bcp_lbl.set_label(bcp_str)
            self.copy_world_loc(bcp.obj_bp, bcp_lbl.anchor, bcp_lbl_loc)

            for opn in opns:
                opn_y = opn.obj_bp.location[1]
                opn_z = opn.obj_bp.location[2]
                opn_w = opn.obj_x.location[0]
                opn_h = opn.obj_z.location[2]
                opn_x = opn.obj_bp.location[0]

                match_x, match_y, match_z = False, False, False

                if is_l_bcp and is_l_bcp.value():
                    match_x = math.isclose(bcp_x + bcp_d, opn_x, abs_tol = 1e-3)
                    match_y = math.isclose(bcp_y + bcp_d, opn_y, abs_tol = 1e-3)
                    match_z = math.isclose(bcp_z + (bcp_h - opn_h) * 0.5,
                                           opn_z, abs_tol = 1e-3)

                elif is_r_bcp and is_r_bcp.value():
                    match_x = math.isclose(bcp_x, opn_x + opn_w + bcp_d, abs_tol = 1e-3)
                    match_y = math.isclose(bcp_y, opn_y, abs_tol = 1e-3)
                    match_z = math.isclose(bcp_z + (bcp_h - opn_h) * 0.5,
                                           opn_z, abs_tol = 1e-3)

                if match_x and match_y and match_z:
                    gap_w = opn_w - bcp_w
                    gap_str = '%s Open' % self.to_inch_lbl(gap_w + bcp_d)
                    gap_lbl_x = -unit.inch(3)
                    gap_lbl_y = opn_w - gap_w * 0.5
                    gap_lbl_loc = (gap_lbl_x, gap_lbl_y, 0)
                    gap_lbl = fd_types.Dimension()
                    gap_lbl.set_label(gap_str)
                    self.copy_world_loc(bcp.obj_bp, gap_lbl.anchor, gap_lbl_loc)

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

    # def flat_crown(self, context, item):
    #     wall = fd_types.Assembly(item.parent)
    #     assy = fd_types.Assembly(item)
    #     hang_h = assy.obj_z.location.z
    #     tkd_vo = assy.get_prompt('Top KD 1 Vertical Offset')
    #     labels = []
    #     tkh_str = ''
    #     for p in item.children:
    #         if p.lm_closets.is_flat_crown_bp and p.mv.type_group == 'INSERT':
    #             fc_prod = fd_types.Assembly(p)
    #             ext_ceil = fc_prod.get_prompt('Extend To Ceiling')
    #             tkh = fc_prod.get_prompt('Top KD Holes Down')
    #             if ext_ceil and ext_ceil.value() and tkh and tkd_vo:
    #                 if tkh.value() == 'One':
    #                     tkh_str = 'Top KD|Down 1 Hole'
    #                 elif tkh.value() == 'Two':
    #                     tkh_str = 'Top KD|Down 2 Holes'
    #                 hang_h -= tkd_vo.value()
    #             for a in p.children:
    #                 if a.mv.type == 'BPASSEMBLY' and 'Flat Crown' in a.name:
    #                     fc_assy = fd_types.Assembly(a)
    #                     fc_h = fc_assy.obj_y.location.y
    #                     fc_str = 'Flat Crown %s' % self.to_inch_lbl(fc_h)
    #                     labels.append((fc_str, fc_h))

    #     labels = list(dict.fromkeys(labels))
    #     if tkh_str:
    #         labels.append((tkh_str, -unit.inch(3)))

    #     for l in labels:
    #         lbl = fd_types.Dimension()
    #         lbl.set_label(l[0])
    #         lbl_y = hang_h + (l[1] * 0.5)
    #         self.copy_world_loc(wall.obj_bp, lbl.anchor, (-0.5, 0, lbl_y))

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

    def apply_l_shelves_tag(self, wall_assembly, context, assembly, l_shelf):
        door_type = None
        tags = []
        text_height = .1
        text_rotation = math.radians(0)
        wall_assembly_bp = fd_types.Assembly(wall_assembly.obj_bp)
        wall_angle = round(math.degrees(
            wall_assembly_bp.obj_bp.rotation_euler[2]))
        if len(assembly.prompts) > 0:
            shelves_qty = assembly.get_prompt("Shelf Quantity").value()
            # Add the bottom shelf to the calculation if has shelves
            if shelves_qty > 0:
                shelves_qty += 1
            tags.append(("L-Shelf", 0.0))
            shelves_tag = str(shelves_qty) + ' Shlvs.'
            tags.append((shelves_tag, 0.0))
            has_door = assembly.get_prompt("Door").value()
            pos_x = assembly.obj_x.location.x
            pos_y = assembly.obj_y.location.y
            parent_height = l_shelf.location[2]
            if has_door:
                door_type = assembly.get_prompt("Door Type").value()
                door_tag = door_type + ' Doors'
                tags.append((door_tag, 0.0))
            if wall_angle == 180:
                text_rotation = math.radians(180)
                tags.reverse()
            for index, tag in enumerate(tags):
                loc_y = ((index + 1) * (pos_y / (len(tags) + 1)))
                bpy.ops.object.text_add()
                text = context.active_object
                text.parent = l_shelf
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

    def apply_corner_shelves_tag(self, wall_assembly, context, assembly, corner_shelf):
        double_doors = None
        tags = []
        text_height = .1
        text_rotation = math.radians(0)
        wall_assembly_bp = fd_types.Assembly(wall_assembly.obj_bp)
        wall_angle = round(math.degrees(
            wall_assembly_bp.obj_bp.rotation_euler[2]))
        if len(assembly.prompts) > 0:
            shelves_qty = assembly.get_prompt("Shelf Quantity").value()
            # Add the bottom shelf to the calculation if has shelves
            if shelves_qty > 0:
                shelves_qty += 1
            tags.append(("Corner Shelf", 0.0))
            shelves_tag = str(shelves_qty) + ' Shlvs.'
            tags.append((shelves_tag, 0.0))
            has_door = assembly.get_prompt("Door").value()
            pos_x = assembly.obj_x.location.x
            pos_y = assembly.obj_y.location.y
            parent_height = corner_shelf.location[2]
            if has_door:
                door_tag = "1 Door"
                double_doors = assembly.get_prompt("Force Double Doors").value()
                if double_doors is not None:
                    door_tag = "Dbl. Doors"
                tags.append((door_tag, 0.0))
            if wall_angle == 180:
                text_rotation = math.radians(180)
                tags.reverse()
            for index, tag in enumerate(tags):
                loc_y = ((index + 1) * (pos_y / (len(tags) + 1)))
                bpy.ops.object.text_add()
                text = context.active_object
                text.parent = corner_shelf
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
        shelf_count = 0
        assemblies = [
            item for item in assembly.children if item.lm_closets.is_shelf_bp]
        for a in assemblies:
            for c in a.children:
                if c.cabinetlib.type_mesh == 'CUTPART' and not c.hide:
                    shelf_count +=1
        return (shelf_count)

    def get_door_count(self, assembly):
        door_count = 0
        for obj in assembly.children:
            if obj.lm_closets.is_door_bp:
                for o in obj.children:
                    if ((o.cabinetlib.type_mesh == 'CUTPART' or
                         o.cabinetlib.type_mesh == 'BUYOUT') and not o.hide):
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
            if 'corner shelves' in item.name.lower():
                corner_assy = fd_types.Assembly(item)
                self.apply_corner_shelves_tag(
                    wall_assembly, context, corner_assy, item)
            if 'l shelves' in item.name.lower():
                l_shelf_assy = fd_types.Assembly(item)
                self.apply_l_shelves_tag(
                    wall_assembly, context, l_shelf_assy, item)
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

    def draw_hashmark(self, length, axis, line_width=2):
        # Use opengl_dims to create hashmarks
        hashmark = fd_types.Dimension(True)
        hashmark.opengl_dim.gl_width = line_width
        hashmark.anchor.name = 'Hashmark'
        hashmark.end_point.location = [length * (a == axis) for a in self.axes]
        return hashmark.anchor

    def plan_view_hashmarks(self, context, obj):
        wall_mesh = [i for i in obj.children if i.mv.is_wall_mesh][0]
        width = wall_mesh.dimensions.x
        depth = wall_mesh.dimensions.y
        height = wall_mesh.dimensions.z
        wall_angle = round(obj.rotation_euler.z, 4)

        length = unit.inch(9)
        off = unit.inch(1)
        location = (width, depth, height)
        rotation = (0, 0, 45)

        custom_room = context.scene.fd_roombuilder.room_type == 'CUSTOM'
        single_room = context.scene.fd_roombuilder.room_type == 'SINGLE'

        if single_room:
            self.pv_pad += length * 2

        elif custom_room:
            if wall_angle == round(math.radians(-90), 4):  # ok
                off = unit.inch(5)
            elif wall_angle == round(math.radians(180), 4):  # ok
                off = unit.inch(6)
            self.pv_pad += length * 0.25

        else:
            location = (width - depth, depth, height)
            if wall_angle == round(math.radians(-90), 4):
                off = unit.inch(5)
            elif wall_angle == round(math.radians(180), 4):
                off = unit.inch(5)

        hashmark = self.draw_hashmark(length, 'X')
        self.copy_world_loc(obj, hashmark, location)
        self.copy_world_rot(obj, hashmark, rotation)

        label = self.to_inch_lbl(height, prec = 0)
        label_offset = length + off
        text = fd_types.Dimension()
        text.parent(hashmark)
        text.set_label(label)
        text.start_x(value = label_offset)
        hashmark.mv.opengl_dim.hide = True
        if len(hashmark.children) > 0:
            hashmark.children[1].mv.opengl_dim.hide = True

        return hashmark, height

    def return_wall_labels(self, entry_wall, entry_door, elv=False):
        wall_assy = fd_types.Assembly(entry_wall)
        door_assy = fd_types.Assembly(entry_door)

        wall_a = wall_assy.obj_x
        door_a = door_assy.obj_x
        door_b = door_assy.obj_bp
        wall_b = wall_assy.obj_bp
        door_h = door_assy.obj_z

        dims_pts = [[wall_a, door_a], [door_a, door_b], [door_b, wall_b]]

        py, pz = 0, 0

        if elv:
            dh_dim = fd_types.Dimension()
            dh_dim_loc = (door_a.location.x - unit.inch(10), 0, 0)
            self.copy_world_loc(door_h, dh_dim.anchor, dh_dim_loc)
            self.copy_world_loc(door_b, dh_dim.end_point, dh_dim_loc)
            dh_dim.set_label(self.to_inch_lbl(
                abs(dh_dim.end_point.location.z)))
            dh_dim.opengl_dim.gl_text_x = 55

            [d.reverse() for d in dims_pts]
            pz = wall_assy.obj_z.location.z + unit.inch(4)

        else:
            py = wall_assy.obj_y.location.y + unit.inch(14)

        for d in dims_pts:
            dim = fd_types.Dimension()
            dim_loc = (0, py, pz)
            self.copy_world_loc(d[0], dim.anchor, dim_loc)
            self.copy_world_loc(d[1], dim.end_point, dim_loc)
            dim.set_label(self.to_inch_lbl(abs(dim.end_point.location.x)))
            self.ignore_obj_list.append(dim.anchor)
            self.ignore_obj_list.append(dim.end_point)

    def create_plan_view_scene(self, context):
        bpy.ops.scene.new('INVOKE_DEFAULT', type='EMPTY')
        pv_scene = context.scene
        pv_scene.name = "Plan View"
        pv_scene.mv.name_scene = "Plan View"
        pv_scene.mv.plan_view_scene = True
        self.create_linesets(pv_scene)
        hashmark_heights = {}
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
                entry_wall_pv = None
                has_entry = any('Door Frame' in e.name for c in obj.children
                                for e in c.children)
                pv_scene.objects.link(obj)
                # Only link all of the wall meshes

                hashmark, height = self.plan_view_hashmarks(context, obj)
                hashmark_heights[hashmark.name] = round(height, 2)

                for child in obj.children:
                    if child.mv.is_wall_mesh:
                        if has_entry:
                            entry_wall_pv = child.copy()
                            entry_wall_pv.data = child.data.copy()
                            entry_wall_pv.name = 'Entry Wall PV'
                            entry_wall_pv.mv.is_wall_mesh = False
                            entry_wall_pv.mv.type = 'CAGE'
                            pv_scene.objects.link(entry_wall_pv)
                            grp.objects.link(entry_wall_pv)
                        else:
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
                            if has_entry and entry_wall_pv:
                                self.return_wall_labels(wall.obj_bp, obj_bp)
                                # Create a break in return wall at entry location
                                bool_mod_nm = 'MESH.Door Frame.Bool Obj'
                                bool_mod = entry_wall_pv.modifiers.get(
                                    bool_mod_nm)
                                bool_mod.object = assembly_mesh
                                bool_grow = unit.inch(0.125)
                                grow_x = assembly_mesh.dimensions.x
                                grow_y = wall.obj_y.location.y + \
                                    (bool_grow * 2)
                                grow_z = wall.obj_z.location.z + \
                                    (bool_grow * 2)
                                assembly_mesh.location.y -= bool_grow
                                assembly_mesh.location.z -= bool_grow
                                assembly_mesh.dimensions = (
                                    grow_x, grow_y, grow_z)
                                assembly_mesh.hide = True
                                assembly_mesh.hide_render = True

                                # Add icons for entry doors
                                entry_class = obj_bp.mv.class_name
                                entry_sgl = 'PRODUCT_Entry_Door_Double_Panel'
                                entry_dbl = 'PRODUCT_Entry_Double_Door_Double_Panel'
                                swing_door = ((entry_class == entry_sgl) or
                                              (entry_class == entry_dbl))
                                if swing_door:
                                    self.pv_swing_door_icons(
                                        context, obj_bp, wall.obj_bp)

                    if wall and wall.get_wall_mesh():
                        wall.get_wall_mesh().select = True

        show_all_hashmarks = False
        first_hashmark_entry = list(sorted(hashmark_heights.keys()))[:1]
        if len(first_hashmark_entry) > 0:
            first_hashmark_str = list(sorted(hashmark_heights.keys()))[:1][0]
            first_hashmark = bpy.data.objects[str(first_hashmark_str)]
            first_hashmark.mv.opengl_dim.hide = False
            if len(first_hashmark.children) > 0:
                first_hashmark.children[1].mv.opengl_dim.hide = False

        hashmark_heights_mode = self.list_mode(list(hashmark_heights.values()))

        for key, value in hashmark_heights.items():
            if value != hashmark_heights_mode:
                show_all_hashmarks = True

        for item in hashmark_heights:
            if item in bpy.data.objects and not show_all_hashmarks:
                hashmark = bpy.data.objects[str(item)]
                if hashmark.mv.opengl_dim.hide:
                    hsh_objs = [obj for obj in self.get_hierarchy(hashmark)]
                    for h in hsh_objs:
                        bpy.data.objects.remove(h, do_unlink=True)
            elif show_all_hashmarks:
                hashmark = bpy.data.objects[str(item)]
                hashmark.mv.opengl_dim.hide = False
                if len(hashmark.children) > 0:
                    hashmark.children[1].mv.opengl_dim.hide = False

        if custom_room and show_all_hashmarks:
            hashmarks_dict = {}
            counter = 0
            hashmarks = list(sorted(hashmark_heights.keys()))
            for item in hashmarks:
                hashmark = bpy.data.objects[str(item)]
                if not hashmark.mv.opengl_dim.hide and item in bpy.data.objects:
                    wall = fd_types.Assembly(hashmark.parent)
                    hashmarks_dict[counter] = {
                        "hashmark": hashmark.name,
                        "rotation": round(math.degrees(
                            hashmark.parent.rotation_euler[2])),
                        "wall_depth": wall.obj_y.location.y
                    }
                    counter += 1
            for i in range(len(hashmarks_dict)):
                turn_angle = 0
                if i + 1 in hashmarks_dict.keys():
                    hashmark = bpy.data.objects[hashmarks_dict[i]["hashmark"]]
                    current_angle = hashmarks_dict[i]["rotation"]
                    next_one_angle = hashmarks_dict[i + 1]["rotation"]
                    turn_angle = current_angle - next_one_angle
                    wall_depth = hashmarks_dict[i]["wall_depth"]
                    dim_offset = wall_depth
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
        cam_ortho = camera.data.ortho_scale
        pv_font_size = -24.8 * math.log(0.04 * cam_ortho)
        pv_scene.mv.opengl_dim.gl_font_size = pv_font_size

    def process_connected_walls(self, context, walls):
        joints = []
        first_wall = [wall[0] for wall in walls][0]
        last_wall = [wall[0] for wall in walls][-1]
        # Getting wall connections
        connected_walls = [[wall for wall in group if wall is not None]
                           for group in walls]
        [connected_walls.remove(conn)
         for conn in connected_walls if len(conn) == 1]
        for conn in connected_walls:
            curr_wall_asmbly = []
            prvs_wall_asmbly = []
            for obj in conn[0].obj_bp.children:
                product = 'product' in obj.name.lower()
                hanging = 'hanging' in obj.name.lower()
                if product and hanging:
                    curr_wall_asmbly.append(obj)
            for obj in conn[1].obj_bp.children:
                product = 'product' in obj.name.lower()
                hanging = 'hanging' in obj.name.lower()
                if product and hanging:
                    prvs_wall_asmbly.append(obj)
            current_wall = round(math.degrees(
                conn[0].obj_bp.rotation_euler[2]))
            previous_wall = round(math.degrees(
                conn[1].obj_bp.rotation_euler[2]))
            cnctd_wall_angle_check = (
                previous_wall - current_wall) in [90, -270]
            # To know if a corner is a right angle the subtraction between
            # the previous and the current wall need to be 90 or -270 degrees
            if cnctd_wall_angle_check:
                joints.append((conn[0].obj_bp, conn[1].obj_bp))
        joints.append((first_wall.obj_bp, last_wall.obj_bp))
        joints.append((last_wall.obj_bp, first_wall.obj_bp))
        return joints

    def unlink_cleats(self, context):
        # ungrouping objects we do not want to be rendered.
        for obj in bpy.data.objects:
            cutpart = 'cutpart' in obj.name.lower()
            cleat = 'cleat' in obj.name.lower()
            if cleat and cutpart:
                obj.select = True
                bpy.ops.group.objects_remove_all()


    def add_oclusion_partition(self, context, dimensions,
                               location, rotation, parent):
        oclusion_name = "CS Oclusion"
        oclusion_mesh = utils.create_cube_mesh(oclusion_name, dimensions)
        oclusion_mesh.parent = parent
        oclusion_mesh.location = location
        oclusion_mesh.rotation_euler = rotation
        oclusion_mesh.mv.type = 'OBSTACLE'
        oclusion_mesh.mv.comment = "render"
        return oclusion_mesh

    def add_oclusion_partitions(self, context, partitions,
                                position, grp, largest_opening):
        oclusions = []
        previous_scene = context.scene.name
        oclusion_scene = grp.name
        active_children = [
            [ch for ch in part.children if not ch.hide] for part in partitions]
        if len(active_children) > 0:
            active_children = (*active_children,)[0]
            for child in active_children:
                bpy.context.screen.scene = bpy.data.scenes[oclusion_scene]
                partition_width = child.dimensions[1]
                oclusion_z_location = largest_opening
                oclusion_dimensions = child.dimensions
                oclusion_location = (0, 0, 0)
                if position == "first":
                    oclusion_location = (
                        0, (partition_width * -1), (oclusion_z_location * -1))
                elif position == "last":
                    oclusion_location = (
                        0, (partition_width * -1), oclusion_z_location)
                oclusion_name = "Oclusion"
                oclusion_mesh = utils.create_cube_mesh(oclusion_name,
                                                       oclusion_dimensions)
                oclusion_mesh.parent = child
                oclusion_mesh.location = oclusion_location
                oclusion_mesh.rotation_euler = child.rotation_euler
                oclusion_mesh.mv.type = 'OBSTACLE'
                oclusions.append(oclusion_mesh)
                self.group_children(grp, oclusion_mesh)
                self.add_children_to_ignore(oclusion_mesh)
        bpy.context.screen.scene = bpy.data.scenes[previous_scene]
        return oclusions

    def add_cross_sections_items_to_group(self, context, item,
                                          grp, position, location, wall_width):
        openings = item["openings"]
        topshelves = item["topshelves"]
        partitions = item["partitions"]
        openings_widths = []
        for opening in openings:
            opng_assy_width = fd_types.Assembly(opening).obj_x.location.x
            openings_widths.append(opng_assy_width)
        if len(openings_widths) > 0:
            largest_opening = max(openings_widths)
            largest_opening = largest_opening * 1.1
            if len(openings) > 0:
                for op in openings:
                    self.group_children(grp, op)
                    self.add_children_to_ignore(op)
            if len(topshelves) > 0:
                for ts in topshelves:
                    self.group_children(grp, ts)
                    self.add_children_to_ignore(ts)
            if len(partitions) > 0:
                for part in partitions:
                    self.group_children(grp, part)
                    self.add_children_to_ignore(part)
            oclusions = self.add_oclusion_partitions(
                context, partitions, position, grp, largest_opening)
            return oclusions
        return None

    def key_with_max_value(self, d):
        v = list(d.values())
        k = list(d.keys())
        return k[v.index(max(v))]

    def key_with_min_value(self, d):
        v = list(d.values())
        k = list(d.keys())
        return k[v.index(min(v))]

    def cross_section_second_pass(self, context, grp,
                                  obj, position, location, inclusions_dict):
        oclusions = []
        wall_width = fd_types.Assembly(obj).obj_x.location.x
        helper_dict = {}
        for key, item in inclusions_dict.items():
            if position == "first":
                helper_dict[key] = item["start"]
            elif position == "last":
                helper_dict[key] = item["end"]
        measure_set = len(set(list(helper_dict.values())))
        if measure_set <= 1:
            for key, item in inclusions_dict.items():
                oclusion = self.add_cross_sections_items_to_group(context,
                                                                  item,
                                                                  grp,
                                                                  position,
                                                                  location,
                                                                  wall_width)
                oclusions.append(oclusion)
        if measure_set > 1:
            desired_keys = []
            if position == "last":
                max_key = self.key_with_max_value(helper_dict)
                desired_keys.append(max_key)
            elif position == "first":
                min_key = self.key_with_min_value(helper_dict)
                desired_keys.append(min_key)
            for key, item in inclusions_dict.items():
                if key in desired_keys:
                    oclusion = self.add_cross_sections_items_to_group(context,
                                                                      item,
                                                                      grp,
                                                                      position,
                                                                      location,
                                                                      wall_width)
                    oclusions.append(oclusion)
        return oclusions

    def filter_join_and_add_to_group(self, context, grp,
                                     obj, position, location):
        inclusions_dict = {}
        inclusions_list = []
        for c in obj.children:
            insert_matches = []
            insert_matches_with_pos = []
            topshelves = []
            product = 'product' in c.name.lower()
            hanging = 'hanging' in c.name.lower()
            if product and hanging:
                hang_opng_assy = fd_types.Assembly(c)
                hang_opng_width = hang_opng_assy.obj_x.location.x
                partitions_dict = {}
                inclusions_dict[c] = {}
                inclusions_dict[c]["openings"] = []
                inclusions_dict[c]["partitions"] = []
                inclusions_dict[c]["topshelves"] = []
                inclusions_dict[c]["start"] = self.to_inch(c.location[0])
                inclusions_dict[c]["end"] = self.to_inch(
                    (c.location[0] + hang_opng_width))
                for partition in c.children:
                    if 'partition' in partition.name.lower():
                        part_pos = self.to_inch(partition.location[0])
                        partitions_dict[partition] = part_pos
                for cc in c.children:
                    if 'OPENING' in cc.name:
                        opng_loc = self.to_inch(cc.location[0])
                        result = self.find_matching_inserts(context,
                                                            c,
                                                            opng_loc)
                        for res in result:
                            insert_matches_with_pos.append((opng_loc, res))
                    if 'partition' in cc.name.lower():
                        item_location = self.to_inch(cc.location[0])
                        if item_location == location:
                            inclusions_dict[c]["partitions"].append(cc)
                    if 'top' and 'shelf' in cc.name.lower():
                        topshelves.append(cc)
                        item_location = self.to_inch(cc.location[0])
                        if item_location == location:
                            inclusions_dict[c]["topshelves"].append(cc)
                srtd = sorted(insert_matches_with_pos, key=lambda tup: tup[0])
                insert_matches = [item[1] for item in srtd]
                if position == "first":
                    len_part_dict = len(partitions_dict) > 0
                    included_parts = len(inclusions_dict[c]["partitions"]) == 0
                    if len_part_dict and included_parts:
                        part = self.key_with_min_value(partitions_dict)
                        inclusions_dict[c]["partitions"].append(part)
                    if len(insert_matches) > 0:
                        inclusions_dict[c]["openings"].append(
                            insert_matches[:1][0])
                    for incl in inclusions_dict[c]["openings"]:
                        if incl.parent in insert_matches:
                            inclusions_dict[c]["openings"].append(incl.parent)
                            for ch in incl.children:
                                if ch in insert_matches and ch not in inclusions_dict[c]["openings"]:
                                    inclusions_dict[c]["openings"].append(ch)
                    if len(inclusions_dict[c]["topshelves"]) == 0:
                        inclusions_dict[c]["topshelves"].append(
                            topshelves[-1:][0])
                    continue
                if position == "last":
                    len_part_dict = len(partitions_dict) > 0
                    included_parts = len(inclusions_dict[c]["partitions"]) == 0
                    if len_part_dict and included_parts:
                        part = self.key_with_max_value(partitions_dict)
                        inclusions_dict[c]["partitions"].append(part)
                    if len(insert_matches) > 0:
                        inclusions_dict[c]["openings"].append(
                            insert_matches[-1:][0])
                    for incl in inclusions_dict[c]["openings"]:
                        if incl.parent in insert_matches:
                            inclusions_dict[c]["openings"].append(incl.parent)
                            for ch in incl.children:
                                if ch in insert_matches and ch not in inclusions_dict[c]["openings"]:
                                    inclusions_dict[c]["openings"].append(ch)
                    if len(inclusions_dict[c]["topshelves"]) == 0:
                        inclusions_dict[c]["topshelves"].append(
                            topshelves[-1:][0])
                    continue
        oclusions = self.cross_section_second_pass(context,
                                                   grp,
                                                   obj,
                                                   position,
                                                   location,
                                                   inclusions_dict)
        unpacked_oclusions = spread(oclusions)
        for unpacked in unpacked_oclusions:
            inclusions_list.append(unpacked)
        for item in inclusions_dict.values():
            inclusions_list.append(item["partitions"])
            inclusions_list.append(item["openings"])
            inclusions_list.append(item["topshelves"])
        inclusions_list = spread(inclusions_list)
        return inclusions_list

    def add_wall_joints_to_grp(self, context, group_dict, joints):
        aditions = []
        for joint in joints:
            # Every joint is a tuple, a pair of walls forming a... joint.
            # Wall "A"
            a = joint[0]
            a_assy_widths = []
            a_assy_depths = []
            a_wall_assy = fd_types.Assembly(a)
            a_wall_width = self.to_inch(a_wall_assy.obj_x.location.x)
            # Wall B
            b = joint[1]
            b_assy_widths = []
            b_assy_depths = []
            b_wall_assy = fd_types.Assembly(b)
            b_wall_width = self.to_inch(b_wall_assy.obj_x.location.x)
            for obj in a.children:
                product = 'product' in obj.name.lower()
                hanging = 'hanging' in obj.name.lower()
                if product and hanging:
                    hang_opng_assy = fd_types.Assembly(obj)
                    hang_opng_depth = abs(hang_opng_assy.obj_y.location.y)
                    a_assy_depths.append(self.to_inch(hang_opng_depth))
                    for child in obj.children:
                        partition = 'partition' in child.name.lower()
                        if partition:
                            part_width = abs(child.location[0])
                            hanging_width = abs(child.parent.location[0])
                            width = self.to_inch(part_width + hanging_width)
                            a_assy_widths.append(width)
            a_assy_widths = list(set(a_assy_widths))
            a_assy_depths = list(set(a_assy_depths))
            for obj in b.children:
                product = 'product' in obj.name.lower()
                hanging = 'hanging' in obj.name.lower()
                if product and hanging:
                    hang_opng_assy = fd_types.Assembly(obj)
                    hang_opng_depth = abs(hang_opng_assy.obj_y.location.y)
                    b_assy_depths.append(self.to_inch(hang_opng_depth))
                    for child in obj.children:
                        partition = 'partition' in child.name.lower()
                        if partition:
                            part_width = abs(child.location[0])
                            hanging_width = abs(child.parent.location[0])
                            width = self.to_inch(part_width + hanging_width)
                            b_assy_widths.append(width)
            if len(a_assy_widths) == 0 and len(b_assy_widths) == 0:
                continue
            elif len(b_assy_widths) > 0 and len(a_assy_widths) == 0:
                wall_group = group_dict.get(a.name)
                if wall_group is not None:
                    position = "last"
                    added = self.filter_join_and_add_to_group(
                        context,
                        wall_group, b, position, max(b_assy_widths))
                    aditions.append((position, b, a, added))
                continue
            elif len(a_assy_widths) > 0 and len(b_assy_widths) == 0:
                wall_group = group_dict.get(b.name)
                if wall_group is not None:
                    position = "first"
                    added = self.filter_join_and_add_to_group(
                        context,
                        wall_group, a, position, min(a_assy_widths))
                    aditions.append((position, a, b, added))
                continue
            b_assy_widths = list(set(b_assy_widths))
            b_assy_depths = list(set(b_assy_depths))
            # Check available slots on wall joint
            a_left = min(a_assy_widths) >= max(b_assy_depths)
            b_left = min(b_assy_widths) >= max(a_assy_depths)
            a_right = (a_wall_width - max(a_assy_widths)
                       ) >= max(b_assy_depths)
            b_right = (b_wall_width - max(b_assy_widths)
                       ) >= max(a_assy_depths)
            if (a_left and not b_right):
                # Last B on A
                position = "last"
                added = self.filter_join_and_add_to_group(
                    context,
                    group_dict[a.name], b, position, max(b_assy_widths))
                aditions.append((position, b, a, added))
                continue
            if (a_right and not b_left):
                # First B on A
                position = "first"
                added = self.filter_join_and_add_to_group(
                    context,
                    group_dict[a.name], b, position, min(b_assy_widths))
                aditions.append((position, b, a, added))
                continue
            if (b_right and not a_left):
                # First A on B
                position = "first"
                added = self.filter_join_and_add_to_group(
                    context,
                    group_dict[b.name], a, position, min(a_assy_widths))
                aditions.append((position, a, b, added))
                continue
        return aditions

    def create_elv_view_scene(self, context, assembly):
        if assembly.obj_bp and assembly.obj_x and assembly.obj_y and assembly.obj_z:
            grp = bpy.data.groups.new(assembly.obj_bp.mv.name_object)
            floor_obj = bpy.data.objects['Floor']
            grp.objects.link(floor_obj)
            new_scene = self.create_new_scene(context, grp, assembly.obj_bp)

            self.group_children(grp, assembly.obj_bp)
            # wall_mesh = utils.create_cube_mesh(assembly.obj_bp.mv.name_object,
            #                                    (assembly.obj_x.location.x,
            #                                     assembly.obj_y.location.y,
            #                                     assembly.obj_z.location.z))

            # wall_mesh.parent = assembly.obj_bp
            # grp.objects.link(wall_mesh)

            instance = bpy.data.objects.new(
                assembly.obj_bp.mv.name_object + " " + "Instance", None)
            new_scene.objects.link(instance)
            instance.dupli_type = 'GROUP'
            instance.dupli_group = grp

            # Getting blender object labels into group
            lbls_grp = bpy.data.groups.new('{} Labels grp'.format(assembly.obj_bp.mv.name_object))
            lbl_objs = [obj for obj in self.get_hierarchy(assembly.obj_bp)
                        if obj.type == 'FONT' or obj.type == 'CURVE']
            for l in lbl_objs:
                if grp in l.users_group:
                    grp.objects.unlink(l)
                lbls_grp.objects.link(l)

            lbls_instance = bpy.data.objects.new('{} Labels'.format(assembly.obj_bp.mv.name_object), None)
            new_scene.objects.link(lbls_instance)
            lbls_instance.dupli_type = 'GROUP'
            lbls_instance.dupli_group = lbls_grp
            lbls_instance.hide_select = True

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

                if any('Door Frame' in c.name for c in item.children):
                    self.return_wall_labels(assembly.obj_bp, item, True)

                if item.mv.type == 'VISDIM_A':
                    self.ignore_obj_list.append(item)

            self.add_text(context, assembly)
            self.link_tagged_dims_to_scene(new_scene, assembly.obj_bp)
            self.link_custom_entities_to_scene(new_scene, assembly.obj_bp)

            # for item in assembly.obj_bp.children:
            #     # Hanging Opening Item Level.
            #     if item.mv.type == "BPASSEMBLY":                    
            #         self.flat_crown(context, item)

            camera = self.create_camera(new_scene)
            camera.rotation_euler.x = math.radians(90.0)
            camera.rotation_euler.z = assembly.obj_bp.rotation_euler.z
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.view3d.camera_to_view_selected()
            camera.data.ortho_scale += self.ev_pad
            new_scene.mv.opengl_dim.gl_font_size = 22
            instance.hide_select = True
            bpy.ops.object.select_all(action='DESELECT')

            return grp

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
        blo = bpy.data.objects
        e_bp = []
        e_msh = []

        # Find top and bottom KD shelves by looking for expression in drivers
        # used to remove top or bottom shelves
        shelves = [obj for obj in blo if obj.lm_closets.is_shelf_bp]
        for s in shelves:
            s_assy = fd_types.Assembly(s)
            s_p = s.parent
            lck_shf_pmt = s_assy.get_prompt('Is Locked Shelf')
            lck_shf = ''
            if lck_shf_pmt:
                lck_shf = lck_shf_pmt.value()
            top_bot_kd = False

            # Check parent assembly
            in_drawer = False
            if s_p is not None:
                in_drawer = s_p.lm_closets.is_drawer_stack_bp

            for d in s.animation_data.drivers:
                exp = d.driver.expression
                rem_top_str = 'Remove_Top_Shelf'
                rem_bot_str = 'Remove_Bottom_Shelf'
                rem_bot_hang_str = 'Remove_Bottom_Hanging_Shelf'
                top_kd_str = 'Top_KD'
                bot_kd_str = 'Bottom_KD'
                if (rem_top_str in exp or rem_bot_str in exp or
                        top_kd_str in exp or bot_kd_str in exp or rem_bot_hang_str):
                    top_bot_kd = True

            # Find top or bottom KDs
            if (lck_shf and (top_bot_kd or in_drawer)):
                e_bp.append(s)

        # Find vertical panels
        e_bp.extend([obj for obj in blo if obj.lm_closets.is_panel_bp or
                     obj.lm_closets.is_blind_corner_panel_bp])

        # Find drawer structures
        e_bp.extend([obj for obj in blo if obj.lm_closets.is_drawer_box_bp or
                     obj.lm_closets.is_drawer_side_bp or
                     obj.lm_closets.is_drawer_back_bp or
                     obj.lm_closets.is_drawer_sub_front_bp or
                     obj.lm_closets.is_drawer_bottom_bp or
                     obj.lm_closets.is_file_rail_bp])

        # Find toe kicks
        e_bp.extend([obj for obj in blo if obj.lm_closets.is_toe_kick_bp or
                     obj.lm_closets.is_toe_kick_end_cap_bp or
                     obj.lm_closets.is_toe_kick_stringer_bp])

        # Find backings
        e_bp.extend([obj for obj in blo if obj.lm_closets.is_back_bp or
                     obj.lm_closets.is_top_back_bp or
                     obj.lm_closets.is_bottom_back_bp or
                     obj.lm_closets.is_hutch_back_bp or
                     obj.lm_closets.is_drawer_back_bp])

        # Find machining and add to exclusion list
        e_msh.extend(
            [obj for obj in blo if obj.cabinetlib.type_mesh == 'MACHINING'])

        # Find wall meshes
        e_msh.extend([obj for obj in blo if obj.mv.is_wall_mesh])

        # Add children of obj bps to exclusion list
        for bp in e_bp:
            for c in bp.children:
                if c.cabinetlib.type_mesh == 'CUTPART':
                    e_msh.append(c)

        return e_msh

    def level_elv_cameras(self):
        elv_cams = [c for c in bpy.data.objects if c.type == 'CAMERA'
                    and 'Plan View' not in c.name
                    and 'Accordion' not in c.name]
        cam_heights = [e.location.z for e in elv_cams]
        ortho_scales = [e.data.ortho_scale for e in elv_cams]
        avg_height = sum(cam_heights)/len(cam_heights)
        max_ortho_scale = max(ortho_scales)
        for e in elv_cams:
            e.location.z = avg_height
            e.data.ortho_scale = max_ortho_scale

    def execute(self, context):
        bpy.ops.fd_scene.clear_2d_views()
        self.ignore_obj_list = []
        dimprops = get_dimension_props()
        group_walls = {}
        mesh_data_dict = {}
        cross_section_parts = None
        joints = None
        context.window_manager.mv.use_opengl_dimensions = True
        # render_2d_dims = context.window_manager.mv.render_dimensions
        self.font = opengl_dim.get_custom_font()
        self.font_bold = opengl_dim.get_custom_font_bold()
        self.create_linestyles()
        self.main_scene = context.scene
        context.scene.name = "_Main"

        if self.use_single_scene:
            self.create_single_elv_view(context)

        else:
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

            walls = []
            wall_groups = {}

            self.create_plan_view_scene(context)

            for obj in bpy.data.objects:
                if obj.data is not None:
                    mesh_data = obj.data.name
                    mesh_data_dict[obj.name] = mesh_data
            for obj in self.main_scene.objects:
                if obj.mv.type == 'BPWALL':
                    wall = fd_types.Wall(obj_bp=obj)
                    if len(wall.get_wall_groups()) > 0:
                        wall_group = self.create_elv_view_scene(context, wall)
                        left_wall = wall.get_connected_wall('LEFT')
                        walls.append((wall, left_wall))
                        wall_groups[wall.obj_bp.name] = wall_group
                        group_walls[wall_group.name] = wall.obj_bp.name
            joints = self.process_connected_walls(context, walls)
            cross_section_parts = self.add_wall_joints_to_grp(
                context, wall_groups, joints)

        self.clear_unused_linestyles()
        bpy.context.screen.scene = self.main_scene
        wm = context.window_manager.mv
        wm.elevation_scene_index = 0
        bpy.ops.object.select_all(action='DESELECT')
        self.unlink_cleats(context)
        bpy.ops.object.select_all(action='DESELECT')

        if dimprops.include_accordions:
            self.create_acordion_scenes(
                context, mesh_data_dict, cross_section_parts)
        bpy.context.screen.scene = bpy.data.scenes['_Main']
        self.level_elv_cameras()

        # Add objects to freestyle hidden line exclusion group
        fs_exclude_grp = bpy.data.groups['FS Hidden Exclude']
        fs_exclude_objs = self.exclude_fs_hidden()
        for item in fs_exclude_objs:
            if item.name not in fs_exclude_grp.objects:
                fs_exclude_grp.objects.link(item)

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
                        'FONT' or obj.type == 'CURVE' or (obj.type == 'EMPTY'
                        and obj.name.endswith('Labels'))]
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

        # Prevent Main Accordion from being rendered
        if "Z_Main Accordion" in bpy.data.scenes:
            bpy.data.scenes["Z_Main Accordion"].mv.elevation_selected = False

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
