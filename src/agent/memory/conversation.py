from langchain.memory import ConversationBufferMemory

class ChatMemory:
    """
    Short-term memory sederhana untuk LLM Agent.
    Menyimpan percakapan penuh (user <-> assistant) dalam satu sesi.
    """

    def __init__(self):
        # key "chat_history" harus sama dengan yang digunakan di prompt
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    def load(self):
        """Ambil isi memori (riwayat percakapan)"""
        return self.memory.load_memory_variables({})["chat_history"]

    def save(self, user_input: str, ai_output: str):
        """Simpan percakapan baru ke memori"""
        self.memory.save_context({"input": user_input}, {"output": ai_output})

    def clear(self):
        """Hapus semua percakapan (reset sesi)"""
        self.memory.clear()