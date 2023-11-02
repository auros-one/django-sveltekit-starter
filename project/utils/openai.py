import asyncio
import logging
import time
from dataclasses import dataclass

import openai
from django.conf import settings
from openai.error import InvalidRequestError

MODEL_PRICINGS = {
    "gpt-3.5-turbo": {
        "prompt": 0.0000015,
        "completion": 0.000002,
    },
    "gpt-3.5-turbo-16k": {
        "prompt": 0.000003,
        "completion": 0.000004,
    },
    "gpt-4": {
        "prompt": 0.00003,
        "completion": 0.00006,
    },
}


@dataclass
class PromptResult:
    model: str
    prompt_tokens: int
    completion_tokens: int
    completion: str

    @property
    def cost(self) -> float:
        prompt_pricing = self.prompt_tokens * MODEL_PRICINGS[self.model]["prompt"]
        completion_pricing = (
            self.completion_tokens * MODEL_PRICINGS[self.model]["completion"]
        )
        return prompt_pricing + completion_pricing


async def aquery_openai(
    messages: list[dict[str, str]],
    model: str | None = "gpt-3.5-turbo",
    temperature: float | None = 0.2,
    fallback_to_16k: bool = True,
    max_tries: int = 5,
) -> PromptResult:
    """
    Query OpenAI's API with the given messages and model.
    """
    if model is None:
        model = "gpt-3.5-turbo"

    tries = 0
    while True:
        tries += 1
        try:
            openai_completion_request = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
            }
            if HELICONE_API_KEY := settings.HELICONE_API_KEY:
                openai_completion_request["headers"] = {
                    "Helicone-Auth": f"Bearer {HELICONE_API_KEY}",
                }
            completion = await openai.ChatCompletion.acreate(
                **openai_completion_request
            )
            prompt_tokens = completion.usage.prompt_tokens  # type: ignore
            completion_tokens = completion.usage.completion_tokens  # type: ignore
            completion = completion.choices[0].message.content  # type: ignore
            return PromptResult(
                model=model,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                completion=completion,
            )
        except InvalidRequestError as e:
            if (
                e.code == "context_length_exceeded"
                and model != "gpt-3.5-turbo-16k"
                and fallback_to_16k
            ):
                print(
                    "WARNING: GPT-3 context length exceeded, falling back to GPT-3-16k"
                )
                logging.warning(
                    f"GPT-3 context length exceeded, falling back to GPT-3-16k, error: {e}"
                )
                model = "gpt-3.5-turbo-16k"
            else:
                raise e
        except Exception as e:
            if tries >= max_tries:
                raise Exception(
                    f"Tried {max_tries} times but GPT prompt keeps failing, last error: {e}"
                )
            else:
                print(f"Error: {e}, trying again in {1 * tries} seconds")
                logging.error(f"Error: {e}, trying again in {1 * tries} seconds")
                await asyncio.sleep(1 * tries)


def query_openai(
    messages: list[dict[str, str]],
    model: str | None = "gpt-3.5-turbo",
    temperature: float | None = 0.2,
    fallback_to_16k: bool = True,
    max_tries: int = 5,
) -> PromptResult:
    """
    Query OpenAI's API with the given messages and model.
    """
    if model is None:
        model = "gpt-3.5-turbo"

    tries = 0
    while True:
        tries += 1
        try:
            openai_completion_request = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
            }
            if HELICONE_API_KEY := settings.HELICONE_API_KEY:
                openai_completion_request["headers"] = {
                    "Helicone-Auth": f"Bearer {HELICONE_API_KEY}",
                }
            completion = openai.ChatCompletion.create(**openai_completion_request)
            prompt_tokens = completion.usage.prompt_tokens  # type: ignore
            completion_tokens = completion.usage.completion_tokens  # type: ignore
            completion = completion.choices[0].message.content  # type: ignore
            return PromptResult(
                model=model,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                completion=completion,
            )
        except InvalidRequestError as e:
            if (
                e.code == "context_length_exceeded"
                and model != "gpt-3.5-turbo-16k"
                and fallback_to_16k
            ):
                print(
                    "WARNING: GPT-3 context length exceeded, falling back to GPT-3-16k"
                )
                logging.warning(
                    f"GPT-3 context length exceeded, falling back to GPT-3-16k, error: {e}"
                )
                model = "gpt-3.5-turbo-16k"
            else:
                raise e
        except Exception as e:
            if tries >= max_tries:
                raise Exception(
                    f"Tried {max_tries} times but GPT prompt keeps failing, last error: {e}"
                )
            else:
                print(f"Error: {e}, trying again in {1 * tries} seconds")
                logging.error(f"Error: {e}, trying again in {1 * tries} seconds")
                time.sleep(1 * tries)
