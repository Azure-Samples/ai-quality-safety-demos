import os
from pathlib import Path

import azure.identity
from azure.ai.evaluation import (
    AzureOpenAIModelConfiguration,
    GroundednessEvaluator,
    OpenAIModelConfiguration,
    RelevanceEvaluator,
    evaluate,
)
from dotenv import load_dotenv

# Setup the OpenAI client to use either Azure or GitHub Models
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST", "github")
azure_ai_project = None

if API_HOST == "azure":
    credential = azure.identity.DefaultAzureCredential()
    token_provider = azure.identity.get_bearer_token_provider(
        credential, "https://cognitiveservices.azure.com/.default"
    )
    model_config: AzureOpenAIModelConfiguration = {
        "azure_endpoint": os.environ["AZURE_AI_ENDPOINT"],
        "azure_deployment": os.environ["AZURE_AI_CHAT_DEPLOYMENT"],
    }
    AZURE_AI_FOUNDRY = os.getenv("AZURE_AI_FOUNDRY")
    AZURE_AI_PROJECT = os.getenv("AZURE_AI_PROJECT")
    AZURE_RESOURCE_GROUP = os.getenv("AZURE_RESOURCE_GROUP")
    AZURE_SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
    if AZURE_AI_PROJECT and AZURE_RESOURCE_GROUP and AZURE_SUBSCRIPTION_ID:
        azure_ai_project = {
            "subscription_id": AZURE_SUBSCRIPTION_ID,
            "resource_group_name": AZURE_RESOURCE_GROUP,
            "project_name": AZURE_AI_PROJECT,
        }
    azure_ai_project=f"https://{AZURE_AI_FOUNDRY}.services.ai.azure.com/api/projects/{AZURE_AI_PROJECT}"
elif API_HOST == "github":
    model_config: OpenAIModelConfiguration = {
        "type": "openai",
        "api_key": os.environ["GITHUB_TOKEN"],
        "base_url": "https://models.github.ai/inference",
        "model": os.getenv("GITHUB_MODEL", "openai/gpt-4o"),
    }

groundedness_eval = GroundednessEvaluator(model_config)

relevance_eval = RelevanceEvaluator(model_config)

script_dir = Path(__file__).parent
data_path = script_dir / "quality-eval-testdata.jsonl"

result = evaluate(
    data=data_path,
    evaluators={"relevance": relevance_eval, "groundedness": groundedness_eval},
    # column mapping
    evaluator_config={
        "default": {
            "query": "${data.query}",
            "response": "${data.response}",
            "context": "${data.context}",
        }
    },
    output_path=script_dir / "quality-eval-results.jsonl",
    azure_ai_project=azure_ai_project,
)
