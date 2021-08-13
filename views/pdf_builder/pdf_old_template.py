from snap.views.pdf_builder.pdf_builder import Pdf_Builder


class Old_Template_Builder(Pdf_Builder):
    """subclass of Pdf_Builder for construction of pdf files with the old template.

     Attributes:
        path (str): Path where the .pdf file will be save
                    (include name and extension),
                    example: '\an_example\views_old.pdf'.
        print_paper_size (str): Name of the paper format,
                    example: 'LEGAL'.
        pagesize (tuple[int, int]): Tuple with the width and the
                                    height of the paper.
        c (Canvas): Canvas from reportlab for the .pdf generation.
    """

    def draw_logo(self, logo: str) -> None:
        """Draw the Classy Closets logo in the lower left corner of the canvas.
           (override)

        Args:
            logo (str): The path of the logo with directory,
                        name and extension.
        """
        self.c.drawImage(logo, 20, 20, width=170, height=80,
                         mask='auto', preserveAspectRatio=True)

    def draw_margin(self) -> None:
        """Draw the margin of the template in the canvas (override)."""
        width, height = self.pagesize
        self.c.rect(20, 100, width - 40, height - 120)

    def draw_block_info(self) -> None:
        """Draw the block info of the template in the canvas (override)."""
        width, _ = self.pagesize
        self.c.rect(20, 20, 170, 80)
        self.c.rect(20, 20, width - 40, 80)
