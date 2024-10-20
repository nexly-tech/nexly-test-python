from validators import ValidateCompanyNameText, ValidateDateText
from extractors import ExtractorText
from executors import ExecutorText


class Pipeline:

    def __init__(self, path_pdf, params: dict):
        self.path_pdf = path_pdf
        self.params = params

    async def processing(self):
        company_name = self.params.get('company_name')
        date = self.params.get('date')

        extractor = ExtractorText(self.path_pdf, 'company_name', 1)
        validator = ValidateCompanyNameText()

        ex_company_name = ExecutorText(extractor, validator, company_name)
        result = await ex_company_name.start_executor()
        print(result)

        extractor = ExtractorText(self.path_pdf, 'date', 1)
        validator = ValidateDateText()

        ex_date = ExecutorText(extractor, validator, date)
        result = await ex_date.start_executor()
        print(result)

