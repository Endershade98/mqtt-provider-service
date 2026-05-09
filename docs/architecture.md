# Architecture Overview

This document describes the high-level architecture of the MQTT Provider Service.

The system is designed using **Clean Architecture**, **Domain Driven Design (DDD)**, and **Event-Driven principles**, with strict separation between business logic and infrastructure concerns.

---

# Architectural Style

The system follows Clean Architecture principles:

- Domain layer contains pure business logic
- Application layer orchestrates use cases
- Interface layer handles external communication (MQTT, API, WebSocket)
- Infrastructure layer provides technical implementations (DB, broker, queues)

---

# Dependency Rule

All dependencies point inward:

```text
interfaces
   ↓
application
   ↓
domain
````

Infrastructure is an adapter layer and depends on application/domain, never the reverse.

---

# High-Level Structure

```text
src/
├── domain/           # Business rules (entities, value objects, domain events)
├── application/      # Use cases and orchestration
├── interfaces/       # MQTT handlers, API, WebSocket entry points
├── infrastructure/   # External systems (DB, MQTT, Redis, Celery)
```

---

# Core Design Principles

## 1. Domain-Centric Design

The domain is the center of the system.

It models:

* Devices
* Commands
* Telemetry
* State transitions
* Business invariants

The domain is completely framework-agnostic.

---

## 2. Explicit State Machines

Entities enforce valid transitions explicitly.

Example:

* Command lifecycle is strictly controlled
* Invalid transitions raise domain exceptions
* State changes are fully deterministic

---

## 3. Event-Driven Architecture

The system produces domain events:

* CommandCreated
* CommandSent
* CommandAcknowledged
* DeviceStateChanged
* TelemetryReceived

Events are stored via the **Outbox Pattern** to guarantee consistency.

---

## 4. Outbox Pattern

To avoid dual-write problems:

1. Domain changes occur
2. Events are collected
3. Both state + events are committed in a single transaction
4. A background worker dispatches events asynchronously

This ensures:

* no lost events
* no partial writes
* eventual consistency guarantees

---

## 5. ACL (Anti-Corruption Layer)

MQTT is treated as an external protocol.

The system isolates it using:

* MQTTMessageTranslator

Responsibilities:

* parse topics
* normalize payloads
* convert into application DTOs

This prevents MQTT structure from leaking into the domain.

---

# MQTT Processing Pipeline

```text
MQTT Broker
   ↓
MQTT Client (Infrastructure)
   ↓
MQTT Handler (Interface Layer)
   ↓
Translator (ACL)
   ↓
Application Router
   ↓
Use Case
   ↓
Domain Model
   ↓
Repository + Outbox
```

---

# Layer Responsibilities

## Domain Layer

Pure business logic.

Contains:

* Entities (Command, Device, Telemetry)
* Value Objects (DeviceId, Topic, CommandId)
* Domain Events
* State Machines

No dependencies on frameworks or infrastructure.

---

## Application Layer

Orchestration layer.

Responsibilities:

* execute use cases
* load aggregates from repositories
* invoke domain behavior
* persist state changes
* register domain events
* ensure transactional consistency

Example use cases:

* HandleTelemetryUseCase
* AcknowledgeCommandUseCase
* SendCommandUseCase

---

## Interface Layer

Entry points to the system.

Includes:

* MQTT Handlers
* REST API (optional)
* WebSocket consumers (optional)

Responsibilities:

* receive external input
* validate transport format
* delegate to application layer

No business logic allowed.

---

## Infrastructure Layer

Technical implementation details.

Includes:

* MQTT client (Paho)
* Django ORM repositories
* Redis integration
* Celery workers
* Unit of Work implementation

Responsibilities:

* persistence
* messaging
* external system integration

---

# Key Flows

## Telemetry Flow

```text
Device → MQTT Broker → MQTT Client → Handler → Translator → Use Case → Domain → Repository → Outbox
```

Steps:

1. Device sends telemetry
2. MQTT message received
3. Topic + payload translated
4. HandleTelemetryUseCase executed
5. Device state updated
6. Telemetry persisted
7. Events stored in outbox

---

## Command Flow

```text
API → Use Case → Domain → Repository → Outbox → MQTT Publisher → Device → ACK → MQTT Handler → Use Case
```

Steps:

1. Command created
2. Command sent to device
3. Device executes command
4. Device sends ACK
5. ACK processed by system
6. Command marked as ACKED

---

# Consistency Model

The system uses:

* Strong consistency inside a transaction boundary
* Eventual consistency for external systems

Guarantees:

* no lost telemetry
* no lost command state updates
* deterministic domain state transitions

---

# Scalability Strategy

The system is designed to scale horizontally:

* MQTT workers are stateless
* Application layer is stateless
* Redis enables distributed event propagation
* Celery handles async workloads
* Database is the single source of truth

---

# Observability (Design Intent)

Observability is separated from domain logic:

* structured logging
* event tracing (future)
* metrics (future extension)

Domain remains pure and unaware of monitoring concerns.

---

# Design Tradeoffs

## Chosen:

* strict layering
* explicit orchestration
* domain purity
* event-driven consistency
* transactional outbox

## Avoided:

* framework coupling in domain
* hidden magic (signals, implicit ORM logic)
* shared global state
* business logic in infrastructure

---

# Evolution Notes

The architecture evolved through multiple refactoring phases:

* MQTT logic initially leaked into handlers → extracted via Translator
* Use cases initially too coupled → introduced router layer
* Domain events initially lost → solved with Outbox pattern
* Testability improved via fake repositories and UoW abstraction

---

# Summary

This architecture prioritizes:

* correctness
* maintainability
* testability
* scalability
* explicit control flow

It is designed as a production-grade reference implementation for IoT backend systems using MQTT.

