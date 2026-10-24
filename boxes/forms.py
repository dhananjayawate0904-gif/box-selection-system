from decimal import Decimal

from django import forms

from .units import to_cm


DIMENSION_UNITS = (
    ("mm", "Millimetres (mm)"),
    ("cm", "Centimetres (cm)"),
    ("m", "Metres (m)"),
    ("in", "Inches (in)"),
)
MIN_DIMENSION_CM = Decimal("0.01")
MIN_INPUT_DIMENSION = Decimal("0.0001")


class OrderDimensionsForm(forms.Form):
    length = forms.DecimalField(
        label="Length",
        min_value=MIN_INPUT_DIMENSION,
        max_digits=10,
        decimal_places=4,
        widget=forms.NumberInput(attrs={"step": "0.0001", "min": "0.0001"}),
    )
    width = forms.DecimalField(
        label="Width",
        min_value=MIN_INPUT_DIMENSION,
        max_digits=10,
        decimal_places=4,
        widget=forms.NumberInput(attrs={"step": "0.0001", "min": "0.0001"}),
    )
    height = forms.DecimalField(
        label="Height",
        min_value=MIN_INPUT_DIMENSION,
        max_digits=10,
        decimal_places=4,
        widget=forms.NumberInput(attrs={"step": "0.0001", "min": "0.0001"}),
    )
    unit = forms.ChoiceField(
        label="Dimension unit",
        choices=(("", "Select a unit"),) + DIMENSION_UNITS,
        initial="cm",
        widget=forms.Select(),
    )
    weight = forms.DecimalField(
        label="Weight",
        min_value=Decimal("0.01"),
        max_digits=8,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"step": "0.01", "min": "0.01"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        unit = cleaned_data.get("unit")
        dimensions = (
            cleaned_data.get("length"),
            cleaned_data.get("width"),
            cleaned_data.get("height"),
        )
        if unit and all(dimension is not None for dimension in dimensions):
            dimensions_cm = tuple(to_cm(dimension, unit) for dimension in dimensions)
            for field_name, dimension_cm in zip(
                ("length", "width", "height"), dimensions_cm
            ):
                if dimension_cm < MIN_DIMENSION_CM:
                    self.add_error(
                        field_name,
                        "Ensure this dimension is at least 0.01 cm.",
                    )
            cleaned_data["dimensions_cm"] = dimensions_cm
        return cleaned_data
