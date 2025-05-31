# 🤖📊 CSV Agent Chatbot

This is an interactive **CSV Agent Chatbot** built using **LangChain**, **Groq LLMs**, and **Streamlit**. It allows users to upload a CSV file and ask questions about the data in natural language. The system uses a combination of an agent (to interpret and analyze CSV content) and a visualization module (to generate charts or tables using HTML and Chart.js).

---

## 🔧 Features

- 📁 Upload CSV files for analysis
- 💬 Ask natural language questions about the CSV
- 🧠 Uses Groq's powerful LLMs via LangChain integration
- 📊 Automatically generates visualizations and tabular summaries
- 📝 Maintains a persistent chat history in the UI

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) – Web app frontend
- [LangChain](https://www.langchain.com/) – CSV agent creation
- [Groq API](https://console.groq.com/) – LLM backend
- [Chart.js](https://www.chartjs.org/) – Chart rendering in HTML
- [Pydantic](https://docs.pydantic.dev/) – Output validation
- Python 3.9+

---

## 📁 Project Structure

```
csv-agent-chatbot/
│
├── chatbot.py         # Main Streamlit app
├── csv_agent.py       # LangChain CSV agent logic
├── plotter.py         # Visualization formatter using Groq and HTML
├── .env               # Contains your GROQ_API_KEY
└── requirements.txt   # Python dependencies
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/BLUERAY94/yt_csv_agent.git
cd yt_csv_agent
```

### 2. Install dependencies

It is recommended to use a virtual environment.

```bash
pip install -r requirements.txt
```

### 3. Setup environment variables

Create a `.env` file in the root directory and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
```

### 4. Run the app

```bash
streamlit run chatbot.py
```

---

## 📷 Example Workflow

1. Launch the app.
2. Upload a CSV file via the sidebar.
3. Ask a question like _"What is the average salary by department?"_
4. View the chatbot's response and any generated chart/table.

---

## 🧠 How It Works

- **chatbot.py**: Manages UI and chat interaction via Streamlit.
- **csv_agent.py**: Uses LangChain's `create_csv_agent()` to parse and understand queries on uploaded CSV files.
- **plotter.py**: Sends the agent output to a Groq LLM with a structured prompt for generating HTML/Chart.js visualizations.

---

## ⚠️ Notes

- This application assumes the CSV file is clean and structured properly.
- Visualization is handled purely in HTML/JS using Chart.js inside Streamlit.

---

## 🙏 Acknowledgements

- [Groq](https://groq.com/)
- [LangChain](https://www.langchain.com/)
- [Streamlit](https://streamlit.io/)
- [Chart.js](https://www.chartjs.org/)
