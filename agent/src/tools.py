"""Tools that the bot can use to create and edit tickets."""

from typing import Dict, Any, Optional
from models import Ticket, TicketDatabase, identify_issue, get_issue_price
import logging

logger = logging.getLogger(__name__)


class TicketTools:
    """Tools for ticket management."""
    
    def __init__(self, db: TicketDatabase):
        self.db = db
        self.current_ticket: Optional[Ticket] = None
    
    def create_ticket(self, name: str, email: str, phone: str, address: str, issue_description: str) -> Dict[str, Any]:
        """
        Create a new support ticket.
        
        Args:
            name: Customer's name
            email: Customer's email address
            phone: Customer's phone number
            address: Customer's address
            issue_description: Description of the IT issue
            
        Returns:
            Dict containing ticket ID and confirmation details
        """
        try:
            # Identify the issue type and get pricing
            issue_info = identify_issue(issue_description)
            if not issue_info:
                return {
                    "success": False,
                    "error": "Sorry, we don't support that type of issue. We handle: Wi-Fi problems ($20), Email login issues ($15), Slow laptop performance ($25), and Printer problems ($10)."
                }
            
            # Create the ticket
            ticket = Ticket(
                name=name,
                email=email,
                phone=phone,
                address=address,
                issue=issue_info["description"],
                price=issue_info["price"]
            )
            
            ticket_id, confirmation_number = self.db.create_ticket(ticket)
            self.current_ticket = ticket
            
            logger.info(f"Created ticket {ticket_id} with confirmation {confirmation_number} for {name} ({email})")
            
            return {
                "success": True,
                "ticket_id": ticket_id,
                "confirmation_number": confirmation_number,
                "email": email,
                "issue": issue_info["description"],
                "price": issue_info["price"]
            }
            
        except Exception as e:
            logger.error(f"Error creating ticket: {e}")
            return {
                "success": False,
                "error": "Sorry, there was an error creating your ticket. Please try again."
            }
    
    def edit_ticket(self, ticket_id: int, field: str, value: str) -> Dict[str, Any]:
        """
        Edit a ticket field before confirmation.
        
        Args:
            ticket_id: ID of the ticket to edit
            field: Field to update (name, email, phone, address, issue)
            value: New value for the field
            
        Returns:
            Dict containing success status and updated information
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
            
            # Update the ticket
            success = self.db.update_ticket(ticket_id, updates)
            
            if success:
                # Update current ticket if it's the same one
                if self.current_ticket and self.current_ticket.id == ticket_id:
                    if field == "name":
                        self.current_ticket.name = value
                    elif field == "email":
                        self.current_ticket.email = value
                    elif field == "phone":
                        self.current_ticket.phone = value
                    elif field == "address":
                        self.current_ticket.address = value
                    elif field == "issue":
                        self.current_ticket.issue = issue_info["description"]
                        self.current_ticket.price = issue_info["price"]
                
                logger.info(f"Updated ticket {ticket_id} field {field}")
                
                return {
                    "success": True,
                    "field": field,
                    "value": value,
                    "updated_price": updates.get("price")
                }
            else:
                return {
                    "success": False,
                    "error": "Ticket not found or could not be updated"
                }
                
        except Exception as e:
            logger.error(f"Error editing ticket: {e}")
            return {
                "success": False,
                "error": "Sorry, there was an error updating your ticket. Please try again."
            }
    
    def get_ticket_info(self, ticket_id: int) -> Dict[str, Any]:
        """Get information about a ticket."""
        try:
            ticket = self.db.get_ticket(ticket_id)
            if ticket:
                return {
                    "success": True,
                    "ticket": {
                        "id": ticket.id,
                        "name": ticket.name,
                        "email": ticket.email,
                        "phone": ticket.phone,
                        "address": ticket.address,
                        "issue": ticket.issue,
                        "price": ticket.price,
                        "created_at": ticket.created_at
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "Ticket not found"
                }
        except Exception as e:
            logger.error(f"Error getting ticket info: {e}")
            return {
                "success": False,
                "error": "Error retrieving ticket information"
            }
    
    def start_new_ticket_session(self) -> None:
        """Start a new ticket session (clear current ticket)."""
        self.current_ticket = None
        logger.info("Started new ticket session")
    
    def lookup_ticket(self, name: str, email: str, confirmation_number: int) -> Dict[str, Any]:
        """
        Look up an existing ticket by customer details and confirmation number.
        
        Args:
            name: Customer's name
            email: Customer's email address
            confirmation_number: 5-digit confirmation number
            
        Returns:
            Dict containing ticket information if found
        """
        try:
            ticket = self.db.find_ticket_by_customer(name, email, confirmation_number)
            
            if ticket:
                logger.info(f"Found ticket {ticket.id} for {name} ({email})")
                return {
                    "success": True,
                    "ticket": {
                        "id": ticket.id,
                        "name": ticket.name,
                        "email": ticket.email,
                        "phone": ticket.phone,
                        "address": ticket.address,
                        "issue": ticket.issue,
                        "price": ticket.price,
                        "created_at": ticket.created_at
                    },
                    "message": f"Found your ticket! Your issue is: {ticket.issue} for ${ticket.price}"
                }
            else:
                return {
                    "success": False,
                    "error": "Sorry, I couldn't find a ticket with those details. Please check your name, email, and confirmation number."
                }
                
        except Exception as e:
            logger.error(f"Error looking up ticket: {e}")
            return {
                "success": False,
                "error": "Sorry, there was an error looking up your ticket. Please try again."
            }
    
    def update_existing_ticket(self, name: str, email: str, confirmation_number: int, field: str, value: str) -> Dict[str, Any]:
        """
        Update an existing ticket field.
        
        Args:
            name: Customer's name
            email: Customer's email address
            confirmation_number: 5-digit confirmation number
            field: Field to update (phone, address, issue)
            value: New value for the field
            
        Returns:
            Dict containing success status and updated information
        """
        try:
            # First, find the ticket
            ticket = self.db.find_ticket_by_customer(name, email, confirmation_number)
            
            if not ticket:
                return {
                    "success": False,
                    "error": "Sorry, I couldn't find a ticket with those details. Please check your name, email, and confirmation number."
                }
            
            # Prepare updates
            updates = {}
            
            if field == "phone":
                updates["phone"] = value
            elif field == "address":
                updates["address"] = value
            elif field == "issue":
                # Re-identify the issue and update pricing
                issue_info = identify_issue(value)
                if issue_info:
                    updates["issue"] = issue_info["description"]
                    updates["price"] = issue_info["price"]
                else:
                    return {
                        "success": False,
                        "error": "Sorry, I couldn't identify that IT issue. Please describe a common problem like Wi-Fi, email, performance, or printer issues."
                    }
            else:
                return {
                    "success": False,
                    "error": f"Sorry, I can't update the '{field}' field. You can update your phone number, address, or issue description."
                }
            
            # Update the ticket
            success = self.db.update_ticket(ticket.id, updates)
            
            if success:
                logger.info(f"Updated ticket {ticket.id} field {field} for {name} ({email})")
                
                return {
                    "success": True,
                    "field": field,
                    "value": value,
                    "ticket_id": ticket.id,
                    "message": f"Perfect! I've updated your {field}. Your ticket has been modified successfully."
                }
            else:
                return {
                    "success": False,
                    "error": "Sorry, there was an error updating your ticket. Please try again."
                }
                
        except Exception as e:
            logger.error(f"Error updating ticket: {e}")
            return {
                "success": False,
                "error": "Sorry, there was an error updating your ticket. Please try again."
            }

    def get_supported_issues(self) -> Dict[str, Any]:
        """Get information about supported IT issues."""
        issues = []
        for issue_type, config in identify_issue.__globals__["IT_ISSUES"].items():
            issues.append({
                "type": issue_type,
                "description": config["description"],
                "price": config["price"],
                "keywords": config["keywords"]
            })
        
        return {
            "success": True,
            "issues": issues
        }
