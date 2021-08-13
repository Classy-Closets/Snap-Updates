from os import path
import math
import bpy

from snap import sn_types
from .. import closet_props
from .. import closet_paths
from ..common import common_parts


class Standard_Pull(sn_types.Assembly):

    type_assembly = "NONE"

    def draw(self):
        props = bpy.context.scene.sn_closets.closet_options

        self.create_assembly()
        self.obj_bp.snap.export_as_subassembly = False

        obj_props = self.obj_bp.sn_closets
        obj_props.is_handle = True

        pull = self.add_object_from_file(
            path.join(
                closet_paths.get_root_dir(),
                closet_props.PULL_FOLDER_NAME,
                props.pull_category,
                props.pull_name + ".blend"))

        self.add_prompt("Hide", 'CHECKBOX', False)
        self.add_prompt("Pull Length", 'DISTANCE', pull.dimensions.x)
        self.add_prompt("Pull X Location", 'DISTANCE', 0)
        self.add_prompt("Pull Z Location", 'DISTANCE', 0, prompt_obj=self.add_prompt_obj("Pull_Location"))
        self.add_prompt("Pull Rotation", 'ANGLE', 0)

        Width = self.obj_x.snap.get_var("location.x", "Width")
        Height = self.obj_z.snap.get_var("location.z", "Height")
        Depth = self.obj_y.snap.get_var("location.y", "Depth")
        Pull_X_Location = self.get_prompt("Pull X Location").get_var("Pull_X_Location")
        Pull_Z_Location = self.get_prompt("Pull Z Location").get_var("Pull_Z_Location")
        Pull_Rotation = self.get_prompt("Pull Rotation").get_var("Pull_Rotation")
        Hide = self.get_prompt("Hide").get_var("Hide")

        self.set_name(props.pull_name)
        pull.name = props.pull_name
        pull.snap.name_object = props.pull_name
        pull.snap.type_mesh = "HARDWARE"
        pull.snap.loc_x('Width-Pull_Z_Location', [Width, Pull_Z_Location])
        pull.snap.loc_y('Depth+IF(Depth<0,Pull_X_Location,-Pull_X_Location)', [Depth, Pull_X_Location, Pull_Z_Location])
        pull.snap.loc_z('Height', [Height])
        pull.snap.rot_z('Pull_Rotation', [Pull_Rotation])
        pull.snap.rot_x(value=math.radians(-90))
        pull.snap.hide('Hide', [Hide])
        pull.snap.is_cabinet_pull = True
        spec_group = bpy.context.scene.snap.spec_groups[pull.snap.spec_group_index]
        for mat_pointer in spec_group.materials:
            if mat_pointer.name == "Pull_Finish":
                mat_pointer.category_name = "Finished Metals"
                mat_pointer.item_name = props.pull_category
        self.set_material_pointers('Pull_Finish')
        # self.update()
