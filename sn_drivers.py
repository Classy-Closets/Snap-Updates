# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy

def IF(statement,true,false):
    """ Returns true if statement is true Returns false if statement is false:
        statement - conditional statement
        true - value to return if statement is True
        false - value to return if statement is False
    """
    if statement == True:
        return true
    else:
        return false

def OR(*vars):
    """ Returns True if ONE parameter is true
    """
    for var in vars:
        if var:
            return True
    return False

def AND(*vars):
    """ Returns True if ALL parameters are true
    """
    for var in vars:
        if not var:
            return False
    return True

def GET_SMALLEST_SIZE(size,*vars):
    """ Returns the smallest value base on the size and values that are passed in
        Acts like a lookuptable and returns the smallest value that is also >= Par1
        Par1 - Size to lookup
        Par2 - Vars to use as the lookup (values must be ordered smallest to largest)
    """
    for i, var in enumerate(vars):
        if i == len(vars) - 1:
            return var #RETURN LAST ITEM IN LIST
        if size >= var and size <= vars[i+1]:
            return var #IF SIZE IS LARGER THEN VAR BUT SMALLER THAN NEXT RETURN VAR
        if size <= var:
            return var #IF SIZE IF SMALLER THAN CURRENT VALUE RETURN VAR
        
    return vars[-1] #RETURN LAST ITEM IN LIST
        
def EQ1(opening_quantity,start_point,end_point):
    """ Returns equal spacing based on the quantity and start and end point:
        Par1 - opening_quantity - Number of spliters in opening
        Par2 - start_point - Start point to calculate opening size (always smaller number)
        Par3 - end_point - End point to calculate opening size (always larger number)
    """
    opening_size = end_point-start_point
    if opening_quantity == 0:
        return 0
    else:
        mid_point = opening_size/(opening_quantity + 1)
    return mid_point

def INCH(value):
    """ Converts value to meters: expecing value in inches
    """
    return value * .0254

def MILLIMETER(value):
    """ Converts value to meters: expecting value in millimeter
    """
    return value * .001

def LIMIT(val,val_min,val_max):
    """ Returns par1 if value is between min and max else
        the minimum or maximum value value will be returned
    """
    if val>val_max:
        return val_max
    elif val<val_min:
        return val_min
    else:
        return val
    
def PERCENTAGE(value,min,max):
    """ Returns Percentage amount based on the min and max values
    """
    return (value - min)/(max - min)
    
def THICKNESS(sgi,pointer_name):
    spec_group = bpy.context.scene.snap.spec_groups[int(sgi)]
    if pointer_name in spec_group.cutparts:
        return spec_group.cutparts[pointer_name].thickness
    else:
        print("DRIVER ERROR: " + pointer_name + " not found in cut part pointers.")
        return 0

def EDGE_THICKNESS(sgi,pointer_name):
    spec_group = bpy.context.scene.snap.spec_groups[int(sgi)]
    if pointer_name in spec_group.edgeparts:
        return spec_group.edgeparts[pointer_name].thickness
    else:
        print("DRIVER ERROR: " + pointer_name + " not found in edge part pointers.")
        return 0
