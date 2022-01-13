import bpy
from bpy.types import (
    Panel,
    PropertyGroup,
)
from bpy.props import (
    IntProperty,
    BoolProperty,
    PointerProperty,
    CollectionProperty,
    EnumProperty,
)
from snap import sn_unit
from snap import sn_db
from snap import sn_utils
from snap.material_manager import property_groups


enum_items_kd_fitting = []
enum_items_location_code = []


def update_stain_color(self, context):
    if not self.main_tabs == 'STAIN':
        return
    else:
        mat_color_name = self.materials.get_mat_color().name
        stain_colors = self.get_stain_colors()

        if mat_color_name in stain_colors:
            self.stain_color_index = self.stain_colors.find(mat_color_name)
            return
        if mat_color_name == "Cabinet Almond":
            self.stain_color_index = self.stain_colors.find("Almond")
            return
        else:
            self.stain_color_index = self.stain_colors.find("Oxford White")
            bpy.ops.snap.message_box(
                'INVOKE_DEFAULT',
                message='"{}" is not an available stain color!'.format(mat_color_name),
                icon='INFO')


def update_material_and_edgeband_colors(self, context):
    mat_color_name = self.materials.get_mat_color().name
    mat_type = self.materials.get_mat_type()
    stain_colors = self.get_stain_colors()
    moderno_colors = self.get_moderno_colors()

    if not self.use_custom_color_scheme and self.defaults_set:
        self.set_all_material_colors()

    if mat_type.name == "Melamine":
        if mat_color_name in stain_colors:
            self.stain_color_index = self.stain_colors.find(mat_color_name)
            return
        if mat_color_name == "Cabinet Almond":
            self.stain_color_index = self.stain_colors.find("Almond")
            return
        else:
            self.stain_color_index = self.stain_colors.find("Oxford White")
    elif mat_type.name == 'Textured Melamine':
        if mat_color_name in moderno_colors:
            self.moderno_color_index = self.moderno_colors.find(mat_color_name)
            return

    try:
        bpy.ops.closet_materials.poll_assign_materials()
    except Exception:
        pass


def update_render_materials(self, context):
    try:
        bpy.ops.closet_materials.poll_assign_materials()
    except Exception:
        pass


def enum_kd_fitting(self, context):
    if context is None:
        return []

    if len(enum_items_kd_fitting) > 1:
        return enum_items_kd_fitting

    else:
        conn = sn_db.connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT\
                *\
            FROM\
                {CCItems}\
            WHERE\
                ProductType == 'HW' AND\
                Name LIKE '{}'\
            ;".format("%" + "KD - FF" + "%", CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )

        rows = cursor.fetchall()

        for row in rows:
            enum_items_kd_fitting.append((row[0], row[2], row[2]))

        conn.close()

        return enum_items_kd_fitting


class SN_MAT_PT_Closet_Materials_Interface(Panel):
    """Panel to Store all of the Material Options"""
    bl_label = "Room Materials"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 4

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='MATERIAL')

    def draw(self, context):
        layout = self.layout
        props = context.scene.closet_materials
        props.draw(layout)


class Edges(PropertyGroup):
    edge_types: bpy.props.StringProperty(name="Edge Types")


