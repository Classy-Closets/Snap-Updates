import bpy
import snap_db
import operator
import csv
from . import property_groups


enum_items_kd_fitting = []


def update_render_materials(self, context):
    try:
        bpy.ops.db_materials.poll_assign_materials()
    except:
        pass


def enum_kd_fitting(self,context):
    if context is None:
        return []

    if len(enum_items_kd_fitting) > 1:
        return enum_items_kd_fitting
    
    else:
        conn = snap_db.connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT\
                *\
            FROM\
                CCItems\
            WHERE\
                ProductType == 'HW' AND\
                Name LIKE '{}'\
            ;".format("%" + "KD - FF" + "%")
        )

        rows = cursor.fetchall()

        for row in rows:
            enum_items_kd_fitting.append((row[0], row[2], row[2]))
        
        conn.close()

        return enum_items_kd_fitting


class PANEL_Closet_Materials_Interface(bpy.types.Panel):
    """Panel to Store all of the Material Options"""
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "Closet Materials"
    bl_category = "SNaP"
    
    def draw_header(self, context):
        layout = self.layout
        layout.label('',icon='BLANK1')    
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.db_materials
        props.draw(self.layout)


class PROPERTIES_Closet_Materials(bpy.types.PropertyGroup):
    """
    Closet Materials
    """ 

    edges = bpy.props.PointerProperty(type=property_groups.Edges)
    edge_type_index = bpy.props.IntProperty(name="Edge Type Index", default=0)
    edge_color_index = bpy.props.IntProperty(name="Edge Color Index", default=0, update=update_render_materials)

    secondary_edges = bpy.props.PointerProperty(type=property_groups.SecondaryEdges)
    secondary_edge_type_index = bpy.props.IntProperty(name="Secondary Edge Type Index", default=0)
    secondary_edge_color_index = bpy.props.IntProperty(name=" Secondary Edge Color Index", default=0, update=update_render_materials)

    materials = bpy.props.PointerProperty(type=property_groups.Materials)
    mat_type_index = bpy.props.IntProperty(name="Material Type Index", default=0)
    mat_color_index = bpy.props.IntProperty(name="Material Color Index", default=0, update=update_render_materials)

    countertops = bpy.props.PointerProperty(type=property_groups.Countertops)
    ct_type_index = bpy.props.IntProperty(name="Countertop Type Index", default=0)
    ct_mfg_index = bpy.props.IntProperty(name="Countertop Manufactuer Index", default=0)
    ct_color_index = bpy.props.IntProperty(name="Countertop Color Index", default=0, update=update_render_materials)

    stain_colors = bpy.props.CollectionProperty(type=property_groups.StainColor) 
    stain_color_index = bpy.props.IntProperty(name="Stain Color List Index", default=0, update=update_render_materials)

    glaze_colors = bpy.props.CollectionProperty(type=property_groups.GlazeColor)
    glaze_color_index = bpy.props.IntProperty(name="Glaze Color List Index", default=0, update=update_render_materials)
    glaze_styles = bpy.props.CollectionProperty(type=property_groups.GlazeStyle)
    glaze_style_index = bpy.props.IntProperty(name="Glaze Style List Index", default=0)

    moderno_colors = bpy.props.CollectionProperty(type=property_groups.DoorColor)
    moderno_color_index = bpy.props.IntProperty(name="Door Color List Index", default=0, update=update_render_materials)

    glass_colors = bpy.props.CollectionProperty(type=property_groups.GlassColor)
    glass_color_index = bpy.props.IntProperty(name="Glass Color List Index", default=0, update=update_render_materials) 

    wire_basket_colors = bpy.props.EnumProperty(
        name="Wire Basket Color",
        items=(
            ('CHROME', 'Chrome', "Chrome"),
            ('WHITE', 'White', "White")
        ),
        default='CHROME'
    )

    kd_fitting_color = bpy.props.EnumProperty(
        name="KD Fitting Color",
        items=enum_kd_fitting,
    )

    drawer_slides = bpy.props.CollectionProperty(type=property_groups.DrawerSlide)
    drawer_slide_index = bpy.props.IntProperty(name="Drawer Slide List Index", default=0) 

    def check_render_mats(self):
        try:
            edge = self.edges.get_edge_color().has_render_mat
            edge2 = self.secondary_edges.get_edge_color().has_render_mat
            mat = self.materials.get_mat_color().has_render_mat
            ct = self.countertops.color_has_render_mat()

            if all((edge, edge2, mat, ct)):
                return True
            else:
                return False
        except:
            return False

    def get_edge_description(self, obj=None, assembly=None, part_name=None):
        type_code = self.edges.get_edge_type().type_code
        color_code = self.edges.get_edge_color().color_code

        name = snap_db.query_db(
            "SELECT\
                Name\
            FROM\
                CCItems\
            WHERE ProductType = 'EB' AND ItemTypeCode = '{type_code}' AND ItemColorCode = '{color_code}';\
            ".format(type_code=type_code, color_code=color_code)
        )

        if len(name) == 0:
            print("No SKU found for - Edge Type Code: {} Color Code: {}".format(type_code, color_code))
            return "Unknown"
        elif len(name) == 1:
            return name[0][0]
        else:
            print("Multiple SKUs found for - Edge Type Code: {} Color Code: {}".format(type_code, color_code))
            print(name)
            return "Unknown"  

    def get_edge_sku(self, obj=None, assembly=None, part_name=None):
        type_code = self.edges.get_edge_type().type_code
        color_code = self.edges.get_edge_color().color_code

        sku = snap_db.query_db(
            "SELECT\
                SKU\
            FROM\
                CCItems\
            WHERE ProductType = 'EB' AND ItemTypeCode = '{type_code}' AND ItemColorCode = '{color_code}';\
            ".format(type_code=type_code, color_code=color_code)
        )

        if len(sku) == 0:
            print("No SKU found for - Edge Type Code: {} Color Code: {}".format(type_code, color_code))
            return "Unknown"
        elif len(sku) == 1:
            return sku[0][0]
        else:
            print("Multiple SKUs found for - Edge Type Code: {} Color Code: {}".format(type_code, color_code))
            print(sku)
            return "Unknown"        

    def get_edge2_type_name(self):
        name = "Unknown"
        edge_type_code = int(self.edge2_type_menu)
        
        for edge_type in self.edge2_types:
            if edge_type.type_code == edge_type_code:
                name = edge_type.name

        return name

    def get_mat_sku(self, obj=None, assembly=None, part_name=None, mat_name=""):
        mat_type = self.materials.get_mat_type()
        type_code = mat_type.type_code

        if mat_name:
            for mat_color in mat_type.colors:
                if mat_color.name == mat_name:
                    color_code = mat_color.color_code
        else:            
            color_code = self.materials.get_mat_color().color_code
        
        sku = snap_db.query_db(
            "SELECT\
                SKU\
            FROM\
                CCItems\
            WHERE ProductType in ('PM', 'WD') AND ItemTypeCode = '{type_code}' AND ItemColorCode = '{color_code}';\
            ".format(type_code=type_code, color_code=color_code)
        )

        if len(sku) == 0:
            print("No SKU found for - Material Type Code: {} Color Code: {}".format(type_code, color_code))
            return "Unknown"
        elif len(sku) == 1:
            return sku[0][0]
        else:
            print("Multiple SKUs found for - Material Type Code: {} Color Code: {}".format(type_code, color_code))
            print(sku)
            return "Unknown"           

    def get_mat_inventory_name(self, sku=""):
        if sku:
            mat_sku = sku
        else:
            mat_sku = self.get_mat_sku(None, None, None)
        
        mat_name = snap_db.query_db(
            "SELECT\
                Name\
            FROM\
                CCItems\
            WHERE\
                SKU == '{sku}';\
            ".format(sku=mat_sku)
        )

        if len(mat_name) == 0:
            print("No Name found for - Material SKU: {sku}".format(sku=mat_sku))
            return "Unknown"
        elif len(mat_name) == 1:
            return mat_name[0][0]
        else:
            print("Multiple Names found for - Material SKU: {sku}".format(sku=mat_sku))
            print(mat_name)
            return "Unknown"           

    def get_stain_color(self):
        return self.stain_colors[self.stain_color_index]

    def get_glaze_color(self):
        return self.glaze_colors[self.glaze_color_index]

    def get_glaze_style(self):
        return self.glaze_styles[self.glaze_style_index]

    def get_drawer_slide_type(self):
        return self.drawer_slides[self.drawer_slide_index]

    def draw(self, layout):
        c_box = layout.box()

        self.edges.draw(c_box)
        self.secondary_edges.draw(c_box)
        self.materials.draw(c_box)
        self.countertops.draw(c_box)

        #Stain     
        box = c_box.box()
        box.label("Stain Color Selection:")

        if len(self.stain_colors) > 0:
            active_stain_color = self.get_stain_color()

            row = box.row(align=True)
            split = row.split(percentage=0.25)
            split.label("Color:")        
            split.menu('MENU_Stain_Colors', text=active_stain_color.name, icon='SOLO_ON')
            
            if active_stain_color.name != "None":
                active_glaze_color = self.get_glaze_color()
                row = box.row(align=True)
                split = row.split(percentage=0.25)
                split.label("Glaze Color:")              
                split.menu('MENU_Glaze_Colors', text=active_glaze_color.name, icon='SOLO_ON')

                if active_glaze_color.name != "None":
                    active_glaze_style = self.get_glaze_style()
                    row = box.row(align=True)
                    split = row.split(percentage=0.25)
                    split.label("Glaze Style:")                
                    split.menu('MENU_Glaze_Styles', text=active_glaze_style.name, icon='SOLO_ON')
            
        else:
            row = box.row()
            row.label("None", icon='ERROR')            

        #Moderno Doors
        box = c_box.box()
        box.label("Moderno Door Color Selection:")

        if len(self.moderno_colors) > 0:
            active_door_color = self.moderno_colors[self.moderno_color_index]

            row = box.row(align=True)
            split = row.split(percentage=0.25)
            split.label("Color:")        
            split.menu('MENU_Door_Colors', text=active_door_color.name, icon='SOLO_ON')

        else:
            row = box.row()
            row.label("None", icon='ERROR')               
        
        #Glass
        box = c_box.box()
        box.label("Glass Inset Color Selection:")

        if len(self.glass_colors):        
            active_glass_color = self.glass_colors[self.glass_color_index]

            row = box.row(align=True)
            split = row.split(percentage=0.25)
            split.label("Color:")
            split.menu('MENU_Glass_Colors', text=active_glass_color.name, icon='SOLO_ON')
        else:
            row = box.row()
            row.label("None", icon='ERROR')                

        #Wire Basket
        box = c_box.box()
        box.label("Hardware:")
        col = box.column()
        row = col.row(align=True)
        split = row.split(percentage=0.40)
        split.label("Wire Basket Color:")
        split.prop(self, "wire_basket_colors", text="")
        row = col.row(align=True)
        split = row.split(percentage=0.40)
        split.label("KD Fitting Color:")
        split.prop(self, "kd_fitting_color", text="")

        row = c_box.row()
        row.scale_y = 1.5
        row.operator("db_materials.poll_assign_materials", text="Update Materials", icon='FILE_REFRESH')


    
def register():
    bpy.utils.register_class(PANEL_Closet_Materials_Interface)
    bpy.utils.register_class(PROPERTIES_Closet_Materials)    
    bpy.types.Scene.db_materials = bpy.props.PointerProperty(type=PROPERTIES_Closet_Materials)


def unregister():
    bpy.utils.unregister_class(PANEL_Closet_Materials_Interface)
    bpy.utils.unregister_class(PROPERTIES_Closet_Materials)

