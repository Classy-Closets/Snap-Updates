import bpy
import os
import random
import string
import sys

from bpy.props import StringProperty
try:
    import PIL
except ModuleNotFoundError:
    python_lib_path = os.path.join(os.path.dirname(__file__), "..", "python_lib")
    sys.path.append(python_lib_path)
from PIL import Image as PImage
from PIL import ImageChops

from snap.views.pdf_builder.pdf_director import PDF_Director
from snap.project_manager import pm_utils


class OPERATOR_create_pdf(bpy.types.Operator):
    bl_idname = "2dviews.report_2d_drawings"
    bl_label = "Export Selected 2D Views"
    bl_description = "This creates a 2D drawing pdf of all of the images"

    filepath: StringProperty(subtype="FILE_PATH")
    filename: StringProperty()
    directory: StringProperty()
    files = None
    project_name = "project"
    room_name = "room"

    def invoke(self, context, event):
        bfile = bpy.path.abspath("//")
        pm_props = context.window_manager.sn_project
        project_name = pm_props.current_file_project
        room_name = pm_props.current_file_room
        self.directory = bfile
        clean_room_name = pm_utils.clean_name(room_name)
        self.filename = f'2D Views - {project_name} - {clean_room_name}.pdf'
        context.window_manager.fileselect_add(self)

        return {'RUNNING_MODAL'}

    def _check_file_access(self):
        """Check if the path of the selected .pdf file can be accessed"""
        if os.path.exists(self.filepath):
            try:
                f = open(self.filepath, 'wb')
                f.close()
            except IOError:
                directory, filename = os.path.split(self.filepath)
                bpy.ops.snap.message_box(
                    'INVOKE_DEFAULT',
                    message="\"{}\" is currently open.\nUnable to overwrite file.".format(filename))
                return False
        return True

    @staticmethod
    def _save_images(images, image_dic, tempdir):
        """Save the views as .jpg images and return a list with its paths.

        Args:
            images (list): List of images from context.
            image_dic (dict): Dictionary with images from bpy data.
            tempdir (str): Path where the images will be saved.

        Returns:
            pdf_images (list): A list with the paths of the images that will be
                               included in the .pdf file.
        """

        pdf_images = []
        for img in images:
            image = image_dic[img.image_name]
            image.filepath_raw = os.path.join(
                tempdir, image.name + ".jpg")
            image.file_format = 'JPEG'
            image.save()
            # image.save_render(os.path.join(
            #   tempdir, image.name + ".jpg"))
            pdf_images.append(os.path.join(
                tempdir, image.name + ".jpg"))
        return pdf_images

    @staticmethod
    def _get_file_path(keys_list, sn_project,
                       bpy_filepath, bpy_datafiles, tempdir):
        if 'sn_projects' in keys_list:
            proj_props = sn_project
        else:
            proj_props = None

        if bpy_filepath == "":
            if proj_props:
                proj_name = proj_props.projects[proj_props.project_index].name
                file_path = os.path.join(bpy_datafiles, "projects", proj_name)
            else:
                file_path = tempdir
                room_name = "Unsaved"
        else:
            project_path = os.path.dirname(bpy_filepath)
            room_name, ext = os.path.splitext(
                os.path.basename(bpy_filepath))
            if proj_props and len(proj_props.projects) > 0:
                proj_name = proj_props.projects[proj_props.project_index].name
                file_path = os.path.join(bpy_datafiles, "projects", proj_name)
            else:
                file_path = os.path.join(project_path, room_name)
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
        return file_path

    @staticmethod
    def _create_str_materials_dict():
        """Create an auxiliary dictionary with the functions (as str)
           that must be executed to obtain the values of the materials,
           used to find missing values.

        Returns:
            prop_dict (dict): Dictionary with materials (key)
                              and the functions (value) to get its values.
        """
        prop_dict = {}
        prop_dict["Surface Pointer"] =\
            "cl_materials.materials.get_mat_color().name"
        prop_dict["Edge Pointer"] = "cl_materials.edges.get_edge_color().name"
        prop_dict["CT Pointer"] = "cl_materials.countertops.get_color_name()"
        prop_dict["Stain Pointer"] =\
            "cl_materials.stain_colors[cl_materials.stain_color_index].name"
        prop_dict["Glass Pointer"] =\
            "cl_materials.glass_colors[cl_materials.glass_color_index].name"  # noqa: E501
        return prop_dict

    @staticmethod
    def _materials(cl_materials):
        """Create a dictionary with the data of materials to put in the pdf file.

        Args:
            cl_materials (obj): Closet materials, from bpy context.

        Returns:
            material_dict (dict): Dictionary with materials and its values.
        """
        material_dict = {}
        prop_dict = OPERATOR_create_pdf._create_str_materials_dict()
        keys = prop_dict.keys()
        for key in keys:
            try:
                material_dict[key] = eval(prop_dict[key])
            except Exception as e:
                print(e)

        return material_dict

    @staticmethod
    def _has_ct(ct_materials, material_dict, data_objects):
        ct_type = ct_materials.edges.get_edge_type().name
        for obj in data_objects:
            props = obj.sn_closets
            if props.is_counter_top_insert_bp:
                return (ct_type + " " + material_dict['CT Pointer'])
        return ("None")

    # REFACTOR closet_materials function replaces this
    # def edge_type_name(self,context):
    #     name = "Unknown"
    #     props = context.scene.closet_materials
    #     edge_type_code = int(props.edge_type_menu)

    #     for edge_type in props.edge_types:
    #         if edge_type.type_code == edge_type_code:
    #             name = edge_type.name

    #     return name

    # REFACTOR closet_materials replaces closet_materials
    def edge_type(self, context):
        props = context.scene.closet_materials
        return props.edges.get_edge_type().description
        # Until I confirm this work, I am leaving the unexecuted code below in
        if props.edge_profile == 'SQUARE':
            return context.scene.closet_materials.square_edge
        else:
            return context.scene.closet_materials.round_edge

    @staticmethod
    def _slide_type(sn_closets):
        if sn_closets.closet_options.box_type == 'MEL':
            return sn_closets.closet_options.mel_slide_name
        else:
            return sn_closets.closet_options.dt_slide_name

    @staticmethod
    def _door_style(data_objects):
        for obj in data_objects:
            if "Door.Cutpart" in obj.name and not obj.hide_viewport:
                return "Melamine"
            if " Door" in obj.name and not obj.hide_viewport:
                return obj.snap.comment

    @staticmethod
    def _drawer_style(data_objects):
        for obj in data_objects:
            if "Drawer Front.Cutpart" in obj.name and not obj.hide_viewport:
                return "Melamine"
            if " Drawer" in obj.snap.comment and not obj.hide_viewport:
                return obj.snap.comment

