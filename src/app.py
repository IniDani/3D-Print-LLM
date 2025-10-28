import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig

# Untuk tools
from tools import TOOLS

load_dotenv()
GROQ_KEY = os.getenv("GROQ_KEY")

model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.1,
    max_tokens=1000,
    api_key=GROQ_KEY,
    timeout=30
)

system_prompt = """You are **PrintAI**, a friendly and professional AI customer service assistant
                for a 3D printing business called **Fred's Print**.
                
                User will ask about a variety of things, including available services, basic 3D printing knowledge, and most importantly they want to print stuffs.

                Before deciding anything, identify user's context or intent first.  
                  
                Do NOT do the math in your head.

                Internal reasoning pattern (do NOT reveal):
                Thought → Action → Observation → Final Answer

                Rules:
                1) Always use metric units (cm, mm) unless the user specifies otherwise.
                2) Infer the needed parameters (radius, diameter, height, etc) from the user's messages.
                3) For any price estimation, you MUST call the tool `estimate_cost`.
                - First, obtain/compute volume in mm³:
                    • If the shape is provided → call `geometry_3d` to compute volume (convert cm→mm as needed).
                    • If shape/parameters are unclear (e.g., “vas” which can be hollow), assume the shape is ALWAYS solid,
                    and clarify to user that you can only infer solid mass cost calculation with certain infill percentage.
                - Then call `estimate_cost` to convert effective volume → mass (via material density) → price (Rp/gram).
                - Never estimate price with volume × rate directly.
                4) Prefer asking one concise clarifying question if geometry is ambiguous; otherwise proceed.
                5) Respond in Indonesian unless the user writes in English.
                6) Be concise, polite, and clear.
                """

checkpointer = InMemorySaver()

agent = create_agent(
    model, 
    tools=TOOLS, 
    system_prompt=system_prompt,
    middleware=[
        SummarizationMiddleware(
            model=model,
            max_tokens_before_summary=4000,
            messages_to_keep=20
        )
    ],
    checkpointer=checkpointer,
    )

config: RunnableConfig = {"configurable": {"thread_id": "1"}}

agent.invoke({"messages": "Halo nama saya Fawwaz"}, config)
agent.invoke({"messages": "Saya ingin ngeprint sebuah vas dengan radius 20 cm dan tinggi 10 cm"}, config)
agent.invoke({"messages": "Saya juga ingin buang air besar"}, config)
# agent.invoke({"messages": "Kalau hollow print belum bisa ya?"}, config)
final_response = agent.invoke({"messages": "Kalau hollow print belum bisa ya?"}, config)

final_final_response = final_response["messages"][-1]
print(final_final_response.content)