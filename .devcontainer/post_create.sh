#!/bin/zsh

echo "Installing Powerlevel10k..."
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git $SPLUNK_HOME/powerlevel10k
$SPLUNK_HOME/powerlevel10k/gitstatus/install
cp .devcontainer/.p10k.zsh $SPLUNK_HOME/.p10k.zsh
cp .devcontainer/.zshrc $SPLUNK_HOME/.zshrc

echo "Setup GitHub CLI config..."
mkdir -p $SPLUNK_HOME/.config/gh
cp /tmp/gh-config-host/hosts.yml $SPLUNK_HOME/.config/gh/hosts.yml
chmod 600 $SPLUNK_HOME/.config/gh/hosts.yml

echo "Setup python environment..."
uv sync --locked --python $SPLUNK_HOME/bin/python3
uv pip install $(uv pip freeze | grep splunk-sdk) --target app/bin/lib

echo "Get splunk token..."
bash .devcontainer/get_splunk_token.sh

echo "Setup complete!"
