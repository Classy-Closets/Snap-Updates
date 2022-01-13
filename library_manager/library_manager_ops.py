import os
import subprocess
import inspect
import time

import bpy
from bpy.types import Operator
from bpy.props import (
    BoolProperty,
    EnumProperty,
)

from .. import sn_utils, sn_unit, sn_handlers


THUMBNAIL_FILE_NAME = "thumbnail.blend"


def get_thumbnail_path():
    return os.path.join(os.path.dirname(__file__), THUMBNAIL_FILE_NAME)


class SNAP_OT_load_library_modules(Operator):
    """ This will load all of the products from the products module.
    """
    bl_idname = "snap.load_library_modules"
    bl_label = "Load Library Modules"
    bl_description = "This will load the available product library modules"
    bl_options = {'UNDO'}

    external_lib_only: BoolProperty(name="External Libraries Only", default=False)

    def get_library(self, libraries, library_name, module_name, package_name, path):
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
        wm = context.window_manager.snap
        scene_props = context.scene.snap

        for library in wm.lib_products:
            wm.lib_products.remove(0)

        for library in wm.lib_inserts:
            wm.lib_inserts.remove(0)

        packages = sn_utils.get_library_packages(context, only_external=True if self.external_lib_only else False)

        for package in packages:
            pkg = import_module(package)
            for mod_name, mod in inspect.getmembers(pkg):
                for name, obj in inspect.getmembers(mod):
                    if inspect.isclass(obj) and "PRODUCT_" in name:
                        product = obj()
                        if product.assembly_name == "":
                            product.assembly_name = name.replace("PRODUCT_", "").replace("_", " ")
                        path = os.path.join(os.path.dirname(pkg.__file__), "products")
                        lib = self.get_library(wm.lib_products, product.library_name, mod_name, package, path)
                        item = lib.items.add()
                        item.name = product.assembly_name
                        item.class_name = name
                        item.library_name = product.library_name
                        item.category_name = product.category_name
                        item.lib_path = os.path.join(os.path.dirname(pkg.__file__), "products")
                        thumbnail_path = os.path.join(item.lib_path, item.category_name, item.name.strip() + ".png")
                        if os.path.exists(thumbnail_path):
                            item.has_thumbnail = True
                        else:
                            item.has_thumbnail = False
                        file_path = os.path.join(item.lib_path, item.category_name, item.name.strip() + ".blend")
                        if os.path.exists(file_path):
                            item.has_file = True
                        else:
                            item.has_file = False

                    if inspect.isclass(obj) and "INSERT_" in name:
                        insert = obj()
                        if insert.assembly_name == "":
                            insert.assembly_name = name.replace("INSERT_", "").replace("_", " ")
                        path = os.path.join(os.path.dirname(pkg.__file__), "inserts", insert.library_name)
                        lib = self.get_library(wm.lib_inserts, insert.library_name, mod_name, package, path)
                        item = lib.items.add()
                        item.name = insert.assembly_name
                        item.class_name = name
                        item.library_name = insert.library_name
                        item.category_name = insert.category_name
                        item.lib_path = os.path.join(os.path.dirname(pkg.__file__), "inserts", insert.library_name)
                        thumbnail_path = os.path.join(item.lib_path, item.category_name, item.name.strip() + ".png")
                        if os.path.exists(thumbnail_path):
                            item.has_thumbnail = True
                        else:
                            item.has_thumbnail = False
                        file_path = os.path.join(item.lib_path, item.category_name, item.name.strip() + ".blend")
                        if os.path.exists(file_path):
                            item.has_file = True
                        else:
                            item.has_file = False

        try:
            active_library = wm.libraries[scene_props.active_library_name]
            library_name = active_library.name
        except KeyError as error:
            print(error)
            print("Library: {} not found.".format(scene_props.active_library_name))
            print("Reloading SNaP Libraries...")
            active_library = wm.libraries[0]
            library_name = active_library.name
            scene_props.active_library_name = library_name

                            
        return {'FINISHED'}


