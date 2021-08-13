
import bpy
from bpy.types import Panel, UIList

from snap import sn_types, sn_unit

EXPOSED_MATERIAL = ("Closet Materials", "Oxford White")
CHROME_MATERIAL = ("Finished Metals", "Chrome")
GLASS_MATERIAL = ("Glass", "Glass")
MIRROR_MATERIAL = ("Glass", "Mirror")
LUCITE_MATERIAL = ("Glass", "Lucite")
COUNTER_TOP_MATERIAL = ("Closet Materials", "Oxford White")
CORE = ("Wood Core", "PB")
MODERNO_DOOR = ("Closet Materials", "U Cannes")
HANGER_WOOD = ("Wood Finished", "Craft Oak")
BLACK_MATERIAL = ("Finished Metals", "Black Anodized Metal")
NICKEL_MATERIAL = ("Finished Metals", "Matte Nickel")
ALUMINUM_MATERIAL = ("Finished Metals", "Aluminum")
GOLD_MATERIAL = ("Finished Metals", "Matte Gold")
SLATE_MATERIAL = ("Finished Metals", "Gray Anodized Metal")
WHITE = ("Closet Materials", "Oxford White")


class Material_Pointers():

    Closet_Part_Surfaces = sn_types.Material_Pointer(EXPOSED_MATERIAL)
    Closet_Part_Edges = sn_types.Material_Pointer(EXPOSED_MATERIAL)
    Closet_Part_Edges_Secondary = sn_types.Material_Pointer(EXPOSED_MATERIAL)
    Pull_Finish = sn_types.Material_Pointer(CHROME_MATERIAL)
    Rod_Finish = sn_types.Material_Pointer(CHROME_MATERIAL)
    Hanger_Wood = sn_types.Material_Pointer(HANGER_WOOD)
    Door_Surface = sn_types.Material_Pointer(EXPOSED_MATERIAL)
    Custom_Door_Surface = sn_types.Material_Pointer(EXPOSED_MATERIAL)
    Custom_Door_Edge = sn_types.Material_Pointer(EXPOSED_MATERIAL)
    Wood_Door_Surface = sn_types.Material_Pointer(EXPOSED_MATERIAL)
    Moderno_Door = sn_types.Material_Pointer(MODERNO_DOOR)
    Door_Edge = sn_types.Material_Pointer(EXPOSED_MATERIAL)
    Countertop_Surface = sn_types.Material_Pointer(COUNTER_TOP_MATERIAL)
    Drawer_Box_Surface = sn_types.Material_Pointer(EXPOSED_MATERIAL)
    Drawer_Box_Edge = sn_types.Material_Pointer(EXPOSED_MATERIAL)
    Wire_Basket = sn_types.Material_Pointer(CHROME_MATERIAL)
    Glass = sn_types.Material_Pointer(GLASS_MATERIAL)
    Mirror = sn_types.Material_Pointer(MIRROR_MATERIAL)
    Chrome = sn_types.Material_Pointer(CHROME_MATERIAL)
    Black = sn_types.Material_Pointer(BLACK_MATERIAL)
    Nickel = sn_types.Material_Pointer(NICKEL_MATERIAL)
    Gold = sn_types.Material_Pointer(GOLD_MATERIAL)
    Slate = sn_types.Material_Pointer(SLATE_MATERIAL)
    Aluminum = sn_types.Material_Pointer(ALUMINUM_MATERIAL)
    Molding = sn_types.Material_Pointer(EXPOSED_MATERIAL)
    Lucite = sn_types.Material_Pointer(LUCITE_MATERIAL)
    Core = sn_types.Material_Pointer(CORE)
    Entry_Door_Surface = sn_types.Material_Pointer(WHITE)
    Window_Frame_Surface = sn_types.Material_Pointer(WHITE)


