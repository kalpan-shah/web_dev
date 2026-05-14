# Todo APP - Template 
Last Updated: May 14, 2026

### Setup
1. Install uv
2. Install requirements
    ```bash
    cd src
    uv sync
    ```
3. Rename the .env.template to .env and update variables accordingly

### Run
`uv run uvicorn app.main:app --reload --reload-dir ./app`

### Run Tests
`pytest`
