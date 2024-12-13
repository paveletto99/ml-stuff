#!/usr/bin/env bash

# install lsp
pip install --upgrade pip
pip install ruff-lsp

# Install Python dependencies with uv
curl -LsSf https://astral.sh/uv/install.sh | bash
source $HOME/.local/bin/env bash
uv sync