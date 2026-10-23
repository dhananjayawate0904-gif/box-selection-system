# AI-Assisted Box Selection System

A small Django application that recommends the lowest-cost warehouse box able to contain an order and support its weight. The recommendation itself is deterministic business logic; AI assisted with development, not with runtime predictions.

## Features

- Enter order length, width, height (cm), and weight (kg).
- Check all six rotations of the order dimensions against each box.
- Reject boxes that cannot fit the order or support its weight.
- Choose the lowest-cost eligible box, with ties resolved by internal volume and then case-insensitive box name.
- Show a clear no-fit message when inventory has no suitable box.
- Validate every value on the server and protect POST requests with Django CSRF middleware.
- Load or refresh three sample boxes with a repeatable management command.

The displayed box cost is a decimal amount without a currency symbol because the assignment does not specify a currency.

## Algorithm

For each box whose maximum weight is at least the order weight, the service generates all permutations of the order's three dimensions. A box is eligible when one orientation fits all three internal dimensions. It then chooses the minimum `(cost, internal volume, case-insensitive name, exact name)` tuple so ties remain deterministic even when names differ only by letter case. Exact dimensional and weight-capacity boundaries are accepted. If there are no eligible boxes, the service returns `None`; it never substitutes a larger or overweight box.

This is not an AI/ML prediction system. The runtime selection uses transparent comparisons and deterministic sorting only.

## Architecture

- `config/` contains Django settings and the root URL configuration.
- `boxes/models.py` defines the validated `Box` inventory model and database constraints.
- `boxes/forms.py` validates submitted order measurements.
- `boxes/services.py` contains independently testable recommendation logic.
- `boxes/views.py`, `boxes/urls.py`, and `boxes/templates/` provide the request flow and interface.
- `boxes/static/boxes/styles.css` provides the responsive styling.
- `boxes/management/commands/load_sample_boxes.py` supplies repeatable demo data.
- `boxes/tests.py` covers the service, form, web flow, CSRF protection, and sample-data command.
- `boxes/migrations/0001_initial.py` creates the inventory table.
- `docs/README.md` explains how to add a genuine exported chat transcript.

## File tree

```text
.
├── .gitignore
├── AI_USAGE.md
├── LEARNING_REFLECTION_TEMPLATE.md
├── README.md
├── TEST_CASES.md
├── TEST_OUTPUT.md
├── requirements.txt
├── config/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── boxes/
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── management/commands/load_sample_boxes.py
    ├── migrations/0001_initial.py
    ├── models.py
    ├── services.py
    ├── static/boxes/styles.css
    ├── templates/boxes/home.html
    ├── tests.py
    ├── urls.py
    └── views.py
```

## Prerequisites

- Python 3.10 or newer
- pip (included with Python)
- Git (optional for running the application; required for the GitHub workflow)
- SQLite (bundled with supported Python distributions)

Django is the only third-party runtime dependency. No external AI service, paid API, Docker, or JavaScript package is required.

## Setup and run on Windows

Open PowerShell or Command Prompt in the project directory.

### PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py load_sample_boxes
python manage.py runserver
```

If PowerShell blocks activation, run the commands without activating the environment by replacing `python` with `.\.venv\Scripts\python.exe`.

### Command Prompt

```bat
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py load_sample_boxes
python manage.py runserver
```

Open the local address printed by Django (normally `http://127.0.0.1:8000/`). Run the sample-data command whenever you want to restore the sample inventory; it updates the three named samples instead of inserting duplicates.

## Database and sample inventory

The project uses the SQLite database `db.sqlite3` in the project directory. Apply the checked-in migration with:

```powershell
python manage.py migrate
```

Load or refresh the three sample boxes with:

```powershell
python manage.py load_sample_boxes
```

The sample boxes are named Small, Medium, and Large. The command is idempotent for those names and updates their dimensions, capacities, and costs if they already exist.

## Tests and checks

