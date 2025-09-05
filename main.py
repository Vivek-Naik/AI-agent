from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from tools import search_tool, wiki_tool, save_tool
import os

# -----------------------------
# 1. Load API key
# -----------------------------
load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")

# -----------------------------
# 2. Initialize LLM
# -----------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=gemini_api_key
)

# -----------------------------
# 3. Define structured response schema
# -----------------------------
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    source: list[str]
    tools_used: list[str]

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# -----------------------------
# 4. Create prompt template
# -----------------------------
prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a research assistant that helps the user generate research papers.
You have access to these tools:
1. SearchTool: use this to search the web.
2. WikiTool: use this to get Wikipedia summaries.
3. SaveToText: use this to save the research output to a file.

IMPORTANT:
- Only use SaveToText if the user explicitly asks to "save to file".
- Output **must** be strictly valid JSON matching this format:
{format_instructions}
Do not add any extra text, explanation, or commentary outside of JSON.
    """),
    ("placeholder", "{chat_history}"),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}")
]).partial(format_instructions=parser.get_format_instructions())

# -----------------------------
# 5. Tools
# -----------------------------
tools = [search_tool, wiki_tool, save_tool]

# -----------------------------
# 6. Memory
# -----------------------------
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# -----------------------------
# 7. Create agent and executor
# -----------------------------
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)

# -----------------------------
# 8. Run chatbot loop
# -----------------------------
print("💡 Type 'exit' or 'quit' to stop the chatbot.\n")

while True:
    query = input("Enter your research query: ")

    if query.lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break

    raw_response = agent_executor.invoke({"query": query})

    try:
        structured_response = parser.parse(raw_response["output"])
        print("\n✅ Structured Response:")
        print(f"Topic: {structured_response.topic}")
        print(f"Summary: {structured_response.summary}")
        print(f"Source: {structured_response.source}")
        print(f"Tools Used: {structured_response.tools_used}\n")

        # Save to file only if user asked for it
        if "save to file" in query.lower():
            save_tool.func({
                "topic": structured_response.topic,
                "summary": structured_response.summary,
                "source": structured_response.source,
                "tools_used": structured_response.tools_used
            })
            print("💾 Saved output to file.\n")

    except Exception as e:
        print(f"❌ Error parsing response: {e}")
        print("Raw output:", raw_response["output"])
