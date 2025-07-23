import os

import azure.identity
import rich
from azure.ai.evaluation import (
    AzureOpenAIModelConfiguration,
    OpenAIModelConfiguration,
)
from dotenv import load_dotenv
from promptflow.client import load_flow

# Setup the OpenAI client to use either Azure or GitHub Models
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST", "github")

if API_HOST == "azure":
    credential = azure.identity.DefaultAzureCredential()
    token_provider = azure.identity.get_bearer_token_provider(
        credential, "https://cognitiveservices.azure.com/.default"
    )
    model_config: AzureOpenAIModelConfiguration = {
        "azure_endpoint": os.environ["AZURE_AI_ENDPOINT"],
        "azure_deployment": os.environ["AZURE_AI_CHAT_DEPLOYMENT"],
    }
elif API_HOST == "github":
    model_config: OpenAIModelConfiguration = {
        "type": "openai",
        "api_key": os.environ["GITHUB_TOKEN"],
        "base_url": "https://models.github.ai/inference",
        "model": os.getenv("GITHUB_MODEL", "gpt-4o"),
    }

query = "I've been on hold for 30 minutes just to ask about my luggage! This is ridiculous. Where is my bag?"
response = "I apologize for the long wait time, that must have been frustrating. I understand you're concerned about your luggage. Let me help you locate it right away. Could you please provide your bag tag number or flight details so I can track it for you?"

friendliness_eval = load_flow(source="friendliness.prompty", model={"configuration": model_config})
friendliness_score = friendliness_eval(query=query, response=response)
rich.print(f"Friendliness score: {friendliness_score}")
