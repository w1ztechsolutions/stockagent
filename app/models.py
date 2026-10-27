from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: str = Field(..., description="Role: 'system', 'user', or 'assistant'")
    content: str = Field(..., description="Message content")

class ChatRequest(BaseModel):
    message: str = Field(..., description="User message")
    session_id: Optional[str] = Field(None, description="Session identifier")
    history: Optional[List[ChatMessage]] = Field(None, description="Conversation history")

class ChatResponse(BaseModel):
    response: str = Field(..., description="Assistant response")
    session_id: str = Field(..., description="Session ID")
    model_used: str = Field(..., description="Model that generated response")
    steps: int = Field(..., description="Agent steps taken")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Service status")
    provider: str = Field(..., description="Active LLM provider")
    database: str = Field(..., description="Database status")
    model: str = Field(..., description="Active model name")

class QuoteResponse(BaseModel):
    symbol: str = Field(..., description="Stock symbol")
    found: bool = Field(..., description="Whether quote was found")
    currency: str = Field(default="MWK", description="Currency code")
    trade_date: Optional[str] = Field(None, description="Trade date")
    close: Optional[float] = Field(None, description="Closing price")
    change_percent: Optional[float] = Field(None, description="Percentage change")
    pe_ratio: Optional[float] = Field(None, description="P/E ratio")
    dividend_yield: Optional[float] = Field(None, description="Dividend yield %")
    error: Optional[str] = Field(None, description="Error message")