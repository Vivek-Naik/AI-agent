from langchain.agents import Tool
from datetime import datetime
import json

# -----------------------------
# 1. SaveToText Tool
# -----------------------------
def save_to_text(data: dict, filename: str = "output.txt") -> str:
    """
    Save the structured response (JSON) to a file with timestamp.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    formatted_text = f"---Research Output ({timestamp})---\n{json.dumps(data, indent=4)}\n\n"
    with open(filename, "a", encoding="utf-8") as file:
        file.write(formatted_text)
    return f"Data saved to {filename}"

save_tool = Tool(
    name="SaveToText",
    func=save_to_text,
    description="Use this tool to save the research output to a text file. Call only if user asks to save."
)

# -----------------------------
# 2. Search Tool
# -----------------------------
def search_function(query: str) -> str:
    # Placeholder function for web search
    return f"Search result for '{query}'"

search_tool = Tool(
    name="SearchTool",
    func=search_function,
    description="Use this tool to search the web for information."
)

# -----------------------------
# 3. Wikipedia Tool
# -----------------------------
def wiki_function(query: str) -> str:
    # Placeholder function for Wikipedia summaries
    return f"Wikipedia summary for '{query}'"

wiki_tool = Tool(
    name="WikiTool",
    func=wiki_function,
    description="Use this tool to get summaries from Wikipedia."
)
