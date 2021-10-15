import os
import sys

try:
    import reportlab
except ModuleNotFoundError:
    python_lib_path = os.path.join(os.path.dirname(__file__), "..", "python_lib")
    sys.path.append(python_lib_path)

from abc import ABC
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import elevenSeventeen, legal, letter
from PIL import Image as PImage

registerFont(TTFont('Calibri', 'calibri.ttf'))


class Pdf_Builder(ABC):
    """Parent class from builder pattern for construction of pdf files

     Attributes:
        path (str): Path where the .pdf file will be save
                    (include name and extension),
                    example: '\an_example\views.pdf'.
        print_paper_size (str): Name of the paper format,
                    example: 'LEGAL'.
        pagesize (tuple[int, int]): Tuple with the width and the
                                    height of the paper.
        c (Canvas): Canvas from reportlab for the .pdf generation.
    """

    def __init__(self, path: str, print_paper_size: str) -> None:
        self.print_paper_size = print_paper_size
        self.path = path
        width, height = paper_size(print_paper_size)
        self.pagesize = (width, height)
        self.c = canvas.Canvas(self.path, pagesize=self.pagesize)

    def draw_main_image(self, image: str) -> None:
        """Draw an image in the canvas.

        Args:
            image (str): The path of the image including directory,
                         name and extension.
        """
        canvas = PImage.open(image)
        canvas_width, canvas_height = canvas.size
        proportion = round(canvas_width / canvas_height, 3)
        width, height = self.pagesize
        # PV+ELVs, PV+ACC, 1 ELV pp
        if proportion <= 1.4:
            start_x, start_y = 0, 130
            target_w, target_h = width - 40, height - 150
        # 2 ELVs pp
        elif 1.4 < proportion <= 2.5:
            start_x, start_y = 0, 130
            target_w, target_h = width - 0, height - 200
        # 3 ELVs pp
        elif proportion > 2.5: 
            start_x, start_y = 0, 95
            target_w, target_h = width, height - 140
        self.c.drawImage(image, start_x, start_y, width=target_w,
                         height=target_h,
                         mask='auto', preserveAspectRatio=True) 

    def draw_info(self, form_info: dict) -> None:
        """Draw the info about the project in the canvas.

        Args:
            form_info (dict): A dictionary with labels, values and positions.
        """
        self.c.setFont("Calibri", 9)
        for field in form_info:
            lbl, val = field["label"], field["value"]
            separator = ":"
            if len(lbl) == 0:
                separator = ""
            pos = field["position"][self.print_paper_size]
            self.c.drawString(pos[0], pos[1], f'{lbl}{separator} {val}')

    def draw_logo(self, logo: str) -> None:
        """Draw the Classy Closets logo in the canvas.

        Args:
            logo (str): The path of the logo with directory,
                        name and extension.
        """
        pass

    def draw_margin(self) -> None:
        """Draw the margins of the template in the canvas."""
        pass

    def draw_block_info(self) -> None:
        """Draw the block info of the template in the canvas."""
        pass

    def show_page(self) -> None:
        """Show a page in the canvas"""
        self.c.showPage()


def paper_size(papersize_str) -> tuple:
    """Define the size of the paper depending on the name of the paper format.

    Args:
        papersize_str (str): Name of the paper format,
                example: 'LEGAL'.
    Returns:
        A tuple with the width and the height of the papers.
    """
    if papersize_str == "ELEVENSEVENTEEN":
        return landscape(elevenSeventeen)
    elif papersize_str == "LEGAL":
        return landscape(legal)
    elif papersize_str == "LETTER":
        return landscape(letter)