class SNAP_OT_brd_library_items(Operator):
    """ Library management tools.
    """
    bl_idname = "snap.brd_library_items"
    bl_label = "Build Render Draw Library Items"
    bl_description = "This operator will build render or draw every selected item in the library"
    bl_options = {'UNDO'}
    
    operation_type: EnumProperty(name="Operation Type",items=[('BUILD','Build','Build'),
                                                               ('RENDER','Render','Render'),
                                                               ('DRAW','Draw','Draw')])
    
    library_type: EnumProperty(name="Library Type",items=[('PRODUCT','Product','Product'),
                                                           ('INSERT','Insert','Insert')])
    
    _timer = None
    
    item_list = []
    current_product = 0
    package_name = ""
    module_name = ""
    library_path = ""
    
    placement = 0
    
    # def __del__(self):
    #     bpy.context.window.cursor_set('DEFAULT')
    #     bpy.context.area.header_text_set()
    
    def invoke(self, context, event):
        wm = context.window_manager
        props = wm.snap
        
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
        
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        context.window.cursor_set('WAIT')
        context.area.tag_redraw()
        progress = context.window_manager.snap
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
        script_file.write("from snap import sn_utils\n")
        script_file.write("bpy.ops.sn_material.reload_spec_group_from_library_modules()\n")
        script_file.write("def select_objects():\n")
        script_file.write("    for obj in bpy.data.objects:\n")
        script_file.write("        if obj.type == 'MESH':\n")
        script_file.write("            obj.select_set(True)\n")        
        script_file.write("pkg = __import__('" + self.package_name + "')\n")
        script_file.write("item = eval('pkg." + self.module_name + "." + class_name + "()')" + "\n")
        script_file.write("if hasattr(item, 'pre_draw'):\n")
        script_file.write("    item.pre_draw()\n")        
        script_file.write("item.draw()\n")
        script_file.write("item.update()\n")
        script_file.write("file_name = item.assembly_name if item.assembly_name != '' else sn_utils.get_product_class_name('" + class_name + "')\n")
        script_file.write("tn_path = os.path.join(r'" + self.library_path + "',item.category_name,file_name)\n")
        script_file.write("bpy.ops.object.select_all(action='DESELECT')\n")
        script_file.write("select_objects()\n")
        script_file.write("bpy.ops.view3d.camera_to_view_selected()\n")

        script_file.write("for mat in bpy.data.materials:\n")
        script_file.write("    bpy.data.materials.remove(mat,do_unlink=True)\n")

        #RENDER
        script_file.write("bpy.context.scene.camera.data.lens = 40\n")
        script_file.write("bpy.context.scene.camera.location.z += .05\n")
        script_file.write("render = bpy.context.scene.render\n")
        script_file.write("render.resolution_x = 540\n")
        script_file.write("render.resolution_y = 540\n")
        script_file.write("render.engine = 'BLENDER_EEVEE'\n")
        script_file.write("bpy.context.scene.eevee.use_gtao = True\n")
        script_file.write("bpy.context.scene.eevee.use_ssr = True\n")
        script_file.write("render.film_transparent = True\n")
        script_file.write("render.use_file_extension = True\n")
        script_file.write("render.filepath = tn_path\n")
        script_file.write("bpy.ops.render.render(write_still=True)\n")                
        script_file.close()
        subprocess.call(bpy.app.binary_path + ' "' + filepath + '" -b --python "' + script + '"')

    def render_insert(self, class_name):
        filepath = get_thumbnail_path()
        script = os.path.join(bpy.app.tempdir, 'thumbnail.py')
        script_file = open(script, 'w')
        script_file.write("import bpy\n")
        script_file.write("import os\n")
        script_file.write("from snap import sn_utils\n")
        script_file.write("bpy.ops.sn_material.reload_spec_group_from_library_modules()\n")
        script_file.write("pkg = __import__('" + self.package_name + "')\n")
        script_file.write("item = eval('pkg." + self.module_name + "." + class_name + "()')" + "\n")
        script_file.write("if hasattr(item, 'pre_draw'):\n")
        script_file.write("    item.pre_draw()\n")
        script_file.write("item.draw()\n")
        script_file.write("item.update()\n")
        script_file.write("file_name = item.assembly_name if item.assembly_name != '' else sn_utils.get_insert_class_name('" + class_name + "')\n")
        script_file.write("tn_path = os.path.join(r'" + self.library_path + "',item.category_name,file_name)\n")
        script_file.write('sn_utils.render_assembly(item,tn_path)\n')
        script_file.close()
        subprocess.call(bpy.app.binary_path + ' "' + filepath + '" -b --python "' + script + '"')

    def build_product(self, class_name):
        script = os.path.join(bpy.app.tempdir, 'building.py')
        script_file = open(script, 'w')
        script_file.write("from snap import sn_utils\n")
        script_file.write("pkg = __import__('" + self.package_name + "')\n")
        script_file.write("item = eval('pkg." + self.module_name + "." + class_name + "()')" + "\n")
        script_file.write("if hasattr(item, 'pre_draw'):\n")
        script_file.write("    item.pre_draw()\n")
        script_file.write("item.draw()\n")
        script_file.write("item.update()\n")
        script_file.write("if item.assembly_name == '':\n")
        script_file.write("    item.assembly_name = sn_utils.get_product_class_name('" + class_name + "')\n")
        script_file.write('sn_utils.save_assembly(item,r"' + self.library_path + '"' + ')\n')
        script_file.close()
        subprocess.call(bpy.app.binary_path + ' -b --python "' + script + '"')

    def update_closet_id_props(obj, parent_obj):
        if "ID_PROMPT" in parent_obj:
            obj["ID_PROMPT"] = parent_obj["ID_PROMPT"]

    def set_child_properties(self, obj, id_prompt=None):
        if "IS_DRAWERS_BP" in obj and obj["IS_DRAWERS_BP"]:
            assembly = sn_types.Assembly(obj)
            calculator = assembly.get_calculator('Front Height Calculator')
            if calculator:
                calculator.calculate()
                self.calculators.append(calculator)

        if "IS_VERTICAL_SPLITTER_BP" in obj and obj["IS_VERTICAL_SPLITTER_BP"]:
            assembly = sn_types.Assembly(obj)
            calculator = assembly.get_calculator('Opening Height Calculator')
            if calculator:
                calculator.calculate()
                self.calculators.append(calculator)

        if id_prompt:
            obj["ID_PROMPT"] = id_prompt
        if obj.type == 'EMPTY':
            obj.hide_viewport = True
        if obj.type == 'MESH':
            obj.display_type = 'TEXTURED'

        for child in obj.children:
            self.set_child_properties(child, id_prompt=id_prompt)

    def draw_product(self,class_name):
        start_time = time.perf_counter()
        pkg = __import__(self.package_name)
        item = eval("pkg." + self.module_name + "." + class_name + "()")

        if hasattr(item, 'pre_draw'):
            item.pre_draw()

        item.draw()
        if "ID_PROMPT" in item.obj_bp:
            id_prompt = item.obj_bp["ID_PROMPT"]
        self.set_child_properties(item.obj_bp, id_prompt=id_prompt)
        item.obj_bp.location.x = self.placement
        if item.width:
            item.obj_x.location.x = item.width
        if item.depth:
            item.obj_y.location.y = item.depth
        if item.height:
            item.obj_z.location.z = item.height
        self.placement += item.obj_x.location.x + sn_unit.inch(10)

        print("{} : Draw Time --- {} seconds --- Objects in scene: {} ({} visible)".format(
            item.obj_bp.snap.name_object,
            round(time.perf_counter() - start_time, 8),
            len(bpy.data.objects),
            len([ob for ob in bpy.context.view_layer.objects if ob.visible_get()])))

    def cancel(self, context):
        progress = context.window_manager.snap
        progress.current_item = 0
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        context.window.cursor_set('DEFAULT')
        context.area.header_text_set(None)        
        return {'FINISHED'}


