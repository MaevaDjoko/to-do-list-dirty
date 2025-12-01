import os
import sys
import json
import django
from django.conf import settings
from django.test.utils import get_runner

# Définir le module settings de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todo.settings")

# Configurer Django
django.setup()

# Importer les tests après que Django soit configuré
from tasks.tests import TaskTest

# Récupérer le test runner
TestRunner = get_runner(settings)
test_runner = TestRunner()

# Lancer les tests
failures = test_runner.run_tests(["tasks"])

# Récupérer les IDs des tests décorés
results = []
for attr_name in dir(TaskTest):
    attr = getattr(TaskTest, attr_name)
    if callable(attr) and hasattr(attr, "test_case_id"):
        results.append({
            "test_case_id": attr.test_case_id,
            "name": attr_name,
            "status": "passed" if not failures else "failed"
        })

# Écrire le JSON
with open("result_test_auto.json", "w") as f:
    json.dump(results, f, indent=2)

# Quitter avec code de sortie
sys.exit(bool(failures))
