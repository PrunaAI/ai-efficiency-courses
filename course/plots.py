import matplotlib.pyplot as plt

from typing import Dict, List, Optional
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt


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


def create_multiple_plots(
    data_dicts: List[Dict[str, float]],
    x_label: str,
    y_label: str,
    titles: Optional[List[str]] = None,
    n_cols: int = 2,
) -> None:
    """
    Creates and displays a raster (grid) of bar plots, each using a different data_dict.

    Args:
        data_dicts (List[Dict[str, float]]): List of dictionaries, each containing the data to plot for a subplot.
        x_label (str): Label for the x-axis.
        y_label (str): Label for the y-axis.
        titles (Optional[List[str]]): List of titles for each subplot. If None, generic titles are used.
        n_cols (int): Number of columns in the raster grid.

    Returns:
        None: Displays the raster plot in the default browser or notebook.
    """
    try:
        n_plots = len(data_dicts)
        n_rows = (n_plots + n_cols - 1) // n_cols

        # Use generic titles if not provided
        if titles is None:
            titles = [f"Plot {i + 1}" for i in range(n_plots)]
        elif len(titles) < n_plots:
            # Pad titles if not enough provided
            titles += [f"Plot {i + 1}" for i in range(len(titles), n_plots)]

        fig = make_subplots(rows=n_rows, cols=n_cols, subplot_titles=titles)

        for idx in range(n_rows * n_cols):
            row = idx // n_cols + 1
            col = idx % n_cols + 1
            if idx < n_plots:
                data_dict = data_dicts[idx]
                fig.add_trace(
                    go.Bar(
                        x=list(data_dict.keys()),
                        y=list(data_dict.values()),
                        showlegend=False,
                    ),
                    row=row,
                    col=col,
                )
            else:
                # Add empty trace for unused subplots
                fig.add_trace(go.Bar(x=[], y=[], showlegend=False), row=row, col=col)

        fig.update_layout(
            height=400 * n_rows,
            width=500 * n_cols,
            title_text="Raster of Module Stats",
            template="plotly_white",
            margin=dict(l=40, r=40, t=60, b=80),
        )

        # Update axes for all subplots
        for i in range(1, n_rows * n_cols + 1):
            fig["layout"][f"xaxis{i}"]["title"] = x_label
            fig["layout"][f"yaxis{i}"]["title"] = y_label
            fig["layout"][f"xaxis{i}"]["tickangle"] = -45

        fig.show()
    except Exception as e:
        raise RuntimeError(
            f"Failed to create raster plot with data_dicts={data_dicts}, x_label={x_label}, y_label={y_label}, titles={titles}, n_cols={n_cols}"
        ) from e


import matplotlib.pyplot as plt
from typing import Dict, Any, List

def create_pareto_front(
    results: Dict[str, Any],
    metric1_name: str,
    metric2_name: str,
    results2: Dict[str, List[Any]] = None,
) -> None:
    """
    Plot a Pareto front comparing two metrics across models/quantizers.

    This function supports two input formats:
    1. results = {model: {metric1_name: value, metric2_name: value}}
    2. results + results2 where each is {model: [metric_objects]} with
       metric_objects having `.name` and `.result`.

    Args:
        results: Dictionary of results for the first format OR metric1 results (second format).
        metric1_name: Name of the first metric to plot on x-axis.
        metric2_name: Name of the second metric to plot on y-axis.
        results2: (Optional) Dictionary of results for the second metric in the second format.
    """
    labels = []
    metric1_values = []
    metric2_values = []

    if results2 is None:
        # Format 1: results[model][metric_name] = value
        for model, metrics in results.items():
            if metrics is not None and metric1_name in metrics and metric2_name in metrics:
                labels.append(model)
                metric1_values.append(metrics[metric1_name])
                metric2_values.append(metrics[metric2_name])
    else:
        # Format 2: results[model] = [metric objects with .name and .result]
        for model_name in results.keys():
            if model_name in results and model_name in results2:
                labels.append(model_name)
                try:
                    metric1_val = [m.result for m in results[model_name] if m.name == metric1_name][0]
                    metric2_val = [m.result for m in results2[model_name] if m.name == metric2_name][0]
                    metric1_values.append(metric1_val)
                    metric2_values.append(metric2_val)
                except IndexError:
                    print(f"{model_name} missing one of the metrics.")
            else:
                print(f"{model_name} missed evaluation.")

    # Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(metric1_values, metric2_values)

    for i, label in enumerate(labels):
        plt.annotate(
            label,
            (metric1_values[i], metric2_values[i]),
            xytext=(5, 5),
            textcoords="offset points",
        )

    plt.xlabel(metric1_name)
    plt.ylabel(metric2_name)
    plt.title(f"Pareto Front: {metric1_name} vs {metric2_name}")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.show()


