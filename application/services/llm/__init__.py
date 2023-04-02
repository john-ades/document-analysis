from typing import Union

import openai

from config import Config

openai.api_key = Config.openai_key()

"""
Completion vs Chat Completion
Completion:
    - Is more expensive than chat completion tasks
    - Can be fine tuned
Chat Completion:
    - Uses up to data models, less expensive
    - Cannot be fine tuned

"""
OPENAI_CHAT_COMPLETION_MODEL = "gpt-3.5-turbo"
OPENAI_COMPLETION_MODEL = "text-davinci-003"


def llm_completion(prompt: Union[str, list[str]]) -> list[str]:
    """
    Large Language Model Completion Task:
        Takes a text input and runs it through a large language model for a completion.
        The settings are set to parse through unstructured text data.
    """
    response = openai.Completion.create(
        model=OPENAI_COMPLETION_MODEL,
        prompt=prompt,
        temperature=0,
        max_tokens=1620,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return [choice.get('text').strip() for choice in response.get('choices')]
