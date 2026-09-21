"""Utilitários de calendário compartilhados pelo módulo de locação.

Este arquivo já existe no sistema e é usado por relatórios e faturamento.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

# A operação é toda no Brasil. O horário de verão foi extinto em 2019, portanto o
# deslocamento é fixo e não depende de base de fusos instalada no sistema operacional.
FUSO_BRASIL = timezone(timedelta(hours=-3), name="America/Sao_Paulo")

# Feriados nacionais usados pelo fechamento de faturamento.
FERIADOS_NACIONAIS: frozenset[date] = frozenset(
    {
        date(2026, 1, 1),    # Confraternização Universal
        date(2026, 2, 16),   # Carnaval
        date(2026, 2, 17),   # Carnaval
        date(2026, 4, 3),    # Sexta-feira Santa
        date(2026, 4, 21),   # Tiradentes
        date(2026, 5, 1),    # Dia do Trabalho
        date(2026, 6, 4),    # Corpus Christi
        date(2026, 9, 7),    # Independência
        date(2026, 10, 12),  # Nossa Senhora Aparecida
        date(2026, 11, 2),   # Finados
        date(2026, 11, 15),  # Proclamação da República
        date(2026, 11, 20),  # Consciência Negra
        date(2026, 12, 25),  # Natal
    }
)


def para_horario_local(instante: datetime) -> datetime:
    """Converte um instante timezone-aware para o fuso da operação."""
    if instante.tzinfo is None:
        raise ValueError("instante deve ser timezone-aware")
    return instante.astimezone(FUSO_BRASIL)


def data_local(instante: datetime) -> date:
    """Retorna a data de calendário do instante, no fuso da operação."""
    return para_horario_local(instante).date()


def eh_dia_util(dia: date) -> bool:
    """True se `dia` for dia útil: não é fim de semana nem feriado nacional."""
    return dia.weekday() < 5 and dia not in FERIADOS_NACIONAIS


def dias_uteis_entre(inicio: date, fim: date) -> int:
    """Conta dias úteis no intervalo (inicio, fim], usado pelo fechamento de faturamento."""
    if fim <= inicio:
        return 0
    total = 0
    cursor = inicio + timedelta(days=1)
    while cursor <= fim:
        if eh_dia_util(cursor):
            total += 1
        cursor += timedelta(days=1)
    return total
