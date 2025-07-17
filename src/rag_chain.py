from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory
from config.settings import CONTEXTUALIZE_Q_SYSTEM_PROMPT, QA_SYSTEM_PROMPT, LLM_MODEL

# Handles the RAG pipeline, including LLM setup, retrieval, and conversational logic
class RAGChain:
    def __init__(self, api_key):
        """
        Initialize RAG chain with Groq LLM
        Args:
            api_key: Groq API key for authenticating LLM requests
        """
        # Set up the Groq LLM with the specified model
        self.llm = ChatGroq(groq_api_key=api_key, model_name=LLM_MODEL)
        self.rag_chain = None  # Will hold the retrieval chain
        self.conversational_rag_chain = None  # Will hold the history-aware chain
    
    def create_rag_chain(self, retriever):
        """
        Create the RAG chain with a history-aware retriever and QA chain
        Args:
            retriever: Document retriever for semantic search
        """
        # Prompt for reformulating user questions with chat history
        contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", CONTEXTUALIZE_Q_SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        
        # Create a retriever that is aware of chat history
        history_aware_retriever = create_history_aware_retriever(
            self.llm, 
            retriever, 
            contextualize_q_prompt
        )
        
        # Prompt for the main QA task
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", QA_SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        
        # Chain for combining retrieved documents and generating answers
        question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)
        
        # The main retrieval-augmented generation chain
        self.rag_chain = create_retrieval_chain(
            history_aware_retriever, 
            question_answer_chain
        )
    
    def create_conversational_chain(self, get_session_history_func):
        """
        Create a conversational RAG chain that maintains message history
        Args:
            get_session_history_func: Function to get session history for a session ID
        """
        # Wrap the RAG chain with message history for context-aware conversations
        self.conversational_rag_chain = RunnableWithMessageHistory(
            self.rag_chain,
            get_session_history_func,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )
    
    def get_response(self, user_input, session_id):
        """
        Get a response from the conversational RAG chain
        Args:
            user_input: User's question
            session_id: Session identifier for chat history
        Returns:
            Response from the chain (dict with 'answer' key)
        """
        if not self.conversational_rag_chain:
            raise ValueError("Conversational RAG chain not initialized")
        
        # Invoke the chain with user input and session context
        response = self.conversational_rag_chain.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}}
        )
        
        return response 