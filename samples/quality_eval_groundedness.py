import os

import rich
from azure.ai.evaluation import (
    AzureOpenAIModelConfiguration,
    GroundednessEvaluator,
)
from dotenv import load_dotenv

# Setup the OpenAI client to use Azure OpenAI
load_dotenv(override=True)

model_config: AzureOpenAIModelConfiguration = {
    "azure_endpoint": os.environ["AZURE_AI_ENDPOINT"],
    "azure_deployment": os.environ["AZURE_AI_CHAT_DEPLOYMENT"],
}

query = "Given the product specification for the Contoso Home Furnishings Dining Chair, provide an engaging marketing product description."
context = 'Dining chair. Wooden seat. Four legs. Backrest. Brown. 18" wide, 20" deep, 35" tall. Holds 250 lbs.'
response = 'Introducing our timeless wooden dining chair, designed for both comfort and durability. Crafted with a solid teak seat and sturdy four-legged base, this chair offers reliable support for up to 250 lbs. The smooth brown finish adds a touch of rustic elegance, while the ergonomically shaped backrest ensures a comfortable dining experience. Measuring 18" wide, 20" deep, and 35" tall, it\'s the perfect blend of form and function, making it a versatile addition to any dining space. Elevate your home with this beautifully simple yet sophisticated seating option.'

groundedness_eval = GroundednessEvaluator(model_config, is_reasoning_model=True)
groundedness_score = groundedness_eval(
    query=query,
    context=context,
    response=response,
)
rich.print(groundedness_score)
