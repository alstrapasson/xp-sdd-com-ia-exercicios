#!/usr/bin/env python3
"""Environment verification for the XP + SDD with AI (Codex) training program.

Runs a series of independent checks and prints a human-readable report, then writes a
JSON report the participant sends back to the instructor.

Design constraints:
  - Python standard library only. The participant may not have installed anything yet.
  - No check may abort the run: every failure is caught and reported as a result.
  - Every failing check must carry a concrete remediation string. A red line the
    participant cannot act on is worse than no check at all.

Usage:
    python verificar_ambiente.py
    python verificar_ambiente.py --json-only
    python verificar_ambiente.py --output C:/tmp/relatorio.json
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import socket
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

# The Windows console defaults to a legacy code page, which mangles accented names read
# from git config. Reconfiguring here keeps the report legible without touching the shell.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

PROGRAM = "Capacitacao XP + SDD com IA (Codex) - Strapa Tecnologia"
MIN_PYTHON = (3, 11)
COMMAND_TIMEOUT = 20
NETWORK_TIMEOUT = 8

OK = "OK"
WARN = "ATENCAO"
FAIL = "FALHA"

# Windows terminals that do not understand ANSI leave escape codes visible in the
# report, which reads as a broken script to a participant who has not started yet.
USE_COLOR = sys.stdout.isatty() and (os.name != "nt" or os.environ.get("WT_SESSION"))
_COLORS = {OK: "\033[32m", WARN: "\033[33m", FAIL: "\033[31m"}


def paint(status: str) -> str:
    if not USE_COLOR:
        return status
    return f"{_COLORS.get(status, '')}{status}\033[0m"


@dataclass
class Result:
    name: str
    status: str
    detail: str
    remediation: str = ""
    data: dict = field(default_factory=dict)


def run(cmd: list[str]) -> tuple[int, str]:
    """Run a command, returning (exit_code, combined_output). Never raises."""
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError:
        return 127, "command not found"
    except subprocess.TimeoutExpired:
        return 124, f"timeout after {COMMAND_TIMEOUT}s"
    except OSError as exc:  # permission denied, exec format error, ...
        return 126, str(exc)
    return proc.returncode, ((proc.stdout or "") + (proc.stderr or "")).strip()


def first_version(text: str) -> str:
    match = re.search(r"\d+\.\d+(?:\.\d+)?", text)
    return match.group(0) if match else ""


# --------------------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------------------


def check_python() -> Result:
    current = sys.version_info[:3]
    detail = f"Python {'.'.join(map(str, current))} em {sys.executable}"
    if current[:2] < MIN_PYTHON:
        return Result(
            "Python >= 3.11",
            FAIL,
            detail,
            "Instale Python 3.11 ou superior em https://www.python.org/downloads/ e "
            "reabra o terminal. No Windows, marque 'Add python.exe to PATH'.",
            {"version": ".".join(map(str, current))},
        )
    return Result("Python >= 3.11", OK, detail, data={"version": ".".join(map(str, current))})


def check_git() -> Result:
    if not shutil.which("git"):
        return Result(
            "Git instalado",
            FAIL,
            "git nao encontrado no PATH",
            "Instale o Git em https://git-scm.com/downloads e reabra o terminal.",
        )
    code, out = run(["git", "--version"])
    if code != 0:
        return Result("Git instalado", FAIL, out, "Reinstale o Git; o binario esta no PATH mas nao executa.")
    return Result("Git instalado", OK, out.strip(), data={"version": first_version(out)})


def check_git_identity() -> Result:
    if not shutil.which("git"):
        return Result("Identidade Git configurada", FAIL, "git ausente", "Instale o Git primeiro.")
    _, name = run(["git", "config", "--get", "user.name"])
    _, email = run(["git", "config", "--get", "user.email"])
    name, email = name.strip(), email.strip()
    if not name or not email:
        return Result(
            "Identidade Git configurada",
            FAIL,
            f"user.name={name or '(vazio)'} user.email={email or '(vazio)'}",
            'Configure: git config --global user.name "Seu Nome" && '
            'git config --global user.email "voce@empresa.com". '
            "Sem isso os commits do laboratorio nao sao atribuiveis.",
        )
    return Result("Identidade Git configurada", OK, f"{name} <{email}>", data={"name": name, "email": email})


def check_codex_cli() -> Result:
    if not shutil.which("codex"):
        return Result(
            "Codex CLI instalado",
            FAIL,
            "codex nao encontrado no PATH",
            "Instale com: npm install -g @openai/codex  (requer Node.js 20+). "
            "Alternativa sem Node: consulte 01-instalacao-e-ambiente.md.",
        )
    code, out = run(["codex", "--version"])
    if code != 0:
        return Result(
            "Codex CLI instalado",
            FAIL,
            out,
            "O binario 'codex' esta no PATH mas nao executa. Reinstale: npm install -g @openai/codex",
        )
    return Result("Codex CLI instalado", OK, out.splitlines()[0] if out else "ok",
                  data={"version": first_version(out)})


def check_codex_auth() -> Result:
    """Authentication is the single most common Day 1 blocker, so it is checked two ways."""
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    auth_file = codex_home / "auth.json"
    api_key = os.environ.get("OPENAI_API_KEY", "")

    if auth_file.is_file() and auth_file.stat().st_size > 0:
        return Result(
            "Codex autenticado",
            OK,
            f"credencial encontrada em {auth_file}",
            data={"method": "auth.json", "path": str(auth_file)},
        )
    if api_key:
        return Result(
            "Codex autenticado",
            WARN,
            "OPENAI_API_KEY definida no ambiente, mas sem sessao interativa gravada",
            "Recomendado rodar 'codex login' para autenticar pela conta corporativa. "
            "Chave de API avulsa pode nao ter acesso aos modelos do programa.",
            {"method": "env"},
        )
    return Result(
        "Codex autenticado",
        FAIL,
        f"nenhuma credencial em {auth_file} nem OPENAI_API_KEY definida",
        "Rode 'codex login' e conclua o fluxo no navegador. Se a licenca corporativa ainda "
        "nao foi provisionada, avise o instrutor HOJE - este e o bloqueio mais comum.",
        {"method": "none"},
    )


def check_codex_config() -> Result:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    config = codex_home / "config.toml"
    if not config.is_file():
        return Result(
            "config.toml do Codex",
            WARN,
            f"{config} ainda nao existe",
            "Nao e bloqueante: o arquivo sera criado no laboratorio do Dia 2. "
            "Se preferir adiantar, crie o diretorio ~/.codex/.",
            {"path": str(config), "exists": False},
        )
    try:
        text = config.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return Result("config.toml do Codex", WARN, f"nao foi possivel ler: {exc}",
                      "Verifique as permissoes do arquivo.")
    profiles = re.findall(r"^\s*\[profiles\.([A-Za-z0-9_-]+)\]", text, re.MULTILINE)
    mcp = re.findall(r"^\s*\[mcp_servers\.([A-Za-z0-9_-]+)\]", text, re.MULTILINE)
    return Result(
        "config.toml do Codex",
        OK,
        f"{config} | perfis: {', '.join(profiles) or 'nenhum'} | MCP: {', '.join(mcp) or 'nenhum'}",
        data={"path": str(config), "exists": True, "profiles": profiles, "mcp_servers": mcp},
    )


def check_node() -> Result:
    if not shutil.which("node"):
        return Result(
            "Node.js (para instalar o Codex CLI)",
            WARN,
            "node nao encontrado",
            "So e necessario se voce instalar o Codex via npm. Se o 'codex' ja funciona, ignore.",
        )
    _, out = run(["node", "--version"])
    version = first_version(out)
    major = int(version.split(".")[0]) if version else 0
    if major and major < 20:
        return Result(
            "Node.js (para instalar o Codex CLI)",
            WARN,
            f"Node {version} - abaixo do recomendado",
            "Atualize para Node 20 LTS ou superior.",
            {"version": version},
        )
    return Result("Node.js (para instalar o Codex CLI)", OK, out.strip(), data={"version": version})


def check_uv_or_pipx() -> Result:
    """Spec Kit's `specify` CLI is distributed for uv/pipx; either one is enough."""
    found = [tool for tool in ("uv", "pipx") if shutil.which(tool)]
    if not found:
        return Result(
            "uv ou pipx (para o Spec Kit)",
            FAIL,
            "nem uv nem pipx encontrados",
            "Instale o uv: https://docs.astral.sh/uv/getting-started/installation/ "
            "(Windows PowerShell: irm https://astral.sh/uv/install.ps1 | iex). "
            "Alternativa: python -m pip install --user pipx",
        )
    return Result("uv ou pipx (para o Spec Kit)", OK, ", ".join(found), data={"tools": found})


