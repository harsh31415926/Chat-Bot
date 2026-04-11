import streamlit as st
from langchain_core.messages import HumanMessage
from langgraph_tool_backend import chatbot, retrieve_all_threads
import uuid


# ================== UI CONFIG ==================
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

st.markdown("""
<style>

/* GLOBAL */
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

/* Background */
.main {
    background: linear-gradient(135deg, #020617, #0f172a);
    color: white;
}

/* Header */
h2 {
    font-weight: 600;
    letter-spacing: 0.5px;
}

/* Chat container spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    border-radius: 16px;
    padding: 12px 14px;
    margin-bottom: 10px;
    animation: fadeIn 0.3s ease-in-out;
}

/* User message */
[data-testid="stChatMessage"]:has(div[data-testid="user"]) {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
}

/* Assistant message */
[data-testid="stChatMessage"]:has(div[data-testid="assistant"]) {
    background-color: #020617;
    border: 1px solid #1e293b;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #020617);
    border-right: 1px solid #1e293b;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* Buttons */
.stButton button {
    width: 100%;
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 8px;
    margin-bottom: 6px;
    transition: all 0.2s ease;
}

.stButton button:hover {
    transform: scale(1.02);
    background: linear-gradient(90deg, #1d4ed8, #6d28d9);
}

/* Input box */
input {
    border-radius: 12px !important;
    border: 1px solid #334155 !important;
    background-color: #020617 !important;
    color: white !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background: #334155;
    border-radius: 10px;
}

/* Animation */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(5px);}
    to {opacity: 1; transform: translateY(0);}
}

</style>
""", unsafe_allow_html=True)


# ================== LOGIC (UNCHANGED) ==================

def generate_id():
    return str(uuid.uuid4())


def generate_title(user_input):
    return user_input[:30] + "..." if len(user_input) > 30 else user_input


def reset_chat():
    new_id = generate_id()
    st.session_state['thread_id'] = new_id
    add_threads(new_id, "New Chat")
    st.session_state['message_history'] = []


def add_threads(thread_id, name="New Chat"):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'][thread_id] = name


def load_convo(thread_id):
    state = chatbot.get_state(
        config={'configurable': {'thread_id': thread_id}}
    )
    return state.values.get('messages', [])


if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = {}

add_threads(st.session_state['thread_id'])

CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}


# ================== SIDEBAR ==================

st.sidebar.title("🤖 AI Chat")
st.sidebar.markdown("---")

if st.sidebar.button("➕ New Chat"):
    reset_chat()

st.sidebar.markdown("### 💬 Conversations")

for thread_id, name in list(st.session_state['chat_threads'].items())[::-1]:
    if st.sidebar.button(f"🗂️ {name}"):
        st.session_state['thread_id'] = thread_id
        messages = load_convo(thread_id)

        tot_message = []
        for message in messages:
            role = 'user' if isinstance(message, HumanMessage) else 'assistant'
            tot_message.append({'role': role, 'content': message.content})

        st.session_state['message_history'] = tot_message
        st.rerun()


# ================== HEADER ==================

st.markdown("## 🤖 AI Assistant")
st.markdown("##### Smart. Fast. Context-aware.")


# ================== CHAT ==================

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_input = st.chat_input('💬 Type your message...')

if user_input:

    if len(st.session_state['message_history']) == 0:
        st.session_state['chat_threads'][st.session_state['thread_id']] = generate_title(user_input)

    st.session_state['message_history'].append({'role': 'user', 'content': user_input})

    with st.chat_message('user'):
        st.markdown(user_input)

    with st.chat_message('assistant'):
        with st.spinner('🤔 Thinking...'):
            out = chatbot.invoke(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG
            )
            ai_message = out['messages'][-1].content

        st.markdown(ai_message)

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})