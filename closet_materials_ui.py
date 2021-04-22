import bpy
from . import property_groups


MAX_MENU_COL_LEN = 24


class G:
    pass


class OPS_change_active_index(bpy.types.Operator):
    bl_idname = "db_materials.change_active_index"
    bl_label = "Change Active Index"
    bl_description = "This changes the active collection index"
    bl_options = {'UNDO'}

    name = bpy.props.StringProperty(name="Item Name")

    i_type = bpy.props.EnumProperty(
        name="Index Type",
        items = [
            ('TYPE', 'TYPE', ''),
            ('MFG', 'MFG', ''),
            ('COLOR', 'COLOR', '')
        ]
    )

    def execute(self, context):
        countertops = context.scene.db_materials.countertops

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


class MENU_Edge_Types(bpy.types.Menu):
    bl_label = "Edge Types"

    def draw(self, context):
        cab_mat_props = context.scene.db_materials
        types = cab_mat_props.edges.edge_types
        layout = self.layout
        row = layout.row()
        G.collection = types        

        for index, item in enumerate(types):

            if index % MAX_MENU_COL_LEN == 0:
                col = row.column()            

            op = col.operator(
                'db_materials.change_active_index',
                text=item.name,
                icon='FILE_TICK' if index == cab_mat_props.edge_type_index else 'LINK'
            )

            op.name = item.name
            op.i_type = 'TYPE'


class MENU_Edge_Colors(bpy.types.Menu):
    bl_label = "Edge Colors"

    def draw(self, context):
        cab_mat_props = context.scene.db_materials
        edge_type = cab_mat_props.edges.get_edge_type()
        colors = edge_type.colors
        layout = self.layout
        row = layout.row()
        G.collection = colors

        for index, item in enumerate(colors):

            if index % MAX_MENU_COL_LEN == 0:
                col = row.column()

            op = col.operator(
                'db_materials.change_active_index',
                text=item.name,
                icon='FILE_TICK' if index == cab_mat_props.edge_color_index else item.get_icon()
            )                

            op.name = item.name
            op.i_type = 'COLOR'           


class MENU_Door_Drawer_Edge_Types(bpy.types.Menu):
    bl_label = "Door/Drawer Edge Types"

    def draw(self, context):
        cab_mat_props = context.scene.db_materials
        types = cab_mat_props.door_drawer_edges.edge_types
        layout = self.layout
        row = layout.row()
        G.collection = types        

        for index, item in enumerate(types):

            if index % MAX_MENU_COL_LEN == 0:
                col = row.column()            

            op = col.operator(
                'db_materials.change_active_index',
                text=item.name,
                icon='FILE_TICK' if index == cab_mat_props.door_drawer_edge_type_index else 'LINK'
            )

            op.name = item.name
            op.i_type = 'TYPE'


class MENU_Door_Drawer_Edge_Colors(bpy.types.Menu):
    bl_label = "Door/Drawer Edge Colors"

    def draw(self, context):
        cab_mat_props = context.scene.db_materials
        edge_type = cab_mat_props.door_drawer_edges.get_edge_type()
        colors = edge_type.colors
        layout = self.layout
        row = layout.row()
        G.collection = colors

        for index, item in enumerate(colors):

            if index % MAX_MENU_COL_LEN == 0:
                col = row.column()

            op = col.operator(
                'db_materials.change_active_index',
                text=item.name,
                icon='FILE_TICK' if index == cab_mat_props.door_drawer_edge_color_index else item.get_icon()
            )                

            op.name = item.name
            op.i_type = 'COLOR'           


class MENU_Secondary_Edge_Types(bpy.types.Menu):
    bl_label = "Secondary Edge Types"

    def draw(self, context):
        cab_mat_props = context.scene.db_materials
        types = cab_mat_props.secondary_edges.edge_types
        layout = self.layout
        row = layout.row()
        G.collection = types        

        for index, item in enumerate(types):

            if index % MAX_MENU_COL_LEN == 0:
                col = row.column()            

            op = col.operator(
                'db_materials.change_active_index',
                text=item.name,
                icon='FILE_TICK' if index == cab_mat_props.secondary_edge_type_index else 'LINK'
            )

            op.name = item.name
            op.i_type = 'TYPE'


