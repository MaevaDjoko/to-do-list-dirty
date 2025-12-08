import json
from django.core.management.base import BaseCommand
from tasks.models import Task


class Command(BaseCommand):
    help = "Import tasks from dataset.json"

    def handle(self, *args, **kwargs):
        with open("tasks/dataset.json") as f:
            data = json.load(f)
            for task_data in data:
                Task.objects.create(**task_data)
        self.stdout.write(self.style.SUCCESS(f"Imported {len(data)} tasks"))
