from decimal import Decimal
from itertools import permutations

from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse

from .forms import OrderDimensionsForm
from .models import Box
from .services import recommend_box
from .units import format_all_units, from_cm, to_cm


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


class UnitConversionTests(TestCase):
    def test_to_cm_uses_exact_decimal_conversions(self):
        cases = (
            ("10", "mm", "1"),
            ("30.48", "cm", "30.48"),
            ("0.3048", "m", "30.48"),
            ("12", "in", "30.48"),
        )
        for value, unit, expected in cases:
            with self.subTest(unit=unit):
                self.assertEqual(to_cm(Decimal(value), unit), Decimal(expected))

    def test_from_cm_uses_exact_decimal_conversions(self):
        cases = (
            ("2.54", "mm", "25.4"),
            ("30.48", "cm", "30.48"),
            ("30.48", "m", "0.3048"),
            ("30.48", "in", "12"),
        )
        for value, unit, expected in cases:
            with self.subTest(unit=unit):
                self.assertEqual(from_cm(Decimal(value), unit), Decimal(expected))

    def test_format_all_units_returns_decimal_values(self):
        values = format_all_units(Decimal("30.48"))

        self.assertEqual(values, {
            "mm": Decimal("304.80"),
            "cm": Decimal("30.48"),
            "m": Decimal("0.3048"),
            "in": Decimal("12.00000000000000000000000000"),
        })
        self.assertTrue(all(isinstance(value, Decimal) for value in values.values()))

    def test_round_trip_preserves_values_for_each_unit(self):
        values = (("304.8", "mm"), ("30.48", "cm"), ("0.3048", "m"), ("12", "in"))
        for value, unit in values:
            with self.subTest(unit=unit):
                self.assertEqual(
                    from_cm(to_cm(Decimal(value), unit), unit),
                    Decimal(value),
                )

    def test_invalid_unit_raises_clear_value_error(self):
        with self.assertRaisesRegex(ValueError, "Unknown dimension unit"):
            to_cm(Decimal("1"), "yards")

    def test_float_values_are_not_accepted(self):
        with self.assertRaisesRegex(TypeError, "Decimal, not float"):
            to_cm(1.0, "cm")


