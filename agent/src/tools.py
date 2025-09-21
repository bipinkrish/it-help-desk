"""Tools that the bot can use to create and edit tickets."""

from typing import Dict, Any, Optional
from models import identify_issue
import logging
import os
import aiohttp

logger = logging.getLogger("livekit.agents")
base_url = os.getenv("API_BASE_URL", "http://localhost:3000/api")
logger.info(f"Tools initialized", extra={
    "component": "TicketTools",
    "api_base_url": base_url
})

class TicketTools:
    """Tools for ticket management."""
    
    def __init__(self):
        self.current_ticket: Optional[Dict[str, Any]] = None
        self.ticket_draft: Optional[Dict[str, Any]] = None
    
    async def create_ticket(self, name: str, email: str, phone: str, address: str, issue_description: str) -> Dict[str, Any]:
        """
        Create a new support ticket.
        """
        try:
            # Use draft data if available, otherwise use provided parameters
            final_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "address": address,
                "issue_description": issue_description,
            }
            
            # Merge with draft if it exists
            if self.ticket_draft:
                final_data.update(self.ticket_draft)
                logger.info(f"Using draft data for ticket creation", extra={
                    "component": "TicketTools",
                    "draft": self.ticket_draft,
                    "final_data": final_data
                })
            
            # Identify the issue type and get pricing
            issue_info = identify_issue(final_data["issue_description"])
            if not issue_info:
                return {
                    "success": False,
                    "error": "Sorry, we don't support that type of issue. We handle: Wi-Fi problems ($20), Email login issues ($15), Slow laptop performance ($25), and Printer problems ($10)."
                }
            
            # Send to Next.js API
            url = f"{base_url}/tickets"
            payload = {
                "name": final_data["name"],
                "email": final_data["email"],
                "phone": final_data["phone"],
                "address": final_data["address"],
                "issue_description": issue_info["description"],
            }
            logger.info(f"Making HTTP request to create ticket", extra={
                "component": "TicketTools",
                "method": "POST",
                "url": url,
                "payload": payload
            })
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    text = await resp.text()
                    logger.info(f"HTTP response received", extra={
                        "component": "TicketTools",
                        "status": resp.status,
                        "response_preview": text[:300]
                    })
                    if resp.status != 200:
                        return {"success": False, "error": "API error while creating ticket"}
                    
                    # Clear draft after successful creation
                    self.ticket_draft = None
                    return {"success": True, **(await resp.json())}
            
        except Exception as e:
            logger.error(f"Error creating ticket: {e}")
            return {
                "success": False,
                "error": "Sorry, there was an error creating your ticket. Please try again."
            }
    
    async def edit_ticket(self, field: str, value: str) -> Dict[str, Any]:
        """
        Edit a ticket field before confirmation (in memory only).
        """
        try:
            # Validate field
            valid_fields = ["name", "email", "phone", "address", "issue"]
            if field not in valid_fields:
                return {
                    "success": False,
                    "error": f"Invalid field. Can only edit: {', '.join(valid_fields)}"
                }
            
            # Initialize draft if it doesn't exist
            if self.ticket_draft is None:
                self.ticket_draft = {}
            
            # Update the draft
            self.ticket_draft[field] = value
            
            # If editing issue, re-identify the issue type and price
            if field == "issue":
                issue_info = identify_issue(value)
                if not issue_info:
                    return {
                        "success": False,
                        "error": "Sorry, we don't support that type of issue. We handle: Wi-Fi problems ($20), Email login issues ($15), Slow laptop performance ($25), and Printer problems ($10)."
                    }
                self.ticket_draft["issue"] = issue_info["description"]
                self.ticket_draft["price"] = issue_info["price"]
            
            logger.info(f"Updated ticket draft", extra={
                "component": "TicketTools",
                "field": field,
                "value": value,
                "draft": self.ticket_draft
            })
            
            return {
                "success": True,
                "field": field,
                "value": value,
                "message": f"Updated {field} to: {value}",
                "draft": self.ticket_draft
            }
                
        except Exception as e:
            logger.error(f"Error editing ticket draft: {e}")
            return {
                "success": False,
                "error": "Sorry, there was an error updating your ticket details. Please try again."
            }
