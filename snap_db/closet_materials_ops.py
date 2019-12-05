import bpy
from mv import fd_types, unit


class OPERATOR_Poll_Assign_Materials(bpy.types.Operator):
    bl_idname = "db_materials.poll_assign_materials"
    bl_label = ""
    bl_description = ""
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene.db_materials.check_render_mats()

    def execute(self, context):
        bpy.ops.db_materials.assign_materials()

        return {'FINISHED'}


class OPERATOR_Assign_Materials(bpy.types.Operator):
    bl_idname = "db_materials.assign_materials"
    bl_label = "Assign Materials"
    bl_description = "This will assign the material names"
    bl_options = {'UNDO'}
    
    update_countertops = bpy.props.BoolProperty(name="Update Countertops",default=False)
    only_update_pointers = bpy.props.BoolProperty(name="Only Update Pointers",default=False)

    props_closet = None
    props_closet_materials = None

    # @classmethod
    # def poll(cls, context):
    #     return context.scene.db_materials.check_render_mats()
    
    def scene_assemblies(self,context):
        for obj in bpy.context.scene.objects:
            if obj.mv.type == 'BPASSEMBLY':
                assembly = fd_types.Assembly(obj)
                yield assembly

    def set_manufacturing_material(self,obj):
        """ Sets the cutpart_material_name property so the materials
            get exported as the correct names.
        """
        props = bpy.context.scene.db_materials
        mat_type = props.materials.get_mat_type()
        edge_type = props.edges.get_edge_type()
        edge2_type = props.secondary_edges.get_edge_type()
        
        obj.mv.cutpart_material_name = mat_type.get_inventory_material_name()
        
        if obj.mv.edge_w1 != "":
            if obj.mv.edge_w1 == 'Edge':
                obj.mv.edgeband_material_name_w1 = edge_type.get_inventory_edge_name()
            else:
                obj.mv.edgeband_material_name_w1 = edge2_type.get_inventory_edge_name()
        
        if obj.mv.edge_w2 != "":
            if obj.mv.edge_w2 == 'Edge':
                obj.mv.edgeband_material_name_w2 = edge_type.get_inventory_edge_name()
            else:
                obj.mv.edgeband_material_name_w2 = edge2_type.get_inventory_edge_name()

        if obj.mv.edge_l1 != "":
            if obj.mv.edge_l1 == 'Edge':
                obj.mv.edgeband_material_name_l1 = edge_type.get_inventory_edge_name()
            else:
                obj.mv.edgeband_material_name_l1 = edge2_type.get_inventory_edge_name()

        if obj.mv.edge_l2 != "":
            if obj.mv.edge_l2 == 'Edge':
                obj.mv.edgeband_material_name_l2 = edge_type.get_inventory_edge_name()
            else:
                obj.mv.edgeband_material_name_l2 = edge2_type.get_inventory_edge_name()           

    def set_material(self,part):
        for child in part.obj_bp.children:
            if child.cabinetlib.type_mesh == 'CUTPART':
                self.set_manufacturing_material(child)  

    def set_door_material(self,part):
        for obj in part.obj_bp.children:
            if obj.cabinetlib.type_mesh == 'CUTPART':
                props = self.props_closet_materials
                mat_type = props.materials.get_mat_type()
                edge_type = props.edges.get_edge_type()

                obj.mv.cutpart_material_name = mat_type.get_inventory_material_name()
                obj.mv.edgeband_material_name_w1 = edge_type.get_inventory_edge_name()
                obj.mv.edgeband_material_name_w2 = edge_type.get_inventory_edge_name()
                obj.mv.edgeband_material_name_l1 = edge_type.get_inventory_edge_name()
                obj.mv.edgeband_material_name_l2 = edge_type.get_inventory_edge_name()                  
                                      
    def set_drawer_bottom_material(self,part):
        for obj in part.obj_bp.children:
            if obj.cabinetlib.type_mesh == 'CUTPART':
                props = self.props_closet_materials
                box_type = self.props_closet.closet_options.box_type

                if box_type == 'MEL':
                    obj.mv.cutpart_material_name = "White Paper 11300" 
                else:
                    obj.mv.cutpart_material_name = "Baltic Birch 30250"                                     
                                
    def set_drawer_part_material(self,part):
        for obj in part.obj_bp.children:
            if obj.cabinetlib.type_mesh == 'CUTPART':
                props = self.props_closet_materials
                box_type = self.props_closet.closet_options.box_type

                if box_type == 'MEL':
                    obj.mv.cutpart_material_name = "Oxford White 12200" 
                else:
                    obj.mv.cutpart_material_name = "Baltic Birch 32200"                                  

                obj.mv.edgeband_material_name_l1 = "Oxford White 1030"
                obj.mv.edgeband_material_name_l2 = ""
                obj.mv.edgeband_material_name_w1 = ""
                obj.mv.edgeband_material_name_w2 = "" 
                
    def set_countertop_material(self,part):
        print(part.assembly_name)
        # countertop_type = part.get_prompt("Countertop Type")

        # print("PART", part.get_prompt("Countertop Type"))
        # print("PART OBJ BP", part.obj_bp.get_prompt("Countertop Type"))

        #print(countertop_type, countertop_type.value)

        # for obj in part.obj_bp.children:
        #     if obj.cabinetlib.type_mesh == 'BUYOUT':
        #         props = self.props_closet_materials
        #         obj.mv.buyout_material_name = props.countertops.get_ct_inventory_name()   

    def update_material_pointers(self,context):
        mat_props = self.props_closet_materials
        default_props = self.props_closet.closet_options
        
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

            #Construction Defaults 
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
            surface_pointer.item_name = mat_props.materials.get_mat_color().name 

            molding_pointer.library_name = "Cabinet Materials"
            molding_pointer.category_name = "Classy Closets"
            molding_pointer.item_name = mat_props.stain_colors[mat_props.stain_color_index].name 
            
            edge_pointer.library_name = "Cabinet Materials"
            edge_pointer.category_name = "Classy Closets"
            edge_pointer.item_name = mat_props.edges.get_edge_color().name 
            
            edge_pointer_2.library_name = "Cabinet Materials"
            edge_pointer_2.category_name = "Classy Closets"
            edge_pointer_2.item_name = mat_props.secondary_edges.get_edge_color().name            
            
            door_pointer.library_name = "Cabinet Materials"
            door_pointer.category_name = "Classy Closets"
            door_pointer.item_name = mat_props.materials.get_mat_color().name  
            
            door_edge_pointer.library_name = "Cabinet Materials"
            door_edge_pointer.category_name = "Classy Closets"
            door_edge_pointer.item_name = mat_props.edges.get_edge_color().name  
            
            wood_door_pointer.library_name = "Cabinet Materials"
            wood_door_pointer.category_name = "Classy Closets"
            wood_door_pointer.item_name = mat_props.stain_colors[mat_props.stain_color_index].name 

            moderno_door_pointer.library_name = "Cabinet Materials"
            moderno_door_pointer.category_name = "Classy Closets"
            moderno_door_pointer.item_name = mat_props.moderno_colors[mat_props.moderno_color_index].name 

            glass_panel_pointer.library_name = "Cabinet Materials"
            glass_panel_pointer.category_name = "Classy Closets"
            glass_panel_pointer.item_name = mat_props.glass_colors[mat_props.glass_color_index].name 

            countertop_pointer.library_name = "Cabinet Materials"

            if "Melamine" in mat_props.countertops.get_type().name:
                countertop_pointer.category_name = "Classy Closets"
            else:
                countertop_pointer.category_name = "Classy Closets CT"

            countertop_pointer.item_name = mat_props.countertops.get_color_name()
    
    def update_drawer_materials(self):
        props = self.props_closet
        # props = props_closet.get_scene_props()
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
        self.props_closet = context.scene.lm_closets
        self.props_closet_materials = context.scene.db_materials

        if self.only_update_pointers:
            self.update_material_pointers(context)
            self.update_drawer_materials()
        else:
            self.update_drawer_materials()

            for assembly in self.scene_assemblies(context):
                props = assembly.obj_bp.lm_closets
                

                if props.is_panel_bp:
                    #What is 37.47 inch?
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


def register():
    bpy.utils.register_class(OPERATOR_Poll_Assign_Materials)
    bpy.utils.register_class(OPERATOR_Assign_Materials)


def unregister():
    bpy.utils.unregister_class(OPERATOR_Poll_Assign_Materials)
    bpy.utils.unregister_class(OPERATOR_Assign_Materials)
 