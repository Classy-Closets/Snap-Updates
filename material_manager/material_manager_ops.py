import bpy
from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class
from os.path import splitext, split, join, exists
from bpy.props import BoolProperty, IntProperty, FloatProperty, EnumProperty, StringProperty, CollectionProperty, PointerProperty, FloatVectorProperty
from bpy.types import PropertyGroup, Panel
import os
import subprocess
import re
import bpy
from PIL import Image

class BlendScriptExecuter():
    
    def run_blend_script(self, script, sync=True, blend_file=None, silently_error=False):
        
        # we need to figure out how many excess spaces or tabs are added to the string
        # The first line will define the baseline extra spaces
        
        spaces = len(re.match('^[\\s]+', script).group(0)) - 1
        script = re.sub('\\n[\\s]{' + str(spaces) + '}', '\n', script)
        
        # we are going to try and replace all the {test} vals in the string
        matches = re.findall('(?<!{){[a-zA-Z0-9_]+}', script)
                    
        for match in matches:

            # strip curly brackets
            match = match[1:-1]
            attrs = match.split('.')
            result_val = self.props
            for attr in attrs:
                result_val = getattr(result_val, match)
            if attr == None:
                raise Exception('{} does not have attribute {}'.format(self.bl_idname, match))
                
            # if we use slashes, we may need to double down

            if isinstance(result_val, str):
                result_val = result_val.replace('\\','\\\\')
                result_val = 'r\'' + result_val + '\''
            else:
                result_val = str(list(result_val))
            
                
            script = re.sub('{' + match + '}', result_val, script)
            continue
        print(script)
            
        # at this point, we should have a complete script
        process = None
        cmd = bpy.app.binary_path
        
        # if a blend file path is defined. open that first
        if blend_file is not None:
            cmd += ' "{}"'.format(blend_file)
            
        cmd += ' -b'
        
        if 'sys.exit' not in script:
            cmd += ' --python-exit-code 1 '
            
        cmd += ' --python-expr "{}"'.format(script)
        
        process = subprocess.Popen(cmd)
        
        if sync:
            process.wait()
        
        return process.returncode
            

class GenerateMetalProperties(PropertyGroup):
    metal_name : StringProperty(name="Metal Name",
                                description="The name for the new metal",
                                default="")
                                
    metal_color : FloatVectorProperty(name="Metal Color",
                                      subtype='COLOR',
                                      default=(1.0, 1.0, 1.0),
                                      min=0.0, max=1.0)
                                      
    # actual values are roughness values for principled shader
    finish_type : EnumProperty(name="Finish Type",
                              description="Defines how smooth the metal is",
                              items=[
                                ("0.5", "Matte", ""),
                                ("0.01", "Gloss", "")
                              ])
    
    base_path = split(bpy.app.binary_path)[0]
    finished_metal_path = join(base_path, 'data', 'materials', 'Metals', 'Finished Metals', 'Metals.blend')
    rod_metal_path = join(base_path, 'data', 'materials', 'Cabinet Materials', 'Metals', 'Rod Materials.blend')
    
    # This decides where we are storing the new metal    
    metal_type : EnumProperty(name="Metal Type",
                              description="Decides where to save the material",
                              items=[
                                (finished_metal_path, "Finished Metal", ""),
                                (rod_metal_path, "Rod Metal", "")
                              ])
                              
                              
class SNAP_OT_ConfirmGenerateMetal(Operator):
    bl_idname = "material.confirm_generate_metal"
    bl_label = "Metal with that name exists. Do you want to replace it?"       
    
    def invoke(self, context, event):
        props = bpy.context.window_manager.AddMetalProps
        source_file = props.metal_type
        material_name = props.metal_name
        source_dir = os.path.dirname(source_file)
        thumbnail_path = join(source_dir, material_name) + '.png'
                
        if exists(thumbnail_path):
            
            return context.window_manager.invoke_confirm(self, event)
        else:
            return self.execute(context)
        
    def execute(self, context):
        bpy.ops.material.generate_metal('INVOKE_DEFAULT')
        return {'FINISHED'}
    

