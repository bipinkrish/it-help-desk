"""LiveKit agent for the IT Help Desk bot."""

import asyncio
import logging
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

from livekit.agents import JobContext, WorkerOptions, cli, llm, stt, tts
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero, whisper

from models import TicketDatabase, identify_issue
from tools import TicketTools

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ITHelpDeskAgent:
    """IT Help Desk Voice Agent."""
    
    def __init__(self):
        self.db = TicketDatabase()
        self.ticket_tools = TicketTools(self.db)
        self.conversation_state = {
            "stage": "greeting",  # greeting, collecting_info, confirming, completed
            "collected_info": {
                "name": None,
                "email": None,
                "phone": None,
                "address": None,
                "issue": None,
                "price": None
            },
            "current_ticket_id": None,
            "attempts": 0
        }
    
    async def entrypoint(self, ctx: JobContext):
        """Main entrypoint for the agent."""
        logger.info("IT Help Desk Agent started")
        
        # Wait for the room to be ready
        await ctx.wait_for_room()
        
        # Get the room and participant
        room = ctx.room
        participant = ctx.participant
        
        logger.info(f"Connected to room: {room.name}, participant: {participant.identity}")
        
        # Initialize voice assistant
        assistant = VoiceAssistant(
            vad=stt.VAD.create(silero.VAD.load()),
            stt=stt.STT.create(whisper.STT.load()),
            llm=llm.LLM.create(openai.LLM(model="gpt-3.5-turbo")),
            tts=tts.TTS.create(silero.TTS.load()),
            chat_ctx=llm.ChatContext(
                messages=[
                    llm.ChatMessage.system(self._get_system_prompt())
                ]
            ),
            fnc_ctx=llm.FunctionContext(
                functions=[
                    self._create_ticket_function(),
                    self._edit_ticket_function(),
                    self._get_supported_issues_function()
                ]
            )
        )
        
        # Start the voice assistant
        await assistant.start(ctx.room)
        
        # Handle conversation flow
        await self._handle_conversation(assistant)
        
        logger.info("IT Help Desk Agent completed")
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the LLM."""
        return """You are a professional IT Help Desk assistant. Your role is to:

1. Greet callers professionally and warmly
2. Collect their contact information: name, email, phone number, and address
3. Understand their IT issue and identify if it's one of the supported types
4. Quote the correct service price
5. Allow them to modify details if needed
6. Create a support ticket when they confirm
7. Provide a confirmation number

SUPPORTED ISSUES AND PRICING:
- Wi-Fi not working: $20
- Email login issues (password reset): $15  
- Slow laptop performance (CPU change): $25
- Printer problems (power plug change): $10

CONVERSATION FLOW:
1. Greet: "Welcome to IT Help Desk. May I have your name and email?"
2. Collect contact info: "Thanks, [name]. What's your phone number and address?"
3. Ask about issue: "Got it. What issue are you facing today?"
4. Identify issue and quote price: "That's one of our supported issues. The service fee is $[price]. Should I create a ticket?"
5. Create ticket if confirmed: "Ticket created. Your confirmation number is [id]. You'll get a confirmation at [email]. Thank you!"

IMPORTANT RULES:
- Be concise and friendly
- If they mention an unsupported issue, explain what you do support
- Always quote the correct price for supported issues
- If they want to change details, use the edit_ticket function
- Handle interruptions gracefully
- Keep responses under 2 seconds
- If someone is rude or inappropriate, remain professional

Use the available functions to create and edit tickets as needed."""
    
    def _create_ticket_function(self) -> llm.Function:
        """Define the create_ticket function for the LLM."""
        return llm.Function(
            name="create_ticket",
            description="Create a new support ticket with customer information",
            parameters={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Customer's full name"
                    },
                    "email": {
                        "type": "string",
                        "description": "Customer's email address"
                    },
                    "phone": {
                        "type": "string",
                        "description": "Customer's phone number"
                    },
                    "address": {
                        "type": "string",
                        "description": "Customer's address"
                    },
                    "issue_description": {
                        "type": "string",
                        "description": "Description of the IT issue"
                    }
                },
                "required": ["name", "email", "phone", "address", "issue_description"]
            }
        )
    
    def _edit_ticket_function(self) -> llm.Function:
        """Define the edit_ticket function for the LLM."""
        return llm.Function(
            name="edit_ticket",
            description="Edit a ticket field before confirmation",
            parameters={
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "integer",
                        "description": "ID of the ticket to edit"
                    },
                    "field": {
                        "type": "string",
                        "enum": ["name", "email", "phone", "address", "issue"],
                        "description": "Field to update"
                    },
                    "value": {
                        "type": "string",
                        "description": "New value for the field"
                    }
                },
                "required": ["ticket_id", "field", "value"]
            }
        )
    
    def _get_supported_issues_function(self) -> llm.Function:
        """Define the get_supported_issues function for the LLM."""
        return llm.Function(
            name="get_supported_issues",
            description="Get information about supported IT issues and their pricing",
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    
    async def _handle_conversation(self, assistant: VoiceAssistant):
        """Handle the conversation flow and function calls."""
        try:
            while True:
                # Wait for function calls
                await asyncio.sleep(0.1)
                
                # Process any pending function calls
                if hasattr(assistant, '_function_calls'):
                    for call in assistant._function_calls:
                        await self._process_function_call(call)
                        assistant._function_calls.remove(call)
                
        except Exception as e:
            logger.error(f"Error in conversation handler: {e}")
    
    async def _process_function_call(self, call: llm.FunctionCall):
        """Process a function call from the LLM."""
        try:
            function_name = call.function_name
            arguments = call.arguments
            
            logger.info(f"Processing function call: {function_name} with args: {arguments}")
            
            if function_name == "create_ticket":
                result = self.ticket_tools.create_ticket(
                    name=arguments.get("name"),
                    email=arguments.get("email"),
                    phone=arguments.get("phone"),
                    address=arguments.get("address"),
                    issue_description=arguments.get("issue_description")
                )
                
            elif function_name == "edit_ticket":
                result = self.ticket_tools.edit_ticket(
                    ticket_id=arguments.get("ticket_id"),
                    field=arguments.get("field"),
                    value=arguments.get("value")
                )
                
            elif function_name == "get_supported_issues":
                result = self.ticket_tools.get_supported_issues()
                
            else:
                result = {"success": False, "error": "Unknown function"}
            
            # Send result back to LLM
            if hasattr(call, 'result'):
                call.result = result
            
            logger.info(f"Function call result: {result}")
            
        except Exception as e:
            logger.error(f"Error processing function call: {e}")
            if hasattr(call, 'result'):
                call.result = {"success": False, "error": str(e)}


async def main():
    """Main function to start the agent."""
    # Initialize the agent
    agent = ITHelpDeskAgent()
    
    # Configure worker options
    options = WorkerOptions(
        entrypoint_fnc=agent.entrypoint,
        prewarm_processes=1,
    )
    
    # Start the worker
    await cli.run_worker(options)


if __name__ == "__main__":
    asyncio.run(main())
