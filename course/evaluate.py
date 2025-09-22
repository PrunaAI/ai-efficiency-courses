from transformers import AutoModelForCausalLM, AutoTokenizer
from pruna import SmashConfig, smash
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
import gc
import copy
from typing import Union, List
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Pipeline

def evaluate(
    models: Union[str, PrunaModel, List[Union[str, PrunaModel]]],
    tokenizer_id_or_tokenizer=None,
    metrics=None,
    dataset: Union[str, PrunaDataModule] = "WikiText",
):
    """
    Evaluate one or more models using the specified metrics.

    Args:
        models (str | PrunaModel | list): A model ID, a PrunaModel,
                                          or a list of them.
        tokenizer_id_or_tokenizer (str | AutoTokenizer, optional):
            Tokenizer or tokenizer ID. Used only for single-model evaluation.
        metrics (list, optional): List of metric instances to compute.
        dataset (str | PrunaDataModule, optional): Dataset to use for evaluation.

    Returns:
        dict | list:
            If a single model is evaluated, returns the list of metric results.
            If multiple models are evaluated, returns a dict mapping model IDs
            to their results (or error messages).
    """

    def _evaluate_single_model(model_id_or_pruna_model, tokenizer_id_or_tokenizer, metrics, dataset):
        """Helper for evaluating a single model."""
        print("model_id_or_pruna_model", model_id_or_pruna_model)
        print(type(model_id_or_pruna_model))

        if isinstance(model_id_or_pruna_model, PrunaModel):
            underlying_model = model_id_or_pruna_model.model
            print("underlying_model_prunamodel", underlying_model)

            if isinstance(underlying_model, Pipeline):
                print("underlying_model_pipeline", underlying_model)
                model = underlying_model.model
                tokenizer = underlying_model.tokenizer
            else:
                print("underlying_model_not_pipeline", underlying_model)
                if isinstance(tokenizer_id_or_tokenizer, str):
                    tokenizer = AutoTokenizer.from_pretrained(tokenizer_id_or_tokenizer)
                else:
                    tokenizer = tokenizer_id_or_tokenizer
            wrapped_model = model_id_or_pruna_model
            model_id = underlying_model.name_or_path
            device = wrapped_model.device
        else:
            underlying_model = model_id_or_pruna_model.model
            print("underlying_model_prunamodel", underlying_model)
            if isinstance(tokenizer_id_or_tokenizer, str):
                tokenizer = AutoTokenizer.from_pretrained(tokenizer_id_or_tokenizer)
            else:
                tokenizer = tokenizer_id_or_tokenizer
            wrapped_model = model_id_or_pruna_model
            model_id = underlying_model.name_or_path
            device = wrapped_model.device
            # device = "cuda" if torch.cuda.is_available() else "cpu"
            # print("else", model_id_or_pruna_model)
            # model = AutoModelForCausalLM.from_pretrained(
            #     model_id_or_pruna_model,
            #     torch_dtype="auto",
            # ).to(device)
            # tokenizer_id_or_tokenizer = tokenizer_id_or_tokenizer or model_id_or_pruna_model
            # if isinstance(tokenizer_id_or_tokenizer, str):
            #     tokenizer = AutoTokenizer.from_pretrained(tokenizer_id_or_tokenizer)
            # else:
            #     tokenizer = tokenizer_id_or_tokenizer
            # wrapped_model = PrunaModel(
            #     model,
            #     smash_config=SmashConfig(device=device),
            # )
            # model_id = model_id_or_pruna_model

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

        # Prepare dataset
        if isinstance(dataset, str):
            datamodule = PrunaDataModule.from_string(dataset, tokenizer=tokenizer)
        else:
            datamodule = dataset

        # Run evaluation
        eval_agent = EvaluationAgent(
            request=metrics,
            datamodule=datamodule,
            device=device,
        )
        model_results = eval_agent.evaluate(wrapped_model)

        # Cleanup
        try:
            from course.models import clear_cache
            clear_cache(model, tokenizer)
        except Exception:
            pass

        return model_id, model_results

    if isinstance(models, list):
        results = {}
        for model in models:
            print(f"\nEvaluating {model}")
            try:
                model_id, res = _evaluate_single_model(model, tokenizer_id_or_tokenizer, metrics, dataset)
                results[model_id] = res
                print(f"Results for {model_id}:")
                print(res)
            except Exception as e:
                print(f"Error evaluating {model}: {str(e)}")
                results[str(model)] = str(e)
        return results
    else:
        _, res = _evaluate_single_model(models, tokenizer_id_or_tokenizer, metrics, dataset)
        return res


# def evaluate_model(
#     model_id_or_pruna_model,
#     tokenizer_id_or_tokenizer=None,
#     metrics=None,
#     dataset: Union[str, PrunaDataModule] = None,
# ):
#     """
#     Evaluate a model using the specified metrics.

#     Args:
#         model_id_or_pruna_model (str): model to evaluate
#         tokenizer_id_or_tokenizer (str): tokenizer to use to process data
#         metrics (list): List of metric instances to compute
#         dataset (str | PrunaDataModule): Dataset to use for evaluation

#     Returns:
#         list: List of metric results
#     """
#     if dataset is None:
#         dataset = "WikiText"