class SNAP_OT_GenerateMetal(BlendScriptExecuter, Operator):
    bl_idname = "material.generate_metal"
    bl_label = "Create metal"
    
    generate_thumbnail_script = """
        import bpy
        import sys
        import os
        
        source_file = {metal_type}
        material_name = {metal_name}
        source_dir = os.path.dirname(source_file)
        thumbnail_path = os.path.join(source_dir, material_name)
                    
        def inch_to_meter(inch):
            return round(inch / 39.3700787, 6)
        
        with bpy.data.libraries.load(source_file, False, True) as (data_from, data_to):
            for mat in data_from.materials:
                if mat == material_name:
                    data_to.materials = [mat]
                    break
                
        context = bpy.context
        
        for mat in data_to.materials:
            bpy.ops.mesh.primitive_cube_add()
            obj = bpy.context.scene.view_layers[0].objects.active
            obj.dimensions = (inch_to_meter(24), inch_to_meter(24), inch_to_meter(24))
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            mod = obj.modifiers.new('bevel','BEVEL')
            mod.segments = 5
            mod.width = .05
            bpy.ops.object.modifier_apply(modifier='bevel')
            
            # replaced fd ops with code snippets
            # originally fd_object.unwrap_mesh op:
            mode = obj.mode
            if obj.mode == 'OBJECT':
                bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.smart_project(angle_limit=66, island_margin=0, area_weight=0)
            if mode == 'OBJECT':
                bpy.ops.object.editmode_toggle()
                
            # originally fd_object.add_material_slot
            override = {'active_object':obj,
                        'object':obj,
                        'window':context.window,
                        'region':context.region}
            bpy.ops.object.material_slot_add(override)
            for slot in obj.material_slots:
                slot.material = mat
            bpy.ops.view3d.camera_to_view_selected()
            render = bpy.context.scene.render
            render.use_file_extension = True
            render.filepath = thumbnail_path
            render.engine = 'BLENDER_EEVEE'
            bpy.ops.render.render(write_still=True)
        """

    create_material_script = """
        import bpy
        import sys
        
        loc = {metal_type}
        name = {metal_name}
        color = [*{metal_color}, 1]
        roughness = float({finish_type})
        mats = bpy.data.materials
        def create_metal(name, color, roughness):
            
            mat = mats.get(name)
            if mat is None:
                mat = mats.new(name)
                            
            mat.use_nodes = True
            mat.use_fake_user = True
            nodes = mat.node_tree.nodes
            principled_node = nodes.get('Principled BSDF')
            principled_node.inputs['Base Color'].default_value = color
            principled_node.inputs['Roughness'].default_value = roughness
            principled_node.inputs['Metallic'].default_value = 1
            
        create_metal(name, color, roughness)    
        bpy.ops.wm.save_as_mainfile(filepath=loc)
        sys.exit(0)
        """
            
    def execute(self, context):
        self.props = bpy.context.window_manager.AddMetalProps
    
        if self.props.metal_name == '':
            raise Exception('you need a metal name')

        # 1. create material from values in the appropriate blend file                
        if not exists(self.props.metal_type):
            raise Exception('the file {} must exist'.format(self.props.metal_type))
            
        source_file = self.props.metal_type
        material_name = self.props.metal_name
        source_dir = os.path.dirname(source_file)
        thumbnail_path = join(source_dir, material_name) + '.png'
        
        exitcode = self.run_blend_script(self.create_material_script, blend_file=self.props.metal_type)
        
        if exitcode != 0:
            print('if err includes dependency issues, make sure file at {} has all mats upgraded to 2.8. Check other logs for actual error'.format(self.props.metal_type))
        print('finished')
            
        # 2. generate preview image
        thumbnail_template_loc = os.path.join(os.path.dirname(bpy.app.binary_path), 'thumbnail.blend')
        
        if not exists(thumbnail_template_loc):
            raise Exception('the file "thumbnail.blend" needs to be in the same dir as the blender binary')
        
        self.run_blend_script(self.generate_thumbnail_script, blend_file=thumbnail_template_loc)
        
        # TODO: 3. refresh the file broswer to include thumbnail

        return {'FINISHED'}
    
    
class SNAP_PT_GenerateMetalPanel(Panel):
    bl_idname="SNAP_PT_generate_metal"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "Create Metal"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        return True 
    
    def draw(self, context):
        layout = self.layout
        AddMetalProps = bpy.context.window_manager.AddMetalProps
        layout.prop(AddMetalProps, 'metal_name')
        layout.prop(AddMetalProps, 'metal_color')
        layout.prop(AddMetalProps, 'finish_type')
        layout.prop(AddMetalProps, 'metal_type')
        layout.operator('material.confirm_generate_metal', text='Create Metal')
        

class MelamineLoaderProperties(PropertyGroup):
    filepath: StringProperty(name="File Path", subtype="FILE_PATH")
    name: StringProperty(name="Name")
    