class MENU_Secondary_Edge_Colors(bpy.types.Menu):
    bl_label = "Secondary Edge Colors"

    def draw(self, context):
        cab_mat_props = context.scene.db_materials
        edge_type = cab_mat_props.secondary_edges.get_edge_type()
        colors = edge_type.colors
        layout = self.layout
        row = layout.row()
        G.collection = colors

        for index, item in enumerate(colors):

            if index % MAX_MENU_COL_LEN == 0:
                col = row.column()

            op = col.operator(
                'db_materials.change_active_index',
                text=item.name,
                icon='FILE_TICK' if index == cab_mat_props.secondary_edge_color_index else item.get_icon()
            )                

            op.name = item.name
            op.i_type = 'COLOR'           


class MENU_Mat_Colors(bpy.types.Menu):
    bl_label = "Material Colors"

    def draw(self, context):
        cab_mat_props = context.scene.db_materials
        mat_type = cab_mat_props.materials.get_mat_type()
        colors = mat_type.colors
        layout = self.layout
        row = layout.row()
        G.collection = colors

        for index, item in enumerate(colors):

            if index % MAX_MENU_COL_LEN == 0:
                col = row.column()

            if item.oversize_max_len > 0:
                max_len_inch = round(item.oversize_max_len/25.4,2)
                max_len_str = ' - (Max Length: {}")'.format(max_len_inch)
                label = item.name + max_len_str
            else:
                label = item.name                

            op = col.operator(
                'db_materials.change_active_index',
                text=label,
                icon='FILE_TICK' if index == cab_mat_props.mat_color_index else item.get_icon()
            )

            op.name = item.name
            op.i_type = 'COLOR'   


class MENU_Mat_Types(bpy.types.Menu):
    bl_label = "Material Types"

    def draw(self, context):
        cab_mat_props = context.scene.db_materials
        types = cab_mat_props.materials.mat_types
        layout = self.layout
        row = layout.row()
        G.collection = types                

        for index, item in enumerate(types):

            if index % MAX_MENU_COL_LEN == 0:
                col = row.column()    

            op = col.operator(
                'db_materials.change_active_index',
                text=item.name,
                icon='FILE_TICK' if index == cab_mat_props.mat_type_index else 'LINK'
            )

            op.name = item.name
            op.i_type = 'TYPE'

                                
class MENU_Door_Drawer_Mat_Colors(bpy.types.Menu):
    bl_label = "Custom Material Colors"

    def draw(self, context):
        cab_mat_props = context.scene.db_materials
        mat_type = cab_mat_props.door_drawer_materials.get_mat_type()
        colors = mat_type.colors
        layout = self.layout
        row = layout.row()
        G.collection = colors

        for index, item in enumerate(colors):

            if index % MAX_MENU_COL_LEN == 0:
                col = row.column()

            op = col.operator(
                'db_materials.change_active_index',
                text=item.name,
                icon='FILE_TICK' if index == cab_mat_props.door_drawer_mat_color_index else item.get_icon()
            )                

            op.name = item.name
            op.i_type = 'COLOR'   


class MENU_Door_Drawer_Mat_Types(bpy.types.Menu):
    bl_label = "Custom Material Types"

    def draw(self, context):
        cab_mat_props = context.scene.db_materials
        types = cab_mat_props.door_drawer_materials.mat_types
        layout = self.layout
        row = layout.row()
        G.collection = types                

        for index, item in enumerate(types):

            if index % MAX_MENU_COL_LEN == 0:
                col = row.column()    

            op = col.operator(
                'db_materials.change_active_index',
                text=item.name,
                icon='FILE_TICK' if index == cab_mat_props.door_drawer_mat_type_index else 'LINK'
            )

            op.name = item.name
            op.i_type = 'TYPE'                                


class MENU_Countertop_Types(bpy.types.Menu):
    bl_label = "Countertop Types"

    def draw(self, context):
        cab_mat_props = context.scene.db_materials
        types = cab_mat_props.countertops.countertop_types
        layout = self.layout
        row = layout.row()
        G.collection = types

        for index, item in enumerate(types):

            if index % MAX_MENU_COL_LEN == 0:
                col = row.column()

            op = col.operator(
                'db_materials.change_active_index',
                text=item.name,
                icon='FILE_TICK' if index == cab_mat_props.ct_type_index else 'LINK'
            )

            op.name = item.name
            op.i_type = 'TYPE'