# QUANTITIES
    # PULLS
    @staticmethod
    def _get_pull_qty(data_objects):
        number_of_pulls = 0
        for obj in data_objects:
            if obj.snap.is_cabinet_pull and not obj.hide_viewport:
                number_of_pulls += 1
        return number_of_pulls

    @staticmethod
    def _get_pull_type(pull_quantity, sn_closets):
        if pull_quantity == 0:
            pull_type = "None"
        else:
            pull_type = sn_closets.closet_options.pull_name
        return pull_type

    # RODS
    @staticmethod
    def _get_rod_qty(data_objects):
        number_of_rods = 0
        for obj in data_objects:
            if "Hang Rod" in obj.snap.name_object and not obj.hide_viewport:
                number_of_rods += 1
        return number_of_rods

    @staticmethod
    def _get_rod_type(rod_quantity, sn_closets):
        if rod_quantity == 0:
            rod_type = "None"
        else:
            rod_type = sn_closets.closet_options.rods_name
        return rod_type

    # ROD_LENGTH
    @staticmethod
    def _get_rod_length(data_objects):
        length_of_rods = 0
        for obj in data_objects:
            if "Hang Rod" in obj.snap.name_object and not obj.hide_viewport:
                # return obj.dimensions.x
                length_of_rods += obj.dimensions.x
        return length_of_rods

    # DRAWERS
    @staticmethod
    def _get_drawer_qty(data_objects):
        number_of_drawers = 0
        for obj in data_objects:
            if "Drawer Bottom" in obj.name and not obj.hide_viewport:
                number_of_drawers += 1
        return number_of_drawers

    @staticmethod
    def _get_glaze_style(glaze_color, clt_materials):
        if glaze_color == "None":
            glaze_style = "None"
        else:
            glaze_style = clt_materials.get_glaze_style().description
        return glaze_style

    # DOORS
    @staticmethod
    def _get_door_qty(data_objects):
        number_of_doors = 0
        for obj in data_objects:
            if " Door" in obj.name and not obj.hide_viewport:
                number_of_doors += 1
        return number_of_doors

    def random_string(self, length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.sample(letters, length))
        return result_str

    def trim(self, image):
        bg = PImage.new(image.mode, image.size, image.getpixel((0, 0)))
        diff = ImageChops.difference(image, bg)
        diff = ImageChops.add(diff, diff, 2.0, 0)
        bbox = diff.getbbox()
        if bbox:
            return image.crop(bbox)

    """
    Parameters:
        images_list - a list of image paths (string)
        output - output image file (string)
        border - an optional tuple with the desired border in pixels, in the following order: (left, top, right, bottom)
    """

    def join_images_horizontal(self, images_list, output, border=(25, 0, 50, 0), keep_width=False):
        white_bg = (255, 255, 255)
        cropped_ims = []
        original_ims = []
        for i in images_list:
            im = PImage.open(i)
            original_ims.append(im)
            cropped_ims.append(self.trim(im))
        for i in cropped_ims:
            if not i:
                cropped_ims.remove(i)
        if len(cropped_ims) > 0:
            widths, heights = zip(*(i.size for i in cropped_ims))
            orig_widths, orig_heights = zip(*(i.size for i in original_ims))
            if keep_width:
                total_width = sum(orig_widths) + border[0] + border[2]
                x_offset = border[0] + int((sum(orig_widths) - sum(widths)) / 2)
            else:
                total_width = sum(widths) + border[0] + border[2]
                x_offset = border[0]
            max_height = max(heights) + border[1] + border[3]
            new_im = PImage.new('RGB', (total_width, max_height), white_bg)
            for im in cropped_ims:
                y_offset = int((max(heights) - im.size[1]) / 2) + border[1]
                new_im.paste(im, (x_offset, y_offset))
                x_offset += im.size[0] + 10
            # Always save as PNG, JPG makes blender crash silently
            img_file = os.path.join(bpy.app.tempdir + output + ".png")
            new_im.save(img_file)
            return img_file
        else:
            return None

    def join_images_vertical(self, images_files_list, output, vertical_padding=0):
        white_bg = (255, 255, 255)
        images_list = []
        for i in images_files_list:
            im = PImage.open(i)
            images_list.append(im)
        widths, heights = zip(*(i.size for i in images_list))
        max_width = max(widths)
        total_height = sum(heights) + (vertical_padding * 2)
        new_im = PImage.new('RGB', (max_width, total_height), white_bg)
        y_offset = 0
        for im in images_list:
            new_im.paste(im, (0, y_offset + vertical_padding))
            y_offset += im.size[1]
        # Always save as PNG, JPG makes blender crash silently
        img_file = os.path.join(bpy.app.tempdir + output + ".png")
        new_im.save(img_file)
        return img_file

    def get_image_size(self, image_file):
        image = PImage.open(image_file)
        width, height = image.size
        return (int(width), int(height))

    # Internal function
    # receives: a list of sn_images and a layout option
    # return: a page asemm to be appended to the PDF file
    # LAYOUTS:
    # full - One image per page - Full Page
    # two - Two images per page, side by side
    # three - Three images per page, side by side
    # 1up2down  - One image on upper half, two on the bottom half
    # 1up3down - One image on upper half, three on the bottom half
    def __prepare_image_page__(self, sn_images_list, page_paper_size, option):
        if option == "full":
            return self.join_images_horizontal([bpy.app.tempdir + sn_images_list[0].name + ".jpg"],
                                               self.random_string(6))
        if option == "two":
            sn_images_list = sn_images_list[:2]
            image_files = [(bpy.app.tempdir + image.name + ".jpg")
                           for image in sn_images_list]
            return self.join_images_horizontal(image_files, self.random_string(6))
        if option == "three":
            sn_images_list = sn_images_list[:3]
            image_files = [(bpy.app.tempdir + image.name + ".jpg")
                           for image in sn_images_list]
            return self.join_images_horizontal(image_files, self.random_string(6))
        if option == "1up2down":
            sn_images_list = sn_images_list[:3]
            lower_part = [(bpy.app.tempdir + image.name + ".jpg")
                          for image in sn_images_list[1:]]
            upper_part = [(bpy.app.tempdir + image.name + ".jpg")
                          for image in sn_images_list[:1]]
            lower_image = self.join_images_horizontal(
                lower_part, option + "lower")
            lower_w, lower_h = self.get_image_size(lower_image)
            upper_w, upper_h = self.get_image_size(
                bpy.app.tempdir + sn_images_list[0].name + ".jpg")
            border = (int((lower_w - upper_w) / 2), 10,
                      (int((lower_w - upper_w) / 2)), 10)
            upper_image = self.join_images_horizontal(
                upper_part, option + "upper", border, True)
            img = self.join_images_vertical([upper_image, lower_image], 
                                            self.random_string(6))
            return img
        if option == "1up3down":
            sn_images_list = sn_images_list[:4]
            lower_part = [(bpy.app.tempdir + image.name + ".jpg")
                          for image in sn_images_list[1:]]
            upper_part = [(bpy.app.tempdir + image.name + ".jpg")
                          for image in sn_images_list[:1]]
            lower_image = self.join_images_horizontal(
                lower_part, option + "lower")
            lower_w, lower_h = self.get_image_size(lower_image)
            upper_w, upper_h = self.get_image_size(
                bpy.app.tempdir + sn_images_list[0].name + ".jpg")
            border = (int((lower_w - upper_w) / 2), 10,
                      int((lower_w - upper_w) / 2), 10)
            upper_image = self.join_images_horizontal(
                upper_part, option + "upper", border, True)
            img = self.join_images_vertical([upper_image, lower_image], 
                                            self.random_string(6))
            return img

        return False

    """Resizes an image given it's filename.

    Args:
        img (str): image file path
        proportion (float): the desired proportion, 1 being 100%
    """
    def resize_image(self, img, proportion=0.7) -> str:
        img_w, img_h = self.get_image_size(img)
        res_width, res_height = int(img_w * proportion), int(img_h * proportion)
        to_res = PImage.open(img)
        resized = to_res.resize((res_width, res_height), PImage.ANTIALIAS)
        res_name = os.path.join(bpy.app.tempdir + self.random_string(8) + '.jpg')
        resized.save(res_name)
        return res_name

    # HINGES
