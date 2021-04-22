import bpy
from mv import utils, fd_types
from . import mv_closet_defaults as props_closet

def draw_shelf_interface(layout,shelf):
    is_lock_shelf = shelf.get_prompt("Is Locked Shelf")
    is_forced_locked_shelf = shelf.get_prompt("Is Forced Locked Shelf")
    if is_forced_locked_shelf:
        if not is_forced_locked_shelf.value():
            if is_lock_shelf:
                box = layout.box()
                is_lock_shelf.draw_prompt(box)
        else:
            box = layout.box()
            box.label("Is Forced Locked Shelf")
    else:
        if is_lock_shelf:
            box = layout.box()
            is_lock_shelf.draw_prompt(box)

def draw_backing_mats(layout, back):
    props = back.obj_bp.lm_closets

    if props.is_back_bp or props.is_bottom_back_bp or props.is_top_back_bp:
        layout.prop(props, "use_unique_material")

        if props.use_unique_material:
            layout.prop(props, "unique_mat_types", text="Backing Material Type")

            if props.unique_mat_types == 'MELAMINE':
                layout.prop(props, "unique_mat_mel", text="Backing Material Color")
            if props.unique_mat_types == 'TEXTURED_MELAMINE':
                layout.prop(props, "unique_mat_tex_mel", text="Backing Material Color")
            if props.unique_mat_types == 'VENEER':
                layout.prop(props, "unique_mat_veneer", text="Backing Material Color")
            
class PANEL_Closet_Options(bpy.types.Panel):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + "Closet_Options"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "Closet Options"
    bl_category = "SNaP"
    
    props = None
    
    def draw_header(self, context):
        layout = self.layout
        layout.label('',icon='BLANK1')    

    def draw(self, context):
        self.props = props_closet.get_scene_props()
        self.props.draw(self.layout)        
        
class PANEL_Closet_Properties(bpy.types.Panel):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + "Closet_Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"
    bl_label = "Closet Properties"
    
    props = None
    
    @classmethod
    def poll(cls, context):
        if context.object:
            return True
        return False
    
    def draw_header(self, context):
        layout = self.layout
        layout.label('',icon='BLANK1')    

    def draw_product_props(self,layout,obj_product_bp):
        product = fd_types.Assembly(obj_product_bp)
        row = layout.row(align=True)
        row.label("Product: " + product.obj_bp.mv.name_object,icon='OUTLINER_OB_LATTICE')
        row = layout.row(align=True)
        row.operator("fd_assembly.copy_assembly",text="Copy Product",icon='PASTEDOWN').object_name = obj_product_bp.name
        row.operator('fd_assembly.delete_selected_assembly',text="Delete Product",icon='X').object_name = obj_product_bp.name
    
    def draw_insert_props(self,layout,obj_insert_bp):
        insert = fd_types.Assembly(obj_insert_bp)
        row = layout.row(align=True)
        row.label("Insert: " + insert.obj_bp.mv.name_object,icon='STICKY_UVS_LOC')
        row = layout.row(align=True)
        row.operator("fd_assembly.copy_assembly",text="Copy Insert",icon='PASTEDOWN').object_name = obj_insert_bp.name
        row.operator('fd_assembly.delete_selected_assembly',text="Delete Insert",icon='X').object_name = obj_insert_bp.name

    def draw_assembly_props(self,layout,obj_assembly_bp):
        assembly = fd_types.Assembly(obj_assembly_bp)
        row = layout.row(align=True)
        row.label("Part: " + assembly.obj_bp.mv.name_object,icon='OUTLINER_DATA_LATTICE')
        row = layout.row(align=True)
        row.operator("fd_assembly.copy_assembly",text="Copy Part",icon='PASTEDOWN').object_name = obj_assembly_bp.name
        row.operator('fd_assembly.delete_selected_assembly',text="Delete Part",icon='X').object_name = obj_assembly_bp.name        
        draw_shelf_interface(layout, assembly)
        draw_backing_mats(layout, assembly)

    def draw(self, context):
        layout = self.layout
        obj_product_bp = utils.get_bp(context.object,'PRODUCT')
        obj_insert_bp = utils.get_bp(context.object,'INSERT')
        obj_assembly_bp = utils.get_assembly_bp(context.object)
        
        col = layout.column(align=True)
        
        box = col.box()
        if obj_product_bp:
            self.draw_product_props(box, obj_product_bp)
        else:
            box.label("No Product Selected",icon='OUTLINER_DATA_LATTICE')
        
        box = col.box()
        if obj_insert_bp:
            self.draw_insert_props(box, obj_insert_bp)
        else:
            box.label("No Insert Selected",icon='STICKY_UVS_LOC')
        
        box = col.box()
        if obj_assembly_bp:
            self.draw_assembly_props(box, obj_assembly_bp)
        else:
            box.label("No Part Selected",icon='OUTLINER_DATA_LATTICE')

bpy.utils.register_class(PANEL_Closet_Options)
bpy.utils.register_class(PANEL_Closet_Properties)
