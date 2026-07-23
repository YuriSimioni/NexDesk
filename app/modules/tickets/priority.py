# Importing necessary libraries
from enum import Enum

# Tickets Priorities
class TicketPriority(Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    URGENT = "URGENT"
    CRITICAL = "CRITICAL"
    