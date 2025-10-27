from langgraph.checkpoint.memory import MemorySaver
import uuid
from pprint import pprint

class ChatMemory:
    """
    Short-term memory for LLM Agent using LangGraph's MemorySaver.
    This stores and retrieves message history persistently.
    """

    def __init__(self):
        # Initialize a memory saver (like a persistent checkpoint)
        self.memory = MemorySaver()

    def _config(self, thread_id="default"):
        return {"configurable": {"thread_id": thread_id, "checkpoint_ns": "default"}}

    def load(self, thread_id="default"):
        config = {"configurable": {"thread_id": thread_id, "checkpoint_ns": "default"}}
        snapshot = self.memory.get(config)
        if not snapshot or "channel_values" not in snapshot:
            return []
        return snapshot["channel_values"].get("messages", [])


    def save(self, user_input, ai_output, thread_id="default"):
        config = {"configurable": {"thread_id": thread_id, "checkpoint_ns": "default"}}

        # Load existing messages
        messages = self.load(thread_id)
        messages.append({"role": "user", "content": user_input})
        messages.append({"role": "assistant", "content": ai_output})

        checkpoint = {
            "id": str(uuid.uuid4()),                   
            "channel_values": {"messages": messages},  
            "channel_versions": {},                     
            "pending_sends": [],
            "versions_seen": {},
        }

        # Save to memory
        self.memory.put(config, checkpoint, metadata={}, new_versions={})

    def print_memory(self, thread_id="default"):
        config = {"configurable": {"thread_id": thread_id, "checkpoint_ns": "default"}}
        snapshot = self.memory.get(config)

        if not snapshot or "channel_values" not in snapshot:
            print(f"[empty] No conversation found for thread '{thread_id}'")
            return

        messages = snapshot["channel_values"].get("messages", [])
        print(f"\nMemory for thread '{thread_id}':\n")
        for msg in messages:
            print(f"{msg['role'].capitalize()}: {msg['content']}")
