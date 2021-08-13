import bpy
from bpy.types import Operator
from bpy.props import (
    StringProperty,
    EnumProperty
)


MAX_COL_LEN = 24


class G:
    pass


class SNAP_MATERIALS_OT_change_active_index(Operator):
    bl_idname = "closet_materials.change_active_index"
    bl_label = "Change Active Index"
    bl_description = "This changes the active collection index"
    bl_options = {'UNDO'}

    name: StringProperty(name="Item Name")

    i_type: EnumProperty(
        name="Index Type",
        items=[
            ('TYPE', 'TYPE', ''),
            ('MFG', 'MFG', ''),
            ('COLOR', 'COLOR', '')
        ]
    )

    def execute(self, context):
        countertops = context.scene.closet_materials.countertops

        collection_name = G.collection.data.bl_rna.name

        for index, item in enumerate(G.collection):
            if item.name == self.name:

                if collection_name in ('Edges', 'SecondaryEdges','DoorDrawerEdges'):
                    if self.i_type == 'TYPE':
                        G.collection.data.set_type_index(index)
                        return {'FINISHED'}

                if collection_name in ('EdgeType', 'SecondaryEdgeType','DoorDrawerEdgeType'):
                    if self.i_type == 'COLOR':
                        G.collection.data.set_color_index(index)
                        return {'FINISHED'}

                if collection_name in ('Materials', 'MaterialType', 'DoorDrawerMaterials','DoorDrawerMaterialType'):
                    if self.i_type == 'TYPE':
                        G.collection.data.set_type_index(index)

                    elif self.i_type == 'COLOR':
                        G.collection.data.set_color_index(index)

                    return {'FINISHED'}


                if self.i_type == 'TYPE':
                    countertops.set_ct_type_index(index)

                if self.i_type == 'MFG':
                    countertops.get_type().set_mfg_index(index)

                if self.i_type == 'COLOR':
                    ct_type = countertops.get_type()
                    
                    if len(ct_type.colors) > 0:
                        ct_type.set_color_index(index)

                    else:
                        ct_type.get_mfg().set_color_index(index)

        return {'FINISHED'}


class SNAP_MATERIAL_MT_Edge_Types(bpy.types.Menu):
    bl_label = "Edge Types"

    def draw(self, context):
        cab_mat_props = context.scene.closet_materials
        types = cab_mat_props.edges.edge_types
        layout = self.layout
        row = layout.row()
        G.collection = types        

        for index, item in enumerate(types):

            if index % MAX_COL_LEN == 0:
                col = row.column()            

            op = col.operator(
                'closet_materials.change_active_index',
                text=item.name,
                icon='RADIOBUT_ON' if index == cab_mat_props.edge_type_index else 'RADIOBUT_OFF'
            )

            op.name = item.name
            op.i_type = 'TYPE'


class SNAP_MATERIAL_MT_Edge_Colors(bpy.types.Menu):
    bl_label = "Edge Colors"

    def draw(self, context):
        cab_mat_props = context.scene.closet_materials
        edge_type = cab_mat_props.edges.get_edge_type()
        colors = edge_type.colors
        layout = self.layout
        row = layout.row()
        G.collection = colors

        for index, item in enumerate(colors):

            if index % MAX_COL_LEN == 0:
                col = row.column()

            op = col.operator(
                'closet_materials.change_active_index',
                text=item.name,
                icon='RADIOBUT_ON' if index == cab_mat_props.edge_color_index else item.get_icon()
            )                

            op.name = item.name
            op.i_type = 'COLOR'           


class SNAP_MATERIAL_MT_Door_Drawer_Edge_Types(bpy.types.Menu):
    bl_label = "Door/Drawer Edge Types"

    def draw(self, context):
        cab_mat_props = context.scene.closet_materials
        types = cab_mat_props.door_drawer_edges.edge_types
        layout = self.layout
        row = layout.row()
        G.collection = types        

        for index, item in enumerate(types):

            if index % MAX_COL_LEN == 0:
                col = row.column()            

            op = col.operator(
                'closet_materials.change_active_index',
                text=item.name,
                icon='RADIOBUT_ON' if index == cab_mat_props.door_drawer_edge_type_index else 'RADIOBUT_OFF'
            )

            op.name = item.name
            op.i_type = 'TYPE'


