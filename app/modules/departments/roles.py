# Importing necessary libraries
from enum import Enum

# Roles departments
class DepartmentRole(Enum):
    ADMINISTRATOR = "administrator"
    MANAGER = "manager"
    OPERATOR = "operator"
    USER = "user"
    