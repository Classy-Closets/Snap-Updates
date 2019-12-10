from mv import fd_types, unit

EXPOSED_MATERIAL = ("Cabinet Materials","Laminate Solid","White Melamine")
CHROME_MATERIAL = ("Metals","Metals","Chrome")
GLASS_MATERIAL = ("Glass","Glass","Glass")
MIRROR_MATERIAL = ("Cabinet Materials","Classy Closets","Mirror")
LUCITE_MATERIAL = ("Glass","Lucite","Lucite")
COUNTER_TOP_MATERIAL = ("Cabinet Materials","Classy Closets","TEST")
CORE = ("Cabinet Materials","Wood Core","PB")
MODERNO_DOOR = ("Moderno Door")


class Material_Pointers():
    
    Closet_Part_Surfaces = fd_types.Material_Pointer(EXPOSED_MATERIAL)

    Closet_Part_Edges = fd_types.Material_Pointer(EXPOSED_MATERIAL)
    
    Closet_Part_Edges_Secondary = fd_types.Material_Pointer(EXPOSED_MATERIAL)    

    Pull_Finish = fd_types.Material_Pointer(CHROME_MATERIAL)

    Rod_Finish = fd_types.Material_Pointer(CHROME_MATERIAL)

    Door_Surface = fd_types.Material_Pointer(EXPOSED_MATERIAL)

    Wood_Door_Surface = fd_types.Material_Pointer(EXPOSED_MATERIAL)

    Moderno_Door = fd_types.Material_Pointer(MODERNO_DOOR)

    Door_Edge = fd_types.Material_Pointer(EXPOSED_MATERIAL)

    Countertop_Surface = fd_types.Material_Pointer(COUNTER_TOP_MATERIAL)

    Drawer_Box_Surface = fd_types.Material_Pointer(EXPOSED_MATERIAL)

    Drawer_Box_Edge = fd_types.Material_Pointer(EXPOSED_MATERIAL)
    
    Wire_Basket = fd_types.Material_Pointer(CHROME_MATERIAL)
    
    Glass = fd_types.Material_Pointer(GLASS_MATERIAL)
    
    Mirror = fd_types.Material_Pointer(MIRROR_MATERIAL)
    
    Chrome = fd_types.Material_Pointer(CHROME_MATERIAL)
    
    Molding = fd_types.Material_Pointer(EXPOSED_MATERIAL)
    
    Lucite = fd_types.Material_Pointer(LUCITE_MATERIAL)
    
    Core = fd_types.Material_Pointer(CORE)
    
class Cutpart_Pointers():
    
    Panel = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                   core="Closet_Part_Surfaces",
                                   top="Closet_Part_Surfaces",
                                   bottom="Closet_Part_Surfaces")

    Shelf = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                   core="Closet_Part_Surfaces",
                                   top="Closet_Part_Surfaces",
                                   bottom="Closet_Part_Surfaces")
    
    Cleat = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                   core="Closet_Part_Surfaces",
                                   top="Closet_Part_Surfaces",
                                   bottom="Closet_Part_Surfaces")    
    
    Toe_Kick = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                      core="Closet_Part_Surfaces",
                                      top="Closet_Part_Surfaces",
                                      bottom="Closet_Part_Surfaces")

    Back = fd_types.Cutpart_Pointer(thickness=unit.inch(.25),
                                  core="Closet_Part_Surfaces",
                                  top="Closet_Part_Surfaces",
                                  bottom="Closet_Part_Surfaces")

    Drawer_Sides = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                            core="Drawer_Box_Surface",
                                            top="Drawer_Box_Surface",
                                            bottom="Drawer_Box_Surface")

    Drawer_Part = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                         core="Drawer_Box_Surface",
                                         top="Drawer_Box_Surface",
                                         bottom="Drawer_Box_Surface")

    Shoe_Cubby = fd_types.Cutpart_Pointer(thickness=unit.inch(.25),
                                        core="Closet_Part_Surfaces",
                                        top="Closet_Part_Surfaces",
                                        bottom="Closet_Part_Surfaces")

    Drawer_Back = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                        core="Drawer_Box_Surface",
                                        top="Drawer_Box_Surface",
                                        bottom="Drawer_Box_Surface")

    Drawer_Bottom = fd_types.Cutpart_Pointer(thickness=unit.inch(.25),
                                        core="Drawer_Box_Surface",
                                        top="Drawer_Box_Surface",
                                        bottom="Drawer_Box_Surface")

    Thick_Drawer_Bottom = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                        core="Drawer_Box_Surface",
                                        top="Drawer_Box_Surface",
                                        bottom="Drawer_Box_Surface")

    Slab_Door = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                       core="Closet_Part_Surfaces",
                                       top="Door_Surface",
                                       bottom="Door_Surface")
    
    Lucite_Front = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                          core="Lucite",
                                          top="Lucite",
                                          bottom="Lucite")
    
    Slab_Drawer_Front = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                               core="Closet_Part_Surfaces",
                                               top="Door_Surface",
                                               bottom="Door_Surface")

    Hanging_Rail = fd_types.Cutpart_Pointer(thickness=unit.inch(.75),
                                               core="Chrome",
                                               top="Chrome",
                                               bottom="Chrome")

class Edgepart_Pointers():
    
    Edge = fd_types.Edgepart_Pointer(thickness=unit.inch(.01),
                                     material="Closet_Part_Edges")
    
    Edge_2 = fd_types.Edgepart_Pointer(thickness=unit.inch(.01),
                                     material="Closet_Part_Edges_Secondary")    
    
    Door_Edges = fd_types.Edgepart_Pointer(thickness=unit.inch(.01),
                                           material="Door_Edge")
    
    Lucite_Edges = fd_types.Edgepart_Pointer(thickness=unit.inch(.01),
                                             material="Lucite")    
    
    Drawer_Box_Edge = fd_types.Edgepart_Pointer(thickness=unit.inch(.01),
                                                material="Drawer_Box_Surface")