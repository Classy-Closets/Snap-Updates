'''
Created on Mar 27, 2017

@author: montes
'''

import bpy
import bgl
import blf
import os
import time
import math
import mathutils
from fractions import Fraction
from mv import utils
from bpy_extras import view3d_utils, object_utils
import bpy_extras.image_utils as img_utils

IMP_CONV_FAC_INCHES = 39.3700787

def get_imp_rounded(value):
    g_props = bpy.context.scene.mv.opengl_dim
    precision = g_props.gl_precision
    inches = value * IMP_CONV_FAC_INCHES
    result = math.modf(inches)
    
    return (round(result[0], precision), result[1])

def fmt_imp(value):
    g_props = bpy.context.scene.mv.opengl_dim
    dist_imp = get_imp_rounded(value)
    str_dist = "{}{}{}"
    
    if g_props.gl_dim_units in ('FEET', 'AUTO'):
        feet = int(dist_imp[1] // 12)
        inch = int(dist_imp[1] % 12)
        fract = Fraction(dist_imp[0])     
        
        if feet == 0:
            feet_fmt = ""
        else:
            feet_fmt = str(feet) + "' "
        if inch == 0:
            inch_fmt = ""
            if fract != 0 and g_props.gl_number_format == 'DECIMAL':
                inch_fmt += "0"
        else:
            inch_fmt = str(inch)
            
        if fract == 0:
            fract_fmt = ""
            if inch != 0:
                inch_fmt += '"'
        elif g_props.gl_number_format == 'FRACTION':
            fract_fmt = " " + str(fract) + '"'
        else:
            fract_fmt = "." + str(dist_imp[0])[2:] + '"'
    
        return str_dist.format(feet_fmt, inch_fmt, fract_fmt)
    
    if g_props.gl_dim_units in ('INCH', 'AUTO'):
        inch = int(dist_imp[1])
        fract = Fraction(dist_imp[0])
        
        if inch == 0:
            inch_fmt = "" if g_props.gl_number_format == 'FRACTION' else "0"
        else:
            inch_fmt = str(inch)
            
        if fract == 0:
            fract_fmt = ""    
        elif g_props.gl_number_format == 'FRACTION':
            fract_fmt = " " + str(fract)
        else:
            fract_fmt = "." + str(dist_imp[0])[2:]
    
        return str_dist.format(inch_fmt, fract_fmt, '"')

def get_rv3d(context, region):
    if not context.space_data.region_quadviews:
        return context.space_data.region_3d
    else:
        if context.area.type != 'VIEW_3D' or context.space_data.type != 'VIEW_3D':
            return
        i = -1
        for region in context.area.regions:
            if region.type == 'WINDOW':
                i += 1
                if context.region.id == region.id:
                    break
        else:
            return

        return context.space_data.region_quadviews[i]    

def draw_opengl(self, context):
    context = bpy.context
    
    if context.window_manager.mv.use_opengl_dimensions:
        region = context.region
        rv3d = get_rv3d(context, region)
        
        
        if not rv3d: return

        layers = []
        for x in range(0, 20):
            if bpy.context.scene.layers[x] is True:
                layers.extend([x])
    
        bgl.glEnable(bgl.GL_BLEND)
    
        for obj in context.scene.objects:
            if obj.mv.type == 'VISDIM_A':
                for x in range(0, 20):
                    if obj.layers[x] is True:
                        if x in layers:
                            opengl_dim = obj.mv.opengl_dim
                            if not opengl_dim.hide:
                                draw_dimensions(context, obj, opengl_dim, region, rv3d)
                        break
    
        #---------- restore opengl defaults
        bgl.glLineWidth(1)
        bgl.glDisable(bgl.GL_BLEND)
        bgl.glColor4f(0.0, 0.0, 0.0, 1.0)    
    
    else:
        return
    
def draw_dimensions(context, obj, i_props, region, rv3d):
    g_props = bpy.context.scene.mv.opengl_dim
    
    fsize = g_props.gl_font_size    
    a_size = g_props.gl_arrow_size
    a_type = g_props.gl_arrow_type
    b_type = g_props.gl_arrow_type
    
    if i_props.gl_color == 0:
        rgb = g_props.gl_default_color
    else:
        rgb = g_props.standard_colors[i_props.gl_color]                        
 
    a_p1 = get_location(obj)
    b_p1 = None
    
    for child in obj.children:
        if child.mv.type == 'VISDIM_B':
            b_p1 = get_location(child)
    
    if a_p1 and b_p1:
        dist = utils.calc_distance(a_p1, b_p1)  
        
        loc = get_location(obj)
        midpoint3d = interpolate3d(a_p1, b_p1, math.fabs(dist / 2))
        vn = mathutils.Vector((midpoint3d[0] - loc[0],
                               midpoint3d[1] - loc[1],
                               midpoint3d[2] - loc[2]))
      
        vn.normalize()
          
        v1 = [a_p1[0], a_p1[1], a_p1[2]]
        v2 = [b_p1[0], b_p1[1], b_p1[2]]    
          
        screen_point_ap1 = get_2d_point(region, rv3d, a_p1)
        screen_point_bp1 = get_2d_point(region, rv3d, b_p1)
        
        if None in (screen_point_ap1,screen_point_bp1):
            return
        elif check_overlap_2d_point(screen_point_ap1, screen_point_bp1) and i_props.gl_label == "":
            return
          
        bgl.glLineWidth(i_props.gl_width)
        bgl.glColor4f(rgb[0], rgb[1], rgb[2], rgb[3])
              
        midpoint3d = interpolate3d(v1, v2, math.fabs(dist / 2))
        gap3d = (midpoint3d[0], midpoint3d[1], midpoint3d[2])
        txtpoint2d = get_2d_point(region, rv3d, gap3d)
        
        if not i_props.line_only:
            if i_props.gl_label == "":
                txt_dist = str(format_distance(dist))
            else:
                txt_dist = i_props.gl_label
          
            draw_text(txtpoint2d[0], 
                      txtpoint2d[1],
                      txt_dist, 
                      rgb, 
                      fsize,
                      i_props,
                      screen_point_ap1,
                      screen_point_bp1)
      
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glColor4f(rgb[0], rgb[1], rgb[2], rgb[3])      
    
        if not i_props.line_only:
            draw_arrow(screen_point_ap1, screen_point_bp1, a_size, a_type, b_type)  
            draw_extension_lines(screen_point_ap1, screen_point_bp1, a_size)
            
        draw_line(screen_point_ap1, screen_point_bp1)
                       
def draw_text(x_pos, y_pos, display_text, rgb, fsize, i_props, anchor_co, endpoint_co):
    font_id = 0
    blf.size(font_id, fsize, 72)
    #- height of one line
    mwidth, mheight = blf.dimensions(font_id, "Tp")  # uses high/low letters

    origional_x = x_pos
    origional_y = y_pos

    # split lines
    mylines = display_text.split("|")
    maxwidth = 0
    maxheight = len(mylines) * mheight

    #---------- Draw all lines-+
    for index, line in enumerate(mylines):
        text_width, text_height = blf.dimensions(font_id, line)

        y_pos -= mheight * index
        x_pos -= text_width * 0.5     
        
        if not check_overlap_2d_point(anchor_co, endpoint_co):
            #if vertical line text placement
            if anchor_co[0] == endpoint_co[0]:
                if i_props.v_line_text_placement == 'LEFT':
                    x_pos -= text_width * 0.5 + i_props.line_to_text_pad * 2
                elif i_props.v_line_text_placement == 'RIGHT':
                    x_pos += text_width * 0.5
            
            #horizontal line text placement
            if anchor_co[1] == endpoint_co[1]:
                if i_props.h_line_text_placement == 'TOP':
                    y_pos += i_props.line_to_text_pad
                elif i_props.h_line_text_placement == 'BOTTOM':
                    y_pos -= text_height + i_props.line_to_text_pad
        
            blf.position(font_id,
                         x_pos + i_props.gl_text_x,
                         y_pos + i_props.gl_text_y,
                         0)
        else:
            blf.position(font_id,
                         x_pos,
                         y_pos,
                         0)
        
        bgl.glColor4f(rgb[0], rgb[1], rgb[2], rgb[3])
        blf.draw(font_id, " " + line)
        
        # saves max width
        if maxwidth < text_width:
            maxwidth = text_width
            
        #Reset original position for multiple lines
        x_pos = origional_x
        y_pos = origional_y

    return maxwidth, maxheight

def format_distance(value):
    g_props = bpy.context.scene.mv.opengl_dim
    bldr_units = bpy.context.scene.unit_settings.system
    pr = g_props.gl_precision
    fmt = "%1." + str(pr) + "f"
    units = g_props.gl_dim_units
    
    if units == 'AUTO' and bldr_units == "METRIC":
        if round(value, 2) >= 1.0:
            fmt += " m"
            tx_dist = fmt % value
        else:
            if round(value, 2) >= 0.01:
                fmt += " cm"
                d_cm = value * 100
                tx_dist = fmt % d_cm
            else:
                fmt += " mm"
                d_mm = value * 1000
                tx_dist = fmt % d_mm

    elif units == "METER":
        fmt += " m"
        tx_dist = fmt % value

    elif units == "CENTIMETER":
        fmt += " cm"
        d_cm = value * (100)
        tx_dist = fmt % d_cm

    elif units == "MILIMETER":
        fmt += " mm"
        d_mm = value * (1000)
        tx_dist = fmt % d_mm

    elif units in ("FEET", "INCH") or units == 'AUTO' and bldr_units == 'IMPERIAL':
        tx_dist = fmt_imp(value)
        
    else:
        tx_dist = fmt % value

    return tx_dist

def draw_extension_lines(v1, v2, size=20):
    rad_a = math.radians(90)
    rad_b = math.radians(270)

    v = interpolate3d((v1[0], v1[1], 0.0), (v2[0], v2[1], 0.0), size)
    v1i = (v[0] - v1[0], v[1] - v1[1])

    v = interpolate3d((v2[0], v2[1], 0.0), (v1[0], v1[1], 0.0), size)
    v2i = (v[0] - v2[0], v[1] - v2[1])

    v1a = (int(v1i[0] * math.cos(rad_a) - v1i[1] * math.sin(rad_a) + v1[0]),
           int(v1i[1] * math.cos(rad_a) + v1i[0] * math.sin(rad_a)) + v1[1])
    v1b = (int(v1i[0] * math.cos(rad_b) - v1i[1] * math.sin(rad_b) + v1[0]),
           int(v1i[1] * math.cos(rad_b) + v1i[0] * math.sin(rad_b) + v1[1]))

    v2a = (int(v2i[0] * math.cos(rad_a) - v2i[1] * math.sin(rad_a) + v2[0]),
           int(v2i[1] * math.cos(rad_a) + v2i[0] * math.sin(rad_a)) + v2[1])
    v2b = (int(v2i[0] * math.cos(rad_b) - v2i[1] * math.sin(rad_b) + v2[0]),
           int(v2i[1] * math.cos(rad_b) + v2i[0] * math.sin(rad_b) + v2[1]))
    
    draw_line(v1, v1a)
    draw_line(v1, v1b)
    
    draw_line(v2, v2a)
    draw_line(v2, v2b)

def draw_arrow(v1, v2, size=20, a_typ="1", b_typ="1"):
    rad45 = math.radians(45)
    rad315 = math.radians(315)
    rad90 = math.radians(90)
    rad270 = math.radians(270)

    v = interpolate3d((v1[0], v1[1], 0.0), (v2[0], v2[1], 0.0), size)

    v1i = (v[0] - v1[0], v[1] - v1[1])

    v = interpolate3d((v2[0], v2[1], 0.0), (v1[0], v1[1], 0.0), size)
    v2i = (v[0] - v2[0], v[1] - v2[1])

    if a_typ == "3":
        rad_a = rad90
        rad_b = rad270
    else:
        rad_a = rad45
        rad_b = rad315

    v1a = (int(v1i[0] * math.cos(rad_a) - v1i[1] * math.sin(rad_a) + v1[0]),
           int(v1i[1] * math.cos(rad_a) + v1i[0] * math.sin(rad_a)) + v1[1])
    v1b = (int(v1i[0] * math.cos(rad_b) - v1i[1] * math.sin(rad_b) + v1[0]),
           int(v1i[1] * math.cos(rad_b) + v1i[0] * math.sin(rad_b) + v1[1]))

    if b_typ == "3":
        rad_a = rad90
        rad_b = rad270
    else:
        rad_a = rad45
        rad_b = rad315

    v2a = (int(v2i[0] * math.cos(rad_a) - v2i[1] * math.sin(rad_a) + v2[0]),
           int(v2i[1] * math.cos(rad_a) + v2i[0] * math.sin(rad_a)) + v2[1])
    v2b = (int(v2i[0] * math.cos(rad_b) - v2i[1] * math.sin(rad_b) + v2[0]),
           int(v2i[1] * math.cos(rad_b) + v2i[0] * math.sin(rad_b) + v2[1]))

    if a_typ == "1" or a_typ == "3":
        draw_line(v1, v1a)
        draw_line(v1, v1b)

    if b_typ == "1" or b_typ == "3":
        draw_line(v2, v2a)
        draw_line(v2, v2b)

    if a_typ == "2":
        draw_triangle(v1, v1a, v1b)
    if b_typ == "2":
        draw_triangle(v2, v2a, v2b)

#     draw_line(v1, v2)

def draw_line(v1, v2):
    # noinspection PyBroadException
    try:
        if v1 is not None and v2 is not None:
            bgl.glBegin(bgl.GL_LINES)
            bgl.glVertex2f(*v1)
            bgl.glVertex2f(*v2)
            bgl.glEnd()
    except:
        pass

def draw_triangle(v1, v2, v3):
    # noinspection PyBroadException
    try:
        if v1 is not None and v2 is not None and v3 is not None:
            bgl.glBegin(bgl.GL_TRIANGLES)
            bgl.glVertex2f(*v1)
            bgl.glVertex2f(*v2)
            bgl.glVertex2f(*v3)
            bgl.glEnd()
    except:
        pass

def get_2d_point(region, rv3d, point3d):
    if rv3d is not None and region is not None:
        return view3d_utils.location_3d_to_region_2d(region, rv3d, point3d)
    else:
        return get_render_location(point3d)
    
def check_overlap_2d_point(sp1, sp2):
    if round(sp1[0], 2) == round(sp2[0], 2) and round(sp1[1], 2) == round(sp2[1], 2):
        return True
    else:
        return False

def get_render_location(mypoint):
    v1 = mathutils.Vector(mypoint)
    scene = bpy.context.scene
    co_2d = object_utils.world_to_camera_view(scene, scene.camera, v1)
    # Get pixel coords
    render_scale = scene.render.resolution_percentage / 100
    render_size = (int(scene.render.resolution_x * render_scale),
                   int(scene.render.resolution_y * render_scale))

    return [round(co_2d.x * render_size[0]), round(co_2d.y * render_size[1])]

def interpolate3d(v1, v2, d1):
    # calculate vector
    v = (v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])
    # calculate distance between points
    d0 = utils.calc_distance(v1, v2)

    # calculate interpolate factor (distance from origin / distance total)
    # if d1 > d0, the point is projected in 3D space
    if d0 > 0:
        x = d1 / d0
    else:
        x = d1

    final = (v1[0] + (v[0] * x), v1[1] + (v[1] * x), v1[2] + (v[2] * x))
    return final

