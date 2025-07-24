import os

import azure.identity
import rich
from azure.ai.evaluation import (
    AzureOpenAIModelConfiguration,
    GroundednessEvaluator,
    OpenAIModelConfiguration,
)
from dotenv import load_dotenv

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
        "model": os.getenv("GITHUB_MODEL", "openai/gpt-4o"),
    }

query = "Given the product specification for the Contoso Home Furnishings Dining Chair, provide an engaging marketing product description."
context = 'Dining chair. Wooden seat. Four legs. Backrest. Brown. 18" wide, 20" deep, 35" tall. Holds 250 lbs.'
response = 'Introducing our timeless wooden dining chair, designed for both comfort and durability. Crafted with a solid teak seat and sturdy four-legged base, this chair offers reliable support for up to 250 lbs. The smooth brown finish adds a touch of rustic elegance, while the ergonomically shaped backrest ensures a comfortable dining experience. Measuring 18" wide, 20" deep, and 35" tall, it\'s the perfect blend of form and function, making it a versatile addition to any dining space. Elevate your home with this beautifully simple yet sophisticated seating option.'

groundedness_eval = GroundednessEvaluator(model_config)
groundedness_score = groundedness_eval(
    query=query,
    context=context,
    response=response,
)
rich.print(groundedness_score)
