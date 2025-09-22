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
)
from course.slides import show_slides
from course.plots import create_single_plot, create_multiple_plots, create_pareto_front, create_comparison_plots
from course.evaluate import evaluate, evaluate_configs

__all__ = [
    "SMALL_MODEL_IDS",
    "MEDIUM_MODEL_IDS",
    "LARGE_MODEL_IDS",
    "ALL_MODEL_IDS",
    "show_slides",
    "create_single_plot",
    "create_multiple_plots",
    "create_pareto_front",
    "evaluate",
    "evaluate_configs",
    "create_comparison_plots",
]
