
import bpy
from bpy.types import Operator
from . import products
from mv import fd_types, utils, unit

class OPERATOR_Entry_Door_Standard_Draw_Plan(Operator):
    bl_idname = products.LIBRARY_NAMESPACE + ".draw_plan"
    bl_label = "Draw Closet Plan View"
    bl_description = "Creates the plan view for closets"
    
    object_name = bpy.props.StringProperty(name="Object Name",default="")
    
    product = None
    
    def execute(self, context):
        print("Creating Entry Plan View Object for: ", self.object_name)
        obj_bp = bpy.data.objects[self.object_name]
        self.product = fd_types.Assembly(obj_bp)
        
        #TODO CREATE OBJ TAG FOR IDENTIFYING DOOR SUBASSEMBLIES
        for child in obj_bp.children:
            if child.type == 'MESH':
                print(child.name)
                if 'Panel' in child.name:
                    print("This is a panel: ", child.name)
        
        x_location = self.product.obj_bp.location.x
        
        width = self.product.obj_x.location.x
        height = self.product.obj_z.location.z
        depth = unit.inch(2.0)
        
        door_mesh = utils.create_cube_mesh(self.product.obj_bp.mv.name_object,(width, height, depth))
        door_mesh.parent = self.product.obj_bp.parent
        door_mesh.location = self.product.obj_bp.location
        door_mesh.location.x = x_location
        door_mesh.rotation_euler = self.product.obj_bp.rotation_euler
        door_mesh.mv.type = 'CAGE'        
        
        return {'FINISHED'}
    

def register():
    bpy.utils.register_class(OPERATOR_Entry_Door_Standard_Draw_Plan)