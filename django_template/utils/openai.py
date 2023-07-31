import asyncio
from dataclasses import dataclass

import bs4
import openai
from openai.error import InvalidRequestError

MODEL_PRICINGS = {
    "gpt-3.5-turbo": {
        "prompt": 0.000002,
        "completion": 0.000002,
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


async def query_openai(
    messages: list[dict[str, str]],
    model: str | None = "gpt-3.5-turbo",
    temperature: float | None = 0.2,
    fallback_to_gpt4: bool = True,
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
            completion = await openai.ChatCompletion.acreate(
                **openai_completion_request
            )
            prompt_tokens = completion.usage.prompt_tokens
            completion_tokens = completion.usage.completion_tokens
            completion = completion.choices[0].message.content
            return PromptResult(
                model=model,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                completion=completion,
            )
        except InvalidRequestError as e:
            if (
                e.code == "context_length_exceeded"
                and model != "gpt-4"
                and fallback_to_gpt4
            ):
                model = "gpt-4"
            else:
                raise e
        except Exception as e:
            if tries >= max_tries:
                raise Exception(
                    f"Tried {max_tries} times but GPT prompt keeps failing, last error: {e}"
                )
            else:
                await asyncio.sleep(5 * tries)




