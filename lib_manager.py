import bpy
from bpy.types import Header, Menu, Operator, UIList, PropertyGroup
from bpy.props import (
    StringProperty,
    BoolProperty,
    IntProperty,
    FloatProperty,
    FloatVectorProperty,
    BoolVectorProperty,
    PointerProperty,
    EnumProperty,
    CollectionProperty
    )
import os
import subprocess
import sys
import snap_db
import inspect
from mv import utils, unit


THUMBNAIL_FILE_NAME = "thumbnail.blend"


def get_thumbnail_path():
    return os.path.join(os.path.dirname(bpy.app.binary_path),THUMBNAIL_FILE_NAME)


class List_Library_Item(PropertyGroup):
    """ Class to put products, inserts, and parts in a list view
        Used to show all library items
    """
    bp_name = StringProperty(name='BP Name')
    class_name = StringProperty(name='Class Name')
    library_name = StringProperty(name='Library Name')
    category_name = StringProperty(name='Category Name')
    selected = BoolProperty(name="Selected")
    has_thumbnail = BoolProperty(name="Has Thumbnail")
    has_file = BoolProperty(name="Has File")

bpy.utils.register_class(List_Library_Item)


class List_Library(PropertyGroup):
    package_name = StringProperty(name="Package Name")
    module_name = StringProperty(name="Module Name")
    lib_path = StringProperty(name="Library Path")
    items = CollectionProperty(name="Items",type=List_Library_Item)
    index = IntProperty(name="Index")

bpy.utils.register_class(List_Library)


# class WM_PROPS(PropertyGroup):

#     library_types = EnumProperty(
#         name="SNaP Library Types",
#         items=[
#             ('PRODUCT',"Product","Product"),
#             ('INSERT',"Insert","Insert")
#             ],
#         default = 'PRODUCT'
#         )  
    
#     lib_products = CollectionProperty(name="Library Products", type=List_Library)
#     lib_product_index = IntProperty(name="Library Product Index", default=0)
#     lib_inserts = CollectionProperty(name="Library Inserts", type=List_Library)
#     lib_insert_index = IntProperty(name="Library Insert Index", default=0)
#     current_item = IntProperty(name="Current Item", default = 0)
#     total_items = IntProperty(name="Total Items", default = 0)   
                
# bpy.utils.register_class(WM_PROPS)


class OPS_load_library_modules(Operator):
    """ This will load all of the products from the products module.
    """
    bl_idname = "snap.load_library_modules"
    bl_label = "Load Library Modules"
    bl_description = "This will load the available product library modules"
    bl_options = {'UNDO'}
    
    external_lib_only = bpy.props.BoolProperty(name="External Libraries Only", default=False)

    def get_library(self,libraries,library_name,module_name,package_name,path):
        if library_name in libraries:
            lib = libraries[library_name]
        else:
            lib = libraries.add()
            lib.name = library_name
            lib.module_name = module_name
            lib.package_name = package_name
            lib.lib_path = path
        return lib

    def execute(self, context):
        from importlib import import_module
        wm = context.window_manager.cabinetlib

        for library in wm.lib_products:
            wm.lib_products.remove(0)
        
        for library in wm.lib_inserts:
            wm.lib_inserts.remove(0)        
        
        packages = utils.get_library_packages(context, only_external=True if self.external_lib_only else False)
        
        for package in packages:
            pkg = import_module(package)
            for mod_name, mod in inspect.getmembers(pkg):
                for name, obj in inspect.getmembers(mod):
                    if inspect.isclass(obj) and "PRODUCT_" in name:
                        product = obj()
                        if product.assembly_name == "":
                            product.assembly_name = name.replace("PRODUCT_","").replace("_"," ")
                        path = os.path.join(os.path.dirname(pkg.__file__),"products",product.library_name)
                        lib = self.get_library(wm.lib_products,product.library_name,mod_name,package,path)
                        item = lib.items.add()
                        item.name = product.assembly_name
                        item.class_name = name
                        item.library_name = product.library_name
                        item.category_name = product.category_name
                        item.lib_path = os.path.join(os.path.dirname(pkg.__file__),"products",product.library_name)
                        thumbnail_path = os.path.join(item.lib_path,item.category_name,item.name.strip() + ".png")
                        if os.path.exists(thumbnail_path):
                            item.has_thumbnail = True
                        else:
                            item.has_thumbnail = False
                        file_path = os.path.join(item.lib_path,item.category_name,item.name.strip() + ".blend")
                        if os.path.exists(file_path):
                            item.has_file = True
                        else:
                            item.has_file = False            
                            
                    if inspect.isclass(obj) and "INSERT_" in name:
                        insert = obj()
                        if insert.assembly_name == "":
                            insert.assembly_name = name.replace("INSERT_","").replace("_"," ")
                        path = os.path.join(os.path.dirname(pkg.__file__),"inserts",insert.library_name)
                        lib = self.get_library(wm.lib_inserts,insert.library_name,mod_name,package,path)
                        item = lib.items.add()
                        item.name = insert.assembly_name
                        item.class_name = name
                        item.library_name = insert.library_name
                        item.category_name = insert.category_name
                        item.lib_path = os.path.join(os.path.dirname(pkg.__file__),"inserts",insert.library_name)
                        thumbnail_path = os.path.join(item.lib_path,item.category_name,item.name.strip() + ".png")
                        if os.path.exists(thumbnail_path):
                            item.has_thumbnail = True
                        else:
                            item.has_thumbnail = False
                        file_path = os.path.join(item.lib_path,item.category_name,item.name.strip() + ".blend")
                        if os.path.exists(file_path):
                            item.has_file = True
                        else:
                            item.has_file = False       
        return {'FINISHED'}


