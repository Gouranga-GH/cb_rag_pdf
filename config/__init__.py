"""
Configuration package for the Mod_Custom_RAG_CH_FU_2127

This package contains configuration settings and constants used throughout the application.
"""

from .settings import *

__all__ = [
    'EMBEDDING_MODEL',
    'LLM_MODEL', 
    'CHUNK_SIZE',
    'CHUNK_OVERLAP',
    'CONTEXTUALIZE_Q_SYSTEM_PROMPT',
    'QA_SYSTEM_PROMPT',
    'TEMP_PDF_PATH',
    'HF_TOKEN',
    'GROQ_API_KEY'
] 