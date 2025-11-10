"""
AI Efficiency Courses Library

A comprehensive library for managing and working with AI efficiency course materials,
including notebook synchronization, Colab integration, and course utilities.
"""

from course.evaluate import evaluate_model
from course.models import (
    ALL_MODEL_IDS,
    LARGE_MODEL_IDS,
    MEDIUM_MODEL_IDS,
    SMALL_MODEL_IDS,
)
from course.plots import (
    create_comparison_plots,
    create_pareto_front,
    create_single_plot,
)
from course.slides import show_slides

__all__ = [
    "SMALL_MODEL_IDS",
    "MEDIUM_MODEL_IDS",
    "LARGE_MODEL_IDS",
    "ALL_MODEL_IDS",
    "show_slides",
    "create_single_plot",
    "create_pareto_front",
    "evaluate_model",
    "create_comparison_plots",
]
