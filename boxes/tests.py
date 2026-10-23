from decimal import Decimal
from itertools import permutations

from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse

from .forms import OrderDimensionsForm
from .models import Box
from .services import recommend_box


def make_box(name, dimensions, weight="10.00", cost="5.00"):
    return Box.objects.create(
        name=name,
        internal_length=dimensions[0],
        internal_width=dimensions[1],
        internal_height=dimensions[2],
        maximum_weight=weight,
        cost=cost,
    )


class RecommendationServiceTests(TestCase):
    def test_selects_lowest_cost_eligible_box(self):
        make_box("Premium", ("10", "10", "10"), cost="9.00")
        cheapest = make_box("Budget", ("10", "10", "10"), cost="2.00")

        result = recommend_box(
            Decimal("8"), Decimal("7"), Decimal("6"), Decimal("3")
        )

        self.assertEqual(result, cheapest)

    def test_more_expensive_eligible_box_is_not_selected(self):
        cheapest = make_box("Affordable", ("12", "12", "12"), cost="3.00")
        make_box("Deluxe", ("20", "20", "20"), cost="8.00")

        result = recommend_box(
            Decimal("8"), Decimal("7"), Decimal("6"), Decimal("3")
        )

        self.assertEqual(result, cheapest)

    def test_rotation_allows_fit(self):
        rotated_box = make_box("Rotated", ("4", "8", "2"))

        result = recommend_box(
            Decimal("8"), Decimal("4"), Decimal("2"), Decimal("3")
        )

        self.assertEqual(result, rotated_box)

    def test_each_of_six_orientations_is_checked(self):
        order_dimensions = (Decimal("1"), Decimal("2"), Decimal("3"))

        for index, orientation in enumerate(permutations(order_dimensions)):
            with self.subTest(orientation=orientation):
                box = make_box(f"Orientation {index}", orientation)
                result = recommend_box(*order_dimensions, Decimal("3"))
                self.assertEqual(result, box)
                box.delete()

    def test_weight_equal_to_capacity_is_accepted(self):
        box = make_box("Exact capacity", ("10", "10", "10"), weight="4.00")

        result = recommend_box(
            Decimal("5"), Decimal("4"), Decimal("3"), Decimal("4")
        )

        self.assertEqual(result, box)

    def test_weight_above_capacity_is_rejected(self):
        make_box("Too light", ("10", "10", "10"), weight="3.99")

        result = recommend_box(
            Decimal("5"), Decimal("4"), Decimal("3"), Decimal("4")
        )

        self.assertIsNone(result)

    def test_dimension_equal_to_box_dimension_is_accepted(self):
        box = make_box("Exact fit", ("8", "7", "6"))

        result = recommend_box(
            Decimal("8"), Decimal("7"), Decimal("6"), Decimal("3")
        )

        self.assertEqual(result, box)

    def test_product_too_large_in_every_orientation_returns_no_fit(self):
        make_box("Small", ("3", "5", "8"))

        result = recommend_box(
            Decimal("4"), Decimal("5"), Decimal("8"), Decimal("3")
        )

        self.assertIsNone(result)

    def test_empty_inventory_returns_no_fit(self):
        result = recommend_box(
            Decimal("1"), Decimal("2"), Decimal("3"), Decimal("1")
        )

        self.assertIsNone(result)

    def test_equal_cost_prefers_smallest_volume(self):
        make_box("Large", ("20", "20", "20"), cost="5.00")
        smallest = make_box("Small", ("10", "10", "10"), cost="5.00")

        result = recommend_box(
            Decimal("4"), Decimal("4"), Decimal("4"), Decimal("2")
        )

        self.assertEqual(result, smallest)

    def test_equal_cost_and_volume_prefers_name_deterministically(self):
        make_box("zeta", ("10", "10", "10"), cost="5.00")
        alphabetic = make_box("Alpha", ("10", "10", "10"), cost="5.00")

        result = recommend_box(
            Decimal("4"), Decimal("4"), Decimal("4"), Decimal("2")
        )

        self.assertEqual(result, alphabetic)

    def test_casefold_name_tie_has_exact_name_fallback(self):
        make_box("alpha", ("10", "10", "10"), cost="5.00")
        uppercase = make_box("Alpha", ("10", "10", "10"), cost="5.00")

        result = recommend_box(
            Decimal("4"), Decimal("4"), Decimal("4"), Decimal("2")
        )

        self.assertEqual(result, uppercase)


class OrderDimensionsFormTests(TestCase):
    valid_data = {
        "length": "4.00",
        "width": "3.00",
        "height": "2.00",
        "weight": "1.00",
    }

    def test_missing_value_is_rejected(self):
        data = self.valid_data.copy()
        data.pop("length")

        form = OrderDimensionsForm(data)

        self.assertFalse(form.is_valid())
        self.assertIn("length", form.errors)

    def test_malformed_value_is_rejected(self):
        data = self.valid_data | {"width": "not-a-number"}

        form = OrderDimensionsForm(data)

        self.assertFalse(form.is_valid())
        self.assertIn("width", form.errors)

    def test_zero_and_negative_values_are_rejected(self):
        for field in self.valid_data:
            for invalid_value in ("0", "-1.00"):
                with self.subTest(field=field, value=invalid_value):
                    data = self.valid_data | {field: invalid_value}
                    form = OrderDimensionsForm(data)
                    self.assertFalse(form.is_valid())
                    self.assertIn(field, form.errors)


class BoxSelectionViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.box = make_box("Web box", ("10", "8", "6"), weight="5", cost="2.50")
        self.order_data = {
            "length": "8.00",
            "width": "6.00",
            "height": "4.00",
            "weight": "3.00",
        }

    def test_main_page_loads(self):
        response = self.client.get(reverse("boxes:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "What are you shipping?")

    def test_valid_post_displays_recommendation(self):
        response = self.client.post(reverse("boxes:home"), self.order_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.box.name)
        self.assertContains(response, "2.50")

    def test_no_fit_post_displays_clear_message(self):
        data = self.order_data | {"length": "30.00", "weight": "3.00"}

        response = self.client.post(reverse("boxes:home"), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No suitable box in inventory")

    def test_invalid_post_displays_validation_error(self):
        data = self.order_data | {"weight": "-1"}

        response = self.client.post(reverse("boxes:home"), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ensure this value is greater than or equal to 0.01.")
        self.assertNotContains(response, "YOUR BEST MATCH")

    def test_post_requires_csrf_token(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.get(reverse("boxes:home"))

        response = csrf_client.post(reverse("boxes:home"), self.order_data)

        self.assertEqual(response.status_code, 403)

    def test_post_with_csrf_token_succeeds(self):
        csrf_client = Client(enforce_csrf_checks=True)
        page = csrf_client.get(reverse("boxes:home"))
        token = page.cookies["csrftoken"].value

        response = csrf_client.post(
            reverse("boxes:home"),
            self.order_data,
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.box.name)


class SampleBoxCommandTests(TestCase):
    def test_sample_command_is_idempotent(self):
        call_command("load_sample_boxes")
        call_command("load_sample_boxes")

        self.assertEqual(Box.objects.count(), 3)
        self.assertEqual(
            set(Box.objects.values_list("name", flat=True)),
            {"Small", "Medium", "Large"},
        )
