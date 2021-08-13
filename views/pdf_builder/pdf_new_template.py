from snap.views.pdf_builder.pdf_builder import Pdf_Builder
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
import json
import os

registerFont(TTFont('Calibri-Bold', 'calibrib.ttf'))
registerFont(TTFont('Calibri', 'calibri.ttf'))
GREY = (0.851, 0.851, 0.851)
REDWINE = (0.435, 0.078, 0.0)
BLACK = (0.0, 0.0, 0.0)


class New_Template_Builder(Pdf_Builder):
    """subclass of Pdf_Builder for construction of pdf files with the new template.

    Attributes:
        path (str): Path where the .pdf file will be save
                    (include name and extension),
                    example: '\an_example\views_new.pdf'.
        print_paper_size (str): Name of the paper format,
                    example: 'LEGAL'.
        pagesize (tuple[int, int]): Tuple with the width and the
                                    height of the paper.
        c (Canvas): Canvas from reportlab for the .pdf generation.
        _dic_sections (dict): Dictionary with positions and names
                             of the sections.
        _dic_lines (dict): Dictionary with positions and lengths of lines.
        _dic_labels (dict): Dictionary with positions and names of the labels.
    """

    def __init__(self, path: str, print_paper_size: str) -> None:
        sections_path = os.path.join(os.path.dirname(__file__),
                                     "new_template_sections.json")
        lines_path = os.path.join(os.path.dirname(__file__),
                                  "new_template_lines.json")
        labels_path = os.path.join(os.path.dirname(__file__),
                                   "new_template_labels.json")
        self.dic_sections = New_Template_Builder._open_json_file(sections_path)
        """The .json file in 'sections_path' contains:

        A list of dictionaries each represent a section in the block info:
            "label": the name of the section
            "position": a dictionary with the coordinates of the label in the
                        .pdf file, depending on the paper size (key)
        """
        self.dic_lines = New_Template_Builder._open_json_file(lines_path)
        """The .json file in 'lines_path' contains:

        A list of dictionaries each represent a line in the block info:
            "length": the size of the line
            "position": the initial position of the line,
                        depending on the paper size (key)
        """
        self.dic_labels = New_Template_Builder._open_json_file(labels_path)
        """The .json file in 'labels_path' contains:

        A list of dictionaries each represent a label in the block info:
            "data": a dictionary with the name of the label and the position
            "bold": 1 if the label is bold
            "underline": 1 if the label is underlined
            "checkbox": 1 if the label has a checkbox
        """
        super().__init__(path, print_paper_size)

    @staticmethod
    def _open_json_file(file: str) -> dict:
        """Open a json file and return a dictionary."""
        with open(file) as f:
            json_file = json.load(f)
        return json_file

    def _draw_section(self, msg: str, position: tuple) -> None:
        """Create a section separation (rectangle with rotate text)
           in the canvas.

        Args:
            msg (str): The name of the section.
            position (tuple): Coordinates (x, y) of the lower left corner
                              of the rectangle.
        """
        self.c.setFont("Calibri", 9)
        self.c.setFillColorRGB(*GREY)
        self.c.setStrokeColorRGB(*REDWINE)
        posx, posy = position
        x, y, w, h, r = posx, posy, 18, 91, 3
        self.c.roundRect(x, y, w, h, r, stroke=1, fill=1)
        self.c.setFillColorRGB(*REDWINE)
        self.c.saveState()
        self.c.translate((posx + 3 + (w / 2)), (posy + (h / 2)))
        self.c.rotate(90)
        self.c.drawCentredString(0, 0, msg)
        self.c.restoreState()
        self.c.setFillColorRGB(*BLACK)
        self.c.setStrokeColorRGB(*BLACK)

    def _draw_sections(self) -> None:
        """Draw a all section separators in the canvas."""
        for section in self.dic_sections:
            self._draw_section(section["label"],
                               section["position"][self.print_paper_size])

    def _draw_lines(self) -> None:
        """Draw a all section separators of the block info."""
        for line in self.dic_lines:
            posx, posy = line["position"][self.print_paper_size]
            length = line["length"]
            self.c.line(posx, posy, posx + length, posy)

    def _draw_labels(self) -> None:
        """Write all labels in the block info."""
        for group in self.dic_labels:
            self._set_label_style(group)
            self._write_labels(group["data"])
            if(group["checkbox"] == 1):
                self._draw_check_box(group["data"])
            if(group["underline"] == 1):
                self._draw_underlines(group["data"])

    def _draw_underlines(self, group_label: dict) -> None:
        """Draw a group of underlines

        Args:
            group_label (dic): A dictionary with the coordinates of a
                               group of underlines.
        """
        for label in group_label:
            posx, posy = label["position"][self.print_paper_size]
            len_txt = len(label["label"])
            self.c.line(posx, posy - 2, posx + 5*len_txt, posy - 2)

    def _draw_check_box(self, group_label: dict) -> None:
        """Draw a group of check box

        Args:
            group_label (dic): A dictionary with the coordinates
                               of a group of check box.
        """
        selected = False
        form = self.c.acroForm
        for label in group_label:
            posx, posy = label["position"][self.print_paper_size]
            form.radio(
                name='ext_ratio',
                tooltip='Field ext ratio',
                value='value1',
                selected=selected,
                x=posx-12, y=posy,
                borderStyle='solid',
                shape='circle',
                borderWidth=1,
                size=12
            )

    def _set_label_style(self, group_label: dict) -> None:
        """Set the text style for a group of labels

        Args:
            group_label (dic): A dictionary with the style data of
                              a group of labels.
        """
        bold = group_label["bold"]
        if bold == 1:
            self.c.setFont("Calibri-Bold", 9)
        else:
            self.c.setFont("Calibri", 9)

    def _write_labels(self, dic_labels: dict) -> None:
        """Write labels in the block info.

        Args:
            dic_labels (dic): A dictionary with the data
                              for the block info.
        """
        for label in dic_labels:
            posx, posy = label["position"][self.print_paper_size]
            msg = label["label"]
            self.c.drawString(posx, posy, msg)

    def draw_logo(self, logo: str) -> None:
        """Draw the Classy Closets logo in the upper left of the canvas.
           (override)

        Args:
            logo (str): The path of the logo with directory,
                        name and extension.
        """
        self.c.drawImage(logo, 30, 542, width=150, height=57, mask='auto',
                         preserveAspectRatio=True)

    def draw_block_info(self) -> None:
        """Draw the block info of the template in the canvas (override)."""
        self._draw_sections()
        self._draw_lines()
        self._draw_labels()
