"""Testes triviais que já acompanham o repositório.

Servem para confirmar que o ambiente está de pé. Use-os como ponto de partida se quiser
escrever os seus — mas não é obrigatório escrever testes neste exercício.
"""

from datetime import datetime, timezone
from decimal import Decimal

from locacao.calendario import FUSO_BRASIL, data_local, eh_dia_util
from locacao.modelos import Contrato, Devolucao, PLANO_STANDARD


def test_contrato_pode_ser_construido():
    contrato = Contrato(
        id="CT-1",
        cliente_id="CLI-1",
        plano=PLANO_STANDARD,
        valor_diaria=Decimal("100.00"),
        dias_contratados=5,
        devolucao_prevista=datetime(2026, 3, 10, 14, 0, tzinfo=timezone.utc),
        ocorrencias_anteriores=0,
    )
    devolucao = Devolucao(contrato_id="CT-1", devolvido_em=datetime(2026, 3, 10, 14, 0, tzinfo=timezone.utc))

    assert contrato.valor_diaria == Decimal("100.00")
    assert devolucao.contrato_id == contrato.id


def test_calendario_converte_para_horario_local():
    # 03:00 UTC é 00:00 no Brasil (UTC-3), ainda no dia anterior em relação a 02:00 UTC.
    instante = datetime(2026, 3, 10, 3, 0, tzinfo=timezone.utc)

    assert instante.astimezone(FUSO_BRASIL).hour == 0
    assert data_local(instante).isoformat() == "2026-03-10"
    assert eh_dia_util(data_local(instante)) is True
