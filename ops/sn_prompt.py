import bpy
from bpy.types import Header, Menu, Operator, PropertyGroup, Panel

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       BoolVectorProperty,
                       PointerProperty,
                       CollectionProperty,
                       EnumProperty)

from ..sn_props import prompt_types


class SN_PPT_OT_add_prompt(Operator):
    bl_idname = "sn_prompt.add_prompt"
    bl_label = "Add Prompt"
    bl_description = "This adds a prompt to the object"
    bl_options = {'UNDO'}
    
    obj_name: StringProperty(name="Data Name",default="")

    prompt_name: StringProperty(name="Prompt Name",default="New Prompt")
    prompt_type: EnumProperty(name="Prompt Type",items=prompt_types)
    obj = None

    @classmethod
    def poll(cls, context):
        return True

    def get_data(self,context):
        if self.obj_name in bpy.data.objects:
            return bpy.data.objects[self.obj_name]
        else:
            return context.object

    def execute(self, context):     
        self.obj.snap.add_prompt(self.prompt_type,self.prompt_name)
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self,context,event):
        self.obj = bpy.data.objects[self.obj_name]    
        self.prompt_name = "New Prompt"
        counter = 1
        while self.prompt_name + " " + str(counter) in self.obj.snap.prompts:
            counter += 1
        self.prompt_name = self.prompt_name + " " + str(counter)
            
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=250)

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Prompt Name")
        row.prop(self,"prompt_name",text="")
        row = layout.row()
        row.label(text="Prompt Type")
        row.prop(self,"prompt_type",text="")


class SN_PPT_OT_delete_prompt(Operator):
    bl_idname = "sn_prompt.delete_prompt"
    bl_label = "Delete Prompt"
    bl_description = "This deletes the prompt that is passed in with prompt_name"
    bl_options = {'UNDO'}
    
    obj_name: StringProperty(name="Object Name",default="") #WHY DON"T POINTERS WORK?
    prompt_name: StringProperty(name="Prompt Name",default="New Prompt")

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        obj = bpy.data.objects[self.obj_name]
        obj.snap.delete_prompt(self.prompt_name)
        return {'FINISHED'}

    def invoke(self,context,event):
        if self.obj_name in bpy.data.objects:
            obj = bpy.data.objects[self.obj_name]
            wm = context.window_manager
            return wm.invoke_props_dialog(self, width=380)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Are you sure you want to delete the prompt")
        layout.label(text=self.prompt_name)


class SN_PPT_OT_add_calculator(Operator):
    bl_idname = "sn_prompt.add_calculator"
    bl_label = "Add Calculator"
    bl_description = "This adds a calculator to the object"
    bl_options = {'UNDO'}
    
    obj_name: StringProperty(name="Data Name",default="")

    calculator_name: StringProperty(name="Calculator Name",default="New Prompt")
    obj = None

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):     
        calc_distance_obj = bpy.data.objects.new('Calc Distance Obj',None)
        calc_distance_obj.empty_display_size = .001        
        calc_distance_obj.parent = self.obj.parent
        context.view_layer.active_layer_collection.collection.objects.link(calc_distance_obj)
        self.obj.snap.add_calculator(self.calculator_name,calc_distance_obj)
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self,context,event):
        self.obj = bpy.data.objects[self.obj_name]
        self.calculator_name = "New Calculator"
        counter = 1
        while self.calculator_name + " " + str(counter) in self.obj.snap.calculators:
            counter += 1
        self.calculator_name = self.calculator_name + " " + str(counter)
            
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=250)

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Calculator Name")
        row.prop(self,"calculator_name",text="")


class SN_PPT_OT_add_calculator_prompt(Operator):
    bl_idname = "sn_prompt.add_calculator_prompt"
    bl_label = "Add Calculator"
    bl_description = "This adds a prompt to a calculator"
    bl_options = {'UNDO'}
    
    calculator_name: StringProperty(name="Calculator Name",default="")
    obj_name: StringProperty(name="Data Name",default="")

    prompt_name: StringProperty(name="Prompt Name",default="New Prompt")
    obj = None

    @classmethod
    def poll(cls, context):
        return True

    def get_data(self,context):
        if self.obj_name in bpy.data.objects:
            return bpy.data.objects[self.obj_name]
        else:
            return context.object

    def get_calculator(self):
        for calculator in self.obj.snap.calculators:
            if calculator.name == self.calculator_name:
                return calculator

    def execute(self, context):
        calculator = self.get_calculator()      
        calculator.add_calculator_prompt(self.prompt_name)
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self,context,event):
        self.obj = bpy.data.objects[self.obj_name]
        self.prompt_name = "New Prompt"
        counter = 1
        calculator = self.get_calculator()
        while self.prompt_name + " " + str(counter) in calculator.prompts:
            counter += 1
        self.prompt_name = self.prompt_name + " " + str(counter)
            
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=250)

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Prompt Name")
        row.prop(self,"prompt_name",text="")


class SN_PPT_OT_edit_calculator(Operator):
    bl_idname = "sn_prompt.edit_calculator"
    bl_label = "Edit Calculator"
    bl_description = "This opens a dialog to edit a calculator"
    bl_options = {'UNDO'}
    
    calculator_name: StringProperty(name="Calculator Name",default="")
    obj_name: StringProperty(name="Data Name",default="")

    prompt_name: StringProperty(name="Prompt Name",default="New Prompt")
    obj = None
    calculator = None

    @classmethod
    def poll(cls, context):
        return True

    def get_data(self,context):
        if self.obj_name in bpy.data.objects:
            return bpy.data.objects[self.obj_name]
        else:
            return context.object

    def get_calculator(self):
        for calculator in self.obj.snap.calculators:
            if calculator.name == self.calculator_name:
                return calculator

    def execute(self, context):
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self,context,event):
        self.obj = self.get_data(context)
        self.calculator = self.get_calculator()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=250)

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Calculator Name")
        row.prop(self.calculator,"name",text="")