class Cutpart_Pointers():

    Panel = sn_types.Cutpart_Pointer(thickness=sn_unit.inch(.75),
                                     core="Closet_Part_Surfaces",
                                     top="Closet_Part_Surfaces",
                                     bottom="Closet_Part_Surfaces")

    Shelf = sn_types.Cutpart_Pointer(thickness=sn_unit.inch(.75),
                                     core="Closet_Part_Surfaces",
                                     top="Closet_Part_Surfaces",
                                     bottom="Closet_Part_Surfaces")

    Cleat = sn_types.Cutpart_Pointer(thickness=sn_unit.inch(.75),
                                     core="Closet_Part_Surfaces",
                                     top="Closet_Part_Surfaces",
                                     bottom="Closet_Part_Surfaces")

    Cover_Cleat = sn_types.Cutpart_Pointer(thickness=sn_unit.inch(.375),
                                           core="Closet_Part_Surfaces",
                                           top="Closet_Part_Surfaces",
                                           bottom="Closet_Part_Surfaces")

    Toe_Kick = sn_types.Cutpart_Pointer(thickness=sn_unit.inch(.75),
                                        core="Closet_Part_Surfaces",
                                        top="Closet_Part_Surfaces",
                                        bottom="Closet_Part_Surfaces")

    Back = sn_types.Cutpart_Pointer(thickness=sn_unit.inch(.25),
                                    core="Closet_Part_Surfaces",
                                    top="Closet_Part_Surfaces",
                                    bottom="Closet_Part_Surfaces")

    Drawer_Sides = sn_types.Cutpart_Pointer(thickness=sn_unit.inch(.75),
                                            core="Drawer_Box_Surface",
                                            top="Drawer_Box_Surface",
                                            bottom="Drawer_Box_Surface")

    Drawer_Part = sn_types.Cutpart_Pointer(thickness=sn_unit.inch(.75),
                                           core="Drawer_Box_Surface",
                                           top="Drawer_Box_Surface",
                                           bottom="Drawer_Box_Surface")

    Shoe_Cubby = sn_types.Cutpart_Pointer(thickness=sn_unit.inch(.25),
                                          core="Closet_Part_Surfaces",
                                          top="Closet_Part_Surfaces",
                                          bottom="Closet_Part_Surfaces")

    Drawer_Back = sn_types.Cutpart_Pointer(thickness=sn_unit.inch(.75),
                                           core="Drawer_Box_Surface",
                                           top="Drawer_Box_Surface",
                                           bottom="Drawer_Box_Surface")

    Drawer_Bottom = sn_types.Cutpart_Pointer(thickness=sn_unit.inch(.25),
                                             core="Drawer_Box_Surface",
                                             top="Drawer_Box_Surface",
                                             bottom="Drawer_Box_Surface")

    Thick_Drawer_Bottom = sn_types.Cutpart_Pointer(thickness=sn_unit.inch(.75),
                                                   core="Drawer_Box_Surface",
                                                   top="Drawer_Box_Surface",
                                                   bottom="Drawer_Box_Surface")

    Slab_Door = sn_types.Cutpart_Pointer(thickness=sn_unit.inch(.75),
                                         core="Closet_Part_Surfaces",
                                         top="Door_Surface",
                                         bottom="Door_Surface")

    Lucite_Front = sn_types.Cutpart_Pointer(thickness=sn_unit.inch(.75),
                                            core="Lucite",
                                            top="Lucite",
                                            bottom="Lucite")

    Slab_Drawer_Front = sn_types.Cutpart_Pointer(thickness=sn_unit.inch(.75),
                                                 core="Closet_Part_Surfaces",
                                                 top="Door_Surface",
                                                 bottom="Door_Surface")

    Hanging_Rail = sn_types.Cutpart_Pointer(thickness=sn_unit.inch(.75),
                                            core="Chrome",
                                            top="Chrome",
                                            bottom="Chrome")


class Edgepart_Pointers():

    Edge = sn_types.Edgepart_Pointer(thickness=sn_unit.inch(.01), material="Closet_Part_Edges")
    Edge_2 = sn_types.Edgepart_Pointer(thickness=sn_unit.inch(.01), material="Closet_Part_Edges_Secondary")
    Door_Edges = sn_types.Edgepart_Pointer(thickness=sn_unit.inch(.01), material="Door_Edge")
    Lucite_Edges = sn_types.Edgepart_Pointer(thickness=sn_unit.inch(.01), material="Lucite")
    Drawer_Box_Edge = sn_types.Edgepart_Pointer(thickness=sn_unit.inch(.01), material="Drawer_Box_Surface")


class SNAP_UL_material_pointers(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=item.name, icon='HAND')
        layout.label(text=str(item.item_name), icon='STYLUS_PRESSURE')


class SNAP_UL_cutparts(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.7)
        split.label(text=item.name, icon='MOD_UVPROJECT')
        split.prop(item, 'thickness', text="")


class SNAP_UL_edgeparts(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.7)
        split.label(text=item.name, icon='EDGESEL')
        split.prop(item, 'thickness', text="")


class SNAP_PT_Specification_Groups(Panel):
    bl_label = "Specification Groups"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Dev"
    bl_context = "objectmode"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        prefs = context.preferences.addons["snap"].preferences
        return prefs.debug_mode

    def draw_header(self, context):
        layout = self.layout
        layout.label(text='', icon='SOLO_ON')

    def draw(self, context):
        layout = self.layout
        library = context.scene.snap

        if len(library.spec_groups) == 0:
            layout.operator('sn_material.reload_spec_group_from_library_modules', icon='FILE_REFRESH')
        else:
            active_spec_group = library.spec_groups[library.spec_group_index]
            col = layout.column(align=True)
            box = col.box()
            row = box.row(align=True)
            row.scale_y = 1.3
            row.prop_enum(library, "spec_group_tabs", 'MATERIALS', icon='MATERIAL', text="Materials")
            row.prop_enum(library, "spec_group_tabs", 'CUTPARTS', icon='MOD_UVPROJECT', text="Cutparts")
            row.prop_enum(library, "spec_group_tabs", 'EDGEPARTS', icon='EDGESEL', text="Edgeparts")

            if library.spec_group_tabs == 'MATERIALS':
                active_spec_group.draw_materials(col)
            if library.spec_group_tabs == 'CUTPARTS':
                active_spec_group.draw_cutparts(col)
            if library.spec_group_tabs == 'EDGEPARTS':
                active_spec_group.draw_edgeparts(col)


classes = (
    SNAP_UL_material_pointers,
    SNAP_UL_cutparts,
    SNAP_UL_edgeparts,
    SNAP_PT_Specification_Groups
)

register, unregister = bpy.utils.register_classes_factory(classes)

