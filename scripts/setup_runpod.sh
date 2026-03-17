#! /usr/bin/env bash

readonly SCRIPT_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
readonly PROJ_DIR="$(dirname "$SCRIPT_DIR")"

#######################
# Setup system-level  #
#######################

# Install linux packages
apt-get update
apt-get install -y less python3-dev build-essential ranger tmux unzip vim

# uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# git
git config --global user.email "librakevin@gmail.com"
git config --global user.name "Terry Tao"


#######################
# Setup this project  #
#######################

# uv sync in this project
cd "$PROJ_DIR"
uv sync

# add project to path
bash $SCRIPT_DIR/add_path.sh
source "$HOME/.bashrc"
hf_bucket --help

# wandb
source .venv/bin/activate
wandb login


#######################
# Setup nanochat      #
#######################

# clone nanochat repo
# cd $HOME
# git clone https://github.com/taot/nanochat.git
# cd nanochat

# # install python packages
# uv sync --extra gpu
