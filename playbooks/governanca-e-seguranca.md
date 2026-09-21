# Playbook de Governança e Segurança — Desenvolvimento Assistido por IA

**Entregável 5 da proposta.** Documento destinado à aprovação interna de segurança e jurídico.

| | |
|---|---|
| **Organização** | Actionsys |
| **Elaborado por** | Strapa Tecnologia — André Luiz Strapasson |
| **Versão** | 1.0 — modelo para adaptação |
| **Status** | Minuta para revisão interna |

> **Este documento é um modelo.** Os campos entre `<...>` precisam ser preenchidos pela
> Actionsys, e as políticas precisam ser confrontadas com as normas internas de segurança da
> informação, proteção de dados e propriedade intelectual já vigentes. Nenhuma seção aqui
> substitui parecer jurídico.

---

## 1. Escopo

Aplica-se ao uso de agentes de codificação assistida por IA — Codex CLI, extensões de IDE e
integrações MCP — por profissionais de engenharia da Actionsys, em repositórios da
organização.

**Não cobre:** uso de IA generativa para texto, imagem ou atendimento; ferramentas de IA
embarcadas em produtos de terceiros; uso pessoal fora do ambiente corporativo.

---

## 2. Princípios

1. **A responsabilidade não é delegável.** O agente propõe; a pessoa responde. Toda linha
   integrada é de autoria e responsabilidade de quem abriu o PR.
2. **Todo conteúdo externo é entrada não confiável.** Issue, comentário, dependência,
   resposta de servidor MCP e página web são dados — nunca instruções.
3. **Delega-se o que se sabe verificar.** Sem critério de verificação, não há delegação: há
   aposta.
4. **Verificação determinística precede revisão humana.** O que a máquina consegue conferir
   sai da carga cognitiva da pessoa.
5. **Configuração de agente é código.** Versionada, revisada e testada como código.
6. **Quem gera não aprova.** A avaliação de uma mudança acontece fora da sessão que a
   produziu, e as verificações obrigatórias rodam no CI — fora do alcance do agente.
7. **"Pronto" é evidência, não afirmação.** Conclusão declarada pelo agente não substitui a
   saída das verificações.

---

## 3. Classificação de repositórios

A política de uso varia conforme a sensibilidade. Classificar antes de liberar.

| Classe | Descrição | Sandbox máximo | Aprovação mínima | Agente autônomo |
|---|---|---|---|:-:|
| **A — Crítico** | Dado pessoal, financeiro, credencial, código sob NDA | `workspace-write` | `untrusted` | Não |
| **B — Interno** | Sistemas internos sem dado pessoal | `workspace-write` | `on-request` | Com supervisão |
| **C — Baixo risco** | Ferramental interno, protótipo, documentação | `workspace-write` | `on-request` | Sim |

`danger-full-access` **não é autorizado em nenhuma classe** com credencial válida presente no
ambiente. Exceções exigem aprovação nominal de `<responsável>` e registro com prazo de validade.

**Classificação vigente:** `<a Actionsys preenche a lista de repositórios por classe>`

---

## 4. Tratamento de dados e propriedade intelectual

### 4.1 O que nunca entra em contexto de agente

- Segredos, credenciais, tokens, chaves privadas, arquivos `.env`.
- Dado pessoal de cliente, colaborador ou terceiro, identificável ou pseudonimizado.
- Dado sujeito a sigilo contratual, NDA ou regulatório.
- Base de dados de produção, dump ou amostra não anonimizada.

> A regra vale inclusive para "só para o agente entender a estrutura". Não existe essa exceção.
> Para estrutura, use schema sem dados ou dados sintéticos.

### 4.2 Retenção e treinamento

`<A Actionsys precisa preencher, com base no contrato vigente com o fornecedor do modelo:>`

- Plano contratado e política de retenção aplicável: `<...>`
- O conteúdo enviado é usado para treinamento? `<sim/não — citar cláusula>`
- Prazo de retenção de prompts e respostas: `<...>`
- Região de processamento e implicações para a LGPD: `<...>`

> **Esta seção é a que o jurídico vai ler primeiro.** Ela não pode ser preenchida pelo
> fornecedor do treinamento — depende do contrato entre a Actionsys e o fornecedor do modelo.

