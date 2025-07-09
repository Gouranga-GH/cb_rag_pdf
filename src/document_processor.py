from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
import tempfile
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL


class DocumentProcessor:
    def __init__(self):
        """Initialize the document processor with embeddings model"""
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE, 
            chunk_overlap=CHUNK_OVERLAP
        )
        self.temp_files = []  # Track temporary files for cleanup
    
    def process_uploaded_files(self, uploaded_files):
        """
        Process uploaded PDF files and create vector store
        
        Args:
            uploaded_files: List of uploaded PDF files from Streamlit
            
        Returns:
            Chroma vector store and retriever
        """
        documents = []
        
        for uploaded_file in uploaded_files:
            # Create unique temporary file for each upload
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            temp_file_path = temp_file.name
            self.temp_files.append(temp_file_path)
            
            # Save uploaded file temporarily
            with open(temp_file_path, "wb") as file:
                file.write(uploaded_file.getvalue())
            
            # Load PDF documents
            loader = PyPDFLoader(temp_file_path)
            docs = loader.load()
            documents.extend(docs)
        
        # Split documents into chunks
        splits = self.text_splitter.split_documents(documents)
        
        # Create vector store
        vectorstore = Chroma.from_documents(
            documents=splits, 
            embedding=self.embeddings
        )
        
        # Create retriever
        retriever = vectorstore.as_retriever()
        
        return vectorstore, retriever
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        for temp_file in self.temp_files:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception as e:
                    print(f"Warning: Could not remove temporary file {temp_file}: {e}")
        self.temp_files = []  # Clear the list 