class SNAP_MATERIAL_MT_Door_Drawer_Edge_Colors(bpy.types.Menu):
    bl_label = "Door/Drawer Edge Colors"

    def draw(self, context):
        cab_mat_props = context.scene.closet_materials
        edge_type = cab_mat_props.door_drawer_edges.get_edge_type()
        colors = edge_type.colors
        layout = self.layout
        row = layout.row()
        G.collection = colors

        for index, item in enumerate(colors):

            if index % MAX_COL_LEN == 0:
                col = row.column()

            op = col.operator(
                'closet_materials.change_active_index',
                text=item.name,
                icon='RADIOBUT_ON' if index == cab_mat_props.door_drawer_edge_color_index else item.get_icon()
            )                

            op.name = item.name
            op.i_type = 'COLOR'           


class SNAP_MATERIAL_MT_Secondary_Edge_Types(bpy.types.Menu):
    bl_label = "Secondary Edge Types"

    def draw(self, context):
        cab_mat_props = context.scene.closet_materials
        types = cab_mat_props.secondary_edges.edge_types
        layout = self.layout
        row = layout.row()
        G.collection = types        

        for index, item in enumerate(types):

            if index % MAX_COL_LEN == 0:
                col = row.column()            

            op = col.operator(
                'closet_materials.change_active_index',
                text=item.name,
                icon='RADIOBUT_ON' if index == cab_mat_props.secondary_edge_type_index else 'RADIOBUT_OFF'
            )

            op.name = item.name
            op.i_type = 'TYPE'


class SNAP_MATERIAL_MT_Secondary_Edge_Colors(bpy.types.Menu):
    bl_label = "Secondary Edge Colors"

    def draw(self, context):
        cab_mat_props = context.scene.closet_materials
        edge_type = cab_mat_props.secondary_edges.get_edge_type()
        colors = edge_type.colors
        layout = self.layout
        row = layout.row()
        G.collection = colors

        for index, item in enumerate(colors):

            if index % MAX_COL_LEN == 0:
                col = row.column()

            op = col.operator(
                'closet_materials.change_active_index',
                text=item.name,
                icon='RADIOBUT_ON' if index == cab_mat_props.secondary_edge_color_index else item.get_icon()
            )                

            op.name = item.name
            op.i_type = 'COLOR'           


class SNAP_MATERIAL_MT_Mat_Colors(bpy.types.Menu):
    bl_label = "Material Colors"

    def draw(self, context):
        cab_mat_props = context.scene.closet_materials
        mat_type = cab_mat_props.materials.get_mat_type()
        colors = mat_type.colors
        layout = self.layout
        row = layout.row()
        G.collection = colors

        for index, item in enumerate(colors):

            if index % MAX_COL_LEN == 0:
                col = row.column()

            if item.oversize_max_len > 0:
                max_len_inch = round(item.oversize_max_len/25.4,2)
                max_len_str = ' - (Max Length: {}")'.format(max_len_inch)
                label = item.name + max_len_str
            else:
                label = item.name                

            op = col.operator(
                'closet_materials.change_active_index',
                text=label,
                icon='RADIOBUT_ON' if index == cab_mat_props.mat_color_index else item.get_icon()
            )

            op.name = item.name
            op.i_type = 'COLOR'   


class SNAP_MATERIAL_MT_Mat_Types(bpy.types.Menu):
    bl_label = "Material Types"

    def draw(self, context):
        cab_mat_props = context.scene.closet_materials
        types = cab_mat_props.materials.mat_types
        layout = self.layout
        row = layout.row()
        G.collection = types                

        for index, item in enumerate(types):

            if index % MAX_COL_LEN == 0:
                col = row.column()    

            op = col.operator(
                'closet_materials.change_active_index',
                text=item.name,
                icon='RADIOBUT_ON' if index == cab_mat_props.mat_type_index else 'RADIOBUT_OFF'
            )

            op.name = item.name
            op.i_type = 'TYPE'

                                
class SNAP_MATERIAL_MT_Door_Drawer_Mat_Colors(bpy.types.Menu):
    bl_label = "Custom Material Colors"

    def draw(self, context):
        cab_mat_props = context.scene.closet_materials
        mat_type = cab_mat_props.door_drawer_materials.get_mat_type()
        colors = mat_type.colors
        layout = self.layout
        row = layout.row()
        G.collection = colors

        for index, item in enumerate(colors):

            if index % MAX_COL_LEN == 0:
                col = row.column()

            op = col.operator(
                'closet_materials.change_active_index',
                text=item.name,
                icon='RADIOBUT_ON' if index == cab_mat_props.door_drawer_mat_color_index else item.get_icon()
            )                

            op.name = item.name
            op.i_type = 'COLOR'   


