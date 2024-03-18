#!/usr/bin/env python3
from openai import OpenAI

from constants import BASE_EMBEDDING_MODEL


openai_client = OpenAI()


def embed(text: str):
    response = openai_client.embeddings.create(
        model=BASE_EMBEDDING_MODEL, input=text, encoding_format="float"
    )
    return response.data[0].embedding