### 4.3 Propriedade do código gerado

- Código gerado com assistência é tratado como obra da Actionsys, nos mesmos termos do código
  escrito diretamente. `<confirmar com o jurídico>`
- Trecho reconhecidamente derivado de fonte licenciada deve ser identificado e ter a licença
  respeitada. Quando houver dúvida sobre origem, **não integrar**.
- Dependência introduzida por agente segue a política de licenças vigente da organização.

### 4.4 Registro

- Specs, planos e tasks versionados junto ao código constituem o registro da intenção.
- PRs identificam quando houve assistência de IA. `<definir: label, campo no template, ou nada>`

---

## 5. As quatro superfícies de risco

### 5.1 Prompt injection por conteúdo não confiável

**O risco.** O agente não distingue "conteúdo que devo processar" de "instrução que devo
seguir". Texto malicioso em uma issue, em um comentário de PR, na docstring de uma dependência
ou na resposta de um servidor MCP pode redirecionar o comportamento do agente — inclusive para
ler credenciais e incluí-las em um PR.

**Onde entra conteúdo não confiável**

| Vetor | Quem controla |
|---|---|
| Issues e comentários de PR | Qualquer pessoa com acesso ao tracker |
| README e docstring de dependência, inclusive transitiva | O mantenedor do pacote |
| Resposta de servidor MCP de terceiro | O operador do servidor |
| Página web buscada pelo agente | Qualquer um |
| Código em PR de fork | Contribuidor externo |

**Controles**

| Camada | Controle | Responsável |
|---|---|---|
| Sandbox | Sessão que consome conteúdo externo roda `read-only` (perfil `triagem`) | Desenvolvedor |
| Rede | Egresso restrito. Agente que não alcança a internet não exfiltra por HTTP | `<Infra>` |
| Credencial | Escopo mínimo, curta duração, separada da credencial pessoal | `<Segurança>` |
| Revisão | Diff lido integralmente, com atenção ao que não estava no escopo | Revisor do PR |

**Pergunta obrigatória na revisão:** *o que mudou aqui que ninguém pediu?*

### 5.2 Supply chain de skills e servidores MCP

**O risco.** Instalar um skill de terceiro é executar instruções de um estranho no seu
repositório, com as suas credenciais. Um servidor MCP de terceiro é mais grave: é **código
executando na sua máquina**.

Skills e servidores MCP são **dependências** e devem seguir a política de dependências da
organização — com a agravante de que o efeito recai sobre o comportamento do agente, não sobre
uma função isolada.

**Critérios de adoção — obrigatórios**

- [ ] Origem identificável e mantenedor conhecido.
- [ ] `SKILL.md` lido integralmente, incluindo todo `scripts/`.
- [ ] Nenhuma execução de rede sem justificativa explícita.
- [ ] Fixado em versão ou commit. **Nunca `latest`.**
- [ ] Revisão por segundo par de olhos antes de entrar em repositório da organização.
- [ ] Reavaliação a cada atualização — confiança prévia não se herda.

**Curadoria.** `<Definir: quem mantém o repositório central de skills aprovados, com que
periodicidade é revisado, e como um skill é removido.>` O módulo opcional de Escala e
Multiplicação cobre a operação desse repositório central.

### 5.3 Segredos e exfiltração

| Controle | Detalhe |
|---|---|
| Segredo fora do contexto | `.env` e credenciais nunca lidos pelo agente |
| Varredura pré-commit | Hook que bloqueia segredo no diff |
| Credencial dedicada | Identidade própria para agente, escopo mínimo, revogável sem quebrar o desenvolvedor |
| Isolamento de rede | O controle mais eficaz e o menos usado |
| Rotação | `<periodicidade>` |

**Se houver suspeita de vazamento:** rotacionar a credencial imediatamente, **antes** de
investigar. Acionar `<canal de resposta a incidentes>`.

### 5.4 Dependências introduzidas pelo agente

**O risco.** O agente resolve problemas adicionando bibliotecas. É solução legítima, e é onde
entram typosquatting, pacote abandonado e transitiva com licença incompatível.

**Controles**

- Princípio na constitution: dependência nova exige justificativa no PR — por que não dá com
  o que já existe.
