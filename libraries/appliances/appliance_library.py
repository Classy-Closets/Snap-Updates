import os
from snap import sn_unit
from . import appliance_types
from .appliance_paths import (
    WALL_APPLIANCE_PATH,
    COOKTOP_APPLIANCE_PATH,
    SINK_APPLIANCE_PATH,
    FAUCET_APPLIANCE_PATH,
    LAUNDRY_APPLIANCE_PATH
)


# ---------PRODUCT: PARAMETRIC APPLIANCES


class PRODUCT_Refrigerator(appliance_types.Parametric_Wall_Appliance):

    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "Refrigerator"
        self.width = sn_unit.inch(36)
        self.height = sn_unit.inch(84)
        self.depth = sn_unit.inch(27)
        self.appliance_path = os.path.join(WALL_APPLIANCE_PATH, "Professional Refrigerator Generic.blend")
        super().__init__()


class PRODUCT_Range(appliance_types.Parametric_Wall_Appliance):

    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "Range"
        self.width = sn_unit.inch(30)
        self.height = sn_unit.inch(42)
        self.depth = sn_unit.inch(28)
        self.appliance_path = os.path.join(WALL_APPLIANCE_PATH, "Professional Gas Range Generic.blend")
        super().__init__()


class PRODUCT_Dishwasher(appliance_types.Parametric_Wall_Appliance):

    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "Dishwasher"
        self.width = sn_unit.inch(24)
        self.height = sn_unit.inch(34)
        self.depth = sn_unit.inch(23)
        self.appliance_path = os.path.join(WALL_APPLIANCE_PATH, "Professional Dishwasher Generic.blend")
        self.add_countertop = True
        super().__init__()


class PRODUCT_Range_Hood(appliance_types.Parametric_Wall_Appliance):

    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "Range Hood"
        self.width = sn_unit.inch(30)
        self.height = sn_unit.inch(14)
        self.depth = sn_unit.inch(12.5)
        self.appliance_path = os.path.join(WALL_APPLIANCE_PATH, "Wall Mounted Range Hood 01.blend")
        self.height_above_floor = sn_unit.inch(60)
        super().__init__()

# ---------PRODUCT: COOK TOPS


class PRODUCT_Wolf_CG152_Transitional_Gas_Cooktop(appliance_types.Countertop_Appliance):

    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(COOKTOP_APPLIANCE_PATH, "Wolf CG152 Transitional Gas Cooktop.blend")
        super().__init__()

# ---------PRODUCT: SINKS


class PRODUCT_Bathroom_Sink(appliance_types.Countertop_Appliance):

    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(SINK_APPLIANCE_PATH, "Bathroom Sink.blend")
        super().__init__()


class PRODUCT_Double_Basin_Sink(appliance_types.Countertop_Appliance):

    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(SINK_APPLIANCE_PATH, "Double Basin Sink.blend")
        super().__init__()


class PRODUCT_Single_Basin_Sink(appliance_types.Countertop_Appliance):

    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(SINK_APPLIANCE_PATH, "Single Basin Sink.blend")
        super().__init__()

# ---------PRODUCT: FAUCETS


class PRODUCT_Bathroom_Faucet(appliance_types.Object_Appliance):

    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(FAUCET_APPLIANCE_PATH, "Bathroom Faucet.blend")
        super().__init__()


class PRODUCT_Faucet(appliance_types.Object_Appliance):

    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(FAUCET_APPLIANCE_PATH, "Faucet.blend")
        super().__init__()


class PRODUCT_High_Arc_Faucet(appliance_types.Object_Appliance):

    def __init__(self):
        self.category_name = "Appliances"
        self.assembly_name = "High-Arc Faucet"
        self.appliance_path = os.path.join(FAUCET_APPLIANCE_PATH, "High-Arc Faucet.blend")
        super().__init__()

# ---------PRODUCT: LAUNDRY


class PRODUCT_Washer(appliance_types.Object_Appliance):

    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(LAUNDRY_APPLIANCE_PATH, "Washer.blend")
        super().__init__()


class PRODUCT_Dryer(appliance_types.Object_Appliance):

    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(LAUNDRY_APPLIANCE_PATH, "Dryer.blend")
        super().__init__()


class PRODUCT_Metal_Stool(appliance_types.Object_Appliance):

    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(LAUNDRY_APPLIANCE_PATH, "Metal Stool.blend")
        super().__init__()


class PRODUCT_Wall_Mirror(appliance_types.Parametric_Wall_Appliance):

    def __init__(self):
        self.category_name = "Appliances"
        self.width = sn_unit.inch(24)
        self.height = sn_unit.inch(.75)
        self.depth = sn_unit.inch(-12)
        self.appliance_path = os.path.join(LAUNDRY_APPLIANCE_PATH, "Wall Mirror.blend")
        self.height_above_floor = sn_unit.inch(36)
        super().__init__()


class PRODUCT_Vanity_Light_5(appliance_types.Static_Wall_Appliance):

    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(LAUNDRY_APPLIANCE_PATH, "Vanity Light 5.blend")
        self.height_above_floor = sn_unit.inch(78)
        super().__init__()


class PRODUCT_Vanity_Light_4(appliance_types.Static_Wall_Appliance):

    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(LAUNDRY_APPLIANCE_PATH, "Vanity Light 4.blend")
        self.height_above_floor = sn_unit.inch(78)
        super().__init__()


class PRODUCT_Vanity_Light_3(appliance_types.Static_Wall_Appliance):

    def __init__(self):
        self.category_name = "Appliances"
        self.appliance_path = os.path.join(LAUNDRY_APPLIANCE_PATH, "Vanity Light 3.blend")
        self.height_above_floor = sn_unit.inch(78)
        super().__init__()
