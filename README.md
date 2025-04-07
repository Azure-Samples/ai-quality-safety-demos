# AI Quality & Safety Demos

This repository contains a collection of Python scripts that demonstrate how to use the OpenAI API and Azure AI Evaluation SDK to evaluate the quality and safety of AI-generated content. Most of the scripts can be run for free with GitHub Models in GitHub Codespaces, but the safety_eval.py script requires an Azure AI Project. See below for more details.

## Available scripts

Check the `samples` directory for the available scripts.

* [chat_error_contentfilter.py](samples/chat_error_contentfilter.py): Makes a chat completion call with OpenAI package with a violent message and handles the content safety error in the response.
* [chat_error_jailbreak.py](samples/chat_error_jailbreak.py): Makes a chat completion call with OpenAI package with a jailbreak attempt and handles the content safety error in the response.
* [quality_eval_groundedness.py](samples/quality_eval_groundedness.py): Evaluates the groundedness of a sample answer and sources using the Azure AI Evaluation SDK.
* [quality_eval_all_builtin_judges.py](samples/quality_eval_all_builtin_judges.py): Evaluates the quality of a sample query and answer using all of the built-in GPT-based evaluators in the Azure AI Evaluation SDK.
* [quality_eval_custom.py](samples/quality_eval_custom.py): Evaluates the quality of a sample query and answer the Azure AI Evaluation SDK with a custom evaluator for "friendliness".
* [quality_eval_other_builtins.py](samples/quality_eval_other_builtins.py): Evaluates the quality of a sample query and answer using non-GPT-based evaluators in the Azure AI Evaluation SDK (NLP metrics like F1, BLEU, ROUGE, etc.).
* [quality_eval_bulk.py](samples/quality_eval_bulk.py): Evaluates the quality of multiple query/answer pairs using the Azure AI Evaluation SDK.
* [safety_eval.py](samples/safety_eval.py): Evaluates the safety of a sample query and answer using the Azure AI Evaluation SDK. This script requires an Azure AI Project.

## Configuring GitHub Models

If you open this repository in GitHub Codespaces, you can run the scripts for free using GitHub Models without any additional steps, as your `GITHUB_TOKEN` is already configured in the Codespaces environment.

If you want to run the scripts locally, you need to set up the `GITHUB_TOKEN` environment variable with a GitHub personal access token (PAT). You can create a PAT by following these steps:

1. Go to your GitHub account settings.
2. Click on "Developer settings" in the left sidebar.
3. Click on "Personal access tokens" in the left sidebar.
4. Click on "Tokens (classic)" or "Fine-grained tokens" depending on your preference.
5. Click on "Generate new token".
6. Give your token a name and select the scopes you want to grant. For this project, you don't need any specific scopes.
7. Click on "Generate token".
8. Copy the generated token.
9. Set the `GITHUB_TOKEN` environment variable in your terminal or IDE:

    ```shell
    export GITHUB_TOKEN=your_personal_access_token
    ```

## Provisioning Azure AI resources

This project includes infrastructure as code (IaC) to provision the Azure AI resources needed to run the quality and safety evaluation scripts. The IaC is defined in the `infra` directory and uses the Azure Developer CLI to provision the resources.

1. Make sure the [Azure Developer CLI (azd)](https://aka.ms/install-azd) is installed.

2. Login to Azure:

    ```shell
    azd auth login
    ```

    For GitHub Codespaces users, if the previous command fails, try:

   ```shell
    azd auth login --use-device-code
    ```

3. Provision the OpenAI account:

    ```shell
    azd provision
    ```

    It will prompt you to provide an `azd` environment name (like "ai-evals"), select a subscription from your Azure account, and select a [location where the Azure AI safety evaluators are available](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/evaluate-sdk#region-support). Then it will provision the resources in your account.

4. Once the resources are provisioned, you should now see a local `.env` file with all the environment variables needed to run the scripts.
5. To delete the resources, run:

    ```shell
    azd down
    ```
