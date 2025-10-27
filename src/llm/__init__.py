# __init__.py
from provider import LLMBot
from prompts import Prompt

# Initialize
llm_instance = LLMBot().llm
prompt_instance = Prompt()

# Chain them together
chain = prompt_instance.prompt | llm_instance

# Run
result = chain.invoke(
    {
        "user_name": prompt_instance.get_prompt(user_input="Halo saya mau print casing"),
        "current_date": prompt_instance.get_prompt(user_input="Halo saya mau print casing"),
        "chat_history": prompt_instance.get_prompt(user_input="Halo saya mau print casing"),
        "input": prompt_instance.get_prompt(user_input="Halo saya mau print casing")
    }
)

print(result.content)  # result is an AIMessage object