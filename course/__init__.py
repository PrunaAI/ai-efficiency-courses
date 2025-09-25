"""
AI Efficiency Courses Library

A comprehensive library for managing and working with AI efficiency course materials,
including notebook synchronization, Colab integration, and course utilities.
"""

from course.models import (
    SMALL_MODEL_IDS,
    MEDIUM_MODEL_IDS,
    LARGE_MODEL_IDS,
    ALL_MODEL_IDS,
    clear_cache,
)
from course.slides import show_slides
from course.plots import create_single_plot, create_pareto_front
from course.evaluate import evaluate_model, evaluate_configs

__all__ = [
    "SMALL_MODEL_IDS",
    "MEDIUM_MODEL_IDS",
    "LARGE_MODEL_IDS",
    "ALL_MODEL_IDS",
    "show_slides",
    "create_single_plot",
    "create_pareto_front",
    "evaluate_model",
    "evaluate_configs",
    "clear_cache",
]
