from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

class LLM():
    def __init__(self):
        self.openai = OpenAI(api_key='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')
        self.session = None

    def send_message(self, prompt, model = 'gpt-4o-mini') -> str:
        completion = self.openai.chat.completions.create(
        model=model,
        messages=[
                {"role": "system", "content": prompt},
            ],
        response_format={"type": "json_object"}
        )

        response = completion.choices[0].message.content

        return response
    
    def send_message_for_code(self, prompt, model = 'gpt-4o-mini') -> str:
        completion = self.openai.chat.completions.create(
        model=model,
        messages=[
                {"role": "system", "content": prompt},
            ],
        response_format={"type": "text"}
        )

        response = completion.choices[0].message.content

        return response
    
    def generate_embedding(self, data):
        embd = self.openai.embeddings.create(
            model="text-embedding-3-small",
            input="The food was delicious and the waiter...",
            encoding_format="float"
            )
        return embd.data[0].embedding