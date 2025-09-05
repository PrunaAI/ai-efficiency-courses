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
    self,
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


def plot_pareto_front(results, metric1_name, metric2_name):
    """
    Plot a pareto front comparing two metrics across different quantization methods.

    Args:
        results (dict): Dictionary mapping quantizer names to their evaluation results
        metric1_name (str): Name of the first metric to plot on x-axis
        metric2_name (str): Name of the second metric to plot on y-axis

    Creates a scatter plot showing the tradeoff between the two metrics for each quantizer,
    with points labeled by quantizer name. Includes a grid and appropriate axis labels.
    """
    # Extract metrics for each quantizer
    quantizers = []
    metric1_values = []
    metric2_values = []

    for quantizer, result in results.items():
        if result is not None and metric1_name in result and metric2_name in result:
            quantizers.append(quantizer)
            metric1_values.append(result[metric1_name])
            metric2_values.append(result[metric2_name])

    plt.figure(figsize=(10, 6))
    plt.scatter(metric1_values, metric2_values)
    for i, quantizer in enumerate(quantizers):
        plt.annotate(
            quantizer,
            (metric1_values[i], metric2_values[i]),
            xytext=(5, 5),
            textcoords="offset points",
        )
    plt.xlabel(metric1_name)
    plt.ylabel(metric2_name)
    plt.title(f"Pareto Front: {metric1_name} vs {metric2_name}")
    plt.grid(True, linestyle="--", alpha=0.7)

    plt.show()
