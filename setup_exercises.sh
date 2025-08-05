#!/bin/bash

# Install UV if not already installed
if ! command -v uv &> /dev/null; then
    echo "Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# Initialize the project with UV
echo "Setting up AI Efficiency Courses with UV..."
uv python install 3.10
uv sync

# Install pruna_pro from custom index
echo "Installing pruna_pro from custom index..."
uv add pruna_pro==0.2.2.post1 --index-url https://prunaai.pythonanywhere.com/simple/

echo "Setup complete! Activate the environment with:"
echo "source .venv/bin/activate"

# # Setup Hugging Face cache directory (optional)
# CACHE_PATH=<path_to_cache>
# export TORCH_HOME=$CACHE_PATH
# export HF_HOME=$CACHE_PATH
# export HUGGINGFACE_HUB_CACHE=$CACHE_PATH
# export HUGGINGFACE_ASSETS_CACHE=$CACHE_PATH
# export TRANSFORMERS_CACHE=$CACHE_PATH
# mkdir -p $HF_HOME
# export HF_TOKEN=<hf_token>

# # Export Pruna token (optional)
# export PRUNA_TOKEN=<pruna_token>
