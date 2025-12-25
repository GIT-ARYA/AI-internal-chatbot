# src/m2_role_guard.py

"""
Milestone 2 – Phase B1
Role-Based Access Guard
"""

# Role hierarchy definition
ROLE_ACCESS_MAP = {
    "Employees": ["Employees"],
    "HR": ["HR"],
    "Finance": ["Finance"],
    "Marketing": ["Marketing"],
    "Engineering": ["Engineering"],
    "C-Level": ["Employees", "HR", "Finance", "Marketing", "Engineering"]
}


def validate_role(role: str):
    """
    Validates if the given role exists in the system.
    """
    if role not in ROLE_ACCESS_MAP:
        raise ValueError(f"Invalid role: {role}")


def get_allowed_roles(role: str):
    """
    Returns the list of roles the user is allowed to access.
    """
    validate_role(role)
    return ROLE_ACCESS_MAP[role]


def is_access_allowed(user_role: str, document_role: str) -> bool:
    """
    Checks if a user role can access a document role.
    """
    allowed_roles = get_allowed_roles(user_role)
    return document_role in allowed_roles


def demo():
    print("\n=== Role Guard Demo ===")
    tests = [
        ("Finance", "Finance"),
        ("Finance", "HR"),
        ("C-Level", "HR"),
        ("Employees", "Finance"),
    ]

    for user_role, doc_role in tests:
        allowed = is_access_allowed(user_role, doc_role)
        print(f"User: {user_role} | Doc: {doc_role} → Access: {allowed}")


if __name__ == "__main__":
    demo()
