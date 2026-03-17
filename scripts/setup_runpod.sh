#! /usr/bin/env bash

SCRIPT_DIR="$(dirname "$(realpath "$0")")"

# Install linux packages
apt-get update
apt-get install -y less python3-dev build-essential ranger tmux unzip vim

# uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# git
git config --global user.email "librakevin@gmail.com"
git config --global user.name "Terry Tao"

# clone nanochat repo
cd $HOME
git clone https://github.com/taot/nanochat.git
cd nanochat

# install python packages
uv sync --extra gpu

# wandb
source .venv/bin/activate
wandb login
