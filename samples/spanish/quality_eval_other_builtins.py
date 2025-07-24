import os

import azure.identity
import rich
from azure.ai.evaluation import (
    AzureOpenAIModelConfiguration,
    BleuScoreEvaluator,
    F1ScoreEvaluator,
    GleuScoreEvaluator,
    MeteorScoreEvaluator,
    OpenAIModelConfiguration,
    RougeScoreEvaluator,
    RougeType,
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

f1_eval = F1ScoreEvaluator()
f1_score = f1_eval(response=response, ground_truth=ground_truth)
rich.print(f1_score)

rouge_eval = RougeScoreEvaluator(rouge_type=RougeType.ROUGE_1)
rouge_score = rouge_eval(response=response, ground_truth=ground_truth)
rich.print(rouge_score)

bleu_eval = BleuScoreEvaluator()
bleu_score = bleu_eval(response=response, ground_truth=ground_truth)
rich.print(bleu_score)

meteor_eval = MeteorScoreEvaluator(alpha=0.9, beta=3.0, gamma=0.5)
meteor_score = meteor_eval(response=response, ground_truth=ground_truth)
rich.print(meteor_score)


gleu_eval = GleuScoreEvaluator()
gleu_score = gleu_eval(response=response, ground_truth=ground_truth)
rich.print(gleu_score)
