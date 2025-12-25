# src/m2_test_runner.py

"""
Milestone 2 – Phase B4
Automated Test Runner for Role-Based Access
"""

from m2_test_cases import TEST_CASES
from m2_retriever import secure_retrieve


def run_tests():
    print("\n=== Milestone 2 | Automated Test Runner ===\n")

    passed = 0
    failed = 0

    for test in TEST_CASES:
        print(f"Running Test {test['id']}: {test['description']}")
        results = secure_retrieve(
            query=test["query"],
            user_role=test["role"],
            top_k=3
        )

        if test["expected_result"] == "ALLOW":
            if len(results) > 0:
                print(f"✅ PASS: Access allowed as expected\n")
                passed += 1
            else:
                print(f"❌ FAIL: Expected access but got no results\n")
                failed += 1

        elif test["expected_result"] == "DENY":
            if len(results) == 0:
                print(f"✅ PASS: Access denied as expected\n")
                passed += 1
            else:
                print(f"❌ FAIL: Unauthorized data was returned\n")
                failed += 1

        else:
            print(f"⚠️ Invalid expected_result value in test {test['id']}")
            failed += 1

    print("\n=== TEST SUMMARY ===")
    print(f"Total Tests: {len(TEST_CASES)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed == 0:
        print("\n🎉 ALL TESTS PASSED – Role-based access is SECURE\n")
    else:
        print("\n🚨 SOME TESTS FAILED – Review access rules\n")


if __name__ == "__main__":
    run_tests()
