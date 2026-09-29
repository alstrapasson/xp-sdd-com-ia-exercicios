"""Cálculo de multa por devolução atrasada."""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP

from .calendario import para_horario_local
from .modelos import Contrato, Devolucao, PLANO_PREMIUM

PERCENTUAL_MULTA_DIARIA = Decimal("0.15")
TAXA_FIXA_PRIMEIRO_ATRASO = Decimal("50.00")
TETO_MULTA = Decimal("500.00")
TOLERANCIA_STANDARD = timedelta(minutes=30)
TOLERANCIA_PREMIUM = timedelta(hours=2)
DESCONTO_PREMIUM = Decimal("0.50")
UM_DIA = timedelta(days=1)
CENTAVOS = Decimal("0.01")


def calcular_multa(contrato: Contrato, devolucao: Devolucao) -> Decimal:
    """Calcula a multa devida pela devolução atrasada de um equipamento.

    Args:
        contrato: Contrato de locação correspondente.
        devolucao: Evento de devolução registrado pelo pátio.

    Returns:
        O valor da multa em BRL, com duas casas decimais. Zero quando não há multa devida.
    """
    prevista = para_horario_local(contrato.devolucao_prevista)
    devolvida = para_horario_local(devolucao.devolvido_em)

    atraso = devolvida - prevista
    if atraso <= timedelta(0):
        return Decimal("0.00")

    tolerancia = TOLERANCIA_PREMIUM if contrato.plano == PLANO_PREMIUM else TOLERANCIA_STANDARD
    if atraso <= tolerancia:
        return Decimal("0.00")

    dias_atraso = _dias_cobraveis(atraso)
    multa = contrato.valor_diaria * PERCENTUAL_MULTA_DIARIA * Decimal(dias_atraso)

    if contrato.plano == PLANO_PREMIUM:
        multa *= DESCONTO_PREMIUM
    elif contrato.ocorrencias_anteriores == 0:
        multa += TAXA_FIXA_PRIMEIRO_ATRASO

    return min(multa, TETO_MULTA).quantize(CENTAVOS, rounding=ROUND_HALF_UP)


def _dias_cobraveis(atraso: timedelta) -> int:
    """Conta qualquer fração de dia em atraso como um dia cobravel."""
    dias_completos = atraso // UM_DIA
    return int(dias_completos) + (1 if atraso % UM_DIA else 0)
