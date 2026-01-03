# src/m2_test_runner.py

from m2_test_cases import TEST_CASES
from m2_retriever import secure_retrieve


def run_tests():
    print("\n=== Milestone 2 | Test Runner ===\n")

    passed = 0

    for test in TEST_CASES:
        print(f"Running {test['id']}...")
        results = secure_retrieve(test["query"], test["role"])

        if test["expected"] == "ALLOW" and results:
            print("✅ PASS\n")
            passed += 1
        elif test["expected"] == "DENY" and not results:
            print("✅ PASS\n")
            passed += 1
        else:
            print("❌ FAIL\n")

    print(f"Passed {passed}/{len(TEST_CASES)} tests")


if __name__ == "__main__":
    run_tests()
