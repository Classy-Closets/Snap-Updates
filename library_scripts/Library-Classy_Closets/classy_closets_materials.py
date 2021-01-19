
import bpy
from mv import fd_types, unit
from . import classy_closets_lists
from . import mv_closet_defaults as props_closet

def get_material_properties(context):
    return context.scene.cc_materials

def update_materials(self,context):
    exec("bpy.ops." + props_closet.LIBRARY_NAME_SPACE + ".assign_materials(update_countertops=False)")

def update_countertop(self,context):
    exec("bpy.ops." + props_closet.LIBRARY_NAME_SPACE + ".assign_materials(update_countertops=True)")

class PANEL_Panel_Interface(bpy.types.Panel):
    """Panel to Store all of the Cabinet Options"""
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "Closet Materials"
    bl_category = "Fluid Designer"
    
    def draw_header(self, context):
        layout = self.layout
        layout.label('',icon='BLANK1')    
    
    def draw(self, context):
        props = context.scene.cc_materials
        props.draw(self.layout)   

class PROPERTIES_Classy_Materials(bpy.types.PropertyGroup):

    edge_profile = bpy.props.EnumProperty(name="Edge Profile",
                                                 items=[('SQUARE',"Square Edge","Edges are Square"),
                                                        ('ROUND',"Round Edge","Edges are Round")],
                                                 description="This is the edge profile selection",
                                                 update=update_materials)
    
    square_edge = bpy.props.EnumProperty(name="Square Edge Type",
                                                 items=[('1MM',"1mm","This is the square edge type"),
                                                        ('THIN',"Thin","This is the square edge type"),
                                                        ('1M_PVC',"1mm PVC","This is the square edge type"),
                                                        ('1M_DOLCE',"1mm Dolce","This is the square edge type"),
                                                        ('3M_PVC',"3mm PVC","This is the square edge type")],
                                                 description="This is the edge type selection",
                                                 update=update_materials)

    thin_edge = bpy.props.EnumProperty(name="Edge Color",
                                                 items=classy_closets_lists.thin_edge_materials,
                                                 description="This is the thin edge color",
                                                 update=update_materials)
    mm1_edge = bpy.props.EnumProperty(name="Edge Color",
                                                 items=classy_closets_lists.mm1_edge_materials,
                                                 description="This is the 1mm edge color",
                                                 update=update_materials)
    m1pvc_edge = bpy.props.EnumProperty(name="Edge Color",
                                                 items=classy_closets_lists.m1pvc_edge_materials,
                                                 description="This is the 1mm pvc edge color",
                                                 update=update_materials)
    m1dol_edge = bpy.props.EnumProperty(name="Edge Color",
                                                 items=classy_closets_lists.m1dol_edge_materials,
                                                 description="This is the 1mm dolce edge color",
                                                 update=update_materials)
    m3pvc_edge = bpy.props.EnumProperty(name="Edge Color",
                                                 items=classy_closets_lists.m3pvc_edge_materials,
                                                 description="This is the 3mm pvc edge color",
                                                 update=update_materials)    
        
    round_edge = bpy.props.EnumProperty(name="Round Edge Color",
                                                 items=classy_closets_lists.round_edge_materials,
                                                 description="This is the round edge color",
                                                 update=update_materials)

    edge_2_type = bpy.props.EnumProperty(name="Secondary Edge Type",
                                                 items=[('1MM',"1mm","This is the square edge type"),
                                                        ('THIN',"Thin","This is the square edge type"),
                                                        ('1M_PVC',"1mm PVC","This is the square edge type"),
                                                        ('1M_DOLCE',"1mm Dolce","This is the square edge type"),
                                                        ('3M_PVC',"3mm PVC","This is the square edge type")],
                                                 description="This is the secondary edge type",
                                                 update=update_materials)

    thin_edge_2 = bpy.props.EnumProperty(name="Edge Color",
                                                 items=classy_closets_lists.thin_edge_materials,
                                                 description="This is the thin edge color",
                                                 update=update_materials)
    mm1_edge_2 = bpy.props.EnumProperty(name="Edge Color",
                                                 items=classy_closets_lists.mm1_edge_materials,
                                                 description="This is the 1mm edge color",
                                                 update=update_materials)
    m1pvc_edge_2 = bpy.props.EnumProperty(name="Edge Color",
                                                 items=classy_closets_lists.m1pvc_edge_materials,
                                                 description="This is the 1mm pvc edge color",
                                                 update=update_materials)
    m1dol_edge_2 = bpy.props.EnumProperty(name="Edge Color",
                                                 items=classy_closets_lists.m1dol_edge_materials,
                                                 description="This is the 1mm dolce edge color",
                                                 update=update_materials)
    m3pvc_edge_2 = bpy.props.EnumProperty(name="Edge Color",
                                                 items=classy_closets_lists.m3pvc_edge_materials,
                                                 description="This is the 3mm pvc edge color",
                                                 update=update_materials)  

    thin_edge_2 = bpy.props.EnumProperty(name="Edge Color",
                                                 items=classy_closets_lists.thin_edge_materials,
                                                 description="This is the secondary edge color",
                                                 update=update_materials)
    
    material_type = bpy.props.EnumProperty(name="Material Type",
                                                 items=[('MELAMINE',"Untextured Melamine","This is the material type"),
                                                        ('TEXTURED',"Textured Melamine","This is the textured material type")],
                                                 description="This is the material selection",
                                                 update=update_materials)

    melamine_material = bpy.props.EnumProperty(name="Material Color",
                                                 items=classy_closets_lists.melamine_materials,
                                                 description="This is the material color",
                                                 update=update_materials)

    textured_melamine_material = bpy.props.EnumProperty(name="Material Color",
                                                 items=classy_closets_lists.textured_melamine_materials,
                                                 description="This is the textured material color",
                                                 update=update_materials)
    
    stain_color =  bpy.props.EnumProperty(name="Stain Color",
                                                 items=classy_closets_lists.stain_colors,
                                                 description="This is the stain color",
                                                 update=update_materials)
    
    moderno_color =  bpy.props.EnumProperty(name="Moderno Door Color",
                                                 items=classy_closets_lists.moderno_colors,
                                                 description="This is the Moderno Door color",
                                                 update=update_materials)
    
    glass_color =  bpy.props.EnumProperty(name="Glass Color",
                                                 items=classy_closets_lists.glass_colors,
                                                 description="This is the glass color",
                                                 update=update_materials)
    
    ct_type = bpy.props.EnumProperty(name="Countertop Type",
                                                 items=[('MELAMINE',"Melamine - Same as Material Selection","This is the countertop type"),
                                                        ('HPL',"HPL","This is the countertop type"),
                                                        ('QUARTZ',"Quartz","This is the countertop type"),
                                                        ('GRANITE',"Granite","This is the countertop type")],
                                                 description="This is the countertop type selection",
                                                 default="MELAMINE",
                                                 update=update_countertop)
    
    hpl_manufacturer = bpy.props.EnumProperty(name="HPL Manufacturer",
                                                 items=[('WILSONART',"Wilsonart","This is the HPL countertop manufacturer"),
                                                        ('FORMICA',"Formica","This is the HPL countertop manufacturer"),
                                                        ('PIONITE',"Pionite","This is the HPL countertop manufacturer")],
                                                 description="This is the countertop selection",
                                                 update=update_materials)
    
    wilsonart_ct_color =  bpy.props.EnumProperty(name="Countertop Color",
                                                 items=classy_closets_lists.wilsonart_ct,
                                                 description="This is the HPL countertop color",
                                                 update=update_materials)
    
    formica_ct_color =  bpy.props.EnumProperty(name="Countertop Color",
                                                 items=classy_closets_lists.formica_ct,
                                                 description="This is the HPL countertop color",
                                                 update=update_materials)
    
    pionite_ct_color =  bpy.props.EnumProperty(name="Countertop Color",
                                                 items=classy_closets_lists.pionite_ct,
                                                 description="This is the HPL countertop color",
                                                 update=update_materials)
    
    quartz_manufacturer = bpy.props.EnumProperty(name="Quartz Manufacturer",
                                                 items=[('CAESARSTONE',"Caesarstone","This is the quartz countertop manufacturer"),
                                                        ('CAMBRIA',"Cambria","This is the quartz countertop manufacturer"),
                                                        ('CORIAN',"Corian","This is the quartz countertop manufacturer"),
                                                        ('SILESTONE',"Silestone","This is the quartz countertop manufacturer"),
                                                        ('VADERA',"Vadera","This is the quartz countertop manufacturer"),
                                                        ('WILSONART',"Wilsonart","This is the quartz countertop manufacturer")],
                                                 description="This is the countertop selection",
                                                 update=update_materials)
    
    quartz_cambria_collection = bpy.props.EnumProperty(name="Cambria Quartz Collections",
                                                 items=[('CAMBRIAN',"Cambrian","This is the quartz countertop manufacturer"),
                                                        ('CLASSIC',"Classic","This is the quartz countertop manufacturer"),
                                                        ('COASTAL',"Coastal","This is the quartz countertop manufacturer"),
                                                        ('DESERT',"Desert","This is the quartz countertop manufacturer"),
                                                        ('JEWEL',"Jewel","This is the quartz countertop manufacturer"),
                                                        ('MARBLE',"Marble","This is the quartz countertop manufacturer"),
                                                        ('OCEANIC',"Oceanic","This is the quartz countertop manufacturer"),
                                                        ('QUARRY',"Quarry","This is the quartz countertop manufacturer"),
                                                        ('WATERSTONE',"Waterstone","This is the quartz countertop manufacturer")],
                                                 description="This is the countertop selection",
                                                 update=update_materials)
    
    quartz_caesarstone_color =  bpy.props.EnumProperty(name="Quartz Color",
                                                 items=classy_closets_lists.quartz_caesarstone,
                                                 description="This is the quartz countertop color",
                                                 update=update_materials)
    
    quartz_cambria_cambrian_color =  bpy.props.EnumProperty(name="Quartz Color",
                                                 items=classy_closets_lists.quartz_cambria_cambrian,
                                                 description="This is the quartz countertop color",
                                                 update=update_materials)
    
    quartz_cambria_classic_color =  bpy.props.EnumProperty(name="Quartz Color",
                                                 items=classy_closets_lists.quartz_cambria_classic,
                                                 description="This is the quartz countertop color",
                                                 update=update_materials)
    
    quartz_cambria_coastal_color =  bpy.props.EnumProperty(name="Quartz Color",
                                                 items=classy_closets_lists.quartz_cambria_coastal,
                                                 description="This is the quartz countertop color",
                                                 update=update_materials)
    
    quartz_cambria_desert_color =  bpy.props.EnumProperty(name="Quartz Color",
                                                 items=classy_closets_lists.quartz_cambria_desert,
                                                 description="This is the quartz countertop color",
                                                 update=update_materials)
    
    quartz_cambria_jewel_color =  bpy.props.EnumProperty(name="Quartz Color",
                                                 items=classy_closets_lists.quartz_cambria_jewel,
                                                 description="This is the quartz countertop color",
                                                 update=update_materials)
    
    quartz_cambria_marble_color =  bpy.props.EnumProperty(name="Quartz Color",
                                                 items=classy_closets_lists.quartz_cambria_marble,
                                                 description="This is the quartz countertop color",
                                                 update=update_materials)
    
    quartz_cambria_oceanic_color =  bpy.props.EnumProperty(name="Quartz Color",
                                                 items=classy_closets_lists.quartz_cambria_oceanic,
                                                 description="This is the quartz countertop color",
                                                 update=update_materials)
    
    quartz_cambria_quarry_color =  bpy.props.EnumProperty(name="Quartz Color",
                                                 items=classy_closets_lists.quartz_cambria_quarry,
                                                 description="This is the quartz countertop color",
                                                 update=update_materials)
    
    quartz_cambria_waterstone_color =  bpy.props.EnumProperty(name="Quartz Color",
                                                 items=classy_closets_lists.quartz_cambria_waterstone,
                                                 description="This is the quartz countertop color",
                                                 update=update_materials)
    
    quartz_corian_color =  bpy.props.EnumProperty(name="Quartz Color",
                                                 items=classy_closets_lists.quartz_corian,
                                                 description="This is the quartz countertop color",
                                                 update=update_materials)
    
    quartz_silestone_color =  bpy.props.EnumProperty(name="Quartz Color",
                                                 items=classy_closets_lists.quartz_silestone,
                                                 description="This is the quartz countertop color",
                                                 update=update_materials)
    
    quartz_vadera_color =  bpy.props.EnumProperty(name="Quartz Color",
                                                 items=classy_closets_lists.quartz_vadera,
                                                 description="This is the quartz countertop color",
                                                 update=update_materials)
    
    quartz_wilsonart_color =  bpy.props.EnumProperty(name="Quartz Color",
                                                 items=classy_closets_lists.quartz_wilsonart,
                                                 description="This is the quartz countertop color",
                                                 update=update_materials)
    
    granite_color =  bpy.props.EnumProperty(name="Granite Color",
                                                 items=classy_closets_lists.granite_colors,
                                                 description="This is the granite countertop color",
                                                 update=update_materials)
    
    glaze_color =  bpy.props.EnumProperty(name="Glaze Color",
                                                 items=classy_closets_lists.glaze_colors,
                                                 description="This is the glaze color",
                                                 update=update_materials)
    
    glaze_style =  bpy.props.EnumProperty(name="Glaze Style",
                                                 items=classy_closets_lists.glaze_styles,
                                                 description="This is the glaze style",
                                                 update=update_materials)
    

    def get_edge_material(self):
        if self.square_edge == 'THIN':
            return self.thin_edge
        elif self.square_edge == '1MM':
            return self.mm1_edge
        elif self.square_edge == '1M_PVC':
            return self.m1pvc_edge
        elif self.square_edge == '1M_DOLCE':
            return self.m1dol_edge
        elif self.square_edge == '3M_PVC':
            return self.m3pvc_edge
        
    def get_edge_material_2_type(self):
        if self.edge_2_type == 'THIN':
            return self.thin_edge_2
        elif self.edge_2_type == '1MM':
            return self.mm1_edge_2
        elif self.edge_2_type == '1M_PVC':
            return self.m1pvc_edge_2
        elif self.edge_2_type == '1M_DOLCE':
            return self.m1dol_edge_2
        elif self.edge_2_type == '3M_PVC':
            return self.m3pvc_edge_2 
    
    def get_square_edge_name(self):
        if self.square_edge == 'THIN':
            return "EB " + self.thin_edge +" 1030"
        elif self.square_edge == '1MM':
            return "EB " + self.mm1_edge +" 1037"
        elif self.square_edge == '1M_PVC':
            return "EB " + self.m1pvc_edge +" 1040"
        elif self.square_edge == '1M_DOLCE':
            return "EB " + self.m1dol_edge +" 1045"
        elif self.square_edge == '3M_PVC':
            return "EB " + self.m3pvc_edge +" 3030"     
    
    def get_top_bottom_door_edge_name(self):
        return "EB " + self.round_edge +" 1030"  
    
    def get_round_edge_name(self):
        return "RE " + self.round_edge +" 1030"  

    def get_inventory_edge_name(self):
        return self.get_square_edge_name()      

    def get_inventory_edge_2_name(self):
        if self.edge_2_type == 'THIN':
            return "EB " + self.thin_edge_2 +" 1030"
        elif self.edge_2_type == '1MM':
            return "EB " + self.mm1_edge_2 +" 1037"
        elif self.edge_2_type == '1M_PVC':
            return "EB " + self.m1pvc_edge_2 +" 1040"
        elif self.edge_2_type == '1M_DOLCE':
            return "EB " + self.m1dol_edge_2 +" 1045"
        elif self.edge_2_type == '3M_PVC':
            return "EB " + self.m3pvc_edge_2 +" 3030"

    def get_inventory_material_name(self):
        if self.material_type == 'MELAMINE':
            return self.melamine_material + " 15200"
        else:
            return self.textured_melamine_material + " 15150"

    def get_material_name(self):
        if self.material_type == 'MELAMINE':
            return self.melamine_material
        else:
            return self.textured_melamine_material
    
    def get_stain_name(self):
        return self.stain_color   
     
    def get_moderno_name(self):
        return self.moderno_color   
    
    def get_glass_name(self):
        return self.glass_color       

    def get_ct_name(self):
        if self.ct_type == 'HPL' and self.hpl_manufacturer == 'WILSONART':
            return self.wilsonart_ct_color
        elif self.ct_type == 'HPL' and self.hpl_manufacturer == 'FORMICA':
            return self.formica_ct_color
        elif self.ct_type == 'HPL' and self.hpl_manufacturer == 'PIONITE':
            return self.pionite_ct_color
        elif self.ct_type == 'MELAMINE':
            return self.get_material_name()
        elif self.ct_type == 'QUARTZ' and self.quartz_manufacturer == 'CAESARSTONE':
            return self.quartz_caesarstone_color
        elif self.ct_type == 'QUARTZ' and self.quartz_manufacturer == 'CORIAN':
            return self.quartz_corian_color
        elif self.ct_type == 'QUARTZ' and self.quartz_manufacturer == 'SILESTONE':
            return self.quartz_silestone_color
        elif self.ct_type == 'QUARTZ' and self.quartz_manufacturer == 'VADERA':
            return self.quartz_vadera_color
        elif self.ct_type == 'QUARTZ' and self.quartz_manufacturer == 'WILSONART':
            return self.quartz_wilsonart_color
        elif self.ct_type == 'QUARTZ' and self.quartz_manufacturer == 'CAMBRIA' and self.quartz_cambria_collection == 'CAMBRIAN':
            return self.quartz_cambria_cambrian_color
        elif self.ct_type == 'QUARTZ' and self.quartz_manufacturer == 'CAMBRIA' and self.quartz_cambria_collection == 'CLASSIC':
            return self.quartz_cambria_classic_color
        elif self.ct_type == 'QUARTZ' and self.quartz_manufacturer == 'CAMBRIA' and self.quartz_cambria_collection == 'COASTAL':
            return self.quartz_cambria_coastal_color
        elif self.ct_type == 'QUARTZ' and self.quartz_manufacturer == 'CAMBRIA' and self.quartz_cambria_collection == 'DESERT':
            return self.quartz_cambria_desert_color
        elif self.ct_type == 'QUARTZ' and self.quartz_manufacturer == 'CAMBRIA' and self.quartz_cambria_collection == 'JEWEL':
            return self.quartz_cambria_jewel_color
        elif self.ct_type == 'QUARTZ' and self.quartz_manufacturer == 'CAMBRIA' and self.quartz_cambria_collection == 'MARBLE':
            return self.quartz_cambria_marble_color
        elif self.ct_type == 'QUARTZ' and self.quartz_manufacturer == 'CAMBRIA' and self.quartz_cambria_collection == 'OCEANIC':
            return self.quartz_cambria_oceanic_color
        elif self.ct_type == 'QUARTZ' and self.quartz_manufacturer == 'CAMBRIA' and self.quartz_cambria_collection == 'QUARRY':
            return self.quartz_cambria_quarry_color
        elif self.ct_type == 'QUARTZ' and self.quartz_manufacturer == 'CAMBRIA' and self.quartz_cambria_collection == 'WATERSTONE':
            return self.quartz_cambria_waterstone_color
        elif self.ct_type == 'GRANITE':
            return self.granite_color

    def get_ct_inventory_name(self):
        if self.ct_type == 'HPL':
            return "HPL " + self.hpl_manufacturer + " " + self.get_ct_name()
        elif self.ct_type == 'QUARTZ':
            return "Quartz " + self.quartz_manufacturer + " " + self.get_ct_name()
        elif self.ct_type == 'GRANITE':
            return "Granite " + self.get_ct_name()
        elif self.ct_type == 'MELAMINE':
            return "Melamine " + self.get_inventory_material_name()

    def draw(self,layout):
        box = layout.box()
        box.label("Edge Selection:")
        box.prop(self,"square_edge",text="Edge Type")
        if self.square_edge == 'THIN':
            box.prop(self,"thin_edge")
        elif self.square_edge == '1MM':
            box.prop(self,"mm1_edge") 
        elif self.square_edge == '1M_PVC':
            box.prop(self,"m1pvc_edge")   
        elif self.square_edge == '1M_DOLCE':
            box.prop(self,"m1dol_edge")
        elif self.square_edge == '3M_PVC':
            box.prop(self,"m3pvc_edge")

        box = layout.box()
        box.label("Secondary Edge Selection: (Same as Material Selection)")
        box.prop(self,"edge_2_type")
        if self.edge_2_type == 'THIN':
            box.prop(self,"thin_edge_2")
        elif self.edge_2_type == '1MM':
            box.prop(self,"mm1_edge_2") 
        elif self.edge_2_type == '1M_PVC':
            box.prop(self,"m1pvc_edge_2")   
        elif self.edge_2_type == '1M_DOLCE':
            box.prop(self,"m1dol_edge_2")
        elif self.edge_2_type == '3M_PVC':
            box.prop(self,"m3pvc_edge_2")

        box = layout.box()    
        box.label("Material Selection:")
        box.prop(self,"material_type")
        if self.material_type == 'MELAMINE':
            box.prop(self,"melamine_material")
        elif self.material_type == 'TEXTURED':
            box.prop(self,"textured_melamine_material")
            
        box = layout.box()    
        box.label("Countertop Selection:")
        box.prop(self,"ct_type")

        if self.ct_type == 'MELAMINE':
