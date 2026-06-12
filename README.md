# 🚀 NEXORA CAPITAL — AI Trading Desk

> **Quant Intelligence · Execution Systems · Internal Use Only**

NEXORA CAPITAL is a production-style AI chatbot built using **LangGraph** and **Groq LLM**, designed to simulate an intelligent **hedge fund trading desk interface**.

This project demonstrates how to build **stateful AI agents** with memory, tool calling, database persistence, and high-speed inference.

---

## 🧠 Features

- ⚡ **Ultra-fast Responses**: Powered by Groq Cloud (`llama-3.3-70b-versatile` & `llama-3.1-8b-instant`).
- 🔁 **Stateful Conversations**: Multi-thread session state managed via LangGraph memory.
- 🛠️ **Tool-Calling Integration**: Agent automatically triggers search (DuckDuckGo), stock market data (Alpha Vantage), and arithmetic calculators.
- 💾 **SQLite DB Checkpointing**: Persistent conversation threads stored in a database.
- 🏦 **Hedge Fund UI**: Premium, dark-themed dashboard built with custom Streamlit styling and CSS glassmorphism.

---

## 📂 Frontend App Options

We provide three frontend entrypoints depending on your testing level:
1. **[streamlit_app.py](streamlit_app.py)**: The basic UI with memory.
2. **[frontend_streamlit.py](frontend_streamlit.py)**: High-end hedge-fund-styled UI with radial gradients.
3. **[streamlit_frontend_database.py](streamlit_frontend_database.py)**: The complete feature set featuring agent tool execution (Search, Finance APIs) and persistent database storage.

---

## 🛠️ Local Setup (macOS & Linux)

### 1. Clone & Navigate
```bash
git clone https://github.com/your-username/nexora-capital.git
cd nexora-capital
```

### 2. Set Up a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Open `.env` and fill in your API credentials:
```env
GROQ_API_KEY=gsk_...
ALPHA_VANTAGE_API_KEY=...
```

### 5. Run the Application
Start the premium app with database persistence and tools:
```bash
streamlit run streamlit_frontend_database.py
```
*(Alternatively, you can run `streamlit run frontend_streamlit.py` or `streamlit run streamlit_app.py`)*

---

## 🌩️ Deploying to Streamlit Community Cloud

1. Push your code to a public **GitHub Repository** (refer to safety instructions below).
2. Go to [share.streamlit.io](https://share.streamlit.io/) and log in.
3. Click **New app**, select your repository, branch, and set the Main file path to:
   `streamlit_frontend_database.py` (or `streamlit_app.py`)
4. Expand **Advanced settings...** and paste your environment variables into the **Secrets** text area:
   ```toml
   GROQ_API_KEY = "your-groq-key-here"
   ALPHA_VANTAGE_API_KEY = "your-alpha-vantage-key-here"
   ```
5. Click **Deploy**!

---

## 🛡️ Security & GitHub Best Practices

To protect your API credentials:
* **Never commit your `.env` or `chatbot.db` file**. The `.gitignore` has been pre-configured to block these.
* Utilize the `.env.example` file to show collaborators which environment variables are expected.
* For team deployment, add variables in Streamlit's secrets manager.