class SNAP_MATERIAL_MT_Door_Drawer_Mat_Types(bpy.types.Menu):
    bl_label = "Custom Material Types"

    def draw(self, context):
        cab_mat_props = context.scene.closet_materials
        types = cab_mat_props.door_drawer_materials.mat_types
        layout = self.layout
        row = layout.row()
        G.collection = types                

        for index, item in enumerate(types):

            if index % MAX_COL_LEN == 0:
                col = row.column()    

            op = col.operator(
                'closet_materials.change_active_index',
                text=item.name,
                icon='RADIOBUT_ON' if index == cab_mat_props.door_drawer_mat_type_index else 'RADIOBUT_OFF'
            )

            op.name = item.name
            op.i_type = 'TYPE'                                


class SNAP_MATERIAL_MT_Countertop_Types(bpy.types.Menu):
    bl_label = "Countertop Types"

    def draw(self, context):
        cab_mat_props = context.scene.closet_materials
        types = cab_mat_props.countertops.countertop_types
        layout = self.layout
        row = layout.row()
        G.collection = types

        for index, item in enumerate(types):

            if index % MAX_COL_LEN == 0:
                col = row.column()

            op = col.operator(
                'closet_materials.change_active_index',
                text=item.name,
                icon='RADIOBUT_ON' if index == cab_mat_props.ct_type_index else 'RADIOBUT_OFF'
            )

            op.name = item.name
            op.i_type = 'TYPE'


class SNAP_MATERIAL_MT_Countertop_Mfgs(bpy.types.Menu):
    bl_label = "Countertop Manufactuers"

    def draw(self, context):
        cab_mat_props = context.scene.closet_materials
        ct_type = cab_mat_props.countertops.get_type()
        mfgs = ct_type.manufactuers
        mfg_index = cab_mat_props.ct_mfg_index
        layout = self.layout
        row = layout.row()
        G.collection = mfgs

        for index, item in enumerate(mfgs):

            if index % MAX_COL_LEN == 0:
                col = row.column()

            op = col.operator(
                'closet_materials.change_active_index',
                text=item.name,
                icon='RADIOBUT_ON' if index == mfg_index else 'RADIOBUT_OFF'
            )

            op.name = item.name
            op.i_type = 'MFG'


class SNAP_MATERIAL_MT_Countertop_Colors(bpy.types.Menu):
    bl_label = "Countertop Colors"

    def draw(self, context):        
        cab_mat_props = context.scene.closet_materials
        ct_type = cab_mat_props.countertops.get_type()
        layout = self.layout
        row = layout.row()        

        if len(ct_type.colors) > 0:
            colors = ct_type.colors
            color_index = cab_mat_props.ct_color_index
        
        elif len(ct_type.manufactuers) > 0:
            ct_mfg = ct_type.get_mfg()
            colors = ct_mfg.colors
            color_index = cab_mat_props.ct_color_index

        G.collection = colors

        for index, item in enumerate(colors):

            if index % MAX_COL_LEN == 0:
                col = row.column()

            op = col.operator(
                'closet_materials.change_active_index',
                text=item.name,
                icon='RADIOBUT_ON' if index == color_index else item.get_icon()
            )

            op.name = item.name
            op.i_type = 'COLOR'


class SNAP_MATERIAL_MT_Stain_Colors(bpy.types.Menu):
    bl_label = "Stain Colors"

    def draw(self, context):
        cab_mat_props = context.scene.closet_materials
        colors = cab_mat_props.stain_colors
        layout = self.layout
        row = layout.row()

        for index, stain_color in enumerate(colors):

            if index % MAX_COL_LEN == 0:
                col = row.column()

            if index == cab_mat_props.stain_color_index:
                props = col.operator('closet_materials.change_active_stain_color', text=stain_color.name, icon='RADIOBUT_ON')
                props.stain_color_name = stain_color.name

            else:
                props = col.operator('closet_materials.change_active_stain_color', text=stain_color.name, icon='RADIOBUT_OFF')
                props.stain_color_name = stain_color.name


class OPS_Change_Active_Stain_Color(Operator):
    bl_idname = "closet_materials.change_active_stain_color"
    bl_label = "Change Stain Color"
    bl_description = "This changes the active stain color"
    bl_options = {'UNDO'}

    stain_color_name: StringProperty(name="Stain Color Name")

    def execute(self, context):
        props = context.scene.closet_materials
        stain_colors = props.stain_colors        

        for index, stain_color in enumerate(stain_colors):
            if stain_color.name == self.stain_color_name:
                context.scene.closet_materials.stain_color_index = index

        return {'FINISHED'}


