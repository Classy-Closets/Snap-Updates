import bpy
import os
import random
import string
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import legal, letter, elevenSeventeen, inch, A4, landscape
from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import reportlab.lib.colors as colors
from reportlab.platypus.flowables import BulletDrawer

from mv import fd_types, unit, utils

from PIL import Image, ImageChops


def get_dimension_props():
    dimprops = eval("bpy.context.scene.mv_closet_dimensions")
    return dimprops


class OPERATOR_create_pdf(bpy.types.Operator):
    bl_idname = "2dviews.report_2d_drawings"
    bl_label = "Save 2D Drawing As..."
    bl_description = "This creates a 2D drawing pdf of all of the images"

    filter_glob = bpy.props.StringProperty(default="*.pdf", options={'HIDDEN'})
    filepath = bpy.props.StringProperty(subtype="FILE_PATH")
    filename = bpy.props.StringProperty()
    directory = bpy.props.StringProperty()
    files = None

    def invoke(self, context, event):
        bfile = bpy.path.abspath("//")
        self.directory = bfile
        self.filename = "2D Views.pdf"
        op = context.window_manager.fileselect_add(self)

        print(event.type)
        return {'RUNNING_MODAL'}

    def check_file_access(self):
        if os.path.exists(self.filepath):
            try:
                f = open(self.filepath, 'wb')
                f.close()

            except IOError:
                self.report(
                    {'ERROR'}, "The selected file could not be accessed!: {}".format(self.filepath))
                return False

        return True

    def materials(self, context):
        material_dict = {}
        for spec_group in context.scene.mv.spec_groups:

            surface_pointer = spec_group.materials["Closet_Part_Surfaces"]
            edge_pointer = spec_group.materials["Closet_Part_Edges"]
            ct_pointer = spec_group.materials["Countertop_Surface"]
            stain_pointer = spec_group.materials["Wood_Door_Surface"]
            glass_pointer = spec_group.materials["Glass"]

            material_dict["Surface Pointer"] = surface_pointer.item_name
            material_dict["Edge Pointer"] = edge_pointer.item_name
            material_dict["CT Pointer"] = ct_pointer.item_name
            material_dict["Stain Pointer"] = stain_pointer.item_name
            material_dict["Glass Pointer"] = glass_pointer.item_name
            break

        return material_dict

    def has_ct(self, context):

        material_dict = self.materials(context)
        ct_type = context.scene.cc_materials.ct_type

        for obj in bpy.data.objects:
            props = obj.lm_closets
            if props.is_counter_top_insert_bp:
                return (ct_type + " " + material_dict['CT Pointer'])

        return ("None")

    # REFACTOR db_materials function replaces this
    # def edge_type_name(self,context):
    #     name = "Unknown"
    #     props = context.scene.db_materials
    #     edge_type_code = int(props.edge_type_menu)

    #     for edge_type in props.edge_types:
    #         if edge_type.type_code == edge_type_code:
    #             name = edge_type.name

    #     return name

    # REFACTOR db_materials replaces cc_materials
    def edge_type(self, context):
        props = context.scene.cc_materials
        if props.edge_profile == 'SQUARE':
            return context.scene.cc_materials.square_edge
        else:
            return context.scene.cc_materials.round_edge

    def slide_type(self, context):
        if context.scene.lm_closets.closet_options.box_type == 'MEL':
            return context.scene.lm_closets.closet_options.mel_slide_name
        else:
            return context.scene.lm_closets.closet_options.dt_slide_name

    def door_style(self, context):
        for obj in bpy.data.objects:
            if "Door.Cutpart" in obj.name and obj.hide == False:
                return "Melamine"
            if " Door" in obj.name and obj.hide == False:
                return obj.mv.comment

    def drawer_style(self, context):
        for obj in bpy.data.objects:
            if "Drawer Front.Cutpart" in obj.name and obj.hide == False:
                return "Melamine"
            if " Drawer" in obj.mv.comment and obj.hide == False:
                return obj.mv.comment

