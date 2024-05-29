from openai import OpenAI
from server import credentials
from prompt import SYSTEM_INSTRUCTIONS, QUERY_INSTRUCTIONS


class OpenAiConnect:
    def __init__(self) -> None:
        self.__client = OpenAI(
            api_key=credentials.get('auth').get('openai')['api_key']
        )

    def get_analysis(self, mail_text: str):
        response = self.__client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTIONS},
                {"role": "user", "content": QUERY_INSTRUCTIONS.format(
                    email=mail_text
                )}
            ]
        )

        return response.choices[0].message.content
