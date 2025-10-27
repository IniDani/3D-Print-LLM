# __init__.py
from provider import LLMBot
from prompts import Prompt

# Initialize
llm_instance = LLMBot().llm
prompt_instance = Prompt().prompt

# Chain them together
chain = prompt_instance | llm_instance

# Run
result = chain.invoke(
    {
        "output_language": "German",
        "input": "I love programming.",
        "input_language": "English",
    }
)

print(result.content)  # result is an AIMessage object