#             box.label("Edge Selection:")
#             box.prop(self,"edge_profile")
#             if self.edge_profile == 'SQUARE':
#                 box.prop(self,"square_edge")
#                 if self.square_edge == 'THIN':
#                     box.prop(self,"thin_edge")
#                 elif self.square_edge == '1M_PVC':
#                     box.prop(self,"m1pvc_edge")   
#                 elif self.square_edge == '1M_DOLCE':
#                     box.prop(self,"m1dol_edge")
#                 elif self.square_edge == '3M_PVC':
#                     box.prop(self,"m3pvc_edge")
#             elif self.edge_profile == 'ROUND':
#                 box.prop(self,"round_edge")
#     
#             box.label("Secondary Edge Selection: (Same as Material Selection)")
#             box.prop(self,"thin_edge_2")
#       
#             box.label("Material Selection:")
#             box.prop(self,"material_type")
#             if self.material_type == 'MELAMINE':
#                 box.prop(self,"melamine_material")
#             elif self.material_type == 'TEXTURED':
#                 box.prop(self,"textured_melamine_material")
            pass
        
        if self.ct_type == 'HPL':
            box.prop(self,"hpl_manufacturer")
            if self.hpl_manufacturer == 'WILSONART':
                box.prop(self,"wilsonart_ct_color")
            elif self.hpl_manufacturer == 'FORMICA':
                box.prop(self,"formica_ct_color")
            elif self.hpl_manufacturer == 'PIONITE':
                box.prop(self,"pionite_ct_color")
                
        if self.ct_type == 'QUARTZ':
            box.prop(self,"quartz_manufacturer")
            if self.quartz_manufacturer == 'CAESARSTONE':
                box.prop(self,"quartz_caesarstone_color")
            elif self.quartz_manufacturer == 'CAMBRIA':
                box.prop(self,"quartz_cambria_collection")
                if self.quartz_cambria_collection == 'CAMBRIAN':
                    box.prop(self,"quartz_cambria_cambrian_color")
                elif self.quartz_cambria_collection == 'CLASSIC':
                    box.prop(self,"quartz_cambria_classic_color")
                elif self.quartz_cambria_collection == 'COASTAL':
                    box.prop(self,"quartz_cambria_coastal_color")
                elif self.quartz_cambria_collection == 'DESERT':
                    box.prop(self,"quartz_cambria_desert_color")
                elif self.quartz_cambria_collection == 'JEWEL':
                    box.prop(self,"quartz_cambria_jewel_color")
                elif self.quartz_cambria_collection == 'MARBLE':
                    box.prop(self,"quartz_cambria_marble_color")
                elif self.quartz_cambria_collection == 'OCEANIC':
                    box.prop(self,"quartz_cambria_oceanic_color")
                elif self.quartz_cambria_collection == 'QUARRY':
                    box.prop(self,"quartz_cambria_quarry_color")
                elif self.quartz_cambria_collection == 'WATERSTONE':
                    box.prop(self,"quartz_cambria_waterstone_color")
            elif self.quartz_manufacturer == 'CORIAN':
                box.prop(self,"quartz_corian_color")
            elif self.quartz_manufacturer == 'SILESTONE':
                box.prop(self,"quartz_silestone_color")
            elif self.quartz_manufacturer == 'VADERA':
                box.prop(self,"quartz_vadera_color")
            elif self.quartz_manufacturer == 'WILSONART':
                box.prop(self,"quartz_wilsonart_color")
                
        if self.ct_type == 'GRANITE':
            box.prop(self,"granite_color")
                                    
        box = layout.box()
        box.label("Stain Color Selection:")
        box.prop(self,"stain_color")
        
        if self.stain_color != "None":
            box.prop(self,"glaze_color")
            
        if self.glaze_color != "None":
            box.prop(self,"glaze_style")

        box = layout.box()
        box.label("Moderno Door Color Selection:")
        box.prop(self,"moderno_color")   
        
        box = layout.box()
        box.label("Glass Inset Color Selection:")
        box.prop(self,"glass_color")              
                    
        row = layout.row()
        row.scale_y = 1.5
        row.operator(props_closet.LIBRARY_NAME_SPACE + ".assign_materials",text="Update Materials",icon='FILE_REFRESH')
        
