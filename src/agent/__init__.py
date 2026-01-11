"""PixelPipe Agent Module.

A vision-based screenshot classifier and data extractor using LangGraph.
"""

from agent.graph import graph
from agent.state import AgentState
from agent.config import MODEL_NAME, llm
from agent.schemas import (
    RouterSchema,
    EventSchema,
    ReceiptSchema,
    CodeSchema,
)
from agent.nodes import (
    vision_router_node,
    extract_event_node,
    extract_receipt_node,
    extract_code_node,
    human_review_node,
    tool_calendar_node,
    tool_expense_node,
    tool_stackoverflow_node,
)
from agent.utils import encode_image

__all__ = [
    "graph",
    "AgentState",
    "MODEL_NAME",
    "llm",
    "RouterSchema",
    "EventSchema",
    "ReceiptSchema",
    "CodeSchema",
    "vision_router_node",
    "extract_event_node",
    "extract_receipt_node",
    "extract_code_node",
    "human_review_node",
    "tool_calendar_node",
    "tool_expense_node",
    "tool_stackoverflow_node",
    "encode_image",
]
