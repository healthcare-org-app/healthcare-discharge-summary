# discharge-summary-service

discharge-summary-service — domain: ehr

- **Port:** 8311
- **Language:** Python 3.11 + Flask
- **Database:** `ehr` (Postgres, table `discharge_summary`)
- **Event bus:** Kafka

## API

| Method    | Path                       |
|-----------|----------------------------|
| GET       | `/api/discharge_summary/`          |
| POST      | `/api/discharge_summary/`          |
| GET       | `/api/discharge_summary/<id>`      |
| PUT/PATCH | `/api/discharge_summary/<id>`      |
| DELETE    | `/api/discharge_summary/<id>`      |
| GET       | `/health`                  |
| GET       | `/ready`                   |

## Events

**Publishes:** (none)
**Subscribes:** encounter.ended

## HTTP peer dependencies

- `ehr-service`
- `clinical-notes-service`
- `audit-log-service`

## Local dev

```bash
pip install -e ../../libs/py-healthcare-common
pip install -r requirements.txt
cp .env.example .env
(cd ../../infra && docker compose up -d postgres kafka kafka-init)
python -m app.main
```

## Tests

```bash
pytest
```
