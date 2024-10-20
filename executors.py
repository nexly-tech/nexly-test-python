
class ExecutorText:

    def __init__(self, extractor: object, validator: object, search_text: str):
        self.search_text = search_text
        self.extractor = extractor
        self.validator = validator

    async def start_executor(self):
        data_ex = await self.extractor.get_text()
        result = await self.validator.validate(self.search_text, data_ex)
        return result
