from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory
from config.settings import CONTEXTUALIZE_Q_SYSTEM_PROMPT, QA_SYSTEM_PROMPT, LLM_MODEL


class RAGChain:
    def __init__(self, api_key):
        """
        Initialize RAG chain with Groq LLM
        
        Args:
            api_key: Groq API key
        """
        self.llm = ChatGroq(groq_api_key=api_key, model_name=LLM_MODEL)
        self.rag_chain = None
        self.conversational_rag_chain = None
    
    def create_rag_chain(self, retriever):
        """
        Create the RAG chain with history-aware retriever
        
        Args:
            retriever: Document retriever
        """
        # Create contextualize question prompt
        contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", CONTEXTUALIZE_Q_SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        
        # Create history-aware retriever
        history_aware_retriever = create_history_aware_retriever(
            self.llm, 
            retriever, 
            contextualize_q_prompt
        )
        
        # Create QA prompt
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", QA_SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        
        # Create question-answer chain
        question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)
        
        # Create retrieval chain
        self.rag_chain = create_retrieval_chain(
            history_aware_retriever, 
            question_answer_chain
        )
    
    def create_conversational_chain(self, get_session_history_func):
        """
        Create conversational RAG chain with message history
        
        Args:
            get_session_history_func: Function to get session history
        """
        self.conversational_rag_chain = RunnableWithMessageHistory(
            self.rag_chain,
            get_session_history_func,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )
    
    def get_response(self, user_input, session_id):
        """
        Get response from the conversational RAG chain
        
        Args:
            user_input: User's question
            session_id: Session identifier
            
        Returns:
            Response from the chain
        """
        if not self.conversational_rag_chain:
            raise ValueError("Conversational RAG chain not initialized")
        
        response = self.conversational_rag_chain.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}}
        )
        
        return response 