from typing import Any, Dict, List

import matplotlib.pyplot as plt
import plotly.graph_objects as go


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


def create_comparison_plots(
    data_dict: Dict[str, List[Any]],
    title: str,
    x_label: str,
    y_label: str = "Value",
):
    """
    Plot evaluation metrics for different model configurations.
    Args:
        data_dict (dict): Dictionary containing evaluation metrics for each model configuration
        title (str): Title of the plot
        x_label (str): Label for the x-axis
        y_label (str): Label for the y-axis
    """
    # Get metrics names from the first result (all configs assumed same set of metrics)
    first_result_list = next(iter(data_dict.values()))
    metrics = [mr.name for mr in first_result_list]

    # Prepare data dictionary {metric_name: {bits: value}}
    data = {metric: {} for metric in metrics}

    for bits, results in data_dict.items():
        for mr in results:
            data[mr.name][bits] = mr.result

    # Calculate subplot grid size
    n_metrics = len(metrics)
    n_cols = 3
    n_rows = (n_metrics + n_cols - 1) // n_cols  # ceiling division

    # Create figure with subplots
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
    fig.suptitle(title, y=1.02)

    # Flatten axes array to iterate easily
    axes = axes.flatten()

    # Plot each metric
    for idx, metric in enumerate(metrics):
        ax = axes[idx]
        bits_list = list(data[metric].keys())
        values = list(data[metric].values())

        ax.bar(bits_list, values)
        ax.set_title(metric)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.tick_params(axis="x", rotation=45)

    # Hide unused subplots
    for idx in range(len(metrics), len(axes)):
        axes[idx].set_visible(False)

    plt.tight_layout()
    plt.show()


def create_pareto_front(
    data_dict: Dict[str, Dict[str, float]], metric1_name: str, metric2_name: str
) -> None:
    """
    Plot pareto front comparing two metrics across different models or methods.

    Args:
        data_dict: The dictionary mapping items to their metric values.
        metric1_name: The name of the first metric to plot on the x-axis.
        metric2_name: The name of the second metric to plot on the y-axis.
    """

    # Extract the values
    items = []
    metric1_values = []
    metric2_values = []

    for item, metrics in data_dict.items():
        if metric1_name in metrics and metric2_name in metrics:
            items.append(item)
            metric1_values.append(metrics[metric1_name])
            metric2_values.append(metrics[metric2_name])

    # Plot the values
    plt.figure(figsize=(10, 6))
    plt.scatter(metric1_values, metric2_values)

    for i, model in enumerate(items):
        plt.annotate(
            model,
            (metric1_values[i], metric2_values[i]),
            xytext=(5, 5),
            textcoords="offset points",
        )

    plt.xlabel(metric1_name)
    plt.ylabel(metric2_name)
    plt.title(f"Pareto Front: {metric1_name} vs {metric2_name}")
    plt.grid(True, linestyle="--", alpha=0.7)

    plt.show()
