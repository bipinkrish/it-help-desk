"""IT Help Desk Voice Bot using LiveKit Agents framework."""

from livekit import agents
from livekit.agents import AgentSession, Agent
from livekit.plugins import (
    groq,
    deepgram,
)

from agent_config import AGENT_INSTRUCTIONS, INITIAL_GREETING, AGENT_CONFIG


class ITHelpDeskAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=AGENT_INSTRUCTIONS)


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
