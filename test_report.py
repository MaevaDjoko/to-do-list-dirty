import json
import yaml

# Lecture du cahier de tests
with open("test_list.yaml", "r", encoding="utf-8") as f:
    test_list = yaml.safe_load(f)

# Lecture résultats classiques (auto-json)
with open("result_test_auto.json", "r", encoding="utf-8") as f:
    test_results_auto = json.load(f)

# Lecture résultats Selenium
with open("result_test_selenium.json", "r", encoding="utf-8") as f:
    test_results_selenium = json.load(f)

result_dict = {
    tr["test_case_id"]: tr.get("status", "not_found")
    for tr in test_results_auto
}

selenium_status = test_results_selenium.get("status", "failed").lower()

# On l'ajoute avec la clé "auto-selenium"
result_dict["auto-selenium"] = "passed" if selenium_status == "success" else "failed"

# ---- Rapport ----

total = len(test_list)
passed = 0
failed = 0
not_found = 0
manual = 0

for test in test_list:
    test_id = test["id"]
    test_type = test["type"]
    status = result_dict.get(test_id, None)

    if test_type.startswith("auto"):
        if status == "passed":
            symbol = "✅ Passed"
            passed += 1
        elif status == "failed":
            symbol = "❌ Failed"
            failed += 1
        else:
            symbol = "🕳️ Not found"
            not_found += 1
    else:
        symbol = "🫱 Manual test needed"
        manual += 1

    print(f"{test_id} | {test_type} | {symbol}")

# --- Summary ---
def pct(n):
    return round(n / total * 100, 1)

print("\n--- Summary ---")
print(f"Number of tests: {total}")
print(f"✅ Passed tests: {passed} ({pct(passed)}%)")
print(f"❌ Failed tests: {failed} ({pct(failed)}%)")
print(f"🕳️ Not found tests: {not_found} ({pct(not_found)}%)")
print(f"🫱 Test to pass manually: {manual} ({pct(manual)}%)")
print(f"🏁 Passed + Manual: {passed + manual} ({pct(passed + manual)}%)")
