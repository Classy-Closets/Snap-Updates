from . import closet_props, closet_dimensions
from .ops import drop_closet
from .ops import closet_ops
from .ui import closet_prompts_ui
from .ui import closet_panels
from . import closet_machining
# from . import closet_pricing
from . import spec_group_closet
from . import project_pricing


modules = (
    closet_props,
    drop_closet,
    closet_ops,
    closet_prompts_ui,
    closet_panels,
    closet_dimensions,
    spec_group_closet,
    project_pricing
)


def register():

    for mod in modules:
        mod.register()


def unregister():

    for mod in reversed(modules):
        mod.unregister()


# #DATA SCRIPTS
# from . import data_closet_carcass
# from . import data_closet_carcass_corner
# from . import data_closet_carcass_hutch
# from . import data_single_parts
# from . import data_closet_doors
# from . import data_drawers
# from . import data_ironing_boards
# from . import data_deco_fillers
# from . import data_hampers
# from . import data_closet_splitters
# from . import data_applied_panel
# from . import data_fixed_shelf_and_rod

# PRODUCT LIBRARIES
from . import closet_library

# #CLOSET DEFAULTS
# from . import mv_closet_defaults

# #CLOSET DIMENSIONS
# from . import mv_closet_dimensions

# #MACHINING MODULE
# from . import mv_closet_machining

# #PRICING MODULE
# from . import closet_pricing

# #CLOSET PROPERTIES
# from . import mv_closet_properties

# #Classy Closets
# from . import classy_closets_materials

