"""Database models for the IT Help Desk system."""

from typing import Optional, Dict, Any
from dataclasses import dataclass
from agent_config import SUPPORTED_ISSUES


# IT Issue configurations with pricing (using centralized config)
IT_ISSUES = {
    "wifi": {
        "keywords": ["wifi", "wi-fi", "wireless", "internet", "connection", "network", "connectivity"],
        "description": SUPPORTED_ISSUES["wifi"]["description"],
        "price": SUPPORTED_ISSUES["wifi"]["price"]
    },
    "email": {
        "keywords": ["email", "login", "password", "reset", "account", "access", "signin"],
        "description": SUPPORTED_ISSUES["email"]["description"],
        "price": SUPPORTED_ISSUES["email"]["price"]
    },
    "performance": {
        "keywords": ["laptop", "slow", "performance", "cpu", "speed", "computer", "pc", "optimization"],
        "description": SUPPORTED_ISSUES["performance"]["description"],
        "price": SUPPORTED_ISSUES["performance"]["price"]
    },
    "printer": {
        "keywords": ["printer", "printing", "power", "plug", "cable", "hardware", "driver"],
        "description": SUPPORTED_ISSUES["printer"]["description"],
        "price": SUPPORTED_ISSUES["printer"]["price"]
    }
}


def identify_issue(description: str) -> Optional[Dict[str, Any]]:
    """Identify the IT issue type from a description."""
    description_lower = description.lower()
    
    for issue_type, config in IT_ISSUES.items():
        for keyword in config["keywords"]:
            if keyword in description_lower:
                return {
                    "type": issue_type,
                    "description": config["description"],
                    "price": config["price"]
                }
    
    return None


def get_issue_price(issue_type: str) -> Optional[int]:
    """Get the price for a specific issue type."""
    if issue_type in IT_ISSUES:
        return IT_ISSUES[issue_type]["price"]
    return None
