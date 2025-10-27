import os
from langchain_ollama import ChatOllama

class LLMBot:
    def __init__(self):
        self.llm = ChatOllama(
            model="llama3.2",
            temperature=0
        )