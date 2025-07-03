#!/bin/bash

VENV_DIR=".venv"

echo "--- d4jules Setup Script ---"

# Verificar a existência do ambiente virtual
if [ ! -d "$VENV_DIR" ]; then
  echo "Virtual environment '$VENV_DIR' not found. Creating..."
  python3 -m venv "$VENV_DIR"
  if [ $? -eq 0 ]; then
    echo "Virtual environment '$VENV_DIR' reported as created by 'python3 -m venv'."
    echo "Checking contents of $VENV_DIR/bin/ immediately after creation:"
    ls -la "$VENV_DIR/bin/"
    if [ -f "$VENV_DIR/bin/activate" ]; then
      echo "'activate' script found in $VENV_DIR/bin/."
    else
      echo "Error: 'activate' script NOT found in $VENV_DIR/bin/ immediately after creation. This is unexpected."
      exit 1
    fi
  else
    echo "Error: Failed to create virtual environment '$VENV_DIR' (python3 -m venv command failed)."
    exit 1 # Sair se a criação do venv falhar
  fi
else
  echo "Virtual environment '$VENV_DIR' found."
  echo "Checking contents of $VENV_DIR/bin/ (pre-existing):"
  ls -la "$VENV_DIR/bin/"
  if [ ! -f "$VENV_DIR/bin/activate" ]; then
     echo "Error: Pre-existing '$VENV_DIR' found, but 'activate' script is missing from $VENV_DIR/bin/. Try removing .venv and running again."
     exit 1
  fi
fi

echo "Attempting to activate virtual environment..."
source "$VENV_DIR/bin/activate"
if [ $? -ne 0 ]; then
  echo "Error: Failed to activate virtual environment."
  exit 1
fi
echo "Virtual environment activated."

echo "Updating repository..."
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
git pull origin "$CURRENT_BRANCH"
if [ $? -ne 0 ]; then
  echo "Warning: 'git pull' failed. Proceeding with current local version."
  # Depending on strictness, one might choose to exit here.
  # For now, a warning is issued.
fi

echo "Upgrading pip..."
pip install --upgrade pip
if [ $? -ne 0 ]; then
  echo "Warning: Failed to upgrade pip."
  # Not critical enough to exit usually
fi

echo "Installing/updating dependencies from requirements.txt..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
  echo "Error: Failed to install dependencies from requirements.txt."
  exit 1 # Dependencies are critical
fi
echo "Dependencies installed/updated."

echo "Running d4jules scraper application..."
python3 src/scraper_cli.py
# Running the script directly. Ensure PYTHONPATH is set up if imports within scraper_cli fail.
# Or, if src is meant to be an installable package, `python -m src.scraper_cli` might be used
# after installation or if PYTHONPATH includes the parent of `src`.
# For now, direct script execution is simpler if scraper_cli.py handles its own imports relative to `src`.
# scraper_cli.py will handle its own exit codes. If it fails, start.sh will still complete.
# For stricter error handling, check $? after the python3 command.

echo "----------------------------"
echo "d4jules setup script finished. Application execution completed or attempted."
