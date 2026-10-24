from django.shortcuts import render

from .forms import OrderDimensionsForm
from .models import Box
from .services import recommend_box
from .units import format_all_units


UNIT_LABELS = {"mm": "mm", "cm": "cm", "m": "m", "in": "in"}


def _format_dimension(value):
    return format(value.normalize(), "f")


def _format_box_dimensions(box):
    converted_dimensions = tuple(
        format_all_units(value)
        for value in (
            box.internal_length,
            box.internal_width,
            box.internal_height,
        )
    )
    return {
        unit: " × ".join(
            _format_dimension(dimension[unit]) for dimension in converted_dimensions
        )
        for unit in ("mm", "cm", "m", "in")
    }


def home(request):
    form = OrderDimensionsForm(request.POST or None)
    recommendation = None
    recommended_dimensions = None
    selected_unit = form["unit"].value() or "cm"
    searched = request.method == "POST"

    if request.method == "POST" and form.is_valid():
        length, width, height = form.cleaned_data["dimensions_cm"]
        recommendation = recommend_box(
            length=length,
            width=width,
            height=height,
            weight=form.cleaned_data["weight"],
        )
        if recommendation:
            dimensions_by_unit = _format_box_dimensions(recommendation)
            recommended_dimensions = [
                {
                    "label": UNIT_LABELS[unit],
                    "dimensions": dimensions_by_unit[unit],
                }
                for unit in ("mm", "cm", "m", "in")
            ]

    return render(
        request,
        "boxes/home.html",
        {
            "form": form,
            "recommendation": recommendation,
            "recommended_dimensions": recommended_dimensions,
            "selected_unit_label": UNIT_LABELS.get(selected_unit, "cm"),
            "searched": searched and form.is_valid(),
        },
    )


def size_chart(request):
    return render(
        request,
        "boxes/size_chart.html",
        {
            "box_rows": [
                {"box": box, "dimensions": _format_box_dimensions(box)}
                for box in Box.objects.all()
            ]
        },
    )
