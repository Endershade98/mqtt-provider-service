# System State Tables

This document defines the states used across the system components.

---

## MQTT Worker States

| State Code | Name              | Description                    |
| ---------- | ----------------- | ------------------------------ |
| DIS        | Disconnected      | Not connected to broker        |
| CON        | Connecting        | Attempting connection          |
| CND        | Connected         | Connected to broker            |
| MSG_RCV    | ReceivingMessage  | Message received               |
| MSG_PROC   | ProcessingMessage | Message parsing and validation |
| DOM_UPD    | UpdatingDomain    | Use case execution             |

---

## WebSocket States

| State Code | Name            | Description             |
| ---------- | --------------- | ----------------------- |
| IDL        | Idle            | No active connection    |
| CC         | ClientConnected | WebSocket connected     |
| RECV       | ReceivingEvent  | Receiving data          |
| PROC       | ProcessingEvent | Processing event        |
| BC         | Broadcast       | Sending data to clients |
| DISC       | Disconnected    | Connection closed       |

---

## Celery States

| State Code | Name        | Description     |
| ---------- | ----------- | --------------- |
| IDL        | Idle        | No task running |
| SCH        | Scheduled   | Task scheduled  |
| RUN        | RunningTask | Task executing  |
| OK         | TaskSuccess | Task completed  |
| FAIL       | TaskFailed  | Task failed     |
| RET        | Retry       | Retrying task   |

---

## Cronjob States

| State Code | Name            | Description               |
| ---------- | --------------- | ------------------------- |
| WAIT       | Waiting         | Waiting for schedule      |
| RUN        | RunningCron     | Cron executing            |
| CALL       | InvokingUseCase | Calling application layer |
| OK         | Success         | Task completed            |
| FAIL       | Failure         | Task failed               |

---

## Frontend States

| State Code | Name          | Description             |
| ---------- | ------------- | ----------------------- |
| IDL        | Idle          | Initial state           |
| CON        | ConnectingWS  | Connecting to WebSocket |
| CND        | Connected     | Connected to backend    |
| RCV        | ReceivingData | Receiving updates       |
| UI_UPD     | UpdatingUI    | Updating interface      |
| DISC       | Disconnected  | Connection lost         |