# QUANTITIES
    # PULLS
    def get_pull_qty(self, context):
        number_of_pulls = 0
        for obj in bpy.data.objects:
            if obj.mv.is_cabinet_pull and obj.hide == False:
                number_of_pulls += 1
        return number_of_pulls

    # RODS
    def get_rod_qty(self, context):
        number_of_rods = 0
        for obj in bpy.data.objects:
            if "Hang Rod" in obj.mv.name_object and obj.hide == False:
                number_of_rods += 1
        return number_of_rods

    # ROD_LENGTH
    def get_rod_length(self, context):
        length_of_rods = 0
        for obj in bpy.data.objects:
            if "Hang Rod" in obj.mv.name_object and obj.hide == False:
                # return obj.dimensions.x
                length_of_rods += obj.dimensions.x
        return length_of_rods

    # DRAWERS
    def get_drawer_qty(self, context):
        number_of_drawers = 0
        for obj in bpy.data.objects:
            if "Drawer Bottom" in obj.name and obj.hide == False:
                number_of_drawers += 1
        return number_of_drawers

    # DOORS
    def get_door_qty(self, context):
        number_of_doors = 0
        for obj in bpy.data.objects:
            if " Door" in obj.name and obj.hide == False:
                number_of_doors += 1
        return number_of_doors

    def random_string(self, length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.sample(letters, length))
        return result_str

    def trim(self, image):
        bg = Image.new(image.mode, image.size, image.getpixel((0, 0)))
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

    def join_images_horizontal(self, images_list, output, border=(25, 75, 50, 75), keep_width=False):
        white_bg = (255, 255, 255)
        cropped_ims = []
        original_ims = []
        for i in images_list:
            im = Image.open(i)
            original_ims.append(im)
            cropped_ims.append(self.trim(im))
        widths, heights = zip(*(i.size for i in cropped_ims))
        orig_widths, orig_heights = zip(*(i.size for i in original_ims))
        if keep_width:
            total_width = sum(orig_widths) + border[0] + border[2]
            x_offset = border[0] + int((sum(orig_widths) - sum(widths)) / 2)
        else:
            total_width = sum(widths) + border[0] + border[2]
            x_offset = border[0]
        max_height = max(heights) + border[1] + border[3]
        new_im = Image.new('RGB', (total_width, max_height), white_bg)
        for im in cropped_ims:
            y_offset = max(heights) - im.size[1] + border[1]
            new_im.paste(im, (x_offset, y_offset))
            x_offset += im.size[0] + 10
        # Always save as PNG, JPG makes blender crash silently
        img_file = os.path.join(bpy.app.tempdir + output + ".png")
        new_im.save(img_file)
        return img_file

    def join_images_vertical(self, images_files_list, output, vertical_padding=50):
        white_bg = (255, 255, 255)
        images_list = []
        for i in images_files_list:
            im = Image.open(i)
            images_list.append(im)
        widths, heights = zip(*(i.size for i in images_list))
        max_width = max(widths)
        total_height = sum(heights) + (vertical_padding * 2)
        new_im = Image.new('RGB', (max_width, total_height), white_bg)
        y_offset = 0
        for im in images_list:
            new_im.paste(im, (0, y_offset + vertical_padding))
            y_offset += im.size[1]
        # Always save as PNG, JPG makes blender crash silently
        img_file = os.path.join(bpy.app.tempdir + output + ".png")
        new_im.save(img_file)
        return img_file

    def get_image_size(self, image_file):
        image = Image.open(image_file)
        width, height = image.size
        return (int(width), int(height))

    # Internal function
    # receives: a list of fd_images and a layout option
    # return: a page asemm to be appended to the PDF file
    # LAYOUTS:
    # full - One image per page - Full Page
    # two - Two images per page, side by side
    # three - Three images per page, side by side
    # 1up2down  - One image on upper half, two on the bottom half
    # 1up3down - One image on upper half, three on the bottom half
    def __prepare_image_page__(self, fd_images_list, page_paper_size, option):
        if option == "full":
            return self.join_images_horizontal([bpy.app.tempdir + fd_images_list[0].name + ".jpg"], self.random_string(6))
        if option == "two":
            fd_images_list = fd_images_list[:2]
            image_files = [(bpy.app.tempdir + image.name + ".jpg")
                           for image in fd_images_list]
            return self.join_images_horizontal(image_files, self.random_string(6))
        if option == "three":
            fd_images_list = fd_images_list[:3]
            image_files = [(bpy.app.tempdir + image.name + ".jpg")
                           for image in fd_images_list]
            return self.join_images_horizontal(image_files, self.random_string(6))
        if option == "1up2down":
            fd_images_list = fd_images_list[:3]
            lower_part = [(bpy.app.tempdir + image.name + ".jpg")
                          for image in fd_images_list[1:]]
            upper_part = [(bpy.app.tempdir + image.name + ".jpg")
                          for image in fd_images_list[:1]]
            lower_image = self.join_images_horizontal(
                lower_part, option + "lower")
            lower_w, lower_h = self.get_image_size(lower_image)
            upper_w, upper_h = self.get_image_size(
                bpy.app.tempdir + fd_images_list[0].name + ".jpg")
            border = (int((lower_w - upper_w)/2), 50,
                      (int((lower_w - upper_w)/2)), 50)
            upper_image = self.join_images_horizontal(
                upper_part, option + "upper", border, True)
            return self.join_images_vertical([upper_image, lower_image], self.random_string(6))
        if option == "1up3down":
            fd_images_list = fd_images_list[:4]
            lower_part = [(bpy.app.tempdir + image.name + ".jpg")
                          for image in fd_images_list[1:]]
            upper_part = [(bpy.app.tempdir + image.name + ".jpg")
                          for image in fd_images_list[:1]]
            lower_image = self.join_images_horizontal(
                lower_part, option + "lower")
            lower_w, lower_h = self.get_image_size(lower_image)
            upper_w, upper_h = self.get_image_size(
                bpy.app.tempdir + fd_images_list[0].name + ".jpg")
            border = (int((lower_w - upper_w)/2), 50,
                      int((lower_w - upper_w)/2), 50)
            upper_image = self.join_images_horizontal(
                upper_part, option + "upper", border, True)
            return self.join_images_vertical([upper_image, lower_image], self.random_string(6))
        return False

    def fix_file_ext(self, name, file_ext):
        if not name.lower().endswith(file_ext):
            name_strs = name.split('.')
            if len(name_strs) > 1 and name_strs[-1] == 'ccp' or 'blend':
                fixed_name = '{}.{}'.format('.'.join(name_strs[:-1]), file_ext)
            else:
                fixed_name = '{}.{}'.format(name, file_ext)
            return fixed_name
        else:
            return name

    # HINGES
