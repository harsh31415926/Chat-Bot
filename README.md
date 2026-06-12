# 🚀 CHATW AI — Agentic Intelligence Platform

> Intelligent Conversations · Agentic Workflows · Real-Time Assistance

CHATW AI is a modern AI assistant built using LangGraph, Streamlit, and Groq LLMs. It demonstrates how to build production-ready agentic systems with memory, tool integration, database persistence, and ultra-fast inference.

The platform is designed to provide intelligent, context-aware conversations while showcasing advanced AI engineering concepts such as stateful agents, workflow orchestration, and tool calling.

---

## 🧠 Core Features

### ⚡ High-Speed Inference

Powered by Groq's ultra-low-latency models including:

* llama-3.3-70b-versatile
* llama-3.1-8b-instant

### 🔁 Stateful Memory

Maintains conversation context using LangGraph memory architecture for seamless multi-turn interactions.

### 🛠️ Tool Calling

Supports intelligent tool execution including:

* Web Search
* Financial Data Retrieval
* Mathematical Calculations
* Custom Agent Actions

### 💾 Persistent Storage

Stores conversation history and agent state using SQLite-based checkpointing.

### 🎨 Modern User Experience

Built with Streamlit and custom styling to deliver a professional, responsive, and visually appealing interface.

---

## 🏗️ Technology Stack

* Python
* LangGraph
* LangChain
* Streamlit
* Groq API
* SQLite
* DuckDuckGo Search
* Alpha Vantage API

---

## 📂 Application Entry Points

### 1. streamlit_app.py

Basic chatbot interface with conversation memory.

### 2. frontend_streamlit.py

Enhanced premium interface with custom styling and improved user experience.

### 3. streamlit_frontend_database.py

Full production-style application with:

* Database persistence
* Tool execution
* Stateful memory
* Advanced workflows

---

## 🚀 Local Installation

### Clone Repository

```bash
git clone https://github.com/your-username/chatw-ai.git
cd chatw-ai
```

### Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
```

### Run Application

```bash
streamlit run frontend_streamlit.py
```

or

```bash
streamlit run streamlit_frontend_database.py
```

---

## 🌐 Live Demo

CHATW AI is deployed on Streamlit Community Cloud:

https://chatw-chatbot.streamlit.app/

---

## ☁️ Streamlit Deployment

Add the following secrets in Streamlit Cloud:

```toml
GROQ_API_KEY = "your-groq-key"
ALPHA_VANTAGE_API_KEY = "your-alpha-vantage-key"
```

Then deploy using:

```text
frontend_streamlit.py
```

or

```text
streamlit_frontend_database.py
```

as the entrypoint.

---

## 🔒 Security Best Practices

* Never commit `.env` files.
* Never commit API keys.
* Store credentials using Streamlit Secrets.
* Keep databases and temporary files excluded using `.gitignore`.
* Rotate API keys immediately if they are accidentally exposed.

---

## 🎯 Purpose

This project serves as a practical demonstration of modern Agentic AI systems, combining conversational intelligence, memory, tool usage, and workflow orchestration into a deployable production-style application.
