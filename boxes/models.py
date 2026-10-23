from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q


class Box(models.Model):
    name = models.CharField("box name", max_length=100, unique=True)
    internal_length = models.DecimalField(
        "internal length (cm)",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    internal_width = models.DecimalField(
        "internal width (cm)",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    internal_height = models.DecimalField(
        "internal height (cm)",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    maximum_weight = models.DecimalField(
        "maximum weight (kg)",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    cost = models.DecimalField(
        "cost",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    class Meta:
        ordering = ["name"]
        constraints = [
            models.CheckConstraint(
                condition=Q(internal_length__gt=0),
                name="box_length_positive",
            ),
            models.CheckConstraint(
                condition=Q(internal_width__gt=0),
                name="box_width_positive",
            ),
            models.CheckConstraint(
                condition=Q(internal_height__gt=0),
                name="box_height_positive",
            ),
            models.CheckConstraint(
                condition=Q(maximum_weight__gt=0),
                name="box_maximum_weight_positive",
            ),
            models.CheckConstraint(condition=Q(cost__gt=0), name="box_cost_positive"),
        ]

    @property
    def internal_volume(self):
        return self.internal_length * self.internal_width * self.internal_height

    def __str__(self):
        return self.name
