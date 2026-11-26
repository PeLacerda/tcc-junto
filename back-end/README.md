# API AirH2O (FastAPI + SQLite)

## Instalar
```
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy "passlib[bcrypt]" "bcrypt==4.0.1" python-jose[crypt] python-dotenv python-multipart alembic
```

## Criar/atualizar o banco (cria usuarios e medicoes)
```
alembic upgrade head
```

## Rodar
```
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

## Rotas de medição
- `POST /api/medicoes` — recebe o JSON enviado pelo ESP32.
- `GET  /api/medicoes/ultima` — último nível, usado pelo tanque de cisterna do front.
- `GET  /api/medicoes/historico?limite=50` — últimas medições, usadas no log de eventos do front (limite de 1 a 200).
