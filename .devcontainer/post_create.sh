#!/bin/zsh

echo "Setup python environment..."
uv sync --locked --python $SPLUNK_HOME/bin/python3
uv pip install $(uv pip freeze | grep splunk-sdk) --target app/bin/lib

echo "Get splunk token..."
bash .devcontainer/get_splunk_token.sh

echo "Setup complete!"
