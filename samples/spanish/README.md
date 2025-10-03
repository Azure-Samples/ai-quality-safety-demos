# Demos de Calidad y Seguridad de IA

Este repositorio contiene una colección de scripts de Python que muestran cómo usar la API de OpenAI y el Azure AI Evaluation SDK para evaluar la calidad y seguridad de contenido generado por IA. La mayoría de los scripts se pueden ejecutar gratis con GitHub Models en GitHub Codespaces, pero el script `safety_eval.py` requiere un Proyecto de Azure AI. Abajo hay más detalles.

## Scripts disponibles

Revisa el directorio `samples/spanish` para ver los scripts disponibles.

* [chat_error_contentfilter.py](samples/spanish/chat_error_contentfilter.py): Hace una llamada de chat completion con el paquete de OpenAI con un mensaje violento y maneja el error de seguridad de contenido en la respuesta.
* [chat_error_jailbreak.py](samples/spanish/chat_error_jailbreak.py): Hace una llamada de chat completion con el paquete de OpenAI con un intento de jailbreak y maneja el error de seguridad de contenido en la respuesta.
* [quality_eval_groundedness.py](samples/spanish/quality_eval_groundedness.py): Evalúa la fundamentación de una respuesta de muestra y fuentes usando el Azure AI Evaluation SDK.
* [quality_eval_all_builtin_judges.py](samples/spanish/quality_eval_all_builtin_judges.py): Evalúa la calidad de una consulta y respuesta de muestra usando todos los evaluadores basados en GPT integrados en el Azure AI Evaluation SDK.
* [quality_eval_custom.py](samples/spanish/quality_eval_custom.py): Evalúa la calidad de una consulta y respuesta de muestra con el Azure AI Evaluation SDK con un evaluador personalizado para "amabilidad".
* [quality_eval_other_builtins.py](samples/spanish/quality_eval_other_builtins.py): Evalúa la calidad de una consulta y respuesta de muestra usando evaluadores no basados en GPT en el Azure AI Evaluation SDK (métricas de NLP como F1, BLEU, ROUGE, etc.).
* [quality_eval_bulk.py](samples/spanish/quality_eval_bulk.py): Evalúa la calidad de múltiples pares de consulta/respuesta usando el Azure AI Evaluation SDK.
* [safety_eval.py](samples/spanish/safety_eval.py): Evalúa la seguridad de una consulta y respuesta de muestra usando el Azure AI Evaluation SDK. Este script requiere un Azure AI Project.

## Configurando GitHub Models

Si abres este repositorio en GitHub Codespaces, puedes ejecutar los scripts gratis usando GitHub Models sin pasos adicionales, ya que tu `GITHUB_TOKEN` ya está configurado en el entorno de Codespaces.

Si quieres ejecutar los scripts localmente, necesitas configurar la variable de entorno `GITHUB_TOKEN` con un token de acceso personal (PAT) de GitHub. Puedes crear un PAT siguiendo estos pasos:

1. Ve a la configuración de tu cuenta de GitHub.
2. Haz clic en "Developer settings" en la barra lateral izquierda.
3. Haz clic en "Personal access tokens" en la barra lateral izquierda.
4. Haz clic en "Tokens (classic)" o "Fine-grained tokens" según tu preferencia.
5. Haz clic en "Generate new token".
6. Dale un nombre a tu token y selecciona los permisos que quieras otorgar. Para este proyecto, no necesitas permisos específicos.
7. Haz clic en "Generate token".
8. Copia el token generado.
9. Configura la variable de entorno `GITHUB_TOKEN` en tu terminal o IDE:

    ```shell
    export GITHUB_TOKEN=tu_token_de_acceso_personal
    ```

## Aprovisionando recursos de Azure AI

Este proyecto incluye infraestructura como código (IaC) para aprovisionar los recursos de Azure AI necesarios para ejecutar los scripts de evaluación de calidad y seguridad. La IaC está definida en el directorio `infra` y usa el Azure Developer CLI para aprovisionar los recursos.

1. Asegúrate de tener instalado el [Azure Developer CLI (azd)](https://aka.ms/install-azd).

2. Inicia sesión en Azure:

    ```shell
    azd auth login
    ```

    Para usuarios de GitHub Codespaces, si el comando anterior falla, intenta:

   ```shell
    azd auth login --use-device-code
    ```

3. Aprovisiona la cuenta de OpenAI:

    ```shell
    azd provision
    ```

    Te pedirá que proporciones un nombre de entorno `azd` (como "ai-evals"), selecciones una suscripción de tu cuenta de Azure y selecciones una [ubicación donde los evaluadores de seguridad de Azure AI estén disponibles](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/evaluate-sdk#region-support). Luego aprovisionará los recursos en tu cuenta.

4. Una vez que los recursos estén aprovisionados, deberías ver un archivo local `.env` con todas las variables de entorno necesarias para ejecutar los scripts.
5. Para borrar los recursos, puedes usar el siguiente comando:

    ```shell
    azd down
    ```
