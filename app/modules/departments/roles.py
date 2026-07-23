# Importing necessary libraries
from enum import Enum

# Roles departments
class DepartmentRole(Enum):
    ADMINISTRATOR = "ADMINISTRATOR"
    MANAGER = "MANAGER"
    OPERATOR = "OPERATOR"
    USER = "USER"
    