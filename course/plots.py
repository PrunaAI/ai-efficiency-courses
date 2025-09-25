import matplotlib.pyplot as plt
import plotly.graph_objects as go

from typing import Any, Dict, List, Optional


def create_single_plot(
    data_dict: Dict[str, float], x_label: str, y_label: str, title: str
) -> None:
    """
    Creates and displays a bar plot using Plotly.

    Args:
        data_dict (Dict[str, float]): Dictionary containing the data to plot, where keys are labels and values are the corresponding values.
        x_label (str): Label for the x-axis.
        y_label (str): Label for the y-axis.
        title (str): Title of the plot.

    Returns:
        None: Displays the plot in the default browser or notebook.
    """
    try:
        fig = go.Figure(
            data=[go.Bar(x=list(data_dict.keys()), y=list(data_dict.values()))]
        )
        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            yaxis_title=y_label,
            xaxis_tickangle=-45,
            template="plotly_white",
            margin=dict(l=40, r=40, t=60, b=80),
        )
        fig.show()
    except Exception as e:
        # Provide rich error context for debugging
        raise RuntimeError(
            f"Failed to plot module stats with data_dict={data_dict}, x_label={x_label}, y_label={y_label}, title={title}"
        ) from e


def create_pareto_front(results: Dict[str, Dict[str, float]], metric1_name: str, metric2_name: str) -> None:
    """
    Plot pareto front comparing two metrics across different models or methods.

    Args:
        results: The dictionary mapping items to their metric values.
        metric1_name: The name of the first metric to plot on the x-axis.
        metric2_name: The name of the second metric to plot on the y-axis.
    """

    # Extract the values
    items = []
    metric1_values = []
    metric2_values = []

    for item, metrics in results.items():
        if metric1_name in metrics and metric2_name in metrics:
            items.append(item)
            metric1_values.append(metrics[metric1_name])
            metric2_values.append(metrics[metric2_name])

    # Plot the values
    plt.figure(figsize=(10, 6))
    plt.scatter(metric1_values, metric2_values)

    for i, model in enumerate(items):
        plt.annotate(model, (metric1_values[i], metric2_values[i]), xytext=(5, 5), textcoords="offset points")

    plt.xlabel(metric1_name)
    plt.ylabel(metric2_name)
    plt.title(f"Pareto Front: {metric1_name} vs {metric2_name}")
    plt.grid(True, linestyle="--", alpha=0.7)

    plt.show()