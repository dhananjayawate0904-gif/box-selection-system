from itertools import permutations

from .models import Box


def recommend_box(length, width, height, weight, boxes=None):
    """Return the cheapest box that fits the order, or None when none qualify."""
    if boxes is None:
        boxes = Box.objects.all()

    order_orientations = tuple(permutations((length, width, height)))
    eligible_boxes = []

    for box in boxes:
        if weight > box.maximum_weight:
            continue

        box_dimensions = (
            box.internal_length,
            box.internal_width,
            box.internal_height,
        )
        fits = any(
            all(
                order_side <= box_side
                for order_side, box_side in zip(orientation, box_dimensions)
            )
            for orientation in order_orientations
        )
        if fits:
            eligible_boxes.append(box)

    if not eligible_boxes:
        return None

    return min(
        eligible_boxes,
        key=lambda box: (
            box.cost,
            box.internal_volume,
            box.name.casefold(),
            box.name,
        ),
    )
