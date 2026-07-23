# Importing necessary libraries
from enum import Enum

# Ticket status
class TicketStatus(Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"
    CANCELED = "CANCELED" 