# WSI Patch Vision Transformer Agent

A Python CLI, FastAPI service, and browser demonstration for **deterministic screening of synthetic WSI workflow metrics**. Despite the repository name, the current code **does not** read whole-slide images, tile image data, extract DINO embeddings, run a Vision Transformer, or implement a clinically validated pathology model.

The worker rules are configurable *demonstration thresholds* in source code, **not** thresholds specified by CAP or DICOM and **not appropriate for clinical decisions**.

## Browser interface

Open `web/index.html` through an HTTP server or the FastAPI service. The browser evaluation runs entirely in JavaScript without Python or a backend. It checks a primary metric above 25, a secondary metric above 12, critical flags, and selected status keywords. Results can be exported to JSON. The browser demonstration **does not create cryptographic audit signatures**.

The interface also offers a connected API mode when served by the Python application. In that mode, the request is sent to the same-origin FastAPI endpoint and the Python audit service performs the evaluation and signs an **in-memory** audit record.

No model weights, image data, WSI input, or medical diagnoses are supported.

## Install and run

Requires Python 3.9 or newer. For the documented server and test workflows:

```bash
git clone https://github.com/abusuraihsakhri/wsi-patch-vision-transformer-agent.git
cd wsi-patch-vision-transformer-agent
python -m pip install -e ".[api,test]"
python -m pytest -v
wsi-patch-vision-transformer-agent audit --task-id DEMO-001 --target SPEC-001 --primary 29.4 --secondary 14.8
wsi-patch-vision-transformer-agent batch -i sample.csv -o results.csv
wsi-patch-vision-transformer-agent verify-audit
wsi-patch-vision-transformer-agent serve --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/` for the web interface or `http://127.0.0.1:8000/docs` for FastAPI's interactive API documentation. For the standalone browser demonstration:

```bash
python -m http.server 8080 --directory web
```

Then open `http://127.0.0.1:8080/`. The installed command invokes the primary `cli.py`; the alternative CLI remains available as `python -m patho_vit_agent.cli`.

## API and input

- `POST /api/audit`: accepts `task_id`, `target_identifier`, `primary_metric` (required), plus optional `secondary_metric`, `status_descriptor`, `is_critical_flag`, and `attributes`.
- `GET /health`: service health.
- `GET /metrics`: JSON operational summary (not Prometheus exposition).
- `GET /api/audit/logs`: the in-memory audit chain and its HMAC integrity check.
- `POST /api/chat`: deterministic mock response; no external LLM provider is connected.

CSV batch processing expects the columns in `sample.csv`. Boolean values accept `true/false`, `yes/no`, or `1/0` (case-insensitive). Unsupported booleans are rejected per row. Spreadsheet-formula-like strings are escaped on CSV export.

The Python and browser rule sets have corresponding regression tests, but they are separate implementations.

## Security and privacy

Use **synthetic identifiers only**. The pattern-matching guard catches some common identifiers but **does not fully detect or de-identify protected health information**. No HIPAA compliance or clinical approval is claimed. The service has **no authentication or authorization**; keep it bound to loopback or behind appropriate controls. The audit trail is memory-only and disappears on restart. Set `AUDIT_SECRET_KEY` to a strong private value for consistent HMAC signing across processes; without it, a new random ephemeral key is generated. Never commit this key.

```bash
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
docker compose up --build
```

Docker Compose binds port 8000 to the host's loopback interface by default. The web-only GitHub Pages build is static and executes **no Python backend** or audit HMAC signing.

## Testing and technology

- Python 3.10–3.12 are tested in GitHub Actions, using pytest, FastAPI, Pydantic v2, and the standard-library CSV/HMAC modules.
- Browser evaluator uses native ES modules, standard JavaScript, and HTML/CSS; no Pyodide runtime is needed.
- Run `node --test tests/test_web.mjs` for browser business-logic tests (Node 22).
- Browser compatibility: current evergreen browsers supporting JavaScript modules and Blob downloads.
- The codebase includes a separate legacy `patho_vit_agent` orchestration flow and generalized enrichment demonstrations, retained for compatibility.

## License

MIT — see [LICENSE](LICENSE).
