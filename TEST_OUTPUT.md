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
