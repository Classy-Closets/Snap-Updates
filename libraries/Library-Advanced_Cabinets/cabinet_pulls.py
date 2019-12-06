import bpy
import os
from mv import utils, unit, fd_types
from . import cabinet_properties

class Standard_Pull(fd_types.Assembly):
    
    library_name = "Cabinet Doors"
    type_assembly = "INSERT"
    
    door_type = "" # Base, Tall, Upper, Sink, Suspended
    door_swing = "" # Left Swing, Right Swing, Double Door, Flip up

    pull_name = ""

    def draw(self):
        props = cabinet_properties.get_scene_props()
        self.create_assembly()

        self.pull_name = props.pull_name
        
        pull = self.add_object(os.path.join(os.path.dirname(__file__),
                                            cabinet_properties.PULL_FOLDER_NAME,
                                            props.pull_category,
                                            self.pull_name+".blend"))
        
        self.add_tab(name='Main Options',tab_type='VISIBLE')
        self.add_prompt(name="Pull Price",prompt_type='PRICE',value=0,tab_index=0)
        self.add_prompt(name="Hide",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Pull Length",prompt_type='DISTANCE',value=pull.obj.dimensions.x,tab_index=0)
        self.add_prompt(name="Pull X Location",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Pull Z Location",prompt_type='DISTANCE',value=0,tab_index=0)
        self.add_prompt(name="Pull Rotation",prompt_type='ANGLE',value=0,tab_index=0)
        self.add_prompt(name="Pull Quantity",prompt_type='QUANTITY',value=1,tab_index=0)
        
        Width = self.get_var("dim_x","Width")
        Height = self.get_var("dim_z","Height")
        Depth = self.get_var("dim_y","Depth")
        Pull_X_Location = self.get_var("Pull X Location")
        Pull_Z_Location = self.get_var("Pull Z Location")
        Hide = self.get_var("Hide")
        
        pull.set_name(self.pull_name)
        pull.obj.mv.is_cabinet_pull = True
        pull.obj.mv.comment = self.pull_name
        pull.x_loc('Width-Pull_Z_Location',[Width,Pull_Z_Location])
        pull.y_loc('Depth+IF(Depth<0,Pull_X_Location,-Pull_X_Location)',[Depth,Pull_X_Location,Pull_Z_Location])
        pull.z_loc('Height',[Height])
        pull.x_rot(value = -90)
        if self.door_swing == 'Left Swing':
            pull.z_rot(value = 180)
        pull.material("Cabinet_Pull_Finish")
        pull.hide('Hide',[Hide])
        
        self.update()