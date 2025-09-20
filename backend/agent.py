"""IT Help Desk Voice Bot using LiveKit Agents framework."""

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    groq,
    cartesia,
    deepgram,
)
# from tools import TicketTools
# from models import TicketDatabase




class ITHelpDeskAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""
            You are an IT Help Desk AI assistant. You help customers with common IT issues.
            
            Supported issues and prices:
            - Wi-Fi problems: $20
            - Email login issues: $15  
            - Slow laptop performance: $25
            - Printer problems: $10
            
            Your process:
            1. Greet the customer warmly
            2. Ask for their name and email address
            3. Understand their IT problem
            4. Identify which supported issue it matches
            5. Quote the service price
            6. Ask if they want to proceed
            7. If yes, collect additional details (phone, address)
            8. Create a support ticket
            9. Provide confirmation number
            
            Be helpful, professional, and clear about pricing.
            """
        )


async def entrypoint(ctx: agents.JobContext):
    """Main entrypoint for the IT Help Desk agent."""
    
    # Create agent session with STT-LLM-TTS pipeline (cloud-based)
    session = AgentSession(
        stt=deepgram.STT(model="nova-2", language="en"),
        llm=groq.LLM(model="openai/gpt-oss-20b"),
        tts=cartesia.TTS(model="sonic-2", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02"),
        # Remove VAD for cloud deployment - use built-in turn detection
    )

    # Start the session
    await session.start(
        room=ctx.room,
        agent=ITHelpDeskAssistant(),
        # Remove noise cancellation for cloud deployment
    )

    # Generate initial greeting
    await session.generate_reply(
        instructions="Greet the customer and ask how you can help with their IT issue today."
    )


def main():
    """Main function to run the agent."""
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))


if __name__ == "__main__":
    main()
