import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig

load_dotenv()
GROQ_KEY = os.getenv("GROQ_KEY")

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.1,
    max_tokens=1000,
    api_key=GROQ_KEY,
    timeout=30
)

system_prompt = """You are **PrintAI**, a friendly and professional AI customer service assistant 
          for a 3D printing business called **Fred's Print**.
          You help customers understand materials, print pricing, and geometry calculations.

          Follow this reasoning pattern internally (do NOT show to user):
          ---
          Thought: analyze the user's request and decide what data or tools are needed.
          Action: if needed, choose one tool and specify its parameters.
          Observation: summarize the result of the tool execution.
          Final Answer: provide a natural, helpful, and polite response.
          ---

          Rules:
          1. Always use metric units (cm, mm) unless the user specifies otherwise.
          2. If the customer asks for cost estimation, use: total_volume × 0.12 IDR per mm³.
          3. Respond in Indonesian unless the user writes in English.
          4. Be concise, polite, and clear.
          5. Never show Thought/Action/Observation — only return the Final Answer.
          """

checkpointer = InMemorySaver()

agent = create_agent(
    model, 
    tools=[], 
    system_prompt=system_prompt,
    middleware=[
        SummarizationMiddleware(
            model=model,
            max_tokens_before_summary=4000,
            messages_to_keep=20
        )
    ],
    checkpointer=checkpointer)

config: RunnableConfig = {"configurable": {"thread_id": "1"}}

agent.invoke({"messages": "halo nama saya fred"}, config)
agent.invoke({"messages": "saya ingin ngeprint casing HP dengan ukuran 15x7x1 cm"}, config)
agent.invoke({"messages": "bandingin harga kalau pake PLA vs ABS"}, config)
final_response = agent.invoke({"messages": "namaku siapa?"}, config)

final_response["messages"][-1].pretty_print()