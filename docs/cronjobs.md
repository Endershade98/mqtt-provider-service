# Cronjob Container

An alternative to Celery Beat is a dedicated cronjob container.

## Responsibilities

* Execute scheduled commands at fixed intervals
* Trigger application use cases via management commands

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Waiting
    Waiting --> RunningCron
    RunningCron --> InvokingUseCase
    InvokingUseCase --> CronSuccess
    InvokingUseCase --> CronFail
    CronSuccess --> Waiting
    CronFail --> Waiting
```

## Notes

* Suitable for simple periodic tasks
* Each cronjob must call application use cases
* Should not contain business logic
