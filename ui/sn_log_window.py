import bpy


class SN_OT_log_window(bpy.types.Operator):
    """A pop-up window with a some message for the user."""

    bl_idname = "snap.log_window"
    bl_label = "Log Window"
    bl_options = {'UNDO'}

    message: bpy.props.StringProperty(name="Message", default="")
    message2: bpy.props.StringProperty(name="Message_2", default="")
    icon: bpy.props.StringProperty(name="Icon")

    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        lay = self.layout
        box = lay.box()
        box.label(text=self.message, icon=self.icon)
        if self.message2 != "":
            box.label(text=self.message2)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


def register():
    bpy.utils.register_class(SN_OT_log_window)


def unregister():
    bpy.utils.unregister_class(SN_OT_log_window)