def check_specify() -> Result:
    if not shutil.which("specify"):
        return Result(
            "Spec Kit (CLI specify)",
            WARN,
            "specify nao encontrado no PATH",
            "Nao e bloqueante para o Dia 1. Instale antes do Dia 4 com: "
            "uv tool install specify-cli --from git+https://github.com/github/spec-kit.git",
        )
    code, out = run(["specify", "--version"])
    detail = out.splitlines()[0] if out else "instalado"
    status = OK if code == 0 else WARN
    return Result("Spec Kit (CLI specify)", status, detail, data={"version": first_version(out)})


def check_pytest() -> Result:
    code, out = run([sys.executable, "-m", "pytest", "--version"])
    if code != 0:
        return Result(
            "pytest disponivel",
            FAIL,
            "pytest nao instalado para este Python",
            f"Instale com: {Path(sys.executable).name} -m pip install pytest. "
            "O kata baseline depende dele.",
        )
    return Result("pytest disponivel", OK, out.splitlines()[0], data={"version": first_version(out)})


def check_network() -> Result:
    """Corporate proxies and TLS interception are a recurring cause of silent failures."""
    hosts = [("api.openai.com", 443), ("github.com", 443)]
    unreachable: list[str] = []
    for host, port in hosts:
        try:
            with socket.create_connection((host, port), timeout=NETWORK_TIMEOUT):
                pass
        except OSError as exc:
            unreachable.append(f"{host}:{port} ({exc.__class__.__name__})")

    proxies = {
        var: os.environ[var]
        for var in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy")
        if os.environ.get(var)
    }
    if unreachable:
        return Result(
            "Conectividade de rede",
            FAIL,
            "sem acesso a: " + "; ".join(unreachable),
            "Provavel bloqueio de firewall ou proxy corporativo. Peca a liberacao de "
            "api.openai.com e github.com (443) ao time de infraestrutura e avise o instrutor.",
            {"unreachable": unreachable, "proxies": sorted(proxies)},
        )
    detail = "api.openai.com e github.com acessiveis"
    if proxies:
        detail += f" | proxy configurado: {', '.join(sorted(proxies))}"
    return Result("Conectividade de rede", OK, detail, data={"proxies": sorted(proxies)})


