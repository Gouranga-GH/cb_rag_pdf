import streamlit as st
from typing import List, Optional


class UIComponents:
    @staticmethod
    def setup_page():
        """Setup the main page configuration"""
        st.title("KnowFlow: Upload. Converse. Understand.")
        st.write("A blend of “conversation” and “insight”.")
    
    @staticmethod
    def get_api_key() -> Optional[str]:
        """
        Get Groq API key from user input
        
        Returns:
            API key string or None if not provided
        """
        return st.text_input("Enter your Groq API key:", type="password")
    
    @staticmethod
    def get_session_id() -> str:
        """
        Get session ID from user input
        
        Returns:
            Session ID string
        """
        return st.text_input("Session ID (Change this to your own session ID for tracking)", value="my_session")
    
    @staticmethod
    def upload_files() -> List:
        """
        File uploader for PDF files
        
        Returns:
            List of uploaded files
        """
        return st.file_uploader(
            "Choose PDF files", 
            type="pdf", 
            accept_multiple_files=True
        )
    
    @staticmethod
    def get_user_question() -> Optional[str]:
        """
        Get user question input
        
        Returns:
            User question string or None if not provided
        """
        return st.text_input("Your question:")
    
    @staticmethod
    def display_response(response: dict):
        """
        Display the AI response
        
        Args:
            response: Response dictionary from RAG chain
        """
        st.write("Assistant:", response['answer'])
    
    @staticmethod
    def display_chat_history_sidebar(session_history, session_id: str = "default_session"):
        """
        Display chat history in a sidebar with human-readable format
        
        Args:
            session_history: Chat message history object
            session_id: Session identifier for clearing history
        """
        with st.sidebar:
            st.header("💬 Chat History")
            
            # Add clear history button
            if session_history.messages:
                if st.button("🗑️ Clear History", key="clear_history"):
                    session_history.clear()
                    st.rerun()
            
            if not session_history.messages:
                st.info("No chat history yet. Start a conversation!")
                return
            
            # Display messages in a readable format
            for i, message in enumerate(session_history.messages):
                # Check message type by class name to avoid import issues
                message_type = type(message).__name__
                if "Human" in message_type:
                    st.markdown(f"**You:** {message.content}")
                elif "AI" in message_type or "Assistant" in message_type:
                    st.markdown(f"**Assistant:** {message.content}")
                else:
                    # Fallback for other message types
                    st.markdown(f"**{message_type}:** {message.content}")
                
                # Add a separator between messages
                if i < len(session_history.messages) - 1:
                    st.divider()
    
    @staticmethod
    def display_chat_history(session_history):
        """
        Display chat history (legacy method - kept for compatibility)
        
        Args:
            session_history: Chat message history object
        """
        # This method is now deprecated in favor of display_chat_history_sidebar
        pass
    
    @staticmethod
    def display_session_store(session_store: dict):
        """
        Display session store for debugging
        
        Args:
            session_store: Dictionary containing all sessions
        """
        st.write("Session Store:", session_store)
    
    @staticmethod
    def show_warning(message: str):
        """
        Display warning message
        
        Args:
            message: Warning message to display
        """
        st.warning(message)
    
    @staticmethod
    def show_success(message: str):
        """
        Display success message
        
        Args:
            message: Success message to display
        """
        st.success(message)
    
    @staticmethod
    def show_info(message: str):
        """
        Display info message
        
        Args:
            message: Info message to display
        """
        st.info(message) 