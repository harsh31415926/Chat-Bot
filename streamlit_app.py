import streamlit_app as st
from backend_langgraph import chatbot
from langchain_core.messages import HumanMessage
import uuid

def generate_id():
    return str(uuid.uuid4())

def reset_chat():
    new_id = generate_id()
    st.session_state['thread_id'] = new_id
    add_threads(new_id)
    st.session_state['message_history'] = []

def add_threads(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_convo(thread_id):
    return chatbot.get_state(
        config={'configurable': {'thread_id': thread_id}}
    ).values['messages']

# ===================Session State ==============================
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_threads(st.session_state['thread_id'])

# CONFIG must be after session state init
CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

# ======================= SIDEBAR ================================
st.sidebar.title("Chatbot")

if st.sidebar.button("Add new chat"):
    reset_chat()

st.sidebar.header("My Convos")

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_convo(thread_id)

        tot_message = []
        for message in messages:
            role = 'user' if isinstance(message, HumanMessage) else 'assistant'
            tot_message.append({'role': role, 'content': message.content})

        st.session_state['message_history'] = tot_message
        st.rerun()

# ======================= CHAT UI ================================
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_input = st.chat_input('Type here')

if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content
            for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})