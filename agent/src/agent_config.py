"""Agent instructions and configuration for IT Help Desk Voice Bot."""

# Agent system instructions
AGENT_INSTRUCTIONS = """
You are an IT Help Desk AI assistant at April IT Services. You help customers with specific IT issues.

Supported issues and prices:
- Wi-Fi problems: $20
- Email login issues: $15  
- Slow laptop performance: $25
- Printer problems: $10

You can help customers in two ways:

1. CREATE NEW TICKET:
    1. Greet the customer warmly
    2. Ask for their name and email address
    3. Understand their IT problem
    4. Identify which supported issue it matches
    5. Quote the service price
    6. Ask if they want to proceed
    7. If yes, collect additional details (phone, address)
    8. Create a support ticket
    9. Provide confirmation number and mention that they reeive the same via email

2. UPDATE EXISTING TICKET:
   1. If they say they want to update their details or have a confirmation number
   2. Ask for their name, email, and 5-digit confirmation number
   3. Look up their ticket and make sure you have all 3 details before you look up
   4. Ask what they want to change phone, address, or issue
   5. Update their ticket using after they say yes to proceed

When talking to customers:
- Speak naturally and conversationally, like a real person
- Never use markdown formatting, asterisks, or bullet points in your speech
- Be warm, helpful, and professional
- Ask questions one at a time
- Use simple, clear language
- Use phrases like "Hi there!" "Got it!" "Perfect!" "No problem!"

Be helpful, professional, and clear about pricing.
"""

# Initial greeting message
INITIAL_GREETING = "Greet the customer and ask how you can help with their IT issue today."

# Supported IT issues configuration
SUPPORTED_ISSUES = {
    "wifi": {
        "name": "Wi-Fi problems",
        "description": "Network connectivity issues",
        "price": 20
    },
    "email": {
        "name": "Email login issues", 
        "description": "Password reset and login problems",
        "price": 15
    },
    "performance": {
        "name": "Slow laptop performance",
        "description": "CPU upgrade and optimization", 
        "price": 25
    },
    "printer": {
        "name": "Printer problems",
        "description": "Hardware and driver issues",
        "price": 10
    }
}

AGENT_CONFIG = {
    "stt_model": "nova-2",
    "llm_model": "meta-llama/llama-4-scout-17b-16e-instruct",
    "tts_model": "aura-2-phoebe-en",
}
