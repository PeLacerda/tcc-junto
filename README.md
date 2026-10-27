# TCC AirH2O

Monitoramento do nível da cisterna: ESP32 (sensores de nível) → API (FastAPI) → front-end (tanque de cisterna).

- `arduino/airh2o_monitor/` — firmware do ESP32-WROOM-32 (abrir `airh2o_monitor.ino` na Arduino IDE)
- `back-end/` — API FastAPI + SQLite
- `front-end/index.html` — painel

## Como rodar a demonstração
1. PC e ESP32 na mesma rede Wi-Fi. Descubra o IP do PC (`hostname -I`).
2. `back-end/`: `alembic upgrade head` e `python -m uvicorn main:app --host 0.0.0.0 --port 8000`.
3. `arduino/airh2o_monitor/config.h`: preencha `WIFI_SSID`, `WIFI_PASSWORD` e `API_BASE_URL` (IP do PC). Envie para a placa.
4. `front-end/index.html`: ajuste `API_URL` (mesmo IP) e abra no navegador.
5. Ligue um fio de nível ao GND (curto): o ESP envia na hora e o tanque atualiza em até 2 s.