class SNAP_MATERIAL_MT_Glaze_Colors(bpy.types.Menu):
    bl_label = "Glaze Colors"

    def draw(self, context):
        cab_mat_props = context.scene.closet_materials
        colors = cab_mat_props.glaze_colors
        layout = self.layout
        row = layout.row()

        for index, glaze_color in enumerate(colors):

            if index % MAX_COL_LEN == 0:
                col = row.column()

            if index == cab_mat_props.glaze_color_index:
                props = col.operator('closet_materials.change_active_glaze_color', text=glaze_color.name, icon='RADIOBUT_ON')
                props.glaze_color_name = glaze_color.name

            else:
                props = col.operator('closet_materials.change_active_glaze_color', text=glaze_color.name, icon='RADIOBUT_OFF')
                props.glaze_color_name = glaze_color.name


class OPS_Change_Active_Glaze_Color(Operator):
    bl_idname = "closet_materials.change_active_glaze_color"
    bl_label = "Change Glaze Color"
    bl_description = "This changes the active glaze color"
    bl_options = {'UNDO'}

    glaze_color_name: StringProperty(name="Glaze Color Name")

    def execute(self, context):
        props = context.scene.closet_materials
        glaze_colors = props.glaze_colors        

        for index, glaze_color in enumerate(glaze_colors):
            if glaze_color.name == self.glaze_color_name:
                context.scene.closet_materials.glaze_color_index = index

        return {'FINISHED'}


class SNAP_MATERIAL_MT_Glaze_Styles(bpy.types.Menu):
    bl_label = "Glaze Styles"

    def draw(self, context):
        cab_mat_props = context.scene.closet_materials
        styles = cab_mat_props.glaze_styles
        layout = self.layout
        row = layout.row()

        for index, glaze_style in enumerate(styles):

            if index % MAX_COL_LEN == 0:
                col = row.column()

            if index == cab_mat_props.glaze_style_index:
                props = col.operator('closet_materials.change_active_glaze_style', text=glaze_style.name, icon='RADIOBUT_ON')
                props.glaze_style_name = glaze_style.name

            else:
                props = col.operator('closet_materials.change_active_glaze_style', text=glaze_style.name, icon='RADIOBUT_OFF')
                props.glaze_style_name = glaze_style.name


class OPS_Change_Active_Glaze_Style(Operator):
    bl_idname = "closet_materials.change_active_glaze_style"
    bl_label = "Change Glaze Style"
    bl_description = "This changes the active glaze style"
    bl_options = {'UNDO'}

    glaze_style_name: StringProperty(name="Glaze Style Name")

    def execute(self, context):
        props = context.scene.closet_materials
        glaze_styles = props.glaze_styles        

        for index, glaze_style in enumerate(glaze_styles):
            if glaze_style.name == self.glaze_style_name:
                context.scene.closet_materials.glaze_style_index = index

        return {'FINISHED'}


class SNAP_MATERIAL_MT_Door_Colors(bpy.types.Menu):
    bl_label = "Door Colors"

    def draw(self, context):
        cab_mat_props = context.scene.closet_materials
        colors = cab_mat_props.moderno_colors
        layout = self.layout
        row = layout.row()

        for index, door_color in enumerate(colors):

            if index % MAX_COL_LEN == 0:
                col = row.column()

            if index == cab_mat_props.moderno_color_index:
                props = col.operator('closet_materials.change_active_door_color', text=door_color.name, icon='RADIOBUT_ON')
                props.door_color_name = door_color.name

            else:
                props = col.operator('closet_materials.change_active_door_color', text=door_color.name, icon='RADIOBUT_OFF')
                props.door_color_name = door_color.name


class OPS_Change_Active_Door_Color(Operator):
    bl_idname = "closet_materials.change_active_door_color"
    bl_label = "Change Door Color"
    bl_description = "This changes the active door color"
    bl_options = {'UNDO'}

    door_color_name: StringProperty(name="Door Color Name")

    def execute(self, context):
        props = context.scene.closet_materials
        moderno_colors = props.moderno_colors        

        for index, door_color in enumerate(moderno_colors):
            if door_color.name == self.door_color_name:
                context.scene.closet_materials.moderno_color_index = index

        return {'FINISHED'}


