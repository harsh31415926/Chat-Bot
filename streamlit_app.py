import streamlit as st
from backend_langgraph import chatbot
from langchain_core.messages import HumanMessage
import uuid

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="Your Assistant",
    page_icon="📈",
    layout="wide"
)

# ====================== CUSTOM CSS ======================
st.markdown("""
<style>
/* Background */
body {
    background-color: #0e1117;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #1f2937;
}

/* Titles */
h1, h2, h3 {
    color: #e5e7eb;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 8px;
}

/* User message */
[data-testid="stChatMessage"][aria-label="user"] {
    background-color: #1f2937;
    border-left: 4px solid #3b82f6;
}

/* Assistant message */
[data-testid="stChatMessage"][aria-label="assistant"] {
    background-color: #111827;
    border-left: 4px solid #10b981;
}

/* Buttons */
.stButton>button {
    background-color: #1f2937;
    color: #e5e7eb;
    border-radius: 8px;
    border: 1px solid #374151;
}

.stButton>button:hover {
    background-color: #374151;
}

/* Input box */
textarea {
    background-color: #111827 !important;
    color: #e5e7eb !important;
}

/* Chat input */
div[data-testid="stChatInput"] {
    border-top: 1px solid #1f2937;
}
</style>
""", unsafe_allow_html=True)

# ====================== UTIL FUNCTIONS ======================

def generate_id():
    return str(uuid.uuid4())

def add_threads(thread_id, title="New Chat"):
    exists = any(t["id"] == thread_id for t in st.session_state['chat_threads'])
    if not exists:
        st.session_state['chat_threads'].append({
            "id": thread_id,
            "title": title
        })

def reset_chat():
    new_id = generate_id()
    st.session_state['thread_id'] = new_id
    st.session_state['message_history'] = []
    add_threads(new_id, "New Chat")

def load_convo(thread_id):
    state = chatbot.get_state(
        config={'configurable': {'thread_id': thread_id}}
    )
    messages = state.values.get('messages', [])

    formatted = []
    for msg in messages:
        role = 'user' if isinstance(msg, HumanMessage) else 'assistant'
        formatted.append({'role': role, 'content': msg.content})

    return formatted

# ====================== SESSION STATE ======================

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_threads(st.session_state['thread_id'])

CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

# ====================== HEADER ======================
st.markdown("""
<div style="padding: 10px 0;">
    <h2>📊 AI Assistant</h2>
    <p style="color:#9ca3af;">Your intelligent financial co-pilot powered by AI</p>
</div>
""", unsafe_allow_html=True)

# ====================== SIDEBAR ======================

st.sidebar.markdown("## 💼 Workspace")

if st.sidebar.button("➕ New Chat"):
    reset_chat()
    st.rerun()

st.sidebar.markdown("### 📂 Conversations")

for thread in reversed(st.session_state['chat_threads']):
    if st.sidebar.button(
    f"💬 {thread['title']}",
    key=thread["id"],   # 🔥 UNIQUE KEY
    use_container_width=True
):
        st.session_state['thread_id'] = thread["id"]
        st.session_state['message_history'] = load_convo(thread["id"])
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("⚡ Powered by AI + LangGraph")

# ====================== CHAT UI ======================

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_input = st.chat_input("Ask about markets, AI, or finance...")

# ====================== CHAT LOGIC ======================

if user_input:

    st.session_state['message_history'].append({
        'role': 'user',
        'content': user_input
    })

    for thread in st.session_state['chat_threads']:
        if thread["id"] == st.session_state['thread_id'] and thread["title"] == "New Chat":
            thread["title"] = user_input[:30]

    with st.chat_message('user'):
        st.markdown(user_input)

    with st.chat_message('assistant'):
        placeholder = st.empty()
        full_response = ""

        for message_chunk, metadata in chatbot.stream(
            {'messages': [HumanMessage(content=user_input)]},
            config=CONFIG,
            stream_mode='messages'
        ):
            if message_chunk.content:
                full_response += message_chunk.content
                placeholder.markdown(full_response)

    st.session_state['message_history'].append({
        'role': 'assistant',
        'content': full_response
    })