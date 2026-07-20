# Importing necessary libraries
from enum import Enum

# Tickets Priorities
class TicketPriority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"
    