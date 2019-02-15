import re


class ContentExtractor:
    @staticmethod
    def tei_contents_to_text(contents):
        contents = ' '.join(contents.split())
        match = re.findall("<text>.*?</text>", contents)
        if match:
            return ' '.join(re.sub("<.*?>", "", match[0]).split())
        else:
            return ""
