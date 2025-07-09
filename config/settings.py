import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Model Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "Gemma2-9b-It"

# Text Processing Configuration
CHUNK_SIZE = 5000
CHUNK_OVERLAP = 500

# System Prompts
CONTEXTUALIZE_Q_SYSTEM_PROMPT = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

QA_SYSTEM_PROMPT = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

# File Configuration
TEMP_PDF_PATH = "./temp.pdf"

# Environment Variables
HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY") 