class SnapMaterialSceneProps(PropertyGroup):
    """
    Closet Materials
    """
    main_tabs: EnumProperty(
        name="Closet Material Tabs",
        items=[('MATERIAL', "Material", ""),
               ('COUNTERTOP', "Countertop", ""),
               ('HARDWARE', "Hardware", ""),
               ('DOORS_AND_DRAWER_FACES', "Upgraded Door & Drawer Faces", ""),
               ('MOLDING',"Molding",'Show the molding options.'),
               ('GLASS', "Glass", "")],
        default='MATERIAL',
        update=update_stain_color)

    use_custom_color_scheme: BoolProperty(
        name="Use Custom edge and color scheme",
        description="Use Custom edge and color scheme.",
        default=False,
        update=update_material_and_edgeband_colors)

    default_color = "Oxford White"
    default_edge_color = "Oxford White"
    default_mat_type = "Melamine"
    default_edge_type = "1mm Dolce"
    defaults_set: BoolProperty(name="Default materials have been set", default=False)

    materials: PointerProperty(type=property_groups.Materials)
    mat_type_index: IntProperty(name="Material Type Index", default=0)
    mat_color_index: IntProperty(name="Material Color Index", default=0, update=update_material_and_edgeband_colors)

    edges: PointerProperty(type=property_groups.Edges)
    edge_type_index: IntProperty(name="Edge Type Index", default=0)
    edge_color_index: IntProperty(name="Edge Color Index", default=0, update=update_render_materials)

    secondary_edges: PointerProperty(type=property_groups.SecondaryEdges)
    secondary_edge_type_index: IntProperty(name="Secondary Edge Type Index", default=0)
    secondary_edge_color_index: IntProperty(name=" Secondary Edge Color Index", default=0, update=update_render_materials)

    door_drawer_edges: PointerProperty(type=property_groups.DoorDrawerEdges)
    door_drawer_edge_type_index: IntProperty(name="Door/Drawer Edge Type Index", default=0)
    door_drawer_edge_color_index: IntProperty(name="Door/Drawer Edge Color Index", default=0, update=update_render_materials)

    door_drawer_materials: PointerProperty(type=property_groups.DoorDrawerMaterials)
    door_drawer_mat_type_index: IntProperty(name="Door/Drawer Material Type Index", default=0)
    door_drawer_mat_color_index: IntProperty(name="Door/Drawer Material Color Index", default=0, update=update_render_materials)

    countertops: PointerProperty(type=property_groups.Countertops)
    ct_type_index: IntProperty(name="Countertop Type Index", default=0)
    ct_mfg_index: IntProperty(name="Countertop Manufactuer Index", default=0)
    ct_color_index: IntProperty(name="Countertop Color Index", default=0, update=update_render_materials)

    stain_colors: CollectionProperty(type=property_groups.StainColor)
    stain_color_index: IntProperty(name="Stain Color List Index", default=15, update=update_render_materials)

    glaze_colors: CollectionProperty(type=property_groups.GlazeColor)
    glaze_color_index: IntProperty(name="Glaze Color List Index", default=0, update=update_render_materials)
    glaze_styles: CollectionProperty(type=property_groups.GlazeStyle)
    glaze_style_index: IntProperty(name="Glaze Style List Index", default=0)

    moderno_colors: CollectionProperty(type=property_groups.DoorColor)
    moderno_color_index: IntProperty(name="Door Color List Index", default=0, update=update_render_materials)

    glass_colors: CollectionProperty(type=property_groups.GlassColor)
    glass_color_index: IntProperty(name="Glass Color List Index", default=0, update=update_render_materials)

    backing_veneer_color: CollectionProperty(type=property_groups.BackingVeneerColor)

    wire_basket_colors: EnumProperty(
        name="Wire Basket Color",
        items=(
            ('CHROME', 'Chrome', "Chrome"),
            ('WHITE', 'White', "White")
        ),
        default='CHROME'
    )

    kd_fitting_color: EnumProperty(
        name="KD Fitting Color",
        items=enum_kd_fitting,
    )

    drawer_slides: CollectionProperty(type=property_groups.DrawerSlide)
    drawer_slide_index: IntProperty(name="Drawer Slide List Index", default=0)

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

        name = sn_db.query_db(
            "SELECT\
                Name\
            FROM\
                {CCItems}\
            WHERE ProductType = 'EB' AND TypeCode = '{type_code}' AND ColorCode = '{color_code}';\
            ".format(type_code=type_code, color_code=color_code, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )

        if len(name) == 0:
            print(
                "No SKU found for - Edge Type Code: {} Color Code: {}".format(type_code, color_code))
            return "Unknown"
        elif len(name) == 1:
            return name[0][0]
        else:
            print(
                "Multiple SKUs found for - Edge Type Code: {} Color Code: {}".format(type_code, color_code))
            print(name)
            return "Unknown"

    def get_edge_sku(self, obj=None, assembly=None, part_name=None):
        type_code = self.edges.get_edge_type().type_code
        color_code = self.edges.get_edge_color().color_code
        obj_props = assembly.obj_bp.sn_closets


        # There is no edgebanding for garage colors, so we have to hardcode in alternate edgebanding.
        if self.materials.get_mat_type().type_code == 1:
            sku = self.get_garage_edge_sku(obj, assembly, part_name)
            if sku != "Unknown":
                return sku
            color_name = self.materials.get_mat_color().name
            if color_name == "Duraply Almond":
                return "EB-0000326"
            elif color_name == "Fog Grey":
                return "EB-0000331"
            elif color_name == "Graphite Spectrum":
                return "EB-0000324"
            elif color_name == "Hardrock Maple":
                return "EB-0000333"
            else:
                return "EB-0000338"

        door_drawer_parts = [
            obj_props.is_door_bp,
            obj_props.is_drawer_front_bp,
            obj_props.is_hamper_front_bp
        ]

        if any(door_drawer_parts):
            type_code = self.door_drawer_edges.get_edge_type().type_code
            color_code = self.door_drawer_edges.get_edge_color().color_code

        sku = sn_db.query_db(
            "SELECT\
                SKU\
            FROM\
                {CCItems}\
            WHERE ProductType = 'EB' AND TypeCode = '{type_code}' AND ColorCode = '{color_code}';\
            ".format(type_code=type_code, color_code=color_code, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )

        if len(sku) == 0:
            print(
                "No SKU found for - Edge Type Code: {} Color Code: {}".format(type_code, color_code))
            return "Unknown"
        elif len(sku) == 1:
            return sku[0][0]
        else:
            print(
                "Multiple SKUs found for - Edge Type Code: {} Color Code: {}".format(type_code, color_code))
            print(sku)
            return "Unknown"

    def get_secondary_edge_sku(self, obj=None, assembly=None, part_name=None):
        type_code = self.secondary_edges.get_edge_type().type_code
        color_code = self.secondary_edges.get_edge_color().color_code

        # There is no edgebanding for garage colors, so we have to hardcode in alternate edgebanding.
        if self.materials.get_mat_type().type_code == 1:
            sku = self.get_garage_edge_sku(obj, assembly, part_name)
            if sku != "Unknown":
                return sku
            color_name = self.materials.get_mat_color().name
            if color_name == "Duraply Almond":
                return "EB-0000326"
            elif color_name == "Fog Grey":
                return "EB-0000331"
            elif color_name == "Graphite Spectrum":
                return "EB-0000324"
            elif color_name == "Hardrock Maple":
                return "EB-0000333"
            else:
                return "EB-0000338"

        sku = sn_db.query_db(
            "SELECT\
                SKU\
            FROM\
                {CCItems}\
            WHERE ProductType = 'EB' AND TypeCode = '{type_code}' AND ColorCode = '{color_code}';\
            ".format(type_code=type_code, color_code=color_code, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
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

    def get_edge_inventory_name(self, sku=""):
        if sku:
            edge_sku = sku
        else:
            edge_sku = self.get_edge_sku(None, None, None)

        edge_name = sn_db.query_db(
            "SELECT\
                DisplayName\
            FROM\
                {CCItems}\
            WHERE\
                SKU == '{sku}';\
            ".format(sku=edge_sku, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )

        if len(edge_name) == 0:
            print(
                "No Name found for - Material SKU: {sku}".format(sku=edge_sku))
            return "Unknown"
        elif len(edge_name) == 1:
            return edge_name[0][0]
        else:
            print(
                "Multiple Names found for - Material SKU: {sku}".format(sku=edge_sku))
            print(edge_name)
            return "Unknown"

    def get_garage_edge_sku(self, obj=None, assembly=None, part_name=None):
        part_thickness = 0
        type_code = self.edges.get_edge_type().type_code
        cutpart_name = ""
        mat_type = self.materials.get_mat_type()

        interior_edged_parts = [
            "Garage_Interior_Shelf",
            "Garage_Cleat",
            "Garage_Cover_Cleat"
        ]

        if assembly:
            for child in assembly.obj_bp.children:
                if child.snap.type_mesh == 'CUTPART':
                    cutpart_name = child.snap.cutpart_name

        if obj:
            part_thickness = sn_unit.meter_to_inch(sn_utils.get_part_thickness(obj))
            if obj.snap.type_mesh == 'CUTPART':
                cutpart_name = obj.snap.cutpart_name

        
        # This is to look for our 1" thick white edgebanding
        if part_thickness == 1:
            sku = sn_db.query_db(
                "SELECT\
                    SKU\
                FROM\
                    {CCItems}\
                WHERE ProductType = 'EB' AND TypeCode = '{type_code}' AND ColorCode = {color_code};\
                ".format(type_code=3047, color_code = 110100, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
            )
            if len(sku) == 0:
                print(
                    "No SKU found for - Edgeband Type Code: {} Oxford White".format(type_code))
                return "Unknown"
            elif len(sku) == 1:
                return sku[0][0]
            else:
                print(
                    "Multiple SKUs found for - Edgeband Type Code: {} Oxford White".format(type_code))
                print(sku)
                return "Unknown"


        if cutpart_name in interior_edged_parts:
            sku = sn_db.query_db(
                "SELECT\
                    SKU\
                FROM\
                    {CCItems}\
                WHERE ProductType = 'EB' AND TypeCode = '{type_code}' AND DisplayName LIKE 'Oxford White';\
                ".format(type_code=type_code, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
            )
            if len(sku) == 0:
                print(
                    "No SKU found for - Edgeband Type Code: {} Oxford White".format(type_code))
                return "Unknown"
            elif len(sku) == 1:
                return sku[0][0]
            else:
                print(
                    "Multiple SKUs found for - Edgeband Type Code: {} Oxford White".format(type_code))
                print(sku)
                return "Unknown"
        else:
            return "Unknown"

    def get_mat_sku(self, obj=None, assembly=None, part_name=None):
        mat_type = self.materials.get_mat_type()
        type_code = mat_type.type_code
        color_code = self.materials.get_mat_color().color_code
        color_name = self.materials.get_mat_color().name
        part_thickness = 0

        # Type Code 1 is a temp code for garage materials because garage materials share 15200 with standard melamine material
        if type_code == 1:
            sku = self.get_garage_material_sku(obj, assembly, part_name)
            if sku != "Unknown":
                return sku
            type_code = 15200

        if type_code == 15225 and (color_name != "Oxford White" and color_name != "Cabinet Almond"):  # Need to change type code for oversized materials that are not White or Almond to the Textured Type Code
            type_code = 15150

        if obj:
            part_thickness = sn_unit.meter_to_inch(sn_utils.get_part_thickness(obj))

        if assembly:
            obj_props = assembly.obj_bp.sn_closets

            drawer_box_parts = [
                obj_props.is_drawer_back_bp,
                obj_props.is_drawer_side_bp,
                obj_props.is_drawer_bottom_bp,
                obj_props.is_drawer_sub_front_bp
            ]

            backing_parts = [
                obj_props.is_back_bp,
                obj_props.is_top_back_bp,
                obj_props.is_bottom_back_bp
            ]

            door_drawer_parts = [
                obj_props.is_door_bp,
                obj_props.is_drawer_front_bp,
                obj_props.is_hamper_front_bp
            ]

            glass_shelf_parts = [
                obj_props.is_glass_shelf_bp
            ]

            countertop_parts = [
                obj_props.is_countertop_bp,
                obj_props.is_hpl_top_bp
            ]

            if any(door_drawer_parts):
                door_style = assembly.get_prompt("Door Style")
                if door_style:
                    if door_style.get_value() != "Slab Door":
                        if self.get_stain_color().name != 'None':
                            return self.get_stain_color().sku
                mat_type = self.door_drawer_materials.get_mat_type()
                type_code = mat_type.type_code
                color_code = self.door_drawer_materials.get_mat_color().color_code
                color_name = self.door_drawer_materials.get_mat_color().name

            if any(backing_parts):
                if obj_props.use_unique_material:
                    if obj_props.unique_mat_types == 'MELAMINE':
                        mat_type = self.materials.mat_types['Melamine']
                        mat_name = obj_props.unique_mat_mel

                    if obj_props.unique_mat_types == 'TEXTURED_MELAMINE':
                        mat_type = self.materials.mat_types['Textured Melamine']
                        mat_name = obj_props.unique_mat_tex_mel

                    if obj_props.unique_mat_types == 'VENEER':
                        mat_type = self.materials.mat_types['Veneer']
                        mat_name = obj_props.unique_mat_veneer

                    color_code = mat_type.colors[mat_name].color_code

            if any(drawer_box_parts):
                use_dovetail_construction = assembly.get_prompt("Use Dovetail Construction")
                if use_dovetail_construction:
                    if use_dovetail_construction.get_value():
                        if obj_props.is_drawer_bottom_bp:
                            sku = 'BB-0000004'  # WHITE PAPER 3/8 G1
                        else:
                            material_name = 'BBBB PREFINISH RIP ' + str(round(sn_unit.meter_to_inch(assembly.obj_y.location.y), 2))
                            sku = sn_db.query_db(
                                "SELECT\
                                    SKU\
                                FROM\
                                    {CCItems}\
                                WHERE\
                                    ProductType IN ('BB') AND\
                                    Name LIKE '%{material_name}%' \
                                ;\
                                ".format(CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location, material_name=material_name)
                            )

                            if len(sku) == 0:
                                # print("No SKU Found for: ", material_name)
                                # print()
                                return "Unknown"
                            elif len(sku) == 1:
                                # print("Found One SKU for: ", material_name)
                                # print()
                                return sku[0][0]
                            else:
                                print("Multiple SKUs found for: ", material_name)
                                print(sku)
                                print()
                                return "Unknown"
                    else:
                        if obj_props.is_drawer_bottom_bp:
                            sku = 'PM-0000002'  # WHITE PAPER 3/8 G1
                        else:
                            sku = 'PM-0000004'  # WHITE  PAPER 1/2 G2
                else:
                    if obj_props.is_drawer_bottom_bp:
                        sku = 'PM-0000002'  # WHITE PAPER 3/8 G1
                    else:
                        sku = 'PM-0000004'  # WHITE  PAPER 1/2 G2
                return sku

            if any(glass_shelf_parts):
                glass_color = self.glass_colors[self.glass_color_index].name
                part_thickness = round(part_thickness, 2)
                sku = sn_db.query_db(
                    "SELECT\
                        SKU\
                    FROM\
                        {CCItems}\
                    WHERE\
                        ProductType IN ('GL') AND\
                        Thickness == '{thickness}' AND\
                        Name LIKE '%{glass_color}%'\
                    ;\
                    ".format(glass_color=glass_color, thickness=part_thickness, color_code=color_code, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
                )

                if glass_color == 'None':
                    print("Glass color not selected. Sku determined by thickness: {}".format(part_thickness))
                    if part_thickness == 0.13:
                        return 'GL-0000003'
                    if part_thickness == 0.25:
                        return 'GL-0000004'
                    if part_thickness == 0.38:
                        return 'GL-0000006'
                    if part_thickness == 0.5:
                        return "GL-0000008"
                if len(sku) == 0:
                    print("SKU match not found for selected glass parts - Glass Color: {} Material Thickness: {}".format(glass_color, part_thickness))
                    print("Special order Sku returned: SO-0000001")
                    return 'SO-0000001'
                elif len(sku) == 1:
                    return sku[0][0]
                else:
                    print("Multiple SKUs found for - Glass Color: {} Material Thickness: {}".format(glass_color, part_thickness))
                    print("Default sku returned: " + str(sku[0][0]))
                    return sku[0][0]

            if any(countertop_parts):
                if part_name is not None and 'Melamine' not in part_name:
                    return 'SO-0000001'
            
            if obj_props.is_crown_molding:
                sku = sn_db.query_db(
                    "SELECT\
                        SKU\
                    FROM\
                        {CCItems}\
                    WHERE\
                        ProductType == 'MD' AND\
                        DisplayName == '{molding_name}'\
                    ;\
                    ".format(molding_name=part_name, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
                )

                if len(sku) == 0:
                    print(
                        "No SKU found for - Molding Name: {}".format(part_name))
                    return "Unknown"
                elif len(sku) == 1:
                    return sku[0][0]
                else:
                    print("Multiple SKUs found for - Molding Name: {} ".format(part_name))
                    print(sku)
                    return "Unknown"
                # if part_name == "Traditional Large":
                #     return "MD-0000004"
                # elif part_name == "Traditional Small":
                #     return "MD-0000007"
                # else:
                #     return ""

        if part_thickness == 0.25:
            if any(backing_parts) or obj_props.is_toe_kick_skin_bp:
                shared_sku_colors = [
                    'Oxford White',
                    'Cabinet Almond',
                    'Duraply White',
                    'Duraply Almond'
                ]

                if color_name in shared_sku_colors:
                    sku = 'PM-0000041'
                    return sku

            sku = sn_db.query_db(
                "SELECT\
                    SKU\
                FROM\
                    {CCItems}\
                WHERE\
                    ProductType IN ('PM', 'WD') AND\
                    Thickness == '{thickness}' AND\
                    ColorCode == '{color_code}'\
                ;\
                ".format(thickness=str(part_thickness), color_code=color_code, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
            )

            if len(sku) == 0:
                print(
                    "No SKU found for - Material Thickness: {} Color Code: {}".format(part_thickness, color_code))
                return "Unknown"
            elif len(sku) == 1:
                return sku[0][0]
            else:
                print("Multiple SKUs found for - Material Thickness: {} Color Code: {}".format(
                    part_thickness, color_code))
                print(sku)
                return "Unknown"

        if part_thickness == 0.375:
            sku = sn_db.query_db(
                "SELECT\
                    SKU\
                FROM\
                    {CCItems}\
                WHERE\
                    ProductType IN ('PM', 'WD') AND\
                    Thickness == '{thickness}' AND\
                    ColorCode == '{color_code}'\
                ;\
                ".format(thickness=str(part_thickness), color_code=color_code, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
            )

            if len(sku) == 0:
                # Use 0.75 material if 0.375 sku not found
                part_thickness = 0.75
            elif len(sku) == 1:
                return sku[0][0]
            else:
                print("Multiple SKUs found for - Material Thickness: {} Color Code: {}".format(
                    part_thickness, color_code))
                print(sku)
                return "Unknown"

        if part_thickness == 0.75 or part_thickness == 0:
                sku = sn_db.query_db(
                    "SELECT\
                        SKU\
                    FROM\
                        {CCItems}\
                    WHERE ProductType in ('PM', 'WD') AND TypeCode = '{type_code}' AND ColorCode = '{color_code}';\
                    ".format(type_code=type_code, color_code=color_code, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
                )

                if len(sku) == 0:
                    print(
                        "No SKU found for - Material Type Code: {} Color Code: {}".format(type_code, color_code))
                    return "Unknown"
                elif len(sku) == 1:
                    return sku[0][0]
                else:
                    print(
                        "Multiple SKUs found for - Material Type Code: {} Color Code: {}".format(type_code, color_code))
                    print(sku)
                    return "Unknown"
    
    def get_garage_material_sku(self, obj=None, assembly=None, part_name=None):
        part_thickness = 0
        cutpart_name = ""
        mat_type = self.materials.get_mat_type()
        type_code = 15200
        color_code = self.materials.get_mat_color().color_code
        color_name = self.materials.get_mat_color().name

        exterior_parts = [
            "Garage_End_Panel",
            "Garage_Slab_Door",
            "Garage_Bottom_KD",
            "Garage_Top_KD",
            "Garage_Slab_Drawer_Front"
        ]

        interior_parts = [
            "Garage_Mid_Panel",
            "Garage_Interior_Shelf",
            "Garage_Back",
            "Garage_Interior_KD",
            "Garage_Cover_Cleat",
            "Garage_Cleat"
        ]

        if assembly:
            obj_props = assembly.obj_bp.sn_closets

            backing_parts = [
                obj_props.is_back_bp,
                obj_props.is_top_back_bp,
                obj_props.is_bottom_back_bp
            ]
            
            if any(backing_parts):
                if obj_props.use_unique_material:
                    return "Unknown"

            for child in assembly.obj_bp.children:
                if child.snap.type_mesh == 'CUTPART':
                    cutpart_name = child.snap.cutpart_name
                    # for mat_slot in child.snap.material_slots:
                    #     print("Current Material Slot: ", mat_slot)
                    #     print("Current Material Slot Name: ", mat_slot.name)
                    #     print("Current Material Slot Item Name: ", mat_slot.item_name)
                    #     # print("Current Material Slot Material: ", mat_slot.material)


        if obj:
            part_thickness = sn_unit.meter_to_inch(sn_utils.get_part_thickness(obj))
            if obj.snap.type_mesh == 'CUTPART':
                cutpart_name = obj.snap.cutpart_name

        if part_thickness == 0 or part_thickness == 0.38:
            part_thickness = 0.75

        if part_thickness == 1:
            return "PM-0000475"

        if cutpart_name in exterior_parts:
            sku = sn_db.query_db(
                "SELECT\
                    SKU\
                FROM\
                    {CCItems}\
                WHERE ProductType in ('PM', 'WD') AND TypeCode = '{type_code}' AND ColorCode LIKE '{color_code}';\
                ".format(type_code=type_code, color_code=color_code, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
            )

            if len(sku) == 0:
                print(
                    "No SKU found for - Material Type Code: {} Color Code: {}".format(type_code, color_code))
                return "Unknown"
            elif len(sku) == 1:
                return sku[0][0]
            else:
                print(
                    "Multiple SKUs found for - Material Type Code: {} Color Code: {}".format(type_code, color_code))
                print(sku)
                return "Unknown"

        elif cutpart_name in interior_parts:
            sku = sn_db.query_db(
                "SELECT\
                    SKU\
                FROM\
                    {CCItems}\
                WHERE ProductType in ('PM', 'WD') AND TypeCode = '{type_code}' AND DisplayName LIKE '{display_name}' AND Thickness = '{part_thickness}';\
                ".format(type_code=type_code, display_name="Oxford White", part_thickness=part_thickness, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
            )

            if len(sku) == 0:
                print(
                    "No SKU found for - Material Type Code: {} Display Name: {} Part Thickness: {}".format(type_code, "Oxford White", part_thickness))
                return "Unknown"
            elif len(sku) == 1:
                return sku[0][0]
            else:
                print(
                    "Multiple SKUs found for - Material Type Code: {} Display Name: {} Part Thickness: {}".format(type_code, "Oxford White", part_thickness))
                print(sku)
                return "Unknown"
        else:
            return "Unknown"

    def get_mat_inventory_name(self, sku=""):
        if sku:
            mat_sku = sku
        else:
            mat_sku = self.get_mat_sku(None, None, None)

        mat_name = sn_db.query_db(
            "SELECT\
                Name\
            FROM\
                {CCItems}\
            WHERE\
                SKU == '{sku}';\
            ".format(sku=mat_sku, CCItems="CCItems_" + bpy.context.preferences.addons['snap'].preferences.franchise_location)
        )

        if len(mat_name) == 0:
            print(
                "No Name found for - Material SKU: {sku}".format(sku=mat_sku))
            return "Unknown"
        elif len(mat_name) == 1:
            return mat_name[0][0]
        else:
            print(
                "Multiple Names found for - Material SKU: {sku}".format(sku=mat_sku))
            print(mat_name)
            return "Unknown"

    def get_stain_color(self):
        return self.stain_colors[self.stain_color_index]

    def get_stain_colors(self):
        return [color.name for color in self.stain_colors]

    def get_moderno_colors(self):
        return [color.name for color in self.moderno_colors]

    def get_glaze_color(self):
        return self.glaze_colors[self.glaze_color_index]

    def get_glaze_style(self):
        return self.glaze_styles[self.glaze_style_index]

    def get_glass_color(self):
        return self.glass_colors[self.glass_color_index]

    def get_drawer_slide_type(self):
        return self.drawer_slides[self.drawer_slide_index]

    def set_all_edge_colors(self, mat_color):
        for type_index, edge_type in enumerate(self.edges.edge_types):
            if mat_color.name in edge_type.colors:
                color_index = edge_type.colors.find(mat_color.name)
                self.edge_type_index = type_index
                self.secondary_edge_type_index = type_index
                self.door_drawer_edge_type_index = type_index
                self.edge_color_index = color_index
                self.secondary_edge_color_index = color_index
                self.door_drawer_edge_color_index = color_index
                break

    def set_all_material_colors(self):
        material_type = self.materials.get_mat_type()
        material_color = self.materials.get_mat_color()
        self.door_drawer_mat_type_index = self.door_drawer_materials.mat_types.find(material_type.name)
        door_drawer_mat_type = self.door_drawer_materials.get_mat_type()
        self.door_drawer_mat_color_index = door_drawer_mat_type.colors.find(material_color.name)
        self.set_all_edge_colors(material_color)

    def set_defaults(self):
        self.set_default_material_type()
        self.set_default_edge_type()
        self.set_default_material_color()
        self.set_default_dd_material_color()
        self.set_default_edge_color()
        self.set_default_secondary_edge_color()
        self.set_default_door_drawer_edge_color()
        self.defaults_set = True

    def set_default_material_type(self):
        for i, type in enumerate(self.materials.mat_types):
            if type.name == self.default_mat_type:
                self.mat_type_index = i
                break
        for i, type in enumerate(self.door_drawer_materials.mat_types):
            if type.name == self.default_mat_type:
                self.door_drawer_mat_type_index = i
                break

    def set_default_edge_type(self):
        self.edge_type_index = self.edges.edge_types.find(self.default_edge_type)
        self.secondary_edge_type_index = self.secondary_edges.edge_types.find(self.default_edge_type)
        self.door_drawer_edge_type_index = self.door_drawer_edges.edge_types.find(self.default_edge_type)

    def set_default_material_color(self):
        mat_type = self.materials.get_mat_type()
        color_idx = mat_type.colors.find(self.default_color)

        if color_idx:
            self.mat_color_index = color_idx
        else:
            self.mat_color_index = 0

    def set_default_dd_material_color(self):
        door_drawer_mat_type = self.door_drawer_materials.get_mat_type()
        door_drawer_color_idx = door_drawer_mat_type.colors.find(self.default_color)

        if door_drawer_color_idx:
            self.door_drawer_mat_color_index = door_drawer_color_idx
        else:
            self.door_drawer_mat_color_index = 0

    def set_default_edge_color(self):
        edge_type = self.edges.get_edge_type()
        color_idx = edge_type.colors.find(self.default_edge_color)

        if color_idx:
            self.edge_color_index = color_idx
        else:
            self.edge_color_index = 0

    def set_default_secondary_edge_color(self):
        secondary_edge_type = self.secondary_edges.get_edge_type()
        color_idx = secondary_edge_type.colors.find(self.default_edge_color)

        if color_idx:
            self.secondary_edge_color_index = color_idx
        else:
            self.secondary_edge_color_index = 0

    def set_default_door_drawer_edge_color(self):
        edge_type = self.door_drawer_edges.get_edge_type()
        color_idx = edge_type.colors.find(self.default_edge_color)

        if color_idx:
            self.door_drawer_edge_color_index = color_idx
        else:
            self.door_drawer_edge_color_index = 0

    def draw(self, layout):
        options = bpy.context.scene.sn_closets.closet_options
        c_box = layout.box()
        tab_col = c_box.column(align=True)
        row = tab_col.row(align=True)
        row.prop_enum(self, "main_tabs", 'MATERIAL')
        row.prop_enum(self, "main_tabs", 'COUNTERTOP')
        row.prop_enum(self, "main_tabs", 'HARDWARE')
        row = tab_col.row(align=True)
        row.prop_enum(self, "main_tabs", 'MOLDING')
        row.prop_enum(self, "main_tabs", 'GLASS')
        row = tab_col.row(align=True)
        row.prop_enum(self, "main_tabs", 'DOORS_AND_DRAWER_FACES')

        if self.main_tabs == 'MATERIAL':
            if self.use_custom_color_scheme:
                self.materials.draw(c_box)
                self.edges.draw(c_box)
                self.secondary_edges.draw(c_box)
                box = c_box.box()
                box.label(text="Doors/Drawer Faces:")
                self.door_drawer_edges.draw(box)
                self.door_drawer_materials.draw(box)

                box = c_box.box()
                box.label(text="Stain Color Selection:")

                if len(self.stain_colors) > 0:
                    active_stain_color = self.get_stain_color()
                    row = box.row(align=True)
                    split = row.split(factor=0.25)
                    split.label(text="Color:")
                    split.menu(
                        'SNAP_MATERIAL_MT_Stain_Colors',
                        text=active_stain_color.name, icon='RADIOBUT_ON')

                    if active_stain_color.name != "None":
                        active_glaze_color = self.get_glaze_color()
                        row = box.row(align=True)
                        split = row.split(factor=0.25)
                        split.label(text="Glaze Color:")
                        split.menu(
                            'SNAP_MATERIAL_MT_Glaze_Colors',
                            text=active_glaze_color.name, icon='RADIOBUT_ON')

                        if active_glaze_color.name != "None":
                            active_glaze_style = self.get_glaze_style()
                            row = box.row(align=True)
                            split = row.split(factor=0.25)
                            split.label(text="Glaze Style:")
                            split.menu(
                                'SNAP_MATERIAL_MT_Glaze_Styles',
                                text=active_glaze_style.name, icon='RADIOBUT_ON')
                else:
                    row = box.row()
                    row.label(text="None", icon='ERROR')

                box = c_box.box()
                box.label(text="Moderno Door Color Selection:")

                if len(self.moderno_colors) > 0:
                    active_door_color = self.moderno_colors[self.moderno_color_index]
                    row = box.row(align=True)
                    split = row.split(factor=0.25)
                    split.label(text="Color:")
                    split.menu(
                        'SNAP_MATERIAL_MT_Door_Colors',
                        text=active_door_color.name, icon='RADIOBUT_ON')
                else:
                    row = box.row()
                    row.label(text="None", icon='ERROR')
            else:
                self.materials.draw(c_box)
            c_box.prop(self, "use_custom_color_scheme")

        if self.main_tabs == 'COUNTERTOP':
            self.countertops.draw(c_box)

        if self.main_tabs == 'GLASS':
            box = c_box.box()
            box.label(text="Glass Inset Color Selection:")

            if len(self.glass_colors):
                active_glass_color = self.glass_colors[self.glass_color_index]
                row = box.row(align=True)
                split = row.split(factor=0.25)
                split.label(text="Color:")
                split.menu(
                    'SNAP_MATERIAL_MT_Glass_Colors',
                    text=active_glass_color.name, icon='RADIOBUT_ON')
            else:
                row = box.row()
                row.label(text="None", icon='ERROR')

        if self.main_tabs == 'MOLDING':
            options.draw_molding_options(c_box)

        if self.main_tabs == 'DOORS_AND_DRAWER_FACES':
            options.draw_door_options(c_box)

        if self.main_tabs == 'HARDWARE':
            box = c_box.box()
            box.label(text="Hardware:")
            options.draw_hardware_options(box)
            col = box.column()
            row = col.row(align=True)
            split = row.split(factor=0.40)
            split.label(text="Wire Basket Color:")
            split.prop(self, "wire_basket_colors", expand=True)
            row = col.row(align=True)
            split = row.split(factor=0.40)
            split.label(text="KD Fitting Color:")
            split.prop(self, "kd_fitting_color", text="")
            row = c_box.row()
            row.scale_y = 1.5
            

        c_box.operator(
            "closet_materials.poll_assign_materials",
            text="Update Materials", icon='FILE_REFRESH')

    @classmethod
    def register(cls):
        bpy.types.Scene.closet_materials = PointerProperty(
            name="SNaP Materials",
            description="SNaP Material Scene Properties",
            type=cls,
        )

    @classmethod
    def unregister(cls):
        del bpy.types.Scene.closet_materials


classes = (
    SN_MAT_PT_Closet_Materials_Interface,
    SnapMaterialSceneProps
)

register, unregister = bpy.utils.register_classes_factory(classes)
