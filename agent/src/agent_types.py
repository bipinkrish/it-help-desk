from typing import Literal, List
from typing_extensions import TypedDict


class UserDetails(TypedDict):
    name: str
    email: str
    phone: str
    address: str


class CreateTicketResponse(TypedDict):
    success: Literal[True]
    ticket_id: int
    confirmation_number: int
    email: str
    issue: str
    price: int


class ErrorResponse(TypedDict):
    success: Literal[False]
    error: str


class LookupTicketResponse(TypedDict):
    success: Literal[True]
    ticket: dict
    message: str


class UpdateExistingTicketResponse(TypedDict):
    success: Literal[True]
    field: str
    value: str
    ticket_id: int
    message: str


class SupportedIssueItem(TypedDict):
    type: str
    description: str
    price: int
    keywords: List[str]


class SupportedIssuesResponse(TypedDict):
    success: Literal[True]
    issues: List[SupportedIssueItem]