class SNAP_MATERIAL_MT_Glass_Colors(bpy.types.Menu):
    bl_label = "Glass Colors"

    def draw(self, context):
        cab_mat_props = context.scene.closet_materials
        colors = cab_mat_props.glass_colors
        layout = self.layout
        row = layout.row()

        for index, glass_color in enumerate(colors):

            if index % MAX_COL_LEN == 0:
                col = row.column()

            if index == cab_mat_props.glass_color_index:
                props = col.operator('closet_materials.change_active_glass_color', text=glass_color.name, icon='RADIOBUT_ON')
                props.glass_color_name = glass_color.name

            else:
                props = col.operator('closet_materials.change_active_glass_color', text=glass_color.name, icon='RADIOBUT_OFF')
                props.glass_color_name = glass_color.name


class OPS_Change_Active_Glass_Color(Operator):
    bl_idname = "closet_materials.change_active_glass_color"
    bl_label = "Change Glass Color"
    bl_description = "This changes the active glass color"
    bl_options = {'UNDO'}

    glass_color_name: StringProperty(name="Glass Color Name")

    def execute(self, context):
        props = context.scene.closet_materials
        glass_colors = props.glass_colors        

        for index, glass_color in enumerate(glass_colors):
            if glass_color.name == self.glass_color_name:
                context.scene.closet_materials.glass_color_index = index

        return {'FINISHED'}


class SNAP_MATERIAL_MT_Drawer_Slides(bpy.types.Menu):
    bl_label = "Drawer Slides"

    def draw(self, context):
        cab_mat_props = context.scene.closet_materials
        slide_types = cab_mat_props.drawer_slides
        layout = self.layout
        row = layout.row()

        for index, slide_type in enumerate(slide_types):

            if index % MAX_COL_LEN == 0:
                col = row.column()

            if index == cab_mat_props.drawer_slide_index:
                props = col.operator('closet_materials.change_slide_type', text=slide_type.name, icon='RADIOBUT_ON')
                props.slide_type_name = slide_type.name

            else:
                props = col.operator('closet_materials.change_slide_type', text=slide_type.name, icon='RADIOBUT_OFF')
                props.slide_type_name = slide_type.name


class OPS_Change_Active_Slide_Type(Operator):
    bl_idname = "closet_materials.change_slide_type"
    bl_label = "Change Drawer Slide Type"
    bl_description = "This changes the active drawer slide type"
    bl_options = {'UNDO'}

    slide_type_name: StringProperty(name="Slide Type Name")

    def execute(self, context):
        props = context.scene.closet_materials
        slide_types = props.drawer_slides        

        for index, slide_type in enumerate(slide_types):
            if slide_type.name == self.slide_type_name:
                context.scene.closet_materials.drawer_slide_index = index

        return {'FINISHED'}


classes = (
    SNAP_MATERIAL_MT_Edge_Types,
    SNAP_MATERIAL_MT_Edge_Colors,
    SNAP_MATERIAL_MT_Door_Drawer_Edge_Types,
    SNAP_MATERIAL_MT_Door_Drawer_Edge_Colors,
    SNAP_MATERIAL_MT_Secondary_Edge_Types,
    SNAP_MATERIAL_MT_Secondary_Edge_Colors,
    SNAP_MATERIAL_MT_Mat_Types,
    SNAP_MATERIAL_MT_Mat_Colors,
    SNAP_MATERIAL_MT_Door_Drawer_Mat_Types,
    SNAP_MATERIAL_MT_Door_Drawer_Mat_Colors,
    SNAP_MATERIAL_MT_Countertop_Types,
    SNAP_MATERIAL_MT_Countertop_Mfgs,
    SNAP_MATERIAL_MT_Countertop_Colors,
    SNAP_MATERIAL_MT_Stain_Colors,
    SNAP_MATERIAL_MT_Glaze_Colors,
    SNAP_MATERIAL_MT_Glaze_Styles,
    SNAP_MATERIAL_MT_Door_Colors,
    SNAP_MATERIAL_MT_Glass_Colors,
    SNAP_MATERIAL_MT_Drawer_Slides,
    OPS_Change_Active_Stain_Color,
    OPS_Change_Active_Glaze_Color,
    OPS_Change_Active_Glaze_Style,
    OPS_Change_Active_Door_Color,
    OPS_Change_Active_Glass_Color,
    OPS_Change_Active_Slide_Type,
    SNAP_MATERIALS_OT_change_active_index
)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()