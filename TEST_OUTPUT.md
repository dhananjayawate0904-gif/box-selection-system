# Test and Command Output

This file records observed local command results. Commands were run with the checked-in project in the existing `.venv` virtual environment. No output below is fabricated.

## Environment

```text
> .venv\Scripts\python.exe --version
Python 3.14.0

> .venv\Scripts\python.exe -m django --version
6.1.2

> .venv\Scripts\python.exe -m pip --version
pip 25.2 from C:\Users\chand\OneDrive\Desktop\box\box-selection-system\.venv\Lib\site-packages\pip (python 3.14)
```

## Django system check

Command: `.venv\Scripts\python.exe manage.py check`

```text
System check identified no issues (0 silenced).
Exit status: 0
```

## Migration consistency check

Command: `.venv\Scripts\python.exe manage.py makemigrations --check --dry-run`

```text
No changes detected
Exit status: 0
```

## Automated tests

Command: `.venv\Scripts\python.exe manage.py test`

```text
Creating test database for alias 'default'...
.....................
----------------------------------------------------------------------
Ran 22 tests in 0.254s

OK
Destroying test database for alias 'default'...
Found 22 test(s).
System check identified no issues (0 silenced).
Created sample box: Small
Created sample box: Medium
Created sample box: Large
Updated sample box: Small
Updated sample box: Medium
Updated sample box: Large
Exit status: 0
```

The sample command messages during this run come from its isolated command test, which invokes the command twice.

## Applying migrations

Command: `.venv\Scripts\python.exe manage.py migrate`

```text
Operations to perform:
  Apply all migrations: boxes, contenttypes
Running migrations:
  Applying boxes.0001_initial... OK
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
Exit status: 0
```

## Sample-data command repeatability

The first and second invocations of `.venv\Scripts\python.exe manage.py load_sample_boxes` produced:

```text
Created sample box: Small
Created sample box: Medium
Created sample box: Large
Exit status: 0

Updated sample box: Small
Updated sample box: Medium
Updated sample box: Large
Exit status: 0
```

Database verification command:

```text
> .venv\Scripts\python.exe manage.py shell -c "from boxes.models import Box; print('Box count:', Box.objects.count()); print('Names:', ', '.join(Box.objects.order_by('name').values_list('name', flat=True)))"
8 objects imported automatically (use -v 2 for details).

Box count: 3
Names: Large, Medium, Small
Exit status: 0
```

## Scope

These checks verify the local development implementation only. No deployment, production configuration, manual browser test, GitHub repository creation, or push was performed.

## 2026-10-24 — Multi-unit input and size chart

The baseline results above are retained unchanged. During implementation, the first focused feature run exposed test fixture requests that omitted the newly required unit and one stale assertion for the retired demo names. Those test issues were corrected; the failure and successful reruns are included here.

### Intermediate focused run (before corrections)

Command: `.venv\Scripts\python.exe manage.py test boxes.tests.UnitConversionTests boxes.tests.OrderDimensionsFormTests boxes.tests.BoxSelectionViewTests boxes.tests.SampleBoxCommandTests boxes.tests.SizeChartViewTests boxes.tests.SizeChartRegressionTests -v 2`

Observed output:

```text
Found 25 test(s).
Ran 25 tests in 0.568s
FAILED (failures=8)
Exit status: 1
```

### Django check and migration state

Command: `.venv\Scripts\python.exe manage.py check`

```text
System check identified no issues (0 silenced).
Exit status: 0
```

Command: `.venv\Scripts\python.exe manage.py makemigrations --check --dry-run`

```text
No changes detected
Exit status: 0
```

Command: `.venv\Scripts\python.exe manage.py migrate`

```text
Operations to perform:
  Apply all migrations: boxes, contenttypes
Running migrations:
  No migrations to apply.
Exit status: 0
```

### Size-chart seed repeatability

Command: `.venv\Scripts\python.exe manage.py load_sample_boxes` (run twice)