class OPERATOR_Assign_Materials(bpy.types.Operator):
    bl_idname = props_closet.LIBRARY_NAME_SPACE + ".assign_materials"
    bl_label = "Assign Materials"
    bl_description = "This will assign the material names"
    bl_options = {'UNDO'}
    
    update_countertops = bpy.props.BoolProperty(name="Update Countertops",default=False)
    only_update_pointers = bpy.props.BoolProperty(name="Only Update Pointers",default=False)
    
    def scene_assemblies(self,context):
        for obj in bpy.context.scene.objects:
            if obj.mv.type == 'BPASSEMBLY':
                assembly = fd_types.Assembly(obj)
                yield assembly

    def set_manufacturing_material(self,obj):
        """ Sets the cutpart_material_name property so the materials
            get exported as the correct names.
        """
        props = get_material_properties(bpy.context)
        
        obj.mv.cutpart_material_name = props.get_inventory_material_name()
        
        if obj.mv.edge_w1 != "":
            if obj.mv.edge_w1 == 'Edge':
                obj.mv.edgeband_material_name_w1 = props.get_inventory_edge_name()
            else:
                obj.mv.edgeband_material_name_w1 = props.get_inventory_edge_2_name()
        
        if obj.mv.edge_w2 != "":
            if obj.mv.edge_w2 == 'Edge':
                obj.mv.edgeband_material_name_w2 = props.get_inventory_edge_name()
            else:
                obj.mv.edgeband_material_name_w2 = props.get_inventory_edge_2_name()

        if obj.mv.edge_l1 != "":
            if obj.mv.edge_l1 == 'Edge':
                obj.mv.edgeband_material_name_l1 = props.get_inventory_edge_name()
            else:
                obj.mv.edgeband_material_name_l1 = props.get_inventory_edge_2_name()

        if obj.mv.edge_l2 != "":
            if obj.mv.edge_l2 == 'Edge':
                obj.mv.edgeband_material_name_l2 = props.get_inventory_edge_name()
            else:
                obj.mv.edgeband_material_name_l2 = props.get_inventory_edge_2_name()           

    def set_material(self,part):
        for child in part.obj_bp.children:
            if child.cabinetlib.type_mesh == 'CUTPART':
                self.set_manufacturing_material(child)  

    def set_door_material(self,part):
        for obj in part.obj_bp.children:
            if obj.cabinetlib.type_mesh == 'CUTPART':
                props = get_material_properties(bpy.context)
                
                obj.mv.cutpart_material_name = props.get_inventory_material_name()
                
