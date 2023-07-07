from io import TextIOWrapper
from xml.sax import ContentHandler, parse
import os


class Dispatcher:
    def dispatch(self, prefix: str, name: str, attrs=None):
        mname = prefix+name.capitalize()
        dname = 'default'+prefix.capitalize()
        method = getattr(self, mname, None)
        if callable(method):
            args = ()
        else:
            method = getattr(self, dname, None)
            args = name,
        if prefix == "start":
            args += attrs,
        if callable(method):
            method(*args)

    def startElement(self, name, attrs):
        self.dispatch("start", name, attrs)

    def endElement(self, name):
        self.dispatch('end', name)


class WebsiteConstructor(Dispatcher, ContentHandler):
    passthrough = False
    out: TextIOWrapper

    def __init__(self, directory) -> None:
        super().__init__()
        self.directory = [directory]
        self.ensureDirectory()

    def ensureDirectory(self):
        path = os.path.join(*self.directory)
        os.makedirs(path, exist_ok=True)

    def characters(self, content):
        super().characters(content)
        if self.passthrough:
            self.out.write(content)

    def defaultStart(self, name, attrs: dict):
        if self.passthrough:
            self.out.write("<"+name)
            for key, val in attrs.items():
                self.out.write(f' {key}={val}')
            self.out.write(">")

    def defaultEnd(self, name):
        if self.passthrough:
            self.out.write(f"</{name}>")

    def endDirectory(self):
        self.directory.pop()

    def startPage(self, attrs):
        filename = os.path.join(*self.directory+[attrs['name']+'.html'])
        self.out = open(filename, 'w')
        self.writeHeader(attrs["title"])
        self.passthrough = True

    def endPage(self):
        self.passthrough = False
        self.writeFooter()
        self.out.close()

    def writeHeader(self, title):
        self.out.write('<html>\n <head>\n   <title>')
        self.out.write(title)
        self.out.write('</title>\n </head>\n <body>\n')

    def writeFooter(self):
        self.out.write('\n </body>\n</html>\n')

# class WebsiteConstructor(Dispatcher, ContentHandler):


#     def endPage(self):
#         self.passthrough = False
#         self.writeFooter()
#         self.out.close()


parse('website.xml', WebsiteConstructor('public_html'))