Run these from the activated virtual environment:

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Django creates an isolated temporary test database; tests do not require sample records in the local development database. Actual command output, versions, and exit statuses from this implementation are recorded in [TEST_OUTPUT.md](./TEST_OUTPUT.md), with the individual cases in [TEST_CASES.md](./TEST_CASES.md).

## AI and assignment materials

AI assistance was used to develop and verify the application. The runtime algorithm is ordinary deterministic Django/Python business logic, not an AI model. [AI_USAGE.md](./AI_USAGE.md) records the observed tools and work. The developer must complete [LEARNING_REFLECTION_TEMPLATE.md](./LEARNING_REFLECTION_TEMPLATE.md) independently; AI has not supplied reflection answers.

No genuine transcript export was provided with the workspace. See [docs/README.md](./docs/README.md) for how to place the actual chat export in `docs/`. No transcript is claimed to be present.

## Limitations and troubleshooting

- Dimensions are in centimetres and weight is in kilograms. The form accepts positive decimal values to two fractional digits.
- The cost field is a decimal with no assumed currency.
- There is no authentication, payment, external AI API, product/order database, or deployment configuration.
- `DEBUG` is enabled for this local assignment. The fallback Django secret key is for local development only; do not deploy with the development settings or key. Set a private `DJANGO_SECRET_KEY` and configure production settings before deployment.
- If imports fail, activate `.venv` and run `python -m pip install -r requirements.txt`.
- If the database schema is missing, run `python manage.py migrate`.
- If recommendations show no boxes, run `python manage.py load_sample_boxes` or add inventory through a deliberate code/data change.
- If PowerShell prevents virtual-environment activation, use the interpreter directly as shown above or use Command Prompt activation.

## GitHub submission

The project is prepared for local Git version control. No GitHub repository or remote is created by this application. After creating an empty repository on GitHub, add its URL and push the branch:

```powershell
git remote add origin https://github.com/<YOUR-USERNAME>/<YOUR-REPOSITORY>.git
git push -u origin main
```

Replace the placeholders with your own repository details. Do not commit credentials or `.env` files. To verify the submission, open the repository page in a browser and check that the source, migration, tests, and required documentation appear in the file list; confirm that `.venv/` and `db.sqlite3` do not.

## Deploying on Render

The Django project module is `config`; the production WSGI application is `config.wsgi:application`. Render's free web service uses an ephemeral filesystem, so this project's local SQLite database and its data are not durable across service restarts, rebuilds, or redeploys. The SQLite setup remains available for local development. Use a persistent external database if production data must survive.

1. Commit and push the deployment changes to the existing `origin` remote, then create a **Web Service** in Render connected to that repository:

   ```powershell
   git add requirements.txt config/settings.py README.md
   git commit -m "Prepare Django app for Render"
   git push origin main
   ```
2. Select the Python runtime. Set the build command to:

   ```text
   pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate && python manage.py load_sample_boxes
   ```

   The sample command is repeatable and initializes the demo inventory. For an external persistent database, configure the database and its driver before migrating.
3. Set the start command to:

   ```text
   gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
   ```

4. In the service's environment settings, set `DEBUG` to `false` and `DJANGO_SECRET_KEY` to a newly generated private random value. You can generate one locally with `python -c "import secrets; print(secrets.token_urlsafe(50))"` and paste the result into Render; do not commit it. Render provides `RENDER_EXTERNAL_HOSTNAME`; the settings use it for Django's allowed host and HTTPS CSRF origin, and default `DEBUG` to false when that hostname is present. If you use a custom domain, add its hostname to `DJANGO_ALLOWED_HOSTS` and its full `https://` origin to `CSRF_TRUSTED_ORIGINS`, as comma-separated values when listing more than one.
5. Deploy and review the Render build and service logs. The application should redirect HTTP requests to HTTPS, and collected CSS is served by WhiteNoise.

These are deployment instructions only; they do not mean that a Render service has been created or deployed. The default SQLite database is appropriate for a demonstration without durable writes, not for storing production inventory or orders.