```text
First run: created Small Flat, Mailer Small, Garment Flat, Standard Small,
Standard Cube, Multi-Item, Medium, Tall Medium, Large, Large Flat, and
Extra-Large Flat (custom).
First seed exit status: 0

Second run: updated Small Flat, Mailer Small, Garment Flat, Standard Small,
Standard Cube, Multi-Item, Medium, Tall Medium, Large, Large Flat, and
Extra-Large Flat (custom).
Second seed exit status: 0
```

Database verification command:

```text
Box count: 11
Names: Extra-Large Flat (custom), Garment Flat, Large, Large Flat, Mailer Small,
Medium, Multi-Item, Small Flat, Standard Cube, Standard Small, Tall Medium
Exit status: 0
```

### Focused feature rerun

Command: `.venv\Scripts\python.exe manage.py test boxes.tests.UnitConversionTests boxes.tests.OrderDimensionsFormTests boxes.tests.BoxSelectionViewTests boxes.tests.SampleBoxCommandTests boxes.tests.SizeChartViewTests boxes.tests.SizeChartRegressionTests -v 2`

```text
Found 26 test(s).
Ran 26 tests in 0.573s
OK
Exit status: 0
```

### Full Django test suite

Command: `.venv\Scripts\python.exe manage.py test -v 2`

Observed output:

```text
Found 38 test(s).
Ran 38 tests in 0.452s
OK
Destroying test database for alias 'default'...
System check identified no issues (0 silenced).
Exit status: 0
```

The full run includes the unit conversions, equivalent cross-unit recommendations, all-unit result display, size-chart response, 11-row idempotent seed, the 67 × 56 × 5 cm regression (observed recommendation: Extra-Large Flat (custom)), over-limit no-fit case, and the exact/0.01-inch-over boundary. Django used and destroyed its isolated temporary test database.

### Final rerun after canonical minimum validation adjustment

The form now applies the existing 0.01 cm minimum after conversion, so the same physical minimum works consistently across units.

Commands and observed output:

```text
> .venv\Scripts\python.exe manage.py check
System check identified no issues (0 silenced).
Exit status: 0

> .venv\Scripts\python.exe manage.py makemigrations --check --dry-run
No changes detected
Exit status: 0

> .venv\Scripts\python.exe manage.py migrate
Operations to perform:
  Apply all migrations: boxes, contenttypes
Running migrations:
  No migrations to apply.
Exit status: 0
```

Both final seed invocations exited 0 and printed the same 11 lines of `Updated sample box: <name>` for Small Flat, Mailer Small, Garment Flat, Standard Small, Standard Cube, Multi-Item, Medium, Tall Medium, Large, Large Flat, and Extra-Large Flat (custom).

```text
Box count: 11
Names: Extra-Large Flat (custom), Garment Flat, Large, Large Flat, Mailer Small,
Medium, Multi-Item, Small Flat, Standard Cube, Standard Small, Tall Medium
Exit status: 0
```

Final full test command: `.venv\Scripts\python.exe manage.py test -v 2`

```text
Found 39 test(s).
Ran 39 tests in 0.686s
OK
Destroying test database for alias 'default'...
System check identified no issues (0 silenced).
Exit status: 0
```

### Final run after legacy-sample cleanup coverage

The updated final implementation also has an isolated test covering replacement of the exact unchanged legacy demo rows. Final validation output:

```text
System check identified no issues (0 silenced).
Exit status: 0
No changes detected
Exit status: 0
Operations to perform:
  Apply all migrations: boxes, contenttypes
Running migrations:
  No migrations to apply.
Exit status: 0
Box count: 11
Found 40 test(s).
Ran 40 tests in 0.575s
OK
Destroying test database for alias 'default'...
System check identified no issues (0 silenced).
Exit status: 0
```

The two seed invocations both exited 0 and updated the same 11 chart rows. Django created and destroyed the isolated test database for the final 40-test run.

### Latest rerun after chart-value assertions

Command: `.venv\Scripts\python.exe manage.py test -v 2`

```text
Found 40 test(s).
Ran 40 tests in 0.605s
OK
Exit status: 0
```

### Final repository verification

After the final code and documentation review, these results were observed:

```text
git diff --check
No output
Exit status: 0

manage.py test -v 2
Found 40 test(s).
Ran 40 tests in 0.575s
OK
Exit status: 0
```
