import os
from typing import List, Optional
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class ProjectContext:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        self.embedding_function = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_function
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )

    def add_code_files(self, file_paths: List[str]):
        """Ingests code files into the vector database."""
        documents = []
        for path in file_paths:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    docs = self.text_splitter.create_documents(
                        [content], 
                        metadatas=[{"source": path}]
                    )
                    documents.extend(docs)
        
        if documents:
            self.vector_store.add_documents(documents)
            self.vector_store.persist()
            print(f"Added {len(documents)} document chunks to context.")

    def retrieve_context(self, query: str, k: int = 4) -> List[Document]:
        """Retrieves relevant code context for a given query."""
        return self.vector_store.similarity_search(query, k=k)

    def clear_context(self):
        """Clears the vector database."""
        self.vector_store.delete_collection()
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_function
        )
