#!/usr/bin/bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$HOME/.venvs/mcp1c"
SRC_DIR="$REPO_DIR/src"

echo "==> Создаём venv: $VENV_DIR"
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

export PYTHONPATH="$SRC_DIR"

echo "==> Устанавливаем зависимости"
pip install --upgrade pip
pip install -r "$REPO_DIR/requirements.txt"

echo "==> Чистим предыдущую сборку"
rm -rf "$REPO_DIR/build" "$REPO_DIR/dist"

echo "==> Собираем бинарь"
cd "$REPO_DIR"
python -m PyInstaller "$REPO_DIR/mcp1c.spec" --clean

echo ""
echo "✓ Готово: $REPO_DIR/dist/mcp1c-proxy"
echo ""
cp $REPO_DIR/dist/mcp1c-proxy ~/.local/bin
chmod +x ~/.local/bin/mcp1c-proxy
mkdir ~/.config/mcp1c
cp  $REPO_DIR/mcp1c.conf ~/.config/mcp1c/mcp1c.conf 
echo "Установить глобально:"
echo "  sudo cp $REPO_DIR/dist/mcp1c-proxy /usr/local/bin/"
echo "  sudo chmod +x /usr/local/bin/mcp1c-proxy"
