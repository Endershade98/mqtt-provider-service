# Architecture Overview

This project is designed as a scalable IoT backend using a Clean Architecture and Domain-Driven Design (DDD) approach.

The system is composed of multiple independent components:

* MQTT Worker (message ingestion)
* Application Layer (use cases)
* Domain Layer (business logic)
* Persistence Layer (database)
* Redis (event streaming and channel layer)
* Django ASGI + Channels (WebSocket communication)
* Celery + Beat (asynchronous tasks)
* Cronjob container (optional scheduled tasks)
* Frontend (React dashboard)

## High-Level Flow

1. Devices publish telemetry via MQTT.
2. MQTT Worker consumes messages and invokes application use cases.
3. Domain logic updates system state and persists data.
4. Events are published to Redis.
5. WebSocket consumers broadcast updates to frontend clients.
6. Background tasks (Celery or cron) handle retries and maintenance.

## Architectural Principles

* Strict separation of concerns (Domain, Application, Infrastructure, Interfaces)
* Stateless services for horizontal scalability
* Event-driven communication via Redis
* Idempotent operations for reliability
* Testability at all layers (unit, integration, end-to-end)
