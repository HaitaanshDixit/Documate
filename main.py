from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, HTMLResponse
from pathlib import Path

from src.loader import load_document
from src.rag_pipeline import RAGPipeline

app = FastAPI()

# Global pipeline instance (created at startup)
rag_pipeline = None

@app.on_event("startup")
def startup_event():
    global rag_pipeline
    try:
        rag_pipeline = RAGPipeline()
        print("[INFO] RAG pipeline initialized successfully")
    except Exception as e:
        print(f"[ERROR] Failed to initialize RAG pipeline: {e}")
        raise
    
#simple html
@app.get("/", response_class=HTMLResponse)
def index():
    """Simple HTML form for uploading a file and query."""
    return """
    <html><body>
      <h2>Upload a Document & Ask a Question</h2>
      <form action="/upload/" enctype="multipart/form-data" method="post">
        <label>Choose File:</label>
        <input name="file" type="file" required><br><br>
        <label>Query:</label>
        <input name="query" type="text" placeholder="Enter your question" required><br><br>
        <input type="submit" value="Upload & Ask">
      </form>
    </body></html>
    """

@app.post("/upload/")
async def upload(file: UploadFile = File(...), query: str = Form(...)):
    if rag_pipeline is None:
        return JSONResponse(status_code=503, content={"error": "RAG pipeline not initialized"})

    # Save file temporarily
    temp_path = Path(f"temp_files/{file.filename}")
    temp_path.parent.mkdir(exist_ok=True)
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # Load documents
    try:
        docs = load_document(temp_path)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

    # Add documents to vectorstore
    rag_pipeline.add_documents(docs)

    # Get answer from query
    try:
        response = rag_pipeline.get_answer(query)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    return JSONResponse(content={"answer": response})



"""
from pyngrok import ngrok
ngrok.kill()
ngrok.set_auth_token("YOUR_NGROK_TOKEN")  # if needed
public_url = ngrok.connect(8000)
print(public_url)
"""