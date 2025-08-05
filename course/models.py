# Small, medium, and large model groups for AI efficiency courses
from typing import List

SMALL_MODEL_IDS: List[str] = [
    "facebook/opt-125m",
    "facebook/opt-350m",
    "meta-llama/Llama-3.2-1B",
    "meta-llama/Llama-3.2-1B-Instruct",
    "google/gemma-3-1b-it",
    "HuggingFaceTB/SmolLM-135M",
    "HuggingFaceTB/SmolLM-135M-instruct",
    "HuggingFaceTB/SmolLM2-135M",
    "HuggingFaceTB/SmolLM2-135M-Instruct",
    "HuggingFaceTB/SmolLM-360M",
    "HuggingFaceTB/SmolLM-360M-Instruct",
    "HuggingFaceTB/SmolLM2-360M",
    "HuggingFaceTB/SmolLM2-360M-Instruct",
    "PleIAs/Pleias-350m-Preview",
    "PleIAs/Pleias-Pico",
    "PleIAs/Pleias-Nano",
]

MEDIUM_MODEL_IDS: List[str] = [
    "facebook/opt-1.3b",
    "google/gemma-3-4b-it",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
    "meta-llama/Llama-3.2-3B-Instruct",
    "HuggingFaceTB/SmolLM-1.7B",
    "HuggingFaceTB/SmolLM-1.7B-Instruct",
    "HuggingFaceTB/SmolLM2-1.7B",
    "HuggingFaceTB/SmolLM2-1.7B-Instruct",
    "PleIAs/Pleias-1.2b-Preview",
    "PleIAs/Pleias-3b-Preview",
]

LARGE_MODEL_IDS: List[str] = [
    "facebook/opt-2.7b",
    # "microsoft/Phi-4-mini-instruct",
    # Add more large models as needed
]

# Optionally, for convenience, you can provide a combined list:
ALL_MODEL_IDS: List[str] = SMALL_MODEL_IDS + MEDIUM_MODEL_IDS + LARGE_MODEL_IDS
