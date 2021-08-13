import os

import bpy
from bpy.types import (
    Panel,
    UIList,
    Menu
)


class SNAP_UL_lib(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=item.name,icon='LATTICE_DATA')


class SNAP_UL_lib_productlist(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=item.name,icon='LATTICE_DATA')
        if not item.has_thumbnail:
            layout.label(text='',icon='RENDER_RESULT')
        if not item.has_file:
            layout.label(text='',icon='FILE_BLEND')
        layout.prop(item,'selected',text="")


class SNAP_UL_lib_insertlist(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=item.name,icon='STICKY_UVS_LOC')
        if not item.has_thumbnail:
            layout.label(text='',icon='RENDER_RESULT')
        if not item.has_file:
            layout.label(text='',icon='FILE_BLEND')
        layout.prop(item,'selected',text="")


class SNAP_MT_Product_Library_Options(Menu):
    bl_label = "Product Library Options"

    def draw(self, context):
        layout = self.layout
        layout.operator("snap.select_all_products",text="Select All",icon='CHECKBOX_HLT').select_all = True
        layout.operator("snap.select_all_products",text="Deselect All",icon='CHECKBOX_DEHLT').select_all = False


class SNAP_MT_Insert_Library_Options(Menu):
    bl_label = "Insert Library Options"

    def draw(self, context):
        layout = self.layout
        layout.operator("snap.select_all_inserts",text="Select All",icon='CHECKBOX_HLT').select_all = True
        layout.operator("snap.select_all_inserts",text="Deselect All",icon='CHECKBOX_DEHLT').select_all = False


class SNAP_PT_Library_Management(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Dev"
    bl_context = "objectmode"
    bl_label = "Library Manager"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        prefs = context.preferences.addons["snap"].preferences
        return prefs.debug_mode

    def draw_header(self, context):
        layout = self.layout
        layout.label(text='', icon='GROUP')
    
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        wm_props = wm.snap

        col = layout.column(align=True)
        box = col.box()
        row = box.row(align=True)
        row.prop_enum(wm_props, "library_types", 'PRODUCT', icon='LATTICE_DATA', text="Products")
        row.prop_enum(wm_props, "library_types", 'INSERT', icon='STICKY_UVS_LOC', text="Inserts")
        
        if wm_props.library_types == 'PRODUCT':
            if len(wm_props.lib_products) < 1:
                box.operator('snap.load_library_modules',text="Load Library Modules",icon='FILE_REFRESH')
            else:
                row = box.row(align=True)
                row.scale_y = 1.3
                row.operator("snap.load_library_modules",text="",icon='FILE_REFRESH')
                props = row.operator('snap.brd_library_items',text="Build",icon='FILE_BLEND')
                props.operation_type = 'BUILD'
                props.library_type = 'PRODUCT'
                props = row.operator('snap.brd_library_items',text="Render",icon='RENDER_RESULT')
                props.operation_type = 'RENDER'
                props.library_type = 'PRODUCT'
                props = row.operator('snap.brd_library_items',text="Draw",icon='GREASEPENCIL')
                props.operation_type = 'DRAW'
                props.library_type = 'PRODUCT'
                row.menu('SNAP_MT_Product_Library_Options',text="",icon='DOWNARROW_HLT')
                col.template_list("SNAP_UL_lib", " ", wm_props, "lib_products", wm_props, "lib_product_index")
                lib = wm_props.lib_products[wm_props.lib_product_index]
                col.template_list("SNAP_UL_lib_productlist", " ", lib, "items", lib, "index")
                
        if wm_props.library_types == 'INSERT':
            if len(wm_props.lib_inserts) < 1:
                box.operator('snap.load_library_modules',text="Load Library Modules",icon='FILE_REFRESH')
            else:
                row = box.row(align=True)
                row.scale_y = 1.3
                row.operator("snap.load_library_modules",text="",icon='FILE_REFRESH')
                props = row.operator('snap.brd_library_items',text="Build",icon='FILE_BLEND')
                props.operation_type = 'BUILD'
                props.library_type = 'INSERT'
                props = row.operator('snap.brd_library_items',text="Render",icon='RENDER_RESULT')
                props.operation_type = 'RENDER'
                props.library_type = 'INSERT'
                props = row.operator('snap.brd_library_items',text="Draw",icon='GREASEPENCIL')
                props.operation_type = 'DRAW'
                props.library_type = 'INSERT'
                row.menu('SNAP_MT_Insert_Library_Options',text="",icon='DOWNARROW_HLT')
                col.template_list("SNAP_UL_lib", " ", wm_props, "lib_inserts", wm_props, "lib_insert_index")
                lib = wm_props.lib_inserts[wm_props.lib_insert_index]
                col.template_list("SNAP_UL_lib_insertlist", " ", lib, "items", lib, "index")        


def register():
    bpy.utils.register_class(SNAP_PT_Library_Management)
    bpy.utils.register_class(SNAP_UL_lib)
    bpy.utils.register_class(SNAP_UL_lib_productlist)
    bpy.utils.register_class(SNAP_UL_lib_insertlist)
    bpy.utils.register_class(SNAP_MT_Product_Library_Options)
    bpy.utils.register_class(SNAP_MT_Insert_Library_Options)


def unregister():
    bpy.utils.unregister_class(SNAP_PT_Library_Management)
    bpy.utils.unregister_class(SNAP_UL_lib)
    bpy.utils.unregister_class(SNAP_UL_lib_productlist)
    bpy.utils.unregister_class(SNAP_UL_lib_insertlist)
    bpy.utils.unregister_class(SNAP_MT_Product_Library_Options)
    bpy.utils.unregister_class(SNAP_MT_Insert_Library_Options)
