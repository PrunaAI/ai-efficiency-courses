from transformers import AutoModelForCausalLM, AutoTokenizer
from pruna import SmashConfig
from pruna import PrunaModel
from pruna.data.pruna_datamodule import PrunaDataModule
from pruna.evaluation.evaluation_agent import EvaluationAgent
from pruna.evaluation.metrics import (
    TotalTimeMetric,
    TorchMetricWrapper,
    EnergyConsumedMetric,
    TotalMACsMetric,
    TotalParamsMetric,
    InferenceMemoryMetric,
)
from typing import Union
from transformers import Pipeline
import torch


def evaluate_model(
    model_id_or_pruna_model,
    tokenizer_id_or_tokenizer=None,
    metrics=None,
    dataset: Union[str, PrunaDataModule] = None,
):
    """
    Evaluate a model using the specified metrics.

    Args:
        model_id_or_pruna_model (str): model to evaluate
        tokenizer_id_or_tokenizer (str): tokenizer to use to process data
        metrics (list): List of metric instances to compute
        dataset (str | PrunaDataModule): Dataset to use for evaluation

    Returns:
        list: List of metric results
    """
    if dataset is None:
        dataset = "WikiText"

    if isinstance(model_id_or_pruna_model, PrunaModel):
        underlying_model = model_id_or_pruna_model.model
        # Check if the object is a transformers Pipeline
        if isinstance(underlying_model, Pipeline):
            model = underlying_model.model
            tokenizer = underlying_model.tokenizer
        else:
            if isinstance(tokenizer_id_or_tokenizer, str):
                tokenizer = AutoTokenizer.from_pretrained(tokenizer_id_or_tokenizer)
            else:
                tokenizer = tokenizer_id_or_tokenizer
        wrapped_model = model_id_or_pruna_model
        model_id = underlying_model.name_or_path
        device = wrapped_model.device
    else:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = AutoModelForCausalLM.from_pretrained(
            model_id_or_pruna_model,
            torch_dtype="auto",
        )
        model = model.to(device)
        tokenizer_id_or_tokenizer = tokenizer_id_or_tokenizer or model_id_or_pruna_model
        if isinstance(tokenizer_id_or_tokenizer, str):
            tokenizer = AutoTokenizer.from_pretrained(tokenizer_id_or_tokenizer)
        else:
            tokenizer = tokenizer_id_or_tokenizer
        wrapped_model = PrunaModel(
            model,
            smash_config=SmashConfig(device=device),
        )
        model_id = model_id_or_pruna_model

    if metrics is None or metrics == []:
        metrics = [
            TotalTimeMetric(
                n_iterations=100,
                n_warmup_iterations=10,
                device=device,
                timing_type="sync",
            ),
            InferenceMemoryMetric(),
            EnergyConsumedMetric(
                n_iterations=100, n_warmup_iterations=10, device=device
            ),
            TotalMACsMetric(),
            TotalParamsMetric(),
            TorchMetricWrapper(metric_name="perplexity", call_type="single"),
        ]

    # Create task and evaluation agent
    if isinstance(dataset, str):
        datamodule = PrunaDataModule.from_string(dataset, tokenizer=tokenizer)
    else:
        datamodule = dataset

    eval_agent = EvaluationAgent(
        request=metrics,
        datamodule=datamodule,
        device=device,
    )

    # Run evaluation
    model_results = eval_agent.evaluate(wrapped_model)

    # Cleanup
    try:
        from course.models import delete

        delete(model, tokenizer)
    except Exception:
        pass

    return model_results
