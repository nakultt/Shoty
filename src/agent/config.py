"""Configuration for the PixelPipe agent."""

from langchain_ollama import ChatOllama

# Model Configuration
MODEL_NAME = "qwen3-vl:8b"

# Temperature=0 is CRITICAL for consistent JSON extraction
llm = ChatOllama(model=MODEL_NAME, temperature=0)

print(f"✅ Loaded Model: {MODEL_NAME}")
