from transformers import pipeline

PROMPT = """Identify the amount, Transaction Type (CREDIT/DEBIT), Vendor, Id of Vendor to which the amount is paied, and in case of credit from which the amount is recived and category of transaction like - Travel/Food/Tax/Fees. and return in JSON format. As given below:

{
    "amount" : amount,
    "tx_type" : CR/DR,
    "vendor" : vendor,
    "vendor_id" : vendor id,
    "expense category": category        
}"""


class HuggingFaceConnect:

    def __init__(self) -> None:
        self.generator = pipeline(
            "text2text-generation", model="google/flan-t5-base"
        )

    def get_analysis(self, text: str) -> dict:
        return self.generator(PROMPT + f"\n\nThe Email is Given Below:\n{text}")[0]['generated_text']
