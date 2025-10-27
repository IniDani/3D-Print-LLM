from provider import LLMBot
from prompts import Prompt
from agent.memory.conversation import ChatMemory

# Initialize
llm_instance = LLMBot().llm
prompt_instance = Prompt()
memory = ChatMemory()

# Simulasi percakapan 2 kali
def chat_once(user_input: str):
    # Ambil history lama
    chat_history = memory.load()

    # Format prompt baru dengan history
    formatted_prompt = prompt_instance.get_prompt(
        user_name="Dani",
        chat_history=chat_history,
        user_input=user_input
    )

    # Jalankan LLM
    chain = prompt_instance.prompt | llm_instance
    result = chain.invoke({
        "current_date": "27 October 2025",
        "user_name": "Dani",
        "chat_history": chat_history,
        "input": user_input
    })

    # Simpan hasil ke memori
    memory.save(user_input, result.content)

    print(f"🧍 User: {user_input}")
    print(f"🤖 PrintAI: {result.content}\n")

# Jalankan simulasi
chat_once("Halo, saya mau print casing HP ukuran 15x7x1 cm.")
chat_once("Bahannya bagus pakai PLA atau ABS?")
chat_once("Oh, kalau saya mau hitung volume casing itu berapa?")