# 🧠 HR Policy ChatBot

A conversational AI chatbot that answers questions about HR policies using **LangChain**, **OpenAI**, **FAISS**, and **Streamlit**.  
It indexes HR policy HTML documents and enables semantic search and chat-based Q&A through a RAG (Retrieval-Augmented Generation) pipeline.

---

## ✅ Features

- 💬 **Conversational Q&A**: Ask HR policy questions in natural language.
- 🔍 **Semantic Search**: Retrieves relevant policy content using vector embeddings via FAISS.
- 🌐 **Web UI**: Simple and clean interface built with Streamlit.
- 🤖 **OpenAI Integration**: Uses GPT-4o (or GPT-3.5) for high-quality, context-aware answers.
- 📂 **Flexible Document Input**: Supports loading HR documents from local HTML files or websites [hr-policies](https://www.hrhelpboard.com/hr-policies.html).

---

## Project Structure

```
hrpc/
│
├── src/
│   ├── hrpc-FAISS-upload.py      # Script to index HR policy HTML files
│   ├── hrpc-query.py             # Streamlit chatbot app
│   ├── requirements.txt          # Python dependencies
│   ├── .env                      # OpenAI API key (not for public sharing)
│   └── img/
│       └── hr-logo.jpeg          # HR logo for UI
│
├── hr-policies/                  # Folder with downloaded HR policy HTML files
├── faiss_index/                  # Generated FAISS vector index (after running upload script)
└── README.md                     # This file
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repo-url>
cd hrpc
```

### 2. Download HR Policy HTML Files

You need a folder named `hr-policies` containing HR policy HTML files.  
You can use a tool like `wget` (Linux/WSL) or download manually.

Example with WSL:
```bash
wget -r -A.html -P hr-policies https://www.hrhelpboard.com/hr-policies.html
```

### 3. Create and Activate a Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 4. Install Dependencies

```powershell
pip install -r src/requirements.txt
```

### 5. Add Your OpenAI API Key

Create a `.env` file in the `src/` directory with:
```
OPENAI_API_KEY=sk-...
```

### 6. Index the HR Policy Documents

Run the upload script to create the FAISS vector index:

the below code 'upload_htmls()' is excecuted only once and then commented as the vector database is saved

  experiments 
  
    upload_htmls()
    
  the below function is experimental to trigger a semantic search on the vector DB
  
    faiss_query() 
    
```powershell
python src/hrpc-FAISS-upload.py
```
This will create a `faiss_index` folder with the vector database.

### 7. Run the Chatbot Web App

```powershell
streamlit run src/hrpc-query.py
```
Open the provided local URL in your browser.

---

## Usage

- Enter your HR policy question in the chat input.
- The chatbot will respond based on the indexed HR policy documents.
- Previous chat history is used for context-aware answers.

---

## Troubleshooting

- **Missing logo or index file**: Ensure `src/img/hr-logo.jpeg` and `faiss_index/index.faiss` exist.
- **Import errors**: Make sure all dependencies are installed and up to date.
- **OpenAI errors**: Check your API key and usage limits.

---

## 📌 Optional Next Steps
- Integrate with a company’s SharePoint or internal document management system
- Deploy the chatbot on the cloud (e.g., Streamlit Cloud, Azure App Service, or Docker)
