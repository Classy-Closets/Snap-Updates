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

# <pep8 compliant>

import bpy
from bpy.types import UIList
from snap import sn_unit


class SN_UL_combobox(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=item.name)


class SN_UL_prompts(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=item.name)
        if item.prompt_type == 'FLOAT':
            layout.label(text=str(item.float_value))
        if item.prompt_type == 'DISTANCE':
            layout.label(text=str(sn_unit.meter_to_active_unit(item.distance_value)))
        if item.prompt_type == 'ANGLE':
            layout.label(text=str(item.angle_value))
        if item.prompt_type == 'QUANTITY':
            layout.label(text=str(item.quantity_value))
        if item.prompt_type == 'PERCENTAGE':
            layout.label(text=str((item.percentage_value)))
        if item.prompt_type == 'CHECKBOX':
            layout.label(text=str(item.checkbox_value))
        if item.prompt_type == 'COMBOBOX':
            layout.label(text=str(item.combobox_index))
        if item.prompt_type == 'TEXT':
            layout.label(text=str(item.text_value))


class SN_UL_calculators(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=item.name)


classes = (
    SN_UL_combobox,
    SN_UL_prompts,
    SN_UL_calculators,
)

register, unregister = bpy.utils.register_classes_factory(classes)
