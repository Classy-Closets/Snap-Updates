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

# <pep8 compliant>
import bpy
from bpy.types import (
    Header,
    Menu,
    Panel,
)

from bl_ui.properties_grease_pencil_common import (
    AnnotationDataPanel,
)
from bl_ui.space_toolsystem_common import (
    ToolActivePanelHelper,
)
from bpy.app.translations import contexts as i18n_contexts


class VIEW3D_HT_header(Header):
    bl_space_type = 'VIEW_3D'

    @staticmethod
    def draw_xform_template(layout, context):
        obj = context.active_object
        object_mode = 'OBJECT' if obj is None else obj.mode
        has_pose_mode = (
            (object_mode == 'POSE') or
            (object_mode == 'WEIGHT_PAINT' and context.pose_object is not None)
        )

        tool_settings = context.tool_settings

        # Mode & Transform Settings
        scene = context.scene

        if context.scene.snap.ui.use_default_blender_interface:
            # Orientation
            if object_mode in {'OBJECT', 'EDIT', 'EDIT_GPENCIL'} or has_pose_mode:
                orient_slot = scene.transform_orientation_slots[0]
                row = layout.row(align=True)

                sub = row.row()
                sub.ui_units_x = 4
                sub.prop_with_popover(
                    orient_slot,
                    "type",
                    text="",
                    panel="VIEW3D_PT_transform_orientations",
                )

            # Pivot
            if object_mode in {'OBJECT', 'EDIT', 'EDIT_GPENCIL', 'SCULPT_GPENCIL'} or has_pose_mode:
                layout.prop(tool_settings, "transform_pivot_point", text="", icon_only=True)

            # Snap
            show_snap = False
            if obj is None:
                show_snap = True
            else:
                if (object_mode not in {
                        'SCULPT', 'VERTEX_PAINT', 'WEIGHT_PAINT', 'TEXTURE_PAINT',
                        'PAINT_GPENCIL', 'SCULPT_GPENCIL', 'WEIGHT_GPENCIL', 'VERTEX_GPENCIL'
                }) or has_pose_mode:
                    show_snap = True
                else:

                    paint_settings = UnifiedPaintPanel.paint_settings(context)

                    if paint_settings:
                        brush = paint_settings.brush
                        if brush and hasattr(brush, "stroke_method") and brush.stroke_method == 'CURVE':
                            show_snap = True

            if show_snap:
                snap_items = bpy.types.ToolSettings.bl_rna.properties["snap_elements"].enum_items
                snap_elements = tool_settings.snap_elements
                if len(snap_elements) == 1:
                    text = ""
                    for elem in snap_elements:
                        icon = snap_items[elem].icon
                        break
                else:
                    text = "Mix"
                    icon = 'NONE'
                del snap_items, snap_elements

                row = layout.row(align=True)
                row.prop(tool_settings, "use_snap", text="")

                sub = row.row(align=True)
                sub.popover(
                    panel="VIEW3D_PT_snapping",
                    icon=icon,
                    text=text,
                )

            # Proportional editing
            if object_mode in {'EDIT', 'PARTICLE_EDIT', 'SCULPT_GPENCIL', 'EDIT_GPENCIL', 'OBJECT'}:
                row = layout.row(align=True)
                kw = {}
                if object_mode == 'OBJECT':
                    attr = "use_proportional_edit_objects"
                else:
                    attr = "use_proportional_edit"

                    if tool_settings.use_proportional_edit:
                        if tool_settings.use_proportional_connected:
                            kw["icon"] = 'PROP_CON'
                        elif tool_settings.use_proportional_projected:
                            kw["icon"] = 'PROP_PROJECTED'
                        else:
                            kw["icon"] = 'PROP_ON'
                    else:
                        kw["icon"] = 'PROP_OFF'

            row.prop(tool_settings, attr, icon_only=True, **kw)
            sub = row.row(align=True)
            sub.active = getattr(tool_settings, attr)
            sub.prop_with_popover(
                tool_settings,
                "proportional_edit_falloff",
                text="",
                icon_only=True,
                panel="VIEW3D_PT_proportional_edit",
            )

    def draw(self, context):
        layout = self.layout

        tool_settings = context.tool_settings
        view = context.space_data
        shading = view.shading
        show_region_tool_header = view.show_region_tool_header

        if not show_region_tool_header:
            layout.row(align=True).template_header()

        row = layout.row(align=True)
        obj = context.active_object
        # mode_string = context.mode
        object_mode = 'OBJECT' if obj is None else obj.mode
        has_pose_mode = (
            (object_mode == 'POSE') or
            (object_mode == 'WEIGHT_PAINT' and context.pose_object is not None)
        )

        # Note: This is actually deadly in case enum_items have to be dynamically generated
        #       (because internal RNA array iterator will free everything immediately...).
        # XXX This is an RNA internal issue, not sure how to fix it.
        # Note: Tried to add an accessor to get translated UI strings instead of manual call
        #       to pgettext_iface below, but this fails because translated enumitems
        #       are always dynamically allocated.
        act_mode_item = bpy.types.Object.bl_rna.properties["mode"].enum_items[object_mode]
        act_mode_i18n_context = bpy.types.Object.bl_rna.properties["mode"].translation_context

        sub = row.row(align=True)
        sub.ui_units_x = 5.5
        sub.operator_menu_enum(
            "object.mode_set", "mode",
            text=bpy.app.translations.pgettext_iface(act_mode_item.name, act_mode_i18n_context),
            icon=act_mode_item.icon,
        )
        del act_mode_item

        layout.template_header_3D_mode()

        # Contains buttons like Mode, Pivot, Layer, Mesh Select Mode...
        if obj:
            # Particle edit
            if object_mode == 'PARTICLE_EDIT':
                row = layout.row()
                row.prop(tool_settings.particle_edit, "select_mode", text="", expand=True)

        # Grease Pencil
        if obj and obj.type == 'GPENCIL' and context.gpencil_data:
            gpd = context.gpencil_data

            if gpd.is_stroke_paint_mode:
                row = layout.row()
                sub = row.row(align=True)
                sub.prop(tool_settings, "use_gpencil_draw_onback", text="", icon='MOD_OPACITY')
                sub.separator(factor=0.4)
                sub.prop(tool_settings, "use_gpencil_automerge_strokes", text="")
                sub.separator(factor=0.4)
                sub.prop(tool_settings, "use_gpencil_weight_data_add", text="", icon='WPAINT_HLT')
                sub.separator(factor=0.4)
                sub.prop(tool_settings, "use_gpencil_draw_additive", text="", icon='FREEZE')

            # Select mode for Editing
            if gpd.use_stroke_edit_mode:
                row = layout.row(align=True)
                row.prop_enum(tool_settings, "gpencil_selectmode_edit", text="", value='POINT')
                row.prop_enum(tool_settings, "gpencil_selectmode_edit", text="", value='STROKE')

                subrow = row.row(align=True)
                subrow.enabled = not gpd.use_curve_edit
                subrow.prop_enum(tool_settings, "gpencil_selectmode_edit", text="", value='SEGMENT')

                # Curve edit submode
                row = layout.row(align=True)
                row.prop(gpd, "use_curve_edit", text="",
                         icon='IPO_BEZIER')
                sub = row.row(align=True)
                sub.active = gpd.use_curve_edit
                sub.popover(
                    panel="VIEW3D_PT_gpencil_curve_edit",
                    text="Curve Editing",
                )

            # Select mode for Sculpt
            if gpd.is_stroke_sculpt_mode:
                row = layout.row(align=True)
                row.prop(tool_settings, "use_gpencil_select_mask_point", text="")
                row.prop(tool_settings, "use_gpencil_select_mask_stroke", text="")
                row.prop(tool_settings, "use_gpencil_select_mask_segment", text="")

            # Select mode for Vertex Paint
            if gpd.is_stroke_vertex_mode:
                row = layout.row(align=True)
                row.prop(tool_settings, "use_gpencil_vertex_select_mask_point", text="")
                row.prop(tool_settings, "use_gpencil_vertex_select_mask_stroke", text="")
                row.prop(tool_settings, "use_gpencil_vertex_select_mask_segment", text="")

            if gpd.is_stroke_paint_mode:
                row = layout.row(align=True)
                row.prop(gpd, "use_multiedit", text="", icon='GP_MULTIFRAME_EDITING')

            if (
                    gpd.use_stroke_edit_mode or
                    gpd.is_stroke_sculpt_mode or
                    gpd.is_stroke_weight_mode or
                    gpd.is_stroke_vertex_mode
            ):
                row = layout.row(align=True)
                row.prop(gpd, "use_multiedit", text="", icon='GP_MULTIFRAME_EDITING')

                sub = row.row(align=True)
                sub.enabled = gpd.use_multiedit
                sub.popover(
                    panel="VIEW3D_PT_gpencil_multi_frame",
                    text="Multiframe",
                )

        overlay = view.overlay

        VIEW3D_MT_editor_menus.draw_collapsible(context, layout)

        if not context.scene.snap.ui.use_default_blender_interface:
            col = layout.column()
            if shading.type == 'WIREFRAME':
                col.operator_menu_enum("sn_general.change_shade_mode", "mode", text="Wire Frame", icon='SHADING_WIRE')
            if shading.type == 'SOLID':
                col.operator_menu_enum("sn_general.change_shade_mode", "mode", text="Solid", icon='SHADING_SOLID')
            if shading.type == 'MATERIAL':
                col.operator_menu_enum("sn_general.change_shade_mode", "mode", text="Material", icon='MATERIAL')
            if shading.type == 'RENDERED':
                col.operator_menu_enum("sn_general.change_shade_mode", "mode", text="Rendered", icon='SHADING_RENDERED')

            # Snap
            show_snap = False
            if obj is None:
                show_snap = True
            else:
                if (object_mode not in {
                        'SCULPT', 'VERTEX_PAINT', 'WEIGHT_PAINT', 'TEXTURE_PAINT',
                        'PAINT_GPENCIL', 'SCULPT_GPENCIL', 'WEIGHT_GPENCIL', 'VERTEX_GPENCIL'
                }) or has_pose_mode:
                    show_snap = True
                else:

                    paint_settings = UnifiedPaintPanel.paint_settings(context)

                    if paint_settings:
                        brush = paint_settings.brush
                        if brush and hasattr(brush, "stroke_method") and brush.stroke_method == 'CURVE':
                            show_snap = True

            if show_snap:
                snap_items = bpy.types.ToolSettings.bl_rna.properties["snap_elements"].enum_items
                snap_elements = tool_settings.snap_elements
                if len(snap_elements) == 1:
                    text = ""
                    for elem in snap_elements:
                        icon = snap_items[elem].icon
                        break
                else:
                    text = "Mix"
                    icon = 'NONE'
                del snap_items, snap_elements

                row = layout.row(align=True)
                row.prop(tool_settings, "use_snap", text="")

                sub = row.row(align=True)
                sub.popover(
                    panel="VIEW3D_PT_snapping",
                    icon=icon,
                    text=text,
                )

            # Gizmo toggle & popover.
            row = layout.row(align=True)
            # FIXME: place-holder icon.
            row.prop(view, "show_gizmo", text="", toggle=True, icon='GIZMO')
            sub = row.row(align=True)
            sub.active = view.show_gizmo
            sub.popover(
                panel="VIEW3D_PT_gizmo_display",
                text="",
            )

            layout.prop(overlay, "show_extras", text="", icon='LIGHT_DATA')                               

        layout.separator_spacer()

        if object_mode in {'PAINT_GPENCIL', 'SCULPT_GPENCIL'}:
            # Grease pencil
            if object_mode == 'PAINT_GPENCIL':
                layout.prop_with_popover(
                    tool_settings,
                    "gpencil_stroke_placement_view3d",
                    text="",
                    panel="VIEW3D_PT_gpencil_origin",
                )

            if object_mode in {'PAINT_GPENCIL', 'SCULPT_GPENCIL'}:
                layout.prop_with_popover(
                    tool_settings.gpencil_sculpt,
                    "lock_axis",
                    text="",
                    panel="VIEW3D_PT_gpencil_lock",
                )

            if object_mode == 'PAINT_GPENCIL':
                # FIXME: this is bad practice!
                # Tool options are to be displayed in the topbar.
                if context.workspace.tools.from_space_view3d_mode(object_mode).idname == "builtin_brush.Draw":
                    settings = tool_settings.gpencil_sculpt.guide
                    row = layout.row(align=True)
                    row.prop(settings, "use_guide", text="", icon='GRID')
                    sub = row.row(align=True)
                    sub.active = settings.use_guide
                    sub.popover(
                        panel="VIEW3D_PT_gpencil_guide",
                        text="Guides",
                    )

            layout.separator_spacer()
        elif not show_region_tool_header:
            # Transform settings depending on tool header visibility
            VIEW3D_HT_header.draw_xform_template(layout, context)

            layout.separator_spacer()

        if context.scene.snap.ui.use_default_blender_interface:
            # Viewport Settings
            layout.popover(
                panel="VIEW3D_PT_object_type_visibility",
                icon_value=view.icon_from_show_object_viewport,
                text="",
            )

            # Gizmo toggle & popover.
            row = layout.row(align=True)
            # FIXME: place-holder icon.
            row.prop(view, "show_gizmo", text="", toggle=True, icon='GIZMO')
            sub = row.row(align=True)
            sub.active = view.show_gizmo
            sub.popover(
                panel="VIEW3D_PT_gizmo_display",
                text="",
            )

            # Overlay toggle & popover.
            row = layout.row(align=True)
            row.prop(overlay, "show_overlays", icon='OVERLAY', text="")
            sub = row.row(align=True)
            sub.active = overlay.show_overlays
            sub.popover(panel="VIEW3D_PT_overlay", text="")

            row = layout.row()
            row.active = (object_mode == 'EDIT') or (shading.type in {'WIREFRAME', 'SOLID'})

            # While exposing 'shading.show_xray(_wireframe)' is correct.
            # this hides the key shortcut from users: T70433.
            if has_pose_mode:
                draw_depressed = overlay.show_xray_bone
            elif shading.type == 'WIREFRAME':
                draw_depressed = shading.show_xray_wireframe
            else:
                draw_depressed = shading.show_xray
            row.operator(
                "view3d.toggle_xray",
                text="",
                icon='XRAY',
                depress=draw_depressed,
            )

            row = layout.row(align=True)
            row.prop(shading, "type", text="", expand=True)
            sub = row.row(align=True)
            # TODO, currently render shading type ignores mesh two-side, until it's supported
            # show the shading popover which shows double-sided option.

            # sub.enabled = shading.type != 'RENDERED'
            sub.popover(panel="VIEW3D_PT_shading", text="")


