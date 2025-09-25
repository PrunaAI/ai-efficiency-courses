import copy
from typing import Union

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Pipeline

from pruna import SmashConfig, smash, PrunaModel
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
    try:
        from course.models import clear_cache
        clear_cache(model, tokenizer)
    except Exception:
        pass

    return model_results

def evaluate_configs(model_id, smash_configs, dataset=None):
    """Evaluate multiple configurations on a model.

    Args:
        model_id: The base model ID to evaluate quantization
        smash_configs: The list of configurations to evaluate
        dataset: Name of the dataset to evaluate

    Returns:
        dict: Dictionary mapping quantization bit width to evaluation results, where each result contains:
            - Elapsed time
            - GPU memory usage
            - Energy consumption
            - Model architecture details
            - Perplexity score
            Returns None for configurations that fail
    """
    results = {}

    model = AutoModelForCausalLM.from_pretrained(model_id)
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    for smash_config in smash_configs:
        model_copy = copy.deepcopy(model)

        try:
            # Apply quantization
            quantized_model = smash(model_copy, smash_config)

            # Evaluate
            result = evaluate_model(model_id_or_pruna_model=quantized_model, tokenizer_id_or_tokenizer=tokenizer, dataset=dataset)
            results[smash_config[smash_config["quantizer"] + "_weight_bits"]] = result

        except Exception as e:
            print(f"Error evaluating {smash_config['quantizer']}: {str(e)}")
            results[smash_config[smash_config["quantizer"] + "_weight_bits"]] = None

        finally:
            del model_copy
            del quantized_model
            try:
                from course.models import clear_cache
                clear_cache(model, tokenizer)
            except Exception:
                pass

    return results