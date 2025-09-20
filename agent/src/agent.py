"""IT Help Desk Voice Bot using LiveKit Agents framework."""

from agent.config import agent_config
from livekit import agents
from livekit.agents import AgentSession, Agent
from livekit.plugins import (
    groq,
    cartesia,
    deepgram,
)
import sys
import os

# Add config directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
from ..config.agent_config import AGENT_INSTRUCTIONS, INITIAL_GREETING, AGENT_CONFIG


class ITHelpDeskAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=AGENT_INSTRUCTIONS)


async def entrypoint(ctx: agents.JobContext):
    """Main entrypoint for the IT Help Desk agent."""
    
    # Create agent session with STT-LLM-TTS pipeline (cloud-based)
    session = AgentSession(
        stt=deepgram.STT(model=AGENT_CONFIG["stt"], language=AGENT_CONFIG["language"]),
        llm=groq.LLM(model=AGENT_CONFIG["llm"]),
        tts=cartesia.TTS(model=AGENT_CONFIG["tts"], voice=AGENT_CONFIG["voice"]),
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
