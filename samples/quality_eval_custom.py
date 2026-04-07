import os
from pathlib import Path

import azure.identity
import openai
import prompty
import rich
from dotenv import load_dotenv

# Setup the OpenAI client to use Azure OpenAI
load_dotenv(override=True)

credential = azure.identity.DefaultAzureCredential()
token_provider = azure.identity.get_bearer_token_provider(
    credential, "https://cognitiveservices.azure.com/.default"
)
client = openai.OpenAI(
    base_url=os.environ["AZURE_AI_ENDPOINT"].rstrip("/") + "/openai/v1/",
    api_key=token_provider,
)
MODEL_NAME = os.environ["AZURE_AI_CHAT_DEPLOYMENT"]

query = "I've been on hold for 30 minutes just to ask about my luggage! This is ridiculous. Where is my bag?"
response = "I apologize for the long wait time, that must have been frustrating. I understand you're concerned about your luggage. Let me help you locate it right away. Could you please provide your bag tag number or flight details so I can track it for you?"


class FriendlinessEvaluator:
    def __init__(self, client):
        current_dir = Path(__file__).parent
        prompty_path = current_dir / "friendliness.prompty"
        self.prompt = prompty.load(prompty_path)
        self.client = client

    def __call__(self, *, response: str, **kwargs):
        messages = prompty.prepare(self.prompt, {"response": response})
        completion = self.client.responses.create(
            model=MODEL_NAME,
            temperature=0,
            max_output_tokens=1000,
            store=False,
            input=messages,
        )
        return completion.output_text


friendliness_eval = FriendlinessEvaluator(client)
friendliness_score = friendliness_eval(query=query, response=response)
rich.print(f"Friendliness score: {friendliness_score}")