class SN_PPT_OT_run_calculator(Operator):
    bl_idname = "sn_prompt.run_calculator"
    bl_label = "Run Calculator"
    bl_description = "This runs the calculate function for a calculator"
    bl_options = {'UNDO'}
    
    calculator_name: StringProperty(name="Calculator Name",default="")
    obj_name: StringProperty(name="Data Name",default="")

    prompt_name: StringProperty(name="Prompt Name",default="New Prompt")
    obj = None
    calculator = None

    @classmethod
    def poll(cls, context):
        return True

    def get_data(self,context):
        if self.obj_name in bpy.data.objects:
            return bpy.data.objects[self.obj_name]
        else:
            return context.object

    def get_calculator(self):
        for calculator in self.obj.snap.calculators:
            if calculator.name == self.calculator_name:
                return calculator

    def execute(self, context):
        self.obj = self.get_data(context)
        self.calculator = self.get_calculator()
        if self.calculator:
            self.calculator.calculate()
        context.area.tag_redraw()
        return {'FINISHED'}


class SN_PPT_OT_edit_prompt(Operator):
    bl_idname = "sn_prompt.edit_prompt"
    bl_label = "Edit Prompt"
    bl_description = "This opens a dialog to edit a prompt"
    bl_options = {'UNDO'}
    
    obj_name: StringProperty(name="Object Name",default="") #WHY DON"T POINTERS WORK?
    prompt_name: StringProperty(name="Prompt Name",default="New Prompt")

    prompt = None

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self,context,event):
        if self.obj_name in bpy.data.objects:
            obj = bpy.data.objects[self.obj_name]
            self.prompt = obj.snap.prompts[self.prompt_name]
            wm = context.window_manager
            return wm.invoke_props_dialog(self, width=380)

    def draw(self, context):
        layout = self.layout
        self.prompt.draw_prompt_properties(layout)


class SN_PPT_OT_add_comboxbox_value(Operator):
    bl_idname = "sn_prompt.add_combobox_value"
    bl_label = "Add Combobox Value"
    bl_description = "This adds a combobox item to a combobox prompt"
    bl_options = {'UNDO'}
    
    obj_name: StringProperty(name="Object Name",default="") #WHY DON"T POINTERS WORK?
    prompt_name: StringProperty(name="Prompt Name",default="New Prompt")

    combobox_name: StringProperty(name="Combobox Name",default="Combobox Item")

    prompt = None

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        item = self.prompt.combobox_items.add()
        item.name = self.combobox_name
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self,context,event):
        if self.obj_name in bpy.data.objects:
            obj = bpy.data.objects[self.obj_name]
            self.prompt = obj.snap.prompts[self.prompt_name]
            wm = context.window_manager
            return wm.invoke_props_dialog(self, width=250)

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Name")
        row.prop(self,'combobox_name',text="")


class SN_PPT_OT_delete_comboxbox_value(Operator):
    bl_idname = "sn_prompt.delete_combobox_value"
    bl_label = "Delete Combobox Value"
    bl_description = "This deletes a combobox item from a combobox"
    bl_options = {'UNDO'}

    obj_name: StringProperty(name="Object Name",default="") #WHY DON"T POINTERS WORK?
    prompt_name: StringProperty(name="Prompt Name",default="New Prompt")

    combobox_name: StringProperty(name="Combobox Name",default="Combobox Item")

    prompt = None

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        #TODO: Remove Item
        return {'FINISHED'}

    def invoke(self,context,event):
        if self.obj_name in bpy.data.objects:
            obj = bpy.data.objects[self.obj_name]
            self.prompt = obj.snap.prompts[self.prompt_name]
            wm = context.window_manager
            return wm.invoke_props_dialog(self, width=380)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Are you sure you want to delete the combobox value")


class SN_PPT_OT_update_all_prompts_in_scene(Operator):
    bl_idname = "sn_prompt.update_all_prompts_in_scene"
    bl_label = "Update All Prompts In Scene"
    bl_description = "This will update all of the prompts in the scene with the value that is passed in"
    bl_options = {'UNDO'}

    prompt_name: StringProperty(name="Prompt Name")
    prompt_type: StringProperty(name="Prompt Type")
    float_value: FloatProperty(name="Float Value")
    bool_value: BoolProperty(name="Bool Value")
    string_value: StringProperty(name="String Value")

    def execute(self, context):
        for obj in context.scene.objects:
            if obj.snap.prompts:
                prompt = obj.snap.get_prompt(self.prompt_name)
                if prompt:
                    if self.prompt_type in {'NUMBER', 'QUANTITY', 'DISTANCE', 'PERCENTAGE', 'ANGLE', 'PRICE'}:
                        prompt.set_value(self.float_value)
                    if self.prompt_type in {'COMBOBOX', 'TEXT'}:
                        prompt.set_value(self.string_value)
                    if self.prompt_type == 'CHECKBOX':
                        prompt.set_value(self.bool_value)
                    obj.location = obj.location
        return {'FINISHED'}


classes = (
    SN_PPT_OT_add_prompt,
    SN_PPT_OT_delete_prompt,
    SN_PPT_OT_add_calculator,
    SN_PPT_OT_add_calculator_prompt,
    SN_PPT_OT_edit_calculator,
    SN_PPT_OT_run_calculator,
    SN_PPT_OT_edit_prompt,
    SN_PPT_OT_add_comboxbox_value,
    SN_PPT_OT_delete_comboxbox_value,
    SN_PPT_OT_update_all_prompts_in_scene
)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
