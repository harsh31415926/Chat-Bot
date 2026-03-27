# 🚀 NEXORA CAPITAL — AI Trading Desk

> **Quant Intelligence · Execution Systems · Internal Use Only**

NEXORA CAPITAL is a production-style AI chatbot built using **LangGraph** and **Groq LLM**, designed to simulate an intelligent **hedge fund trading desk interface**.

This project demonstrates how to build **stateful AI agents** with memory, modular workflows, and high-speed inference — moving beyond simple chatbots into **real AI systems**.

---

## 🧠 Features

- ⚡ Ultra-fast responses using Groq (`llama-3.1-8b-instant`)
- 🔁 Stateful conversations (thread-based memory)
- 🧩 Modular agent architecture (LangGraph nodes)
- 💬 Context-aware chat (retains conversation history)
- 🏦 Hedge fund-inspired UI (Streamlit frontend)
- 🔧 Easily extensible (add tools, APIs, trading logic)

---

## ⚙️ Tech Stack

- **LangGraph** → Agent workflow & state management  
- **Groq LLM** → Fast inference engine  
- **LangChain Core** → Message handling  
- **Streamlit** → Interactive UI  
- **Python** → Backend logic  

---

## 🏗️ Architecture

- Uses `StateGraph` for workflow orchestration  
- Maintains state using `InMemorySaver`  
- Each request updates the conversation thread  

---

## 🧪 How It Works

1. User enters a query in Streamlit UI  
2. Input is converted into a `HumanMessage`  
3. LangGraph routes it to the `chat_node`  
4. Groq LLM processes full conversation context  
5. Response is returned and stored in memory  

---

## 📦 Installation

```bash
git clone https://github.com/your-username/nexora-capital.git
cd nexora-capital
pip install -r requirements.txt
