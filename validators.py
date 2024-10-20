import unicodedata


class ValidateCompanyNameText:

    @staticmethod
    async def validate(search_text: str, data_extractor: list[str]):
        try:
            unicodedata.normalize("NFC", search_text)
            if search_text in data_extractor:
                return 'Company name validation passed.'
            else:
                return f'Company name validation failed: expected "{search_text}", found "{data_extractor}".'
        except Exception as e:
            print(e)


class ValidateDateText:
    @staticmethod
    async def validate(search_text: str, data_extractor: list[str]):
        try:
            unicodedata.normalize("NFC", search_text)

            if search_text in data_extractor:
                return 'Date validation passed.'
            else:
                return f'Date validation failed: expected "{search_text}", found "{data_extractor}".'
        except Exception as e:
            print(e)