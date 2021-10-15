import json
import os


class PDF_Form_Content:
    """Interface with some functions to fill the form data"""

    def __init__(self, form_info):
        self.form_info = form_info

    def get_tag_from_varname(self, varname):
        try:
            tag = next(
                filter(lambda tag: tag["varname"] == varname, self.form_info))
        except StopIteration:
            print(f"varname: {varname} was not found ! ! !")
            tag = None
            # raise
            # tag = next(
            #    filter(lambda tag: tag["varname"] == "test", self.form_info))
        return tag

    def set_value(self, varname, value):
        tag = self.get_tag_from_varname(varname)
        if tag is not None:
            tag["value"] = value


def fill_form(form, props, material_dict, **kwargs):
    file = os.path.join(os.path.dirname(__file__),
                        "varnames.json")
    """The json file 'varnames.json' contains a list with the names
       of the variables from blender that will be put in the .pdf file"""
    with open(file) as f:
        varnames = json.load(f)
    for varname in varnames:
        tag = form.get_tag_from_varname(varname)
        if tag is not None:
            tag["value"] = getattr(props, tag["varname"])

    varnames_with_matkeys = [
        ("material", "Surface Pointer"),
        ("eb_color", "Edge Pointer"),
        ("glass", "Glass Pointer"),
        ("paint_stain", "Stain Pointer")
    ]
    for varname, matkey in varnames_with_matkeys:
        tag = form.get_tag_from_varname(varname)
        if tag is not None:
            tag["value"] = material_dict[matkey]

    # eb_type -> e
    form.set_value("eb_type", kwargs["edge_type_name"])
    # countertops -> ct,
    form.set_value("countertops", kwargs["ct"])
    # door_style -> door_style, door_quantity
    form.set_value(
        "door_style",
        f"{kwargs['door_style']} Qty: {kwargs['door_quantity']}"
    )
    # drawer_style -> drawer_style, drawer_quantity
    form.set_value(
        "drawer_style",
        f"{kwargs['drawer_style']} Qty: {kwargs['drawer_quantity']}"
    )
    # glaze_color -> glaze_color
    form.set_value("glaze_color", kwargs["glaze_color"])
    # glaze_style -> glaze_style
    form.set_value("glaze_style", kwargs["glaze_style"])
    # pulls -> pull_type, pull_quantity
    form.set_value(
        "pulls",
        f"{kwargs['pull_type']} Qty: {kwargs['pull_quantity']}"
    )
    # rods -> rod_type, rod_quantity, rod_length
    form.set_value(
        "rods",
        f"{kwargs['rod_type']} " +
        f"Qty: {kwargs['rod_quantity']} LF: {kwargs['rod_length']}"
    )
    # slides -> slide_type
    form.set_value("slides", kwargs["slide_type"])
    # hinges -> hinge_type

    return form.form_info
