# Clear the contents of the .env file
Set-Content -Path .env -Value ""

# Append new values to the .env file
$azureAiChatDeployment = azd env get-value AZURE_AI_CHAT_DEPLOYMENT
$azureAiChatModel = azd env get-value AZURE_AI_CHAT_MODEL
$azureAiEndpoint = azd env get-value AZURE_AI_ENDPOINT
$azureAiFoundry = azd env get-value AZURE_AI_FOUNDRY
$azureAiProject = azd env get-value AZURE_AI_PROJECT
$azureSubscriptionId = azd env get-value AZURE_SUBSCRIPTION_ID
$azureResourceGroup = azd env get-value AZURE_RESOURCE_GROUP

Add-Conent -Path .env -Value "API_HOST=azure"
Add-Content -Path .env -Value "AZURE_AI_CHAT_DEPLOYMENT=$azureAiChatDeployment"
Add-Content -Path .env -Value "AZURE_AI_CHAT_MODEL=$azureAiChatModel"
Add-Content -Path .env -Value "AZURE_AI_ENDPOINT=$azureAiEndpoint"
Add-Content -Path .env -Value "AZURE_AI_FOUNDRY=$azureAiFoundry"
Add-Content -Path .env -Value "AZURE_AI_PROJECT=$azureAiProject"
Add-Content -Path .env -Value "AZURE_SUBSCRIPTION_ID=$azureSubscriptionId"
Add-Content -Path .env -Value "AZURE_RESOURCE_GROUP=$azureResourceGroup"
