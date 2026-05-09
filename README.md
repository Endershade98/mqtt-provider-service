# MQTT Provider Service

Production-grade backend service for managing IoT device fleets through MQTT.

Designed to demonstrate modern backend engineering practices:

- Clean Architecture
- Domain Driven Design (DDD)
- Test Driven Development (TDD)
- Event-Driven Systems
- Transactional Outbox Pattern
- Scalable Messaging Pipelines

---

# Project Goal

Most MQTT backends become tightly coupled to frameworks, brokers, and persistence layers.

This project demonstrates how to build an IoT backend where:

- business logic remains framework-agnostic
- infrastructure can evolve independently
- message ingestion remains scalable
- domain consistency is protected
- testing remains fast and maintainable

---

# Core Features

## Device Lifecycle Management

Track device operational state:

- online
- offline
- heartbeat updates
- last_seen timestamps

---

## Command Execution Pipeline

Supports full command lifecycle:

- pending
- sent
- acknowledged
- failed
- retrying
- expired

All transitions are enforced by explicit domain rules.

---

## MQTT Telemetry Ingestion

Receives telemetry messages such as:

devices/{device_id}/telemetry

Processes payloads and stores telemetry consistently.

---

## MQTT ACK Flow

Receives acknowledgements such as:

devices/{device_id}/ack

Updates command state safely.

---

## Reliable Event Publishing

Uses Outbox Pattern to ensure:

- aggregate persistence and events happen atomically
- no dual-write inconsistencies
- async dispatch can be retried safely

---

# Architecture

src/
├── domain/
├── application/
├── interfaces/
├── infrastructure/

---

# Layer Responsibilities

## Domain

Pure business logic.

Contains:

- Entities
- Value Objects
- Domain Events
- State Machines

Framework independent.

---

## Application

Coordinates use cases.

Examples:

- HandleTelemetryUseCase
- AcknowledgeCommandUseCase
- SendCommandUseCase

Responsibilities:

- load aggregates
- invoke domain behavior
- commit transactions
- publish events

---

## Interfaces

System entry points:

- MQTT handlers
- REST APIs
- WebSocket consumers

---

## Infrastructure

Adapters and external systems:

- Django ORM repositories
- MQTT client
- Redis
- Celery
- PostgreSQL-ready persistence layer

---

# MQTT Processing Flow

MQTT Broker
↓
MQTT Client
↓
Handler
↓
Translator (ACL)
↓
Router
↓
Use Case
↓
Domain
↓
Repository + Outbox

---

# Testing Strategy

## Unit Tests

Covers:

- domain entities
- value objects
- state transitions
- DTO validation

## Integration Tests

Covers:

- repositories
- use cases
- MQTT adapters
- persistence boundaries

## End-to-End Tests

Covers:

- MQTT ACK flow
- telemetry pipeline

---

## Current Quality Status

- 76 tests passing
- 90%+ coverage
- strict architectural boundary tests enabled

---

# Engineering Decisions

This project intentionally favors:

- explicit code over magic abstractions
- composition over inheritance
- rich domain models over anemic services
- maintainability over shortcuts
- deterministic testing over fragile integration setups

---

# Documentation

See `/docs`

- architecture.md
- testing.md
- decisions.md
- epic-history.md
- local-setup.md

---

# Local Development

## Run tests

pytest

## Run coverage

pytest --cov=src --cov-report=term-missing

---

# Tech Stack

- Python 3.11
- Django
- Pytest
- MQTT (Paho client)
- Redis
- Celery
- PostgreSQL-ready

---

# Future Enhancements

- Device authentication
- Retry scheduler
- Metrics + observability
- Dockerized local stack
- Kubernetes deployment
- Multi-tenant support

---

# Why This Repository Matters

This repository was built as a portfolio-grade backend system to demonstrate skills relevant to modern software engineering roles:

- distributed systems thinking
- scalable backend architecture
- messaging systems
- maintainable code design
- production-oriented testing strategy

---

# License

MIT