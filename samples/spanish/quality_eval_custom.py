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

query = "¡He estado en espera por 30 minutos solo para preguntar por mi equipaje! Esto es ridículo. ¿Dónde está mi maleta?"
response = "Lamento mucho la larga espera, debe haber sido frustrante. Entiendo que estés preocupado por tu equipaje. Déjame ayudarte a localizarlo de inmediato. ¿Podrías proporcionarme el número de etiqueta de tu maleta o los detalles de tu vuelo para poder rastrearlo?"

friendliness_eval = load_flow(source="friendliness.prompty", model={"configuration": model_config})
friendliness_score = friendliness_eval(query=query, response=response)
rich.print(f"Friendliness score: {friendliness_score}")
