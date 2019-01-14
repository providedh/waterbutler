import io
import copy
from enum import Enum
# from waterbutler.providers.osfstorage
from .tei_p5_normalizator import Tei5Normalizator
from waterbutler.core.streams.base import BaseStream

import logging
logger = logging.getLogger(__name__)


class FileType(Enum):
    TEI_P5 = 1
    PREFIXED_TEI_P5 = 2
    TEI_P4 = 3
    PREFIXED_TEI_P4 = 4
    CSV = 5
    OTHER = 6


class TeiHandler(BaseStream):
    """Stream-like handler that recognizes TEI/CSV files and migrate them to TEI P5."""

    def __init__(self, file_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_path = file_path
        self.encoding = None
        self.text = io.StringIO()
        self.type = None
        self.error = None

    def _parse_encoding(self):
        encoding = 'utf-8'
        file = open(self.file_path, "r")
        # line = file.readline()
        # TODO read encoding from line: <?xml ... encoding="xxx" ... ?>
        file.close()
        return encoding

    def recognize(self):
        try:
            self.encoding = self._parse_encoding()
            file = open(self.file_path, "r", encoding=self.encoding)
            chunk = file.read()
            while chunk:
                self.text.write(chunk)
                chunk = file.read()
            file.close()
            self.text.seek(io.SEEK_SET)
        except Exception as exc:
            self.error = exc
            return FileType.OTHER
        # TODO file type recognition
        self.type = FileType.TEI_P5
        # self.type = FileType.PREFIXED_TEI_P5
        self.text.seek(io.SEEK_SET)
        if (self.type == FileType.PREFIXED_TEI_P5 or self.type == FileType.TEI_P4 or
                self.type == FileType.PREFIXED_TEI_P4 or self.type == FileType.CSV):
            return self.type, True
        else:
            return self.type, False

    def migrate(self):
        if self.type == FileType.TEI_P4:
            self.text
            # TODO delegate to specific class
        if self.type == FileType.CSV:
            self.text
            # TODO delegate to specific class
        # TEI P5 normalization (?)
        if self.type == FileType.PREFIXED_TEI_P5:
            old_text = copy.deepcopy(self.text)
            try:
                normalizator = Tei5Normalizator()
                xml_text_raw = self.text.getvalue()
                xml_text_normalized = normalizator.remove_default_tei5_namespace(xml_text_raw)
                self.text.truncate(0)
                self.text.seek(io.SEEK_SET)
                self.text.write(xml_text_normalized)

            except Exception as ex:
                print(ex)
                self.text = old_text

        self.text.seek(io.SEEK_SET)

    def close(self):
        self.text.close()

    async def read(self, size=-1):
        chunk = self.text.read(size)
        return bytes(chunk, self.encoding)

    async def _read(self, size):
        pass

    def size(self):
        pass

    def get_text(self):
        return self.text.getvalue()