class SNAP_PT_MelamineLoader(Panel):
    bl_idname="SNAP_PT_SNAP_PT_melamine_loader"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "Create Melamine from Image"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        return True 
    
    def draw(self, context):
        layout = self.layout
        MelamineLoader = bpy.context.window_manager.MelamineLoader
        layout.prop(MelamineLoader, 'name')
        layout.prop(MelamineLoader, 'filepath', text="Image Location")
        layout.operator('material.confirm_create_melamine', text="Create Melamine Material")
        
class SNAP_OT_ConfirmMelamineLoader(Operator):
    bl_idname = "material.confirm_create_melamine"
    bl_label = "Melamine with that name exists. Do you want to replace it?"       
    
    def invoke(self, context, event):
        props = bpy.context.window_manager.MelamineLoader
        name = props.name
        base_path = split(bpy.app.binary_path)[0]
        loc = join(base_path, 'libraries','materials','Closet Materials', name +'.blend')
                
        if exists(loc):
            
            return context.window_manager.invoke_confirm(self, event)
        else:
            return self.execute(context)
        
    def execute(self, context):
        bpy.ops.material.create_melamine('INVOKE_DEFAULT')
        return {'FINISHED'}



class SNAP_OT_MelamineLoader(BlendScriptExecuter, Operator):
    bl_idname = "material.create_melamine"
    bl_label = "Create Material From Image"
    script = """
        import bpy
        import os
        from os.path import split, join, splitext
        from PIL import Image
        import sys
        
        filepath = {filepath}
        name = {name}
        
        # settings up the paths. We are going to save it to the custom data folder
        base_path = split(bpy.app.binary_path)[0]
        melamine_loc = join(base_path, 'libraries', 'materials', 'Closet Materials')
        img_name = split(filepath)[1]
        new_img_path = join(melamine_loc, img_name)
        
        # We are going to open this in PIL, first, for resizing. It is more robust
        img = Image.open(filepath)
        img.thumbnail([512, 512])
        img.save(join(melamine_loc, img_name))
        
        # This script should run on a different instance of blender
        
        bl_img = bpy.data.images.load(join(melamine_loc, img_name), check_existing=False)
        for mat in bpy.data.materials:
            bpy.data.materials.remove(mat)
        
        mat_name = splitext(img_name)[0]
        mat = bpy.data.materials.new(mat_name)
        mat.use_fake_user = True
        mat.use_nodes = True
        tree = mat.node_tree
        nodes = tree.nodes
        links = tree.links
        
        # I could work with the default nodes, but it is easier to create them myself
        for node in nodes:
            nodes.remove(node)
            
        output_node = nodes.new('ShaderNodeOutputMaterial')
        output_node.location = (300, 0)
        
        principled_node = nodes.new('ShaderNodeBsdfPrincipled')
        principled_node.location = (0, 0)
        
        col_node = nodes.new('ShaderNodeTexImage')
        col_node.location = (-300, 0)
        col_node.image = bl_img
        
        links.new(col_node.outputs[0], principled_node.inputs['Base Color'])
        links.new(principled_node.outputs[0], output_node.inputs[0])
        
        bpy.ops.wm.save_as_mainfile(filepath=join(melamine_loc, name + '.blend'))
        sys.exit(0)
        """
    
    def execute(self, context):
        
        # we need to assign this for the script executor
        self.props = bpy.context.window_manager.MelamineLoader
        exitcode = self.run_blend_script(self.script)
        
        if exitcode != 0:
            raise Exception('Operator failed')
            return {'CANCELLED'}
                
        return {'FINISHED'}

classes = (
    SNAP_OT_GenerateMetal,
    SNAP_PT_GenerateMetalPanel,
    SNAP_OT_ConfirmGenerateMetal,
    GenerateMetalProperties,
    SNAP_OT_MelamineLoader,
    SNAP_PT_MelamineLoader,
    MelamineLoaderProperties,
    SNAP_OT_ConfirmMelamineLoader
)

def register():
    for cls in classes:
        register_class(cls)
    bpy.types.WindowManager.AddMetalProps = PointerProperty(type=GenerateMetalProperties)
    bpy.types.WindowManager.MelamineLoader = PointerProperty(type=MelamineLoaderProperties)

def unregister():
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.WindowManager.AddMetalProps
    del bpy.types.WindowManager.MelamineLoader

if __name__ == "__main__":
    register()