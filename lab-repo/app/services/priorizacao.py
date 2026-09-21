# -*- coding: utf-8 -*-
# calculo de prioridade - migrado do sistema antigo em 2019
# TODO revisar com o pessoal da manutencao - jsilva
# obs: nao mexer sem falar com o Marcelo (planejamento)

from datetime import datetime, timezone

from ..models import StatusOrdem

FATORES = {"A": 1, "B": 3, "C": 5}


def calc(o, eq, ref=None):
    if ref is None:
        ref = datetime.now(timezone.utc)

    p = FATORES.get(eq.criticidade.value, 5)

    # corretiva sobe
    if o.tipo.value == "corretiva":
        p = p - 1
    elif o.tipo.value == "preditiva":
        p = p + 1

    d = (ref - o.aberta_em).days
    if d > 30:
        p = p - 2
    elif d > 7:
        p = p - 1

    if o.reaberturas > 0:
        p = p - o.reaberturas

    # equipamento com muita hora de operacao tem desgaste
    if eq.horas_operacao > 15000:
        p = p - 1

    if o.status == StatusOrdem.AGUARDANDO_PECA:
        p = p + 2

    if p < 1:
        p = 1
    if p > 5:
        p = 5
    return p


def ordenar(ordens, equipamentos, ref=None):
    def k(o):
        eq = equipamentos.get(o.equipamento_id)
        if eq is None:
            return (99, o.aberta_em)
        return (calc(o, eq, ref), o.aberta_em)

    return sorted(ordens, key=k)
