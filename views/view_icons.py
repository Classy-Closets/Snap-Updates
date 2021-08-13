"""
Utilities for drawing Plan View icons using Blender curves
"""
import bpy
import math
import mathutils
from snap import sn_types
from snap import sn_unit as unit


def draw_curve(name, points, curve_type, closed=False, fill=False):
    # Create curve
    curve = bpy.data.curves.new(name, 'CURVE')
    curve.dimensions = '2D'
    curve.extrude = 0.001
    if fill:
        curve.fill_mode = 'BOTH'
    else:
        curve.fill_mode = 'NONE'
    # Create spline for curve
    spline = curve.splines.new(type=curve_type)
    spline.points.add(len(points)-1)
    if curve_type == 'NURBS':
        spline.use_bezier_u = True
        spline.resolution_u = 8
    if closed:
        spline.use_cyclic_u = True
    for i, p in enumerate(points):
        spline.points[i].co = list(p) + [1]

    # Create object
    obj = bpy.data.objects.new(name, curve)
    return obj


def move_curve(curve, vector):
    loc_vec = mathutils.Vector(vector)
    loc_mtx = mathutils.Matrix.Translation(loc_vec)
    curve.data.transform(loc_mtx)


def flip_curve(curve, axis):
    scale_vec = [a == axis for a in ('X', 'Y', 'Z')]
    scale_mtx = mathutils.Matrix.Scale(-1, 4, scale_vec)
    curve.data.transform(scale_mtx)


def draw_rectangle(name, width, height, off_x, off_y, fill=False):
    rect_points = [(off_x, off_y, 0),
                   (off_x, height + off_y, 0),
                   (width + off_x, height + off_y, 0),
                   (width + off_x, off_y, 0)]

    rect_obj = draw_curve(name, rect_points, 'POLY', True, fill)

    return rect_obj


def draw_door_swing_icon(width, depth):
    door_n = 'ICON.CURVE.Door'
    swing_n = 'ICON.CURVE.Swing'
    door_crv = draw_rectangle(door_n, depth, width, 0, 0, True)
    swing_crv_pts = [(depth, width, 0),
                     (width * 0.9, width * 0.9, 0),
                     (width, 0, 0)]

    swing_crv = draw_curve(swing_n, swing_crv_pts, 'NURBS')
    return [door_crv, swing_crv]


def pv_swing_door_icons(context, entry_door, wall):
    depth = unit.inch(2)
    wall_assy = sn_types.Assembly(wall)
    entry_assy = sn_types.Assembly(entry_door)
    entry_w = entry_assy.obj_x.location.x
    wall_d = wall_assy.obj_y.location.y
    pmt_rev = entry_assy.get_prompt('Reverse Swing')
    pmt_side = entry_assy.get_prompt('Door Swing')

    # Create the empty that will contain the icon shapes
    icon_obj_n = 'ICON.{}'.format(entry_door.snap.class_name)
    icon_obj = bpy.data.objects.new(icon_obj_n, None)
    icon_obj.empty_display_size = unit.inch(1)
    icon_obj.empty_display_type = 'SPHERE'
    icon_obj.snap.type = 'VISDIM_A'
    icon_obj.parent = entry_door
    context.scene.collection.objects.link(icon_obj)
    sgl_entry = pmt_rev and pmt_side
    dbl_entry = pmt_rev and not pmt_side
    icon_crvs = []

    if dbl_entry:
        swing_rev = pmt_rev.get_value()
        icon_crvs = draw_door_swing_icon(entry_w * 0.5, depth)
        crvs_mirror = draw_door_swing_icon(entry_w * 0.5, depth)
        for c in crvs_mirror:
            flip_curve(c, 'X')
            move_curve(c, (entry_w, 0, 0))
            icon_crvs.append(c)
        if swing_rev:
            icon_obj.rotation_euler.x = math.radians(180)
        else:
            icon_obj.location.y = wall_d

    elif sgl_entry:
        swing_rev = pmt_rev.get_value()
        swing_side = pmt_side.get_value()
        icon_crvs = draw_door_swing_icon(entry_w, depth)
        if swing_side == 1 and swing_rev:
            icon_obj.location.x = entry_w
            icon_obj.rotation_euler.z = math.radians(180)

        elif swing_side == 1 and not swing_rev:
            icon_obj.location.x = entry_w
            icon_obj.location.y = wall_d
            icon_obj.rotation_euler.y = math.radians(180)

        elif swing_side == 0 and swing_rev:
            icon_obj.rotation_euler.x = math.radians(180)

        elif swing_side == 0 and not swing_rev:
            icon_obj.location.y = wall_d

    for c in icon_crvs:
        c.parent = icon_obj
        context.scene.collection.objects.link(c)