class VIEW3D_MT_editor_menus(Menu):
    bl_label = ""

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        mode_string = context.mode
        edit_object = context.edit_object
        gp_edit = obj and obj.mode in {'EDIT_GPENCIL', 'PAINT_GPENCIL', 'SCULPT_GPENCIL',
                                       'WEIGHT_GPENCIL', 'VERTEX_GPENCIL'}
        ts = context.scene.tool_settings

        layout.menu("VIEW3D_MT_view")

        # Select Menu
        if gp_edit:
            if mode_string not in {'PAINT_GPENCIL', 'WEIGHT_GPENCIL'}:
                if (
                        mode_string == 'SCULPT_GPENCIL' and
                        (ts.use_gpencil_select_mask_point or
                         ts.use_gpencil_select_mask_stroke or
                         ts.use_gpencil_select_mask_segment)
                ):
                    layout.menu("VIEW3D_MT_select_gpencil")
                elif mode_string == 'EDIT_GPENCIL':
                    layout.menu("VIEW3D_MT_select_gpencil")
                elif mode_string == 'VERTEX_GPENCIL':
                    layout.menu("VIEW3D_MT_select_gpencil")
        elif mode_string in {'PAINT_WEIGHT', 'PAINT_VERTEX', 'PAINT_TEXTURE'}:
            mesh = obj.data
            if mesh.use_paint_mask:
                layout.menu("VIEW3D_MT_select_paint_mask")
            elif mesh.use_paint_mask_vertex and mode_string in {'PAINT_WEIGHT', 'PAINT_VERTEX'}:
                layout.menu("VIEW3D_MT_select_paint_mask_vertex")
        elif mode_string != 'SCULPT':
            layout.menu("VIEW3D_MT_select_%s" % mode_string.lower())

        if gp_edit:
            pass
        elif mode_string == 'OBJECT':
            layout.menu("VIEW3D_MT_add", text="Add", text_ctxt=i18n_contexts.operator_default)
        elif mode_string == 'EDIT_MESH':
            layout.menu("VIEW3D_MT_mesh_add", text="Add", text_ctxt=i18n_contexts.operator_default)
        elif mode_string == 'EDIT_CURVE':
            layout.menu("VIEW3D_MT_curve_add", text="Add", text_ctxt=i18n_contexts.operator_default)
        elif mode_string == 'EDIT_SURFACE':
            layout.menu("VIEW3D_MT_surface_add", text="Add", text_ctxt=i18n_contexts.operator_default)
        elif mode_string == 'EDIT_METABALL':
            layout.menu("VIEW3D_MT_metaball_add", text="Add", text_ctxt=i18n_contexts.operator_default)
        elif mode_string == 'EDIT_ARMATURE':
            layout.menu("TOPBAR_MT_edit_armature_add", text="Add", text_ctxt=i18n_contexts.operator_default)

        if gp_edit:
            if obj and obj.mode == 'PAINT_GPENCIL':
                layout.menu("VIEW3D_MT_draw_gpencil")
            elif obj and obj.mode == 'EDIT_GPENCIL':
                layout.menu("VIEW3D_MT_edit_gpencil")
                layout.menu("VIEW3D_MT_edit_gpencil_stroke")
                layout.menu("VIEW3D_MT_edit_gpencil_point")
            elif obj and obj.mode == 'WEIGHT_GPENCIL':
                layout.menu("VIEW3D_MT_weight_gpencil")
            if obj and obj.mode == 'VERTEX_GPENCIL':
                layout.menu("VIEW3D_MT_paint_gpencil")

        elif edit_object:
            layout.menu("VIEW3D_MT_edit_%s" % edit_object.type.lower())

            if mode_string == 'EDIT_MESH':
                layout.menu("VIEW3D_MT_edit_mesh_vertices")
                layout.menu("VIEW3D_MT_edit_mesh_edges")
                layout.menu("VIEW3D_MT_edit_mesh_faces")
                layout.menu("VIEW3D_MT_uv_map", text="UV")
            elif mode_string in {'EDIT_CURVE', 'EDIT_SURFACE'}:
                layout.menu("VIEW3D_MT_edit_curve_ctrlpoints")
                layout.menu("VIEW3D_MT_edit_curve_segments")

        elif obj:
            if mode_string != 'PAINT_TEXTURE':
                layout.menu("VIEW3D_MT_%s" % mode_string.lower())
            if mode_string == 'SCULPT':
                layout.menu("VIEW3D_MT_mask")
                layout.menu("VIEW3D_MT_face_sets")

        elif bpy.context.scene.snap.ui.use_default_blender_interface:
            layout.menu("VIEW3D_MT_object")


