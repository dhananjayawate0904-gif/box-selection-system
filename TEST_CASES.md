# Test Cases

All results below are from `python manage.py test` in the project's virtual environment. Django created and destroyed an isolated temporary test database. No case depends on the development database's sample data.

## Automated cases

| Area | Case and setup | Expected result | Actual result |
|---|---|---|---|
| Recommendation | Two eligible boxes with different prices | Lowest-cost box is returned | PASS |
| Recommendation | A lower-cost eligible box and a more expensive eligible box | Lower-cost box is returned | PASS |
| Recommendation | Order fits only after rotating dimensions | Rotated-fit box is returned | PASS |
| Recommendation | A `(1, 2, 3)` order and each of its six permutations, tested separately | Each orientation fits its matching box | PASS (six subtests) |
| Recommendation | Order weight equals the box capacity | Box is accepted | PASS |
| Recommendation | Order weight exceeds capacity | No box is returned | PASS |
| Recommendation | Each order dimension exactly equals its corresponding box dimension | Exact fit is accepted | PASS |
| Recommendation | One order side is too large in every orientation | No box is returned | PASS |
| Recommendation | Empty box inventory | No box is returned | PASS |
| Recommendation | Equal-cost eligible boxes with different volumes | Smaller-volume box is returned | PASS |
| Recommendation | Equal cost and volume but different names | Case-insensitively earlier name is returned | PASS |
| Recommendation | Equal cost, volume, and case-folded name (`Alpha`, `alpha`) | Exact-name fallback makes selection deterministic | PASS |
| Form | Required length is missing | Form is invalid with a length error | PASS |
| Form | Width is not numeric | Form is invalid with a width error | PASS |
| Form | Each dimension and weight receives zero and a negative value | Each invalid field is rejected | PASS (eight subtests) |
| Page | GET the main page | HTTP 200 and form heading are present | PASS |
| Page | POST valid order dimensions matching the isolated fixture | HTTP 200 and recommended box and cost are shown | PASS |
| Page | POST dimensions too large for the fixture | HTTP 200 and clear no-fit message are shown | PASS |
| Page | POST negative weight | HTTP 200 with validation error and no recommendation | PASS |
| CSRF | POST without a token using an enforcing client | HTTP 403 | PASS |
| CSRF | POST with a token obtained from the page | HTTP 200 and recommendation are shown | PASS |
| Sample data | Run the sample-data management command twice in an empty test database | Exactly 11 named chart records remain, with distinct costs | PASS |
| Sample data | Seed the exact unchanged legacy demo rows, then run the updated command | The legacy placeholders are replaced by exactly 11 chart records | PASS |
| Units | Convert 10 mm, 30.48 cm, 0.3048 m, and 12 in to centimetres | Each yields the exact Decimal value 30.48 | PASS |
| Units | Convert 2.54 cm to mm and 30.48 cm to inches | Exact Decimal values 25.4 mm and 12 in | PASS |
| Units | Format 30.48 cm and round-trip each supported unit | Returns Decimal mm, cm, m, and in values; each input round-trips | PASS |
| Units | Pass an unsupported unit and a float value | Clear `ValueError` for unit; float is rejected so conversion remains Decimal-only | PASS |
| Form | Submit equivalent dimensions as 304.8 mm, 30.48 cm, 0.3048 m, and 12 in | All convert to 30.48 cm and return the same recommendation | PASS |
| Form | Submit 0.0001 m and 0.001 cm dimensions | The canonical 0.01 cm minimum is accepted for the first and rejects the second | PASS |
| Form | Omit the unit or submit `yards` | Unit field is invalid | PASS |
| Page | POST 10 × 8 × 6 inches against an isolated Standard Small box | The Standard Small recommendation is returned | PASS |
| Page | POST a fitting order | The result displays dimensions in mm, cm, m, and in, plus capacity and cost | PASS |
| Size chart | GET `/size-chart/` after seeding the isolated test inventory | HTTP 200; all 11 names and unit columns are present | PASS |
| Regression | Recommend for 67 × 56 × 5 cm at 2 kg against the seeded chart | The observed recommendation is Extra-Large Flat (custom) | PASS |
| Regression | Submit 71.13 cm × 2 cm × 2 cm at 2 kg against the seeded chart | No box fits in any orientation | PASS |
| Boundary | Submit exactly 28 × 24 × 4 inches, then 28.01 × 24 × 4 inches | Exact custom-box boundary fits; 0.01 inch above returns no fit | PASS |

## Manual tests

No manual browser interaction or screen-reader audit was performed. The HTTP request/response behavior above is automated through Django's test client; it is not a claim of manual UI testing.

## Summary

**Automated:** 40 tests passed, 0 failed in the final post-change `-v 2` run. Earlier focused-run failures and corrected reruns are retained in [TEST_OUTPUT.md](./TEST_OUTPUT.md). Orientation and invalid-number subtests are exercised within their parent test methods.

**Manual:** Not performed.
