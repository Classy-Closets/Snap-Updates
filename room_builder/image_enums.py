import os
from snap import sn_paths, sn_utils

PAINT_LIBRARY_NAME = "Paint"
PAINT_CATEGORY_NAME = "Textured Wall Paint"
CARPET_CATEGORY_NAME = "Flooring - Carpet"
TILE_CATEGORY_NAME = "Flooring - Tile"
HARDWOOD_CATEGORY_NAME = "Flooring - Wood Flooring"
# MOLDING_ASSEMBLY = os.path.join(os.path.dirname(__file__), "Moldings", "assemblies", "molding.blend")
# BASE_PRO_PATH = os.path.join(os.path.dirname(__file__), "Moldings", "profiles", "base")
# CROWN_PRO_PATH = os.path.join(os.path.dirname(__file__), "Moldings", "profiles", "crown")

preview_collections = {}
preview_collections["carpet"] = sn_utils.create_image_preview_collection()
preview_collections["wood_floor"] = sn_utils.create_image_preview_collection()
preview_collections["tile"] = sn_utils.create_image_preview_collection()
preview_collections["paint"] = sn_utils.create_image_preview_collection()
preview_collections["base molding"] = sn_utils.create_image_preview_collection()
preview_collections["crown molding"] = sn_utils.create_image_preview_collection()


def enum_carpet(self, context):
    if context is None:
        return []
    icon_dir = os.path.join(sn_paths.MATERIAL_DIR, CARPET_CATEGORY_NAME)
    pcoll = preview_collections["carpet"]
    return sn_utils.get_image_enum_previews(icon_dir, pcoll)


def enum_wood_floor(self, context):
    if context is None:
        return []

    icon_dir = os.path.join(sn_paths.MATERIAL_DIR, HARDWOOD_CATEGORY_NAME)
    pcoll = preview_collections["wood_floor"]
    return sn_utils.get_image_enum_previews(icon_dir, pcoll)


def enum_tile_floor(self, context):
    if context is None:
        return []

    icon_dir = os.path.join(sn_paths.MATERIAL_DIR, TILE_CATEGORY_NAME)
    pcoll = preview_collections["tile"]
    return sn_utils.get_image_enum_previews(icon_dir, pcoll)


def enum_wall_material(self, context):
    if context is None:
        return []

    icon_dir = os.path.join(sn_paths.MATERIAL_DIR, PAINT_CATEGORY_NAME)
    pcoll = preview_collections["paint"]
    return sn_utils.get_image_enum_previews(icon_dir, pcoll)


def enum_base_molding(self, context):
    if context is None:
        return []
    icon_dir = os.path.join(os.path.dirname(__file__), "Moldings", "profiles", "Base")
    pcoll = preview_collections["base molding"]
    return sn_utils.get_image_enum_previews(icon_dir, pcoll)


def enum_crown_molding(self, context):
    if context is None:
        return []

    icon_dir = os.path.join(os.path.dirname(__file__), "Moldings", "profiles", "Crown")
    pcoll = preview_collections["crown molding"]
    return sn_utils.get_image_enum_previews(icon_dir, pcoll)
