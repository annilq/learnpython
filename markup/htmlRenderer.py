from handler import *
import re

class HTMLRenderer(Handler):
    """
    用于渲染HTML的具体处理程序
    HTMLRenderer的方法可通过超类Handler的方法
    start()、end()和sub()来访问。这些方法实现了
    HTML文档使用的基本标记
    """
    def start_document(self):
      print('<html><head><title>...</title></head><body>')
    def end_document(self):
      print('</body></html>')
    def start_paragraph(self):
      print('<p>')
    def end_paragraph(self):
      print('</p>')
    def start_heading(self):
      print('<h2>')
    def end_heading(self):
      print('</h2>')
    def start_list(self):
      print('<ul>')
    def end_list(self):
      print('</ul>')
    def start_listitem(self):
      print('<li>')
    def end_listitem(self):
      print('</li>')
    def start_title(self):
      print('<h1>')
    def end_title(self):
      print('</h1>')
    def sub_emphasis(self, match):
      return '<em>{}</em>'.format(match.group(1))
    def sub_url(self, match):
      return '<a href="{}">{}</a>'.format(match.group(1), match.group(1))
    def sub_mail(self, match):
      return '<a href="mailto:{}">{}</a>'.format(match.group(1), match.group(1))
    def feed(self, data):
      print(data)