# Tripletex

## Dataflow

`Main.py` is the orchestrator for the Tripletex service.

## CI pipeline

The GitHub Actions workflow in `.github/workflows/tripeltex-ci.yml` runs whenever files in `tripeltex/` change and performs:

- dependency installation on Python 3.12
- Python bytecode compilation with `python -m compileall .`
- a FastAPI smoke import check
- pytest-based unit tests for OCR helpers and the Tripletex HTTP client
- a Docker image build using `tripeltex/Dockerfile`
