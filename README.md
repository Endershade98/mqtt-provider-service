Epic 1: MQTT Client robusto

Obiettivo: rendere il client MQTT resiliente, con LWT, riconnessione, gestione thread separati.

Tasks:

Creare MQTTClient in infrastructure/mqtt/client.py con loop separato da WSGI
Implementare riconnessione automatica e LWT
Scrivere log dettagliati per connessione, disconnessione e messaggi ricevuti
Aggiornare DeviceState su messaggi telemetria e LWT
Test: Unit test su on_message, integration test con broker MQTT simulato
Epic 2: Command Service con retry

Obiettivo: invio comandi sicuro, retry automatico, gestione errori.

Tasks:

Refactor di send_command per separare logica DB da publish MQTT
Implementare worker periodico retry_commands.py con Celery o cron
Logica di max_retries e gestione stato pending/sent/ack/failed
Pubblicare comandi anche sul Channel Layer per realtime (opzionale)
Test: unit test per logica retry, integration test per invio MQTT e aggiornamento DB
Epic 3: Telemetria e Digital Twin

Obiettivo: gestire telemetria con Digital Twin aggiornato in realtime.

Tasks:

Refactor TelemetryService per chiudere connessioni DB e separare parsing topic dalla logica DB
Aggiornare DeviceState con is_online, last_telemetry, firmware_version
Pubblicare dati su Django Channels Layer per frontend
Test: unit test parsing topic, integration test DB + MQTT, E2E test con simulazione device
Epic 4: Autenticazione device

Obiettivo: supportare sia certificate che username/password.

Tasks:

Creare AuthService nel service layer
Validare credenziali o certificate prima di permettere invio/subscribe
Log errori autenticazione
Test: unit test AuthService, integration test con MQTT broker che richiede auth
Epic 5: Struttura Clean Architecture

Obiettivo: garantire separazione netta tra app, services, infrastructure.

Tasks:

Separare logica business (services) da accesso DB (apps/iot)
Non scrivere logica business in views.py o models.py
Standardizzare pattern di sottoscrizione e publish MQTT con service layer
Test: test di architettura (linting + pattern adherence)
Epic 6: Test centralizzato

Obiettivo: avere una cartella unica per test unitari, integration e E2E.

Tasks:

Creare tests/ a livello src/ con sottocartelle:
```
src/tests/
├── unit/
│   ├── services/
│   ├── infrastructure/
│   └── apps/
├── integration/
│   ├── mqtt/
│   └── database/
└── e2e/
    └── devices_simulation/
```
Scrivere test base per ogni service layer (unit)
Scrivere integration test per MQTT ↔ DB
Scrivere E2E test simulando device reali con publish/subscribe