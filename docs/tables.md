# System State Model (Revised)

This document defines the operational state model of the system after applying Domain-Driven Design and Clean Architecture principles.

It replaces the previous unified "System State Tables" approach with a clear separation between:

* Domain States (business truth)
* Execution Traces (observability only)
* Infrastructure Lifecycle States (technical health)

---

# Core Principle

The system does not treat all states equally.

There are three distinct categories:

## 1. Domain States (Source of Truth)

Business-relevant states persisted in the domain model.

## 2. Execution Traces (Non-persistent)

Operational steps used for observability, debugging, and metrics.

## 3. Infrastructure Lifecycle States (System Health)

Technical connectivity and runtime conditions of infrastructure components.

---

# MQTT Worker Lifecycle (Infrastructure Trace)

These states describe the runtime behavior of the MQTT worker.
They are NOT part of the domain model.

| State Code | Name         | Description                                |
| ---------- | ------------ | ------------------------------------------ |
| DIS        | Disconnected | MQTT client is not connected to the broker |
| CON        | Connecting   | Attempting to establish connection         |
| CND        | Connected    | Successfully connected to broker           |
| SUB        | Subscribed   | Topic subscriptions completed              |
| IDLE       | Idle         | Waiting for incoming messages              |

---

# MQTT Message Processing Flow (Execution Trace)

Represents internal processing steps of incoming MQTT messages.
This is NOT a state machine and must not influence domain logic.

| State Code | Name             | Description                            |
| ---------- | ---------------- | -------------------------------------- |
| MSG_RCV    | MessageReceived  | Raw MQTT message received              |
| PARSED     | Parsed           | Topic and payload extracted            |
| VALID      | Validated        | Payload structure validated            |
| REJECTED   | Rejected         | Invalid message or unknown device      |
| ROUTE      | Routed           | Message forwarded to application layer |
| EXEC       | ExecutingUseCase | Use case execution triggered           |
| DONE       | Completed        | Processing completed successfully      |

---

# Device State (Domain Model)

Core business state of an IoT device.

| State Code | Name    | Description                                    |
| ---------- | ------- | ---------------------------------------------- |
| OFF        | Offline | Device not connected or LWT triggered          |
| ON         | Online  | Device actively communicating                  |
| STALE      | Stale   | No telemetry received within expected interval |
| UNKNOWN    | Unknown | Device registered but no telemetry yet         |

---

# Command Lifecycle State (Domain Model)

Represents the business lifecycle of a command aggregate.

| State Code | Name         | Description                        |
| ---------- | ------------ | ---------------------------------- |
| PND        | Pending      | Command created but not dispatched |
| SENT       | Sent         | Command published to MQTT broker   |
| ACK        | Acknowledged | Device confirmed execution         |
| FAIL       | Failed       | Execution or delivery failure      |
| RETRY      | Retrying     | Retry attempt in progress          |
| EXPIRED    | Expired      | Retry limit exceeded               |

---

# WebSocket Connection Lifecycle (Infrastructure Trace)

Represents lifecycle of real-time connections.

| State Code | Name           | Description                     |
| ---------- | -------------- | ------------------------------- |
| IDL        | Idle           | No active connection            |
| CONN       | Connecting     | WebSocket handshake in progress |
| OPEN       | Connected      | Connection established          |
| AUTH       | Authorized     | Client authenticated            |
| SUB        | Subscribed     | Subscribed to channels          |
| RECV       | ReceivingEvent | Event received from Redis       |
| SEND       | Sending        | Sending data to client          |
| DISC       | Disconnected   | Connection closed               |

---

# Celery Task Execution Trace

Represents asynchronous task execution lifecycle.

| State Code | Name       | Description                 |
| ---------- | ---------- | --------------------------- |
| IDL        | Idle       | No task executing           |
| SCH        | Scheduled  | Task scheduled              |
| QUE        | Queued     | Waiting in broker queue     |
| RUN        | Running    | Task executing              |
| OK         | Success    | Task completed successfully |
| FAIL       | Failed     | Task execution failed       |
| RET        | Retrying   | Retry in progress           |
| MAX_RET    | MaxRetries | Retry limit reached         |

---

# Cronjob Execution Trace

Represents scheduled job execution flow.

| State Code | Name            | Description               |
| ---------- | --------------- | ------------------------- |
| WAIT       | Waiting         | Waiting for trigger       |
| TRIG       | Triggered       | Execution started         |
| RUN        | Running         | Task executing            |
| CALL       | InvokingUseCase | Application logic invoked |
| OK         | Success         | Execution completed       |
| FAIL       | Failure         | Execution failed          |
| LOG        | Logging         | Result persisted          |

---

# Frontend UI State Model (React)

Represents client-side UI and connection state.

| State Code | Name          | Description                       |
| ---------- | ------------- | --------------------------------- |
| INIT       | Initializing  | Application booting               |
| IDL        | Idle          | No active connection              |
| CON        | ConnectingWS  | Establishing WebSocket connection |
| CND        | Connected     | WebSocket connected               |
| SUB        | Subscribed    | Subscribed to backend streams     |
| RCV        | ReceivingData | Receiving updates                 |
| SYNC       | Syncing       | Synchronizing state               |
| UI_UPD     | UpdatingUI    | UI re-rendering                   |
| ERR        | Error         | Error state                       |
| DISC       | Disconnected  | Connection lost                   |

---

# System-Wide Error Taxonomy (Not a State Machine)

These represent categorized failure conditions across the system.
They are NOT lifecycle states.

| Code     | Name            | Description                             |
| -------- | --------------- | --------------------------------------- |
| NET_ERR  | NetworkError    | Network or broker connectivity issue    |
| AUTH_ERR | AuthError       | Authentication or authorization failure |
| VAL_ERR  | ValidationError | Payload or input validation failure     |
| PROC_ERR | ProcessingError | Use case or domain processing failure   |
| DB_ERR   | DatabaseError   | Persistence layer failure               |
| TIMEOUT  | Timeout         | Operation exceeded allowed time         |

---

# Notes

* Domain states represent business truth and are persisted.
* Execution traces are ephemeral and used only for observability.
* Infrastructure lifecycle states describe system health only.
* No execution trace may directly modify domain state.
* All domain state transitions must be deterministic and testable.
* Observability data must not leak into domain logic.
