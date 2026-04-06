STRATEGIA GENERALE

Ogni Epic segue questo ciclo:
```
Design → Domain → Use Case → Adapter → Test → Refactor
```
E ogni Epic deve produrre:

- codice funzionante
- test unit
- test integration
- flusso end-to-end verificato

### EPIC 1: Fondazioni architetturali (DDD + Clean Architecture)
Obiettivo

Separare completamente dominio, applicazione e infrastruttura.

Tasks
Creare struttura:
domain/
application/
infrastructure/
interfaces/
Definire primi bounded contexts:
Device
Telemetry
Command
Creare prime entity:
Device
Command
Creare repository interface (astratte)
Implementare repository Django (adapter)
Spostare logica fuori da Django models
Test
Unit test sulle entity (domain puro)
Test repository (integration DB)

### EPIC 2: Gestione Device (Digital Twin)
Obiettivo

Gestire stato device in modo consistente.

Tasks
Creare Device entity con metodi:
mark_online()
mark_offline()
Creare DeviceState value object
Creare DeviceRepository
Implementare UpdateDeviceStateUseCase
Gestire:
last_seen
is_online
Test
Unit test entity
Test use case
Integration test DB

### EPIC 3: Ingestion Telemetria (core MQTT)
Obiettivo

Gestire correttamente i messaggi MQTT.

Tasks
Creare HandleTelemetryUseCase
Separare parsing topic → utility
Integrare repository device
Salvare telemetria
Aggiornare stato device
Test
Unit test parsing
Unit test use case
Integration test MQTT → DB

### EPIC 4: MQTT Adapter (Infrastructure Layer)
Obiettivo

Trasformare MQTT in un adapter puro.

Tasks
Refactor MQTTClient
Creare MQTTHandler
Collegare handler → use case
Implementare riconnessione automatica
Implementare LWT
Test
Mock MQTT client
Integration test con broker

### EPIC 5: Command Management
Obiettivo

Gestire lifecycle comandi.

Tasks
Creare Command entity
Creare SendCommandUseCase
Creare CommandRepository
Implementare stati:
pending
sent
ack
failed
Integrare publisher MQTT
Test
Unit test entity
Test use case
Integration test publish

### EPIC 6: Retry e resilienza
Obiettivo

Gestire device offline e retry.

Tasks
Implementare RetryCommandUseCase
Refactor retry_commands.py
Gestire max_retries
Logging errori
Scheduling (cron o Celery)
Test
Unit test retry logic
Integration test retry flow

### EPIC 7: Event-driven architecture (Redis + Channels)
Obiettivo

Integrare realtime event streaming.

Tasks
Integrare Redis
Creare EventPublisher
Pubblicare eventi:
telemetry
device_state
command
Integrare Django Channels
Test
Integration test Redis pub/sub
Test WebSocket events

### EPIC 8: API Layer (interfaccia esterna)
Obiettivo

Esporre API REST pulite.

Tasks
Creare API /devices
Creare API /commands
Validazione input (serializer)
Collegare API → use cases
Test
API test
Integration test end-to-end

### EPIC 9: Sicurezza e autenticazione
Obiettivo

Proteggere accesso device.

Tasks
Implementare AuthService
Validazione:
username/password
certificate
Integrare con MQTT broker
Test
Unit test auth
Integration test accesso device

### EPIC 10: Observability e monitoring
Obiettivo

Monitorare il sistema.

Tasks
Logging strutturato
Metriche:
messaggi MQTT
errori
Health check endpoint
Event tracing
Test
Test logging
Test metriche

### EPIC 11: Performance e scalabilità
Obiettivo

Preparare scaling.

Tasks
Shared subscriptions MQTT
Parallel worker
Ottimizzazione DB
Cache Redis
Test
Load test
Stress test

### EPIC 12: Testing completo (TDD enforcement)
Obiettivo

Garantire qualità.

Tasks
Strutturare test:
tests/
├── unit/
├── integration/
├── e2e/
Aggiungere coverage
Mock MQTT e Redis
Test
Coverage > 80%
Test end-to-end completi