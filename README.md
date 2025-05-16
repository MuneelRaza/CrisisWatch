# CrisisWatch — Real-Time Crisis Analysis Agent

CrisisWatch is an intelligent agent system for tracking, analyzing, and reporting on real-time crisis situations such as conflicts, natural disasters, and humanitarian emergencies. It leverages Exa search, ReliefWeb data, and LLMs via LangGraph to produce factual summaries.

## 📁 Project Structure

```
.
├── agent/                  # Agent logic and tools
├── data/                   # Crisis data (JSON, PDFs)
├── data_ingestion/         # Scripts to fetch GNews, ReliefWeb content
├── data_transformation/    # Post-processing, NER scripts
├── pages/                  # Streamlit UI pages
├── utils/                  # LLM imports, utility helpers
├── main.py                 # Optional entry point for app
├── server.py               # FastAPI server backend
├── test.ipynb              # Notebook for testing components
├── requirements.txt        # Python dependencies
├── .env                    # API keys and config paths
└── README.md               # This file
```

## 🎓 Prerequisites

* Python 3.12+
* Virtualenv or Conda (recommended)
* API keys (see .env setup below)

## ✨ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/crisiswatch.git
cd crisiswatch
```

### 2. Create and Activate a Virtual Environment

Using venv:

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

Using conda:

```bash
conda create -n crisiswatch python=3.12 -y
conda activate crisiswatch
```

### 3. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
RELIEFWEB_DATA_FILE_PATH=data/reliefweb_data
RELIEFWEB_PDF_REPORTS_DIR_PATH=data/pdf_reports
GNEWS_API_KEY=your_gnews_key
TOGETHER_API_KEY=your_together_key
EXA_API_KEY=your_exa_key
NVIDIA_API_KEY=your_nvidia_key
```

Replace values with your actual API keys. Never share this file publicly.

### 5. Run the CLI Agent

```bash
python agent/crisis_agent.py
```

You will see a `>` prompt:

```
> what is the current situation in Gaza
Tool call detected: ...
🔍 Running search for query: ...
```

### 6. Run the Streamlit Interface (Optional)

```bash
streamlit run pages/CrisisWatch_Chatbot.py
```

### 7. Run the FastAPI Server (Optional)

```bash
uvicorn server:app --reload --port 8000
```

## ⚙️ Development Notes

* LLM configuration lives in `utils/import_llm.py`
* Tool definitions are in `agent/exa_tool.py`
* Core agent logic and LangGraph nodes in `agent/crisis_agent.py`
* Prompting templates in `agent/_system_prompt.py`
