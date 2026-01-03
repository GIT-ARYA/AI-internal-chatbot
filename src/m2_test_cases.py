# src/m2_test_cases.py

TEST_CASES = [
    {
        "id": "T1",
        "query": "quarterly financial report",
        "role": "Finance",
        "expected": "ALLOW"
    },
    {
        "id": "T2",
        "query": "quarterly financial report",
        "role": "Marketing",
        "expected": "DENY"
    },
    {
        "id": "T3",
        "query": "engineering architecture",
        "role": "Engineering",
        "expected": "ALLOW"
    },
    {
        "id": "T4",
        "query": "financial summary",
        "role": "Employees",
        "expected": "DENY"
    },
    {
        "id": "T5",
        "query": "employee policies",
        "role": "C-Level",
        "expected": "ALLOW"
    }
]
