from django.core.management.base import BaseCommand

from boxes.models import Box


SAMPLE_BOXES = (
    {
        "name": "Small Flat",
        "internal_length": "15.24",
        "internal_width": "10.16",
        "internal_height": "10.16",
        "maximum_weight": "2.00",
        "cost": "10.00",
    },
    {
        "name": "Mailer Small",
        "internal_length": "22.86",
        "internal_width": "15.24",
        "internal_height": "7.62",
        "maximum_weight": "3.00",
        "cost": "14.00",
    },
    {
        "name": "Garment Flat",
        "internal_length": "30.48",
        "internal_width": "22.86",
        "internal_height": "10.16",
        "maximum_weight": "5.00",
        "cost": "18.00",
    },
    {
        "name": "Standard Small",
        "internal_length": "25.40",
        "internal_width": "20.32",
        "internal_height": "15.24",
        "maximum_weight": "6.00",
        "cost": "20.00",
    },
    {
        "name": "Standard Cube",
        "internal_length": "30.48",
        "internal_width": "25.40",
        "internal_height": "25.40",
        "maximum_weight": "8.00",
        "cost": "26.00",
    },
    {
        "name": "Multi-Item",
        "internal_length": "35.56",
        "internal_width": "25.40",
        "internal_height": "15.24",
        "maximum_weight": "10.00",
        "cost": "32.00",
    },
    {
        "name": "Medium",
        "internal_length": "40.64",
        "internal_width": "30.48",
        "internal_height": "20.32",
        "maximum_weight": "15.00",
        "cost": "40.00",
    },
    {
        "name": "Tall Medium",
        "internal_length": "40.64",
        "internal_width": "25.40",
        "internal_height": "30.48",
        "maximum_weight": "15.00",
        "cost": "42.00",
    },
    {
        "name": "Large",
        "internal_length": "60.96",
        "internal_width": "45.72",
        "internal_height": "30.48",
        "maximum_weight": "25.00",
        "cost": "65.00",
    },
    {
        "name": "Large Flat",
        "internal_length": "60.96",
        "internal_width": "38.10",
        "internal_height": "25.40",
        "maximum_weight": "25.00",
        "cost": "60.00",
    },
    {
        "name": "Extra-Large Flat (custom)",
        "internal_length": "71.12",
        "internal_width": "60.96",
        "internal_height": "10.16",
        "maximum_weight": "20.00",
        "cost": "70.00",
    },
)

LEGACY_SAMPLE_BOXES = (
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
    help = "Create or update the 11-box sample shipping size chart."

    def handle(self, *args, **options):
        for legacy in LEGACY_SAMPLE_BOXES:
            Box.objects.filter(**legacy).delete()

        for sample in SAMPLE_BOXES:
            name = sample["name"]
            defaults = {key: value for key, value in sample.items() if key != "name"}
            _, created = Box.objects.update_or_create(name=name, defaults=defaults)
            action = "Created" if created else "Updated"
            self.stdout.write(f"{action} sample box: {name}")
