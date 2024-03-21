#!/usr/bin/env python3
import logging

from openai import OpenAI

from constants import BASE_EMBEDDING_MODEL


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


openai_client = OpenAI()


def embed(text: str):
    response = openai_client.embeddings.create(
        model=BASE_EMBEDDING_MODEL, input=text, encoding_format="float"
    )
    logger.info(
        f"Usage for embedding in tokens: " f"{response.usage.prompt_tokens} prompt."
    )
    return response.data[0].embedding
