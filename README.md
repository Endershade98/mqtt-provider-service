# MQTT Provider Service

## Overview

MQTT Provider Service is a production-grade backend system designed to manage large-scale IoT device fleets communicating via MQTT.

The system is built to ensure:

* Reliable ingestion of high-frequency telemetry streams
* Strong consistency in device and command state management
* Real-time event propagation to external clients
* Horizontal scalability across all processing layers

It is implemented following **Clean Architecture**, **Domain-Driven Design (DDD)**, and **Test-Driven Development (TDD)** principles, with a strong emphasis on separation of concerns and event-driven design.

---

## Architectural Principles

The system enforces strict architectural boundaries:

* Domain layer is framework-agnostic and contains all business rules
* Application layer orchestrates use cases and domain interactions
* Infrastructure layer implements external integrations (MQTT, DB, Redis, Celery)
* Interface layer exposes APIs, MQTT handlers, and WebSocket consumers
* Communication between components is event-driven where possible
* Observability is treated as a separate concern from domain logic

---

## System Architecture

```
src/
├── domain/           # Business logic (entities, value objects, aggregates, domain events)
├── application/      # Use cases and orchestration layer
├── infrastructure/   # External systems (MQTT, DB, Redis, Celery)
├── interfaces/       # REST API, MQTT handlers, WebSocket consumers
```

---

## Core Design Concepts

### Domain-Centric Design

The domain layer models the core business concepts:

* Device lifecycle and state transitions
* Command lifecycle and execution guarantees
* Telemetry as a business event stream

Domain logic is fully independent of frameworks and infrastructure concerns.

---

### Event-Driven Architecture

The system is built around domain and integration events:

* Domain events represent business facts (e.g. DeviceBecameOnline)
* Integration events are used for external propagation (Redis, WebSockets)
* Outbox pattern ensures reliable event delivery

---

### Separation of Execution Traces

Operational traces (MQTT, Celery, WebSocket states) are not part of the domain model.
They exist solely for observability, logging, and debugging purposes.

---

## Core Components

### MQTT Worker

Responsible for consuming MQTT messages and forwarding them to the application layer.

Responsibilities:

* Manage MQTT connection lifecycle
* Handle reconnection and LWT scenarios
* Parse incoming topics and payloads
* Delegate processing to application use cases

No business logic is implemented in this layer.

---

### Application Layer

Implements use cases that orchestrate domain behavior.

Examples:

* HandleTelemetryUseCase
* SendCommandUseCase
* UpdateDeviceStateUseCase

Responsibilities:

* Load aggregates from repositories
* Execute domain logic
* Persist state changes
* Emit domain events
* Register outbox events for asynchronous processing

---

### Domain Layer

Contains the core business model:

* Device aggregate
* Command aggregate
* Telemetry entity
* Value objects (DeviceId, Topic, Payload)
* Domain events

The domain layer enforces all business invariants and state transition rules.

---

### Persistence Layer

Implements repository interfaces using Django ORM.

Key principles:

* Domain models remain independent of ORM
* Mapping between domain and persistence models is explicit
* All writes are transactional
* Outbox table ensures reliable event dispatching

---

### Event Dispatching System

A dedicated mechanism ensures reliable propagation of events:

* Domain events are stored in an outbox table within the same transaction
* A background worker (Celery) dispatches events asynchronously
* Redis and WebSocket layers consume integration events

---

### WebSocket Layer

Provides real-time communication with frontend clients using Django Channels.

Responsibilities:

* Subscribe to Redis event streams
* Transform integration events for frontend consumption
* Broadcast updates to connected clients

---

### Task Processing

Asynchronous execution is handled via Celery.

Components:

* Celery workers for background execution
* Celery Beat for scheduled tasks
* Optional cron-based container for simple scheduling

---

## Data Flow

### Telemetry Flow

1. Device publishes telemetry via MQTT
2. MQTT Worker receives and parses message
3. Application Use Case processes telemetry
4. Domain updates device state and emits events
5. Events are stored in outbox table
6. Celery dispatcher publishes events to Redis
7. WebSocket layer broadcasts updates to clients

---

### Command Flow

1. External system triggers command via API
2. Application layer creates command aggregate
3. Command is persisted and dispatched via MQTT
4. Device acknowledges execution
5. Command state is updated and events emitted
6. Event propagation follows outbox pipeline

---

## Technology Stack

* Python
* Django (ASGI)
* Django Channels
* Redis (pub/sub + caching)
* Celery (task queue)
* MQTT broker (EMQX or Mosquitto)
* PostgreSQL (recommended)

---

## Testing Strategy

The system follows a strict layered testing approach:

### Unit Tests

* Domain logic validation
* Value object correctness
* Use case behavior

### Integration Tests

* Repository implementations
* MQTT message flow
* Redis event propagation

### End-to-End Tests

* Full device-to-frontend flows
* MQTT → application → DB → WebSocket pipeline

---

## Deployment Model

The system is designed for containerized deployment.

Typical services:

* Django ASGI server
* MQTT worker
* Redis instance
* PostgreSQL database
* Celery workers
* Celery Beat scheduler

Each component is independently scalable.

---

## Scalability Considerations

* Stateless application services
* Horizontal scaling of MQTT workers
* Event-driven decoupling via Redis and outbox pattern
* Separation of read/write workloads where necessary

---

## Observability

Observability is implemented as a separate concern from domain logic.

Includes:

* Structured logging
* Metrics collection (MQTT throughput, command success rate, failures)
* Health checks for all infrastructure components
* Optional distributed tracing integration

---

## Design Goals

* High reliability in IoT communication
* Strong consistency in domain state
* Clear architectural boundaries
* Horizontal scalability
* Production-grade observability
* Maintainable and testable codebase

---

## Future Enhancements

* Device authentication (certificates / token-based)
* Advanced telemetry analytics pipeline
* Multi-tenant architecture support
* Kubernetes-native deployment
* Advanced observability stack (Prometheus, OpenTelemetry)

---

## License

This project is released under the terms defined in the LICENSE file.