class OPS_brd_library_items(Operator):
    """ Library management tools.
    """
    bl_idname = "snap.brd_library_items"
    bl_label = "Build Render Draw Library Items"
    bl_description = "This operator will build render or draw every selected item in the library"
    bl_options = {'UNDO'}
    
    operation_type = EnumProperty(name="Operation Type",items=[('BUILD','Build','Build'),
                                                               ('RENDER','Render','Render'),
                                                               ('DRAW','Draw','Draw')])
    
    library_type = EnumProperty(name="Library Type",items=[('PRODUCT','Product','Product'),
                                                           ('INSERT','Insert','Insert')])
    
    _timer = None
    
    item_list = []
    current_product = 0
    package_name = ""
    module_name = ""
    library_path = ""
    
    placement = 0
    
    def __del__(self):
        bpy.context.window.cursor_set('DEFAULT')
        bpy.context.area.header_text_set()
    
    def invoke(self, context, event):
        wm = context.window_manager
        props = wm.cabinetlib
        
        if self.library_type == 'PRODUCT':
            collection = props.lib_products[props.lib_product_index].items
            self.module_name = props.lib_products[props.lib_product_index].module_name
            self.package_name = props.lib_products[props.lib_product_index].package_name
            self.library_path = props.lib_products[props.lib_product_index].lib_path
            
        if self.library_type == 'INSERT':
            collection = props.lib_inserts[props.lib_insert_index].items
            self.module_name = props.lib_inserts[props.lib_insert_index].module_name
            self.package_name = props.lib_inserts[props.lib_insert_index].package_name
            self.library_path = props.lib_inserts[props.lib_insert_index].lib_path
            
        self.item_list = []
        for item in collection:
            if item.selected:
                self.item_list.append(item)
                
        props.total_items = len(self.item_list)
        
        self._timer = wm.event_timer_add(0.1, context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        context.window.cursor_set('WAIT')
        context.area.tag_redraw()
        progress = context.window_manager.cabinetlib
        header_text = "Processing Item 1 of " + str(progress.total_items)
        context.area.header_text_set(text=header_text)
        
        self.mouse_loc = (event.mouse_region_x,event.mouse_region_y)
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            return self.cancel(context)
        
        if event.type == 'TIMER':
            if progress.current_item + 1 <= len(self.item_list):
                if self.operation_type == 'RENDER':
                    if self.library_type == 'INSERT':
                        self.render_insert(self.item_list[progress.current_item].class_name)
                    else:
                        self.render_product(self.item_list[progress.current_item].class_name)
                if self.operation_type == 'BUILD':
                    self.build_product(self.item_list[progress.current_item].class_name)
                if self.operation_type == 'DRAW':
                    self.draw_product(self.item_list[progress.current_item].class_name)
                progress.current_item += 1
                if progress.current_item + 1 <= len(self.item_list):
                    header_text = "Processing Item " + str(progress.current_item + 1) + " of " + str(progress.total_items)
                context.area.header_text_set(text=header_text)
            else:
                return self.cancel(context)
        return {'PASS_THROUGH'}
    
    def render_product(self,class_name):
        filepath = get_thumbnail_path()
        script = os.path.join(bpy.app.tempdir,'thumbnail.py')
        script_file = open(script,'w')
        script_file.write("import bpy\n")
        script_file.write("import os\n")
        script_file.write("from mv import utils\n")
        script_file.write("bpy.ops.fd_material.reload_spec_group_from_library_modules()\n")
        script_file.write("pkg = __import__('" + self.package_name + "')\n")
        script_file.write("item = eval('pkg." + self.module_name + "." + class_name + "()')" + "\n")
        script_file.write("item.draw()\n")
        script_file.write("item.update()\n")
        script_file.write("file_name = item.assembly_name if item.assembly_name != '' else utils.get_product_class_name('" + class_name + "')\n")
        script_file.write("tn_path = os.path.join(r'" + self.library_path + "',item.category_name,file_name)\n")
        script_file.write('utils.render_assembly(item,tn_path)\n')
        script_file.close()
        subprocess.call(bpy.app.binary_path + ' "' + filepath + '" -b --python "' + script + '"')

    def render_insert(self,class_name):
        filepath = get_thumbnail_path()
        script = os.path.join(bpy.app.tempdir,'thumbnail.py')
        script_file = open(script,'w')
        script_file.write("import bpy\n")
        script_file.write("import os\n")
        script_file.write("from mv import utils\n")
        script_file.write("bpy.ops.fd_material.reload_spec_group_from_library_modules()\n")
        script_file.write("pkg = __import__('" + self.package_name + "')\n")
        script_file.write("item = eval('pkg." + self.module_name + "." + class_name + "()')" + "\n")
        script_file.write("item.draw()\n")
        script_file.write("item.update()\n")
        script_file.write("file_name = item.assembly_name if item.assembly_name != '' else utils.get_insert_class_name('" + class_name + "')\n")
        script_file.write("tn_path = os.path.join(r'" + self.library_path + "',item.category_name,file_name)\n")
        script_file.write('utils.render_assembly(item,tn_path)\n')
        script_file.close()
        subprocess.call(bpy.app.binary_path + ' "' + filepath + '" -b --python "' + script + '"')

    def build_product(self,class_name):
        script = os.path.join(bpy.app.tempdir,'building.py')
        script_file = open(script,'w')
        script_file.write("from snap_db import utils as snap_utils\n")
        script_file.write("from mv import utils\n")
        script_file.write("pkg = __import__('" + self.package_name + "')\n")
        script_file.write("item = eval('pkg." + self.module_name + "." + class_name + "()')" + "\n")
        script_file.write("item.draw()\n")
        script_file.write("item.update()\n")
        script_file.write("if item.assembly_name == '':\n")
        script_file.write("    item.assembly_name = utils.get_product_class_name('" + class_name + "')\n")
        script_file.write('snap_utils.save_assembly(item,r"' + self.library_path + '"' + ')\n')
        script_file.close()
        subprocess.call(bpy.app.binary_path + ' -b --python "' + script + '"')    
    
    def draw_product(self,class_name):
        pkg = __import__(self.package_name)
        item = eval("pkg." + self.module_name + "." + class_name + "()")
        item.draw()
        item.update()
        utils.init_objects(item.obj_bp)
        item.obj_bp.location.x = self.placement
        self.placement += item.obj_x.location.x + unit.inch(10)
        
    def cancel(self, context):
        progress = context.window_manager.cabinetlib
        progress.current_item = 0
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        return {'FINISHED'}

class PANEL_Library_Management(bpy.types.Panel):    
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "Library Manager"
    bl_options = {'DEFAULT_CLOSED'}
    bl_category = "SNaP"
    
    @classmethod
    def poll(cls, context):
        prefs = context.user_preferences.addons["snap_db"].preferences

        if prefs:
            return prefs.enable_lib_manager
        else:
            return False
    
    def draw_header(self, context):
        layout = self.layout
        layout.label('',icon='EXTERNAL_DATA')
    
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        wm_props = wm.cabinetlib

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
                row.menu('MENU_Product_Library_Options',text="",icon='DOWNARROW_HLT')
                col.template_list("LIST_lib", " ", wm_props, "lib_products", wm_props, "lib_product_index")
                lib = wm_props.lib_products[wm_props.lib_product_index]
                col.template_list("LIST_lib_productlist", " ", lib, "items", lib, "index")
                
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
                row.menu('MENU_Insert_Library_Options',text="",icon='DOWNARROW_HLT')
                col.template_list("LIST_lib", " ", wm_props, "lib_inserts", wm_props, "lib_insert_index")
                lib = wm_props.lib_inserts[wm_props.lib_insert_index]
                col.template_list("LIST_lib_insertlist", " ", lib, "items", lib, "index")        


def register():
    #bpy.types.WindowManager.lib_manager = PointerProperty(type=WM_PROPS)
    bpy.utils.register_class(OPS_load_library_modules)
    bpy.utils.register_class(OPS_brd_library_items)
    bpy.utils.register_class(PANEL_Library_Management)


def unregister():
    bpy.utils.unregister_class(OPS_load_library_modules)
    bpy.utils.unregister_class(OPS_brd_library_items)
    bpy.utils.unregister_class(PANEL_Library_Management)


    
