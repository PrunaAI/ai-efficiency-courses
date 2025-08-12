# Efficient AI - Courses

A comprehensive learning path for building, compressing, evaluating, and deploying efficient AI models. From fundamentals to advanced techniques, this course combines theoretical knowledge with practical exercises. Perfect for students, engineers, and researchers looking to master efficient AI development.

## Table of Contents

- [📋 Overview](#overview) - Course overview
- [📚 Lectures](#lectures) - Comprehensive materials
- [💻 Exercises](#exercises) - Hands-on coding practice
- [⚙️ Setup](#setup) - Environment configuration
- [🤝 Community](#community) - Connect with other learners
- [🗂️ Resources](#resources) - Detailed references

## Overview

### 0. Introduction to Efficient AI

| Introduction to Efficient AI |  |
|---------------------------|--|
| 📊 [Slides](slides/00-introduction.pdf) | Introduction to the course concepts |

🎯 Learning Outcomes:
- How does the course work?
- Who is target audience of the course?
- What are the references for the course?

### 1. Language Model Architectures

| Language Model Architectures |  |
|----------------------------|--|
| 📊 [Slides](slides/01-language_model_architectures.pdf) | Learn about LLM building blocks and architectures |
| 🎥 [Video](https://www.youtube.com) | Coming soon |
| 💻 [Exercise](exercises/01-analyze_llm_architectures.ipynb) | Analyze LLM architectures |

🎯 Learning Outcomes: In this chapter, you will learn what are the building blocks, variations, and recent advancements on language models.
- Foundations of language models: tokens, embeddings,...
- Autoregressive language models: transformer, (flash, multi-head, paged) attention, KV cache,...
- State space language models: continuous, recursive, convolution,...
- Diffusion language models: discrete diffusion,...
- Advancements on language models: encoder/decoder, mixture-of-experts,...

### 2. Compression of Language Models

| Compression of Language Models |  |
|------------------------------|--|
| 📊 [Slides](slides/02-compress_language_models.pdf) | Learn about model compression techniques |
| 🎥 [Video](https://www.youtube.com) | Coming soon |
| 💻 [Exercise](exercises/03-run_llm_cpu_vs_gpu.ipynb) | Run LLM on CPU vs GPU |

🎯 Learning Outcomes: In this chapter, you will learn about the motivations and have an overview of model compression.
- Why do we need efficient models? Money, time, memory, Energy/CO2,...
- How to compress models? Quantization, pruning, distillation, compilation,..
- How do compression methdos help efficiency? memory reduction, latency reduction,...

### 3. Evaluation of Language Models

| Evaluation of Language Models |  |
|-----------------------------|--|
| 📊 [Slides](slides/03-evalaute_language_models.pdf) | Learn how to evaluate LLM efficiency |
| 🎥 [Video](https://www.youtube.com) | Coming soon |
| 💻 [Exercise](exercises/02-measure_llm_efficiency.ipynb) | Measure LLM efficiency |

🎯 Learning Outcomes: In this chapter, you will learn how to evaluate the different efficiency aspects of language models.
- Quality evaluation: perplexity, accuracy,...
- Memory evaluation: #Parameters/#Activations, disk/inference/training memory, scaling laws,...
- Compute evaluation: MAC, FLOP, OP, scaling laws...
- Real-world evaluation: latency, througput, money, energy,...

### 4. Quantization of Language Models

| Quantization of Language Models |  |
|--------------------------------|--|
| 📊 [Slides](slides/04-quantize_language_models.pdf) | Learn about model quantization methods |
| 🎥 [Video](https://www.youtube.com) | Coming soon |
| 💻 [Exercise 1](exercises/03-run_llm_cpu_vs_gpu.ipynb) | Run LLM on CPU vs GPU |
| 💻 [Exercise 2](exercises/05-benchmark_llm_bits.ipynb) | Benchmark LLM bit precision |
| 💻 [Exercise 3](exercises/06-use_data_llm_quantization.ipynb) | Use data during quantization |

🎯 Learning Outcomes: In this chapter, you will learn how to quantize models from basic to advanced quantization methods.
- Foundations of quantization: data types, quantization procedure, static/dynamic, linear/codebook, tensor/channel/group,...
- Advancements on quantization: post-training/quantization-aware training, outliers handling, iteratives methods, usage of data,...
- Overview of SOTA quantization: GPTQ, AWQ, HQQ, AQLM, Higgs, Quanto,...

### 5. Finetuning of Language Models

| Finetuning of Language Models |  |
|------------------------------|--|
| 📊 [Slides](slides/05-finetuning_for_llms.pdf) | Learn how to finetune models to improve or recover performance |
| 🎥 [Video](https://www.youtube.com) | Coming soon |
| 💻 [Exercise](exercises/07-finetune_llm.ipynb) | Finetune compressed models |

🎯 Learning Outcomes: In this chapter, you will learn how to finetune models to improve or recover performance.
- Foundations of finetuning: finetuning procedure,...
- Advancements on finetuning: finetuning of all parameters, new parameters, selected parameters, quantized parameters,...
- Overview of SOTA finetuning: LoRA, QLoRA, Perp, P-tuing, DiffPruning,...

## Lectures

The lecture content is based on multiple sources (incl. papers, books, and lectures). If you find it helpful, please ⭐ star the repository!

| Topic | Description | Slides |
|-------|-------------|--------|
| Introduction | Introduction to efficient AI | [slides](slides/00-introduction.pdf) |
| Architectures for LLMs | Model design and optimization | [slides](slides/01-language_model_architectures.pdf) |
| Evaluation for LLMs | Performance metrics and analysis | [slides](slides/02-compress_language_models.pdf) |
| Compression for LLMs | Model size reduction techniques | [slides](slides/03-evalaute_language_models.pdf) |
| Quantization for LLMs | Precision optimization | [slides](slides/04-quantize_language_models.pdf) |
| Finetuning for LLMs | Model adaptation strategies | [slides](slides/05-finetuning_for_llms.pdf) |

> 💡 **Tip**: Access the most recent version of the lecture materials through [this URL](https://ln5.sync.com/dl/7d21bc370/gxpiqj2b-4k22jgex-x8i7zgxr-9pkajy52).

## Exercises

Located in `exercises/` and `solutions/` directories, our hands-on modules include:

| Exercise | Description | Exercise Notebook | Solution Notebook | Difficulty | Hardware |
|----------|-------------|-------------------|-------------------|------------|----------|
| **Core Exercises** | | | | | |
| 🔍 Analyze LLM architectures | Study model design patterns and optimization techniques | [notebook](exercises/01-analyze_llm_architectures.ipynb) | [solution](solutions/01-analyze_llm_architectures.ipynb) | 🟢 | CPU |
| 📊 Measure LLM efficiency | Evaluate model performance and resource usage | [notebook](exercises/02-measure_llm_efficiency.ipynb) | [solution](solutions/02-measure_llm_efficiency.ipynb) | 🟢 | CPU |
| ⚖️ Run LLM on CPU vs GPU | Compare usage of CPU and GPU for LLM inference | [notebook](exercises/03-run_llm_cpu_vs_gpu.ipynb) | [solution](solutions/03-run_llm_cpu_vs_gpu.ipynb) | 🟡 | CPU+GPU |
| 🔢 Benchmark LLM Quantization methods | Analyze impact of different quantization methods | [notebook](exercises/04-benchmark_llm_quantization_methods.ipynb) | [solution](solutions/04-benchmark_llm_quantization_methods.ipynb) | 🟡 | GPU |
| **Advanced Topics** | | | | | |
| 🚀 Benchmark LLM bit precision | Analyze impact of different bit precisions | [notebook](exercises/05-benchmark_llm_bits.ipynb) | [solution](solutions/05-benchmark_llm_bits.ipynb) | 🔴 | GPU |
| 📈 Use data during quantization | Leverage calibration data for better quantization | [notebook](exercises/06-use_data_llm_quantization.ipynb) | [solution](solutions/06-use_data_llm_quantization.ipynb) | 🔴 | GPU |
| 🎯 Finetune compressed models | Adapt quantized models for specific tasks | [notebook](exercises/07-finetune_llm.ipynb) | [solution](solutions/07-finetune_llm.ipynb) | 🔴 | GPU |

## Setup

You can easily setup your coding environment with the options below. Dependencies are specified in the `pyproject.toml`. More specifically, you can complete the exercises with the `pruna` package, and go further with the `pruna_pro`. While `pruna` enable productive exploration of efficient AI topics, `pruna_pro` package allow to address more advanced topics.

### Option 1: Automated Setup (Recommended)
```bash
bash setup_exercises.sh
```

### Option 2: Manual Setup with UV
```bash
# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env

# Setup the project
uv python install 3.10
uv sync
uv add pruna_pro==0.2.2.post1 --index-url https://prunaai.pythonanywhere.com/simple/

# Activate the environment
source .venv/bin/activate
```

### Configuration

- **Hugging Face Token**:
  Set your Hugging Face access token as an environment variable so you can download models and datasets.
  ```bash
  export HF_TOKEN=your_huggingface_token
  ```
  You can find or create your token at [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).

- **Pruna Token** (optional):
  If you want to use advanced features from the `pruna_pro` package, set your Pruna token as an environment variable:
  ```bash
  export PRUNA_TOKEN=your_pruna_token
  ```
  You can obtain a token by signing up at [https://pruna.ai](https://www.pruna.ai/pricing).

- **Google Colab Integration** (optional):
   All notebooks include Google Colab buttons for free GPU access. Click the "Open in Colab" button on any notebook to get started.

   - **Free Tier**: Tesla T4/K80/P100 GPUs, 12GB RAM, limited hours/day
   - **Colab Pro ($9.99/month)**: Priority GPU access, longer runtime, 32GB RAM
   - **Colab Pro+ ($49.99/month)**: A100 GPUs, maximum runtime, 52GB RAM

   💡 **Tip**: Use Runtime → Change runtime type → GPU for best performance

### Hardware Requirements

- **Minimum**: Modest GPU (1080Ti, 2080Ti)
- **Ideal**: High-end GPU (V100, A100)
- **Note**: Exercises are optimized for accessibility with 20+ selected small models to work on modest setup.

### Supported Models

| Model Name | Parameters | Est. Memory | Access |
|------------|------------|-------------------|--------|
| [facebook/opt-125m](https://huggingface.co/facebook/opt-125m) | 125M | 250MB | Public |
| [facebook/opt-350m](https://huggingface.co/facebook/opt-350m) | 350M | 700MB | Public |
| [facebook/opt-1.3b](https://huggingface.co/facebook/opt-1.3b) | 1.3B | 2.6GB | Public |
| [facebook/opt-2.7b](https://huggingface.co/facebook/opt-2.7b) | 2.7B | 5.4GB | Public |
| [meta-llama/Llama-3.2-1B](https://huggingface.co/meta-llama/Llama-3.2-1B) | 1B | 2GB | Gated |
| [meta-llama/Llama-3.2-1B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct) | 1B | 2GB | Gated |
| [meta-llama/Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) | 3B | 6GB | Gated |
| [google/gemma-3-1b-it](https://huggingface.co/google/gemma-3-1b-it) | 1B | 2GB | Gated |
| [google/gemma-3-4b-it](https://huggingface.co/google/gemma-3-4b-it) | 4B | 8GB | Gated |
| [deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B) | 1.5B | 3GB | Public |
| [microsoft/Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct) | 350M | 700MB | Public |
| [HuggingFaceTB/SmolLM-135M](https://huggingface.co/HuggingFaceTB/SmolLM-135M) | 135M | 270MB | Public |
| [HuggingFaceTB/SmolLM-135M-instruct](https://huggingface.co/HuggingFaceTB/SmolLM-135M-instruct) | 135M | 270MB | Public |
| [HuggingFaceTB/SmolLM-360M](https://huggingface.co/HuggingFaceTB/SmolLM-360M) | 360M | 720MB | Public |
| [HuggingFaceTB/SmolLM-360M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM-360M-Instruct) | 360M | 720MB | Public |
| [HuggingFaceTB/SmolLM-1.7B](https://huggingface.co/HuggingFaceTB/SmolLM-1.7B) | 1.7B | 3.4GB | Public |
| [HuggingFaceTB/SmolLM-1.7B-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM-1.7B-Instruct) | 1.7B | 3.4GB | Public |
| [HuggingFaceTB/SmolLM2-135M](https://huggingface.co/HuggingFaceTB/SmolLM2-135M) | 135M | 270MB | Public |
| [HuggingFaceTB/SmolLM2-135M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct) | 135M | 270MB | Public |
| [HuggingFaceTB/SmolLM2-360M](https://huggingface.co/HuggingFaceTB/SmolLM2-360M) | 360M | 720MB | Public |
| [HuggingFaceTB/SmolLM2-360M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct) | 360M | 720MB | Public |
| [HuggingFaceTB/SmolLM2-1.7B](https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B) | 1.7B | 3.4GB | Public |
| [HuggingFaceTB/SmolLM2-1.7B-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B-Instruct) | 1.7B | 3.4GB | Public |
| [PleIAs/Pleias-350m-Preview](https://huggingface.co/PleIAs/Pleias-350m-Preview) | 350M | 700MB | Public |
| [PleIAs/Pleias-Pico](https://huggingface.co/PleIAs/Pleias-Pico) | 350M | 700MB | Public |
| [PleIAs/Pleias-1.2b-Preview](https://huggingface.co/PleIAs/Pleias-1.2b-Preview) | 1.2B | 2.4GB | Public |
| [PleIAs/Pleias-Nano](https://huggingface.co/PleIAs/Pleias-Nano) | 1.2B | 2.4GB | Public |
| [PleIAs/Pleias-3b-Preview](https://huggingface.co/PleIAs/Pleias-3b-Preview) | 3B | 6GB | Public |

> Note: 
> - Exercises have been tested with these models but might work with models which are not listed in this table.
> - Gated models require authentication with Hugging Face token (HF_TOKEN).
> - Estimated memory assumes FP16 precision. Actual memory usage may vary based on implementation and overhead.
> - Memory can be further reduced using quantization techniques covered in the exercises.


## Community

Connect with us across platforms:

[![Website](https://img.shields.io/badge/Pruna.ai-purple?style=flat-square)](https://pruna.ai)
[![X/Twitter](https://img.shields.io/twitter/url?url=https%3A%2F%2Fx.com%2FPrunaAI)](https://x.com/PrunaAI)
[![Dev.to](https://img.shields.io/badge/dev-to-black?style=flat-square)](https://dev.to/pruna-ai)
[![Reddit](https://img.shields.io/badge/Follow-r%2FPrunaAI-orange?style=social)](https://reddit.com/r/PrunaAI)
[![Discord](https://img.shields.io/badge/Discord-join_us-purple?style=flat-square)](https://discord.gg/JFQmtFKCjd)
[![Hugging Face](https://img.shields.io/badge/Huggingface-models-yellow?style=flat-square)](https://huggingface.co/prunaai)
[![Replicate](https://img.shields.io/badge/replicate-black?style=flat-square)](https://replicate.com/prunaai)

## Resources

You can find the main resources in the [Awesome AI efficiency](https://github.com/PrunaAI/awesome-ai-efficiency) repository. It includes complete reference including:
- Facts 📊
- Tools 🛠️
- News Articles 📰
- Reports 📈
- Research Articles 📄
- Blogs 📰
- Books 📚
- Lectures 🎓
- People 🧑‍💻
- Organizations 🌍


⭐ **Support the Project**: If you find these resources valuable, please star this repository and the [Awesome AI efficiency](https://github.com/PrunaAI/awesome-ai-efficiency) collection!
