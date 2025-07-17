from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
import streamlit as st

# Manages chat session histories using Streamlit's session state
class SessionManager:
    def __init__(self):
        """Initialize session manager and ensure session state is set up"""
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Ensure Streamlit session state has a store for chat histories"""
        if 'store' not in st.session_state:
            st.session_state.store = {}
    
    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """
        Get or create chat message history for a session
        Args:
            session_id: Unique identifier for the chat session
        Returns:
            ChatMessageHistory object for the session
        """
        if session_id not in st.session_state.store:
            # Create a new chat history if it doesn't exist
            st.session_state.store[session_id] = ChatMessageHistory()
        return st.session_state.store[session_id]
    
    def get_all_sessions(self):
        """
        Get all active chat sessions and their histories
        Returns:
            Dictionary of all session histories
        """
        return st.session_state.store
    
    def clear_session(self, session_id: str):
        """
        Clear a specific session's chat history
        Args:
            session_id: Session identifier to clear
        """
        if session_id in st.session_state.store:
            del st.session_state.store[session_id]
    
    def clear_all_sessions(self):
        """
        Clear all session histories from session state
        """
        st.session_state.store = {} 