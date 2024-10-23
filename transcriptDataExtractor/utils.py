import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List
from concurrent.futures import ThreadPoolExecutor


class FinancialData(BaseModel):
    """
    BaseModel for structured financial data output.
    """

    assets: List[str] = Field(description="Assets")
    expenditures: List[str] = Field(description="Expenditures")
    income: List[str] = Field(description="Income")


def extract_with_timeout(transcript_path, timeout=10):
    """
    Extracts financial data from transcript file.
    Times out in case the request takes too long.
    """

    with ThreadPoolExecutor() as executor:
        future = executor.submit(extract_financial_data, transcript_path)

        result = future.result(timeout=timeout)
        return result


def extract_financial_data(transcript_path):
    """
    Extracts financial data from transcript file.
    """

    # Open the file.
    try:
        with open(transcript_path, 'r') as file:
            transcript_content = file.read()
    except FileNotFoundError:
        raise FileNotFoundError("Error: Transcript file not found.")

    # Get API key.
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        raise EnvironmentError("Error: OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")

    # Configure model version and creativity level (between 0 and 1).
    model = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4o", temperature=0)
    structured_llm = model.with_structured_output(FinancialData, method="json_mode")

    # Configure prompt.
    prompt_template = PromptTemplate(
        input_variables=["transcript"],
        template="""
        You are a financial assistant who is an expert in finance. You know all about financial planning, businesses, assets, liabilities, debts, funds, laws, etc.
        Extract financial details from the given transcript and categorize them into the following:

        1. **assets**: Extract all information with the actual figures, as sentences mentioning assets. Can include savings, funds, insurances or anything that could be considered a financial asset. Use your expert judgement.
        2. **expenditures**: Extract all information with the actual figures, as sentences mentioning expenditures, costs, regular spending or future expenditures. Use your expert judgement.
        3. **income**: Extract all information with the actual figures, as sentences mentioning income, salary, or earnings. Use your expert judgement.

        Be accurate and categorize appropriately. Check properly. Output the information as a list of facts or sentences under Assets, Expenditures, and Income.
        Use the 3rd person form of grammar.

        Transcript:
        {transcript}

        Respond in JSON with `assets`, `expenditures`, and `income` keys.
        """
    )
    prompt = prompt_template.format(transcript=transcript_content)

    try:
        extracted_data = structured_llm.invoke(prompt)
        return extracted_data
    except Exception as e:
        raise RuntimeError(f"Error invoking model: {e}")
