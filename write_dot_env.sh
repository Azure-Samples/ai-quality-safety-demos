#!/bin/bash

# Clear the contents of the .env file
> .env

# Append new values to the .env file
echo "API_HOST=azure" >> .env
echo "AZURE_AI_CHAT_DEPLOYMENT=$(azd env get-value AZURE_AI_CHAT_DEPLOYMENT)" >> .env
echo "AZURE_AI_CHAT_MODEL=$(azd env get-value AZURE_AI_CHAT_MODEL)" >> .env
echo "AZURE_AI_ENDPOINT=$(azd env get-value AZURE_AI_ENDPOINT)" >> .env
echo "AZURE_AI_FOUNDRY=$(azd env get-value AZURE_AI_FOUNDRY)" >> .env
echo "AZURE_AI_PROJECT=$(azd env get-value AZURE_AI_PROJECT)" >> .env
echo "AZURE_SUBSCRIPTION_ID=$(azd env get-value AZURE_SUBSCRIPTION_ID)" >> .env
echo "AZURE_RESOURCE_GROUP=$(azd env get-value AZURE_RESOURCE_GROUP)" >> .env
