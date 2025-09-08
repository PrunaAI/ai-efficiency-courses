from course.models import delete

def evaluate_models(model_ids, metrics, dataset="WikiText"):
    """
    Evaluate multiple models using the specified metrics.

    Args:
        model_ids (list): List of model IDs to evaluate
        metrics (list): List of metric instances to compute

    Returns:
        dict: Dictionary mapping model IDs to their evaluation results
    """
    results = {}

    for model_id in model_ids:
        print(f"\nEvaluating {model_id}")

        try:
            # Load model and tokenizer
            model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype="auto")
            device = metrics[0].device
            model = model.to(device)
            tokenizer = AutoTokenizer.from_pretrained(model_id)
            wrapped_model = PrunaModel(
                model,
                smash_config=SmashConfig(device=device),
            )

            # Create task and evaluation agent
            eval_agent = EvaluationAgent(
                request=metrics,
                datamodule=PrunaDataModule.from_string(dataset, tokenizer=tokenizer),
                device=device,
            )

            # Run evaluation
            model_results = eval_agent.evaluate(wrapped_model)
            results[model_id] = model_results
            print(f"Results for {model_id}:")
            print(model_results)

            # Cleanup
            delete(model, tokenizer)

        except Exception as e:
            print(f"Error evaluating {model_id}: {str(e)}")
            results[model_id] = str(e)

    return results