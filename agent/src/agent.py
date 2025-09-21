"""IT Help Desk Voice Bot using LiveKit Agents framework."""

from tools import TicketTools
from typing import Union
from agent_types import (
    CreateTicketResponse,
    ErrorResponse,
)
from livekit import agents
from livekit.agents import AgentSession, Agent, function_tool
from livekit.plugins import groq, deepgram
from agent_config import AGENT_INSTRUCTIONS, INITIAL_GREETING, AGENT_CONFIG
import logging

# Configure logging for LiveKit Agents
logger = logging.getLogger("livekit.agents")
logger.setLevel(logging.INFO)


class ITHelpDeskAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=AGENT_INSTRUCTIONS)
        self.ticket_tools = TicketTools()

    @function_tool()
    async def create_ticket(self, context: agents.RunContext, name: str, email: str, phone: str, address: str, issue_description: str) -> Union[CreateTicketResponse, ErrorResponse]:
        """Create a new IT support ticket with user details and issue description."""
        logger.info(f"LLM called create_ticket function", extra={
            "function": "create_ticket",
            "parameters": {
                "name": name,
                "email": email, 
                "phone": phone,
                "address": address,
                "issue_description": issue_description
            }
        })
        result = await self.ticket_tools.create_ticket(name, email, phone, address, issue_description)
        logger.info(f"create_ticket function completed", extra={
            "function": "create_ticket", 
            "result": result
        })
        return result

    @function_tool()
    async def edit_ticket(self, context: agents.RunContext, ticket_id: int, field: str, value: str) -> dict:
        """Edit an ticket's field before confirmation."""
        logger.info(f"LLM called edit_ticket function", extra={
            "function": "edit_ticket",
            "parameters": {
                "ticket_id": ticket_id,
                "field": field,
                "value": value
            }
        })
        result = await self.ticket_tools.edit_ticket(ticket_id, field, value)
        logger.info(f"edit_ticket function completed", extra={
            "function": "edit_ticket", 
            "result": result
        })
        return result


async def entrypoint(ctx: agents.JobContext):
    """Main entrypoint for the IT Help Desk agent."""
    logger.info(f"Starting IT Help Desk agent", extra={
        "room_name": ctx.room.name,
        "agent_type": "ITHelpDeskAssistant"
    })
    
    # Create agent session with STT-LLM-TTS pipeline (cloud-based)
    session = AgentSession(
        stt=deepgram.STT(model=AGENT_CONFIG["stt_model"], language="en"),
        llm=groq.LLM(model=AGENT_CONFIG["llm_model"]),
        tts=deepgram.TTS(model=AGENT_CONFIG["tts_model"]),
    )

    # Start the session
    logger.info("Starting agent session", extra={
        "stt_model": AGENT_CONFIG["stt_model"],
        "llm_model": AGENT_CONFIG["llm_model"], 
        "tts_model": AGENT_CONFIG["tts_model"]
    })
    await session.start(
        room=ctx.room,
        agent=ITHelpDeskAssistant(),
        # Remove noise cancellation for cloud deployment
    )

    # Generate initial greeting
    logger.info("Generating initial greeting", extra={
        "greeting": INITIAL_GREETING
    })
    await session.generate_reply(instructions=INITIAL_GREETING)
    logger.info("Agent session started successfully", extra={
        "status": "ready"
    })


def main():
    """Main function to run the agent."""
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))


if __name__ == "__main__":
    main()
