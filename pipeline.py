import argparse
import asyncio
from datetime import datetime
import PyPDF2  # For reading the PDF file

# --- Extractor Classes ---
class CompanyNameExtractor:
    def __init__(self, pdf_path: str, expected_company_name: str):
        self.pdf_path = pdf_path
        self.expected_company_name = expected_company_name

    async def extract(self) -> dict:
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                cover_page = reader.pages[0]
                text = cover_page.extract_text()

                # Check if the expected company name is in the extracted text
                company_name = self._extract_company_name(text)
                return {"company_name": company_name}
        except Exception as e:
            raise ValueError(f"Failed to extract company name: {e}")

    def _extract_company_name(self, text: str) -> str:
        # Search for the exact company name in the text
        if self.expected_company_name in text:
            return self.expected_company_name
        raise ValueError(f"Expected company name '{self.expected_company_name}' not found on cover page")


class DateExtractor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    async def extract(self) -> dict:
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                cover_page = reader.pages[0]
                text = cover_page.extract_text()

                # Extract the date (assumes the date is on the first page)
                date = self._extract_date(text)
                return {"date": date}
        except Exception as e:
            raise ValueError(f"Failed to extract date: {e}")

    def _extract_date(self, text: str) -> str:
        # Example logic to extract date
        if "2023-12-31" in text:  # Replace with dynamic logic for any date
            return "2023-12-31"  # Example
        raise ValueError("Date not found on cover page")


# --- Validator Classes ---
class CompanyNameValidator:
    async def validate(self, data: dict, expected_company_name: str):
        extracted_company_name = data.get("company_name")
        if not extracted_company_name:
            raise ValueError("Company name was not extracted.")
        
        if extracted_company_name != expected_company_name:
            raise ValueError(f"Company name validation failed: expected '{expected_company_name}', found '{extracted_company_name}'.")
        
        print("Company name validation passed.")


class DateValidator:
    async def validate(self, data: dict, *, expected_date: str):
        extracted_date = data.get("date")
        if not extracted_date:
            raise ValueError("Date was not extracted.")
        
        # Validate the format of the extracted date
        try:
            datetime.strptime(extracted_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Date validation failed: '{extracted_date}' is not in the correct YYYY-MM-DD format.")
        
        if extracted_date != expected_date:
            raise ValueError(f"Date validation failed: expected '{expected_date}', found '{extracted_date}'.")
        
        print("Date validation passed.")


# --- Validation Pipeline ---
class ValidationPipeline:
    def __init__(self, extractors, validators):
        self.extractors = extractors
        self.validators = validators

    async def run(self, expected_company_name: str, expected_date: str):
        extracted_data = {}

        # Extract data from extractors
        extractor_tasks = [extractor.extract() for extractor in self.extractors]
        try:
            extractor_results = await asyncio.gather(*extractor_tasks)
            for result in extractor_results:
                extracted_data.update(result)
        except Exception as e:
            print(f"Error during extraction: {e}")
            return

        # Validate extracted data
        try:
            await self.validators[0].validate(extracted_data, expected_company_name=expected_company_name)
            await self.validators[1].validate(extracted_data, expected_date=expected_date)
        except Exception as e:
            print(f"Validation failed: {e}")
            return

        print("Validation completed successfully.")


# --- Main Script to Run the Pipeline ---
async def main():
    parser = argparse.ArgumentParser(description="Validate company name and date from PDF.")
    parser.add_argument('--company_name', required=True, help="Expected company name.")
    parser.add_argument('--date', required=True, help="Expected date in YYYY-MM-DD format.")
    parser.add_argument('--pdf_path', required=True, help="Path to the PDF file.")

    args = parser.parse_args()

    # Instantiate the extractors and validators
    extractors = [CompanyNameExtractor(args.pdf_path, args.company_name), DateExtractor(args.pdf_path)]
    validators = [CompanyNameValidator(), DateValidator()]

    # Run the validation pipeline
    pipeline = ValidationPipeline(extractors, validators)
    await pipeline.run(args.company_name, args.date)


if __name__ == "__main__":
    asyncio.run(main())
