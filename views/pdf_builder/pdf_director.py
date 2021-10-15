import os
import json
from snap.views.pdf_builder.pdf_old_template import Old_Template_Builder
from snap.views.pdf_builder.pdf_new_template import New_Template_Builder
from snap.views.pdf_builder.fill_pdf import PDF_Form_Content, fill_form


class PDF_Director:
    """Call the steps for building the .pdf files with different styles.

    Attributes:
        form_info (dict): Dictionary with the data for the form.
        form_paths (dict): Dictionary with the paths of the templates.
        path (str): Path where the .pdf file will be save,
                    include directory, name and '.pdf'.
        print_paper_size (str): Name of the paper format,
                    example: 'LEGAL'
        images (list): list of str with the paths of the images,
                       include directory, name and extension.
        logo (str): The path of the logo with directory,
                        name and extension.
        builders(dict): Dictionary with the classes of possibles builders
    """

    def __init__(self, path: str,
                 print_paper_size: str, images: list, logo: str) -> None:
        new_form_path = os.path.join(os.path.dirname(__file__),
                                     "template_db_new.json")
        old_form_path = os.path.join(os.path.dirname(__file__),
                                     "template_db.json")
        '''Structure of the json files in 'new_form_path' and 'old_form_path' is:

        A list of dictionaries each represent a field in the form,
        the keys are:
            "label": the name of the field
            "value": a string to put in front of label
            "position": a dictionary with the coordinates of the label in the
                        .pdf file, depending on the paper size (key)
            "varname": the name of the variable in blender
        '''
        self.form_paths = {"OLD": old_form_path,
                           "NEW": new_form_path}
        self.path = path
        self.print_paper_size = print_paper_size
        self.images = images
        self.logo = logo
        self.builders = {"OLD": Old_Template_Builder,
                         "NEW": New_Template_Builder}

    def make(self, template: str, props: dict,
             material_dict: dict, **ctx) -> None:
        """Make the .pdf file with the style indicated in 'template'."""
        builder = self.builders[template](self.path, self.print_paper_size)
        form_path = self.form_paths[template]
        self.form_info = open_json_file(form_path)
        form = PDF_Form_Content(self.form_info)
        self.form_info = fill_form(form, props, material_dict, **ctx)
        for image in self.images:
            if not image:
                continue
            builder.draw_main_image(image)
            builder.draw_logo(self.logo)
            builder.draw_info(self.form_info)
            builder.draw_margin()
            builder.draw_block_info()
            builder.show_page()
        builder.c.save()


def open_json_file(file: str) -> dict:
    """Open a json file and return a dictionary."""
    with open(file) as f:
        json_file = json.load(f)
    return json_file
