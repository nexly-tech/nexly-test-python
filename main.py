import asyncio
import argparse

from pipeline import Pipeline

async def main():
    # accept terminal parameters
    parser_terminal = argparse.ArgumentParser()
    parser_terminal.add_argument('--company_name')
    parser_terminal.add_argument('--date')
    args_terminal = parser_terminal.parse_args()

    params_terminal = {
        'company_name': args_terminal.company_name,
        'date': args_terminal.date,
    }

    path_pdf = "report.pdf"

    # create a Pipeline object
    pipeline = Pipeline(path_pdf, params_terminal)

    # start working Pipeline
    await pipeline.processing()


if __name__ == "__main__":
    asyncio.run(main())