def get_location(mainobject):
    # Using World Matrix
    m4 = mainobject.matrix_world

    return [m4[0][3], m4[1][3], m4[2][3]]

def render_opengl(self, context):
    from math import ceil

    layers = []
    scene = context.scene
    for x in range(0, 20):
        if scene.layers[x] is True:
            layers.extend([x])

    objlist = context.scene.objects
    render_scale = scene.render.resolution_percentage / 100

    width = int(scene.render.resolution_x * render_scale)
    height = int(scene.render.resolution_y * render_scale)
    
    # I cant use file_format becuase the pdf writer needs jpg format
    # the file_format returns 'JPEG' not 'JPG'
#     file_format = context.scene.render.image_settings.file_format.lower()
    ren_path = bpy.path.abspath(bpy.context.scene.render.filepath) + ".jpg"
    
#     if len(ren_path) > 0:
#         if ren_path.endswith(os.path.sep):
#             initpath = os.path.realpath(ren_path) + os.path.sep
#         else:
#             (initpath, filename) = os.path.split(ren_path)
#         outpath = os.path.join(initpath, "ogl_tmp.png")
#     else:
#         self.report({'ERROR'}, "Invalid render path")
#         return False

    img = get_render_image(ren_path)
    
    if img is None:
        self.report({'ERROR'}, "Invalid render path:" + ren_path)
        return False

    tile_x = 240
    tile_y = 216
    row_num = ceil(height / tile_y)
    col_num = ceil(width / tile_x)
    
    cut4 = (col_num * tile_x * 4) - width * 4  
    totpixel4 = width * height * 4 

    viewport_info = bgl.Buffer(bgl.GL_INT, 4)
    bgl.glGetIntegerv(bgl.GL_VIEWPORT, viewport_info)
    
    img.gl_load(0, bgl.GL_NEAREST, bgl.GL_NEAREST)

    # 2.77 API change
    if bpy.app.version >= (2, 77, 0):
        tex = img.bindcode[0]
    else:
        tex = img.bindcode
    
    if context.scene.name in bpy.data.images:
        old_img = bpy.data.images[context.scene.name]
        old_img.user_clear()
        bpy.data.images.remove(old_img)
             
    img_result = bpy.data.images.new(context.scene.name, width, height)        
    
    tmp_pixels = [1] * totpixel4

    #---------- Loop for all tiles
    for row in range(0, row_num):
        for col in range(0, col_num):
            buffer = bgl.Buffer(bgl.GL_FLOAT, width * height * 4)
            bgl.glDisable(bgl.GL_SCISSOR_TEST)  # if remove this line, get blender screenshot not image
            bgl.glViewport(0, 0, tile_x, tile_y)

            bgl.glMatrixMode(bgl.GL_PROJECTION)
            bgl.glLoadIdentity()

            # defines ortographic view for single tile
            x1 = tile_x * col
            y1 = tile_y * row
            bgl.gluOrtho2D(x1, x1 + tile_x, y1, y1 + tile_y)

            # Clear
            bgl.glClearColor(0.0, 0.0, 0.0, 0.0)
            bgl.glClear(bgl.GL_COLOR_BUFFER_BIT | bgl.GL_DEPTH_BUFFER_BIT)

            bgl.glEnable(bgl.GL_TEXTURE_2D)
            bgl.glBindTexture(bgl.GL_TEXTURE_2D, tex)

            # defines drawing area
            bgl.glBegin(bgl.GL_QUADS)

            bgl.glColor3f(1.0, 1.0, 1.0)
            bgl.glTexCoord2f(0.0, 0.0)
            bgl.glVertex2f(0.0, 0.0)

            bgl.glTexCoord2f(1.0, 0.0)
            bgl.glVertex2f(width, 0.0)

            bgl.glTexCoord2f(1.0, 1.0)
            bgl.glVertex2f(width, height)

            bgl.glTexCoord2f(0.0, 1.0)
            bgl.glVertex2f(0.0, height)

            bgl.glEnd()

            for obj in objlist:
                if obj.mv.type == 'VISDIM_A':
                    for x in range(0, 20):
                        if obj.layers[x] is True:
                            if x in layers:
                                opengl_dim = obj.mv.opengl_dim
                                if not opengl_dim.hide:
                                    draw_dimensions(context, obj, opengl_dim, None, None)
                            break 

            #---------- copy pixels to temporary area
            bgl.glFinish()
            bgl.glReadPixels(0, 0, width, height, bgl.GL_RGBA, bgl.GL_FLOAT, buffer)  # read image data
            for y in range(0, tile_y):
                # final image pixels position
                p1 = (y * width * 4) + (row * tile_y * width * 4) + (col * tile_x * 4)
                p2 = p1 + (tile_x * 4)
                # buffer pixels position
                b1 = y * width * 4
                b2 = b1 + (tile_x * 4)

                if p1 < totpixel4:  # avoid pixel row out of area
                    if col == col_num - 1:  # avoid pixel columns out of area
                        p2 -= cut4
                        b2 -= cut4

                    tmp_pixels[p1:p2] = buffer[b1:b2]

    img_result.pixels = tmp_pixels[:]
    img.gl_free()

    img.user_clear()
    bpy.data.images.remove(img)
    os.remove(ren_path)
    bgl.glEnable(bgl.GL_SCISSOR_TEST)

    #---------- restore opengl defaults
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)
    
    if img_result is not None:            
        return img_result

