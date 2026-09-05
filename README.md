# WSI Patch Vision Transformer Agent

> **Domain:** Digital Pathology & Quantitative Histopathology  
> **Reference Guidelines & Standards:** `College of American Pathologists (CAP) Synoptic Protocols & DICOM WSI`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

WSI Patch Vision Transformer Agent is an enterprise-grade analytical platform for digital pathology workflows. It processes Whole Slide Imaging (WSI) task payloads through a multi-agent consensus system, evaluating metrics against clinical reference standards and generating cryptographically signed audit trails.

The system employs specialized worker agents that independently evaluate task parameters, then aggregates their findings into a consensus dossier with urgency classification and actionable remediation steps.

---

## ⚙️ Key Capabilities & Algorithmic Modules

- **Deterministic Calculation Engine**: Strict compliance with CAP Cancer Protocols and DICOM WSI PS3.16 reference formulations and thresholds.
- **Risk & Urgency Classification**: Multi-tier categorization (ROUTINE, ELEVATED_RISK, CRITICAL_STAT_PANIC) with automated clinical/operational action recommendations.
- **Validation & Guardrails**: Rigorous input bounds checking, NaN/Inf rejection, and anomaly detection.
- **Multi-Agent Consensus**: Three specialized workers (InvariantQC, SafetyEscalation, ProtocolConformance) provide independent evaluations.

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/abusuraihsakhri/wsi-patch-vision-transformer-agent.git
cd wsi-patch-vision-transformer-agent

# Install dependencies
pip install fastapi uvicorn pydantic pytest

# Optional: Set audit secret key for persistent audit trails
export AUDIT_SECRET_KEY="your-secure-key-here"
```

---

## 💻 CLI Quickstart & Usage

### 1. Single Task Evaluation
```bash
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 2. Interactive Chat Query
```bash
python cli.py chat "What is the system status?"
```

### 3. Batch CSV Processing
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Launch REST API Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Parameter Reference
| Parameter | Description | Default |
|:----------|:------------|:--------|
| `--task-id` | Unique task/case identifier | TASK-2026-001 |
| `--target` | Entity or specimen target identifier | KEY-TARGET-01 |
| `--primary` | Primary domain measurement (float) | 28.5 |
| `--secondary` | Secondary kinetic/confidence score (float) | 14.2 |
| `--critical` | Emergency escalation flag | False |
| `--status` | Status code or phenotype descriptor | DISCORDANT |

### Input Data Schema

| Field | Description | Requirement |
|:------|:------------|:------------|
| `task_id` | Unique task/case identifier | Required |
| `target_identifier` | Entity or specimen target identifier | Required |
| `primary_metric` | Primary domain measurement (finite float) | Required |
| `secondary_metric` | Secondary kinetic/confidence score | Optional (default: 0.0) |
| `is_critical_flag` | Emergency escalation trigger | Optional (default: false) |
| `status_descriptor` | Status code or phenotype descriptor | Optional (default: "NOMINAL") |

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active regex inspection blocking SSNs, MRNs, phone numbers, email addresses, and patient identifiers.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition.
* **Secure Key Management:** Audit signing key sourced from `AUDIT_SECRET_KEY` environment variable with secure random fallback.
* **Input Validation:** Pydantic v2 validators reject NaN, Inf, and empty string inputs.
* **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances (`llama3`, `mistral`), Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py 1000
```

### Test Coverage
- PHI guard enforcement
- Specialized worker evaluations
- Supervisor consensus and audit trail
- Input validation (NaN, Inf, empty strings)
- Batch file error handling
- Audit trail integrity verification

---

## 🐳 Container Deployment

```bash
docker build -t wsi-patch-vision-transformer-agent .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY=your-secure-key wsi-patch-vision-transformer-agent
```

Or using Docker Compose:

```bash
docker-compose up -d
```

---

## 📁 Project Structure

```
wsi-patch-vision-transformer-agent/
├── agents/                    # Core multi-agent system
│   ├── __init__.py           # Package version
│   ├── api.py                # FastAPI REST endpoints
│   ├── base.py               # Security, PHI guard, audit trail
│   ├── learning.py           # Bayesian calibration engine
│   ├── llm_factory.py        # LLM provider factory
│   ├── metrics.py            # Prometheus metrics collector
│   ├── models.py             # Pydantic v2 data schemas
│   ├── streamer.py           # WebSocket telemetry broadcaster
│   ├── supervisor.py         # Master orchestrator
│   └── workers.py            # Specialized worker agents
├── patho_vit_agent/          # PathoViT frontier module
│   ├── agents.py             # Sub-agent implementations
│   ├── cli.py                # Alternative CLI
│   ├── engine.py             # Core algorithmic engine
│   ├── models.py             # Data models
│   └── server.py             # FastAPI server factory
├── tests/                    # Pytest test suite
├── web/                      # Web interface
├── cli.py                    # Main CLI entry point
├── enrichment.py             # Enrichment feature engines
├── simulator.py              # High-throughput simulator
├── sample.csv                # Sample batch input
├── sample_payload.json       # Sample API payload
├── benchmark_dataset.json    # Golden benchmark test cases
├── pyproject.toml            # Project configuration
├── Dockerfile                # Container build
└── docker-compose.yml        # Container orchestration
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
