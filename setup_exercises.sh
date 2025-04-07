#!/bin/bash

# Install Miniconda
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O $HOME/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p $HOME/miniconda3
rm ~/miniconda3/miniconda.sh

# Initialize conda for bash shell
source $HOME/miniconda3/bin/activate
conda init --all

# Create courses environment
conda create -y -n courses python=3.10

# Activate courses environment
conda activate courses

# Install required packages
pip install pruna
pip install pruna[full]==0.2.0
pip install pruna_pro==0.2.0 --extra-index-url https://prunaai.pythonanywhere.com/
pip install matplotlib
pip install jupyterlab
# pip install notebook

# # Setup Hugging Face cache directory
# CACHE_PATH=<path_to_cache>
# export TORCH_HOME=$CACHE_PATH
# export HF_HOME=$CACHE_PATH
# export HUGGINGFACE_HUB_CACHE=$CACHE_PATH
# export HUGGINGFACE_ASSETS_CACHE=$CACHE_PATH
# export TRANSFORMERS_CACHE=$CACHE_PATH
# mkdir -p $HF_HOME
# export HF_TOKEN=<hf_token>


# # Export Pruna token
# export PRUNA_TOKEN=<pruna_token>