- Revisão humana obrigatória: nome, mantenedor, última publicação, licença, tamanho da árvore
  transitiva.
- Auditoria automatizada no CI: `<ferramenta>`.
- Lockfile versionado e conferido no diff.

---

## 6. Definition of Done para código assistido

Aplica-se a **toda** mudança, em qualquer nível de rito.

- [ ] Todo critério de aceite tem teste correspondente, e ele já esteve vermelho.
- [ ] Suíte verde; cobertura de regra de negócio não caiu.
- [ ] Diff lido integralmente por um humano.
- [ ] Nada no diff fora do escopo da spec.
- [ ] Dependência nova justificada no PR, ou nenhuma.
- [ ] Spec, plano e tasks versionados no mesmo PR.
- [ ] Verificações determinísticas passaram (lint, tipos, hooks, varredura de segredo) — **no
      CI**, não apenas na sessão do agente.
- [ ] Nenhum teste existente alterado ou silenciado para passar sem justificativa no PR.
- [ ] Se tocou legado: caracterização estava verde antes e continua verde.

> **Sobre "diff lido integralmente".** É inviável em PR de 800 linhas gerado em vinte minutos.
> Ou os PRs ficam menores, ou a revisão é teatro. Esta é a razão pela qual "uma spec por fatia
> vertical" é regra de engenharia, não preferência de estilo.

---

## 7. O que nunca se delega

| Nunca | Por quê |
|---|---|
| Decidir qual é o critério de aceite | É a intenção do negócio |
| Aprovar o próprio diff | Não há revisão sem separação — vale também para o agente revisando a própria sessão |
| Julgar se o comportamento capturado em legado está correto | Exige conhecimento de negócio |
| Decisão arquitetural irreversível | Custo de erro assimétrico |
| A leitura final antes do merge | É onde a responsabilidade se materializa |
| Aplicar migração de dados em produção | Irreversível |
| Aceitar dependência nova sem revisão | Superfície de supply chain |

---

## 8. Papéis

| Papel | Responsabilidade |
|---|---|
| **Desenvolvedor** | Intenção, critérios, revisão do diff, aderência ao DoD |
| **Revisor de PR** | Leitura integral, verificação de escopo, conformidade com a constitution |
| **Mantenedor do repositório** | Constitution, `AGENTS.md`, curadoria dos skills do repositório |
| **`<Champion>`** | Repositório central de skills, evolução da prática, ritual de revisão |
| **`<Segurança>`** | Classificação de repositórios, escopo de credenciais, resposta a incidentes |
| **`<Jurídico>`** | Retenção, treinamento, propriedade intelectual, licenças |

---

## 9. Incidentes

Comunicar a `<canal>` imediatamente ao identificar:

- Credencial exposta em contexto, log, PR ou resposta de agente.
- Comportamento de agente divergente do instruído, com suspeita de injeção.
- Dependência maliciosa ou skill de terceiro com comportamento inesperado.
- Dado pessoal ou sob sigilo enviado a serviço externo.

**Primeiro contenha, depois investigue.** Rotacionar credencial e revogar acesso tem
precedência sobre entender o que aconteceu.

---

## 10. Revisão desta política

| Item | Periodicidade | Responsável |
|---|---|---|
| Classificação de repositórios | `<semestral>` | `<Segurança>` |
| Repositório central de skills | `<mensal>` | `<Champion>` |
| Servidores MCP autorizados | `<trimestral>` | `<Segurança>` |
| Este documento | `<semestral>`, ou a cada mudança relevante de ferramenta | `<Engenharia>` |

---

## Anexo — Checklist de liberação de repositório

Antes de autorizar uso de agente em um repositório:

- [ ] Classe definida (A, B ou C) e registrada.
- [ ] `constitution.md` escrita e aprovada pelo time.
- [ ] `AGENTS.md` com seção "NÃO se aplica" preenchida.
- [ ] Perfis de `config.toml` compatíveis com a classe.
- [ ] Varredura de segredo ativa no pre-commit.
- [ ] Credencial de agente com escopo mínimo provisionada.
- [ ] Servidores MCP revisados e fixados em versão.
- [ ] Skills de terceiro revisados, ou nenhum instalado.
- [ ] DoD acordado com o time e visível.
- [ ] Responsável nomeado.
