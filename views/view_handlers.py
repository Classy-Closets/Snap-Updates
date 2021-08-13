from .opengl_dim import draw_opengl
import bpy


def register():
    bpy.types.SpaceView3D.draw_handler_add(draw_opengl, (None, None), 'WINDOW', 'POST_PIXEL')


def unregister():
    return
    bpy.types.SpaceView3D.draw_handler_remove(draw_opengl, (None, None), 'WINDOW', 'POST_PIXEL')
