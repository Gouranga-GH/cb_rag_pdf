import streamlit as st
from src.document_processor import DocumentProcessor
from src.rag_chain import RAGChain
from src.session_manager import SessionManager
from src.ui_components import UIComponents


class RAGApplication:
    def __init__(self):
        """Initialize the RAG application"""
        self.ui = UIComponents()
        self.session_manager = SessionManager()
        self.document_processor = None
        self.rag_chain = None
    
    def run(self):
        """Main application loop"""
        # Setup page
        self.ui.setup_page()
        
        # Get API key
        api_key = self.ui.get_api_key()
        
        if not api_key:
            self.ui.show_warning("Please enter the Groq API Key")
            return
        
        # Initialize RAG chain
        if not self.rag_chain:
            self.rag_chain = RAGChain(api_key)
        
        # Get session ID
        session_id = self.ui.get_session_id()
        
        # File upload
        uploaded_files = self.ui.upload_files()
        
        # Check if we have new files to process
        if uploaded_files:
            # Check if files have changed (simple check based on file names and sizes)
            current_files_info = [(f.name, f.size) for f in uploaded_files]
            
            # Initialize session state for file tracking
            if 'processed_files_info' not in st.session_state:
                st.session_state.processed_files_info = None
                st.session_state.vectorstore = None
                st.session_state.retriever = None
            
            # Only process if files are new or different
            if st.session_state.processed_files_info != current_files_info:
                # Process documents
                if not self.document_processor:
                    self.document_processor = DocumentProcessor()
                
                try:
                    vectorstore, retriever = self.document_processor.process_uploaded_files(uploaded_files)
                    
                    # Store in session state
                    st.session_state.vectorstore = vectorstore
                    st.session_state.retriever = retriever
                    st.session_state.processed_files_info = current_files_info
                    
                    # Create RAG chain
                    self.rag_chain.create_rag_chain(retriever)
                    
                    # Create conversational chain
                    self.rag_chain.create_conversational_chain(
                        self.session_manager.get_session_history
                    )
                    
                    self.ui.show_success("Documents processed successfully!")
                    
                except Exception as e:
                    st.error(f"Error processing documents: {str(e)}")
                    return
            else:
                # Use cached vectorstore and retriever
                if st.session_state.retriever:
                    # Create RAG chain with cached retriever
                    self.rag_chain.create_rag_chain(st.session_state.retriever)
                    
                    # Create conversational chain
                    self.rag_chain.create_conversational_chain(
                        self.session_manager.get_session_history
                    )
        
        # Chat interface (only if we have processed documents)
        if uploaded_files and (st.session_state.retriever or self.rag_chain.rag_chain):
            user_input = self.ui.get_user_question()
            
            if user_input:
                try:
                    # Get response
                    response = self.rag_chain.get_response(user_input, session_id)
                    
                    # Display response
                    self.ui.display_response(response)
                    
                    # Display chat history in sidebar
                    session_history = self.session_manager.get_session_history(session_id)
                    self.ui.display_chat_history_sidebar(session_history, session_id)
                    
                except Exception as e:
                    st.error(f"Error getting response: {str(e)}")
            else:
                # Display chat history in sidebar even when no new input
                session_history = self.session_manager.get_session_history(session_id)
                self.ui.display_chat_history_sidebar(session_history, session_id)
        
        # Cleanup temporary files when documents are no longer needed
        if not uploaded_files and self.document_processor:
            self.document_processor.cleanup_temp_files()


def main():
    """Main function to run the application"""
    app = RAGApplication()
    app.run()


if __name__ == "__main__":
    main() 