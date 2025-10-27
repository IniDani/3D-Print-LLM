from llm.provider import LLMBot
from llm.prompts import Prompt
from agent.memory.conversation import ChatMemory

# Initialize
llm_instance = LLMBot().llm
prompt_instance = Prompt()
memory = ChatMemory()


def chat_once(user_input: str, thread_id="default"):
    # Load chat history
    chat_history = memory.load(thread_id)
    print(chat_history)

    # Format prompt using previous messages
    formatted_prompt = prompt_instance.get_prompt(
        user_name="fred",
        chat_history=chat_history,
        user_input=user_input
    )

    # Call the LLM
    result = llm_instance.invoke(formatted_prompt)

    # Save conversation to memory
    memory.save(user_input, result.content, thread_id)

    # Print results
    print(f"\nUser: {user_input}")
    print(f"PrintAI: {result.content}\n")

    # Print memory
    memory.print_memory(thread_id)

# Example usage
chat_once("Halo, saya mau print casing HP ukuran 15x7x1 cm.")
chat_once("Bahannya bagus pakai PLA atau ABS?")
chat_once("Kalau saya mau hitung volume casing itu berapa?")