#                 if props.edge_profile == 'SQUARE':
#                     obj.mv.edgeband_material_name_w1 = props.get_square_edge_name()
#                     obj.mv.edgeband_material_name_w2 = props.get_square_edge_name()
#                     obj.mv.edgeband_material_name_l1 = props.get_square_edge_name()
#                     obj.mv.edgeband_material_name_l2 = props.get_square_edge_name()   
#                 else:
                obj.mv.edgeband_material_name_w1 = props.get_top_bottom_door_edge_name()
                obj.mv.edgeband_material_name_w2 = props.get_top_bottom_door_edge_name()
                obj.mv.edgeband_material_name_l1 = props.get_square_edge_name()
                obj.mv.edgeband_material_name_l2 = props.get_square_edge_name()                   
                                      
    def set_drawer_bottom_material(self,part):
        for obj in part.obj_bp.children:
            if obj.cabinetlib.type_mesh == 'CUTPART':
                props = get_material_properties(bpy.context)
                box_type = props_closet.get_scene_props().closet_options.box_type
                if box_type == 'MEL':
                    obj.mv.cutpart_material_name = "White Paper 11300" 
                else:
                    obj.mv.cutpart_material_name = "Baltic Birch 30250"                                     
                                
    def set_drawer_part_material(self,part):
        for obj in part.obj_bp.children:
            if obj.cabinetlib.type_mesh == 'CUTPART':
                props = get_material_properties(bpy.context)
                box_type = props_closet.get_scene_props().closet_options.box_type
                if box_type == 'MEL':
                    obj.mv.cutpart_material_name = "Oxford White 12200" 
                else:
                    obj.mv.cutpart_material_name = "Baltic Birch 32200"                                  

                obj.mv.edgeband_material_name_l1 = "Oxford White 1030"
                obj.mv.edgeband_material_name_l2 = ""
                obj.mv.edgeband_material_name_w1 = ""
                obj.mv.edgeband_material_name_w2 = "" 
                
    def set_countertop_material(self,part):
        for obj in part.obj_bp.children:
            if obj.cabinetlib.type_mesh == 'BUYOUT':
                props = get_material_properties(bpy.context)
                obj.mv.buyout_material_name = props.get_ct_inventory_name()   

    def update_material_pointers(self,context):
        props = get_material_properties(context)
        default_props = props_closet.get_scene_props().closet_options
        
        for spec_group in context.scene.mv.spec_groups:
            surface_pointer = spec_group.materials["Closet_Part_Surfaces"]
            edge_pointer = spec_group.materials["Closet_Part_Edges"]
            edge_pointer_2 = spec_group.materials["Closet_Part_Edges_Secondary"]
            door_pointer = spec_group.materials["Door_Surface"]
            door_edge_pointer = spec_group.materials["Door_Edge"]
            molding_pointer = spec_group.materials["Molding"]    
            drawer_surface = spec_group.materials["Drawer_Box_Surface"]   
            wood_door_pointer = spec_group.materials["Wood_Door_Surface"]
            moderno_door_pointer = spec_group.materials["Moderno_Door"]
            glass_panel_pointer = spec_group.materials["Glass"]
            countertop_pointer = spec_group.materials["Countertop_Surface"]      

            if default_props.box_type == 'MEL':
                drawer_surface.library_name = "Cabinet Materials"
                drawer_surface.category_name = "Classy Closets"
                drawer_surface.item_name = "Oxford White"
            else:
                drawer_surface.library_name = "Cabinet Materials"
                drawer_surface.category_name = "Classy Closets"
                drawer_surface.item_name = "Birch"

            surface_pointer.library_name = "Cabinet Materials"
            surface_pointer.category_name = "Classy Closets"
            surface_pointer.item_name = props.get_material_name()

            molding_pointer.library_name = "Cabinet Materials"
            molding_pointer.category_name = "Classy Closets"
            molding_pointer.item_name = props.get_stain_name()
            
            edge_pointer.library_name = "Cabinet Materials"
            edge_pointer.category_name = "Classy Closets"
            edge_pointer.item_name = props.get_edge_material() 
            
            edge_pointer_2.library_name = "Cabinet Materials"
            edge_pointer_2.category_name = "Classy Closets"
            edge_pointer_2.item_name = props.get_edge_material_2_type()             
            
            door_pointer.library_name = "Cabinet Materials"
            door_pointer.category_name = "Classy Closets"
            door_pointer.item_name = props.get_material_name()    
            
            door_edge_pointer.library_name = "Cabinet Materials"
            door_edge_pointer.category_name = "Classy Closets"
            door_edge_pointer.item_name = props.get_edge_material()  
            
            wood_door_pointer.library_name = "Cabinet Materials"
            wood_door_pointer.category_name = "Classy Closets"
            wood_door_pointer.item_name = props.get_stain_name()     

            moderno_door_pointer.library_name = "Cabinet Materials"
            moderno_door_pointer.category_name = "Classy Closets"
            moderno_door_pointer.item_name = props.get_moderno_name() 

            glass_panel_pointer.library_name = "Cabinet Materials"
            glass_panel_pointer.category_name = "Classy Closets"
            glass_panel_pointer.item_name = props.get_glass_name() 

            countertop_pointer.library_name = "Cabinet Materials"
            countertop_pointer.category_name = "Classy Closets CT"
            countertop_pointer.item_name = props.get_ct_name()
    
    
        bpy.ops.cabinetlib.update_scene_from_pointers()
    
    def update_drawer_materials(self):
        props = props_closet.get_scene_props()
        box_type = props.closet_options.box_type
        for spec_group in bpy.context.scene.mv.spec_groups:
            drawer_part = spec_group.cutparts['Drawer_Part']
            drawer_back = spec_group.cutparts['Drawer_Back']
            drawer_bottom = spec_group.cutparts['Drawer_Bottom']
            if box_type == 'MEL':
                drawer_part.thickness = unit.inch(.5)
                drawer_back.thickness = unit.inch(.5)
                drawer_bottom.thickness = unit.inch(.375)
            else:
                drawer_part.thickness = unit.inch(.5)
                drawer_back.thickness = unit.inch(.5)
                drawer_bottom.thickness = unit.inch(.25)

    def execute(self, context):
        if self.only_update_pointers:
            self.update_material_pointers(context)
            self.update_drawer_materials()
        else:
            self.update_drawer_materials()
            for assembly in self.scene_assemblies(context):
                props = props_closet.get_object_props(assembly.obj_bp)
                
                if props.is_panel_bp:
                    if assembly.obj_x.location.x > unit.inch(37.47):
                        for child in assembly.obj_bp.children:
                            if child.cabinetlib.type_mesh == 'CUTPART':
                                child.mv.edge_w1 = ''
                                child.mv.edge_w2 = ''
                                for mat_slot in child.cabinetlib.material_slots:
                                    if mat_slot.name == 'TopBottomEdge':
                                        mat_slot.pointer_name = "Core"
                    else:
                        for child in assembly.obj_bp.children:
                            if child.cabinetlib.type_mesh == 'CUTPART':
                                child.mv.edge_w1 = 'Edge_2'
                                child.mv.edge_w2 = 'Edge_2'
                                for mat_slot in child.cabinetlib.material_slots:
                                    if mat_slot.name == 'TopBottomEdge':
                                        mat_slot.pointer_name = "Closet_Part_Edges_Secondary"  
                
                if props.is_countertop_bp:
                    self.set_countertop_material(assembly)                        
                 

