from django.core.management.base import BaseCommand

from boxes.models import Box


SAMPLE_BOXES = (
    {
        "name": "Small",
        "internal_length": "20.00",
        "internal_width": "15.00",
        "internal_height": "10.00",
        "maximum_weight": "5.00",
        "cost": "2.50",
    },
    {
        "name": "Medium",
        "internal_length": "40.00",
        "internal_width": "30.00",
        "internal_height": "20.00",
        "maximum_weight": "15.00",
        "cost": "4.75",
    },
    {
        "name": "Large",
        "internal_length": "60.00",
        "internal_width": "45.00",
        "internal_height": "35.00",
        "maximum_weight": "30.00",
        "cost": "7.25",
    },
)


class Command(BaseCommand):
    help = "Create or update the reproducible sample box inventory."

    def handle(self, *args, **options):
        for sample in SAMPLE_BOXES:
            name = sample["name"]
            defaults = {key: value for key, value in sample.items() if key != "name"}
            _, created = Box.objects.update_or_create(name=name, defaults=defaults)
            action = "Created" if created else "Updated"
            self.stdout.write(f"{action} sample box: {name}")
