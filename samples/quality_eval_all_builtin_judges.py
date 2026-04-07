import os

import rich
from azure.ai.evaluation import (
    AzureOpenAIModelConfiguration,
    CoherenceEvaluator,
    FluencyEvaluator,
    GroundednessEvaluator,
    RelevanceEvaluator,
    SimilarityEvaluator,
)
from dotenv import load_dotenv

# Setup the OpenAI client to use Azure OpenAI
load_dotenv(override=True)

model_config: AzureOpenAIModelConfiguration = {
    "azure_endpoint": os.environ["AZURE_AI_ENDPOINT"],
    "azure_deployment": os.environ["AZURE_AI_CHAT_DEPLOYMENT"],
}

context = 'Dining chair. Wooden seat. Four legs. Backrest. Brown. 18" wide, 20" deep, 35" tall. Holds 250 lbs.'
query = "Given the product specification for the Contoso Home Furnishings Dining Chair, provide an engaging marketing product description."
ground_truth = 'The dining chair is brown and wooden with four legs and a backrest. The dimensions are 18" wide, 20" deep, 35" tall. The dining chair has a weight capacity of 250 lbs.'
response = 'Introducing our timeless wooden dining chair, designed for both comfort and durability. Crafted with a solid wood seat and sturdy four-legged base, this chair offers reliable support for up to 250 lbs. The smooth brown finish adds a touch of rustic elegance, while the ergonomically shaped backrest ensures a comfortable dining experience. Measuring 18" wide, 20" deep, and 35" tall, it\'s the perfect blend of form and function, making it a versatile addition to any dining space. Elevate your home with this beautifully simple yet sophisticated seating option.'

groundedness_eval = GroundednessEvaluator(model_config, is_reasoning_model=True)
groundedness_score = groundedness_eval(
    response=response,
    context=context,
)
rich.print("Groundedness", groundedness_score)

relevance_eval = RelevanceEvaluator(model_config, is_reasoning_model=True)
relevance_score = relevance_eval(response=response, query=query)
rich.print("Relevance", relevance_score)

coherence_eval = CoherenceEvaluator(model_config, is_reasoning_model=True)
coherence_score = coherence_eval(response=response, query=query)
rich.print("Coherence", coherence_score)

fluency_eval = FluencyEvaluator(model_config, is_reasoning_model=True)
fluency_score = fluency_eval(response=response, query=query)
rich.print("Fluency", fluency_score)

similarity_eval = SimilarityEvaluator(model_config, is_reasoning_model=True)
similarity_score = similarity_eval(response=response, query=query, ground_truth=ground_truth)
rich.print("Similarity", similarity_score)
