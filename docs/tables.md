# System State Tables

This document defines the operational states across all core components of the system.
Each state represents a well-defined phase in the lifecycle of data processing, communication, and system execution.

---

## MQTT Worker States

| State Code | Name             | Description                                     |
| ---------- | ---------------- | ----------------------------------------------- |
| DIS        | Disconnected     | MQTT client is not connected to the broker      |
| CON        | Connecting       | Attempting to establish connection to broker    |
| CND        | Connected        | Successfully connected and subscribed to topics |
| SUB        | Subscribed       | Topics subscription completed                   |
| MSG_RCV    | MessageReceived  | Raw MQTT message received                       |
| MSG_VAL    | MessageValidated | Payload successfully parsed and validated       |
| MSG_ERR    | MessageError     | Payload parsing or validation failed            |
| ROUTE      | Routing          | Message forwarded to handler layer              |
| DOM_CALL   | DomainInvocation | Application use case execution triggered        |
| IDLE       | Idle             | Waiting for next message                        |

---

## MQTT Message Processing States (Application Flow)

| State Code | Name             | Description                          |
| ---------- | ---------------- | ------------------------------------ |
| IN         | Incoming         | Message received from MQTT layer     |
| PARSED     | Parsed           | Topic and payload extracted          |
| VALID      | Validated        | Message structure is valid           |
| REJECTED   | Rejected         | Message invalid or device unknown    |
| EXEC       | ExecutingUseCase | Application use case running         |
| DB_WRITE   | Persisting       | Data being stored via repository     |
| EVENT_PUB  | EventPublished   | Event propagated to Redis / Channels |
| DONE       | Completed        | Processing completed successfully    |

---

## Device State (Domain)

| State Code | Name    | Description                                        |
| ---------- | ------- | -------------------------------------------------- |
| OFF        | Offline | Device is not connected or LWT triggered           |
| ON         | Online  | Device is actively sending data                    |
| STALE      | Stale   | Device has not sent data within expected timeframe |
| UNKNOWN    | Unknown | Device exists but has no telemetry yet             |

---

## Command Lifecycle States

| State Code | Name         | Description                         |
| ---------- | ------------ | ----------------------------------- |
| PND        | Pending      | Command created but not sent        |
| SENT       | Sent         | Command published to MQTT broker    |
| ACK        | Acknowledged | Device confirmed execution          |
| FAIL       | Failed       | Command failed to send or execute   |
| RETRY      | Retrying     | Command is being retried            |
| EXPIRED    | Expired      | Retry limit reached without success |

---

## WebSocket / Channels States

| State Code | Name            | Description                          |
| ---------- | --------------- | ------------------------------------ |
| IDL        | Idle            | ASGI server ready, no active socket  |
| CONN       | Connecting      | WebSocket handshake in progress      |
| OPEN       | Connected       | WebSocket connection established     |
| AUTH       | Authorized      | Client authenticated (if applicable) |
| SUB        | Subscribed      | Client subscribed to channel/group   |
| RECV       | ReceivingEvent  | Event received from Redis            |
| PROC       | ProcessingEvent | Event transformed for frontend       |
| SEND       | Sending         | Data sent to client                  |
| DISC       | Disconnected    | Connection closed                    |

---

## Celery Task States

| State Code | Name       | Description                   |
| ---------- | ---------- | ----------------------------- |
| IDL        | Idle       | No task currently running     |
| SCH        | Scheduled  | Task scheduled by Celery Beat |
| QUE        | Queued     | Task waiting in broker queue  |
| RUN        | Running    | Task currently executing      |
| OK         | Success    | Task completed successfully   |
| FAIL       | Failed     | Task execution failed         |
| RET        | Retrying   | Task retry in progress        |
| MAX_RET    | MaxRetries | Retry limit reached           |

---

## Cronjob Execution States

| State Code | Name            | Description                     |
| ---------- | --------------- | ------------------------------- |
| WAIT       | Waiting         | Waiting for scheduled execution |
| TRIG       | Triggered       | Cron triggered execution        |
| RUN        | Running         | Task is executing               |
| CALL       | InvokingUseCase | Application use case invoked    |
| OK         | Success         | Task completed successfully     |
| FAIL       | Failure         | Task execution failed           |
| LOG        | Logging         | Execution result logged         |

---

## Frontend (React) States

| State Code | Name          | Description                       |
| ---------- | ------------- | --------------------------------- |
| INIT       | Initializing  | Application bootstrapping         |
| IDL        | Idle          | No active connection              |
| CON        | ConnectingWS  | Establishing WebSocket connection |
| CND        | Connected     | WebSocket connected               |
| SUB        | Subscribed    | Subscribed to backend channels    |
| RCV        | ReceivingData | Receiving real-time updates       |
| SYNC       | Syncing       | Updating application state        |
| UI_UPD     | UpdatingUI    | Rendering UI updates              |
| ERR        | Error         | Connection or processing error    |
| DISC       | Disconnected  | Connection lost                   |

---

## System-Wide Error States

| State Code | Name            | Description                          |
| ---------- | --------------- | ------------------------------------ |
| NET_ERR    | NetworkError    | Connectivity issue (MQTT, Redis, DB) |
| AUTH_ERR   | AuthError       | Authentication failure               |
| VAL_ERR    | ValidationError | Invalid payload or data              |
| PROC_ERR   | ProcessingError | Failure during use case execution    |
| DB_ERR     | DatabaseError   | Persistence failure                  |
| TIMEOUT    | Timeout         | Operation exceeded allowed time      |

---

## Notes

* All state transitions must be deterministic and testable.
* Each state should be observable through logs or monitoring tools.
* State codes are designed to be used in logs, metrics, and debugging.
* Application logic must operate on domain states, not infrastructure states.