class SNAP_OT_select_all_products(Operator):   
    bl_idname = "snap.select_all_products"
    bl_label = "Select All Products"
    bl_description = "This will select all of the products in the library list"
    
    select_all: BoolProperty(name="Select All", default=True)
    
    @classmethod
    def poll(cls, context):
        wm = context.window_manager.snap
        if len(wm.lib_products) > 0:
            return True
        else:
            return False

    def execute(self,context):
        wm = context.window_manager.snap
        lib = wm.lib_products[wm.lib_product_index]
        for item in lib.items:
            item.selected = self.select_all
        return{'FINISHED'}


class SNAP_OT_select_all_inserts(Operator):   
    bl_idname = "snap.select_all_inserts"
    bl_label = "Select All Inserts"
    bl_description = "This will select all of the inserts in the library list"    
    
    select_all: BoolProperty(name="Select All", default=True)
    
    @classmethod
    def poll(cls, context):
        wm = context.window_manager.snap
        if len(wm.lib_inserts) > 0:
            return True
        else:
            return False

    def execute(self,context):
        wm = context.window_manager.snap
        lib = wm.lib_inserts[wm.lib_insert_index]
        for item in lib.items:
            item.selected = self.select_all
        return{'FINISHED'}


def register():
    bpy.utils.register_class(SNAP_OT_load_library_modules)
    bpy.utils.register_class(SNAP_OT_brd_library_items)
    bpy.utils.register_class(SNAP_OT_select_all_products)
    bpy.utils.register_class(SNAP_OT_select_all_inserts)


def unregister():
    bpy.utils.unregister_class(SNAP_OT_load_library_modules)
    bpy.utils.unregister_class(SNAP_OT_brd_library_items)
    bpy.utils.unregister_class(SNAP_OT_select_all_products)
    bpy.utils.unregister_class(SNAP_OT_select_all_inserts)

