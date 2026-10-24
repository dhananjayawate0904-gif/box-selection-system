# AI Usage Record

## Tool and prompt used

- **AI tool:** AI assistant using Copilot SDK in VS Code in this conversation.
- **Other tools used:** Workspace file inspection/editing and local PowerShell commands through the VS Code agent tools. No external AI API, paid service, or third-party code-generation service was used.
- **Prompt:** The user supplied the detailed “AI-Assisted Box Selection System” assignment in the attached text, including the application, tests, documentation, transcript, reflection, and GitHub requirements. There were no separate design prompts from the developer in this work session.

## Outputs accepted and reviewed

This change extends the existing Django form, views, templates, responsive CSS, sample-data command, and automated tests; it adds a pure Decimal conversion module and a size-chart page. The developer should review the implementation before submitting. The service continues to enumerate dimension permutations and use explicit fit, weight, and sort comparisons; it does not call an AI model at runtime.

## Multi-unit size chart change

- **Dimension data provenance:** The standard catalogue examples and their inch measurements were supplied for this task as dimensions found through web searches of standard shipping-box size lists on Staples and ParcelPath pages. The mm, cm, and m figures use the stated exact conversions from those inch values. Extra-Large Flat (custom) is a custom size, not a standard catalogue size.
- **Weight capacities and costs:** All 11 capacities and INR costs are invented sample placeholders, not values sourced from Staples, ParcelPath, or a supplier. Replace them with your supplier’s verified data before relying on recommendations.
- **Prompts used:** [Fill in the prompts you used for this change.]
- **Mistakes found:** [Fill in mistakes you found while reviewing or testing.]
- **External-source verification:** The source names and measurement values above are the task-provided provenance. Individual page URLs and matching exact product listings were not independently captured in the project record.

The assistant used the available Python virtual environment and observed results from Django checks, migration checks, the automated test suite, migration application, and two sample-data command runs. Those observed outputs and exit statuses are recorded in [TEST_OUTPUT.md](./TEST_OUTPUT.md).

## Rejected or modified work

- The scaffold's existing development `SECRET_KEY` was replaced with a clearly labelled local-only fallback and an environment-variable override; no production secret was added.
- Default Django admin, authentication, session, and messages integration was removed so the assignment does not introduce an authentication feature.
- The initial patch for the scaffold settings did not match the existing secret-key line, so that patch failed. The file was inspected and the settings were then deliberately replaced with a minimal project configuration. The final application checks and tests passed afterward.
- No fictional transcript or generated personal-learning reflection was created. The required transcript must be an actual export from this conversation, and the learning reflection must be written by the developer.

## Actual findings and verification

The inspected workspace contained a starter Django project but no box model, app registration, selection logic, user-facing view, or tests. These missing assignment components were added. The scaffold had a hardcoded development-only Django key; the final settings no longer contain that original value.

Observed facts at completion:

- The existing virtual environment uses Python 3.14.0 and Django 6.1.2.
- `manage.py check` and `makemigrations --check --dry-run` passed.
- Django reported 40 tests passing after this change; intermediate focused test failures and their corrected reruns are retained in [TEST_OUTPUT.md](./TEST_OUTPUT.md).
- `makemigrations --check --dry-run` found no schema changes, and `migrate` reported no migrations to apply.
- The local SQLite sample inventory contains 11 boxes after the updated seed command ran twice.
- The updated `load_sample_boxes` command seeds 11 size-chart rows and is tested for repeatability.

See [TEST_OUTPUT.md](./TEST_OUTPUT.md) for the command output and statuses. These facts describe local verification only; they do not claim deployment, a GitHub push, an exported transcript, or a completed personal reflection.

## Developer review still needed

- Verify the code and written explanations against the assignment rubric and be prepared to explain the algorithm.
- Write the learning reflection independently in [LEARNING_REFLECTION_TEMPLATE.md](./LEARNING_REFLECTION_TEMPLATE.md).
- Export the actual conversation using the AI application's export feature and place that genuine file in `docs/`; follow [docs/README.md](./docs/README.md).
- Create and push a GitHub repository only when ready, then verify its contents in the browser.
