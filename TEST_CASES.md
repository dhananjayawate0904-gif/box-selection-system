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
| Sample data | Run the sample-data management command twice | Exactly three named sample records remain | PASS |

## Manual tests

No manual browser interaction or screen-reader audit was performed. The HTTP request/response behavior above is automated through Django's test client; it is not a claim of manual UI testing.

## Summary

**Automated:** 22 tests passed, 0 failed. The orientation and invalid-number subtests are exercised within their parent test methods.

**Manual:** Not performed.
