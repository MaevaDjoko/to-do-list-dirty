from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# URL de votre instance de dev
BASE_URL = "http://127.0.0.1:8000"

# Structure qui contiendra les résultats
results = {
    "test_case_id": "auto-selenium",
    "tests": [],
    "status": "SUCCESS"
}

# Initialisation du navigateur
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def get_last_task_id():
    # Récupère l’ID de la dernière tâche
    task_rows = driver.find_elements(By.CSS_SELECTOR, ".item-row")
    last = task_rows[-1]
    return last.get_attribute("data-task-id")

def save(status, message):
    results["tests"].append({"status": status, "message": message})
    print(status, message)

try:
    # ---- Test 1 : Accéder à la page principale ----
    driver.get(BASE_URL)
    time.sleep(1)

    tasks = driver.find_elements(By.CSS_SELECTOR, ".item-row")
    initial_count = len(tasks)

    results["tests"].append({
        "name": "Chargement de la page principale",
        "result": "SUCCESS",
        "initial_tasks": initial_count
    })

    # ---- Test 2 : Création de 2 tâches ----
    try:
        for i in range(2):
            input_box = driver.find_element(By.NAME, "title")
            input_box.clear()
            input_box.send_keys(f"Tâche Selenium {i+1}")
            input_box.send_keys(Keys.RETURN)
            time.sleep(0.2)

        tasks = driver.find_elements(By.CSS_SELECTOR, ".item-row")

        results["tests"].append({
            "name": "Création des tâches",
            "result": "SUCCESS",
            "count_after_creation": len(tasks)
        })
    except Exception as e:
        results["tests"].append({
            "name": "Création des tâches",
            "result": "FAIL",
            "error": str(e)
        })
        results["status"] = "FAIL"

    # ---- Test 3 : Suppression des tâches ----
    try:
        for i in range(2):
            delete_button = driver.find_elements(By.CSS_SELECTOR, ".btn.btn-sm.btn-danger")[-1]
            delete_button.click()
            time.sleep(0.4)

            submit_btn = WebDriverWait(driver, 6).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']"))
            )
            submit_btn.click()
            time.sleep(0.4)

        tasks = driver.find_elements(By.CSS_SELECTOR, ".item-row")

        results["tests"].append({
            "name": "Suppression des tâches",
            "result": "SUCCESS",
            "count_after_delete": len(tasks)
        })
    except Exception as e:
        results["tests"].append({
            "name": "Suppression des tâches",
            "result": "FAIL",
            "error": str(e)
        })
        results["status"] = "FAIL"

    # ---- Test 4 : Vérification impacts croisés ----
    # Ajout tâche A
    input_box = driver.find_element(By.NAME, "title")
    input_box.send_keys("Tâche A - Selenium")
    input_box.send_keys(Keys.RETURN)
    time.sleep(0.5)

    taskA_id = get_last_task_id()
    save("OK", f"Tâche A ajoutée avec ID={taskA_id}")

    # Ajout tâche B
    input_box = driver.find_element(By.NAME, "title")
    input_box.send_keys("Tâche B - Selenium")
    input_box.send_keys(Keys.RETURN)
    time.sleep(0.5)

    taskB_id = get_last_task_id()
    save("OK", f"Tâche B ajoutée avec ID={taskB_id}")

    # Suppression tâche B
    delete_btn = driver.find_element(
        By.CSS_SELECTOR, f"[data-task-id='{taskB_id}'] a.btn.btn-sm.btn-danger"
    )
    delete_btn.click()

    submit_btn = WebDriverWait(driver, 4).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']"))
    )
    submit_btn.click()
    time.sleep(0.5)

    save("OK", f"Tâche B (ID={taskB_id}) supprimée")

    # Vérification : tâche A doit encore exister
    remaining = driver.find_elements(
        By.CSS_SELECTOR, f"[data-task-id='{taskA_id}']"
    )

    if len(remaining) == 0:
        raise Exception("La tâche A n’existe plus !")

    save("OK", f"Tâche A (ID={taskA_id}) toujours présente")

    results["status"] = "SUCCESS"

except Exception as e:
    save("ERROR", str(e))
    results["status"] = "FAILED"

finally:
    # Sauvegarde JSON des résultats
    with open("../../../result_test_selenium.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    driver.quit()
