# Capacitação XP + SDD com IA (Codex) — exercícios e katas

Material de trabalho dos participantes: o repositório de exercício que atravessa os cinco
dias, os katas cronometrados, os cinco laboratórios, os templates do método e os playbooks
de referência.

Tudo aqui é para ser **executado**, não lido. Se você está começando, vá para
[`ambiente/`](ambiente/) e confirme que sua máquina está de pé antes da primeira aula.

---

## O que tem aqui

| Pasta | O que é | Quando se usa |
|---|---|---|
| [`ambiente/`](ambiente/) | Instalação e script de verificação | Antes do Dia 1 |
| [`kata-a/`](kata-a/) | Kata baseline — multa por devolução atrasada | Dia 1, cronometrado |
| [`lab-repo/`](lab-repo/) | API FastAPI que atravessa os cinco dias | Dias 1 a 5 |
| [`laboratorios/`](laboratorios/) | Os cinco roteiros de laboratório | Um por dia |
| [`kit-sdd/`](kit-sdd/) | Templates: constitution, spec, plan, tasks, `AGENTS.md`, `config.toml` | A partir do Dia 2 |
| [`playbooks/`](playbooks/) | Boas práticas, protocolo brownfield, governança e segurança | Referência contínua |

**Ainda vai chegar aqui:** os skills de exemplo, com seus evals, no Dia 3. O kata final, no
Dia 5. Dê `git pull` no começo de cada aula.

---

## Começando

```bash
git clone https://github.com/alstrapasson/xp-sdd-com-ia-exercicios.git
cd xp-sdd-com-ia-exercicios
```

**Verifique o ambiente** — leva dois minutos e evita perder exercício por instalação:

```bash
python ambiente/verificar_ambiente.py        # ou verificar-ambiente.ps1 no Windows
```

**Confirme que o lab-repo roda:**

```bash
cd lab-repo
pip install -e ".[dev]"
pytest                                        # 12 testes devem passar
```

---

## Uma regra que vale para o kata

> **Não abra `kata-a/` antes da hora.** Ele é cronometrado e mede como você trabalha hoje,
> sem o método que o programa ainda vai ensinar. Ler o enunciado antes não te dá vantagem —
> só apaga o seu ponto de partida, que é a única coisa contra a qual a sua evolução vai ser
> medida no fim do programa.

A mesma lógica vale para os laboratórios: cada um tem seções recolhidas (`<details>`) com
sugestões do que costuma aparecer. Elas existem para você conferir **depois** de escrever a
sua própria lista, não em vez dela.

---

## Como pedir ajuda

- **Ambiente quebrado:** abra uma issue com a saída completa do verificador. Bloqueio de
  ambiente é problema do programa, não seu.
- **Dúvida sobre um exercício durante a aula:** chame o instrutor na hora. Durante o kata
  cronometrado, não — ali o silêncio faz parte da medição.
- **Dúvida depois da aula:** leve para a sessão de mentoria; é para isso que ela existe.

---

## Licença e uso

Material didático da capacitação XP + Spec-Driven Development com IA (Codex), produzido por
**Strapa Tecnologia**. Publicado para uso dos participantes do programa.

Nenhuma licença de uso é concedida além disso: todos os direitos reservados. Se você chegou
aqui de fora e quer usar algo, fale comigo antes.
