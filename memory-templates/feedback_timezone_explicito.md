---
name: Ao mexer com crons/agendamentos, sempre explicitar timezone
description: Crons e schedules silenciosos com timezone errado causam bugs confusos — sempre confirmar TZ
type: feedback
---

Ao criar, editar ou diagnosticar cron jobs, systemd timers, ou qualquer agendamento, sempre explicitar o timezone do sistema e confirmar com o usuario se bate com o horario esperado.

**Why:** VPS geralmente roda em UTC, mas o usuario pensa em horario local (ex: BRT = UTC-3). "Rode as 9h" pode virar "rode as 6h local" se ninguem notar. Esse tipo de bug e invisivel e dificil de pegar.

**How to apply:** Antes de commitar um cron novo ou interpretar um existente, rodar `timedatectl` (Linux) ou `date` (Mac) pra ver o TZ. Declarar no output: "cron vai rodar as 09:00 UTC = 06:00 BRT". Se precisar que rode em horario local, ou muda o TZ do sistema (risco), ou ajusta a hora do cron.
