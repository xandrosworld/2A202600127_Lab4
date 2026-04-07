import warnings
warnings.filterwarnings("ignore")

import streamlit as st
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_anthropic import ChatAnthropic
from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from tools import search_flights, search_hotels, calculate_budget, get_weather, search_activities
from dotenv import load_dotenv
import os

load_dotenv()

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="TravelBuddy — Trợ lý Du lịch Thông minh",
    page_icon="✈️",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Bright sky-blue gradient background */
.stApp {
    background: linear-gradient(160deg, #e0f7fa 0%, #e8f5e9 50%, #fff9c4 100%);
    min-height: 100vh;
}

/* Header */
.travel-header {
    text-align: center;
    padding: 2rem 1rem 0.5rem;
}
.travel-header h1 {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, #0077b6, #00b4d8, #48cae4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
    letter-spacing: -0.5px;
}
.travel-header p {
    color: #546e7a;
    font-size: 0.95rem;
    font-weight: 500;
}

/* Chat messages — user */
[data-testid="stChatMessageContent"] p {
    color: #1a202c !important;
    font-size: 0.96rem;
    line-height: 1.6;
}

/* Chat bubbles */
.stChatMessage {
    border-radius: 18px !important;
    border: 1px solid rgba(0,119,182,0.12) !important;
    background: rgba(255,255,255,0.85) !important;
    backdrop-filter: blur(8px);
    margin-bottom: 0.6rem !important;
    box-shadow: 0 2px 12px rgba(0,119,182,0.07) !important;
}

/* Input */
.stChatInputContainer {
    background: white !important;
    border-radius: 18px !important;
    border: 2px solid #00b4d8 !important;
    box-shadow: 0 4px 20px rgba(0,180,216,0.15) !important;
}
.stChatInputContainer textarea {
    color: #1a202c !important;
    font-size: 0.95rem !important;
}
.stChatInputContainer textarea::placeholder {
    color: #90a4ae !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0077b6 0%, #00b4d8 100%) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * {
    color: white !important;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.25) !important;
}

/* Sidebar button */
.stButton > button {
    background: rgba(255,255,255,0.2) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.4) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: rgba(255,255,255,0.35) !important;
    transform: translateY(-1px) !important;
}

/* Badges */
.badge {
    display: inline-block;
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 0.15rem;
}
.badge-dest {
    background: rgba(255,255,255,0.25);
    color: white;
    border: 1px solid rgba(255,255,255,0.4);
}

/* Spinner text */
.stSpinner > div {
    color: #0077b6 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────
st.markdown("""
<div class="travel-header">
    <h1>✈️ TravelBuddy</h1>
    <p>Trợ lý Du lịch Thông minh · Powered by Claude + LangGraph</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ✈️ TravelBuddy")
    st.markdown("---")
    st.markdown("**Mình có thể giúp bạn:**")
    st.markdown("""
- ✈️ Tìm chuyến bay giá tốt
- 🏨 Gợi ý khách sạn phù hợp
- 💰 Tính toán ngân sách
- 🌤️ Kiểm tra thời tiết
- 🎯 Lên lịch trình tham quan
    """)
    st.markdown("---")
    st.markdown("**Điểm đến hỗ trợ:**")
    st.markdown("""
<span class="badge badge-dest">🏖️ Đà Nẵng</span>
<span class="badge badge-dest">🌴 Phú Quốc</span>
<span class="badge badge-dest">🌆 Hồ Chí Minh</span>
    """, unsafe_allow_html=True)
    st.markdown("**Tuyến bay từ:**")
    st.markdown("""
<span class="badge badge-dest">🏛️ Hà Nội</span>
<span class="badge badge-dest">🌆 Hồ Chí Minh</span>
    """, unsafe_allow_html=True)
    st.markdown("---")
    if st.button("🗑️ Xoá hội thoại", use_container_width=True):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("© 2025 TravelBuddy · Lab 4 Demo")

# ── Build agent (cached) ──────────────────────────────────────
@st.cache_resource
def build_agent():
    with open("system_prompt.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read()

    tools_list = [search_flights, search_hotels, calculate_budget, get_weather, search_activities]
    llm = ChatAnthropic(
        model="claude-sonnet-4-5",
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )
    llm_with_tools = llm.bind_tools(tools_list)

    class AgentState(TypedDict):
        messages: Annotated[list, add_messages]

    def agent_node(state: AgentState) -> dict:
        messages: list[BaseMessage] = state["messages"]
        if not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=system_prompt)] + messages
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    builder = StateGraph(AgentState)
    builder.add_node("agent", agent_node)
    builder.add_node("tools", ToolNode(tools_list))
    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")
    return builder.compile()

graph = build_agent()

# ── Session state ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []

# ── Welcome message ───────────────────────────────────────────
if not st.session_state.messages:
    with st.chat_message("assistant", avatar="✈️"):
        st.markdown("""
Xin chào! Mình là **TravelBuddy** 👋

Mình có thể giúp bạn:
- Tìm **vé máy bay** giá tốt ✈️
- Gợi ý **khách sạn** phù hợp ngân sách 🏨
- Lên **lịch trình** tham quan chi tiết 🗺️
- Kiểm tra **thời tiết** điểm đến 🌤️

Bạn đang muốn đi đâu? 😊
        """)

# ── Render chat history ───────────────────────────────────────
for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "✈️"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ── Chat input ────────────────────────────────────────────────
if prompt := st.chat_input("Hỏi TravelBuddy... VD: Tìm vé Hà Nội → Đà Nẵng"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="✈️"):
        with st.spinner("TravelBuddy đang suy nghĩ..."):
            st.session_state.history.append(("human", prompt))
            result = graph.invoke({"messages": st.session_state.history})
            st.session_state.history = result["messages"]
            reply = result["messages"][-1].content

        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
