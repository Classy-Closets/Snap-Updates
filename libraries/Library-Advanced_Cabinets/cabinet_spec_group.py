"""
Microvellum 
Carcass
Stores the construction logic for the different types of carcasses that are available
in the frameless and face frame library
"""

from mv import unit, fd_types

EXPOSED_CABINET_MATERIAL = ("Plastics","Melamine","White Melamine")
UNEXPOSED_CABINET_MATERIAL = ("Wood","Wood Core","PB")
SEMI_EXPOSED_CABINET_MATERIAL = ("Plastics","Melamine","White Melamine")
DOOR_BOX_MATERIAL = ("Plastics","Melamine","White Melamine")
DOOR_MATERIAL = ("Plastics","Melamine","White Melamine")
GLASS_MATERIAL = ("Glass","Glass","Glass")
METAL = ("Metals","Metals","Stainless Steel")
CHROME = ("Metals","Metals","Chrome")
BLACK_METAL = ("Metals","Metals","Black Anodized Metal")
DRAWER_BOX_MATERIAL = ("Plastics","Melamine","White Melamine")
COUNTER_TOP_MATERIAL = ("Stone","Marble","Basalt Slate")

class Material_Pointers():
    
    Appliance_Metal = fd_types.Material_Pointer(CHROME)
    
    Appliance_Glass = fd_types.Material_Pointer(BLACK_METAL)
    
    Exposed_Exterior_Surface = fd_types.Material_Pointer(EXPOSED_CABINET_MATERIAL)

    Exposed_Interior_Surface = fd_types.Material_Pointer(EXPOSED_CABINET_MATERIAL)

    Semi_Exposed_Surface = fd_types.Material_Pointer(SEMI_EXPOSED_CABINET_MATERIAL)
    
    Exposed_Exterior_Edge = fd_types.Material_Pointer(EXPOSED_CABINET_MATERIAL)

    Exposed_Interior_Edge = fd_types.Material_Pointer(EXPOSED_CABINET_MATERIAL)

    Semi_Exposed_Edge = fd_types.Material_Pointer(EXPOSED_CABINET_MATERIAL)

    Concealed_Surface = fd_types.Material_Pointer(UNEXPOSED_CABINET_MATERIAL)

    Concealed_Edge = fd_types.Material_Pointer(UNEXPOSED_CABINET_MATERIAL)

    Door_Surface = fd_types.Material_Pointer(DOOR_MATERIAL)
    
    Door_Edge = fd_types.Material_Pointer(DOOR_MATERIAL)

    Glass = fd_types.Material_Pointer(GLASS_MATERIAL)

    Cabinet_Pull_Finish = fd_types.Material_Pointer(METAL)
    
    Drawer_Box_Surface = fd_types.Material_Pointer(DRAWER_BOX_MATERIAL)

#     Countertop_Surface = fd_types.Material_Pointer(COUNTER_TOP_MATERIAL)

    Molding = fd_types.Material_Pointer(EXPOSED_CABINET_MATERIAL)
    
