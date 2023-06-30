from htmlRenderer import HTMLRenderer

class Rule:
    type = ""

    def action(self, block: str, handler: HTMLRenderer):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True

    def condition(self, block):
        return True


class HeaddingRule(Rule):
    '''标题只包含一行'''
    type = "heading"

    def condition(self, block):
        return "\n" in block and len(block) < 70 and not block[-1] == ":"


class TitleRule(HeaddingRule):
    '''标题只包含一行'''
    type = "title"
    first = True

    def condition(self, block):
        if not self.first:
            return False
        self.first = True

        return super().condition(block)

class ListItemRule(Rule):
    '''列表项以连字符开始'''
    type='listitem'
    
    def condition(self, block):
        return block[0]=="-"
    def action(self, block: str, handler: HTMLRenderer):
        handler.start(self.type)
        handler.feed(block[1:].strip())
        handler.end(self.type)
        return True
        
class ListRule(ListItemRule):
    type="list"
    inside=False

    def condition(self, block):
        return True
    def action(self, block: str, handler: HTMLRenderer):
        if not self.inside and super().condition(block):
            handler.start(self.type)
            self.inside=True
        elif self.inside and not super().condition(block):
            handler.end(self.type)
            self.inside=False
        return False

class ParagraphRule(Rule):
    type="p"
            