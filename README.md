# Documate 📄

> **Document Q&A powered by RAG (Retrieval-Augmented Generation)**

Documate is a simple yet powerful tool that lets you upload any document and ask questions about it in plain English. Using RAG architecture with FAISS vector search and LangChain, it retrieves relevant sections from your document and generates accurate, context-grounded answers.

---

## 🎯 What It Does

Have a long PDF, a research paper, or a technical manual? Don't read the whole thing — just upload it and ask:

- *"What are the main findings in this report?"*
- *"Summarize the methodology section."*
- *"What does the contract say about termination clauses?"*

Documate finds the relevant parts, reads them, and gives you a straight answer.

---

## Features

-  **Upload any document** — PDF, DOCX, TXT, and more
-  **Semantic search** — Finds relevant sections using vector embeddings, not just keywords
-  **Natural language answers** — Powered by LangChain + Groq/OpenAI LLMs
-  **Fast retrieval** — FAISS vector indexing for instant search
-  **Simple web interface** — No CLI needed, just upload and ask via browser
-  **Local processing** — Documents processed locally, not sent to third-party services (except LLM API calls)

---

## Quick Start

### Prerequisites

- Python 3.9+
- A Groq or OpenAI API key (free tier available)

### Installation

```bash
# Clone the repository
git clone https://github.com/HaitaanshDixit/Documate.git
cd Documate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```bash
# For Groq (recommended - free tier)
GROQ_API_KEY=your_groq_api_key_here

# OR for OpenAI
OPENAI_API_KEY=your_openai_api_key_here
```

> **Get a Groq API key:** Sign up at https://console.groq.com → API Keys → Create new key

### Run the Application

```bash
# Start the FastAPI server
uvicorn main:app --reload
```

The app will be available at `http://127.0.0.1:8000`

---

## How to Use

1. **Open your browser** → Go to `http://127.0.0.1:8000`
2. **Upload a document** → Click "Choose File" and select your document
3. **Ask a question** → Type your query in the text box
4. **Get your answer** → The system retrieves relevant sections and generates a grounded response

### Example

**Document:** *A 20-page research paper on climate change impacts*

**Query:** *"What are the main effects of rising sea levels mentioned in the paper?"*

**Response:**
```
Based on the document, rising sea levels are expected to cause:
1. Coastal flooding affecting 200+ million people by 2050
2. Displacement of island nations and low-lying communities
3. Saltwater intrusion contaminating freshwater supplies
4. Loss of coastal ecosystems including mangroves and wetlands

These findings are discussed primarily in Section 3.2 and Section 4.1 of the paper.
```

---

## How It Works

```
┌─────────────────┐
│  User uploads   │
│    document     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Document Loader │ ← Parses PDF/DOCX/TXT
│ (unstructured)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Text Chunking  │ ← Splits into manageable chunks
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Embeddings    │ ← Convert text → vectors
│ (HuggingFace)   │   (sentence-transformers)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FAISS Index    │ ← Store vectors for fast search
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  User Query     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Vector Search   │ ← Find similar chunks
│    (FAISS)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   LLM (Groq)    │ ← Generate answer from context
│  llama-3.3-70b  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Grounded Answer │
└─────────────────┘
```

### Key Components

1. **Document Loader** (`src/loader.py`) — Loads and parses uploaded documents using the `unstructured` library
2. **RAG Pipeline** (`src/rag_pipeline.py`) — Handles embedding, indexing, retrieval, and LLM generation
3. **FAISS Index** — Stores document chunk embeddings for similarity search
4. **LangChain** — Orchestrates the retrieval and generation workflow
5. **FastAPI** — Serves the web interface and handles file uploads

---

## 📁 Project Structure

```
Documate/
├── main.py                  # FastAPI application entry point
├── requirements.txt         # Python dependencies
├── setup.py                 # Package setup
├── .env                     # API keys (not committed)
│
├── src/
│   ├── loader.py            # Document loading logic
│   └── rag_pipeline.py      # RAG workflow implementation
│
├── temp_files/              # Uploaded documents (temporary storage)
├── faiss_index/             # Persisted FAISS vector index
│
└── .github/workflows/       # CI/CD workflows
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | FastAPI, Uvicorn |
| **RAG** | LangChain, LangChain Community |
| **Vector Store** | FAISS (faiss-cpu) |
| **Embeddings** | HuggingFace Transformers, sentence-transformers |
| **LLM** | Groq API (llama-3.3-70b-versatile) |
| **Document Parsing** | unstructured, python-multipart |
| **Environment** | python-dotenv |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Simple HTML form for uploading documents |
| `POST` | `/upload/` | Upload document + query, returns answer |

### Example API Call

```bash
curl -X POST "http://127.0.0.1:8000/upload/" \
  -F "file=@research_paper.pdf" \
  -F "query=What is the main conclusion?"
```

**Response:**
```json
{
  "answer": "The main conclusion of the paper is that renewable energy adoption must accelerate by 300% to meet 2030 climate targets, as discussed in the final section."
}
```

---

## Configuration

### Supported Document Formats

- PDF (`.pdf`)
- Word Documents (`.docx`, `.doc`)
- Text Files (`.txt`)
- Markdown (`.md`)
- HTML (`.html`)

### Customizing the LLM

By default, Documate uses **Groq's llama-3.3-70b-versatile**. To switch to OpenAI:

1. Add `OPENAI_API_KEY` to your `.env`
2. Update `src/rag_pipeline.py`:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0
)
```

### Adjusting Chunk Size

In `src/rag_pipeline.py`, modify the text splitter parameters:

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Characters per chunk
    chunk_overlap=200     # Overlap between chunks
)
```

---

## Troubleshooting

### Issue: `RAG pipeline not initialized`

**Solution:** Make sure your API key is correctly set in `.env` and the file is in the project root.

### Issue: `ValueError: Unsupported file type`

**Solution:** Documate currently supports PDF, DOCX, TXT, MD, and HTML. Convert other formats before uploading.

### Issue: Slow first query after upload

**Solution:** The first query builds the FAISS index, which can take a few seconds for large documents. Subsequent queries are instant.

### Issue: LLM returning generic answers

**Solution:** The document might be too large. Try splitting it into smaller sections or increasing the `chunk_size` parameter.

---

## Deployment

### Deploy with Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t documate .
docker run -p 8000:8000 --env-file .env documate
```

### Deploy to Railway/Render

1. Push code to GitHub
2. Connect repo to Railway/Render
3. Add environment variable: `GROQ_API_KEY`
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

---

## Contributing

Contributions welcome! Here's how:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m "Add: your feature description"`
6. Push: `git push origin feature/your-feature`
7. Open a Pull Request

**Areas for contribution:**
- Support for more document formats (Excel, PowerPoint)
- Multi-document querying
- Conversational memory (follow-up questions)
- Better UI (Streamlit or React frontend)
- Caching layer for faster repeat queries

---

## License

This project is open source and available under the MIT License.

---

## Acknowledgments

- **LangChain** — For providing the RAG framework
- **FAISS** — For efficient vector similarity search
- **Groq** — For free-tier LLM API access
- **HuggingFace** — For sentence-transformers embeddings
- **unstructured** — For robust document parsing

---

**Built to make document reading less painful**