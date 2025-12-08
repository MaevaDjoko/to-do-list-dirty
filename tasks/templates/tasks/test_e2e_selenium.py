from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from functools import wraps

# URL de votre instance de dev
BASE_URL = "http://127.0.0.1:8000"

# Liste pour stocker les résultats
results = []

# Décorateur pour associer un test à un test_case_id
def tc(test_case_id):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
                results.append({
                    "test_case_id": test_case_id,
                    "name": func.__name__,
                    "status": "passed"
                })
                print(f"{test_case_id} | {func.__name__} | passed")
            except Exception as e:
                results.append({
                    "test_case_id": test_case_id,
                    "name": func.__name__,
                    "status": "failed"
                })
                print(f"{test_case_id} | {func.__name__} | failed")
        return wrapper
    return decorator

# Initialisation du navigateur
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Fonction utilitaire pour récupérer l'ID de la dernière tâche
def get_last_task_id():
    task_rows = driver.find_elements(By.CSS_SELECTOR, ".item-row")
    return task_rows[-1].get_attribute("data-task-id") if task_rows else None

try:

    @tc("T17")
    def test_load_homepage():
        driver.get(BASE_URL)
        time.sleep(1)
        assert len(driver.find_elements(By.CSS_SELECTOR, ".item-row")) >= 0

    @tc("T18")
    def test_create_two_tasks():
        for i in range(2):
            input_box = driver.find_element(By.NAME, "title")
            input_box.clear()
            input_box.send_keys(f"Tâche Selenium {i+1}")
            input_box.send_keys(Keys.RETURN)
            time.sleep(0.2)

    @tc("T19")
    def test_delete_two_tasks():
        for i in range(2):
            delete_btn = driver.find_elements(By.CSS_SELECTOR, ".btn.btn-sm.btn-danger")[-1]
            delete_btn.click()
            submit_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']"))
            )
            submit_btn.click()
            time.sleep(0.3)

    @tc("T20")
    def test_cross_impact():
        # Ajouter tâche A
        input_box = driver.find_element(By.NAME, "title")
        input_box.send_keys("Tâche A - Selenium")
        input_box.send_keys(Keys.RETURN)
        time.sleep(0.5)
        taskA_id = get_last_task_id()

        # Ajouter tâche B
        input_box = driver.find_element(By.NAME, "title")
        input_box.send_keys("Tâche B - Selenium")
        input_box.send_keys(Keys.RETURN)
        time.sleep(0.5)
        taskB_id = get_last_task_id()

        # Supprimer tâche B
        delete_btn = driver.find_element(
            By.CSS_SELECTOR, f"[data-task-id='{taskB_id}'] a.btn.btn-sm.btn-danger"
        )
        delete_btn.click()
        submit_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']"))
        )
        submit_btn.click()
        time.sleep(0.5)

        # Vérifier que tâche A existe toujours
        remaining = driver.find_elements(By.CSS_SELECTOR, f"[data-task-id='{taskA_id}']")
        assert len(remaining) > 0, "Tâche B a été supprimée !"

    @tc("T21")
    def test_create_priority_task():
        input_box = driver.find_element(By.NAME, "title")
        input_box.clear()
        input_box.send_keys("Tâche prioritaire test")

        # cocher la case prioritaire
        checkbox = driver.find_element(By.NAME, "priority")
        checkbox.click()

        input_box.send_keys(Keys.RETURN)
        time.sleep(0.5)

    @tc("T22")
    def test_priority_task_order():
        task_rows = driver.find_elements(By.CSS_SELECTOR, ".item-row")
        first_task_title = task_rows[0].text
        assert "Tâche prioritaire test" in first_task_title, "La tâche prioritaire n'est pas en haut"

    # Exécution des tests
    test_load_homepage()
    test_create_two_tasks()
    test_delete_two_tasks()
    test_cross_impact()
    test_create_priority_task()
    test_priority_task_order()

finally:
    # Sauvegarde des résultats dans le format attendu
    with open("../../../result_test_selenium.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    driver.quit()
