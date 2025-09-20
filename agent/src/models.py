"""Database models for the IT Help Desk system."""

import sqlite3
from typing import Optional, List, Dict, Any
from dataclasses import dataclass


@dataclass
class Ticket:
    """Represents a support ticket."""
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    issue: Optional[str] = None
    price: Optional[int] = None
    created_at: Optional[str] = None


class TicketDatabase:
    """Handles database operations for tickets."""
    
    def __init__(self, db_path: str = "tickets.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize the database with the tickets table."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                phone TEXT,
                address TEXT,
                issue TEXT,
                price INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_ticket(self, ticket: Ticket) -> int:
        """Create a new ticket and return its ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO tickets (name, email, phone, address, issue, price)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ticket.name, ticket.email, ticket.phone, ticket.address, ticket.issue, ticket.price))
        
        ticket_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return ticket_id
    
    def get_ticket(self, ticket_id: int) -> Optional[Ticket]:
        """Get a ticket by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, email, phone, address, issue, price, created_at
            FROM tickets WHERE id = ?
        """, (ticket_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Ticket(
                id=row[0],
                name=row[1],
                email=row[2],
                phone=row[3],
                address=row[4],
                issue=row[5],
                price=row[6],
                created_at=row[7]
            )
        return None
    
    def update_ticket(self, ticket_id: int, updates: Dict[str, Any]) -> bool:
        """Update a ticket with new information."""
        if not updates:
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build dynamic UPDATE query
        set_clauses = []
        values = []
        
        for key, value in updates.items():
            if key in ['name', 'email', 'phone', 'address', 'issue', 'price']:
                set_clauses.append(f"{key} = ?")
                values.append(value)
        
        if not set_clauses:
            conn.close()
            return False
        
        values.append(ticket_id)
        query = f"UPDATE tickets SET {', '.join(set_clauses)} WHERE id = ?"
        
        cursor.execute(query, values)
        updated = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return updated
    
    def get_all_tickets(self) -> List[Ticket]:
        """Get all tickets."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, email, phone, address, issue, price, created_at
            FROM tickets ORDER BY created_at DESC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            Ticket(
                id=row[0],
                name=row[1],
                email=row[2],
                phone=row[3],
                address=row[4],
                issue=row[5],
                price=row[6],
                created_at=row[7]
            )
            for row in rows
        ]
    
    def delete_ticket(self, ticket_id: int) -> bool:
        """Delete a ticket by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted


# IT Issue configurations with pricing
IT_ISSUES = {
    "wifi": {
        "keywords": ["wifi", "wi-fi", "wireless", "internet", "connection", "network"],
        "description": "Wi-Fi not working",
        "price": 20
    },
    "email": {
        "keywords": ["email", "login", "password", "reset", "account", "access"],
        "description": "Email login issues - password reset",
        "price": 15
    },
    "laptop": {
        "keywords": ["laptop", "slow", "performance", "cpu", "speed", "computer", "pc"],
        "description": "Slow laptop performance - CPU change",
        "price": 25
    },
    "printer": {
        "keywords": ["printer", "printing", "power", "plug", "cable", "hardware"],
        "description": "Printer problems - power plug change",
        "price": 10
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