class VIEW3D_MT_view(Menu):
    bl_label = "View"

    def draw(self, context):
        layout = self.layout
        view = context.space_data

        if bpy.context.scene.snap.ui.use_default_blender_interface:
            layout.prop(view, "show_region_toolbar")
            layout.prop(view, "show_region_ui")
            layout.prop(view, "show_region_tool_header")
            layout.prop(view, "show_region_hud")

            layout.separator()

            layout.operator("view3d.view_selected", text="Frame Selected").use_all_regions = False
            if view.region_quadviews:
                layout.operator("view3d.view_selected", text="Frame Selected (Quad View)").use_all_regions = True

            layout.operator("view3d.view_all").center = False
            layout.operator("view3d.view_persportho", text="Perspective/Orthographic")
            layout.menu("VIEW3D_MT_view_local")

            layout.separator()

            layout.menu("VIEW3D_MT_view_cameras", text="Cameras")

            layout.separator()
            layout.menu("VIEW3D_MT_view_viewpoint")
            layout.menu("VIEW3D_MT_view_navigation")
            layout.menu("VIEW3D_MT_view_align")

            layout.separator()

            layout.operator_context = 'INVOKE_REGION_WIN'
            layout.menu("VIEW3D_MT_view_regions", text="View Regions")

            layout.separator()

            layout.operator("screen.animation_play", text="Play Animation")

            layout.separator()

            layout.operator("render.opengl", text="Viewport Render Image", icon='RENDER_STILL')
            layout.operator("render.opengl", text="Viewport Render Animation", icon='RENDER_ANIMATION').animation = True
            props = layout.operator("render.opengl",
                                    text="Viewport Render Keyframes",
                                    icon='RENDER_ANIMATION',
                                    )
            props.animation = True
            props.render_keyed_only = True

            layout.separator()

            layout.menu("INFO_MT_area")
        else:
            layout.prop(view, "show_region_toolbar")
            layout.prop(view, "show_region_ui")
            layout.separator()
            layout.operator("view3d.view_selected", text="Frame Selected").use_all_regions = False
            if view.region_quadviews:
                layout.operator("view3d.view_selected", text="Frame Selected (Quad View)").use_all_regions = True
            layout.operator("view3d.view_all").center = False
            layout.separator()
            layout.menu("VIEW3D_MT_view_viewpoint")
            layout.operator("view3d.view_persportho", text="Perspective/Orthographic")
            layout.separator()
            layout.menu("INFO_MT_area")


