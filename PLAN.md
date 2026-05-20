# ExamInsights Execution Plan

## Summary

Upgrade ExamInsights from a static PDF prototype into a live local-file RAG assistant with better Streamlit UX, role-based prompt presets, metadata-aware insights, and a deployable Render/Docker path.

Chosen defaults:

- Dynamic ingestion: local `data/` folder watcher first.
- Deployment: Render using the existing Docker architecture.
- Role customization: student/educator prompt presets, no auth in this milestone.

## Key Changes

- Backend ingestion:

  - Keep `app.py` as the Pathway RAG backend.
  - Configure local file ingestion to refresh automatically from `data/`.
  - Preserve the existing commented Google Drive config as a later connector option.
  - Add document metadata handling for filename, modified/synced time, and source path where Pathway metadata supports it.
- RAG behavior:

  - Add reusable prompt templates for student and educator modes.
  - Student mode should emphasize study guidance, likely topics, weak-area revision, and answer explanations.
  - Educator mode should emphasize topic frequency, curriculum coverage, repeated question patterns, and gap analysis.
  - Keep the API contract as `POST /v1/pw_ai_answer` with a prompt payload, unless Pathway requires a richer body for metadata filtering.
- Streamlit UX:

  - Replace the single plain question form with:
    - role selector: Student / Educator
    - prompt preset selector
    - custom question text area
    - “Sync now” control that checks backend availability and refreshes UI state
    - “Last synced” / backend status display
  - Improve response rendering so the answer body is shown cleanly instead of dumping the raw JSON object.
  - Add clear error states for backend unavailable, empty prompt, and API timeout.
- Configuration and deployment:

  - Move hardcoded API URL into environment/config with a default suitable for Docker local use.
  - Keep Docker running both backend and Streamlit, but document Render deployment using the existing container model.
  - Update README to describe local live-folder behavior, role modes, environment variables, and Render deployment steps.

## Test Plan

- Static checks:

  - Verify imports and syntax for `app.py` and `streamlit_app.py`.
  - Confirm `config.yaml` still loads and local source config is valid.
- Backend scenarios:

  - Start Pathway server and confirm `/v1/pw_ai_answer` responds for existing PDFs.
  - Add a new PDF to `data/`, wait for refresh interval, and confirm answers can reference the new file.
  - Replace or remove a PDF and confirm responses reflect updated available content.
- Streamlit scenarios:

  - Submit a student preset and confirm the outgoing prompt includes student guidance context.
  - Submit an educator preset and confirm the outgoing prompt includes analysis/curriculum context.
  - Confirm backend-down, empty-prompt, and timeout states show useful messages.
  - Confirm “Last synced” and status indicators update without breaking the form.
- Deployment scenarios:

  - Build Docker image successfully.
  - Run container locally with ports `8000` and `8501`.
  - Validate Render service starts both processes and exposes Streamlit publicly.

## Assumptions

- The first milestone does not add Google Drive credentials, auth, persistent user accounts, or a database.
- “Real-time” means Pathway detects changes in the local `data/` folder on a short refresh interval, not instant filesystem events.
- Existing Gemini/LiteLLM setup remains the LLM provider path.
