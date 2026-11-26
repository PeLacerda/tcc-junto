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

## Cadastro e login
Configure uma chave JWT no arquivo `.env` dentro de `back-end/` antes de iniciar a API:
```
SECRET_KEY=<chave-aleatoria-gerada-pelo-comando-abaixo>
```
Gere a chave com `python -c "import secrets; print(secrets.token_urlsafe(32))"` e coloque o resultado no `.env`.

- `POST /auth/criar_usuario` — cria uma conta com senha protegida por hash.
- `POST /auth/login` — valida email e senha e retorna um token de acesso.
- `GET /auth/me` — consulta a conta autenticada.
- `PUT /auth/me` — atualiza nome, email, telefone e endereço.
- `POST /auth/alterar_senha` — troca a senha após validar a senha atual.
- `DELETE /auth/me` — exclui a conta autenticada.

Envie o token retornado no cabeçalho `Authorization: Bearer <token>` para as rotas protegidas. O painel já usa esses endpoints nos formulários de cadastro, login e perfil.

## Rotas de medição
- `POST /api/medicoes` — recebe o JSON enviado pelo ESP32.
- `GET  /api/medicoes/ultima` — último nível, usado pelo tanque de cisterna do front.
- `GET  /api/medicoes/historico?limite=50` — últimas medições, usadas no log de eventos do front (limite de 1 a 200).
