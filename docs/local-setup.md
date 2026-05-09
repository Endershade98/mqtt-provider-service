# Local Setup

This document explains how to set up and run the MQTT Provider Service locally for development and testing purposes.

---

# Requirements

Ensure you have the following installed:

- Python 3.11+
- pip / virtualenv
- Docker (recommended for infrastructure services)
- Git

---

# Project Setup

## 1. Clone Repository

```bash id="c1v8qp"
git clone <repo-url>
cd mqtt-provider-service
````

---

## 2. Create Virtual Environment

```bash id="v4n2ld"
python -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash id="x9k3pw"
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the root directory:

```bash id="env123"
MQTT_BROKER_HOST=localhost
MQTT_BROKER_PORT=1883

DJANGO_SECRET_KEY=change-me
DEBUG=True
```

---

# Running the System

## 1. Start Infrastructure (Recommended via Docker)

Example stack:

* MQTT Broker (Mosquitto / EMQX)
* Redis
* PostgreSQL

```bash id="d8p0mc"
docker-compose up -d
```

---

## 2. Run Django (if applicable)

```bash id="dj2k9a"
python manage.py runserver
```

---

## 3. Run MQTT Worker

```bash id="mq7x1s"
python scripts/run_mqtt_worker.py
```

This process:

* connects to MQTT broker
* subscribes to device topics
* processes telemetry and ACK messages

---

# Running Tests

## Full test suite

```bash id="t9p3qa"
pytest
```

---

## Coverage report

```bash id="cv8lq2"
pytest --cov=src --cov-report=term-missing
```

Expected:

* ~90% coverage
* full critical path coverage (MQTT + ACK + telemetry flows)

---

# Project Structure Overview

```text id="strct1"
src/
├── domain/
├── application/
├── interfaces/
├── infrastructure/
scripts/
└── run_mqtt_worker.py
```

---

# Key Services

## MQTT Worker

Entry point for MQTT processing:

```bash id="wrk1mq"
python scripts/run_mqtt_worker.py
```

Responsibilities:

* consume MQTT messages
* delegate to application layer
* ensure safe parsing and routing

---

## Django (optional API layer)

Used for:

* device management
* command creation
* administrative operations

---

# Debugging Tips

## MQTT Messages Not Received

Check:

* broker running
* correct topic subscription
* environment variables

---

## Database Issues

Reset local DB:

```bash id="dbreset"
python manage.py flush
```

---

## Logs

All logs are printed to stdout.

Use:

```bash id="logs1"
tail -f logs/app.log
```

(if configured)

---

# Common Issues

## Naive datetime warnings

If Django timezone warnings appear:

Ensure:

```python
USE_TZ = True
```

and use timezone-aware datetimes.

---

## Import Errors

Ensure project root is in PYTHONPATH:

```bash id="pyth1"
export PYTHONPATH=.
```

---

# Recommended Dev Flow

1. Start infrastructure (Docker)
2. Run MQTT worker
3. Run tests continuously
4. Modify domain/application logic first
5. Add integration tests for new flows

---

# Performance Notes

* MQTT worker is stateless → can be scaled horizontally
* DB is single source of truth
* Redis used for event propagation (optional scaling layer)

---

# Summary

This setup is designed to:

* allow fast local development
* simulate production-like architecture
* keep infrastructure reproducible