def check_workspace() -> Result:
    """A writable working directory outside OneDrive/synced folders avoids file-lock noise."""
    cwd = Path.cwd()
    probe = cwd / ".verificacao_ambiente_probe"
    try:
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
    except OSError as exc:
        return Result(
            "Diretorio de trabalho gravavel",
            FAIL,
            f"{cwd} nao e gravavel: {exc}",
            "Rode o script a partir de uma pasta com permissao de escrita, por exemplo C:/projects.",
        )
    synced = any(token in str(cwd).lower() for token in ("onedrive", "dropbox", "google drive"))
    if synced:
        return Result(
            "Diretorio de trabalho gravavel",
            WARN,
            f"{cwd} parece estar em pasta sincronizada na nuvem",
            "Mova o repositorio do kata para um caminho local (ex.: C:/projects). "
            "Sincronizacao gera bloqueio de arquivo durante os testes.",
            {"cwd": str(cwd), "synced": True},
        )
    return Result("Diretorio de trabalho gravavel", OK, str(cwd), data={"cwd": str(cwd)})


CHECKS: list[Callable[[], Result]] = [
    check_python,
    check_git,
    check_git_identity,
    check_node,
    check_codex_cli,
    check_codex_auth,
    check_codex_config,
    check_uv_or_pipx,
    check_specify,
    check_pytest,
    check_network,
    check_workspace,
]

