from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

class MyHTMLParser(HTMLParser):
    output = ""

    def handle_data(self, data):
        self.output += data

    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        self.output += c

    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        self.output += c

    def getoutput(self):
        return self.output
    def clearoutput(self):
        self.output = ""

parser = MyHTMLParser()
parser.feed("Although today's keynote rocked, for every great announcement, AT&amp;T shit on us just a little bit more.'")

print(parser.getoutput())
parser.clearoutput()

parser.feed('HATE safeway ffselect green tea ice cream! bought two cartons, what a waste of money. &gt;_&lt;')
print(parser.getoutput())
