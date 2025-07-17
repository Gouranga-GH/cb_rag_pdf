import streamlit as st
from typing import List, Optional

# Provides all Streamlit UI elements for the app
class UIComponents:
    @staticmethod
    def setup_page():
        """
        Set up the main page configuration (title, description, etc.)
        """
        st.title("KnowFlow: Upload. Converse. Understand.")
        st.write("A blend of “conversation” and “insight”.")
    
    @staticmethod
    def get_api_key() -> Optional[str]:
        """
        Prompt the user to enter their Groq API key (hidden input)
        Returns:
            API key string or None if not provided
        """
        return st.text_input("Enter your Groq API key:", type="password")
    
    @staticmethod
    def get_session_id() -> str:
        """
        Prompt the user to enter a session ID for chat tracking
        Returns:
            Session ID string
        """
        return st.text_input("Session ID (Change this to your own session ID for tracking)", value="my_session")
    
    @staticmethod
    def upload_files() -> List:
        """
        File uploader for PDF files (allows multiple files)
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
        Prompt the user to enter a question for the chatbot
        Returns:
            User question string or None if not provided
        """
        return st.text_input("Your question:")
    
    @staticmethod
    def display_response(response: dict):
        """
        Display the AI response in the main chat area
        Args:
            response: Response dictionary from RAG chain (expects 'answer' key)
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
            
            # Add clear history button if there are messages
            if session_history.messages:
                if st.button("🗑️ Clear History", key="clear_history"):
                    session_history.clear()
                    st.rerun()
            
            if not session_history.messages:
                st.info("No chat history yet. Start a conversation!")
                return
            
            # Display each message in a readable format
            for i, message in enumerate(session_history.messages):
                # Determine message type (human or AI)
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
        (Deprecated) Display chat history in the main area (use sidebar instead)
        Args:
            session_history: Chat message history object
        """
        # This method is now deprecated in favor of display_chat_history_sidebar
        pass
    
    @staticmethod
    def display_session_store(session_store: dict):
        """
        Display the entire session store for debugging purposes
        Args:
            session_store: Dictionary containing all sessions
        """
        st.write("Session Store:", session_store)
    
    @staticmethod
    def show_warning(message: str):
        """
        Display a warning message to the user
        Args:
            message: Warning message to display
        """
        st.warning(message)
    
    @staticmethod
    def show_success(message: str):
        """
        Display a success message to the user
        Args:
            message: Success message to display
        """
        st.success(message)
    
    @staticmethod
    def show_info(message: str):
        """
        Display an informational message to the user
        Args:
            message: Info message to display
        """
        st.info(message) 