def create_comparison_plots(evaluation_results):
    """
    Plot evaluation metrics for different model configurations.

    Args:
        evaluation_results (dict): Dictionary containing evaluation metrics for each model configuration
    """
    # Get metrics from first result (assuming all configs have same metrics)
    first_result = next(iter(evaluation_results.values()))
    metrics = [
        key
        for key in first_result.keys()
        if isinstance(first_result[key], (int, float))
    ]
    data = {}

    for metric in metrics:
        data[metric] = [
            evaluation_results[model][metric] for model in evaluation_results
        ]

    # Calculate number of rows and columns for subplots
    n_metrics = len(metrics)
    n_cols = 3  # Display 3 plots per row
    n_rows = (
        n_metrics + n_cols - 1
    ) // n_cols  # Ceiling division to get number of rows needed

    # Create figure with subplots
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
    fig.suptitle("Comparison of Models with Different Bit Precision", y=1.02)

    # Flatten axes array to make iteration easier
    axes = axes.flatten()

    # Plot each metric
    for idx, (metric, values) in enumerate(data.items()):
        ax = axes[idx]
        ax.bar(list(evaluation_results.keys()), values)
        ax.set_ylabel(metric)
        ax.tick_params(axis="x", rotation=45)

    # Hide empty subplots if any
    for idx in range(len(metrics), len(axes)):
        axes[idx].set_visible(False)

    plt.tight_layout()
    plt.show()


# def plot_pareto_front(results, metric1_name, metric2_name):
#     """
#     Plot a pareto front comparing two metrics across different quantization methods.

#     Args:
#         results (dict): Dictionary mapping quantizer names to their evaluation results
#         metric1_name (str): Name of the first metric to plot on x-axis
#         metric2_name (str): Name of the second metric to plot on y-axis

#     Creates a scatter plot showing the tradeoff between the two metrics for each quantizer,
#     with points labeled by quantizer name. Includes a grid and appropriate axis labels.
#     """
#     # Extract metrics for each quantizer
#     quantizers = []
#     metric1_values = []
#     metric2_values = []

#     for quantizer, result in results.items():
#         if result is not None and metric1_name in result and metric2_name in result:
#             quantizers.append(quantizer)
#             metric1_values.append(result[metric1_name])
#             metric2_values.append(result[metric2_name])

#     plt.figure(figsize=(10, 6))
#     plt.scatter(metric1_values, metric2_values)
#     for i, quantizer in enumerate(quantizers):
#         plt.annotate(
#             quantizer,
#             (metric1_values[i], metric2_values[i]),
#             xytext=(5, 5),
#             textcoords="offset points",
#         )
#     plt.xlabel(metric1_name)
#     plt.ylabel(metric2_name)
#     plt.title(f"Pareto Front: {metric1_name} vs {metric2_name}")
#     plt.grid(True, linestyle="--", alpha=0.7)

#     plt.show()

# def create_pareto_front(metric1_results: Dict[str, float], metric2_results: Dict[str, float], metric1_name: str, metric2_name: str) -> None:
#     """
#     Plot pareto front comparing two metrics across models.

#     Args:
#         metric1_results: Results dictionary for first metric
#         metric2_results: Results dictionary for second metric
#         metric1_name: Name of first metric to display
#         metric2_name: Name of second metric to display
#     """
#     # Extract values for each model
#     models = []
#     metric1_values = []
#     metric2_values = []

#     for model_name in metric1_results.keys():
#         if model_name in metric1_results and model_name in metric2_results:
#             models.append(model_name)
#             metric1_values.append(
#                 [
#                     metric
#                     for metric in metric1_results[model_name]
#                     if metric.name == metric1_name
#                 ][0].result
#             )
#             metric2_values.append(
#                 [
#                     metric
#                     for metric in metric2_results[model_name]
#                     if metric.name == metric2_name
#                 ][0].result
#             )
#         else:
#             print(f"{model_name} missed evaluation.")

#     # Create scatter plot
#     plt.figure(figsize=(10, 6))
#     print(metric2_values)
#     plt.scatter(metric1_values, metric2_values)

#     # Add labels for each point
#     for i, model in enumerate(models):
#         plt.annotate(model, (metric1_values[i], metric2_values[i]))

#     plt.xlabel(metric1_name)
#     plt.ylabel(metric2_name)
#     plt.title(f"Pareto Front: {metric1_name} vs {metric2_name}")
#     plt.grid(True)
#     plt.show()