# Engineering Decisions

This document records key architectural and design decisions made during the evolution of the MQTT Provider Service.

It is intended to improve maintainability, explain tradeoffs, and support technical interviews or code reviews.

---

# 1. Clean Architecture Adoption

## Decision
Adopt Clean Architecture as the foundational structure.

## Rationale
IoT systems tend to become tightly coupled to infrastructure (MQTT brokers, databases, frameworks).

Clean Architecture ensures:

- domain independence from frameworks
- clear dependency direction
- long-term maintainability
- testability of business rules

## Tradeoff
Increased initial complexity due to multiple layers.

---

# 2. Domain Driven Design (DDD)

## Decision
Model the system using DDD principles.

## Rationale
The system has complex business behavior:

- command lifecycle
- device state transitions
- telemetry ingestion semantics

DDD allows:

- explicit business rules
- rich domain models
- reduced anemic services

## Tradeoff
Requires discipline to avoid leaking infrastructure concerns into domain.

---

# 3. MQTT as External Boundary (ACL Pattern)

## Decision
Treat MQTT as an external system and isolate it via an Anti-Corruption Layer (Translator).

## Rationale
MQTT topics and payloads are not domain concepts.

Without isolation:

- domain would depend on protocol structure
- changes in topic format would break business logic

## Implementation
- MQTTMessageTranslator converts:
  - topic → device_id + channel
  - payload → application DTO

## Tradeoff
Extra mapping layer, but strong decoupling benefits.

---

# 4. Router Layer in Application

## Decision
Introduce MQTTApplicationRouter between interface and use cases.

## Rationale
Avoid fat handlers and ensure single orchestration point.

Responsibilities:

- route telemetry vs ack
- delegate to correct use case
- keep interface layer dumb

## Tradeoff
Slight additional abstraction, but improves clarity and testability.

---

# 5. Transactional Outbox Pattern

## Decision
Use Outbox pattern for domain event reliability.

## Rationale
Without it:

- DB writes and event publishing can diverge
- system becomes inconsistent under failure

Outbox ensures:

- atomic commit of state + events
- safe asynchronous dispatch
- replay capability

## Tradeoff
Requires background worker (Celery) for dispatching.

---

# 6. Use Case Per Action Model

## Decision
One use case per business action.

## Rationale
Keeps application layer:

- explicit
- testable
- easy to reason about

Examples:

- HandleTelemetryUseCase
- AcknowledgeCommandUseCase
- SendCommandUseCase

## Tradeoff
More classes, but clearer separation.

---

# 7. Domain Events as First-Class Citizens

## Decision
Model state changes using domain events.

## Rationale
Allows:

- auditability
- event-driven integration
- decoupled downstream systems

Examples:

- CommandAcknowledged
- CommandSent
- DeviceHeartbeatUpdated

---

# 8. Fake Repositories for Integration Tests

## Decision
Use in-memory fake implementations in integration tests.

## Rationale

- faster tests
- deterministic behavior
- no DB dependency for E2E logic validation

## Tradeoff
Requires careful contract alignment with real repositories.

---

# 9. MQTT Handler Must Be Dumb

## Decision
MQTTHandler must contain no business logic.

## Rationale
Interface layer should:

- only translate transport → application call
- not contain orchestration logic

This ensures:

- testability
- separation of concerns
- portability to other protocols

---

# 10. Explicit State Machines in Domain

## Decision
All lifecycle transitions are explicitly validated.

## Rationale
Prevents invalid states such as:

- ACK before SENT
- expired commands being retried incorrectly

Implementation:

- ALLOWED_TRANSITIONS map
- enforced inside entity methods

---

# 11. Django Used Only in Infrastructure Layer

## Decision
Restrict Django ORM usage to infrastructure layer.

## Rationale
Prevents:

- domain coupling to ORM
- framework lock-in
- test complexity

---

# 12. Separation of Telemetry and Command Concerns

## Decision
Treat telemetry and commands as independent flows.

## Rationale
They have different characteristics:

- telemetry: high frequency, append-only
- commands: stateful, lifecycle-driven

---

# 13. Test Strategy Alignment with Architecture

## Decision
Align tests with architecture layers:

- unit → domain logic
- integration → adapters + use cases
- e2e → full MQTT flows

## Rationale
Ensures confidence at each abstraction level.

---

# Summary

These decisions reflect a consistent goal:

> Build a production-grade IoT backend that is decoupled, testable, and scalable without sacrificing clarity.

They also reflect iterative refinement based on real architectural pressure points discovered during development.