"""FastAPI server for token generation and ticket management."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv
import logging
from livekit import api

from models import TicketDatabase
from tools import TicketTools

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="IT Help Desk Bot API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database and tools
db = TicketDatabase()
ticket_tools = TicketTools(db)

# LiveKit configuration
LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

if not all([LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET]):
    raise ValueError("LiveKit credentials not found in environment variables")

# Initialize LiveKit API client
livekit_api = api.LiveKitAPI(
    url=LIVEKIT_URL,
    api_key=LIVEKIT_API_KEY,
    api_secret=LIVEKIT_API_SECRET,
)


class TokenRequest(BaseModel):
    room_name: str
    participant_name: str


class TokenResponse(BaseModel):
    token: str
    url: str


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "IT Help Desk Bot API is running"}


@app.post("/token", response_model=TokenResponse)
async def create_access_token(request: TokenRequest):
    """Create a LiveKit access token for a participant."""
    try:
        # Create access token
        token = api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        
        # Set participant identity and permissions
        token.with_identity(request.participant_name)
        token.with_grants(
            api.VideoGrants(
                room_join=True,
                room=request.room_name,
                can_publish=True,
                can_subscribe=True,
            )
        )
        
        # Generate JWT token
        jwt_token = token.to_jwt()
        
        logger.info(f"Generated token for {request.participant_name} in room {request.room_name}")
        
        return TokenResponse(
            token=jwt_token,
            url=LIVEKIT_URL
        )
        
    except Exception as e:
        logger.error(f"Error generating token: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate access token")


@app.get("/supported-issues")
async def get_supported_issues():
    """Get information about supported IT issues."""
    return ticket_tools.get_supported_issues()


@app.get("/tickets")
async def get_all_tickets():
    """Get all tickets (for admin purposes)."""
    try:
        tickets = db.get_all_tickets()
        return {"tickets": tickets}
    except Exception as e:
        logger.error(f"Error getting tickets: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve tickets")


@app.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: int):
    """Get a specific ticket by ID."""
    try:
        ticket = db.get_ticket(ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return {"ticket": ticket}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting ticket {ticket_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve ticket")


@app.delete("/tickets/{ticket_id}")
async def delete_ticket(ticket_id: int):
    """Delete a ticket by ID."""
    try:
        success = db.delete_ticket(ticket_id)
        if not success:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return {"message": "Ticket deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting ticket {ticket_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete ticket")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
