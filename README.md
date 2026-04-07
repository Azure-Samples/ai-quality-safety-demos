# AI Quality & Safety Demos

This repository contains a collection of Python scripts that demonstrate how to use the OpenAI API and Microsoft Foundry Evaluation SDK to evaluate the quality and safety of AI-generated content. The scripts use Microsoft Foundry resources configured through environment variables. The `safety_eval.py` script also requires a Microsoft Foundry project. See below for setup details.

## Available scripts

Check the `samples` directory for the available scripts.

* [chat_error_contentfilter.py](samples/chat_error_contentfilter.py): Makes a chat completion call with OpenAI package with a violent message and handles the content safety error in the response.
* [chat_error_jailbreak.py](samples/chat_error_jailbreak.py): Makes a chat completion call with OpenAI package with a jailbreak attempt and handles the content safety error in the response.
* [quality_eval_groundedness.py](samples/quality_eval_groundedness.py): Evaluates the groundedness of a sample answer and sources using the Microsoft Foundry Evaluation SDK.
* [quality_eval_all_builtin_judges.py](samples/quality_eval_all_builtin_judges.py): Evaluates the quality of a sample query and answer using all of the built-in GPT-based evaluators in the Microsoft Foundry Evaluation SDK.
* [quality_eval_custom.py](samples/quality_eval_custom.py): Evaluates the quality of a sample query and answer with the Microsoft Foundry Evaluation SDK using a custom evaluator for "friendliness".
* [quality_eval_other_builtins.py](samples/quality_eval_other_builtins.py): Evaluates the quality of a sample query and answer using non-GPT-based evaluators in the Microsoft Foundry Evaluation SDK (NLP metrics like F1, BLEU, ROUGE, etc.).
* [quality_eval_bulk.py](samples/quality_eval_bulk.py): Evaluates the quality of multiple query/answer pairs using the Microsoft Foundry Evaluation SDK.
* [safety_eval.py](samples/safety_eval.py): Evaluates the safety of a sample query and answer using the Microsoft Foundry Evaluation SDK. This script requires a Microsoft Foundry project.

## Running the scripts

Provision the Microsoft Foundry resources for this repo, then run the samples with the generated `.env` file and an authenticated Azure identity.

1. Install the dependencies and activate your virtual environment.
2. Authenticate with Azure:

    ```shell
    azd auth login
    ```

3. Provision the Microsoft Foundry resources:

    ```shell
    azd provision
    ```

4. Confirm that `azd` created a local `.env` file with values such as `AZURE_AI_ENDPOINT` and `AZURE_AI_CHAT_DEPLOYMENT`.
5. Run any sample from the `samples` directory, for example:

    ```shell
    python samples/quality_eval_all_builtin_judges.py
    ```

## Provisioning Microsoft Foundry resources

This project includes infrastructure as code (IaC) to provision the Microsoft Foundry resources needed to run the quality and safety evaluation scripts. The IaC is defined in the `infra` directory and uses the Azure Developer CLI to provision the resources.

1. Make sure the [Azure Developer CLI (azd)](https://aka.ms/install-azd) is installed.

2. Login to Azure:

    ```shell
    azd auth login
    ```

    For GitHub Codespaces users, if the previous command fails, try:

   ```shell
    azd auth login --use-device-code
    ```

3. Provision the Microsoft Foundry resources:

    ```shell
    azd provision
    ```

    It will prompt you to provide an `azd` environment name (like "ai-evals"), select a subscription from your Azure account, and select a [location where the Microsoft Foundry safety evaluators are available](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/evaluate-sdk#region-support). Then it will provision the resources in your account.

4. Once the resources are provisioned, you should now see a local `.env` file with all the environment variables needed to run the scripts.
5. To delete the resources, run:

    ```shell
    azd down
    ```
