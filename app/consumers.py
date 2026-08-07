"""Kafka consumers for discharge-summary-service.

One handler per subscribed topic. Real handlers write to this service's own
database and/or publish follow-up events; stub handlers just log + audit.
"""
from __future__ import annotations

import logging

from psycopg.types.json import Json

from healthcare_common.audit import emit_audit

log = logging.getLogger("discharge-summary-service.consumers")

TABLE = "discharge_summary"


def register(svc) -> None:
    bus = svc.bus
    db = svc.db
    clients = svc.clients

    @bus.on("encounter.ended")
    def _on_encounter_ended(envelope: dict) -> None:
        data = envelope.get("data") or {}
        try:
                    db.execute(f"INSERT INTO {TABLE} (data) VALUES (%s)",
                               (Json({"encounter_id": data.get("id"),
                                      "patient_id":   data.get("patient_id"),
                                      "state": "draft"}),))
        except Exception as e:
            log.exception("discharge-summary-service/encounter.ended handler failed: %s", e)
        emit_audit(bus, action="consume.encounter.ended", actor="system:discharge-summary-service",
                   target=None, details={"envelope_id": envelope.get("id")})

