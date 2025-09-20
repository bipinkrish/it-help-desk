#!/usr/bin/env python3
"""Script to run the IT Help Desk Voice Bot using LiveKit Agents."""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Load environment variables
load_dotenv()

# Import after path setup
from agent import main

if __name__ == "__main__":
    # Check if required credentials are set
    required_vars = [
        'LIVEKIT_URL',
        'LIVEKIT_API_KEY', 
        'LIVEKIT_API_SECRET',
        'DEEPGRAM_API_KEY',
        'OPENAI_API_KEY',
        'CARTESIA_API_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"ERROR: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please update backend/.env with the required credentials:")
        print("- LiveKit Cloud credentials")
        print("- Deepgram API key (for STT)")
        print("- OpenAI API key (for LLM)")
        print("- Cartesia API key (for TTS)")
        sys.exit(1)
    
    try:
        # Run the agent using LiveKit CLI
        main()
    except KeyboardInterrupt:
        print("\nAgent stopped by user")
    except Exception as e:
        print(f"Error starting agent: {e}")
        sys.exit(1)