class MENU_Countertop_Mfgs(bpy.types.Menu):
    bl_label = "Countertop Manufactuers"

    def draw(self, context):
        cab_mat_props = context.scene.db_materials
        ct_type = cab_mat_props.countertops.get_type()
        mfgs = ct_type.manufactuers
        mfg_index = cab_mat_props.ct_mfg_index
        layout = self.layout
        row = layout.row()
        G.collection = mfgs

        for index, item in enumerate(mfgs):

            if index % MAX_MENU_COL_LEN == 0:
                col = row.column()

            op = col.operator(
                'db_materials.change_active_index',
                text=item.name,
                icon='FILE_TICK' if index == mfg_index else 'LINK'
            )

            op.name = item.name
            op.i_type = 'MFG'


class MENU_Countertop_Colors(bpy.types.Menu):
    bl_label = "Countertop Colors"

    def draw(self, context):        
        cab_mat_props = context.scene.db_materials
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

            if index % MAX_MENU_COL_LEN == 0:
                col = row.column()

            op = col.operator(
                'db_materials.change_active_index',
                text=item.name,
                icon='FILE_TICK' if index == color_index else item.get_icon()
            )

            op.name = item.name
            op.i_type = 'COLOR'


class MENU_Stain_Colors(bpy.types.Menu):
    bl_label = "Stain Colors"

    def draw(self, context):
        cab_mat_props = context.scene.db_materials
        colors = cab_mat_props.stain_colors
        layout = self.layout
        row = layout.row()

        for index, stain_color in enumerate(colors):

            if index % MAX_MENU_COL_LEN == 0:
                col = row.column()

            if index == cab_mat_props.stain_color_index:
                props = col.operator('db_materials.change_active_stain_color', text=stain_color.name, icon='FILE_TICK')
                props.stain_color_name = stain_color.name

            else:
                props = col.operator('db_materials.change_active_stain_color', text=stain_color.name, icon='LINK')
                props.stain_color_name = stain_color.name


class OPS_Change_Active_Stain_Color(bpy.types.Operator):
    bl_idname = "db_materials.change_active_stain_color"
    bl_label = "Change Stain Color"
    bl_description = "This changes the active stain color"
    bl_options = {'UNDO'}

    stain_color_name = bpy.props.StringProperty(name="Stain Color Name")

    def execute(self, context):
        props = context.scene.db_materials
        stain_colors = props.stain_colors        

        for index, stain_color in enumerate(stain_colors):
            if stain_color.name == self.stain_color_name:
                context.scene.db_materials.stain_color_index = index

        return {'FINISHED'}


class MENU_Glaze_Colors(bpy.types.Menu):
    bl_label = "Glaze Colors"

    def draw(self, context):
        cab_mat_props = context.scene.db_materials
        colors = cab_mat_props.glaze_colors
        layout = self.layout
        row = layout.row()

        for index, glaze_color in enumerate(colors):

            if index % MAX_MENU_COL_LEN == 0:
                col = row.column()

            if index == cab_mat_props.glaze_color_index:
                props = col.operator('db_materials.change_active_glaze_color', text=glaze_color.name, icon='FILE_TICK')
                props.glaze_color_name = glaze_color.name

            else:
                props = col.operator('db_materials.change_active_glaze_color', text=glaze_color.name, icon='LINK')
                props.glaze_color_name = glaze_color.name


class OPS_Change_Active_Glaze_Color(bpy.types.Operator):
    bl_idname = "db_materials.change_active_glaze_color"
    bl_label = "Change Glaze Color"
    bl_description = "This changes the active glaze color"
    bl_options = {'UNDO'}

    glaze_color_name = bpy.props.StringProperty(name="Glaze Color Name")

    def execute(self, context):
        props = context.scene.db_materials
        glaze_colors = props.glaze_colors        

        for index, glaze_color in enumerate(glaze_colors):
            if glaze_color.name == self.glaze_color_name:
                context.scene.db_materials.glaze_color_index = index

        return {'FINISHED'}


class MENU_Glaze_Styles(bpy.types.Menu):
    bl_label = "Glaze Styles"

    def draw(self, context):
        cab_mat_props = context.scene.db_materials
        styles = cab_mat_props.glaze_styles
        layout = self.layout
        row = layout.row()

        for index, glaze_style in enumerate(styles):

            if index % MAX_MENU_COL_LEN == 0:
                col = row.column()

            if index == cab_mat_props.glaze_style_index:
                props = col.operator('db_materials.change_active_glaze_style', text=glaze_style.name, icon='FILE_TICK')
                props.glaze_style_name = glaze_style.name

            else:
                props = col.operator('db_materials.change_active_glaze_style', text=glaze_style.name, icon='LINK')
                props.glaze_style_name = glaze_style.name


