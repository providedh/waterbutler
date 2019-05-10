import re
import io
from lxml import etree as et

from waterbutler.core.streams import BaseStream
from waterbutler.providers.osfstorage.entities_extractor import EntitiesExtractor
from waterbutler.providers.osfstorage.tei import TeiHandler


class IDsFiller(BaseStream):
    _tags = ('person', 'place', 'org', 'event')
    _namespaces = {'tei': 'http://www.tei-c.org/ns/1.0', 'xml': 'http://www.w3.org/XML/1998/namespace'}

    def __init__(self, contents, filename, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._maxid = None
        if type(contents) is TeiHandler:
            self.__contents = contents.get_text()
            self.__message = contents.get_message()
        elif type(contents) is str:
            self.__contents = contents
            self.__message = ""

        self.text = io.StringIO()
        self._parsed = et.fromstring(bytes(self.__contents, 'utf-8'))
        filename = filename[:-4] if filename[-4:] == ".xml" else filename
        self.filename = filename.replace(' ', '_')

    def __fill_tags(self):
        grouped_tags = EntitiesExtractor.extract_entities_elements(self._parsed)

        modified = False

        for tag, elements in grouped_tags.items():
            for element in elements:
                if element.attrib.get("{{{}}}id".format(self._namespaces['xml'])) is None:
                    modified = True
                    self._maxid[tag] += 1
                    element.attrib['{{{}}}id'.format(self._namespaces['xml'])] = "{}{}-{}".format(tag, self.filename, self._maxid[tag])
        return modified

    def __find_max_ids(self):
        self._maxid = dict()
        for tag in self._tags:
            ids = re.findall('xml:id="{}{}-[0-9]+?"'.format(tag, self.filename), self.__contents)
            ids = [id.split('-')[-1][:-1] for id in ids]
            self._maxid[tag] = max(map(int, ids)) if ids else 0

    def process(self):
        self.__find_max_ids()
        if self.__fill_tags():
            self.text = io.StringIO(et.tostring(self._parsed, pretty_print=True, encoding='utf-8').decode('utf-8'))
            self.text.seek(io.SEEK_SET)
            self.__message += "Filled in missing ids of entities in file."
            return True
        else:
            self.text = io.StringIO(self.__contents)
            self.text.seek(io.SEEK_SET)
            return False  # no change needed

    def get_message(self):
        return self.__message

    def close(self):
        self.text.close()

    async def read(self, size=-1):
        chunk = self.text.read(size)

        return bytes(chunk, "utf-8")

    async def _read(self, size):
        pass

    def size(self):
        pass

    def get_text(self):
        return self.text.getvalue()
