"""Node definitions for the PixelPipe graph."""
 
from langchain_core.messages import HumanMessage

from agent.state import AgentState
from agent.config import llm
from agent.utils import encode_image
from agent.schemas import (
    RouterSchema,
    EventSchema,
    ReceiptSchema,
    CodeSchema,
)


# ==========================================
# ROUTER NODE
# ==========================================

def vision_router_node(state: AgentState):
    """
    Analyzes the image and returns a STRICT classification.
    Uses structured output to prevent freeform responses.
    """
    print(f"\n👀 [ROUTER] Analyzing image...")
    b64_img = encode_image(state['image_path'])
    
    # Force Structured Output using the RouterSchema
    structured_router = llm.with_structured_output(RouterSchema)
    
    msg = HumanMessage(
        content=[
            {"type": "text", "text": "Analyze this image and classify it."},
            {"type": "image_url", "image_url": f"data:image/jpeg;base64,{b64_img}"}
        ]
    )
    
    try:
        response = structured_router.invoke([msg])
        classification = response.category
    except Exception as e:
        print(f"⚠️ Router Error: {e}")
        classification = "UNKNOWN"
            
    print(f"👉 Classified as: {classification}")
    return {"classification": classification}


# ==========================================
# EXTRACTOR NODES
# ==========================================

def extract_event_node(state: AgentState):
    """Extract event/calendar data from the image."""
    print("⚡ [EXTRACTOR] pulling Event data...")
    b64_img = encode_image(state['image_path'])
    extractor = llm.with_structured_output(EventSchema)
    
    msg = HumanMessage(content=[
        {"type": "text", "text": "Extract event details from this image."},
        {"type": "image_url", "image_url": f"data:image/jpeg;base64,{b64_img}"}
    ])
    res = extractor.invoke([msg])
    return {"extracted_data": res.dict()}


def extract_receipt_node(state: AgentState):
    """Extract receipt/expense data from the image."""
    print("⚡ [EXTRACTOR] pulling Receipt data...")
    b64_img = encode_image(state['image_path'])
    extractor = llm.with_structured_output(ReceiptSchema)
    
    msg = HumanMessage(content=[
        {"type": "text", "text": "Extract receipt details from this image."},
        {"type": "image_url", "image_url": f"data:image/jpeg;base64,{b64_img}"}
    ])
    res = extractor.invoke([msg])
    return {"extracted_data": res.dict()}


def extract_code_node(state: AgentState):
    """Analyze code error and suggest a fix."""
    print("⚡ [EXTRACTOR] pulling Code solution...")
    b64_img = encode_image(state['image_path'])
    extractor = llm.with_structured_output(CodeSchema)
    
    msg = HumanMessage(content=[
        {"type": "text", "text": "Analyze the code error and suggest a fix."},
        {"type": "image_url", "image_url": f"data:image/jpeg;base64,{b64_img}"}
    ])
    res = extractor.invoke([msg])
    return {"extracted_data": res.dict()}


# ==========================================
# HUMAN REVIEW NODE
# ==========================================

def human_review_node(state: AgentState):
    """Placeholder node to pause the graph for human review."""
    pass


# ==========================================
# TOOL NODES
# ==========================================

def tool_calendar_node(state: AgentState):
    """Execute Google Calendar integration."""
    d = state['extracted_data']
    print(f"\n📅 [TOOL] Google Calendar: Created '{d['title']}' on {d['date']} at {d['time']}")
    return {"tool_output": "Success"}


def tool_expense_node(state: AgentState):
    """Execute Notion expense logging."""
    d = state['extracted_data']
    print(f"\n💰 [TOOL] Notion: Logged {d['total']} at {d['merchant']}")
    return {"tool_output": "Success"}


def tool_stackoverflow_node(state: AgentState):
    """Execute Obsidian code fix storage."""
    d = state['extracted_data']
    print(f"\n🧠 [TOOL] Obsidian: Saved fix for {d['language']} error.")
    return {"tool_output": "Success"}
