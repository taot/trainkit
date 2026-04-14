#! /usr/bin/env bash

readonly SCRIPT_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
readonly PROJ_DIR="$(dirname "$SCRIPT_DIR")"

print_banner() {
    echo
    echo "#########################"
    echo "$1"
    echo "#########################"
    echo
}

#######################
# Setup system-level  #
#######################

# Install linux packages
print_banner "Installing linux packages"
apt-get update
apt-get install -y less python3-dev build-essential ranger tmux unzip vim

# uv
print_banner "Installing uv"
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# git
print_banner "Configuring git"
git config --global user.email "librakevin@gmail.com"
git config --global user.name "Terry Tao"


#######################
# Setup this project  #
#######################

# uv sync in this project
print_banner "uv sync"
cd "$PROJ_DIR"
uv sync

# add project to path
print_banner "Adding project to path"
bash $SCRIPT_DIR/add_path.sh
export PATH="$PATH:$PROJ_DIR/bin"
hf_bucket --help

# wandb
print_banner "Configuring wandb"
source .venv/bin/activate
wandb login


#######################
# Setup nanochat      #
#######################

# clone nanochat repo
print_banner "Setting up nanochat"
cd $HOME
git clone https://github.com/taot/nanochat.git
cd nanochat

# install python packages
print_banner "Installing python packages for nanochat"
uv sync --extra gpu
