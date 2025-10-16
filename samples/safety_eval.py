import asyncio
import datetime
import logging
import os
import pathlib

import azure.identity
import requests
from azure.ai.evaluation.red_team import AttackStrategy, RedTeam, RiskCategory
from dotenv import load_dotenv
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.WARNING,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

load_dotenv(override=True)
if os.getenv("AZURE_AI_ENDPOINT") is None or os.getenv("AZURE_AI_FOUNDRY") is None:
    raise ValueError(
        "Some Azure environment variables are missing. This code requires Azure OpenAI endpoint and Azure AI Foundry project."
    )
credential = azure.identity.DefaultAzureCredential()


def callback(query: str):
    # send a POST request to an Azure OpenAI Chat completion endpoint
    azure_endpoint = os.environ["AZURE_AI_ENDPOINT"]
    azure_deployment = os.environ["AZURE_AI_CHAT_DEPLOYMENT"]
    endpoint = f"{azure_endpoint}/openai/deployments/{azure_deployment}/chat/completions?api-version=2024-03-01-preview"

    token_provider = azure.identity.get_bearer_token_provider(
        credential, "https://cognitiveservices.azure.com/.default"
    )
    token = token_provider()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    data = {
        "messages": [{"role": "user", "content": query}],
        "model": os.environ["AZURE_AI_CHAT_MODEL"],
        "temperature": 0,
    }
    response = requests.post(
        endpoint,
        headers=headers,
        json=data,
    )
    if response.status_code == 200:
        message = response.json().get("choices", [{}])[0].get("message", {})
        return message["content"]
    elif response.status_code == 400:
        error = response.json().get("error", {})
        if error["code"] == "content_filter":
            return "Assistant is unable to provide a response due to content filtering."
    return "Unable to provide a response due to other error. This response should score as a failure."


async def run_safety_eval():
    # Configure the Azure AI Foundry connection

    AZURE_AI_FOUNDRY = os.environ["AZURE_AI_FOUNDRY"]
    AZURE_AI_PROJECT = os.environ["AZURE_AI_PROJECT"]

    model_red_team = RedTeam(
        azure_ai_project=f"https://{AZURE_AI_FOUNDRY}.services.ai.azure.com/api/projects/{AZURE_AI_PROJECT}",
        credential=credential,
        risk_categories=[
            RiskCategory.Violence,
            RiskCategory.HateUnfairness,
            RiskCategory.Sexual,
            RiskCategory.SelfHarm,
        ],
        num_objectives=1,  # Questions per category
    )

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    scan_name = f"Safety evaluation {timestamp}"
    root_dir = pathlib.Path(__file__).parent

    await model_red_team.scan(
        scan_name=scan_name,
        output_path=f"{root_dir}/{scan_name}.json",
        attack_strategies=[
            AttackStrategy.Baseline,
            # Easy Complexity:
            AttackStrategy.Url,
            # Moderate Complexity:
            AttackStrategy.Tense,
            # Difficult Complexity:
            AttackStrategy.Compose([AttackStrategy.Tense, AttackStrategy.Url]),
        ],
        target=callback,
    )


if __name__ == "__main__":
    asyncio.run(run_safety_eval())
