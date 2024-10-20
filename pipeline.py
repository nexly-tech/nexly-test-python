from validators import ValidateCompanyNameText, ValidateDateText
from extractors import ExtractorText
from executors import ExecutorText


class Pipeline:

    def __init__(self, path_pdf, params: dict):
        self.path_pdf = path_pdf
        self.params = params

    async def processing(self):
        # accept terminal parameters
        company_name = self.params.get('company_name')
        date = self.params.get('date')

        # create an extractor object
        extractor = ExtractorText(self.path_pdf, 'company_name', 1)
        # create an validator object
        validator = ValidateCompanyNameText()

        """create an Executor object that will launch the extractor, 
        and then, based on the extracted data, transfer it to the validator"""
        ex_company_name = ExecutorText(extractor, validator, company_name)
        result = await ex_company_name.start_executor()
        print(result)


        #same steps, but for Date
        extractor = ExtractorText(self.path_pdf, 'date', 1)
        validator = ValidateDateText()

        ex_date = ExecutorText(extractor, validator, date)
        result = await ex_date.start_executor()
        print(result)

