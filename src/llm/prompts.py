from langchain_core.prompts import ChatPromptTemplate

class Prompt:
  def __init__(self):
    self.prompt = ChatPromptTemplate.from_messages(
        [
          (
            "system",
            "You are a helpful assistant that translates {input_language} to {output_language}.",
          ),
          ("human", "{input}"),
        ]
  )