class VIEW3D_MT_select_object(Menu):
    bl_label = "Select"

    def draw(self, _context):
        layout = self.layout

        if bpy.context.scene.snap.ui.use_default_blender_interface:
            layout.operator("object.select_all", text="All").action = 'SELECT'
            layout.operator("object.select_all", text="None").action = 'DESELECT'
            layout.operator("object.select_all", text="Invert").action = 'INVERT'

            layout.separator()

            layout.operator("view3d.select_box")
            layout.operator("view3d.select_circle")

            layout.separator()

            layout.operator_menu_enum("object.select_by_type", "type", text="Select All by Type")
            layout.operator("object.select_camera", text="Select Active Camera")
            layout.operator("object.select_mirror")
            layout.operator("object.select_random", text="Select Random")

            layout.separator()

            layout.menu("VIEW3D_MT_select_object_more_less")

            layout.separator()

            layout.operator_menu_enum("object.select_grouped", "type", text="Select Grouped")
            layout.operator_menu_enum("object.select_linked", "type", text="Select Linked")
            layout.operator("object.select_pattern", text="Select Pattern...")
        else:
            layout.operator("object.select_all", text="All").action = 'SELECT'
            layout.operator("object.select_all", text="None").action = 'DESELECT'
            layout.separator()
            layout.operator("view3d.select_box")
            layout.operator("view3d.select_circle")
            layout.separator()
            layout.operator("object.select_camera", text="Select Active Camera")