#Topshelf                
                if props.is_plant_on_top_bp:
                    exposed_left = assembly.get_prompt("Exposed Left")
                    exposed_right = assembly.get_prompt("Exposed Right")
                    exposed_back = assembly.get_prompt("Exposed Back")
                    if exposed_left:
                        if exposed_left.value():
                            for child in assembly.obj_bp.children:
                                if child.cabinetlib.type_mesh == 'CUTPART':                        
                                    child.mv.edge_w1 = 'Edge'
                                    for mat_slot in child.cabinetlib.material_slots:
                                        if mat_slot.name == 'LeftEdge':
                                            mat_slot.pointer_name = "Closet_Part_Edges"                                
                        else:
                            for child in assembly.obj_bp.children:
                                if child.cabinetlib.type_mesh == 'CUTPART':                        
                                    child.mv.edge_w1 = ''
                                    for mat_slot in child.cabinetlib.material_slots:
                                        if mat_slot.name == 'LeftEdge':
                                            mat_slot.pointer_name = "Core"                    
                    if exposed_right:
                        if exposed_right.value():
                            for child in assembly.obj_bp.children:
                                if child.cabinetlib.type_mesh == 'CUTPART':                        
                                    child.mv.edge_w2 = 'Edge'
                                    for mat_slot in child.cabinetlib.material_slots:
                                        if mat_slot.name == 'RightEdge':
                                            mat_slot.pointer_name = "Closet_Part_Edges"                                   
                        else:
                            for child in assembly.obj_bp.children:
                                if child.cabinetlib.type_mesh == 'CUTPART':                        
                                    child.mv.edge_w2 = ''
                                    for mat_slot in child.cabinetlib.material_slots:
                                        if mat_slot.name == 'RightEdge':
                                            mat_slot.pointer_name = "Core"    
                                              
                    if exposed_back:
                        if exposed_back.value():
                            for child in assembly.obj_bp.children:
                                if child.cabinetlib.type_mesh == 'CUTPART':                        
                                    child.mv.edge_l2 = 'Edge'
                                    for mat_slot in child.cabinetlib.material_slots:
                                        if mat_slot.name == 'BackEdge':
                                            mat_slot.pointer_name = "Closet_Part_Edges"                                   
                        else:
                            for child in assembly.obj_bp.children:
                                if child.cabinetlib.type_mesh == 'CUTPART':                        
                                    child.mv.edge_l2 = ''
                                    for mat_slot in child.cabinetlib.material_slots:
                                        if mat_slot.name == 'BackEdge':
                                            mat_slot.pointer_name = "Core"
                                            

