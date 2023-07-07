from io import TextIOWrapper
from xml.sax import parse
from xml.sax.handler import ContentHandler


class PageMaker(ContentHandler):
    passthrough = False

    def startElement(self, name: str, attrs: dict):
        super().startElement(name, attrs)
        if name == "page":
            self.passthrough = True
            self.out: TextIOWrapper = open(attrs["name"]+".html", "w")
            self.out.write('<html><head>\n')
            self.out.write('<title>{}</title>\n'.format(attrs['title']))
            self.out.write('</head><body>\n')
        elif self.passthrough:
            self.out.write(f'<{name}')
            for key, val in attrs.items():
                self.out.write(f' {key}={val}')
            self.out.write('>')

    def endElement(self, name):
        super().endElement(name)
        if name == "page":
            self.passthrough = False
            self.out.write('\n</body></html>\n')
            self.out.close()
        elif self.passthrough:
            self.out.write(f"</{name}>")

    def characters(self, content):
        super().characters(content)
        if self.passthrough:
            self.out.write(content)


parse("website.xml", PageMaker())