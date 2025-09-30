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
    output_path="quality-eval-results.jsonl",
)