#Crown                
                if props.is_crown_molding:
                    exposed_left = assembly.get_prompt("Exposed Left")
                    exposed_right = assembly.get_prompt("Exposed Right")
                    exposed_back = assembly.get_prompt("Exposed Back")                  
                    
                    if exposed_left:
                        if exposed_left.value():
                            for child in assembly.obj_bp.children:
                                if child.cabinetlib.type_mesh == 'CUTPART':                        
                                    child.mv.edge_w1 = 'Edge'
                                    for mat_slot in child.cabinetlib.material_slots:
                                        if mat_slot.name == 'LeftEdge':
                                            mat_slot.pointer_name = "Closet_Part_Edges_Secondary"                                
                        else:
                            for child in assembly.obj_bp.children:
                                if child.cabinetlib.type_mesh == 'CUTPART':                        
                                    child.mv.edge_w1 = ''
                                    for mat_slot in child.cabinetlib.material_slots:
                                        if mat_slot.name == 'LeftEdge':
                                            mat_slot.pointer_name = "Core"                    
                    if exposed_right:
                        if exposed_right.value():
                            for child in assembly.obj_bp.children:
                                if child.cabinetlib.type_mesh == 'CUTPART':                        
                                    child.mv.edge_w2 = 'Edge'
                                    for mat_slot in child.cabinetlib.material_slots:
                                        if mat_slot.name == 'RightEdge':
                                            mat_slot.pointer_name = "Closet_Part_Edges_Secondary"                                   
                        else:
                            for child in assembly.obj_bp.children:
                                if child.cabinetlib.type_mesh == 'CUTPART':                        
                                    child.mv.edge_w2 = ''
                                    for mat_slot in child.cabinetlib.material_slots:
                                        if mat_slot.name == 'RightEdge':
                                            mat_slot.pointer_name = "Core"    
                                              
                    if exposed_back:
                        if exposed_back.value():
                            for child in assembly.obj_bp.children:
                                if child.cabinetlib.type_mesh == 'CUTPART':                        
                                    child.mv.edge_l2 = 'Edge'
                                    for mat_slot in child.cabinetlib.material_slots:
                                        if mat_slot.name == 'BackEdge':
                                            mat_slot.pointer_name = "Closet_Part_Edges_Secondary"                                   
                        else:
                            for child in assembly.obj_bp.children:
                                if child.cabinetlib.type_mesh == 'CUTPART':                        
                                    child.mv.edge_l2 = ''
                                    for mat_slot in child.cabinetlib.material_slots:
                                        if mat_slot.name == 'BackEdge':
                                            mat_slot.pointer_name = "Core"                                            
                                 
                scene_props = context.scene.cc_materials
                
                if self.update_countertops: 
                    ctop_type = assembly.get_prompt("Countertop Type")
                    if ctop_type:
                        if scene_props.ct_type == 'MELAMINE':
                            ctop_type.set_value('Melamine')    
                        if scene_props.ct_type == 'HPL':
                            ctop_type.set_value('HPL')    
                        if scene_props.ct_type == 'QUARTZ':                   
                            ctop_type.set_value('Quartz')   #Granite 
                        if scene_props.ct_type == 'GRANITE':                   
                            ctop_type.set_value('Granite')            
                
                catnum = assembly.get_prompt("CatNum")
                if catnum:
                    assembly.obj_bp.mv.comment_2 = str(int(catnum.value()))
                              
                if props.is_door_bp:
                    self.set_door_material(assembly)
                elif props.is_drawer_bottom_bp:
                    self.set_drawer_bottom_material(assembly)
                elif props.is_drawer_back_bp or props.is_drawer_side_bp or props.is_drawer_sub_front_bp:
                    self.set_drawer_part_material(assembly)
                else:
                    self.set_material(assembly)               
                    
            self.update_material_pointers(context) 
            
            bpy.ops.cabinetlib.update_scene_from_pointers()               
                
        return {'FINISHED'}
    
#bpy.utils.register_class(PANEL_Panel_Interface)
bpy.utils.register_class(PROPERTIES_Classy_Materials)    
bpy.utils.register_class(OPERATOR_Assign_Materials)    
bpy.types.Scene.cc_materials = bpy.props.PointerProperty(type = PROPERTIES_Classy_Materials)

# @bpy.app.handlers.persistent
# def assign_materials(scene=None):
#     exec("bpy.ops." + props_closet.LIBRARY_NAME_SPACE + ".assign_materials()")
    
# @bpy.app.handlers.persistent
# def assign_material_pointers(scene=None):
#     exec("bpy.ops." + props_closet.LIBRARY_NAME_SPACE + ".assign_materials(only_update_pointers=True)")    
    
# bpy.app.handlers.save_pre.append(assign_materials)    
# bpy.app.handlers.load_post.append(assign_material_pointers)    
