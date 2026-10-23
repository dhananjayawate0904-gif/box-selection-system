# AI Usage Record

## Tool and prompt used

- **AI tool:** AI assistant using Copilot SDK in VS Code in this conversation.
- **Other tools used:** Workspace file inspection/editing and local PowerShell commands through the VS Code agent tools. No external AI API, paid service, or third-party code-generation service was used.
- **Prompt:** The user supplied the detailed “AI-Assisted Box Selection System” assignment in the attached text, including the application, tests, documentation, transcript, reflection, and GitHub requirements. There were no separate design prompts from the developer in this work session.

## Outputs accepted and reviewed

The assistant drafted the Django model, form, recommendation service, view, template, responsive CSS, sample-data command, and automated tests, then produced project documentation. The developer should review these files before submitting. The service enumerates dimension permutations and uses explicit fit, weight, and sort comparisons; it does not call an AI model at runtime.

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
- Django reported 22 tests passing.
- The initial migration was applied to SQLite.
- Running `load_sample_boxes` twice left exactly three sample rows.

See [TEST_OUTPUT.md](./TEST_OUTPUT.md) for the command output and statuses. These facts describe local verification only; they do not claim deployment, a GitHub push, an exported transcript, or a completed personal reflection.

## Developer review still needed

- Verify the code and written explanations against the assignment rubric and be prepared to explain the algorithm.
- Write the learning reflection independently in [LEARNING_REFLECTION_TEMPLATE.md](./LEARNING_REFLECTION_TEMPLATE.md).
- Export the actual conversation using the AI application's export feature and place that genuine file in `docs/`; follow [docs/README.md](./docs/README.md).
- Create and push a GitHub repository only when ready, then verify its contents in the browser.
