from pathlib import Path
#lang comm used
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredEmailLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
    UnstructuredHTMLLoader,
    UnstructuredEPubLoader,
    CSVLoader,
    UnstructuredExcelLoader,
    UnstructuredPowerPointLoader,
    UnstructuredImageLoader
)

def load_document(file_paths):
    if isinstance(file_paths, (str, Path)):
        file_paths = [file_paths]  # Ensure list format

    docs = []
    for path in file_paths:
        path = str(path)
        ext = Path(path).suffix.lower()

        try:
            if ext == '.pdf':
                loader = PyPDFLoader(path)
            elif ext == '.docx':
                loader = UnstructuredWordDocumentLoader(path)
            elif ext in ['.eml', '.msg']:
                loader = UnstructuredEmailLoader(path)
            elif ext == '.txt':
                loader = TextLoader(path)
            elif ext in ['.md', '.markdown']:
                loader = UnstructuredMarkdownLoader(path)
            elif ext == '.html':
                loader = UnstructuredHTMLLoader(path)
            elif ext == '.epub':
                loader = UnstructuredEPubLoader(path)
            elif ext == '.csv':
                loader = CSVLoader(path)
            elif ext in ['.xls', '.xlsx']:
                loader = UnstructuredExcelLoader(path)
            elif ext in ['.ppt', '.pptx']:
                loader = UnstructuredPowerPointLoader(path)
            elif ext in ['.png', '.jpg', '.jpeg']:
                loader = UnstructuredImageLoader(path)
            else:
                print(f"[WARN] Unsupported file type skipped: {path}")
                continue

            docs.extend(loader.load())

        except Exception as e:
            print(f"[ERROR] Failed to load {path}: {e}")
            continue

    return docs
