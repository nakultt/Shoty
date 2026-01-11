"""Pydantic schemas for structured output extraction."""

from typing import Optional, Literal
from pydantic import BaseModel, Field


# Router Schema - Strict classification
class RouterSchema(BaseModel):
    """Schema for the vision router classification."""
    
    category: Literal["EVENT", "RECEIPT", "CODE", "UNKNOWN"] = Field(
        description="The specific type of the image. EVENT=Calendar/Dates. RECEIPT=Shopping/Bills. CODE=Programming Errors."
    )


# Extraction Schemas
class EventSchema(BaseModel):
    """Schema for event/calendar data extraction."""
    
    title: str = Field(description="Title of the event or meeting")
    date: str = Field(description="Date (YYYY-MM-DD)")
    time: str = Field(description="Time (HH:MM AM/PM)")
    attendees: Optional[str] = Field(description="Names of people mentioned, if any")


class ReceiptSchema(BaseModel):
    """Schema for receipt/expense data extraction."""
    
    merchant: str = Field(description="Name of the store/vendor")
    total: str = Field(description="Total amount with currency")
    date: str = Field(description="Date of purchase")
    items: str = Field(description="Comma-separated list of top items")


class CodeSchema(BaseModel):
    """Schema for code error analysis."""
    
    language: str = Field(description="Programming language (Python, JS, etc.)")
    error_msg: str = Field(description="The specific error message text")
    suggested_fix: str = Field(description="A brief 1-sentence potential solution")