#     def get_hinge_qty(self,context):
#         number_of_hinges = 0
#         for obj in bpy.data.objects:
#             #props = obj.sn_closets
#             if obj.snap.is_hinge and obj.hide_viewport == False:
#                 number_of_hinges += 1
#         return 

    def _get_SINGLE_pages(self, plan_view, elevations, props):
        pages = []
        chunk_length = 1
        first_page_qty = 1
        feeds = []
        if len(plan_view) > 0:
            feeds.append(plan_view[0])
        while len(elevations) > 0:
            feeds.append(elevations.pop(0))
        first_page = feeds[:first_page_qty]
        pages.append(self.__prepare_image_page__(
            first_page, props.paper_size, "full"))
        other_pages = feeds[first_page_qty:]
        feeds_chunks = [other_pages[x:x + chunk_length]
                        for x in range(0, len(other_pages), chunk_length)]
        for i in range(len(feeds_chunks)):
            pages.append(self.__prepare_image_page__(
                feeds_chunks[i], props.paper_size, "full"))
        return pages

    def _get_pages_2ELVS(self, plan_view, elevations, props):
        pages = []
        chunk_length = 2
        first_page_qty = 1
        feeds = []
        if len(plan_view) > 0:
            feeds.append(plan_view[0])
        while len(elevations) > 0:
            feeds.append(elevations.pop(0))
        first_page = feeds[:first_page_qty]
        pages.append(self.__prepare_image_page__(
            first_page, props.paper_size, "full"))
        other_pages = feeds[first_page_qty:]
        feeds_chunks = [other_pages[x:x + chunk_length]
                        for x in range(0, len(other_pages), chunk_length)]
        for i in range(len(feeds_chunks)):
            pages.append(self.__prepare_image_page__(
                feeds_chunks[i], props.paper_size, "two"))
        return pages
    
    def _get_pages_1ACCORD(self, accordions, props):
        pages = []
        chunk_length = 1
        first_page_qty = 1
        feeds = []
        while len(accordions) > 0:
            feeds.append(accordions.pop(0))
        first_page = feeds[:first_page_qty]
        pages.append(self.__prepare_image_page__(
            first_page, props.paper_size, "full"))
        other_pages = feeds[first_page_qty:]
        feeds_chunks = [other_pages[x:x + chunk_length]
                        for x in range(0, len(other_pages), chunk_length)]
        for i in range(len(feeds_chunks)):
            pages.append(self.__prepare_image_page__(
                feeds_chunks[i], props.paper_size, "full"))
        return pages

    def _get_pages_plan_1ACCORD(self, plan_view, accordions, props):
        pages = []
        chunk_length = 1
        first_page_qty = 1
        feeds = []
        if len(plan_view) > 0:
            feeds.append(plan_view[0])
        while len(accordions) > 0:
            feeds.append(accordions.pop(0))
        first_page = feeds[:first_page_qty]
        pages.append(self.__prepare_image_page__(
            first_page, props.paper_size, "full"))
        other_pages = feeds[first_page_qty:]
        feeds_chunks = [other_pages[x:x + chunk_length]
                        for x in range(0, len(other_pages), chunk_length)]
        for i in range(len(feeds_chunks)):
            pages.append(self.__prepare_image_page__(
                feeds_chunks[i], props.paper_size, "full"))
        return pages

    def _get_pages_3ELVS(self, plan_view, elevations, props):
        pages = []
        chunk_length = 3
        first_page_qty = 1
        feeds = []
        if len(plan_view) > 0:
            feeds.append(plan_view[0])
        while len(elevations) > 0:
            feeds.append(elevations.pop(0))
        first_page = feeds[:first_page_qty]
        pages.append(self.__prepare_image_page__(
            first_page, props.paper_size, "full"))
        other_pages = feeds[first_page_qty:]
        feeds_chunks = [other_pages[x:x + chunk_length]
                        for x in range(0, len(other_pages), chunk_length)]
        for i in range(len(feeds_chunks)):
            pages.append(self.__prepare_image_page__(
                feeds_chunks[i], props.paper_size, "three"))
        return pages

    def _get_pages_plan_1ELVS(self, plan_view, elevations, props):
        pages = []
        if (len(elevations) == 1):
            first_page_qty = 2
            feeds = []
            if len(plan_view) > 0:
                feeds.append(plan_view[0])
            while len(elevations) > 0:
                feeds.append(elevations.pop(0))
            first_page = feeds[:first_page_qty]
            pages.append(self.__prepare_image_page__(
                first_page, props.paper_size, "two"))
        elif (len(elevations) == 2):
            first_page_qty = 3
            feeds = []
            if len(plan_view) > 0:
                feeds.append(plan_view[0])
            while len(elevations) > 0:
                feeds.append(elevations.pop(0))
            first_page = feeds[:first_page_qty]
            pages.append(self.__prepare_image_page__(
                first_page, props.paper_size, "1up2down"))
        elif (len(elevations) == 3):
            first_page_qty = 4
            feeds = []
            if len(plan_view) > 0:
                feeds.append(plan_view[0])
            while len(elevations) > 0:
                feeds.append(elevations.pop(0))
            first_page = feeds[:first_page_qty]
            pages.append(self.__prepare_image_page__(
                first_page, props.paper_size, "1up3down"))
        elif (len(elevations) == 4):
            chunk_length = 3
            first_page_qty = 2
            feeds = []
            if len(plan_view) > 0:
                feeds.append(plan_view[0])
            while len(elevations) > 0:
                feeds.append(elevations.pop(0))
            first_page = feeds[:first_page_qty]
            other_pages = feeds[first_page_qty:]
            pages.append(self.__prepare_image_page__(
                first_page, props.paper_size, "two"))
            feeds_chunks = [other_pages[x:x + chunk_length]
                            for x in range(0, len(other_pages), chunk_length)]
            for i in range(len(feeds_chunks)):
                pages.append(self.__prepare_image_page__(
                    feeds_chunks[i], props.paper_size, "three"))
        elif (len(elevations) == 5):
            chunk_length = 3
            first_page_qty = 3
            feeds = []
            if len(plan_view) > 0:
                feeds.append(plan_view[0])
            while len(elevations) > 0:
                feeds.append(elevations.pop(0))
            first_page = feeds[:first_page_qty]
            other_pages = feeds[first_page_qty:]
            pages.append(self.__prepare_image_page__(
                first_page, props.paper_size, "1up2down"))
            feeds_chunks = [other_pages[x:x + chunk_length]
                            for x in range(0, len(other_pages), chunk_length)]
            for i in range(len(feeds_chunks)):
                pages.append(self.__prepare_image_page__(
                    feeds_chunks[i], props.paper_size, "three"))
        elif (len(elevations) == 6):
            chunk_length = 3
            first_page_qty = 4
            feeds = []
            if len(plan_view) > 0:
                feeds.append(plan_view[0])
            while len(elevations) > 0:
                feeds.append(elevations.pop(0))
            first_page = feeds[:first_page_qty]
            other_pages = feeds[first_page_qty:]
            pages.append(self.__prepare_image_page__(
                first_page, props.paper_size, "1up3down"))
            feeds_chunks = [other_pages[x:x + chunk_length]
                            for x in range(0, len(other_pages), chunk_length)]
            for i in range(len(feeds_chunks)):
                pages.append(self.__prepare_image_page__(
                    feeds_chunks[i], props.paper_size, "three"))
        elif (len(elevations) > 6):
            chunk_length = 3
            first_page_qty = 1
            feeds = []
            if len(plan_view) > 0:
                feeds.append(plan_view[0])
            while len(elevations) > 0:
                feeds.append(elevations.pop(0))
            first_page = feeds[:first_page_qty]
            pages.append(self.__prepare_image_page__(
                first_page, props.paper_size, "full"))
            other_pages = feeds[first_page_qty:]
            feeds_chunks = [other_pages[x:x + chunk_length]
                            for x in range(0, len(other_pages), chunk_length)]
            for i in range(len(feeds_chunks)):
                pages.append(self.__prepare_image_page__(
                    feeds_chunks[i], props.paper_size, "three"))
        return pages

    def _get_pages_list(self, image_views, props, pdf_images):
        """Modify the images included in the file depending the number of elevations.

        Args:
            image_views (list): List of images from context.
            props (class): Properties from context views_2d.
            pdf_images (list): List of images paths.

        Returns:
            pages (list): A list with the paths of the saved images.
        """
        pages = []
        plan_view = [view for view in image_views if view.is_plan_view]
        elevations = [view for view in image_views if view.is_elv_view]
        islands = [view for view in image_views if view.is_island_view]
        accordions =\
            [view for view in image_views if view.is_acc_view]
        if len(islands) > 0 and len(elevations) > 0:
            elevations += islands
        elif len(islands) > 0 and len(accordions) > 0:
            accordions += islands
        page_layout = props.page_layout_setting
        if len(accordions) > 0:
            page_layout = props.accordions_layout_setting
        if page_layout == 'SINGLE':
            pages = self._get_SINGLE_pages(plan_view, elevations, props)
        elif page_layout == '2ELVS':
            pages = self._get_pages_2ELVS(plan_view, elevations, props)
        elif page_layout == '3ELVS':
            pages = self._get_pages_3ELVS(plan_view, elevations, props)
        elif page_layout == 'PLAN+1ELVS':
            pages = self._get_pages_plan_1ELVS(plan_view, elevations, props)
        elif page_layout == '1_ACCORD':
            pages = self._get_pages_1ACCORD(accordions, props)
        elif page_layout == 'PLAN+1ACCORDS':
            pages = self._get_pages_plan_1ACCORD(plan_view, accordions, props)
        
        return pages

    @staticmethod
    def _create_str_pdf_context():
        """Create an auxiliary dictionary with the functions (as str)
           that must be executed to obtain the data from context,
           used to find missing values.

        Returns:
            prop (dict): Dictionary with properties (key)
                        and the functions (value) to get its values.
        """
        prop = {}
        prop["edge_type_name"] =\
            "context.scene.closet_materials.edges.get_edge_type().description"
        prop["ct"] =\
            "OPERATOR_create_pdf._has_ct(context.scene.closet_materials, material_dict, bpy.data.objects)"  # noqa: E501
        prop["door_style"] =\
            "OPERATOR_create_pdf._door_style(bpy.data.objects)"
        prop["door_quantity"] =\
            "OPERATOR_create_pdf._get_door_qty(bpy.data.objects)"
        prop["drawer_style"] =\
            "OPERATOR_create_pdf._drawer_style(bpy.data.objects)"
        prop["drawer_quantity"] =\
            "OPERATOR_create_pdf._get_drawer_qty(bpy.data.objects)"
        prop["glaze_color"] =\
            "context.scene.closet_materials.get_glaze_color().description"
        prop["glaze_style"] = "OPERATOR_create_pdf._get_glaze_style(" +\
            "context.scene.closet_materials.get_glaze_color().description, " +\
            "context.scene.closet_materials)"
        prop["pull_type"] = "OPERATOR_create_pdf._get_pull_type(" +\
            "OPERATOR_create_pdf._get_pull_qty(bpy.data.objects), " +\
            "context.scene.sn_closets)"
        prop["pull_quantity"] =\
            "OPERATOR_create_pdf._get_pull_qty(bpy.data.objects)"
        prop["rod_type"] = "OPERATOR_create_pdf._get_rod_type(" +\
            "OPERATOR_create_pdf._get_rod_qty(bpy.data.objects), " +\
            "context.scene.sn_closets)"
        prop["rod_quantity"] =\
            "OPERATOR_create_pdf._get_rod_qty(bpy.data.objects)"
        prop["rod_length"] =\
            "OPERATOR_create_pdf._get_rod_length(bpy.data.objects)"
        prop["slide_type"] =\
            "OPERATOR_create_pdf._slide_type(context.scene.sn_closets)"
        return prop

    @staticmethod
    def _pdf_context(context, material_dict):
        """Create a dictionary with the data from context to put in the pdf file.

        Args:
            context (obj): blender context.
            material_dict (dict): Dictionary with material data.

        Returns:
            ctx (dict): Dictionary with the data from blender context.
        """
        ctx = {}
        ctx_str = OPERATOR_create_pdf._create_str_pdf_context()
        keys = ctx_str.keys()
        for key in keys:
            try:
                ctx[key] = eval(ctx_str[key])
            except Exception as e:
                print(e)

        return ctx

    def _fix_file_path(self):
        fixed_file_path = os.path.normpath(self.directory)
        print("FIXED FILEPATH: ", fixed_file_path)
        if os.path.exists(fixed_file_path):
            os.system(
                'start "Title" /D "{}" "{}"'.format(
                    fixed_file_path, self.filename))
        else:
            print('Cannot Find ' + fixed_file_path + self.filename)

    def execute(self, context):
        """Generate the .pdf file when 'Save 2D Drawing As...' is clicked"""
        # check_file_access
        if not self._check_file_access():
            return {'FINISHED'}
        # get views_2d properties
        props = context.window_manager.views_2d
        # get images views
        images = context.window_manager.snap.image_views
        # assign closet materials
        try:
            bpy.ops.closet_materials.assign_materials()
        except Exception as e:
            print(e)
            mess = "Materials assignment was not made "
            mess2 = "Check if the database was loaded"
            bpy.ops.wm.warning_window('INVOKE_DEFAULT',
                                      message=mess, message2=mess2)
        # get images paths and save images
        image_dic = bpy.data.images
        tempdir = bpy.app.tempdir
        pdf_images = OPERATOR_create_pdf._save_images(images,
                                                      image_dic, tempdir)
        # get pages list
        pages = self._get_pages_list(images, props, pdf_images)
        # get .pdf file path
        path = self.filepath
        # get logo
        logo = os.path.join(os.path.dirname(__file__), "full_logo.jpg")
        # get paper size
        print_paper_size = props.paper_size
        # get dictionary of materials
        closet_materials = bpy.context.scene.closet_materials
        material_dict = OPERATOR_create_pdf._materials(closet_materials)
        # create ctx dictionary from context
        ctx = OPERATOR_create_pdf._pdf_context(context, material_dict)
        # create the director
        director = PDF_Director(path, print_paper_size, pages, logo)
        # get props
        props = context.scene.snap
        # Create pdf file
        # only implemented templates "new" and "old"
        director.make("NEW", props, material_dict, **ctx)
        # FIX FILE PATH To remove all double backslashes
        self._fix_file_path()
        # #FIX FILE PATH To remove all double backslashes
        # fixed_file_path = os.path.normpath(file_path)

        # if os.path.exists(os.path.join(fixed_file_path,file_name)):
        #     os.system('start "Title" /D "' + fixed_file_path + '" "' + file_name + '"')
        # else:
        #     print('Cannot Find ' + os.path.join(fixed_file_path,file_name))
        for file in os.listdir(bpy.app.tempdir):
            full_path = os.path.join(bpy.app.tempdir, file)
            os.remove(full_path)

        return {'FINISHED'}


class PDF_generation_Warning_Window(bpy.types.Operator):
    """Show a warning window reporting missing variables.

    Attributes:
        message (str): First line of the warning message.
        message2 (str): Second line of the warning message.
    """

    bl_idname = "wm.warning_window"
    bl_label = "Warning Window"
    bl_options = {'UNDO'}

    message: bpy.props.StringProperty(name="Message")  # noqa F821
    message2: bpy.props.StringProperty(name="Message")  # noqa F821

    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        lay = self.layout
        box = lay.box()
        box.label(text=self.message, icon='ERROR')
        box.label(text=self.message2, icon='ERROR')

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


def menu_draw(self, context):
    self.layout.operator("2dviews.report_2d_drawings")


def register():
    bpy.utils.register_class(OPERATOR_create_pdf)
    bpy.utils.register_class(PDF_generation_Warning_Window)
    bpy.types.VIEW_MT_2dview_reports.append(menu_draw)


def unregister():
    bpy.utils.unregister_class(OPERATOR_create_pdf)
    bpy.utils.unregister_class(PDF_generation_Warning_Window)
    bpy.types.VIEW_MT_2dview_reports.remove(menu_draw)
