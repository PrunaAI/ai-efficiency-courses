# Small, medium, and large model groups for AI efficiency courses
from typing import List

SMALL_MODEL_IDS: List[str] = [
    "facebook/opt-125m",
    "facebook/opt-350m",
    "HuggingFaceTB/SmolLM-135M-instruct",
    "HuggingFaceTB/SmolLM2-135M-Instruct",
    "HuggingFaceTB/SmolLM-360M-Instruct",
    "HuggingFaceTB/SmolLM2-360M-Instruct",
    "PleIAs/Pleias-350m-Preview",
    "PleIAs/Pleias-Pico",
    "LiquidAI/LFM2-350M",
    "LiquidAI/LFM2-700M",
]

MEDIUM_MODEL_IDS: List[str] = [
    "facebook/opt-1.3b",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
    "HuggingFaceTB/SmolLM-1.7B-Instruct",
    "HuggingFaceTB/SmolLM2-1.7B-Instruct",
    "PleIAs/Pleias-1.2b-Preview",
    "PleIAs/Pleias-Nano",
    "NousResearch/Llama-3.2-1B",
    "google/gemma-3-1b-it",
    "LiquidAI/LFM2-1.2B",
]

LARGE_MODEL_IDS: List[str] = [
    "facebook/opt-2.7b",
    "NousResearch/Hermes-3-Llama-3.2-3BPleIAs/Pleias-3b-Preview",
    "google/gemma-3-4b-it",
]

# Optionally, for convenience, you can provide a combined list:
ALL_MODEL_IDS: List[str] = SMALL_MODEL_IDS + MEDIUM_MODEL_IDS + LARGE_MODEL_IDS
