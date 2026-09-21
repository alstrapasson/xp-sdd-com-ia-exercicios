# Etapa 1 — Instalação e verificação de ambiente

Tempo estimado: **20 minutos**. Se passar de 35, pare e chame o instrutor.

Ao final você terá: Python, Git, Codex CLI autenticado e um relatório JSON confirmando que
está tudo de pé.

---

## Antes de começar

**Escolha uma pasta de trabalho local**, fora de OneDrive, Dropbox ou Google Drive. Pastas
sincronizadas travam arquivos durante a execução dos testes e geram erros difíceis de
diagnosticar. Sugestão: `C:\projects\treinamento` (Windows) ou `~/projects/treinamento`
(macOS/Linux). O verificador avisa se detectar pasta sincronizada.

---

## 1. Python 3.11 ou superior

Confira o que você já tem:

```bash
python --version     # Windows
python3 --version    # macOS / Linux
```

Se for menor que 3.11 ou o comando não existir:

- **Windows** — baixe em [python.org/downloads](https://www.python.org/downloads/) e
  **marque "Add python.exe to PATH"** na primeira tela do instalador. É o passo que a maioria
  esquece e que causa a maior parte dos problemas depois.
- **macOS** — `brew install python@3.12`
- **Linux (Debian/Ubuntu)** — `sudo apt install python3.12 python3.12-venv`

Depois instale o `pytest`:

```bash
python -m pip install pytest
```

> **Windows:** se `python` abrir a Microsoft Store em vez de rodar, use `py` no lugar de
> `python`, ou desative os "App execution aliases" do Python em Configurações.

---

## 2. Git

```bash
git --version
```

Se não existir, instale de [git-scm.com/downloads](https://git-scm.com/downloads).

Configure sua identidade — sem isso, os commits dos laboratórios não são atribuíveis:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "voce@actionsys.com.br"
```

---

## 3. Node.js 20+ (só para instalar o Codex CLI)

```bash
node --version
```

Se não tiver, instale a versão **LTS** de [nodejs.org](https://nodejs.org/). O Node não é
usado no treinamento — serve apenas como veículo de instalação do Codex.

---

## 4. Codex CLI

```bash
npm install -g @openai/codex
codex --version
```

Se o `npm install -g` falhar por permissão:

- **Windows** — abra o PowerShell como Administrador e repita.
- **macOS / Linux** — evite `sudo npm`. Configure um prefixo de usuário:
  ```bash
  mkdir -p ~/.npm-global
  npm config set prefix ~/.npm-global
  echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.profile
  source ~/.profile
  ```

---

## 5. Autenticação — o passo crítico

```bash
codex login
```

Isso abre o navegador para você entrar com a **conta corporativa** provisionada pela
Actionsys. Conclua o fluxo e volte ao terminal.

> ### Se você não tem acesso ainda
>
> **Avise o instrutor hoje, não na véspera.** Provisionamento de licença corporativa costuma
> levar mais de uma semana, e este é de longe o bloqueio mais comum deste pré-work.
>
> Você ainda pode fazer as etapas 2 e 3 (leitura e kata) sem o Codex — o kata pode ser feito
> com a ferramenta de IA que você já usa hoje. O que não pode é chegar no Dia 1 sem acesso.

Confirme que funcionou:

```bash
codex
```

Deve abrir a interface interativa. Saia com `/quit` ou `Ctrl+D`.

---

## 6. uv (para o Spec Kit)

O Spec Kit será usado a partir do Dia 4, mas o instalador do `uv` é rápido e evita retrabalho:

```powershell
# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex
```

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Instalar o `specify` agora é **opcional** — faremos isso juntos no Dia 4. Se quiser adiantar:

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

---

## 7. Verificação final

```powershell
# Windows
cd scripts
.\verificar-ambiente.ps1
```

```bash
# macOS / Linux
cd scripts
chmod +x verificar-ambiente.sh
./verificar-ambiente.sh
```

O script roda 12 verificações e classifica cada uma:

| Marca | Significado |
|---|---|
| `OK` | Nada a fazer |
| `ATENCAO` | Não impede o Dia 1; resolva quando puder |
| `FALHA` | **Bloqueia.** Cada falha vem com a instrução exata de correção |

Ele grava `verificacao-ambiente-<usuario>-<data>.json` na pasta atual. **Esse arquivo faz
parte da entrega.**

---

## Problemas conhecidos

| Sintoma | Causa provável | Solução |
|---|---|---|
| `codex: command not found` logo após instalar | O PATH da sessão está desatualizado | Feche e reabra o terminal |
| `verificar-ambiente.ps1 não pode ser carregado` | Política de execução do PowerShell | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` e rode de novo |
| Falha em "Conectividade de rede" | Proxy ou firewall corporativo | Peça liberação de `api.openai.com` e `github.com` (porta 443) e **avise o instrutor** |
| `python` abre a Microsoft Store | Alias de execução do Windows | Use `py` ou desative o alias em Configurações |
| Acentos aparecem corrompidos no terminal | Code page legada do console | Cosmético apenas; não afeta o resultado nem o JSON |
| pytest "não encontra" o pacote `locacao` | Executado da pasta errada | Rode `python -m pytest` **de dentro** da pasta do kata |

Qualquer coisa fora desta lista: mande o print e o JSON do verificador para o instrutor.
