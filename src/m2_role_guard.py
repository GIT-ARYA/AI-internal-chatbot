# src/m2_role_guard.py

"""
Milestone 2 – Module 4
Role-Based Access Control
"""

ROLE_ACCESS = {
    "Employees": ["Employees"],
    "HR": ["HR"],
    "Finance": ["Finance"],
    "Marketing": ["Marketing"],
    "Engineering": ["Engineering"],
    "C-Level": ["Employees", "HR", "Finance", "Marketing", "Engineering"]
}


def validate_role(role):
    if role not in ROLE_ACCESS:
        raise ValueError(f"Invalid role: {role}")


def get_allowed_roles(role):
    validate_role(role)
    return ROLE_ACCESS[role]


def is_access_allowed(user_role, doc_role):
    return doc_role in get_allowed_roles(user_role)


if __name__ == "__main__":
    print("Finance → HR:", is_access_allowed("Finance", "HR"))
    print("C-Level → HR:", is_access_allowed("C-Level", "HR"))
