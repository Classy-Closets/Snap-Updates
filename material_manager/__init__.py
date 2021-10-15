from snap.material_manager import (
    property_groups,
    closet_materials,
    closet_materials_ui,
    closet_materials_ops,
)


def register():
    property_groups.register()
    closet_materials.register()
    closet_materials_ui.register()
    closet_materials_ops.register()


def unregister():
    property_groups.unregister()
    closet_materials.unregister()
    closet_materials_ui.unregister()
    closet_materials_ops.unregister()
