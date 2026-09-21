#!/usr/bin/env bash
# Executa a verificacao de ambiente do pre-work (macOS / Linux / Git Bash).
#   ./verificar-ambiente.sh
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$SCRIPT_DIR/verificar_ambiente.py"

if [ ! -f "$TARGET" ]; then
  echo "ERRO: verificar_ambiente.py nao encontrado em $SCRIPT_DIR" >&2
  exit 1
fi

# Procura um interpretador 3.11+; `python` pode ser 2.x em maquinas antigas.
PYTHON=""
for candidate in python3.13 python3.12 python3.11 python3 python; do
  if command -v "$candidate" >/dev/null 2>&1; then
    if "$candidate" -c 'import sys; sys.exit(0 if sys.version_info[:2] >= (3, 11) else 1)' 2>/dev/null; then
      PYTHON="$candidate"
      break
    fi
  fi
done

if [ -z "$PYTHON" ]; then
  cat >&2 <<'MSG'

ERRO: nenhum Python 3.11 ou superior encontrado.

  macOS:  brew install python@3.12
  Ubuntu: sudo apt install python3.12
  Outros: https://www.python.org/downloads/

Depois reabra o terminal e rode este script novamente.
MSG
  exit 1
fi

"$PYTHON" "$TARGET" "$@"
code=$?

echo
if [ "$code" -eq 0 ]; then
  echo "Ambiente pronto. Envie o arquivo JSON gerado ao instrutor."
else
  echo "Ha bloqueios pendentes. Siga as instrucoes acima e rode novamente."
fi
exit "$code"
