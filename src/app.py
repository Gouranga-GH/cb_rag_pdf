import streamlit as st
from src.document_processor import DocumentProcessor
from src.rag_chain import RAGChain
from src.session_manager import SessionManager
from src.ui_components import UIComponents

# Main application class that orchestrates the RAG chatbot
class RAGApplication:
    def __init__(self):
        """Initialize the RAG application and its core components"""
        self.ui = UIComponents()  # Handles all Streamlit UI elements
        self.session_manager = SessionManager()  # Manages chat sessions and history
        self.document_processor = None  # Will be initialized when needed
        self.rag_chain = None  # Will be initialized after API key is provided
    
    def run(self):
        """Main application loop, executed on every Streamlit rerun"""
        # Set up the Streamlit page (title, description, etc.)
        self.ui.setup_page()
        
        # Prompt user for Groq API key (required for LLM access)
        api_key = self.ui.get_api_key()
        
        if not api_key:
            # If no API key, show warning and stop execution
            self.ui.show_warning("Please enter the Groq API Key")
            return
        
        # Initialize the RAG chain if not already done
        if not self.rag_chain:
            self.rag_chain = RAGChain(api_key)
        
        # Prompt user for a session ID (for chat history tracking)
        session_id = self.ui.get_session_id()
        
        # Prompt user to upload PDF files
        uploaded_files = self.ui.upload_files()
        
        # If files are uploaded, check if they are new or changed
        if uploaded_files:
            # Create a list of (filename, filesize) for comparison
            current_files_info = [(f.name, f.size) for f in uploaded_files]
            
            # Initialize session state variables for file tracking and caching
            if 'processed_files_info' not in st.session_state:
                st.session_state.processed_files_info = None
                st.session_state.vectorstore = None
                st.session_state.retriever = None
            
            # Only process files if they are new or different from previous upload
            if st.session_state.processed_files_info != current_files_info:
                # Initialize DocumentProcessor if not already done
                if not self.document_processor:
                    self.document_processor = DocumentProcessor()
                
                try:
                    # Process uploaded PDFs: split, embed, and store in vector DB
                    vectorstore, retriever = self.document_processor.process_uploaded_files(uploaded_files)
                    
                    # Cache the vectorstore, retriever, and file info in session state
                    st.session_state.vectorstore = vectorstore
                    st.session_state.retriever = retriever
                    st.session_state.processed_files_info = current_files_info
                    
                    # Set up the RAG chain with the new retriever
                    self.rag_chain.create_rag_chain(retriever)
                    
                    # Set up the conversational chain (history-aware)
                    self.rag_chain.create_conversational_chain(
                        self.session_manager.get_session_history
                    )
                    
                    # Notify user of successful processing
                    self.ui.show_success("Documents processed successfully!")
                    
                except Exception as e:
                    # Show error if document processing fails
                    st.error(f"Error processing documents: {str(e)}")
                    return
            else:
                # If files are unchanged, use cached vectorstore and retriever
                if st.session_state.retriever:
                    # Re-create RAG and conversational chains with cached retriever
                    self.rag_chain.create_rag_chain(st.session_state.retriever)
                    self.rag_chain.create_conversational_chain(
                        self.session_manager.get_session_history
                    )
        
        # If documents are processed, show chat interface
        if uploaded_files and (st.session_state.retriever or self.rag_chain.rag_chain):
            # Prompt user for a question
            user_input = self.ui.get_user_question()
            
            if user_input:
                try:
                    # Get AI response from the RAG chain
                    response = self.rag_chain.get_response(user_input, session_id)
                    
                    # Display the AI response in the main area
                    self.ui.display_response(response)
                    
                    # Display chat history in the sidebar
                    session_history = self.session_manager.get_session_history(session_id)
                    self.ui.display_chat_history_sidebar(session_history, session_id)
                    
                except Exception as e:
                    # Show error if response generation fails
                    st.error(f"Error getting response: {str(e)}")
            else:
                # If no new question, still show chat history in sidebar
                session_history = self.session_manager.get_session_history(session_id)
                self.ui.display_chat_history_sidebar(session_history, session_id)
        
        # If no files are uploaded, clean up any temporary files
        if not uploaded_files and self.document_processor:
            self.document_processor.cleanup_temp_files()

# Entrypoint for Streamlit: creates and runs the RAG application

def main():
    """Main function to run the application"""
    app = RAGApplication()
    app.run()

# Ensures the app runs when executed directly (as required by Streamlit)
if __name__ == "__main__":
    main() 