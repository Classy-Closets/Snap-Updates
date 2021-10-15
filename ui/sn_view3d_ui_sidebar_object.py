import bpy
from bpy.types import Panel

from snap import sn_utils


class SN_VIEW3D_PT_object_prompts(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Dev"
    bl_label = "Prompts"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        if context.object:
            return context.preferences.addons["snap"].preferences.debug_mode
        else:
            return False

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='LINENUMBERS_ON')

    def draw(self, context):
        layout = self.layout
        obj = context.object
        obj.snap.draw_prompts(layout)


class SN_VIEW3D_PT_object_material_pointers(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Dev"
    bl_label = "Material Pointers"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        if context.object:
            return context.preferences.addons["snap"].preferences.debug_mode
        else:
            return False

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='SHADING_TEXTURE')

    def draw(self, context):
        layout = self.layout
        obj = context.object
        slot = None
        spec_group = bpy.context.scene.snap.spec_groups[obj.snap.spec_group_index]

        layout.prop(obj.snap, 'type_mesh')

        if obj.snap.type_mesh == 'CUTPART':
            row = layout.row(align=True)
            row.prop_search(obj.snap, "cutpart_name", spec_group, "cutparts", icon='MOD_UVPROJECT', text="")
            row = layout.row(align=True)
            row.prop_search(obj.snap, "edgepart_name", spec_group, "edgeparts", icon='EDGESEL', text="")
            row = layout.row(align=True)
            row.label(text='Material Name: ' + sn_utils.get_material_name(obj))
            row = layout.row(align=True)
            row.label(text='Edge Material Name: ' + obj.snap.edgeband_material_name)
            row = layout.row(align=True)
            if obj.snap.edge_w1 != "":
                row.label(text='Edge W1 Name: ' + obj.snap.edge_w1 + " - " + obj.snap.edgeband_material_name_w1)
            if obj.snap.edge_w2 != "":
                row.label(text='Edge W2 Name: ' + obj.snap.edge_w2 + " - " + obj.snap.edgeband_material_name_w2)
            row = layout.row(align=True)
            if obj.snap.edge_l1 != "":
                row.label(text='Edge L1 Name: ' + obj.snap.edge_l1 + " - " + obj.snap.edgeband_material_name_l1)
            if obj.snap.edge_l2 != "":
                row.label(text='Edge L2 Name: ' + obj.snap.edge_l2 + " - " + obj.snap.edgeband_material_name_l2)        

        if len(obj.material_slots) >= obj.active_material_index + 1:
            slot = obj.material_slots[obj.active_material_index]

        is_sortable = len(obj.material_slots) > 1
        rows = 3
        if (is_sortable):
            rows = 5

        row = layout.row()
        row.label(text='Material Slots:')
        row = layout.row()

        if obj.type == 'GPENCIL':
            row.template_list("GPENCIL_UL_matslots",
                              "",
                              obj,
                              "material_slots",
                              obj,
                              "active_material_index",
                              rows=rows)
        else:
            row.template_list("MATERIAL_UL_matslots",
                              "",
                              obj,
                              "material_slots",
                              obj,
                              "active_material_index", rows=rows)

        col = row.column(align=True)
        col.operator("sn_material.add_material_slot", icon='ADD', text="").object_name = obj.name
        col.operator("object.material_slot_remove", icon='REMOVE', text="")

        col.separator()

        col.menu("MATERIAL_MT_context_menu", icon='DOWNARROW_HLT', text="")

        if is_sortable:
            col.separator()

            col.operator("object.material_slot_move", icon='TRIA_UP', text="").direction = 'UP'
            col.operator("object.material_slot_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

        if slot:
            row = layout.row()
            if len(obj.snap.material_slots) >= obj.active_material_index + 1:
                pointer_slot = obj.snap.material_slots[obj.active_material_index]
                row.prop(pointer_slot, 'name')
                row = layout.row()
                row.prop(pointer_slot, 'pointer_name')
            else:
                row.operator('sn_material.add_material_pointers').object_name = obj.name

        if obj.mode == 'EDIT':
            row = layout.row(align=True)
            row.operator("object.material_slot_assign", text="Assign")
            row.operator("object.material_slot_select", text="Select")
            row.operator("object.material_slot_deselect", text="Deselect")


class SN_VIEW3D_PT_object_drivers(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Dev"
    bl_label = "Drivers"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        if context.object:
            return context.preferences.addons["snap"].preferences.debug_mode
        else:
            return False

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='AUTO')

    def draw(self, context):
        layout = self.layout
        obj = context.object
        if obj:
            drivers = sn_utils.get_drivers(obj)

            if len(drivers) == 0:
                layout.label(text="No Drivers Found on Object")

            for driver in drivers:
                sn_utils.draw_driver(layout, obj, driver)


classes = (
    SN_VIEW3D_PT_object_prompts,
    SN_VIEW3D_PT_object_drivers,
    SN_VIEW3D_PT_object_material_pointers
)

register, unregister = bpy.utils.register_classes_factory(classes)