#     if isinstance(model_id_or_pruna_model, PrunaModel):
#         underlying_model = model_id_or_pruna_model.model
#         # Check if the object is a transformers Pipeline
#         if isinstance(underlying_model, Pipeline):
#             model = underlying_model.model
#             tokenizer = underlying_model.tokenizer
#         else:
#             if isinstance(tokenizer_id_or_tokenizer, str):
#                 tokenizer = AutoTokenizer.from_pretrained(tokenizer_id_or_tokenizer)
#             else:
#                 tokenizer = tokenizer_id_or_tokenizer
#         wrapped_model = model_id_or_pruna_model
#         model_id = underlying_model.name_or_path
#         device = wrapped_model.device
#     else:
#         device = "cuda" if torch.cuda.is_available() else "cpu"
#         model = AutoModelForCausalLM.from_pretrained(
#             model_id_or_pruna_model,
#             torch_dtype="auto",
#         )
#         model = model.to(device)
#         tokenizer_id_or_tokenizer = tokenizer_id_or_tokenizer or model_id_or_pruna_model
#         if isinstance(tokenizer_id_or_tokenizer, str):
#             tokenizer = AutoTokenizer.from_pretrained(tokenizer_id_or_tokenizer)
#         else:
#             tokenizer = tokenizer_id_or_tokenizer
#         wrapped_model = PrunaModel(
#             model,
#             smash_config=SmashConfig(device=device),
#         )
#         model_id = model_id_or_pruna_model

#     if metrics is None or metrics == []:
#         metrics = [
#             TotalTimeMetric(
#                 n_iterations=100,
#                 n_warmup_iterations=10,
#                 device=device,
#                 timing_type="sync",
#             ),
#             InferenceMemoryMetric(),
#             EnergyConsumedMetric(
#                 n_iterations=100, n_warmup_iterations=10, device=device
#             ),
#             TotalMACsMetric(),
#             TotalParamsMetric(),
#             TorchMetricWrapper(metric_name="perplexity", call_type="single"),
#         ]

#     # Create task and evaluation agent
#     if isinstance(dataset, str):
#         datamodule = PrunaDataModule.from_string(dataset, tokenizer=tokenizer)
#     else:
#         datamodule = dataset

#     eval_agent = EvaluationAgent(
#         request=metrics,
#         datamodule=datamodule,
#         device=device,
#     )

#     # Run evaluation
#     model_results = eval_agent.evaluate(wrapped_model)

#     # Cleanup
#     try:
#         from course.models import delete

#         delete(model, tokenizer)
#     except Exception:
#         pass

#     return model_results


# def evaluate_models(model_ids, metrics, dataset="WikiText"):
#     """
#     Evaluate multiple models using the specified metrics.

#     Args:
#         model_ids (list): List of model IDs to evaluate
#         metrics (list): List of metric instances to compute

#     Returns:
#         dict: Dictionary mapping model IDs to their evaluation results
#     """
#     results = {}

#     for model_id in model_ids:
#         print(f"\nEvaluating {model_id}")

#         try:
#             # Load model and tokenizer
#             model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype="auto")
#             device = metrics[0].device
#             model = model.to(device)
#             tokenizer = AutoTokenizer.from_pretrained(model_id)
#             wrapped_model = PrunaModel(
#                 model,
#                 smash_config=SmashConfig(device=device),
#             )

#             # Create task and evaluation agent
#             eval_agent = EvaluationAgent(
#                 request=metrics,
#                 datamodule=PrunaDataModule.from_string(dataset, tokenizer=tokenizer),
#                 device=device,
#             )

#             # Run evaluation
#             model_results = eval_agent.evaluate(wrapped_model)
#             results[model_id] = model_results
#             print(f"Results for {model_id}:")
#             print(model_results)

#             # Cleanup
#             delete(model, tokenizer)

#         except Exception as e:
#             print(f"Error evaluating {model_id}: {str(e)}")
#             results[model_id] = str(e)

#     return results

def evaluate_configs(model, tokenizer, smash_configs, dataset="WikiText"):
    """Evaluate multiple quantization configurations on a model.

    Args:
        model: The base model to evaluate quantization on (AutoModelForCausalLM)
        smash_configs: List of quantization configurations to evaluate
        dataset: Name of the dataset to evaluate on (default: "WikiText")

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

    ### To Complete ###
    for config in smash_configs:
        # Deep copy the model for this config
        model_copy = copy.deepcopy(model)

        try:
            # Apply quantization
            quantized_model = smash(model_copy, config)

            # Evaluate
            result = evaluate(models=quantized_model, tokenizer_id_or_tokenizer=tokenizer, dataset=dataset)
            results[config[config["quantizer"] + "_weight_bits"]] = result

        except Exception as e:
            print(f"Error evaluating {config['quantizer']}: {str(e)}")
            results[config[config["quantizer"] + "_weight_bits"]] = None

        finally:
            del model_copy
            del quantized_model
            torch.cuda.empty_cache()
            gc.collect()
    ### End of To Complete ###

    return results

# from course.models import delete

# def smash_evaluate_perplexity(model, tokenizer, smash_config, dataset="WikiText"):
#     ### To Complete ###
#     model_copy = copy.deepcopy(model)

#     if smash_config:
#         model_copy = smash(model_copy, smash_config)
#     metrics = [TorchMetricWrapper(metric_name="perplexity", call_type="single")]
#     task = Task(
#         metrics, datamodule=PrunaDataModule.from_string(dataset, tokenizer=tokenizer)
#     )
#     eval_agent = EvaluationAgent(task)
#     results = eval_agent.evaluate(model_copy)

#     delete(model_copy)
#     ### End of To Complete ###

#     return results