import os

import azure.identity
import rich
from azure.ai.evaluation import (
    AzureOpenAIModelConfiguration,
    CoherenceEvaluator,
    FluencyEvaluator,
    GroundednessEvaluator,
    OpenAIModelConfiguration,
    RelevanceEvaluator,
    SimilarityEvaluator,
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

context = 'Silla de comedor. Asiento de madera. Cuatro patas. Respaldo. Marrón. 18" de ancho, 20" de profundidad, 35" de alto. Soporta 250 lbs.'
query = "Dada la especificación del producto para la Silla de Comedor de Contoso Home Furnishings, proporciona una descripción de marketing atractiva."
ground_truth = 'La silla de comedor es marrón y de madera con cuatro patas y un respaldo. Las dimensiones son 18" de ancho, 20" de profundidad, 35" de alto. La silla de comedor tiene una capacidad de peso de 250 lbs.'
response = 'Presentamos nuestra atemporal silla de comedor de madera, diseñada tanto para la comodidad como para la durabilidad. Fabricada con un asiento de teca maciza y una base robusta de cuatro patas, esta silla ofrece un soporte confiable de hasta 250 lbs. El acabado caoba liso añade un toque de elegancia rústica, mientras que el respaldo de forma ergonómica garantiza una experiencia de comedor cómoda. Con unas dimensiones de 18" de ancho, 20" de profundidad y 35" de alto, es la combinación perfecta de forma y función, convirtiéndola en una adición versátil a cualquier espacio de comedor. Eleva tu hogar con esta opción de asiento, bella en su sencillez pero sofisticada.'

groundedness_eval = GroundednessEvaluator(model_config)
groundedness_score = groundedness_eval(
    response=response,
    context=context,
)
rich.print("Fundamentación", groundedness_score)

relevance_eval = RelevanceEvaluator(model_config)
relevance_score = relevance_eval(response=response, query=query)
rich.print("Relevancia", relevance_score)

coherence_eval = CoherenceEvaluator(model_config)
coherence_score = coherence_eval(response=response, query=query)
rich.print("Coherencia", coherence_score)

fluency_eval = FluencyEvaluator(model_config)
fluency_score = fluency_eval(response=response, query=query)
rich.print("Fluidez", fluency_score)

similarity_eval = SimilarityEvaluator(model_config)
similarity_score = similarity_eval(response=response, query=query, ground_truth=ground_truth)
rich.print("Similitud", similarity_score)
