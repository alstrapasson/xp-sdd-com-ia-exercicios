"""API de manutenção — repositório de laboratório do treinamento."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .repositorio import carregar_dados_iniciais
from .routers import equipamentos, ordens


@asynccontextmanager
async def lifespan(app: FastAPI):
    carregar_dados_iniciais()
    yield


app = FastAPI(
    title="API de Manutenção",
    description="Repositório de laboratório — Capacitação XP + SDD com IA (Codex)",
    version="0.3.0",
    lifespan=lifespan,
)

app.include_router(equipamentos.router)
app.include_router(ordens.router)


@app.get("/saude", tags=["infra"])
def saude() -> dict[str, str]:
    return {"status": "ok"}
