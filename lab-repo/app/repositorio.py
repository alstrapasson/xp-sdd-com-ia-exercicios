"""Repositório em memória.

Suficiente para os laboratórios: o foco do treinamento é método, não persistência.
Substituir por banco real é exercício explicitamente fora de escopo.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from itertools import count

from .models import Criticidade, Equipamento, OrdemServico, StatusOrdem, TipoOrdem

_seq_ordem = count(1)


class Repositorio:
    def __init__(self) -> None:
        self.equipamentos: dict[str, Equipamento] = {}
        self.ordens: dict[str, OrdemServico] = {}

    # -- equipamentos ------------------------------------------------------------------

    def adicionar_equipamento(self, equipamento: Equipamento) -> Equipamento:
        self.equipamentos[equipamento.id] = equipamento
        return equipamento

    def buscar_equipamento(self, equipamento_id: str) -> Equipamento | None:
        return self.equipamentos.get(equipamento_id)

    def listar_equipamentos(self) -> list[Equipamento]:
        return list(self.equipamentos.values())

    # -- ordens ------------------------------------------------------------------------

    def proximo_id_ordem(self) -> str:
        return f"OS-{next(_seq_ordem):05d}"

    def adicionar_ordem(self, ordem: OrdemServico) -> OrdemServico:
        self.ordens[ordem.id] = ordem
        return ordem

    def buscar_ordem(self, ordem_id: str) -> OrdemServico | None:
        return self.ordens.get(ordem_id)

    def listar_ordens(
        self, *, status: StatusOrdem | None = None, equipamento_id: str | None = None
    ) -> list[OrdemServico]:
        resultado = list(self.ordens.values())
        if status is not None:
            resultado = [o for o in resultado if o.status == status]
        if equipamento_id is not None:
            resultado = [o for o in resultado if o.equipamento_id == equipamento_id]
        return resultado


repositorio = Repositorio()


def carregar_dados_iniciais() -> None:
    """Popula o repositório com dados de laboratório. Idempotente."""
    if repositorio.equipamentos:
        return

    agora = datetime.now(timezone.utc)

    for eq in [
        Equipamento(id="EQ-1", tag="BC-201", setor="Linha 1", criticidade=Criticidade.A,
                    horas_operacao=18_400),
        Equipamento(id="EQ-2", tag="CP-110", setor="Utilidades", criticidade=Criticidade.B,
                    horas_operacao=9_120),
        Equipamento(id="EQ-3", tag="ES-045", setor="Expedição", criticidade=Criticidade.C,
                    horas_operacao=2_300),
    ]:
        repositorio.adicionar_equipamento(eq)

    for equipamento_id, tipo, descricao, dias_atras, status in [
        ("EQ-1", TipoOrdem.CORRETIVA, "Vazamento no selo mecânico da bomba", 2,
         StatusOrdem.EM_EXECUCAO),
        ("EQ-2", TipoOrdem.PREVENTIVA, "Troca de filtro conforme plano de 2000h", 10,
         StatusOrdem.ABERTA),
        ("EQ-3", TipoOrdem.CORRETIVA, "Esteira desalinhada, produto caindo na transferência",
         1, StatusOrdem.AGUARDANDO_PECA),
    ]:
        ordem = OrdemServico(
            id=repositorio.proximo_id_ordem(),
            equipamento_id=equipamento_id,
            tipo=tipo,
            descricao=descricao,
            aberta_em=agora - timedelta(days=dias_atras),
            status=status,
        )
        repositorio.adicionar_ordem(ordem)
