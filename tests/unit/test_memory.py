import re
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import RunnableConfig

# --------- Fake LLM yang membaca history untuk menemukan nama ---------
class FakeMemoryModel(BaseChatModel):
    """Model palsu: jika history berisi 'nama saya <Nama>', lalu user bertanya 'Namaku siapa?'
    maka balas dengan nama yang ditemukan. Selain itu, balas kalimat default.
    """

    def _generate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        # Gabungkan seluruh content pesan agar kita bisa baca history
        text_history = []
        for m in messages:
            if isinstance(m, (HumanMessage, SystemMessage, AIMessage)):
                text_history.append(str(m.content))
            else:
                # fallback jika tipe message lain
                text_history.append(str(getattr(m, "content", "")))

        history = "\n".join(text_history)

        # Cari pola "nama saya <Nama>" / "nama saya adalah <Nama>"
        # Ambil kata setelah "nama saya" (sederhana untuk test)
        m = re.search(r"nama\s+saya(?:\s+adalah)?\s+([A-Za-zÀ-ÖØ-öø-ÿ]+)", history, flags=re.IGNORECASE)

        # Pertanyaan "namaku siapa"
        asked_name = re.search(r"namaku\s+siapa|nama\s+saya\s+siapa\??", history, flags=re.IGNORECASE)

        if m and asked_name:
            name = m.group(1)
            content = f"Namamu {name}."
        else:
            content = "Halo! Saya PrintAI. Ada yang bisa saya bantu terkait 3D printing?"

        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=content))])

    @property
    def _llm_type(self) -> str:
        return "fake-memory-model"

# --------- Test: agent ingat nama setelah beberapa percakapan ---------
def test_agent_remembers_user_name_across_invokes():
    model = FakeMemoryModel()
    checkpointer = InMemorySaver()

    # system prompt ringan; tidak mempengaruhi logika FakeMemoryModel
    system_prompt = (
        "You are PrintAI. Respond in Indonesian. "
        "Use memory across turns if available."
    )

    agent = create_agent(
        model,
        tools=[],                  # tidak perlu tools untuk test memori
        system_prompt=system_prompt,
        middleware=[],             # tanpa summarization; cukup memory
        checkpointer=checkpointer,
    )

    # Konfigurasi thread_id agar memory per user tersimpan
    config: RunnableConfig = {"configurable": {"thread_id": "test_user_001"}}

    # 1) User menyebut nama
    agent.invoke({"messages": "Halo, nama saya Dani"}, config)

    # 2) Percakapan lain (dummy)
    agent.invoke({"messages": "Saya mau print sesuatu"}, config)

    # 3) Tanyakan nama lagi — model harus menjawab 'Namamu Dani'
    final = agent.invoke({"messages": "Namaku siapa?"}, config)
    reply = final["messages"][-1].content

    assert "Namamu" in reply
    assert "Dani" in reply