class VIEW3D_MT_armature_add(Menu):
    bl_idname = "VIEW3D_MT_armature_add"
    bl_label = "Armature"

    def draw(self, _context):
        layout = self.layout

        layout.operator_context = 'EXEC_REGION_WIN'
        layout.operator("object.armature_add", text="Single Bone", icon='BONE_DATA')


class VIEW3D_MT_camera_add(Menu):
    bl_idname = "VIEW3D_MT_camera_add"
    bl_label = "Camera"

    def draw(self, _context):
        layout = self.layout
        layout.operator_context = 'EXEC_REGION_WIN'
        layout.operator("sn_object.add_camera", text="Camera", icon='OUTLINER_OB_CAMERA')


class VIEW3D_MT_add(Menu):
    bl_label = "Add"
    bl_translation_context = i18n_contexts.operator_default

    def draw(self, context):
        layout = self.layout

        if context.scene.snap.ui.use_default_blender_interface:
            # note, don't use 'EXEC_SCREEN' or operators won't get the 'v3d' context.

            # Note: was EXEC_AREA, but this context does not have the 'rv3d', which prevents
            #       "align_view" to work on first call (see T32719).
            layout.operator_context = 'EXEC_REGION_WIN'

            # layout.operator_menu_enum("object.mesh_add", "type", text="Mesh", icon='OUTLINER_OB_MESH')
            layout.menu("VIEW3D_MT_mesh_add", icon='OUTLINER_OB_MESH')

            # layout.operator_menu_enum("object.curve_add", "type", text="Curve", icon='OUTLINER_OB_CURVE')
            layout.menu("VIEW3D_MT_curve_add", icon='OUTLINER_OB_CURVE')
            # layout.operator_menu_enum("object.surface_add", "type", text="Surface", icon='OUTLINER_OB_SURFACE')
            layout.menu("VIEW3D_MT_surface_add", icon='OUTLINER_OB_SURFACE')
            layout.menu("VIEW3D_MT_metaball_add", text="Metaball", icon='OUTLINER_OB_META')
            layout.operator("object.text_add", text="Text", icon='OUTLINER_OB_FONT')
            if context.preferences.experimental.use_new_hair_type:
                layout.operator("object.hair_add", text="Hair", icon='OUTLINER_OB_HAIR')
            if context.preferences.experimental.use_new_point_cloud_type:
                layout.operator("object.pointcloud_add", text="Point Cloud", icon='OUTLINER_OB_POINTCLOUD')
            layout.menu("VIEW3D_MT_volume_add", text="Volume", icon='OUTLINER_OB_VOLUME')
            layout.operator_menu_enum("object.gpencil_add", "type", text="Grease Pencil", icon='OUTLINER_OB_GREASEPENCIL')

            layout.separator()

            if VIEW3D_MT_armature_add.is_extended():
                layout.menu("VIEW3D_MT_armature_add", icon='OUTLINER_OB_ARMATURE')
            else:
                layout.operator("object.armature_add", text="Armature", icon='OUTLINER_OB_ARMATURE')

            layout.operator("object.add", text="Lattice", icon='OUTLINER_OB_LATTICE').type = 'LATTICE'

            layout.separator()

            layout.operator_menu_enum("object.empty_add", "type", text="Empty", icon='OUTLINER_OB_EMPTY')
            layout.menu("VIEW3D_MT_image_add", text="Image", icon='OUTLINER_OB_IMAGE')

            layout.separator()

            layout.menu("VIEW3D_MT_light_add", icon='OUTLINER_OB_LIGHT')
            layout.menu("VIEW3D_MT_lightprobe_add", icon='OUTLINER_OB_LIGHTPROBE')

            layout.separator()

            if VIEW3D_MT_camera_add.is_extended():
                layout.menu("VIEW3D_MT_camera_add", icon='OUTLINER_OB_CAMERA')
            else:
                VIEW3D_MT_camera_add.draw(self, context)

            layout.separator()

            layout.operator("object.speaker_add", text="Speaker", icon='OUTLINER_OB_SPEAKER')

            layout.separator()

            layout.operator_menu_enum("object.effector_add", "type", text="Force Field", icon='OUTLINER_OB_FORCE_FIELD')

            layout.separator()

            has_collections = bool(bpy.data.collections)
            col = layout.column()
            col.enabled = has_collections

            if not has_collections or len(bpy.data.collections) > 10:
                col.operator_context = 'INVOKE_REGION_WIN'
                col.operator(
                    "object.collection_instance_add",
                    text="Collection Instance..." if has_collections else "No Collections to Instance",
                    icon='OUTLINER_OB_GROUP_INSTANCE',
                )
            else:
                col.operator_menu_enum(
                    "object.collection_instance_add",
                    "collection",
                    text="Collection Instance",
                    icon='OUTLINER_OB_GROUP_INSTANCE',
                )

        else:
            layout.separator()
            layout.menu("VIEW3D_MT_mesh_add", icon='OUTLINER_OB_MESH')
            layout.menu("VIEW3D_MT_curve_add", icon='OUTLINER_OB_CURVE')
            layout.operator("object.text_add", text="Text", icon='OUTLINER_OB_FONT')
            layout.separator()
            layout.operator_menu_enum("object.empty_add", "type", text="Empty", icon='OUTLINER_OB_EMPTY')
            layout.separator()
            layout.operator("sn_object.add_camera", icon='OUTLINER_OB_CAMERA')
            layout.menu("VIEW3D_MT_light_add", icon='OUTLINER_OB_LIGHT')
            layout.separator()
            layout.operator_menu_enum("object.gpencil_add", "type", text="Grease Pencil", icon='OUTLINER_OB_GREASEPENCIL')


