import bpy

def get_dimension_props():
    """
    This is a function to get access to all of the scene properties that are registered in this library
    """
    props = eval("bpy.context.scene.snap_closet_dimensions")
    return props

class VIEW_PT_2d_views(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "2D Views"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 2

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        layout = self.layout
        layout.label(text='', icon='ARROW_LEFTRIGHT')

    def draw_dim_options(self, context, layout):
        scene = context.scene
        dim_props = scene.snap.opengl_dim
        sys_units = scene.unit_settings.system
        box = layout.box()

        row = box.row()

        if dim_props.gl_dim_units == 'AUTO':
            row.label(text="Units:" + "                    (" + sys_units.title() + ")")
        else:
            row.label(text="Units:")

        row.prop(dim_props, 'gl_dim_units', text="")

        row = box.row()
        row.label(text="Arrow Type:")
        row.prop(dim_props, 'gl_arrow_type', expand=True)
        row = box.row()
        row.label(text="Color:")
        row.prop(dim_props, 'gl_default_color', text="")
        row = box.row()

        if dim_props.gl_dim_units in ('INCH', 'FEET') or dim_props.gl_dim_units == 'AUTO' and sys_units == 'IMPERIAL':
            row.label(text="Round to the nearest:")
            row.prop(dim_props, 'gl_imperial_rd_factor', text="")
            row = box.row()
            row.label(text="Number format:")
            row.prop(dim_props, 'gl_number_format', expand=True)

        else:
            row.label(text="Precision:")
            row.prop(dim_props, 'gl_precision', text="")

        row = box.row()
        row.label(text="Text Size:")
        row.prop(dim_props, 'gl_font_size', text="")
        row = box.row()
        row.label(text="Arrow Size:")
        row.prop(dim_props, 'gl_arrow_size', text="")

    def draw(self, context):
        props = context.window_manager.views_2d
        sn_wm = context.window_manager.snap

        layout = self.layout
        scene = context.scene
        panel_box = layout.box()

        # ----
        col = panel_box.column(align=True)
        col.prop(sn_wm, 'use_opengl_dimensions',
                 text='{}able Dimensions'.format(
                     "Dis" if sn_wm.use_opengl_dimensions else "En"),
                 icon='HIDE_ON' if sn_wm.use_opengl_dimensions else 'HIDE_OFF',
                 toggle=True)

        row = col.row(align=True)
        row.operator('sn_2d_views.add_dimension',
                     text='Add Dimension', icon='CURVE_NCURVE')
        row.operator('sn_2d_views.add_annotation',
                     text='Add Annotation', icon='ADD')

        row = col.row(align=True)
        row.operator("sn_2d_views.toggle_dimension_handles",
                     text="Show Dimension Handles", icon='OUTLINER_OB_EMPTY').turn_on = True
        row.operator("sn_2d_views.toggle_dimension_handles",
                     text="Hide Dimension Handles", icon='OUTLINER_OB_EMPTY').turn_on = False

        row = col.row(align=True)
        row.operator('sn_2d_views.dimension_interface',
                     text='Dimension Options', icon='SETTINGS')
        row.operator('sn_2d_views.accordion_interface',
                     text='Accordion Options', icon='SETTINGS')

        row = panel_box.row(align=True)
        row.scale_y = 1.3

        elv_scenes = []
        for scene in bpy.data.scenes:
            if scene.snap.elevation_scene:
                elv_scenes.append(scene)

        if len(elv_scenes) < 1:
            row.operator("sn_2d_views.generate_2d_views",
                         text="Prepare 2D Views", icon='RENDERLAYERS')
        else:

            row.operator("sn_2d_views.generate_2d_views",
                         text="", icon='FILE_REFRESH')
            row.operator("sn_2d_views.create_new_view", text="", icon='ADD')
            row.operator("2dviews.render_2d_views",
                         text="Render Selected Scenes", icon='RESTRICT_RENDER_OFF')
            row.menu('VIEW_MT_elevation_scene_options',
                     text="", icon='DOWNARROW_HLT')
            panel_box.template_list("VIEW_UL_scenes",
                                    " ",
                                    bpy.data,
                                    "scenes",
                                    bpy.context.window_manager.snap,
                                    "elevation_scene_index")

        image_views = context.window_manager.snap.image_views

        if len(image_views) > 0:
            dimprops = get_dimension_props()
            row = panel_box.row(align=True)
            if dimprops.include_accordions:
                row.prop(props, 'accordions_layout_setting', text="Accordions layout")
            elif not dimprops.include_accordions:
                row.prop(props, 'page_layout_setting', text="Elevations layout")
            paper_row = panel_box.row(align=True)
            paper_row.label(text='Paper Size')
            paper_row.prop(props, 'paper_size', expand=True)
            panel_box.operator('2dviews.report_2d_drawings', icon='FILE_BLANK')
            panel_box.label(text="Image Views", icon='RENDERLAYERS')
            row = panel_box.row()
            row.template_list("VIEW_UL_2d_images", " ", context.window_manager.snap,
                              "image_views", context.window_manager.snap, "image_view_index")
            col = row.column(align=True)
            col.operator('sn_2d_views.move_2d_image_item',
                         text="", icon='TRIA_UP').direction = 'UP'
            col.operator('sn_2d_views.move_2d_image_item', text="",
                         icon='TRIA_DOWN').direction = 'DOWN'
#             panel_box.operator('2dviews.create_pdf',text="Create PDF",icon='FILE_BLANK')


class VIEW_MT_2dview_reports(bpy.types.Menu):
    bl_label = "2D Reports"

    """
    Report Templates are added to this menu
    """

    def draw(self, context):
        layout = self.layout


class VIEW_MT_elevation_scene_options(bpy.types.Menu):
    bl_label = "Elevation Scene Options"

    def draw(self, context):
        layout = self.layout
        layout.operator("sn_general.select_all_elevation_scenes",
                        text="Select All", icon='CHECKBOX_HLT').select_all = True
        layout.operator("sn_general.select_all_elevation_scenes",
                        text="Deselect All", icon='CHECKBOX_DEHLT').select_all = False
        layout.separator()
        layout.operator('sn_general.project_info',
                        text="View Project Info", icon='INFO')
        layout.operator("2dviews.create_snap_shot",
                        text="Create Snap Shot", icon='SCENE')
        layout.operator("sn_2d_views.append_to_view",
                        text="Append to View", icon='ADD')
        layout.separator()
        layout.operator("sn_scene.user_clear_2d_views",
                        text="Clear All 2D Views", icon='X')


class VIEW_UL_scenes(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        main_accordion = "Z_Main Accordion" in item.snap.name_scene
        virtual = "z_virtual" in item.snap.name_scene
        if (item.snap.plan_view_scene or item.snap.name_scene) and not main_accordion and not virtual:
            layout.label(text=item.snap.name_scene, icon='RESTRICT_RENDER_OFF')
            layout.prop(item.snap, 'elevation_selected', text="")
        elif not item.snap.plan_view_scene and not item.snap.elevation_scene:
            layout.label(text=item.name, icon='SCENE_DATA')

    def filter_items(self, context, data, propname):
        flt_flags = []
        flt_neworder = []
        scenes = getattr(data, propname)
        helper_funcs = bpy.types.UI_UL_list

        if not flt_flags:
            flt_flags = [self.bitflag_filter_item] * len(scenes)

        for i, scene in enumerate(scenes):
            if scene.sn_closets.is_drill_scene:
                flt_flags[i] &= ~self.bitflag_filter_item

        flt_neworder = helper_funcs.sort_items_by_name(scenes, "name")

        return flt_flags, flt_neworder


class VIEW_UL_2d_images(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        layout.label(text=item.name, icon='RENDER_RESULT')
        layout.operator('2dviews.view_image', text="",
                        icon='RESTRICT_VIEW_OFF', emboss=False).image_name = item.name
        layout.operator('2dviews.delete_image', text="",
                        icon='X', emboss=False).image_name = item.name


classes = (
    VIEW_PT_2d_views,
    VIEW_MT_2dview_reports,
    VIEW_MT_elevation_scene_options,
    VIEW_UL_scenes,
    VIEW_UL_2d_images
)

register, unregister = bpy.utils.register_classes_factory(classes)
