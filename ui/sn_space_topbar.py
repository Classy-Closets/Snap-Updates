import bpy
from bpy.types import Header, Menu


class TOPBAR_HT_upper_bar(Header):
    bl_space_type = 'TOPBAR'

    def draw(self, context):
        region = context.region

        if region.alignment == 'RIGHT':
            self.draw_right(context)
        else:
            self.draw_left(context)

    def draw_left(self, context):
        layout = self.layout

        window = context.window
        screen = context.screen

        TOPBAR_MT_editor_menus.draw_collapsible(context, layout)

        layout.separator()

        if not screen.show_fullscreen:
            layout.template_ID_tabs(
                window, "workspace",
                new="workspace.add",
                menu="TOPBAR_MT_workspace_menu",
            )
        else:
            layout.operator(
                "screen.back_to_previous",
                icon='SCREEN_BACK',
                text="Back to Previous",
            )

    def draw_right(self, context):
        layout = self.layout

        window = context.window
        screen = context.screen
        scene = window.scene

        # If statusbar is hidden, still show messages at the top
        if not screen.show_statusbar:
            layout.template_reports_banner()
            layout.template_running_jobs()

        # Active workspace view-layer is retrieved through window, not through workspace.
        layout.template_ID(window, "scene", new="scene.new",
                           unlink="scene.delete")

        if context.scene.snap.ui.use_default_blender_interface:
            row = layout.row(align=True)
            row.template_search(
                window, "view_layer",
                scene, "view_layers",
                new="scene.view_layer_add",
                unlink="scene.view_layer_remove")


class TOPBAR_MT_file(Menu):
    bl_label = "File"

    def draw(self, context):
        layout = self.layout

        layout.operator_context = 'INVOKE_AREA'
        layout.menu("TOPBAR_MT_file_new", text="New", icon='FILE_NEW')
        layout.operator("wm.open_mainfile", text="Open...", icon='FILE_FOLDER')
        layout.menu("TOPBAR_MT_file_open_recent")
        layout.operator("wm.revert_mainfile")
        layout.menu("TOPBAR_MT_file_recover")

        layout.separator()

        layout.operator_context = 'EXEC_AREA' if context.blend_data.is_saved else 'INVOKE_AREA'
        layout.operator("wm.save_mainfile", text="Save", icon='FILE_TICK')

        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.save_as_mainfile", text="Save As...")
        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.save_as_mainfile", text="Save Copy...").copy = True

        layout.separator()

        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.link", text="Link...", icon='LINK_BLEND')
        layout.operator("wm.append", text="Append...", icon='APPEND_BLEND')
        layout.menu("TOPBAR_MT_file_previews")

        layout.separator()

        layout.menu("TOPBAR_MT_file_import", icon='IMPORT')
        layout.menu("TOPBAR_MT_file_export", icon='EXPORT')

        layout.separator()

        layout.menu("TOPBAR_MT_file_external_data")
        layout.menu("TOPBAR_MT_file_cleanup")

        layout.separator()

        layout.operator("snap.load_snap_defaults")
        layout.prop(context.scene.snap.ui, "use_default_blender_interface")

        layout.separator()

        layout.menu("TOPBAR_MT_file_defaults")

        layout.separator()
        layout.operator("wm.quit_blender", text="Quit", icon='QUIT')


class TOPBAR_MT_editor_menus(Menu):
    bl_idname = "TOPBAR_MT_editor_menus"
    bl_label = ""

    def draw(self, context):
        layout = self.layout

        # Allow calling this menu directly (this might not be a header area).
        if getattr(context.area, "show_menus", False):
            layout.menu("TOPBAR_MT_app", text="", icon='EVENT_S')
        else:
            layout.menu("TOPBAR_MT_app", text="SNaP")

        layout.menu("TOPBAR_MT_file")
        layout.menu("TOPBAR_MT_edit")

        layout.menu("TOPBAR_MT_render")

        layout.menu("TOPBAR_MT_window")
        layout.menu("TOPBAR_MT_help")


class TOPBAR_MT_help(Menu):
    bl_label = "Help"

    def draw(self, context):
        layout = self.layout

        show_developer = context.preferences.view.show_developer_ui

        layout.operator("wm.url_open", text="SNaP Release Log", icon='URL').url = "https://classy-closets.github.io/SNaP-2.0/"
        layout.separator()        

        layout.operator("wm.url_open_preset", text="Manual",
                        icon='HELP').type = 'MANUAL'

        layout.operator(
            "wm.url_open", text="Tutorials", icon='URL',
        ).url = "https://www.blender.org/tutorials"
        layout.operator(
            "wm.url_open", text="Support", icon='URL',
        ).url = "https://www.blender.org/support"

        layout.separator()

        layout.operator(
            "wm.url_open", text="User Communities", icon='URL',
        ).url = "https://www.blender.org/community/"
        layout.operator(
            "wm.url_open", text="Developer Community", icon='URL',
        ).url = "https://devtalk.blender.org"

        layout.separator()

        layout.operator(
            "wm.url_open", text="Python API Reference", icon='URL',
        ).url = bpy.types.WM_OT_doc_view._prefix

        if show_developer:
            layout.operator(
                "wm.url_open", text="Developer Documentation", icon='URL',
            ).url = "https://wiki.blender.org/wiki/Main_Page"

            layout.operator("wm.operator_cheat_sheet", icon='TEXT')

        layout.separator()

        layout.operator("wm.url_open_preset",
                        text="Report a Bug", icon='URL').type = 'BUG'

        layout.separator()

        layout.operator("wm.sysinfo")


classes = (
    TOPBAR_HT_upper_bar,
    TOPBAR_MT_file,
    TOPBAR_MT_editor_menus,
    TOPBAR_MT_help,
)

register, unregister = bpy.utils.register_classes_factory(classes)
