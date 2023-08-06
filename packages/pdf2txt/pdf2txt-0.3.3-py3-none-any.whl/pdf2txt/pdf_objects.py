from pdf2txt.utils import get_fonts, fix_sentences

class Span():
    def __init__(self, textline):
        self.text = textline.get_text().strip()
        self.font = get_fonts(textline)
        self.x0, self.x1, self.y0, self.y1=textline.x0, textline.x1, textline.y0, textline.y1


        self.textlines=[textline]
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Span):
            return self.text == other.text and self.x0==other.x0 and self.y1==other.y1
        return False

    def __repr__(self):
        return '<'+self.text+'>'

    def add(self, other, separator='\n'):
        self.text += separator + other.text
        self.y0 = min(other.y0, self.y0)
        self.x0 = min(other.x0, self.x0)
        self.y1=max(other.y1, self.y1)
        self.x1 = max(other.x1, self.x1)
        self.textlines.extend(other.textlines)
        return self

class PDFParagraph(object):
    def __init__(self, parent):
        self.title=None
        self.is_table=False
        self.lines=[]
        self.parent=parent

    def print(self):
        print()
        title=self.title.Text if self.title else ""
        print(title)
        print('-'*len(title))
        for line in self.lines:
            print(line.Text)
    def to_text(self):
        title = self.title.Text if self.title else ""
        return_str= title+'\n'
        return_str+='-'*len(title)
        for line in self.lines:
            return_str+='\n'+line.Text
        return return_str

        # return {
        #     'title': self.title.Text if self.title else "",
        #     'content': fix_sentences([text.Text for text in self.lines])
        # }

class Line():
    def __init__(self, page):
        self.Num=-1
        self.page=page
        self.spans=[]
        self.space_above=-1
        self.space_below=-1

    @property
    def x0(self):
        if len(self.spans):
            return self.spans[0].x0

    @property
    def x1(self):
        if len(self.spans):
            return self.spans[-1].x1

    @property
    def y0(self):
        if len(self.spans):
            return min(self.spans[0].y0, self.spans[-1].y0)

    @property
    def y1(self):
        if len(self.spans):
            return max(self.spans[0].y1, self.spans[-1].y1)


    @property
    def xpos(self):
        return (self.x1+self.x0)/2

    @property
    def ypos(self):
        return (self.y1+self.y0)/2

    @property
    def yposPage(self):
        return 1-(self.ypos/self.page.pdf_height)

    @property
    def Text(self):
        return '\t'.join(t.text for t in self.spans)
    @property
    def yposDoc(self):
        return self.Num+self.yposPage

    @property
    def page_number(self):
        return self.page.number

    def __eq__(self, other):
        return self.Text==other.Text

    def get_feauture(self):
        return {'Page': self.page_number,
                'x0': self.x0,
                'y0': self.y0,
                'x1': self.x1,
                'y1': self.y1,
                'Text': self.Text,
                'lineNumber': self.Num,
                'xpos': self.xpos,
                'ypos': self.ypos,
                'yposPage': self.yposPage,
                'yposDoc': self.yposDoc}