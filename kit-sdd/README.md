# Kit SDD

Entregável 2 e 4 da proposta: templates de `constitution.md`, spec, plano e tasks, mais
`AGENTS.md`, perfis de configuração e a matriz de calibragem.

---

## Conteúdo

| Arquivo | Quando se usa | Quem escreve |
|---|---|---|
| `templates/constitution.md` | Uma vez por repositório, revisada raramente | O time, em acordo |
| `templates/spec.md` | Uma por fatia vertical entregável | Quem conduz a fatia |
| `templates/plan.md` | Uma por spec de rito completo ou reduzido | Quem conduz, com o agente |
| `templates/tasks.md` | Uma por plan | `$speckit-tasks`, revisado por humano |
| `templates/AGENTS.md` | Um por repositório, mais os de subdiretório — inclui as regras de harness e a seção "Sessão" | Quem conhece o repositório |
| `templates/config.toml` | Uma vez por pessoa, em `~/.codex/` | Cada participante |
| `matriz-de-calibragem.md` | Consulta permanente | — |

---

## Como usar com o Spec Kit

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

cd <seu-repo>
specify init --here --integration codex --integration-options="--skills"
```

No Codex CLI os comandos usam prefixo `$` (skills mode), **não** barra:

```
$speckit-constitution   $speckit-specify   $speckit-clarify
$speckit-plan           $speckit-tasks     $speckit-implement
$speckit-analyze        $speckit-checklist $speckit-converge
```

Em Copilot e Claude Code os mesmos comandos aparecem como `/speckit.specify`. Tutorial com
barra não é erro: é outro agente. Mesma ferramenta, mesma spec, invocação diferente — e é
exatamente esse o argumento a favor de um toolkit agnóstico.

---

## Onde os artefatos vivem

```
<repo>/
├── constitution.md              (ou .specify/memory/constitution.md)
├── AGENTS.md
├── specs/
│   └── 001-nome-da-fatia/
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md
└── app/
    └── ...
```

**Versionados junto ao código, no mesmo commit e no mesmo PR.** Não em wiki, não em drive.

Esta é a resposta prática à crítica de Birgitta Böckeler sobre o volume de artefatos: o
problema nunca foi a quantidade, foi **onde eles moravam**. Artefato em wiki apodrece porque
nada o obriga a acompanhar o código. Artefato no repositório, coberto por teste, é mantido
pelo mesmo mecanismo que mantém o código — porque quebra junto com ele.

---

## A relação entre os artefatos

```
constitution.md    princípios inegociáveis    muda em reunião
       ↓
    spec.md        o quê e por quê            uma por fatia
       ↓
    plan.md        como, tecnicamente         uma por spec
       ↓
   tasks.md        em que ordem, testes antes uma por plan
       ↓
     código
```

`AGENTS.md` é ortogonal: instrui o agente sobre **o repositório**, não sobre a fatia. Ele
responde "como se trabalha aqui"; a spec responde "o que fazer agora".

No vocabulário de harness (`runbook.md`, Parte XI), todos estes artefatos são **guias**: atuam
antes de o agente agir. Os checkpoints do `tasks.md` e o DoD são onde os **sensores** entram —
e os templates marcam esses pontos explicitamente.

---

## Os seis erros que os templates tentam evitar

1. **Tecnologia na spec.** Faz o `plan` virar cópia da spec, e você perdeu a etapa que
   protege a escolha técnica. Os templates separam isso de forma explícita.
2. **Princípio não verificável na constitution.** "Código de qualidade" não é princípio, é
   desejo. O template abre com essa regra e fecha com a lista do que **não** vai ali.
3. **`AGENTS.md` que repete o README.** Públicos diferentes: o README apresenta o projeto a
   quem vai contribuir; o `AGENTS.md` instrui quem já vai contribuir.
4. **Implementação antes do teste vermelho.** O template de tasks separa os blocos e coloca
   o checkpoint entre eles, com a observação de que teste que falha por `ImportError` não é
   teste vermelho — é teste quebrado.
5. **"Pronto" sem evidência.** O `tasks.md` pede a saída do comando em cada checkpoint, e o
   `AGENTS.md` instrui o agente a colá-la — contra a vitória prematura.
6. **Estado só na conversa.** A seção "Sessão" do `AGENTS.md` e o `tasks.md` atualizado são o
   que a próxima sessão lê — contra a amnésia entre sessões.

---

## Adaptação ao stack do cliente

Os templates estão preenchidos com o stack de referência do treinamento — **Python 3.11+,
FastAPI, pytest**. Os pontos a trocar estão marcados com `<...>`.

Na reunião de alinhamento, confirmar e ajustar:

- [ ] Linguagem, framework e gerenciador de pacotes.
- [ ] Convenção de nomes e estrutura de diretórios.
- [ ] Padrão de tratamento de erro na borda.
- [ ] Ferramenta de lint, formatação e tipos.
- [ ] Diretórios sensíveis que exigem revisão nominal.
- [ ] Política de dependências vigente na organização.
