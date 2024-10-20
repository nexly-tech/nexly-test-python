import unicodedata

# Для анализа и извлечения текста
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTChar, LTTextBoxHorizontal, LTRect, LTLine


class ExtractorText:
    """Class for extractors"""

    params = {
        'company_name': {
            'font': 'BCDFEE+Aptos-Bold',
            'size': 18.0,
        },
        'date': {
            'font': 'BCDHEE+Aptos',
            'size': 18.0,
        },
    }

    def __init__(self, path_pdf, type_extractor: str, max_pages: int = None):
        self.path_pdf = path_pdf
        self.max_pages = max_pages
        self.type_extractor = type_extractor
        self.param = ExtractorText.params.get(type_extractor, None)

    def __repr__(self):
        return self.__class__.__name__

    async def _get_pages(self):
        try:
            all_pages = tuple(
                value
                for index, value in enumerate(extract_pages(self.path_pdf, maxpages=self.max_pages))
            )
            return all_pages
        except Exception as e:
            print(e)

    async def _get_lines_text(self):
        try:
            pages = await self._get_pages()

            lines_text = []
            for page in pages:
                for line in page:
                    if isinstance(line, LTTextBoxHorizontal) and \
                        not isinstance(line, LTLine) and \
                        not isinstance(line, LTRect):
                        lines_text.append(line)

            return lines_text
        except Exception as e:
            print(e)

    async def get_text(self) -> list:
        lines_text = await self._get_lines_text()

        try:
            result = []
            for line in lines_text:
                for item in line:
                    for ch in item:
                        if isinstance(ch, LTChar):
                            if ch.size == self.param.get('size') and ch.fontname == self.param.get('font'):
                                text = unicodedata.normalize("NFC", line.get_text().strip())
                                result.append(text)
                                break
            if not result:
                print(f"ExtractorText: doesn't find {self.type_extractor}")
            return result
        except Exception as e:
            print(e)



# if isinstance(line, LTTextBoxHorizontal) and \
#                         not isinstance(line, LTLine) and \
#                         not isinstance(line, LTRect):