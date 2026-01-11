"""PixelPipe LangGraph - Vision-based screenshot classification and extraction.

This module defines the main graph that processes images through:
1. Vision Router - Classifies the image type
2. Extractors - Pulls structured data based on classification
3. Human Review - Pauses for user approval
4. Tools - Executes actions (calendar, expense, code storage)
"""

import os
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver

from agent.state import AgentState
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


# ==========================================
# ROUTING LOGIC
# ==========================================

def route_logic(state: AgentState) -> str:
    """Route to the appropriate extractor based on classification."""
    cls = state['classification']
    if cls == "EVENT":
        return "extract_event"
    if cls == "RECEIPT":
        return "extract_receipt"
    if cls == "CODE":
        return "extract_code"
    return END


def approval_logic(state: AgentState) -> str:
    """Route to the appropriate tool based on approval and classification."""
    if state.get('user_feedback') != "APPROVED":
        return END
    cls = state['classification']
    if cls == "EVENT":
        return "tool_calendar"
    if cls == "RECEIPT":
        return "tool_expense"
    if cls == "CODE":
        return "tool_stackoverflow"
    return END


# ==========================================
# GRAPH CONSTRUCTION
# ==========================================

def build_graph():
    """Build and compile the PixelPipe graph."""
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("vision_router", vision_router_node)
    workflow.add_node("extract_event", extract_event_node)
    workflow.add_node("extract_receipt", extract_receipt_node)
    workflow.add_node("extract_code", extract_code_node)
    workflow.add_node("human_review", human_review_node)
    workflow.add_node("tool_calendar", tool_calendar_node)
    workflow.add_node("tool_expense", tool_expense_node)
    workflow.add_node("tool_stackoverflow", tool_stackoverflow_node)

    # Entry edge
    workflow.add_edge(START, "vision_router")

    # Conditional routing: Router -> Extractor
    workflow.add_conditional_edges("vision_router", route_logic, {
        "extract_event": "extract_event",
        "extract_receipt": "extract_receipt",
        "extract_code": "extract_code",
        END: END
    })

    # Extract -> Human Review
    workflow.add_edge("extract_event", "human_review")
    workflow.add_edge("extract_receipt", "human_review")
    workflow.add_edge("extract_code", "human_review")

    # Human Review -> Tool (conditional on approval)
    workflow.add_conditional_edges("human_review", approval_logic, {
        "tool_calendar": "tool_calendar",
        "tool_expense": "tool_expense",
        "tool_stackoverflow": "tool_stackoverflow",
        END: END
    })

    # Tools end the graph
    workflow.add_edge("tool_calendar", END)
    workflow.add_edge("tool_expense", END)
    workflow.add_edge("tool_stackoverflow", END)

    return workflow


# Build the graph
workflow = build_graph()

# Compile with interrupt_before for human-in-the-loop
# Use MemorySaver for standalone mode (python main.py)
# LangGraph API (langgraph dev) handles persistence automatically
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory, interrupt_before=["human_review"])