# Only these block Day 1. The others degrade the experience but do not stop the class.
BLOCKING = {
    "Python >= 3.11",
    "Git instalado",
    "Identidade Git configurada",
    "Codex CLI instalado",
    "Codex autenticado",
    "pytest disponivel",
    "Conectividade de rede",
}


def collect() -> list[Result]:
    results: list[Result] = []
    for check in CHECKS:
        try:
            results.append(check())
        except Exception as exc:  # a broken check must never hide the other results
            results.append(
                Result(
                    check.__name__,
                    WARN,
                    f"verificacao falhou inesperadamente: {exc.__class__.__name__}: {exc}",
                    "Envie a saida completa ao instrutor.",
                )
            )
    return results


def report(results: list[Result]) -> None:
    width = max(len(r.name) for r in results) + 2
    print()
    print("=" * 78)
    print(PROGRAM)
    print("Verificacao de ambiente - pre-work")
    print("=" * 78)
    print(f"Host: {platform.node()} | SO: {platform.system()} {platform.release()}")
    print(f"Data: {datetime.now(timezone.utc).isoformat(timespec='seconds')} (UTC)")
    print("-" * 78)

    for r in results:
        print(f"[{paint(r.status):<9}] {r.name:<{width}} {r.detail}")

    blocking = [r for r in results if r.status == FAIL and r.name in BLOCKING]
    other = [r for r in results if r.remediation and r not in blocking and r.status != OK]

    if blocking:
        print("\n" + "-" * 78)
        print("BLOQUEIOS - resolva antes do Dia 1:")
        for r in blocking:
            print(f"\n  * {r.name}\n    {r.remediation}")
    if other:
        print("\n" + "-" * 78)
        print("Pendencias nao bloqueantes:")
        for r in other:
            print(f"\n  * {r.name}\n    {r.remediation}")

    print("\n" + "=" * 78)
    if blocking:
        print(f"RESULTADO: {len(blocking)} bloqueio(s). O ambiente NAO esta pronto.")
    else:
        warns = sum(1 for r in results if r.status == WARN)
        suffix = f" ({warns} atencao(oes) nao bloqueante(s))" if warns else ""
        print(f"RESULTADO: ambiente pronto para o Dia 1{suffix}.")
    print("=" * 78)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verifica o ambiente para o treinamento.")
    parser.add_argument("--output", help="Caminho do relatorio JSON.")
    parser.add_argument("--json-only", action="store_true", help="Imprime apenas o JSON.")
    args = parser.parse_args()

    results = collect()
    blocking = [r for r in results if r.status == FAIL and r.name in BLOCKING]

    payload = {
        "program": PROGRAM,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "host": platform.node(),
        "user": os.environ.get("USERNAME") or os.environ.get("USER") or "desconhecido",
        "os": f"{platform.system()} {platform.release()}",
        "python": platform.python_version(),
        "ready": not blocking,
        "blocking_failures": [r.name for r in blocking],
        "checks": [asdict(r) for r in results],
    }

    if args.json_only:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        report(results)

    default_name = f"verificacao-ambiente-{payload['user']}-{datetime.now().strftime('%Y%m%d')}.json"
    out_path = Path(args.output) if args.output else Path.cwd() / default_name
    try:
        out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        if not args.json_only:
            print(f"\nRelatorio salvo em: {out_path}")
            print("Envie este arquivo ao instrutor junto com o registro do kata.\n")
    except OSError as exc:
        print(f"\nAviso: nao foi possivel salvar o relatorio ({exc}).", file=sys.stderr)

    return 1 if blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
