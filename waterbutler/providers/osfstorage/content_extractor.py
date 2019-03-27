import re
from lxml import etree as et


class ContentExtractor:
    namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}

    @classmethod
    def tei_contents_to_text(cls, contents):
        text = et.fromstring(bytes(contents, 'UTF-8')).find('tei:text', namespaces=cls.namespaces)
        if text:
            text = str(et.tostring(text), 'UTF-8')
            return ' '.join(re.sub("<.*?>", "", text).split())
        else:
            return ""
