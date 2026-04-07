# Demos de Calidad y Seguridad de IA

Este repositorio contiene una colección de scripts de Python que muestran cómo usar la API de OpenAI y el Azure AI Evaluation SDK para evaluar la calidad y seguridad de contenido generado por IA. Los scripts usan recursos de Microsoft Foundry configurados mediante variables de entorno. El script `safety_eval.py` también requiere un proyecto de Microsoft Foundry. Abajo hay más detalles.

## Scripts disponibles

Revisa el directorio `samples/spanish` para ver los scripts disponibles.

* [chat_error_contentfilter.py](samples/spanish/chat_error_contentfilter.py): Hace una llamada a la Responses API con el paquete de OpenAI usando un mensaje violento y maneja el error de seguridad de contenido en la respuesta.
* [chat_error_jailbreak.py](samples/spanish/chat_error_jailbreak.py): Hace una llamada a la Responses API con el paquete de OpenAI usando un intento de jailbreak y maneja el error de seguridad de contenido en la respuesta.
* [quality_eval_groundedness.py](samples/spanish/quality_eval_groundedness.py): Evalúa la fundamentación de una respuesta de muestra y fuentes usando el Azure AI Evaluation SDK.
* [quality_eval_all_builtin_judges.py](samples/spanish/quality_eval_all_builtin_judges.py): Evalúa la calidad de una consulta y respuesta de muestra usando todos los evaluadores basados en GPT integrados en el Azure AI Evaluation SDK.
* [quality_eval_custom.py](samples/spanish/quality_eval_custom.py): Evalúa la calidad de una consulta y respuesta de muestra con el Azure AI Evaluation SDK usando un evaluador personalizado para "amabilidad".
* [quality_eval_other_builtins.py](samples/spanish/quality_eval_other_builtins.py): Evalúa la calidad de una consulta y respuesta de muestra usando evaluadores no basados en GPT en el Azure AI Evaluation SDK (métricas de NLP como F1, BLEU, ROUGE, etc.).
* [quality_eval_bulk.py](samples/spanish/quality_eval_bulk.py): Evalúa la calidad de múltiples pares de consulta/respuesta usando el Azure AI Evaluation SDK.
* [safety_eval.py](samples/spanish/safety_eval.py): Evalúa la seguridad de una consulta y respuesta de muestra usando el Azure AI Evaluation SDK. Este script requiere un proyecto de Microsoft Foundry.

## Ejecutando los scripts

Primero aprovisiona los recursos de Microsoft Foundry para este repositorio y luego ejecuta los ejemplos con el archivo local `.env` generado y una identidad de Azure autenticada.

1. Instala las dependencias y activa tu entorno virtual.
2. Autentícate con Azure:

    ```shell
    azd auth login
    ```

3. Aprovisiona los recursos de Microsoft Foundry:

    ```shell
    azd provision
    ```

4. Confirma que `azd` haya creado un archivo local `.env` con valores como `AZURE_AI_ENDPOINT` y `AZURE_AI_CHAT_DEPLOYMENT`.
5. Ejecuta cualquier ejemplo del directorio `samples/spanish`, por ejemplo:

    ```shell
    python samples/spanish/quality_eval_all_builtin_judges.py
    ```

## Aprovisionando recursos de Microsoft Foundry

Este proyecto incluye infraestructura como código (IaC) para aprovisionar los recursos de Microsoft Foundry necesarios para ejecutar los scripts de evaluación de calidad y seguridad. La IaC está definida en el directorio `infra` y usa el Azure Developer CLI para aprovisionar los recursos.

1. Asegúrate de tener instalado el [Azure Developer CLI (azd)](https://aka.ms/install-azd).

2. Inicia sesión en Azure:

    ```shell
    azd auth login
    ```

    Para usuarios de GitHub Codespaces, si el comando anterior falla, intenta:

   ```shell
    azd auth login --use-device-code
    ```

3. Aprovisiona los recursos de Microsoft Foundry:

    ```shell
    azd provision
    ```

    Te pedirá que proporciones un nombre de entorno `azd` (como "ai-evals"), selecciones una suscripción de tu cuenta de Azure y selecciones una [ubicación donde los evaluadores de seguridad de Microsoft Foundry estén disponibles](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/evaluate-sdk#region-support). Luego aprovisionará los recursos en tu cuenta.

4. Una vez que los recursos estén aprovisionados, deberías ver un archivo local `.env` con todas las variables de entorno necesarias para ejecutar los scripts.
5. Para borrar los recursos, puedes usar el siguiente comando:

    ```shell
    azd down
    ```
