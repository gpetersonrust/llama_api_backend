import os
import json
from typing import List
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS  # type: ignore


class QADocumentIndexer:
    def __init__(
        self,
        json_paths: List[str],
        faiss_dir: str = "Stores/faiss_index",
        embedding_model: str = "nomic-embed-text",
    ):
        """
        Initialize the indexer for FAISS-based semantic search.
        """
        self.json_paths = json_paths
        self.faiss_dir = faiss_dir
        self.embedding = OllamaEmbeddings(model=embedding_model)
        self.chunked_docs: List[Document] = []

        os.makedirs(faiss_dir, exist_ok=True)

    def load_and_chunk_json(self, chunk_size=1000, chunk_overlap=200):
        """
        Load Q&A entries from JSON files and chunk answers for FAISS indexing.
        """
        all_entries = []

        for path in self.json_paths:
            with open(path, "r", encoding="utf-8") as f:
                file_data = json.load(f)
                for entry in file_data:
                    entry["_filename"] = os.path.basename(path)
                all_entries.extend(file_data)

        full_docs = [
            Document(
                page_content=entry["answer"],
                metadata={
                    "questions": "; ".join(entry.get("questions", [])),
                    "tags": "; ".join(entry.get("tags", [])),
                    "confidence": entry.get("confidence", 0.0),
                    "source": entry.get("source", "unknown"),
                    "approved": entry.get("approved", False),
                    "filename": entry.get("_filename", "unknown.json"),
                },
            )
            for entry in all_entries
        ]

        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        self.chunked_docs = splitter.split_documents(full_docs)
        print(f"✅ Loaded and chunked {len(self.chunked_docs)} total documents.")

    def index_to_faiss(self):
        """
        Embed chunked documents and store them in FAISS vector DB.
        """
        if not self.chunked_docs:
            raise ValueError(
                "❌ No chunked documents found. Run load_and_chunk_json() first."
            )

        faiss_store = FAISS.from_documents(self.chunked_docs, self.embedding)
        faiss_store.save_local(self.faiss_dir)
        print(f"✅ FAISS vector index saved to: {self.faiss_dir}")

    def run_all(self):
        """
        Run the full indexing pipeline:
        1. Load JSON and chunk documents
        2. Index to FAISS (semantic)
        """
        self.load_and_chunk_json()
        self.index_to_faiss()
        print("🚀 FAISS indexing pipeline complete.")

    def load_or_create_faiss(self):
        """
        Load FAISS index if it exists; otherwise, run indexing pipeline and return it.

        Returns:
            FAISS: The loaded FAISS vector store
        """
        index_file = os.path.join(self.faiss_dir, "index.faiss")
        if os.path.exists(index_file):
            print("📦 Loading existing FAISS index...")
            return FAISS.load_local(
                self.faiss_dir, self.embedding, allow_dangerous_deserialization=True
            )
        else:
            print("🚧 FAISS index not found. Building it now...")
            self.run_all()
            return FAISS.load_local(
                self.faiss_dir, self.embedding, allow_dangerous_deserialization=True
            )
