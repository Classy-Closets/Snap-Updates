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

import os

import bpy
from bpy.types import (
    Header,
    Panel,
    Menu,
    UIList
)

import snap
from snap import sn_utils
from snap import sn_handlers
import gpu
from gpu_extras.batch import batch_for_shader
from gpu_extras.presets import draw_texture_2d
import bpy_extras.image_utils as img_utils
from mathutils import Vector
from bpy.app.handlers import persistent


class SN_FILEBROWSER_MT_library_commands(Menu):
    bl_label = "Library Commands"

    def draw(self, context):
        layout = self.layout

        layout.operator(
            'sn_library.open_browser_window',
            icon='FILE_FOLDER').path = context.space_data.params.directory.decode("utf-8")


class SN_FILEBROWSER_PT_product_lib_header(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'UI'
    bl_label = "Closet Library"
    bl_category = "Attributes"
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        if len(context.area.spaces) > 1:
            return True
        return False

    def draw(self, context):
        layout = self.layout
        wm_props = context.window_manager.snap
        scene_props = context.scene.snap
        library_name = ""

        try:
            active_library = wm_props.libraries[scene_props.active_library_name]
            library_name = active_library.name
        except KeyError as error:
            print(error)
            print("Library: {} not found.".format(scene_props.active_library_name))
            print("Reloading SNaP Libraries...")
            sn_handlers.load_libraries()

        col = layout.column()
        row = col.row()
        row.scale_y = 1.25
        row.label(text=library_name)
        row.separator()
        row.menu('SN_FILEBROWSER_MT_library_commands', text="", icon='COLLAPSEMENU')
        row = col.row()
        row.scale_y = 1.25
        row.menu('SN_FILEBROWSER_MT_category_menu',
                 text=scene_props.active_category, icon='FILEBROWSER')


class SN_FILEBROWSER_MT_category_menu(Menu):
    bl_label = "Library Category"

    def draw(self, context):
        layout = self.layout
        scene_props = context.scene.snap
        wm_props = context.window_manager.snap
        active_library = wm_props.libraries[scene_props.active_library_name]

        if active_library.lib_type == 'SNAP':
            root_dir = active_library.thumbnail_dir
            dirs = os.listdir(root_dir)

        if active_library.lib_type == 'STANDARD':
            root_dir = active_library.root_dir
            dirs = os.listdir(root_dir)

        for d in dirs:
            path = os.path.join(root_dir, d)
            if os.path.isdir(path):
                layout.operator('sn_library.change_library_category',
                                text=d, icon='FILEBROWSER').category = d


class SN_FILEBROWSER_PT_library_settings(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_label = "Library"
    bl_region_type = 'HEADER'
    bl_ui_units_x = 32

    def draw(self, context):
        layout = self.layout
        preferences = context.preferences
        snap_prefs = preferences.addons["snap"].preferences
        snap_prefs.draw(context, layout)


class SN_FILEBROWSER_PT_library_tabs(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_label = "Libraries"
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        if len(context.area.spaces) > 1:
            return True

        # can be None when save/reload with a file selector open
        return context.space_data.params is not None

    def draw(self, context):
        

        layout = self.layout
        wm_props = context.window_manager.snap
        scene_props = context.scene.snap
        col = layout.column(align=True)
        icon_num = 0

        for library in wm_props.libraries:
            icon_num += 1
            emboss = library.name == scene_props.active_library_name
            if library.use_custom_icon:
                col.operator(
                    'sn_library.set_active_library',
                    text=library.name,
                    icon_value=snap.snap_icons[library.icon].icon_id,
                    emboss=emboss
                ).library_name = library.name
            else:
                col.operator(
                    'sn_library.set_active_library',
                    text=library.name,
                    icon=library.icon,
                    emboss=emboss
                ).library_name = library.name


class FILEBROWSER_HT_header(Header):
    bl_space_type = 'FILE_BROWSER'

    def draw(self, context):
        layout = self.layout

        st = context.space_data

        if st.active_operator is None:
            layout.template_header()

        layout.menu("FILEBROWSER_MT_view")
        layout.menu("FILEBROWSER_MT_select")

        # can be None when save/reload with a file selector open

        layout.separator_spacer()

        layout.template_running_jobs()


class FILEBROWSER_PT_display(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'HEADER'
    bl_label = "Display"

    @classmethod
    def poll(cls, context):
        if len(context.area.spaces) > 1:
            return False

        # can be None when save/reload with a file selector open
        return context.space_data.params is not None

    def draw(self, context):
        layout = self.layout

        space = context.space_data
        params = space.params

        layout.label(text="Display as")
        layout.column().prop(params, "display_type", expand=True)

        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        if params.display_type == 'THUMBNAIL':
            layout.prop(params, "display_size", text="Size")
        else:
            layout.prop(params, "show_details_size", text="Size")
            layout.prop(params, "show_details_datetime", text="Date")

        layout.prop(params, "recursion_level", text="Recursions")

        layout.use_property_split = False
        layout.separator()

        layout.label(text="Sort by")
        layout.column().prop(params, "sort_method", expand=True)
        layout.prop(params, "use_sort_invert")


class FILEBROWSER_PT_filter(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'HEADER'
    bl_label = "Filter"

    @classmethod
    def poll(cls, context):
        if len(context.area.spaces) > 1:
            return False
        # can be None when save/reload with a file selector open
        return context.space_data.params is not None

    def draw(self, context):
        layout = self.layout

        space = context.space_data
        params = space.params
        is_lib_browser = params.use_library_browsing

        row = layout.row(align=True)
        row.prop(params, "use_filter", text="", toggle=0)
        row.label(text="Filter")

        col = layout.column()
        col.active = params.use_filter

        row = col.row()
        row.label(icon='FILE_FOLDER')
        row.prop(params, "use_filter_folder", text="Folders", toggle=0)

        if params.filter_glob:
            col.label(text=params.filter_glob)
        else:
            row = col.row()
            row.label(icon='FILE_BLEND')
            row.prop(params, "use_filter_blender",
                     text=".blend Files", toggle=0)
            row = col.row()
            row.label(icon='FILE_BACKUP')
            row.prop(params, "use_filter_backup",
                     text="Backup .blend Files", toggle=0)
            row = col.row()
            row.label(icon='FILE_IMAGE')
            row.prop(params, "use_filter_image", text="Image Files", toggle=0)
            row = col.row()
            row.label(icon='FILE_MOVIE')
            row.prop(params, "use_filter_movie", text="Movie Files", toggle=0)
            row = col.row()
            row.label(icon='FILE_SCRIPT')
            row.prop(params, "use_filter_script",
                     text="Script Files", toggle=0)
            row = col.row()
            row.label(icon='FILE_FONT')
            row.prop(params, "use_filter_font", text="Font Files", toggle=0)
            row = col.row()
            row.label(icon='FILE_SOUND')
            row.prop(params, "use_filter_sound", text="Sound Files", toggle=0)
            row = col.row()
            row.label(icon='FILE_TEXT')
            row.prop(params, "use_filter_text", text="Text Files", toggle=0)

        col.separator()

        if is_lib_browser:
            row = col.row()
            row.label(icon='BLANK1')  # Indentation
            row.prop(params, "use_filter_blendid",
                     text="Blender IDs", toggle=0)
            if params.use_filter_blendid:
                row = col.row()
                row.label(icon='BLANK1')  # Indentation
                row.prop(params, "filter_id_category", text="")

                col.separator()

        layout.prop(params, "show_hidden")


def panel_poll_is_upper_region(region):
    # The upper region is left-aligned, the lower is split into it then.
    # Note that after "Flip Regions" it's right-aligned.
    return region.alignment in {'LEFT', 'RIGHT'}


class FILEBROWSER_UL_dir(UIList):
    def draw_item(self, _context, layout, _data, item, icon, _active_data, active_propname, _index):
        direntry = item
        # space = context.space_data

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.enabled = direntry.is_valid
            # Non-editable entries would show grayed-out, which is bad in this specific case, so switch to mere label.
            if direntry.is_property_readonly("name"):
                row.label(text=direntry.name, icon_value=icon)
            else:
                row.prop(direntry, "name", text="",
                         emboss=False, icon_value=icon)

        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.prop(direntry, "path", text="")


class FILEBROWSER_PT_bookmarks_volumes(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_category = "Bookmarks"
    bl_label = "Volumes"

    @classmethod
    def poll(cls, context):
        if len(context.area.spaces) > 1:
            return False
        return panel_poll_is_upper_region(context.region)

    def draw(self, context):
        layout = self.layout
        space = context.space_data

        if space.system_folders:
            row = layout.row()
            row.template_list("FILEBROWSER_UL_dir", "system_folders", space, "system_folders",
                              space, "system_folders_active", item_dyntip_propname="path", rows=1, maxrows=10)


class FILEBROWSER_PT_bookmarks_system(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_category = "Bookmarks"
    bl_label = "System"

    @classmethod
    def poll(cls, context):
        if len(context.area.spaces) > 1:
            return False
        return not context.preferences.filepaths.hide_system_bookmarks and panel_poll_is_upper_region(context.region)

    def draw(self, context):
        layout = self.layout
        space = context.space_data

        if space.system_bookmarks:
            row = layout.row()
            row.template_list("FILEBROWSER_UL_dir", "system_bookmarks", space, "system_bookmarks",
                              space, "system_bookmarks_active", item_dyntip_propname="path", rows=1, maxrows=10)


class FILEBROWSER_MT_bookmarks_context_menu(Menu):
    bl_label = "Bookmarks Specials"

    def draw(self, _context):
        layout = self.layout
        layout.operator("file.bookmark_cleanup", icon='X', text="Cleanup")

        layout.separator()
        layout.operator("file.bookmark_move", icon='TRIA_UP_BAR',
                        text="Move to Top").direction = 'TOP'
        layout.operator("file.bookmark_move", icon='TRIA_DOWN_BAR',
                        text="Move to Bottom").direction = 'BOTTOM'


class FILEBROWSER_PT_bookmarks_favorites(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_category = "Bookmarks"
    bl_label = "Favorites"

    @classmethod
    def poll(cls, context):
        if len(context.area.spaces) > 1:
            return False
        return panel_poll_is_upper_region(context.region)

    def draw(self, context):
        layout = self.layout
        space = context.space_data

        if space.bookmarks:
            row = layout.row()
            num_rows = len(space.bookmarks)
            row.template_list("FILEBROWSER_UL_dir", "bookmarks", space, "bookmarks",
                              space, "bookmarks_active", item_dyntip_propname="path",
                              rows=(2 if num_rows < 2 else 4), maxrows=10)

            col = row.column(align=True)
            col.operator("file.bookmark_add", icon='ADD', text="")
            col.operator("file.bookmark_delete", icon='REMOVE', text="")
            col.menu("FILEBROWSER_MT_bookmarks_context_menu",
                     icon='DOWNARROW_HLT', text="")

            if num_rows > 1:
                col.separator()
                col.operator("file.bookmark_move", icon='TRIA_UP',
                             text="").direction = 'UP'
                col.operator("file.bookmark_move", icon='TRIA_DOWN',
                             text="").direction = 'DOWN'
        else:
            layout.operator("file.bookmark_add", icon='ADD')


class FILEBROWSER_PT_bookmarks_recents(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_category = "Bookmarks"
    bl_label = "Recents"

    @classmethod
    def poll(cls, context):
        if len(context.area.spaces) > 1:
            return False
        return not context.preferences.filepaths.hide_recent_locations and panel_poll_is_upper_region(context.region)

    def draw(self, context):
        layout = self.layout
        space = context.space_data

        if space.recent_folders:
            row = layout.row()
            row.template_list("FILEBROWSER_UL_dir", "recent_folders", space, "recent_folders",
                              space, "recent_folders_active", item_dyntip_propname="path", rows=1, maxrows=10)

            col = row.column(align=True)
            col.operator("file.reset_recent", icon='X', text="")


class FILEBROWSER_PT_advanced_filter(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_category = "Filter"
    bl_label = "Advanced Filter"

    @classmethod
    def poll(cls, context):
        if len(context.area.spaces) > 1:
            return False
        # only useful in append/link (library) context currently...
        return context.space_data.params.use_library_browsing and panel_poll_is_upper_region(context.region)

    def draw(self, context):
        layout = self.layout
        space = context.space_data
        params = space.params

        if params and params.use_library_browsing:
            layout.prop(params, "use_filter_blendid")
            if params.use_filter_blendid:
                layout.separator()
                col = layout.column()
                col.prop(params, "filter_id")


class FILEBROWSER_PT_directory_path(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'UI'
    bl_label = "Directory Path"
    bl_category = "Attributes"
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        if len(context.area.spaces) > 1:
            return False
        return True

    def is_header_visible(self, context):
        for region in context.area.regions:
            if region.type == 'HEADER' and region.height <= 1:
                return False

        return True

    def is_option_region_visible(self, context, space):
        if not space.active_operator:
            return False

        for region in context.area.regions:
            if region.type == 'TOOL_PROPS' and region.width <= 1:
                return False

        return True

    def draw(self, context):
        layout = self.layout
        space = context.space_data
        if space.type != 'FILE_BROWSER':
            return
        params = space.params

        layout.scale_x = 1.3
        layout.scale_y = 1.3

        row = layout.row()
        flow = row.grid_flow(row_major=True, columns=0,
                             even_columns=False, even_rows=False, align=False)

        subrow = flow.row()

        subsubrow = subrow.row(align=True)
        subsubrow.operator("file.previous", text="", icon='BACK')
        subsubrow.operator("file.next", text="", icon='FORWARD')
        subsubrow.operator("file.parent", text="", icon='FILE_PARENT')
        subsubrow.operator("file.refresh", text="", icon='FILE_REFRESH')

        subsubrow = subrow.row()
        subsubrow.operator_context = 'EXEC_DEFAULT'
        subsubrow.operator("file.directory_new", icon='NEWFOLDER', text="")

        subrow.template_file_select_path(params)

        subrow = flow.row()

        subsubrow = subrow.row()
        subsubrow.scale_x = 0.6
        subsubrow.prop(params, "filter_search", text="", icon='VIEWZOOM')

        # Uses prop_with_popover() as popover() only adds the triangle icon in headers.
        subrow.prop_with_popover(
            params,
            "display_type",
            panel="FILEBROWSER_PT_display",
            text="",
            icon_only=True,
        )
        subrow.prop_with_popover(
            params,
            "display_type",
            panel="FILEBROWSER_PT_filter",
            text="",
            icon='FILTER',
            icon_only=True,
        )

        if space.active_operator:
            subrow.operator(
                "screen.region_toggle",
                text="",
                icon='PREFERENCES',
                depress=self.is_option_region_visible(context, space)
            ).region_type = 'TOOL_PROPS'


class FILEBROWSER_MT_view(Menu):
    bl_label = "View"

    def draw(self, context):
        layout = self.layout
        st = context.space_data
        params = st.params

        layout.prop(st, "show_region_toolbar", text="Source List")
        layout.prop(st, "show_region_ui", text="File Path")

        layout.separator()

        layout.prop_menu_enum(params, "display_size")
        layout.prop_menu_enum(params, "recursion_level")

        layout.separator()

        layout.menu("INFO_MT_area")


class FILEBROWSER_MT_select(Menu):
    bl_label = "Select"

    def draw(self, _context):
        layout = self.layout

        layout.operator("file.select_all", text="All").action = 'SELECT'
        layout.operator("file.select_all", text="None").action = 'DESELECT'
        layout.operator("file.select_all", text="Inverse").action = 'INVERT'

        layout.separator()

        layout.operator("file.select_box")


class FILEBROWSER_MT_context_menu(Menu):
    bl_label = "Files Context Menu"

    def draw(self, context):
        layout = self.layout
        st = context.space_data
        params = st.params

        layout.operator("file.previous", text="Back")
        layout.operator("file.next", text="Forward")
        layout.operator("file.parent", text="Go to Parent")
        layout.operator("file.refresh", text="Refresh")

        layout.separator()

        layout.operator("file.filenum", text="Increase Number",
                        icon='ADD').increment = 1
        layout.operator("file.filenum", text="Decrease Number",
                        icon='REMOVE').increment = -1

        layout.separator()

        layout.operator("file.rename", text="Rename")
        sub = layout.row()
        sub.operator_context = 'EXEC_DEFAULT'
        sub.operator("file.delete", text="Delete")

        layout.separator()

        sub = layout.row()
        sub.operator_context = 'EXEC_DEFAULT'
        sub.operator("file.directory_new", text="New Folder")
        layout.operator("file.bookmark_add", text="Add Bookmark")

        layout.separator()

        layout.prop_menu_enum(params, "display_type")
        if params.display_type == 'THUMBNAIL':
            layout.prop_menu_enum(params, "display_size")
        layout.prop_menu_enum(params, "recursion_level", text="Recursions")
        layout.prop_menu_enum(params, "sort_method")


@persistent
def add_icon_to_toolbar(context):
    # This is just to draw the logo at the bottom of the screen
    
    script_loc = os.path.dirname(os.path.realpath(__file__))
    img = img_utils.load_image(os.path.join(script_loc, '..', 'icons', 'classy_closets_icon.jpg'))
    icon_aspect_ratio = img.size[1] / img.size[0]
    img.colorspace_settings.name = 'Linear'
    img.gl_load(frame=0)
    tex = img.bindcode

    toolbar = None
    for area in bpy.context.window.screen.areas:
        if area.type == 'FILE_BROWSER':
            for region in area.regions:
                if region.type == 'TOOLS':
                    toolbar = region
    print('adding icon to toolar')

    def draw_logo():
        # for now, I want to lock the max width (and therefore, height) of the image
        if toolbar:
            toolbar_width = min(toolbar.width, 200)
            img_height = toolbar_width * icon_aspect_ratio
            draw_texture_2d(tex, Vector([0, 0]), toolbar_width, img_height)
    try:
        bpy.types.SpaceFileBrowser.draw_handler_remove(draw_logo, 'TOOLS')
    except:
        pass
    bpy.types.SpaceFileBrowser.draw_handler_add(draw_logo, (), 'TOOLS', 'POST_PIXEL')


classes = (
    SN_FILEBROWSER_PT_library_tabs,
    SN_FILEBROWSER_PT_product_lib_header,
    SN_FILEBROWSER_MT_category_menu,
    SN_FILEBROWSER_MT_library_commands,
    SN_FILEBROWSER_PT_library_settings,
    FILEBROWSER_HT_header,
    FILEBROWSER_PT_display,
    FILEBROWSER_PT_filter,
    FILEBROWSER_UL_dir,
    FILEBROWSER_PT_bookmarks_volumes,
    FILEBROWSER_PT_bookmarks_system,
    FILEBROWSER_MT_bookmarks_context_menu,
    FILEBROWSER_PT_bookmarks_favorites,
    FILEBROWSER_PT_bookmarks_recents,
    FILEBROWSER_PT_advanced_filter,
    FILEBROWSER_PT_directory_path,
    FILEBROWSER_MT_view,
    FILEBROWSER_MT_select,
    FILEBROWSER_MT_context_menu,
)

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register():
    register_classes()
    # bpy.app.handlers.load_post.append(add_icon_to_toolbar)


def unregister():
    unregister_classes()