class OPS_Change_Active_Glaze_Style(bpy.types.Operator):
    bl_idname = "db_materials.change_active_glaze_style"
    bl_label = "Change Glaze Style"
    bl_description = "This changes the active glaze style"
    bl_options = {'UNDO'}

    glaze_style_name = bpy.props.StringProperty(name="Glaze Style Name")

    def execute(self, context):
        props = context.scene.db_materials
        glaze_styles = props.glaze_styles        

        for index, glaze_style in enumerate(glaze_styles):
            if glaze_style.name == self.glaze_style_name:
                context.scene.db_materials.glaze_style_index = index

        return {'FINISHED'}


class MENU_Door_Colors(bpy.types.Menu):
    bl_label = "Door Colors"

    def draw(self, context):
        cab_mat_props = context.scene.db_materials
        colors = cab_mat_props.moderno_colors
        layout = self.layout
        row = layout.row()

        for index, door_color in enumerate(colors):

            if index % MAX_MENU_COL_LEN == 0:
                col = row.column()

            if index == cab_mat_props.moderno_color_index:
                props = col.operator('db_materials.change_active_door_color', text=door_color.name, icon='FILE_TICK')
                props.door_color_name = door_color.name

            else:
                props = col.operator('db_materials.change_active_door_color', text=door_color.name, icon='LINK')
                props.door_color_name = door_color.name


class OPS_Change_Active_Door_Color(bpy.types.Operator):
    bl_idname = "db_materials.change_active_door_color"
    bl_label = "Change Door Color"
    bl_description = "This changes the active door color"
    bl_options = {'UNDO'}

    door_color_name = bpy.props.StringProperty(name="Door Color Name")

    def execute(self, context):
        props = context.scene.db_materials
        moderno_colors = props.moderno_colors        

        for index, door_color in enumerate(moderno_colors):
            if door_color.name == self.door_color_name:
                context.scene.db_materials.moderno_color_index = index

        return {'FINISHED'}


class MENU_Glass_Colors(bpy.types.Menu):
    bl_label = "Glass Colors"

    def draw(self, context):
        cab_mat_props = context.scene.db_materials
        colors = cab_mat_props.glass_colors
        layout = self.layout
        row = layout.row()

        for index, glass_color in enumerate(colors):

            if index % MAX_MENU_COL_LEN == 0:
                col = row.column()

            if index == cab_mat_props.glass_color_index:
                props = col.operator('db_materials.change_active_glass_color', text=glass_color.name, icon='FILE_TICK')
                props.glass_color_name = glass_color.name

            else:
                props = col.operator('db_materials.change_active_glass_color', text=glass_color.name, icon='LINK')
                props.glass_color_name = glass_color.name


class OPS_Change_Active_Glass_Color(bpy.types.Operator):
    bl_idname = "db_materials.change_active_glass_color"
    bl_label = "Change Glass Color"
    bl_description = "This changes the active glass color"
    bl_options = {'UNDO'}

    glass_color_name = bpy.props.StringProperty(name="Glass Color Name")

    def execute(self, context):
        props = context.scene.db_materials
        glass_colors = props.glass_colors        

        for index, glass_color in enumerate(glass_colors):
            if glass_color.name == self.glass_color_name:
                context.scene.db_materials.glass_color_index = index

        return {'FINISHED'}


class MENU_Drawer_Slides(bpy.types.Menu):
    bl_label = "Drawer Slides"

    def draw(self, context):
        cab_mat_props = context.scene.db_materials
        slide_types = cab_mat_props.drawer_slides
        layout = self.layout
        row = layout.row()

        for index, slide_type in enumerate(slide_types):

            if index % MAX_MENU_COL_LEN == 0:
                col = row.column()

            if index == cab_mat_props.drawer_slide_index:
                props = col.operator('db_materials.change_slide_type', text=slide_type.name, icon='FILE_TICK')
                props.slide_type_name = slide_type.name

            else:
                props = col.operator('db_materials.change_slide_type', text=slide_type.name, icon='LINK')
                props.slide_type_name = slide_type.name


