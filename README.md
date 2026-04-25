# MQTT Provider Service

## Overview

MQTT Provider Service is a scalable backend system designed to manage IoT devices through the MQTT protocol.
The system focuses on reliable message ingestion, device state management, and real-time data propagation to connected clients.

It is built following **Clean Architecture**, **Domain-Driven Design (DDD)**, and **Test-Driven Development (TDD)** principles to ensure maintainability, scalability, and testability.

---

## Key Features

* MQTT-based device communication
* Real-time telemetry ingestion and processing
* Command dispatch with retry mechanisms
* Device state tracking (online/offline, last seen)
* WebSocket-based real-time updates
* Asynchronous task processing
* Modular and scalable architecture

---

## Architecture

The system is structured into clearly separated layers:

```
src/
├── domain          # Business logic (entities, value objects, repository interfaces)
├── application     # Use cases (orchestrates domain logic)
├── infrastructure  # External systems (MQTT, database, Celery, Redis)
├── interfaces      # API, MQTT handlers, WebSocket consumers
```

### Architectural Principles

* Dependency inversion: outer layers depend on inner layers
* Domain isolation: no framework dependencies in domain layer
* Stateless services for horizontal scalability
* Event-driven communication for real-time updates
* Explicit separation of responsibilities

---

## Core Components

### MQTT Worker

Consumes messages from the MQTT broker and delegates processing to application use cases.

* Handles connection lifecycle
* Supports automatic reconnection
* Implements Last Will and Testament (LWT)
* Delegates message handling to interface layer

### Application Layer

Implements use cases such as:

* Handle telemetry ingestion
* Send commands to devices
* Update device state

### Domain Layer

Defines core business logic:

* Device entity
* Command lifecycle
* Telemetry events
* Repository contracts

### Persistence Layer

Implements repositories using Django ORM while keeping domain logic independent.

### WebSocket Layer

Provides real-time updates to frontend clients using Django Channels and Redis.

### Task Processing

Handles asynchronous and scheduled tasks using:

* Celery (distributed task queue)
* Celery Beat (scheduler)
* Optional cronjob container

---

## Data Flow

1. Devices publish telemetry via MQTT.
2. MQTT Worker receives messages and forwards them to handlers.
3. Handlers invoke application use cases.
4. Domain logic processes the data and updates state.
5. Data is persisted through repository implementations.
6. Events are propagated to Redis.
7. WebSocket consumers broadcast updates to frontend clients.

---

## Technologies

* Python
* Django
* Django Channels
* Redis
* Celery
* MQTT (EMQX or Mosquitto)
* PostgreSQL (recommended for production)

---

## Project Structure

```
config/             # Django configuration
docs/               # Project documentation and architecture diagrams
src/
  application/      # Use cases
  domain/           # Business logic
  infrastructure/   # External integrations
  interfaces/       # API, MQTT, WebSocket
tests/
  unit/             # Unit tests
  integration/      # Integration tests
  e2e/              # End-to-end tests
```

---

## Testing Strategy

The project follows a layered testing approach:

* Unit tests for domain and application logic
* Integration tests for database and MQTT interactions
* End-to-end tests simulating real device flows

All business-critical logic is covered by tests before integration.

---

## Deployment

The system is designed to run in a containerized environment.

Typical services include:

* Django ASGI server
* MQTT Worker
* Redis
* PostgreSQL
* Celery workers
* Celery Beat scheduler

Each component can be scaled independently.

---

## Design Goals

* High reliability in device communication
* Clear separation of concerns
* Ease of testing and maintenance
* Horizontal scalability
* Real-time data propagation

---

## Future Improvements

* Device authentication via certificates or tokens
* Advanced telemetry analytics
* Multi-tenant support
* Observability (metrics, tracing, logging)
* Kubernetes-based deployment

---

## License

This project is released under the terms of the LICENSE file.
