import streamlit as st
from langchain_core.messages import HumanMessage
from backend_langgraph import chatbot

st.set_page_config(page_title="CHAT W", page_icon="💰", layout="wide")

# ------------------ STYLING ------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&display=swap');

* { font-family: 'Space Grotesk', sans-serif; }

.stApp {
    background-color: #050507;
    background-image: radial-gradient(circle at top, #0b0f1a, #050507);
}

/* Header */
.hero-title {
    font-size: 3.2rem;
    font-weight: 700;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #ffffff, #c7a86c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    color: #8b8b8b;
    font-size: 0.8rem;
    letter-spacing: 4px;
    text-transform: uppercase;
}

/* Ticker */
.ticker {
    display: flex;
    gap: 30px;
    padding: 10px 0;
    border-top: 1px solid #1a1a2e;
    border-bottom: 1px solid #1a1a2e;
    overflow: hidden;
}

.ticker-item {
    font-size: 0.75rem;
    letter-spacing: 2px;
    color: #c7a86c;
}

.ticker-item span {
    color: #10b981;
    margin-left: 5px;
}

/* Tags */
.tag {
    background: #0a0a0f;
    border: 1px solid #1a1a2e;
    color: #c7a86c;
    font-size: 0.65rem;
    padding: 4px 10px;
    margin-right: 6px;
    border-radius: 4px;
}

/* Chat */
[data-testid="stChatMessage"] {
    background: #0a0a0f !important;
    border: 1px solid #1a1a2e !important;
    border-radius: 8px !important;
}

/* Input */
[data-testid="stChatInput"] {
    border: 1px solid #c7a86c !important;
    background: #0a0a0f !important;
    color: white !important;
}

.footer {
    text-align: center;
    color: #444;
    font-size: 0.7rem;
    letter-spacing: 3px;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("<div class='hero-title'>CHAT W</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-sub'>Quant Intelligence · Execution Systems · Internal Use Only</div>", unsafe_allow_html=True)

# ------------------ TICKER ------------------
st.markdown("""
<div class='ticker'>
    <div class='ticker-item'>SPY <span>▲ 1.2%</span></div>
    <div class='ticker-item'>NVDA <span>▲ 4.8%</span></div>
    <div class='ticker-item'>TSLA <span>▲ 3.1%</span></div>
    <div class='ticker-item'>BTC <span>▲ 2.7%</span></div>
    <div class='ticker-item'>ETH <span>▲ 1.9%</span></div>
    <div class='ticker-item'>JPM <span>▲ 0.6%</span></div>
</div>
""", unsafe_allow_html=True)

# ------------------ TAGS ------------------
st.markdown("""
<div>
    <span class='tag'>🏦 Hedge Fund</span>
    <span class='tag'>📈 Quant</span>
    <span class='tag'>🤖 AI Desk</span>
    <span class='tag'>⚡ LangGraph</span>
    <span class='tag'>🧠 Groq LLM</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# ------------------ STATE ------------------
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

CONFIG = {'configurable': {"thread_id": 'trading-desk-1'}}

# ------------------ DISPLAY CHAT ------------------
for message in st.session_state['message_history']:
    with st.chat_message(message['role'], avatar='💰' if message['role']=='assistant' else '👤'):
        st.markdown(message['content'])

# ------------------ INPUT ------------------
user_input = st.chat_input("Enter query: markets, macro, trades...")

if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})

    with st.chat_message('user', avatar='👤'):
        st.markdown(user_input)

    with st.spinner('Executing strategy...'):
        response = chatbot.invoke(
            {'messages': [HumanMessage(content=user_input)]},
            config=CONFIG
        )
        ai_message = response['messages'][-1].content

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})

    with st.chat_message('assistant', avatar='💰'):
        st.markdown(ai_message)

# ------------------ FOOTER ------------------
st.markdown("<div class='footer'>CHAT W · AI TRADING DESK · CONFIDENTIAL</div>", unsafe_allow_html=True)