class OPS_Change_Active_Slide_Type(bpy.types.Operator):
    bl_idname = "db_materials.change_slide_type"
    bl_label = "Change Drawer Slide Type"
    bl_description = "This changes the active drawer slide type"
    bl_options = {'UNDO'}

    slide_type_name = bpy.props.StringProperty(name="Slide Type Name")

    def execute(self, context):
        props = context.scene.db_materials
        slide_types = props.drawer_slides        

        for index, slide_type in enumerate(slide_types):
            if slide_type.name == self.slide_type_name:
                context.scene.db_materials.drawer_slide_index = index

        return {'FINISHED'}


def register():
    bpy.utils.register_class(MENU_Edge_Types)
    bpy.utils.register_class(MENU_Edge_Colors)
    bpy.utils.register_class(MENU_Door_Drawer_Edge_Types)
    bpy.utils.register_class(MENU_Door_Drawer_Edge_Colors)
    bpy.utils.register_class(MENU_Secondary_Edge_Types)
    bpy.utils.register_class(MENU_Secondary_Edge_Colors)
    bpy.utils.register_class(MENU_Mat_Types)
    bpy.utils.register_class(MENU_Mat_Colors)
    bpy.utils.register_class(MENU_Door_Drawer_Mat_Types)
    bpy.utils.register_class(MENU_Door_Drawer_Mat_Colors)
    bpy.utils.register_class(MENU_Countertop_Types)
    bpy.utils.register_class(MENU_Countertop_Mfgs)
    bpy.utils.register_class(MENU_Countertop_Colors)
    bpy.utils.register_class(MENU_Stain_Colors)
    bpy.utils.register_class(MENU_Glaze_Colors)
    bpy.utils.register_class(MENU_Glaze_Styles)
    bpy.utils.register_class(MENU_Door_Colors)
    bpy.utils.register_class(MENU_Glass_Colors)
    bpy.utils.register_class(MENU_Drawer_Slides)
    bpy.utils.register_class(OPS_Change_Active_Stain_Color)
    bpy.utils.register_class(OPS_Change_Active_Glaze_Color)
    bpy.utils.register_class(OPS_Change_Active_Glaze_Style)
    bpy.utils.register_class(OPS_Change_Active_Door_Color)
    bpy.utils.register_class(OPS_Change_Active_Glass_Color)
    bpy.utils.register_class(OPS_Change_Active_Slide_Type)
    bpy.utils.register_class(OPS_change_active_index)

def unregister():
    bpy.utils.unregister_class(MENU_Edge_Types)
    bpy.utils.unregister_class(MENU_Edge_Colors)
    bpy.utils.unregister_class(MENU_Door_Drawer_Edge_Types)
    bpy.utils.unregister_class(MENU_Door_Drawer_Edge_Colors)
    bpy.utils.unregister_class(MENU_Secondary_Edge_Types)
    bpy.utils.unregister_class(MENU_Secondary_Edge_Colors)
    bpy.utils.unregister_class(MENU_Mat_Types)
    bpy.utils.unregister_class(MENU_Mat_Colors)
    bpy.utils.unregister_class(MENU_Door_Drawer_Mat_Types)
    bpy.utils.unregister_class(MENU_Door_Drawer_Mat_Colors)
    bpy.utils.unregister_class(MENU_Countertop_Types)
    bpy.utils.unregister_class(MENU_Countertop_Mfgs)
    bpy.utils.unregister_class(MENU_Countertop_Colors)
    bpy.utils.unregister_class(MENU_Stain_Colors)
    bpy.utils.unregister_class(MENU_Glaze_Colors)
    bpy.utils.unregister_class(MENU_Glaze_Styles)
    bpy.utils.unregister_class(MENU_Door_Colors)
    bpy.utils.unregister_class(MENU_Glass_Colors)
    bpy.utils.unregister_class(MENU_Drawer_Slides)
    bpy.utils.unregister_class(OPS_Change_Active_Stain_Color)
    bpy.utils.unregister_class(OPS_Change_Active_Glaze_Color)
    bpy.utils.unregister_class(OPS_Change_Active_Glaze_Style)
    bpy.utils.unregister_class(OPS_Change_Active_Door_Color)
    bpy.utils.unregister_class(OPS_Change_Active_Glass_Color)
    bpy.utils.unregister_class(OPS_Change_Active_Slide_Type)
    bpy.utils.unregister_class(OPS_change_active_index)
