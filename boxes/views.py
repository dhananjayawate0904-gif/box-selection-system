from django.shortcuts import render

from .forms import OrderDimensionsForm
from .services import recommend_box


def home(request):
    form = OrderDimensionsForm(request.POST or None)
    recommendation = None
    searched = request.method == "POST"

    if request.method == "POST" and form.is_valid():
        recommendation = recommend_box(
            length=form.cleaned_data["length"],
            width=form.cleaned_data["width"],
            height=form.cleaned_data["height"],
            weight=form.cleaned_data["weight"],
        )

    return render(
        request,
        "boxes/home.html",
        {
            "form": form,
            "recommendation": recommendation,
            "searched": searched and form.is_valid(),
        },
    )
