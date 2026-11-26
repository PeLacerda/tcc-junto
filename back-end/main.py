#* para rodar o projeto: python -m uvicorn main:app --host 0.0.0.0 --port 8000  (o --host 0.0.0.0 é necessário para o ESP32 acessar) *#
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/", include_in_schema=False)
async def servir_painel():
    painel = Path(__file__).resolve().parent.parent / "front-end" / "index.html"
    return FileResponse(painel)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# importar os roteadores de requisições
from auth_routes import auth_router
from order_routes import order_router
from medicao_routes import medicao_router

# incluir os roteadores a aba main
app.include_router(auth_router)
app.include_router(order_router)
app.include_router(medicao_router)