#     def get_hinge_qty(self,context):
#         number_of_hinges = 0
#         for obj in bpy.data.objects:
#             #props = obj.lm_closets
#             if obj.mv.is_hinge and obj.hide == False:
#                 number_of_hinges += 1
#         return number_of_hinges
    def execute(self, context):
        if not self.check_file_access():
            return {'FINISHED'}

        props = context.window_manager.views_2d
        dimprops = get_dimension_props()
        incl_accordions = dimprops.include_accordions
        option = props.page_layout_setting
        if incl_accordions:
            option = props.accordions_layout_setting
        bpy.ops.lm_closets.assign_materials()
        pdf_images = []

        images = context.window_manager.mv.image_views
        for img in images:
            image = bpy.data.images[img.image_name]
            image.save_render(os.path.join(
                bpy.app.tempdir, image.name + ".jpg"))
            pdf_images.append(os.path.join(
                bpy.app.tempdir, image.name + ".jpg"))

        if 'fd_projects' in bpy.context.user_preferences.addons.keys():
            proj_props = context.window_manager.fd_project
        else:
            proj_props = None

        if bpy.data.filepath == "":
            if proj_props:
                proj_name = proj_props.projects[proj_props.project_index].name
                file_path = os.path.join(bpy.utils.user_resource(
                    'DATAFILES'), "projects", proj_name)
            else:
                file_path = bpy.app.tempdir
                room_name = "Unsaved"
        else:
            project_path = os.path.dirname(bpy.data.filepath)
            room_name, ext = os.path.splitext(
                os.path.basename(bpy.data.filepath))

            if proj_props and len(proj_props.projects) > 0:
                proj_name = proj_props.projects[proj_props.project_index].name
                file_path = os.path.join(bpy.utils.user_resource(
                    'DATAFILES'), "projects", proj_name)
            else:
                file_path = os.path.join(project_path, room_name)
                if not os.path.exists(file_path):
                    os.makedirs(file_path)

        width, height = self.paper_size(props.paper_size)
        image_views = context.window_manager.mv.image_views
        plan_view = [view for view in image_views if view.is_plan_view]
        elevations = [view for view in image_views if view.is_elv_view and 'accordion' not in view.image_name.lower()]
        accordions = [view for view in image_views if view.is_elv_view and 'accordion' in view.image_name.lower()]
        pages = []

        if option == '1_ACCORD':
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
            feeds_chunks = [other_pages[x:x+chunk_length]
                            for x in range(0, len(other_pages), chunk_length)]
            for i in range(len(feeds_chunks)):
                pages.append(self.__prepare_image_page__(
                    feeds_chunks[i], props.paper_size, "two"))

        if option == '2_ACCORD':
            pages = []
            chunk_length = 2
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
            feeds_chunks = [other_pages[x:x+chunk_length]
                            for x in range(0, len(other_pages), chunk_length)]
            for i in range(len(feeds_chunks)):
                pages.append(self.__prepare_image_page__(
                    feeds_chunks[i], props.paper_size, "two"))

        if option == 'SINGLE':
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
            feeds_chunks = [other_pages[x:x+chunk_length]
                            for x in range(0, len(other_pages), chunk_length)]
            for i in range(len(feeds_chunks)):
                pages.append(self.__prepare_image_page__(
                    feeds_chunks[i], props.paper_size, "full"))

        elif option == '2ELVS':
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
            feeds_chunks = [other_pages[x:x+chunk_length]
                            for x in range(0, len(other_pages), chunk_length)]
            for i in range(len(feeds_chunks)):
                pages.append(self.__prepare_image_page__(
                    feeds_chunks[i], props.paper_size, "two"))

        elif option == '3ELVS':
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
            feeds_chunks = [other_pages[x:x+chunk_length]
                            for x in range(0, len(other_pages), chunk_length)]
            for i in range(len(feeds_chunks)):
                pages.append(self.__prepare_image_page__(
                    feeds_chunks[i], props.paper_size, "three"))

        elif option == 'PLAN+1ELVS':
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
                feeds_chunks = [other_pages[x:x+chunk_length]
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
                feeds_chunks = [other_pages[x:x+chunk_length]
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
                feeds_chunks = [other_pages[x:x+chunk_length]
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
                feeds_chunks = [other_pages[x:x+chunk_length]
                                for x in range(0, len(other_pages), chunk_length)]
                for i in range(len(feeds_chunks)):
                    pages.append(self.__prepare_image_page__(
                        feeds_chunks[i], props.paper_size, "three"))

        elif option == 'PLAN+1ACCORDS':
            pages = []
            if (len(accordions) == 1):
                first_page_qty = 2
                feeds = []
                if len(plan_view) > 0:
                    feeds.append(plan_view[0])
                while len(accordions) > 0:
                    feeds.append(accordions.pop(0))
                first_page = feeds[:first_page_qty]
                pages.append(self.__prepare_image_page__(
                    first_page, props.paper_size, "two"))
            elif (len(accordions) == 2):
                first_page_qty = 3
                feeds = []
                if len(plan_view) > 0:
                    feeds.append(plan_view[0])
                while len(accordions) > 0:
                    feeds.append(accordions.pop(0))
                first_page = feeds[:first_page_qty]
                pages.append(self.__prepare_image_page__(
                    first_page, props.paper_size, "1up2down"))
            elif (len(accordions) == 3):
                first_page_qty = 4
                feeds = []
                if len(plan_view) > 0:
                    feeds.append(plan_view[0])
                while len(accordions) > 0:
                    feeds.append(accordions.pop(0))
                first_page = feeds[:first_page_qty]
                pages.append(self.__prepare_image_page__(
                    first_page, props.paper_size, "1up3down"))
            elif (len(accordions) == 4):
                chunk_length = 3
                first_page_qty = 2
                feeds = []
                if len(plan_view) > 0:
                    feeds.append(plan_view[0])
                while len(accordions) > 0:
                    feeds.append(accordions.pop(0))
                first_page = feeds[:first_page_qty]
                other_pages = feeds[first_page_qty:]
                pages.append(self.__prepare_image_page__(
                    first_page, props.paper_size, "two"))
                feeds_chunks = [other_pages[x:x+chunk_length]
                                for x in range(0, len(other_pages), chunk_length)]
                for i in range(len(feeds_chunks)):
                    pages.append(self.__prepare_image_page__(
                        feeds_chunks[i], props.paper_size, "three"))
            elif (len(accordions) == 5):
                chunk_length = 3
                first_page_qty = 3
                feeds = []
                if len(plan_view) > 0:
                    feeds.append(plan_view[0])
                while len(accordions) > 0:
                    feeds.append(accordions.pop(0))
                first_page = feeds[:first_page_qty]
                other_pages = feeds[first_page_qty:]
                pages.append(self.__prepare_image_page__(
                    first_page, props.paper_size, "1up2down"))
                feeds_chunks = [other_pages[x:x+chunk_length]
                                for x in range(0, len(other_pages), chunk_length)]
                for i in range(len(feeds_chunks)):
                    pages.append(self.__prepare_image_page__(
                        feeds_chunks[i], props.paper_size, "three"))
            elif (len(accordions) == 6):
                chunk_length = 3
                first_page_qty = 4
                feeds = []
                if len(plan_view) > 0:
                    feeds.append(plan_view[0])
                while len(accordions) > 0:
                    feeds.append(accordions.pop(0))
                first_page = feeds[:first_page_qty]
                other_pages = feeds[first_page_qty:]
                pages.append(self.__prepare_image_page__(
                    first_page, props.paper_size, "1up3down"))
                feeds_chunks = [other_pages[x:x+chunk_length]
                                for x in range(0, len(other_pages), chunk_length)]
                for i in range(len(feeds_chunks)):
                    pages.append(self.__prepare_image_page__(
                        feeds_chunks[i], props.paper_size, "three"))
            elif (len(accordions) > 6):
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
                feeds_chunks = [other_pages[x:x+chunk_length]
                                for x in range(0, len(other_pages), chunk_length)]
                for i in range(len(feeds_chunks)):
                    pages.append(self.__prepare_image_page__(
                        feeds_chunks[i], props.paper_size, "three"))

        self.write_images(context, pages, props.paper_size)

        # FIX FILE PATH To remove all double backslashes
        fixed_file_path = os.path.normpath(self.directory)
        print("FIXED FILEPATH: ", fixed_file_path)

        if os.path.exists(fixed_file_path):
            os.system(
                'start "Title" /D "{}" "{}"'.format(fixed_file_path, self.filename))
        else:
            print('Cannot Find ' + fixed_file_path + self.filename)

        # #FIX FILE PATH To remove all double backslashes
        # fixed_file_path = os.path.normpath(file_path)

        # if os.path.exists(os.path.join(fixed_file_path,file_name)):
        #     os.system('start "Title" /D "' + fixed_file_path + '" "' + file_name + '"')
        # else:
        #     print('Cannot Find ' + os.path.join(fixed_file_path,file_name))

        # Clean up temp dir at the end to prevent black renders
        for f in os.listdir(bpy.app.tempdir):
            os.remove(os.path.join(bpy.app.tempdir, f))

        return {'FINISHED'}

    def paper_size(self, papersize_str):
        if papersize_str == "ELEVENSEVENTEEN":
            return landscape(elevenSeventeen)
        elif papersize_str == "LEGAL":
            return landscape(legal)
        elif papersize_str == "LETTER":
            return landscape(letter)

    def write_images(self, context, pages, print_paper_size):
        labels_coordinates = {
            "ELEVENSEVENTEEN": {
                "job_name": (25, 760),
                "job_number": (25, 748),
                "install_date": (25, 736),
                "designer_name": (955, 760),
                "designer_phone": (1100, 760),
                "client_name": (955, 748),
                "client_phone": (1100, 748),
                "client_number": (955, 736),
                "client_email": (1015, 736),
                "material": (200, 85),
                "eb_type": (200, 70),
                "eb_color": (200, 55),
                "countertops": (200, 40),
                "glass": (200, 25),
                "door_style": (370, 85),
                "drawer_style": (370, 70),
                "paint_stain": (370, 55),
                "glaze_color": (370, 40),
                "glaze_style": (370, 25),
                "pulls": (560, 85),
                "rods": (560, 70),
                "slides": (560, 55),
                "hinges": (560, 40),
                "job_comments": (560, 25),
                "tear_out": (800, 85),
                "new_construction": (800, 70),
                "floor": (800, 55),
                "parking_info": (800, 40),
                "touch_up": (930, 85),
                "elevator": (930, 70),
                "door": (930, 55),
                "block_wall": (1060, 85),
                "stairs": (1060, 70),
                "base_height": (1060, 55)
            },
            "LEGAL": {
                "job_name": (25, 580),
                "job_number": (25, 568),
                "install_date": (25, 556),
                "designer_name": (750, 580),
                "designer_phone": (895, 580),
                "client_name": (750, 568),
                "client_phone": (895, 568),
                "client_number": (750, 556),
                "client_email": (835, 556),
                "material": (200, 85),
                "eb_type": (200, 70),
                "eb_color": (200, 55),
                "countertops": (200, 40),
                "glass": (200, 25),
                "door_style": (370, 85),
                "drawer_style": (370, 70),
                "paint_stain": (370, 55),
                "glaze_color": (370, 40),
                "glaze_style": (370, 25),
                "pulls": (560, 85),
                "rods": (560, 70),
                "slides": (560, 55),
                "hinges": (560, 40),
                "job_comments": (560, 25),
                "tear_out": (755, 85),
                "new_construction": (755, 70),
                "floor": (755, 55),
                "parking_info": (755, 40),
                "touch_up": (830, 85),
                "elevator": (830, 70),
                "door": (830, 55),
                "block_wall": (903, 85),
                "stairs": (903, 70),
                "base_height": (903, 55)
            },
            "LETTER": {
                "job_name": (25, 580),
                "job_number": (25, 568),
                "install_date": (25, 556),
                "designer_name": (570, 580),
                "designer_phone": (675, 580),
                "client_name": (570, 568),
                "client_phone": (675, 568),
                "client_number": (570, 556),
                "client_email": (630, 556),
                "material": (200, 85),
                "eb_type": (200, 70),
                "eb_color": (200, 55),
                "countertops": (200, 40),
                "glass": (200, 25),
                "door_style": (300, 85),
                "drawer_style": (300, 70),
                "paint_stain": (300, 55),
                "glaze_color": (300, 40),
                "glaze_style": (300, 25),
                "pulls": (420, 85),
                "rods": (420, 70),
                "slides": (420, 55),
                "hinges": (420, 40),
                "job_comments": (420, 25),
                "tear_out": (610, 85),
                "new_construction": (610, 70),
                "floor": (610, 55),
                "parking_info": (610, 40),
                "touch_up": (660, 85),
                "elevator": (660, 70),
                "door": (660, 55),
                "block_wall": (710, 85),
                "stairs": (710, 70),
                "base_height": (710, 55)
            }
        }

        props = context.scene.mv
        width, height = self.paper_size(print_paper_size)
        material_dict = self.materials(context)
        # REFACTOR edge_profile not used anymore
        # edge_profile = context.scene.cc_materials.edge_profile

        # REFACTOR db_materials replaces cc_materials
        #edge_type_name = context.scene.db_materials.get_edge_description()

        edge_type_name = self.edge_type(context)

        ct_type = context.scene.cc_materials.ct_type
#        pull_type = context.scene.lm_closets.closet_options.pull_name
        pull_quantity = self.get_pull_qty(context)
        ct = self.has_ct(context)
        hinge_type = context.scene.lm_closets.closet_options.hinge_name
#        rod_type = context.scene.lm_closets.closet_options.rods_name
        rod_quantity = self.get_rod_qty(context)
        rod_length = self.get_rod_length(context)
        slide_type = self.slide_type(context)
        drawer_quantity = self.get_drawer_qty(context)
        door_quantity = self.get_door_qty(context)
        door_style = self.door_style(context)
        drawer_style = self.drawer_style(context)
#         hinge_quantity = (2*self.get_door_qty(context))
#         slide_quantity = self.get_drawer_qty(context)
        glaze_color = context.scene.cc_materials.glaze_color
#        objects = self.objects(context)

        if glaze_color == "None":
            glaze_style = "None"
        else:
            glaze_style = context.scene.cc_materials.glaze_style

        if pull_quantity == 0:
            pull_type = "None"
        else:
            pull_type = context.scene.lm_closets.closet_options.pull_name

        if rod_quantity == 0:
            rod_type = "None"
        else:
            rod_type = context.scene.lm_closets.closet_options.rods_name

        self.filepath = self.fix_file_ext(self.filepath, 'pdf')
        self.filename = self.fix_file_ext(self.filename, 'pdf')

        c = canvas.Canvas(
            self.filepath, pagesize=self.paper_size(print_paper_size))
        logo = os.path.join(os.path.dirname(__file__), "full_logo.jpg")
        for page in pages:
            c.setFont("Times-Roman", 9)

        # MAIN DESGIN IMAGE
            # PICTURE
            if type(page) is str:
                c.drawImage(page, 20, 80, width=width-40, height=height -
                            120, mask='auto', preserveAspectRatio=True)
            elif type(page) is tuple or type(page) is list:
                for img in page:
                    image_file = os.path.join(
                        bpy.app.tempdir, img[0].name + ".jpg")
                    c.drawImage(image_file, img[1], img[2], width=img[3],
                                height=img[4], mask='auto', preserveAspectRatio=True)
            else:
                continue

            # PICTURE BOX
            c.rect(20, 100, width-40, height-120)

        # LOGO
            # LOGO
            c.drawImage(logo, 20, 20, width=170, height=80,
                        mask='auto', preserveAspectRatio=True)
            # LOGO BOX
            c.rect(20, 20, 170, 80)

            c.rect(20, 20, width-40, 80)

        # JOB INFO
            # JOB NAME
            c.drawString(labels_coordinates[print_paper_size]["job_name"][0],
                         labels_coordinates[print_paper_size]["job_name"][1], "Job Name: " + props.job_name)
            # JOB NUMBER
            c.drawString(labels_coordinates[print_paper_size]["job_number"][0],
                         labels_coordinates[print_paper_size]["job_number"][1], "Job Number: " + props.job_number)
            # INSTALL DATE
            c.drawString(labels_coordinates[print_paper_size]["install_date"][0],
                         labels_coordinates[print_paper_size]["install_date"][1], "Install Date: " + props.install_date)

        # CLIENT INFO
            # labels_coordinates[print_paper_size][""][0], labels_coordinates[print_paper_size][""][1],
            # DESIGNER
            c.drawString(labels_coordinates[print_paper_size]["designer_name"][0],
                         labels_coordinates[print_paper_size]["designer_name"][1], "Designer: " + props.designer_name)
            # DESIGNER PHONE
            c.drawString(labels_coordinates[print_paper_size]["designer_phone"][0],
                         labels_coordinates[print_paper_size]["designer_phone"][1], "Phone: " + props.designer_phone)
            # CLEINT NAME
            c.drawString(labels_coordinates[print_paper_size]["client_name"][0],
                         labels_coordinates[print_paper_size]["client_name"][1], "Client Name: " + props.client_name)
            # CLEINT PHONE
            c.drawString(labels_coordinates[print_paper_size]["client_phone"][0],
                         labels_coordinates[print_paper_size]["client_phone"][1], "Phone: " + props.client_phone)
            # CLEINT NUMBER
            c.drawString(labels_coordinates[print_paper_size]["client_number"][0],
                         labels_coordinates[print_paper_size]["client_number"][1], "Client #: " + props.client_number)
            # CLEINT EMAIL
            c.drawString(labels_coordinates[print_paper_size]["client_email"][0],
                         labels_coordinates[print_paper_size]["client_email"][1], "Email: " + props.client_email)

        # MATERIALS
            e = str(edge_type_name)

            # MATERIAL
            c.drawString(labels_coordinates[print_paper_size]["material"][0], labels_coordinates[print_paper_size]
                         ["material"][1], "Material: " + material_dict['Surface Pointer'])
            # EDGEBAND
            c.drawString(labels_coordinates[print_paper_size]["eb_type"][0],
                         labels_coordinates[print_paper_size]["eb_type"][1], "EB Type: " + e.capitalize())
            # EDGEBAND COLOR
            c.drawString(labels_coordinates[print_paper_size]["eb_color"][0], labels_coordinates[print_paper_size]
                         ["eb_color"][1], "EB Color: " + material_dict['Edge Pointer'])
            # COUNTERTOPS
            c.drawString(labels_coordinates[print_paper_size]["countertops"][0],
                         labels_coordinates[print_paper_size]["countertops"][1], "Countertops: " + ct)
            # GLASS
            c.drawString(labels_coordinates[print_paper_size]["glass"][0],
                         labels_coordinates[print_paper_size]["glass"][1], "Glass: " + material_dict['Glass Pointer'])

        # WOOD
            # DOOR STYLE
            c.drawString(labels_coordinates[print_paper_size]["door_style"][0], labels_coordinates[print_paper_size]
                         ["door_style"][1], "Door Style: " + str(door_style) + " Qty: " + str(door_quantity))
            # DRAWER STYLE
            c.drawString(labels_coordinates[print_paper_size]["drawer_style"][0], labels_coordinates[print_paper_size]
                         ["drawer_style"][1], "Drawer Style: " + str(drawer_style) + " Qty: " + str(drawer_quantity))
            # STAIN/PAINT
            c.drawString(labels_coordinates[print_paper_size]["paint_stain"][0], labels_coordinates[print_paper_size]
                         ["paint_stain"][1], "Paint/Stain: " + material_dict['Stain Pointer'])
            # GLAZE
            c.drawString(labels_coordinates[print_paper_size]["glaze_color"][0],
                         labels_coordinates[print_paper_size]["glaze_color"][1], "Glaze Color: " + str(glaze_color))

            c.drawString(labels_coordinates[print_paper_size]["glaze_style"][0],
                         labels_coordinates[print_paper_size]["glaze_style"][1], "Glaze Style: " + str(glaze_style))

        # HARDWARE
            # PULLS
            c.drawString(labels_coordinates[print_paper_size]["pulls"][0], labels_coordinates[print_paper_size]
                         ["pulls"][1], "Pulls: " + pull_type + " Qty: " + str(pull_quantity))
            # RODS
            c.drawString(labels_coordinates[print_paper_size]["rods"][0], labels_coordinates[print_paper_size]["rods"]
                         [1], "Rods: " + rod_type + " Qty: " + str(rod_quantity) + " LF: " + str(round(rod_length/.3048, 2)))
            # SLIDES
            c.drawString(labels_coordinates[print_paper_size]["slides"][0],
                         labels_coordinates[print_paper_size]["slides"][1], "Slides: " + str(slide_type))
            # HINGES
            c.drawString(labels_coordinates[print_paper_size]["hinges"][0],
                         labels_coordinates[print_paper_size]["hinges"][1], "Hinges: " + hinge_type)
            # JOB COMMENTS
            c.drawString(labels_coordinates[print_paper_size]["job_comments"][0], labels_coordinates[print_paper_size]
                         ["job_comments"][1], "Job Comments: " + props.job_comments)  # + str(objects))

        # SITE INFO
            # TEAR OUT
            c.drawString(labels_coordinates[print_paper_size]["tear_out"][0],
                         labels_coordinates[print_paper_size]["tear_out"][1], "Tear Out: " + props.tear_out)
            # TOUCH UP
            c.drawString(labels_coordinates[print_paper_size]["touch_up"][0],
                         labels_coordinates[print_paper_size]["touch_up"][1], "Touch Up: " + props.touch_up)
            # BLOCK WALL
            c.drawString(labels_coordinates[print_paper_size]["block_wall"][0],
                         labels_coordinates[print_paper_size]["block_wall"][1], "Block Wall: " + props.block_wall)

            # NEW CONSTRUCTION
            c.drawString(labels_coordinates[print_paper_size]["new_construction"][0],
                         labels_coordinates[print_paper_size]["new_construction"][1], "New Const: " + props.new_construction)
            # ELEVATOR
            c.drawString(labels_coordinates[print_paper_size]["elevator"][0],
                         labels_coordinates[print_paper_size]["elevator"][1], "Elev: " + props.elevator)
            # STAIRS
            c.drawString(labels_coordinates[print_paper_size]["stairs"][0],
                         labels_coordinates[print_paper_size]["stairs"][1], "Stairs: " + props.stairs)

            # FLOOR TYPE
            c.drawString(labels_coordinates[print_paper_size]["floor"][0],
                         labels_coordinates[print_paper_size]["floor"][1], "Floor: " + props.floor)
            # DOOR TYPE
            c.drawString(labels_coordinates[print_paper_size]["door"][0],
                         labels_coordinates[print_paper_size]["door"][1], "Door: " + props.door)
            # BASEBOARD HEIGHT
            c.drawString(labels_coordinates[print_paper_size]["base_height"][0],
                         labels_coordinates[print_paper_size]["base_height"][1], "Base HT: " + props.base_height)

            # PARKING DETAILS/INSTRUCTIONS
            c.drawString(labels_coordinates[print_paper_size]["parking_info"][0],
                         labels_coordinates[print_paper_size]["parking_info"][1], "Parking/Info: " + props.parking)

            c.showPage()

        c.save()


def menu_draw(self, context):
    self.layout.operator("2dviews.report_2d_drawings")


def register():
    bpy.utils.register_class(OPERATOR_create_pdf)
    bpy.types.MENU_2dview_reports.append(menu_draw)


def unregister():
    bpy.utils.unregister_class(OPERATOR_create_pdf)
