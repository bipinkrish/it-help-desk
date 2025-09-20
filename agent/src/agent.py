"""IT Help Desk Voice Bot using LiveKit Agents framework."""

from models import TicketDatabase
from tools import TicketTools
from typing import Union
from agent_types import (
    UserDetails,
    CreateTicketResponse,
    LookupTicketResponse,
    UpdateExistingTicketResponse,
    SupportedIssuesResponse,
    ErrorResponse,
)
from livekit import agents
from livekit.agents import AgentSession, Agent, function_tool
from livekit.plugins import groq, deepgram
from agent_config import AGENT_INSTRUCTIONS, INITIAL_GREETING, AGENT_CONFIG


class ITHelpDeskAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=AGENT_INSTRUCTIONS)
        self.db = TicketDatabase("tickets.db")
        self.ticket_tools = TicketTools(self.db)

    @function_tool()
    async def create_ticket(self, context: agents.RunContext, name: str, email: str, phone: str, address: str, issue_description: str) -> Union[CreateTicketResponse, ErrorResponse]:
        """Create a new IT support ticket with user details and issue description."""
        return await self.ticket_tools.create_ticket(name, email, phone, address, issue_description)

    @function_tool()
    async def edit_ticket(self, context: agents.RunContext, ticket_id: int, field: str, value: str) -> dict:
        """Edit an existing ticket's field before confirmation."""
        return await self.ticket_tools.edit_ticket(ticket_id, field, value)

    @function_tool()
    async def lookup_ticket(self, context: agents.RunContext, name: str, email: str, confirmation_number: int) -> Union[LookupTicketResponse, ErrorResponse]:
        """Look up a ticket using name, email, and confirmation number."""
        return await self.ticket_tools.lookup_ticket(name, email, confirmation_number)

    @function_tool()
    async def update_existing_ticket(self, context: agents.RunContext, name: str, email: str, confirmation_number: int, field: str, value: str) -> Union[UpdateExistingTicketResponse, ErrorResponse]:
        """Update an existing ticket field after verification."""
        return await self.ticket_tools.update_existing_ticket(name, email, confirmation_number, field, value)

    @function_tool()
    async def get_supported_issues(self, context: agents.RunContext) -> SupportedIssuesResponse:
        """Return information about supported IT issues."""
        return await self.ticket_tools.get_supported_issues()


async def entrypoint(ctx: agents.JobContext):
    """Main entrypoint for the IT Help Desk agent."""
    
    # Create agent session with STT-LLM-TTS pipeline (cloud-based)
    session = AgentSession(
        stt=deepgram.STT(model=AGENT_CONFIG["stt_model"], language="en"),
        llm=groq.LLM(model=AGENT_CONFIG["llm_model"]),
        tts=deepgram.TTS(model=AGENT_CONFIG["tts_model"]),
    )

    # Start the session
    await session.start(
        room=ctx.room,
        agent=ITHelpDeskAssistant(),
        # Remove noise cancellation for cloud deployment
    )

    # Generate initial greeting
    await session.generate_reply(instructions=INITIAL_GREETING)


def main():
    """Main function to run the agent."""
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))


if __name__ == "__main__":
    main()
