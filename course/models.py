# Small, medium, and large model groups for AI efficiency courses
from typing import List
import os
import shutil

SMALL_MODEL_IDS: List[str] = [
    "facebook/opt-125m",
    "facebook/opt-350m",
    "HuggingFaceTB/SmolLM-135M-instruct",
    "HuggingFaceTB/SmolLM2-135M-Instruct",
    "HuggingFaceTB/SmolLM-360M-Instruct",
    "HuggingFaceTB/SmolLM2-360M-Instruct",
    "PleIAs/Pleias-350m-Preview",
    "PleIAs/Pleias-Pico",
]

MEDIUM_MODEL_IDS: List[str] = [
    "facebook/opt-1.3b",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
    "HuggingFaceTB/SmolLM-1.7B-Instruct",
    "HuggingFaceTB/SmolLM2-1.7B-Instruct",
    "PleIAs/Pleias-Nano",
    "PleIAs/Pleias-1.2b-Preview",
    "NousResearch/Llama-3.2-1B",
    "google/gemma-3-1b-it",
]

LARGE_MODEL_IDS: List[str] = [
    "facebook/opt-2.7b",
    "NousResearch/Hermes-3-Llama-3.2-3BPleIAs/Pleias-3b-Preview",
    "google/gemma-3-4b-it",
]

# Optionally, for convenience, you can provide a combined list:
ALL_MODEL_IDS: List[str] = SMALL_MODEL_IDS + MEDIUM_MODEL_IDS + LARGE_MODEL_IDS


def clear_cache(path=None):
    """
    Clear the cache of the model ids.
    """
    if path is None:
        paths_to_directories = [
            os.environ["TORCH_HOME"],
            os.environ["HF_HOME"],
            os.environ["HUGGINGFACE_HUB_CACHE"],
            os.environ["HUGGINGFACE_ASSETS_CACHE"],
            os.environ["TRANSFORMERS_CACHE"],
        ]
    else:
        paths_to_directories = [path]

    for path in paths_to_directories:
        if os.path.exists(path):
            print(f"Clearing cache from {path}")
            shutil.rmtree(path)