class Cutpart_Pointers():
    
    Cabinet_Unfinished_Side = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                                       core="Concealed_Surface",
                                                       top="Concealed_Surface",
                                                       bottom="Semi_Exposed_Surface")

    Cabinet_Finished_Side = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                                     core="Concealed_Surface",
                                                     top="Exposed_Exterior_Surface",
                                                     bottom="Semi_Exposed_Surface")
    
    Cabinet_Back = fd_types.Cutpart_Pointer(thickness=unit.inch(.25),
                                            core="Concealed_Surface",
                                            top="Concealed_Surface",
                                            bottom="Semi_Exposed_Surface")

    Cabinet_Thick_Back = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                                  core="Concealed_Surface",
                                                  top="Concealed_Surface",
                                                  bottom="Semi_Exposed_Surface")
    
    Cabinet_Bottom = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                              core="Concealed_Surface",
                                              top="Exposed_Exterior_Surface",
                                              bottom="Semi_Exposed_Surface")
    
    Cabinet_Top = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                           core="Concealed_Surface",
                                           top="Concealed_Surface",
                                           bottom="Semi_Exposed_Surface")
    
    Cabinet_Unfinished_Side_Open = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                                            core="Concealed_Surface",
                                                            top="Concealed_Surface",
                                                            bottom="Exposed_Interior_Surface")

    Cabinet_Finished_Side_Open = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                                          core="Concealed_Surface",
                                                          top="Exposed_Exterior_Surface",
                                                          bottom="Exposed_Interior_Surface")
    
    Cabinet_Back_Open = fd_types.Cutpart_Pointer(thickness=unit.inch(.25),
                                                 core="Concealed_Surface",
                                                 top="Concealed_Surface",
                                                 bottom="Exposed_Interior_Surface")

    Cabinet_Thick_Back_Open = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                                       core="Concealed_Surface",
                                                       top="Concealed_Surface",
                                                       bottom="Exposed_Interior_Surface")
    
    Cabinet_Bottom_Open = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                                   core="Concealed_Surface",
                                                   top="Concealed_Surface",
                                                   bottom="Exposed_Interior_Surface")
    
    Cabinet_Top_Open = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                                core="Concealed_Surface",
                                                top="Concealed_Surface",
                                                bottom="Exposed_Interior_Surface")    
    
    Cabinet_Shelf = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                             core="Concealed_Surface",
                                             top="Semi_Exposed_Surface",
                                             bottom="Semi_Exposed_Surface")
    
    Cabinet_Shelf_Open = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                                  core="Concealed_Surface",
                                                  top="Semi_Exposed_Surface",
                                                  bottom="Semi_Exposed_Surface")    
    
    Cabinet_Division = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                                core="Concealed_Surface",
                                                top="Semi_Exposed_Surface",
                                                bottom="Semi_Exposed_Surface")
    
    Cabinet_Division_Open = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                                     core="Concealed_Surface",
                                                     top="Semi_Exposed_Surface",
                                                     bottom="Semi_Exposed_Surface")
    
    Cabinet_Divider = fd_types.Cutpart_Pointer(thickness=unit.inch(.25),
                                               core="Concealed_Surface",
                                               top="Semi_Exposed_Surface",
                                               bottom="Semi_Exposed_Surface")
    
    Cabinet_Divider_Open = fd_types.Cutpart_Pointer(thickness=unit.inch(.25),
                                                    core="Concealed_Surface",
                                                    top="Semi_Exposed_Surface",
                                                    bottom="Semi_Exposed_Surface")    
    
    Cabinet_Nailer = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                              core="Concealed_Surface",
                                              top="Concealed_Surface",
                                              bottom="Concealed_Surface")
    
    Cabinet_Toe_Kick = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                                core="Concealed_Surface",
                                                top="Concealed_Surface",
                                                bottom="Concealed_Surface")
    
    Cabinet_Filler = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                              core="Concealed_Surface",
                                              top="Exposed_Exterior_Surface",
                                              bottom="Concealed_Surface")
    
    Cabinet_Finger_Pull_Rail = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                                        core="Concealed_Surface",
                                                        top="Concealed_Surface",
                                                        bottom="Exposed_Exterior_Surface")
    
    Cabinet_Valance = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                               core="Concealed_Surface",
                                               top="Exposed_Exterior_Surface",
                                               bottom="Concealed_Surface")
    
    Cabinet_Sink_Sub_Front = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                                      core="Concealed_Surface",
                                                      top="Exposed_Exterior_Surface",
                                                      bottom="Concealed_Surface")    
    
    Cabinet_Door = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                            core="Concealed_Surface",
                                            top="Door_Surface",
                                            bottom="Door_Surface")
    
    Cabinet_Drawer_Front = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                                    core="Concealed_Surface",
                                                    top="Door_Surface",
                                                    bottom="Door_Surface")    
    
    Drawer_Box_Parts = fd_types.Cutpart_Pointer(thickness=unit.inch(.5),
                                          core="Concealed_Surface",
                                          top="Drawer_Box_Surface",
                                          bottom="Drawer_Box_Surface")
    
    Drawer_Box_Bottom = fd_types.Cutpart_Pointer(thickness=unit.inch(.25),
                                           core="Concealed_Surface",
                                           top="Drawer_Box_Surface",
                                           bottom="Drawer_Box_Surface")    
    
    Cabinet_Blind_Panel = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                                   core="Concealed_Surface",
                                                   top="Semi_Exposed_Surface",
                                                   bottom="Exposed_Exterior_Surface")    
    
class Edgepart_Pointers():
    
    Cabinet_Body_Edges = fd_types.Edgepart_Pointer(thickness=unit.inch(.01),
                                                   material="Exposed_Exterior_Edge")

    Cabinet_Body_Edges_Open = fd_types.Edgepart_Pointer(thickness=unit.inch(.01),
                                                        material="Exposed_Exterior_Edge")
    
    Cabinet_Door_Edges = fd_types.Edgepart_Pointer(thickness=unit.inch(.01),
                                                   material="Door_Edge")    
    
    Cabinet_Interior_Edges = fd_types.Edgepart_Pointer(thickness=unit.inch(.01),
                                                       material="Semi_Exposed_Edge")

    Cabinet_Interior_Edges_Open = fd_types.Edgepart_Pointer(thickness=unit.inch(.01),
                                                            material="Exposed_Interior_Edge")    
    
    Drawer_Box_Edges = fd_types.Edgepart_Pointer(thickness=unit.inch(.01),
                                           material="Drawer_Box_Surface")    
    