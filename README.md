# TCC AirH2O

Monitoramento do nível da cisterna: ESP32 (sensores de nível) → API (FastAPI) → front-end (tanque de cisterna).

- `arduino/airh2o_monitor/` — firmware do ESP32-WROOM-32 (abrir `airh2o_monitor.ino` na Arduino IDE)
- `back-end/` — API FastAPI + SQLite
- `front-end/index.html` — painel

## Como rodar a demonstração
1. Conecte o computador e o ESP32 à mesma rede local do hotspot do celular. No `config.h`, `WIFI_SSID` e `WIFI_PASSWORD` devem ser os dados do hotspot.
2. O endereço `192.168.137.1` configurado no firmware e no painel é o IPv4 confirmado do computador que executa a API (não o IP do ESP32). Se mudar de rede, confirme o IPv4 com `ipconfig` e atualize `API_BASE_URL` em `arduino/airh2o_monitor/config.h` e `API_HOST` em `front-end/index.html`.
3. Configure a chave JWT no arquivo `back-end/.env` conforme as instruções de [back-end/README.md](back-end/README.md).
4. No PowerShell, entre em `back-end/`, ative `.\venv\Scripts\Activate.ps1` e execute `alembic upgrade head` para criar/atualizar o banco SQLite. Depois, inicie a API com `python -m uvicorn main:app --host 0.0.0.0 --port 8000`.
5. No computador, abra `http://127.0.0.1:8000/` (HTTP, não HTTPS). A própria API serve o painel na mesma origem, evitando o bloqueio de conteúdo misto. Em outro dispositivo da rede, use `http://192.168.137.1:8000/`. Não use a versão publicada em HTTPS para acessar esta API local. Se o computador estiver conectado por USB ao celular, confirme que o hotspot permite comunicação entre os dispositivos; alguns celulares isolam os clientes.
6. Envie o firmware para a placa. Ligue um fio de nível ao GND (curto): o ESP envia a medição e o painel atualiza em até 2 s.
