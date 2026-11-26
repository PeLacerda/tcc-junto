import re
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session

from dependecies import pegar_sessao
from models import Usuario
from security import SECRET_KEY, bcrypt_context

auth_router = APIRouter(prefix="/auth", tags=["Autenticacao"])
bearer_scheme = HTTPBearer(auto_error=False)
JWT_ALGORITHM = "HS256"
TOKEN_DURATION_HOURS = 12


class CadastroUsuario(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    email: str
    senha: str = Field(min_length=8)
    telefone: int | None = None
    endereco: str | None = None


class LoginUsuario(BaseModel):
    email: str
    senha: str


class AtualizacaoUsuario(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    email: str
    telefone: int | None = None
    endereco: str | None = None


class AlteracaoSenha(BaseModel):
    senha_atual: str
    nova_senha: str = Field(min_length=8)


def normalizar_email(email: str) -> str:
    email = email.strip().lower()
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise HTTPException(status_code=422, detail="Informe um email valido")
    return email


def validar_senha(senha: str):
    if len(senha.encode("utf-8")) > 72:
        raise HTTPException(status_code=422, detail="A senha deve ter no maximo 72 bytes")
    if not any(letra.isalpha() for letra in senha) or not any(digito.isdigit() for digito in senha):
        raise HTTPException(status_code=422, detail="A senha deve conter letras e numeros")


def serializar_usuario(usuario: Usuario):
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "telefone": usuario.telefone,
        "endereco": usuario.endereco,
    }


def criar_token(usuario_id: int) -> str:
    if not SECRET_KEY or len(SECRET_KEY) < 32:
        raise HTTPException(
            status_code=500,
            detail="Configure uma SECRET_KEY com pelo menos 32 caracteres no arquivo .env",
        )

    expiracao = datetime.utcnow() + timedelta(hours=TOKEN_DURATION_HOURS)
    return jwt.encode(
        {"sub": str(usuario_id), "exp": expiracao},
        SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


def usuario_autenticado(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    session: Session = Depends(pegar_sessao),
) -> Usuario:
    if credentials is None or not SECRET_KEY:
        raise HTTPException(
            status_code=401,
            detail="Autenticacao necessaria",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )
        usuario_id = int(payload["sub"])
    except (JWTError, KeyError, TypeError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Token invalido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuario nao encontrado")
    return usuario


@auth_router.post("/criar_usuario", status_code=201)
async def criar_conta(dados: CadastroUsuario, session: Session = Depends(pegar_sessao)):
    if not SECRET_KEY or len(SECRET_KEY) < 32:
        raise HTTPException(
            status_code=500,
            detail="Configure uma SECRET_KEY com pelo menos 32 caracteres no arquivo .env",
        )
    email = normalizar_email(dados.email)
    validar_senha(dados.senha)
    nome = dados.nome.strip()
    if len(nome) < 2:
        raise HTTPException(status_code=422, detail="O nome deve ter pelo menos 2 caracteres")
    usuario_existente = session.query(Usuario).filter(
        func.lower(Usuario.email) == email
    ).first()
    if usuario_existente:
        raise HTTPException(status_code=409, detail="Este email ja esta cadastrado")

    usuario = Usuario(
        nome=nome,
        email=email,
        telefone=dados.telefone,
        senha=bcrypt_context.hash(dados.senha),
        endereco=dados.endereco,
    )
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return {"mensagem": "Conta criada com sucesso", "usuario": serializar_usuario(usuario)}


@auth_router.post("/login")
async def fazer_login(dados: LoginUsuario, session: Session = Depends(pegar_sessao)):
    email = normalizar_email(dados.email)
    usuario = session.query(Usuario).filter(func.lower(Usuario.email) == email).first()
    if usuario is None or not usuario.senha or not bcrypt_context.verify(dados.senha, usuario.senha):
        raise HTTPException(status_code=401, detail="Email ou senha invalidos")

    return {
        "access_token": criar_token(usuario.id),
        "token_type": "bearer",
        "usuario": serializar_usuario(usuario),
    }


@auth_router.get("/me")
async def obter_conta(usuario: Usuario = Depends(usuario_autenticado)):
    return serializar_usuario(usuario)


@auth_router.put("/me")
async def atualizar_conta(
    dados: AtualizacaoUsuario,
    usuario: Usuario = Depends(usuario_autenticado),
    session: Session = Depends(pegar_sessao),
):
    email = normalizar_email(dados.email)
    outro_usuario = session.query(Usuario).filter(
        func.lower(Usuario.email) == email,
        Usuario.id != usuario.id,
    ).first()
    if outro_usuario:
        raise HTTPException(status_code=409, detail="Este email ja esta cadastrado")

    nome = dados.nome.strip()
    if len(nome) < 2:
        raise HTTPException(status_code=422, detail="O nome deve ter pelo menos 2 caracteres")
    usuario.nome = nome
    usuario.email = email
    usuario.telefone = dados.telefone
    usuario.endereco = dados.endereco
    session.commit()
    session.refresh(usuario)
    return serializar_usuario(usuario)


@auth_router.post("/alterar_senha")
async def alterar_senha(
    dados: AlteracaoSenha,
    usuario: Usuario = Depends(usuario_autenticado),
    session: Session = Depends(pegar_sessao),
):
    validar_senha(dados.nova_senha)
    if not bcrypt_context.verify(dados.senha_atual, usuario.senha):
        raise HTTPException(status_code=400, detail="Senha atual incorreta")

    usuario.senha = bcrypt_context.hash(dados.nova_senha)
    session.commit()
    return {"mensagem": "Senha alterada com sucesso"}


@auth_router.delete("/me", status_code=204)
async def excluir_conta(
    usuario: Usuario = Depends(usuario_autenticado),
    session: Session = Depends(pegar_sessao),
):
    session.delete(usuario)
    session.commit()