def get_render_image(outpath):
    saved = False
    try:
        try:
            result = bpy.data.images['Render Result']
            if result.has_data is False:
                result.save_render(outpath)
                saved = True
        except:
            print("No render image found")
            return None

        if saved is False:
            result.save_render(outpath)

        img = img_utils.load_image(outpath)

        return img
    except:
        print("Unexpected render image error")
        return None

def get_2d_renderings(context):
    file_name = bpy.path.basename(context.blend_data.filepath).replace(".blend","")
    write_dir = os.path.join(bpy.app.tempdir, file_name)
    if not os.path.exists(write_dir): os.mkdir(write_dir)
    
    bpy.ops.fd_scene.prepare_2d_elevations()
    
    images = []
    
    #Render Each Scene
    for scene in bpy.data.scenes:
        if scene.mv.elevation_scene:
            context.screen.scene = scene

            # Set Render 2D Properties
            rd = context.scene.render
            rl = rd.layers.active
            freestyle_settings = rl.freestyle_settings
            rd.filepath = os.path.join(write_dir,scene.name)
            rd.image_settings.file_format = 'JPEG'
            rd.engine = 'BLENDER_RENDER'
            rd.use_freestyle = True
            rd.line_thickness = 0.75
            rd.resolution_percentage = 100
            rl.use_pass_combined = False
            rl.use_pass_z = False
            freestyle_settings.crease_angle = 2.617994
            
            # If File already exists then first remove it or this will cause Blender to crash
            if os.path.exists(bpy.path.abspath(context.scene.render.filepath) + context.scene.render.file_extension):
                os.remove(bpy.path.abspath(context.scene.render.filepath) + context.scene.render.file_extension)            
            
            bpy.ops.render.render('INVOKE_DEFAULT', write_still=True)
            
            render_image = bpy.path.abspath(context.scene.render.filepath) + context.scene.render.file_extension
            
            # Wait for Image to render before drawing opengl 
            while not os.path.exists(render_image):
                time.sleep(0.1)
            
            img_result = render_opengl(None,context)
            img_result.save_render(render_image)
             
            if os.path.exists(render_image):
                images.append(render_image)

    bpy.ops.fd_scene.clear_2d_views()
    imgs_to_remove = []
        
    for img in bpy.data.images:
        if img.users == 0:
            imgs_to_remove.append(img)
        
    for im in imgs_to_remove:
        print(im.name)
        bpy.data.images.remove(im)
            
    return images
        
def get_custom_font():
    if "Calibri-Light" in bpy.data.fonts:
        return bpy.data.fonts["Calibri-Light"]
    else:
        return bpy.data.fonts.load(os.path.join(os.path.dirname(bpy.app.binary_path),"Fonts","calibril.ttf"))

def get_custom_font_bold():
    if "Calibri" in bpy.data.fonts:
        return bpy.data.fonts["Calibri"]
    else:
        return bpy.data.fonts.load(os.path.join(os.path.dirname(bpy.app.binary_path),"Fonts","calibri.ttf"))
           
