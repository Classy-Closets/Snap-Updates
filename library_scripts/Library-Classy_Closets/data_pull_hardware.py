from os import path
from mv import fd_types
from . import mv_closet_defaults as props_closet
from . import common_parts

class Standard_Pull(fd_types.Assembly):
    
    type_assembly = "NONE"
    
    def draw(self):
        props = props_closet.get_scene_props().closet_options
        
        self.create_assembly()
        self.obj_bp.mv.export_as_subassembly = False
        
        obj_props = props_closet.get_object_props(self.obj_bp)
        obj_props.is_handle = True
        
        pull = self.add_object(path.join(common_parts.LIBRARY_DATA_DIR,
                                         props_closet.PULL_FOLDER_NAME,
                                         props.pull_category,
                                         props.pull_name+".blend"))

        self.add_tab(name='Main Options',tab_type='VISIBLE')   
        self.add_prompt(name="Hide",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Pull Length",prompt_type='DISTANCE',value=pull.obj.dimensions.x,tab_index=0)
        self.add_prompt(name="Pull X Location",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Pull Z Location",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Pull Rotation",prompt_type='ANGLE',value=0,tab_index=0)
        
        Width = self.get_var("dim_x","Width")
        Height = self.get_var("dim_z","Height")
        Depth = self.get_var("dim_y","Depth")
        Pull_X_Location = self.get_var("Pull X Location")
        Pull_Z_Location = self.get_var("Pull Z Location")
        Pull_Rotation = self.get_var("Pull Rotation")
        Hide = self.get_var("Hide")
        
        pull.set_name(props.pull_name)
        pull.x_loc('Width-Pull_Z_Location',[Width,Pull_Z_Location])
        pull.y_loc('Depth+IF(Depth<0,Pull_X_Location,-Pull_X_Location)',[Depth,Pull_X_Location,Pull_Z_Location])
        pull.z_loc('Height',[Height])
        pull.z_rot('Pull_Rotation',[Pull_Rotation])
        pull.x_rot(value = -90)
        pull.material("Pull_Finish")
        pull.hide('Hide',[Hide])
        pull.obj.mv.is_cabinet_pull = True
        
        self.update()