"""State definition for the PixelPipe agent."""

from typing import TypedDict, Dict, Any


class AgentState(TypedDict):
    """State that flows through the graph."""
    
    image_path: str                 # Path to the screenshot
    classification: str             # "EVENT", "RECEIPT", "CODE", "UNKNOWN"
    extracted_data: Dict[str, Any]  # Extracted structured data
    user_feedback: str              # User approval status
    tool_output: str                # Tool execution result
