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
    
    async def create_ticket(self, name: str, email: str, phone: str, address: str, issue_description: str) -> Dict[str, Any]:
        """
        Create a new support ticket.
        """
        try:
            # Identify the issue type and get pricing
            issue_info = identify_issue(issue_description)
            if not issue_info:
                return {
                    "success": False,
                    "error": "Sorry, we don't support that type of issue. We handle: Wi-Fi problems ($20), Email login issues ($15), Slow laptop performance ($25), and Printer problems ($10)."
                }
            
            # Send to Next.js API
            url = f"{base_url}/tickets"
            payload = {
                "name": name,
                "email": email,
                "phone": phone,
                "address": address,
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
                    return {"success": True, **(await resp.json())}
            
        except Exception as e:
            logger.error(f"Error creating ticket: {e}")
            return {
                "success": False,
                "error": "Sorry, there was an error creating your ticket. Please try again."
            }
    
    async def edit_ticket(self, ticket_id: int, field: str, value: str) -> Dict[str, Any]:
        """
        Edit a ticket field before confirmation.
        """
        try:
            # Validate field
            valid_fields = ["name", "email", "phone", "address", "issue"]
            if field not in valid_fields:
                return {
                    "success": False,
                    "error": f"Invalid field. Can only edit: {', '.join(valid_fields)}"
                }
            
            # If editing issue, re-identify the issue type and price
            updates = {field: value}
            if field == "issue":
                issue_info = identify_issue(value)
                if not issue_info:
                    return {
                        "success": False,
                        "error": "Sorry, we don't support that type of issue. We handle: Wi-Fi problems ($20), Email login issues ($15), Slow laptop performance ($25), and Printer problems ($10)."
                    }
                updates["issue"] = issue_info["description"]
                updates["price"] = issue_info["price"]
            
            url = f"{base_url}/tickets/update-by-id"
            payload = {"ticket_id": ticket_id, "field": field, "value": value}
            logger.info(f"[HTTP] POST {url} payload={payload}")
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    text = await resp.text()
                    logger.info(f"[HTTP] <- {resp.status} {text[:300]}")
                    if resp.status != 200:
                        return {"success": False, "error": "API error while editing ticket"}
                    return await resp.json()
                
        except Exception as e:
            logger.error(f"Error editing ticket: {e}")
            return {
                "success": False,
                "error": "Sorry, there was an error updating your ticket. Please try again."
            }
    
    # def get_ticket_info(self, ticket_id: int) -> Dict[str, Any]:
    #     """Get information about a ticket."""
    #     try:
    #         ticket = self.db.get_ticket(ticket_id)
    #         if ticket:
    #             return {
    #                 "success": True,
    #                 "ticket": {
    #                     "id": ticket.id,
    #                     "name": ticket.name,
    #                     "email": ticket.email,
    #                     "phone": ticket.phone,
    #                     "address": ticket.address,
    #                     "issue": ticket.issue,
    #                     "price": ticket.price,
    #                     "created_at": ticket.created_at
    #                 }
    #             }
    #         else:
    #             return {
    #                 "success": False,
    #                 "error": "Ticket not found"
    #             }
    #     except Exception as e:
    #         logger.error(f"Error getting ticket info: {e}")
    #         return {
    #             "success": False,
    #             "error": "Error retrieving ticket information"
    #         }
    
    def start_new_ticket_session(self) -> None:
        """Start a new ticket session (clear current ticket)."""
        self.current_ticket = None
        logger.info("Started new ticket session")
    
    # async def lookup_ticket(self, name: str, email: str, confirmation_number: int) -> Dict[str, Any]:
    #     """
    #     Look up an existing ticket by customer details and confirmation number.
    #     """
    #     try:
    #         url = f"{base_url}/tickets/lookup"
    #         payload = {"name": name, "email": email, "confirmation_number": confirmation_number}
    #         logger.info(f"[HTTP] POST {url} payload={payload}")
    #         async with aiohttp.ClientSession() as session:
    #             async with session.post(url, json=payload) as resp:
    #                 text = await resp.text()
    #                 logger.info(f"[HTTP] <- {resp.status} {text[:300]}")
    #                 if resp.status != 200:
    #                     return {"success": False, "error": "API error while looking up ticket"}
    #                 return await resp.json()
                
    #     except Exception as e:
    #         logger.error(f"Error looking up ticket: {e}")
    #         return {
    #             "success": False,
    #             "error": "Sorry, there was an error looking up your ticket. Please try again."
    #         }
    
    # async def update_existing_ticket(self, name: str, email: str, confirmation_number: int, field: str, value: str) -> Dict[str, Any]:
    #     """
    #     Update an existing ticket field.
    #     """
    #     try:
    #         url = f"{base_url}/tickets/update"
    #         payload = {"name": name, "email": email, "confirmation_number": confirmation_number, "field": field, "value": value}
    #         logger.info(f"[HTTP] POST {url} payload={payload}")
    #         async with aiohttp.ClientSession() as session:
    #             async with session.post(url, json=payload) as resp:
    #                 text = await resp.text()
    #                 logger.info(f"[HTTP] <- {resp.status} {text[:300]}")
    #                 if resp.status != 200:
    #                     return {"success": False, "error": "API error while updating ticket"}
    #                 return await resp.json()
                
    #     except Exception as e:
    #         logger.error(f"Error updating ticket: {e}")
    #         return {
    #             "success": False,
    #             "error": "Sorry, there was an error updating your ticket. Please try again."
    #         }

    # async def get_supported_issues(self) -> Dict[str, Any]:
    #     """Get information about supported IT issues."""
    #     # Import here to avoid circular imports
    #     from models import IT_ISSUES
        
    #     issues = []
    #     for issue_type, config in IT_ISSUES.items():
    #         issues.append({
    #             "type": issue_type,
    #             "description": config["description"],
    #             "price": config["price"],
    #             "keywords": config["keywords"]
    #         })
        
    #     return {
    #         "success": True,
    #         "issues": issues
    #     }
