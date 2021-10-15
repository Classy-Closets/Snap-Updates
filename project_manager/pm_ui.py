
import bpy
from bpy.types import Panel
from bpy.types import Menu, UIList

from . import pm_utils


class SNAP_UL_Projects(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text="", icon='FILEBROWSER')
        layout.label(text=item.name)
        if item.name == context.window_manager.sn_project.get_project().name:
            layout.popover("SNAP_PT_Project_Info", icon='INFO', text="")
            layout.operator("project_manager.delete_project", text="", icon='X', emboss=True).index = index


class SNAP_UL_Rooms(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        project = context.window_manager.sn_project.get_project()
        room = project.rooms[project.room_index]
        layout.label(text="", icon='SNAP_PEEL_OBJECT')
        layout.prop(item, 'name', text='', emboss=False)
        if item.name == room.name:
            layout.operator("project_manager.delete_room", text="", icon='X', emboss=True).index = index


class SNAP_MT_Project_Tools(Menu):
    bl_label = "Project Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator("sn_library.open_browser_window",
                        text="Open Projects Location in Browser",
                        icon='FILE_FOLDER').path = pm_utils.get_project_dir()


class SNAP_PT_Project_Popup_Menu(Panel):
    bl_label = "Project Popup"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'HEADER'
    bl_label = "Presets"
    path_menu = Menu.path_menu

    @classmethod
    def draw_panel_header(cls, layout):
        layout.emboss = 'PULLDOWN_MENU'
        layout.popover(
            panel="SNAP_PT_Project_Tools",
            icon='COLLAPSEMENU',
            text="")

    def draw(self, context):
        layout = self.layout
        layout.emboss = 'NONE'
        layout.operator_context = 'EXEC_DEFAULT'
        Menu.draw_preset(self, context)


class SNAP_PT_Projects(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "Projects"
    bl_order = 0

    props = None

    def draw_header_preset(self, _context):
        SNAP_PT_Project_Popup_Menu.draw_panel_header(self.layout)

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='INFO')

    def draw_common_ops(self, box):
        row = box.row(align=True)
        row.operator("project_manager.prepare_proj_xml", icon='EXPORT')

    def draw(self, context):
        wm = bpy.context.window_manager.sn_project
        projects = wm.projects
        layout = self.layout
        box = layout.box()

        if len(projects) > 0:
            active_project = wm.projects[wm.project_index]

            if wm.use_compact_ui:
                row_1 = box.row()
                col = row_1.column(align=True)
                row_2 = col.row(align=True)
                row_2.operator("project_manager.create_project", icon='FILE_NEW')
                row_2.menu('SNAP_MT_Project_Tools', text="", icon='DOWNARROW_HLT')
                col.template_list("SNAP_UL_Projects", "", wm, "projects", wm, "project_index", maxrows=5)
                self.draw_common_ops(col)
                active_project.draw(row_1)
            else:
                col = box.column(align=True)
                row = col.row(align=True)
                row.operator("project_manager.create_project", icon='FILE_NEW')
                row.operator("project_manager.copy_project", text="Copy Project", icon='DUPLICATE')
                row.menu('SNAP_MT_Project_Tools', text="", icon='DOWNARROW_HLT')
                if(len(projects) < 5):
                    col.template_list("SNAP_UL_Projects", "", wm, "projects", wm, "project_index", rows=len(projects))
                    self.draw_common_ops(col)
                    active_project = wm.projects[wm.project_index]
                    col.separator()
                    active_project.draw(col)
                else:
                    col.template_list("SNAP_UL_Projects", "", wm, "projects", wm, "project_index", maxrows=5)
                    self.draw_common_ops(col)
                    col.separator()
                    active_project = wm.projects[wm.project_index]
                    active_project.draw(col)
        else:
            row = box.row(align=True)
            row.operator("project_manager.create_project", icon='FILE_NEW')
            row.menu('SNAP_MT_Project_Tools', text="", icon='DOWNARROW_HLT')


class SNAP_PT_Project_Tools(Panel):
    bl_space_type = 'INFO'
    bl_label = "Project Tools"
    bl_region_type = 'HEADER'
    bl_ui_units_x = 10

    def draw(self, context):
        wm = context.window_manager.sn_project
        layout = self.layout
        layout.prop(wm, "use_compact_ui")


class SNAP_PT_Project_Info(Panel):
    bl_space_type = 'INFO'
    bl_label = "Project Info"
    bl_region_type = 'HEADER'
    bl_ui_units_x = 22

    def draw(self, context):
        proj_props = context.window_manager.sn_project.get_project()
        layout = self.layout
        layout.label(text="Project Info")
        box = layout.box()
        col = box.column()
        col.prop(proj_props, 'customer_name')
        col.prop(proj_props, 'client_id')
        col.prop(proj_props, 'project_address')
        col.prop(proj_props, 'city')
        col.prop(proj_props, 'state')
        col.prop(proj_props, 'zip_code')
        col.prop(proj_props, 'customer_phone_1')
        col.prop(proj_props, 'customer_phone_2')
        col.prop(proj_props, 'customer_email')
        col.prop(proj_props, 'project_notes')
        col.prop(proj_props, 'designer')
        col.prop(proj_props, 'design_date')


classes = (
    SNAP_UL_Projects,
    SNAP_UL_Rooms,
    SNAP_MT_Project_Tools,
    SNAP_PT_Project_Popup_Menu,
    SNAP_PT_Projects,
    SNAP_PT_Project_Tools,
    SNAP_PT_Project_Info,
)

register, unregister = bpy.utils.register_classes_factory(classes)
