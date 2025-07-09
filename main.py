"""
Main entry point for the Mod_Custom_RAG_CH_FU_2127

This application provides a conversational RAG system that allows users to:
- Upload PDF documents
- Chat with the content using natural language
- Maintain conversation history across sessions
- Use Groq's LLM for text generation

To run the application:
    streamlit run main.py
"""

from src.app import main

if __name__ == "__main__":
    main() 