class VIEW3D_MT_light_add(Menu):
    bl_idname = "VIEW3D_MT_light_add"
    bl_label = "Light"

    def draw(self, _context):
        layout = self.layout

        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator_enum("object.light_add", "type")
        if not _context.scene.snap.ui.use_default_blender_interface:
            layout.separator()
            layout.operator_context = 'INVOKE_REGION_WIN'
            layout.operator("sn_object.add_room_light", icon='LIGHT_AREA', text="Add Room Light")


class VIEW3D_PT_active_tool(Panel, ToolActivePanelHelper):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"
    # See comment below.
    # bl_options = {'HIDE_HEADER'}

    # Don't show in properties editor.
    @classmethod
    def poll(cls, context):
        bl_default_interface = context.scene.snap.ui.use_default_blender_interface
        return context.area.type == 'VIEW_3D' and bl_default_interface


class VIEW3D_PT_view3d_properties(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "View"
    bl_label = "View"

    @classmethod
    def poll(cls, context):
        return context.scene.snap.ui.use_default_blender_interface

    def draw(self, context):
        layout = self.layout

        view = context.space_data

        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        col = layout.column()

        subcol = col.column()
        subcol.active = bool(view.region_3d.view_perspective != 'CAMERA' or view.region_quadviews)
        subcol.prop(view, "lens", text="Focal Length")

        subcol = col.column(align=True)
        subcol.prop(view, "clip_start", text="Clip Start")
        subcol.prop(view, "clip_end", text="End")

        layout.separator()

        col = layout.column(align=False, heading="Local Camera")
        col.use_property_decorate = False
        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(view, "use_local_camera", text="")
        sub = sub.row(align=True)
        sub.enabled = view.use_local_camera
        sub.prop(view, "camera", text="")

        layout.separator()

        col = layout.column(align=True)
        col.prop(view, "use_render_border")
        col.active = view.region_3d.view_perspective != 'CAMERA'


class VIEW3D_PT_view3d_lock(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "View"
    bl_label = "View Lock"
    bl_parent_id = "VIEW3D_PT_view3d_properties"

    @classmethod
    def poll(cls, context):
        return context.scene.snap.ui.use_default_blender_interface

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        view = context.space_data

        col = layout.column(align=True)
        sub = col.column()
        sub.active = bool(view.region_3d.view_perspective != 'CAMERA' or view.region_quadviews)

        sub.prop(view, "lock_object")
        lock_object = view.lock_object
        if lock_object:
            if lock_object.type == 'ARMATURE':
                sub.prop_search(
                    view, "lock_bone", lock_object.data,
                    "edit_bones" if lock_object.mode == 'EDIT'
                    else "bones",
                    text="Bone",
                )

        col = layout.column(heading="Lock", align=True)
        if not lock_object:
            col.prop(view, "lock_cursor", text="To 3D Cursor")
        col.prop(view, "lock_camera", text="Camera to View")


class VIEW3D_PT_view3d_cursor(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "View"
    bl_label = "3D Cursor"

    @classmethod
    def poll(cls, context):
        return context.scene.snap.ui.use_default_blender_interface

    def draw(self, context):
        layout = self.layout

        cursor = context.scene.cursor

        layout.column().prop(cursor, "location", text="Location")
        rotation_mode = cursor.rotation_mode
        if rotation_mode == 'QUATERNION':
            layout.column().prop(cursor, "rotation_quaternion", text="Rotation")
        elif rotation_mode == 'AXIS_ANGLE':
            layout.column().prop(cursor, "rotation_axis_angle", text="Rotation")
        else:
            layout.column().prop(cursor, "rotation_euler", text="Rotation")
        layout.prop(cursor, "rotation_mode", text="")


class VIEW3D_PT_collections(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "View"
    bl_label = "Collections"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.scene.snap.ui.use_default_blender_interface

    def _draw_collection(self, layout, view_layer, use_local_collections, collection, index):
        need_separator = index
        for child in collection.children:
            index += 1

            if child.exclude:
                continue

            if child.collection.hide_viewport:
                continue

            if need_separator:
                layout.separator()
                need_separator = False

            icon = 'BLANK1'
            # has_objects = True
            if child.has_selected_objects(view_layer):
                icon = 'LAYER_ACTIVE'
            elif child.has_objects():
                icon = 'LAYER_USED'
            else:
                # has_objects = False
                pass

            row = layout.row()
            row.use_property_decorate = False
            sub = row.split(factor=0.98)
            subrow = sub.row()
            subrow.alignment = 'LEFT'
            subrow.operator(
                "object.hide_collection", text=child.name, icon=icon, emboss=False,
            ).collection_index = index

            sub = row.split()
            subrow = sub.row(align=True)
            subrow.alignment = 'RIGHT'
            if not use_local_collections:
                subrow.active = collection.is_visible  # Parent collection runtime visibility
                subrow.prop(child, "hide_viewport", text="", emboss=False)
            else:
                subrow.active = collection.visible_get()  # Parent collection runtime visibility
                icon = 'HIDE_OFF' if child.visible_get() else 'HIDE_ON'
                props = subrow.operator("object.hide_collection", text="", icon=icon, emboss=False)
                props.collection_index = index
                props.toggle = True

        for child in collection.children:
            index = self._draw_collection(layout, view_layer, use_local_collections, child, index)

        return index

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False

        view = context.space_data
        view_layer = context.view_layer

        layout.use_property_split = True
        layout.prop(view, "use_local_collections")
        layout.separator()

        # We pass index 0 here because the index is increased
        # so the first real index is 1
        # And we start with index as 1 because we skip the master collection
        self._draw_collection(layout, view_layer, view.use_local_collections, view_layer.layer_collection, 0)


# Annotation properties
class VIEW3D_PT_grease_pencil(AnnotationDataPanel, Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "View"

    @classmethod
    def poll(cls, context):
        return context.scene.snap.ui.use_default_blender_interface

    # NOTE: this is just a wrapper around the generic GP Panel


class VIEW3D_PT_context_properties(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"
    bl_label = "Properties"
    bl_options = {'DEFAULT_CLOSED'}

    @staticmethod
    def _active_context_member(context):
        obj = context.object
        if obj:
            object_mode = obj.mode
            if object_mode == 'POSE':
                return "active_pose_bone"
            elif object_mode == 'EDIT' and obj.type == 'ARMATURE':
                return "active_bone"
            else:
                return "object"

        return ""

    @classmethod
    def poll(cls, context):
        if not context.scene.snap.ui.use_default_blender_interface:
            return False
        import rna_prop_ui
        member = cls._active_context_member(context)

        if member:
            context_member, member = rna_prop_ui.rna_idprop_context_value(context, member, object)
            return context_member and rna_prop_ui.rna_idprop_has_properties(context_member)

        return False

    def draw(self, context):
        import rna_prop_ui
        member = VIEW3D_PT_context_properties._active_context_member(context)

        if member:
            # Draw with no edit button
            rna_prop_ui.draw(self.layout, context, member, object, False)


classes = (
    VIEW3D_HT_header,
    VIEW3D_MT_editor_menus,
    VIEW3D_MT_view,
    VIEW3D_MT_select_object,
    VIEW3D_MT_add,
    VIEW3D_PT_active_tool,
    VIEW3D_PT_view3d_properties,
    VIEW3D_PT_view3d_lock,
    VIEW3D_PT_view3d_cursor,
    VIEW3D_PT_collections,
    VIEW3D_PT_grease_pencil,
    VIEW3D_PT_context_properties,
    VIEW3D_MT_light_add
)


def register():
    for cls in classes:
        if hasattr(bpy.types, str(cls)):
            bpy.utils.unregister_class(cls)
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