class OrderDimensionsFormTests(TestCase):
    valid_data = {
        "length": "4.00",
        "width": "3.00",
        "height": "2.00",
        "weight": "1.00",
        "unit": "cm",
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
        for field in ("length", "width", "height", "weight"):
            for invalid_value in ("0", "-1.00"):
                with self.subTest(field=field, value=invalid_value):
                    data = self.valid_data | {field: invalid_value}
                    form = OrderDimensionsForm(data)
                    self.assertFalse(form.is_valid())
                    self.assertIn(field, form.errors)

    def test_unit_defaults_to_centimetres(self):
        form = OrderDimensionsForm()

        self.assertEqual(form["unit"].value(), "cm")

    def test_each_unit_converts_form_dimensions_to_centimetres(self):
        cases = (
            ("mm", "304.8"),
            ("cm", "30.48"),
            ("m", "0.3048"),
            ("in", "12"),
        )
        for unit, value in cases:
            with self.subTest(unit=unit):
                data = {
                    "length": value,
                    "width": value,
                    "height": value,
                    "weight": "1.00",
                    "unit": unit,
                }
                form = OrderDimensionsForm(data)
                self.assertTrue(form.is_valid(), form.errors)
                self.assertEqual(
                    form.cleaned_data["dimensions_cm"],
                    (Decimal("30.48"),) * 3,
                )

    def test_minimum_dimension_is_validated_in_canonical_centimetres(self):
        accepted = OrderDimensionsForm({
            "length": "0.0001",
            "width": "0.0001",
            "height": "0.0001",
            "weight": "1",
            "unit": "m",
        })
        rejected = OrderDimensionsForm({
            "length": "0.001",
            "width": "1",
            "height": "1",
            "weight": "1",
            "unit": "cm",
        })

        self.assertTrue(accepted.is_valid(), accepted.errors)
        self.assertEqual(
            accepted.cleaned_data["dimensions_cm"],
            (Decimal("0.0100"),) * 3,
        )
        self.assertFalse(rejected.is_valid())
        self.assertIn("length", rejected.errors)

    def test_equivalent_dimensions_in_each_unit_recommend_the_same_box(self):
        matching_box = make_box("Equivalent dimensions", ("31", "31", "31"))
        cases = (
            ("mm", "304.8"),
            ("cm", "30.48"),
            ("m", "0.3048"),
            ("in", "12"),
        )

        for unit, value in cases:
            with self.subTest(unit=unit):
                data = {
                    "length": value,
                    "width": value,
                    "height": value,
                    "weight": "1.00",
                    "unit": unit,
                }
                form = OrderDimensionsForm(data)
                self.assertTrue(form.is_valid(), form.errors)
                result = recommend_box(
                    *form.cleaned_data["dimensions_cm"],
                    form.cleaned_data["weight"],
                )
                self.assertEqual(result, matching_box)

    def test_missing_and_unknown_units_are_rejected(self):
        for unit in (None, "yards"):
            with self.subTest(unit=unit):
                data = self.valid_data.copy()
                if unit is None:
                    data.pop("unit")
                else:
                    data["unit"] = unit
                form = OrderDimensionsForm(data)
                self.assertFalse(form.is_valid())
                self.assertIn("unit", form.errors)


class BoxSelectionViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.box = make_box("Web box", ("10", "8", "6"), weight="5", cost="2.50")
        self.order_data = {
            "length": "8.00",
            "width": "6.00",
            "height": "4.00",
            "weight": "3.00",
            "unit": "cm",
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

    def test_result_displays_dimensions_in_all_units(self):
        response = self.client.post(reverse("boxes:home"), self.order_data)

        self.assertEqual(response.status_code, 200)
        for unit in ("mm", "cm", "m", "in"):
            with self.subTest(unit=unit):
                self.assertContains(response, f"Internal dimensions ({unit})")

    def test_inches_post_returns_the_matching_box(self):
        standard_small = make_box(
            "Standard Small",
            ("25.40", "20.32", "15.24"),
            weight="6.00",
            cost="20.00",
        )
        data = {
            "length": "10",
            "width": "8",
            "height": "6",
            "weight": "2",
            "unit": "in",
        }

        response = self.client.post(reverse("boxes:home"), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, standard_small.name)

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

        self.assertEqual(Box.objects.count(), 11)
        self.assertEqual(
            Box.objects.values_list("cost", flat=True).distinct().count(),
            11,
        )

    def test_sample_command_replaces_unchanged_legacy_demo_rows(self):
        for name, dimensions, weight, cost in (
            ("Small", ("20", "15", "10"), "5", "2.50"),
            ("Medium", ("40", "30", "20"), "15", "4.75"),
            ("Large", ("60", "45", "35"), "30", "7.25"),
        ):
            make_box(name, dimensions, weight=weight, cost=cost)

        call_command("load_sample_boxes")

        self.assertEqual(Box.objects.count(), 11)
        self.assertEqual(
            Box.objects.get(name="Medium").internal_length,
            Decimal("40.64"),
        )


class SizeChartViewTests(TestCase):
    def setUp(self):
        call_command("load_sample_boxes")

    def test_size_chart_page_contains_every_seeded_box(self):
        response = Client().get(reverse("boxes:size_chart"))

        self.assertEqual(response.status_code, 200)
        for name in (
            "Small Flat",
            "Mailer Small",
            "Garment Flat",
            "Standard Small",
            "Standard Cube",
            "Multi-Item",
            "Medium",
            "Tall Medium",
            "Large",
            "Large Flat",
            "Extra-Large Flat (custom)",
        ):
            with self.subTest(name=name):
                self.assertContains(response, name)
        self.assertContains(response, "How to measure")
        self.assertContains(response, "scope=\"col\"")
        self.assertContains(response, "scope=\"row\"")
        self.assertContains(response, "711.2 × 609.6 × 101.6")
        self.assertContains(response, "71.12 × 60.96 × 10.16")
        self.assertContains(response, "0.7112 × 0.6096 × 0.1016")
        self.assertContains(response, "28 × 24 × 4")


class SizeChartRegressionTests(TestCase):
    def setUp(self):
        call_command("load_sample_boxes")

    def test_67_by_56_by_5_cm_fits_extra_large_flat_custom(self):
        result = recommend_box(
            Decimal("67"),
            Decimal("56"),
            Decimal("5"),
            Decimal("2"),
        )

        self.assertEqual(result.name, "Extra-Large Flat (custom)")

    def test_order_over_71_12_cm_returns_no_fit(self):
        result = recommend_box(
            Decimal("71.13"),
            Decimal("2"),
            Decimal("2"),
            Decimal("2"),
        )

        self.assertIsNone(result)

    def test_exact_inches_boundary_fits_and_001_above_does_not(self):
        exact_dimensions = {
            "length": "28",
            "width": "24",
            "height": "4",
            "weight": "2",
            "unit": "in",
        }
        exact_form = OrderDimensionsForm(exact_dimensions)
        self.assertTrue(exact_form.is_valid(), exact_form.errors)
        exact_box = recommend_box(
            *exact_form.cleaned_data["dimensions_cm"],
            exact_form.cleaned_data["weight"],
        )
        self.assertEqual(exact_box.name, "Extra-Large Flat (custom)")

        above_dimensions = exact_dimensions | {"length": "28.01"}
        above_form = OrderDimensionsForm(above_dimensions)
        self.assertTrue(above_form.is_valid(), above_form.errors)
        above_box = recommend_box(
            *above_form.cleaned_data["dimensions_cm"],
            above_form.cleaned_data["weight"],
        )
        self.assertIsNone(above_box)
