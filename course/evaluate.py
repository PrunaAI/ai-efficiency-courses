import gc
from typing import Union

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Pipeline

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

def evaluate_model(
    model_id_or_pruna_model,
    tokenizer_id_or_tokenizer=None,
    metrics=None,
    dataset: Union[str, PrunaDataModule] = None,
):
    """
    Evaluate a model using the specified metrics.

    Args:
        model_id_or_pruna_model: The model ID or PrunaModel to evaluate.
        tokenizer_id_or_tokenizer: The tokenizer ID or AutoTokenizer to use to process data.
        metrics: The list of metric instances to compute.
        dataset: The dataset to use for evaluation

    Returns:
        list: The list of metric results.
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
        device = wrapped_model.device
    elif isinstance(model_id_or_pruna_model, str):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = AutoModelForCausalLM.from_pretrained(
            model_id_or_pruna_model,
            dtype="auto",
        )
        model = model.to(device)
        tokenizer_id_or_tokenizer = tokenizer_id_or_tokenizer or model_id_or_pruna_model
        if isinstance(tokenizer_id_or_tokenizer, str):
            tokenizer = AutoTokenizer.from_pretrained(tokenizer_id_or_tokenizer)
        else:
            tokenizer = tokenizer_id_or_tokenizer
        tokenizer.pad_token = tokenizer.eos_token
        wrapped_model = PrunaModel(model)
    else:
        underlying_model = model_id_or_pruna_model.model
        if isinstance(tokenizer_id_or_tokenizer, str):
            tokenizer = AutoTokenizer.from_pretrained(tokenizer_id_or_tokenizer)
        else:
            tokenizer = tokenizer_id_or_tokenizer
            wrapped_model = model_id_or_pruna_model
            device = wrapped_model.device


    if not metrics:
        metrics = [
            TotalTimeMetric(
                n_iterations=100,
                n_warmup_iterations=10,
                device=device,
                timing_type="sync",
            ),
            InferenceMemoryMetric(),
            EnergyConsumedMetric(
                n_iterations=100,
                n_warmup_iterations=10,
                device=device,
            ),
            TotalMACsMetric(),
            TotalParamsMetric(),
            TorchMetricWrapper(
                metric_name="perplexity",
                call_type="single",
            ),
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
    del wrapped_model
    del tokenizer
    torch.cuda.empty_cache()
    gc.collect()

    return model_results