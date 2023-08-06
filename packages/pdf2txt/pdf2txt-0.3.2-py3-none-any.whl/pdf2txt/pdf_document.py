from pdf2txt.utils import get_page_layout
from pdf2txt.pdf_page import PDFPage
from pdf2txt.utils import get_fonts_statistics
import pandas as pd

class PDFDocument(object):
    def __init__(self, pdf):

        page = 0
        self.pages=[]
        self.title=[]
        for layout, _ in get_page_layout(pdf):
            page += 1
            self.pages.append(PDFPage(self, layout, page_number=page))

        self.font_statistics=get_fonts_statistics([line for page in self.pages for line in page.horizental_text_lines])


    def get_features(self):
        return pd.DataFrame([feature for page in self.pages for feature in page.get_features()])
    def detect_semantic_structure(self):
        for page in self.pages:
            page.detect_semantic_structure()

    def to_text(self):
        return '\n'.join([p.to_text()+'\n' for p in self.pages])