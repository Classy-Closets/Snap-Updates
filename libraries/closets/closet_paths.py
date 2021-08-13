import os


def get_root_dir():
    return os.path.join(os.path.dirname(__file__))


def get_library_path():
    return os.path.join(get_root_dir(), 'products')


def get_asset_folder_path():
    return os.path.join(get_root_dir(), 'assets')


def get_closet_assemblies_path():
    return os.path.join(get_asset_folder_path(), 'Closet Assemblies')


def get_closet_objects_path():
    return os.path.join(get_asset_folder_path(), 'Objects')
