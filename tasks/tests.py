from django.test import TestCase
# Create your tests here.
from django.urls import reverse
from django.core.management import call_command
from tasks.models import Task
import json

def tc(id):
    def decorator(func):
        setattr(func, "test_case_id", id)
        return func
    return decorator

class TaskTest(TestCase):
    def setUp(self):
        # Création d'une tâche de test
        self.task = Task.objects.create(title="Url Task")

    # Test models
    @tc("T01")
    def test_task_str(self):
        """Test du __str__"""
        self.assertEqual(str(self.task), "Url Task")

    # Test des URLs GET
    @tc("T02")
    def test_list_url(self):
        response = self.client.get(reverse("list"))  # nom de la route 'list'
        self.assertEqual(response.status_code, 200)

    @tc("T03")
    def test_update_task_url(self):
        url = reverse("update_task", args=[self.task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @tc("T04")
    def test_delete_task_url(self):
        url = reverse("delete", args=[self.task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # Test POST
    @tc("T05")
    def test_create_task_post(self):
        response = self.client.post(reverse("list"), {"title": "New task"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 2)

    @tc("T06")
    def test_update_task_post(self):
        url = reverse("update_task", args=[self.task.id])
        response = self.client.post(url, {"title": "Updated Task"})
        self.assertEqual(response.status_code, 302)
        updated = Task.objects.get(id=self.task.id)
        self.assertEqual(updated.title, "Updated Task")

    @tc("T07")
    def test_delete_task_post(self):
        url = reverse("delete", args=[self.task.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    # Test import dataset.json
    @tc("T08")
    def test_import_dataset(self):
        # Vide la base pour le test
        Task.objects.all().delete()
        self.assertEqual(Task.objects.count(), 0)

        # Appelle la commande custom Django créée : import_tasks
        call_command("import_tasks")

        # Vérifie que toutes les tâches du JSON ont été importées
        with open("tasks/dataset.json") as f:
            data = json.load(f)

        self.assertEqual(Task.objects.count(), len(data))
        titles = Task.objects.values_list("title", flat=True)
        for task_data in data:
            self.assertIn(task_data["title"], titles)
    
    # Vérifie qu'une url non existante affiche une erreur 404
    @tc("T15")
    def test_unknown_url(self):
        response = self.client.get("/inexistante")
        self.assertEqual(response.status_code, 404)


        

