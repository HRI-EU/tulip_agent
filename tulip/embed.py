#!/usr/bin/env python3
from openai import OpenAI


openai_client = OpenAI()


def embed(text: str):
    response = openai_client.embeddings.create(
      model="text-embedding-ada-002",
      input=text,
      encoding_format="float"
    )
    return response.data[0].embedding
