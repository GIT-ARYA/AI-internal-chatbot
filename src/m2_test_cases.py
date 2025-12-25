# src/m2_test_cases.py

"""
Milestone 2 – Phase B3
Test Scenarios Definition
"""

TEST_CASES = [
    {
        "id": "T1",
        "description": "Finance user accessing finance documents",
        "query": "quarterly financial performance",
        "role": "Finance",
        "expected_result": "ALLOW"
    },
    {
        "id": "T2",
        "description": "Marketing user trying to access finance documents",
        "query": "quarterly financial performance",
        "role": "Marketing",
        "expected_result": "DENY"
    },
    {
        "id": "T3",
        "description": "Engineering user accessing engineering docs",
        "query": "engineering architecture",
        "role": "Engineering",
        "expected_result": "ALLOW"
    },
    {
        "id": "T4",
        "description": "Employee trying to access finance data",
        "query": "financial summary",
        "role": "Employees",
        "expected_result": "DENY"
    },
    {
        "id": "T5",
        "description": "C-Level accessing HR data",
        "query": "employee policies",
        "role": "C-Level",
        "expected_result": "ALLOW"
    }
]
