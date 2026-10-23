from decimal import Decimal

from django import forms


class OrderDimensionsForm(forms.Form):
    length = forms.DecimalField(
        label="Length",
        min_value=Decimal("0.01"),
        max_digits=8,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"step": "0.01", "min": "0.01"}),
    )
    width = forms.DecimalField(
        label="Width",
        min_value=Decimal("0.01"),
        max_digits=8,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"step": "0.01", "min": "0.01"}),
    )
    height = forms.DecimalField(
        label="Height",
        min_value=Decimal("0.01"),
        max_digits=8,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"step": "0.01", "min": "0.01"}),
    )
    weight = forms.DecimalField(
        label="Weight",
        min_value=Decimal("0.01"),
        max_digits=8,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"step": "0.01", "min": "0.01"}),
    )
