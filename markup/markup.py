import re
import sys

from htmlRenderer import HTMLRenderer

from handler import Handler

from rules import HeaddingRule, ListItemRule, ListRule, ParagraphRule, Rule, TitleRule

from util import blocks
from handler import Handler


class Parse:
    '''this is a main parse'''

    def __init__(self, handle: Handler) -> None:
        self.handler = handle
        self.rules: list[Rule] = []
        self.filters = []

    def addRule(self, rule):
        self.rules.append(rule)

    def addFilter(self, pattern, name):
        def filter(block: str, handler: Handler):
            return re.sub(pattern, handler.sub(name), block)
        self.filters.append(filter)

    def parse(self, file):
        self.handler.start("document")
        for block in blocks(file):
            for filter in self.filters:
                block = filter(block, self.handler)
            for rule in self.rules:
                if rule.condition(block):
                    last = rule.action(block, self.handler)
                    if last:
                        break
        self.handler.end("document")

class BasicTextParser(Parse):

    def __init__(self, handle: Handler) -> None:
        super().__init__(handle)
        self.rules.append(ListRule())
        self.rules.append(ListItemRule())
        self.rules.append(TitleRule())
        self.rules.append(HeaddingRule())
        self.rules.append(ParagraphRule())
        self.addFilter(r'\*(.+?)\*', 'emphasis')
        self.addFilter(r'(http://[\.a-zA-Z/]+)', 'url')
        self.addFilter(r'([\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z]+)', 'mail')

handler = HTMLRenderer()
parser = BasicTextParser(handler)
parser.parse(sys.stdin)
