import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass  # Chạy trong IDLE — bỏ qua, không cần reconfigure

import warnings
warnings.filterwarnings("ignore")  # Ẩn các cảnh báo tương thích của thư viện trên Python 3.14+

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, BaseMessage
from tools import search_flights, search_hotels, calculate_budget, get_weather, search_activities
from dotenv import load_dotenv

load_dotenv()

# 1. Đọc System Prompt
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Khởi tạo LLM và Tools
tools_list = [search_flights, search_hotels, calculate_budget, get_weather, search_activities]
llm = ChatAnthropic(model="claude-sonnet-4-5")
llm_with_tools = llm.bind_tools(tools_list)

# 4. Agent Node — LLM quyết định gọi tool nào, bao nhiêu lần
def agent_node(state: AgentState) -> dict:
    messages: list[BaseMessage] = state["messages"]

    # Đảm bảo System Prompt luôn ở đầu conversation
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = llm_with_tools.invoke(messages)

    # === LOGGING — in rõ agent đang làm gì ===
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"  [TOOL CALL] {tc['name']}({tc['args']})")
    else:
        print("  [DIRECT REPLY] Agent trả lời trực tiếp không qua tool.")

    return {"messages": [response]}

# 5. Xây dựng Graph
builder = StateGraph(AgentState)

# Thêm nodes
builder.add_node("agent", agent_node)

tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

# Khai báo edges
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)   # agent -> tools hoặc END
builder.add_edge("tools", "agent")                         # tools -> agent (loop)

graph = builder.compile()

# 6. Chat loop
if __name__ == "__main__":
    print("=" * 60)
    print("TravelBuddy — Tro ly Du lich Thong minh")
    print("   Go 'quit' de thoat")
    print("=" * 60)

    while True:
        user_input = input("\nBan: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("Tam biet! Chuc ban co chuyen di vui ve!")
            break

        if not user_input:
            continue

        print("\n[TravelBuddy dang suy nghi...]")
        result = graph.invoke({"messages": [("human", user_input)]})
        final = result["messages"][-1]
        print(f"\nTravelBuddy: {final.content}")
