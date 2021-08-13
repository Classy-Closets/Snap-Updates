import bpy
from bpy.types import Panel

from snap import sn_types, sn_utils


def draw_shelf_interface(layout, shelf):
    is_lock_shelf = shelf.get_prompt("Is Locked Shelf")
    is_forced_locked_shelf = shelf.get_prompt("Is Forced Locked Shelf")
    if is_forced_locked_shelf:
        if not is_forced_locked_shelf.get_value():
            if is_lock_shelf:
                box = layout.box()
                is_lock_shelf.draw(box)
        else:
            box = layout.box()
            box.label("Is Forced Locked Shelf")
    else:
        if is_lock_shelf:
            box = layout.box()
            is_lock_shelf.draw(box)


def draw_backing_mats(layout, back):
    props = back.obj_bp.sn_closets

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


class SNAP_PT_closet_options(Panel):
    bl_label = "Closet Options"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 3

    props = None

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='PREFERENCES')

    def draw(self, context):
        self.props = bpy.context.scene.sn_closets
        self.props.draw(self.layout)


class SNAP_PT_Closet_Properties(Panel):
    bl_label = "Closet Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_context = "objectmode"
    bl_order = 1

    props = None

    def draw_header(self, context):
        layout = self.layout

    def draw_product_props(self, layout, obj_product_bp):
        product = sn_types.Assembly(obj_product_bp)
        row = layout.row(align=True)
        row.label(text="Product: " + product.obj_bp.snap.name_object, icon='OUTLINER_OB_LATTICE')
        row = layout.row(align=True)
        row.operator(
            "sn_closets.copy_product", text="Copy Product", icon='PASTEDOWN')
        row.operator(
            'sn_closets.delete_closet', text="Delete Product", icon='X')

    def draw_insert_props(self, layout, obj_insert_bp):
        insert = sn_types.Assembly(obj_insert_bp)
        row = layout.row(align=True)
        row.label(text="Insert: " + insert.obj_bp.snap.name_object, icon='STICKY_UVS_LOC')
        row = layout.row(align=True)
        row.operator("sn_closets.copy_insert", text="Copy Insert", icon='PASTEDOWN')
        row.operator('sn_closets.delete_closet_insert', text="Delete Insert", icon='X')

    def draw_assembly_props(self, layout, obj_assembly_bp):
        assembly = sn_types.Assembly(obj_assembly_bp)
        row = layout.row(align=True)
        row.label(text="Part: " + assembly.obj_bp.snap.name_object, icon='OUTLINER_DATA_LATTICE')
        if assembly.obj_bp.get("ALLOW_PART_DELETE"):
            row = layout.row()
            row.operator(
                'sn_closets.delete_part',
                text="Delete Part - {}".format(assembly.obj_bp.snap.name_object),
                icon='X')
        draw_shelf_interface(layout, assembly)
        draw_backing_mats(layout, assembly)

    def draw(self, context):
        layout = self.layout
        obj_product_bp = sn_utils.get_bp(context.object, 'PRODUCT')
        obj_insert_bp = sn_utils.get_bp(context.object, 'INSERT')
        obj_assembly_bp = sn_utils.get_assembly_bp(context.object)

        col = layout.column(align=True)
        box = col.box()
        if obj_product_bp:
            self.draw_product_props(box, obj_product_bp)
        else:
            box.label(text="No Product Selected", icon='OUTLINER_DATA_LATTICE')
        box = col.box()
        if obj_insert_bp:
            self.draw_insert_props(box, obj_insert_bp)
        else:
            box.label(text="No Insert Selected", icon='STICKY_UVS_LOC')
        box = col.box()
        if obj_assembly_bp:
            self.draw_assembly_props(box, obj_assembly_bp)
        else:
            box.label(text="No Part Selected", icon='OUTLINER_DATA_LATTICE')


classes = (
    SNAP_PT_closet_options,
    SNAP_PT_Closet_Properties
)

register, unregister = bpy.utils.register_classes_factory(classes)
