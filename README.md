# Efficient AI - Courses

A comprehensive learning path for building, compressing, evaluating, and deploying efficient AI models. From fundamentals to advanced techniques, this course combines theoretical knowledge with practical exercises. Perfect for students, engineers, and researchers looking to master efficient AI development.

## Quick Links

- [📚 Lectures](#lectures) - Comprehensive slides and materials
- [💻 Exercises](#exercises) - Hands-on coding practice
- [📖 References](#references) - Curated resources and papers
- [⚙️ Setup](#setup) - Environment configuration
- [🤝 Community](#community) - Connect with other learners

## Lectures

The lecture content is based on multiple sources (incl. papers, books, and lectures).
You can find the main sources in the [Awesome AI efficiency](https://github.com/PrunaAI/awesome-ai-efficiency) repository.
If you find it helpful, please ⭐ star the repository!

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

| Exercise | Description | Exercise Notebook | Solution Notebook |
|----------|-------------|-------------------|-------------------|
| **Core Exercises** | | | |
| 🔍 Analyze LLM architectures | Study model design patterns and optimization techniques | [notebook](exercises/01-analyze_llm_architectures.ipynb) | [solution](solutions/01-analyze_llm_architectures.ipynb) |
| 📊 Measure LLM efficiency | Evaluate model performance and resource usage | [notebook](exercises/02-measure_llm_efficiency.ipynb) | [solution](solutions/02-measure_llm_efficiency.ipynb) |
| ⚖️ Run LLM on CPU vs GPU | Compare usage of CPU and GPU for LLM inference | [notebook](exercises/03-run_llm_cpu_vs_gpu.ipynb) | [solution](solutions/03-run_llm_cpu_vs_gpu.ipynb) |
| 🔢 Benchmark LLM Quantization methods | Analyze impact of different quantization methods | [notebook](exercises/04-benchmark_llm_quantization_methods.ipynb) | [solution](solutions/04-benchmark_llm_quantization_methods.ipynb) |
| **Advanced Topics** | | | |
| 🚀 Benchmark LLM bit precision | Analyze impact of different bit precisions | [notebook](exercises/05-benchmark_llm_bits.ipynb) | [solution](solutions/05-benchmark_llm_bits.ipynb) |
| 📈 Use data during quantization | Leverage calibration data for better quantization | [notebook](exercises/06-use_data_llm_quantization.ipynb) | [solution](solutions/06-use_data_llm_quantization.ipynb) |
| 🎯 Finetune compressed models | Adapt quantized models for specific tasks | [notebook](exercises/07-finetune_llm.ipynb) | [solution](solutions/07-finetune_llm.ipynb) |

## Setup

You can easily setup your coding environment. In particular, most exercises are based on the `pruna` package for productive exploration of efficient AI topics.
Further, some exercises require the `pruna_pro` package to address more advanced topics.

1. **Environment Setup**
   ```bash
   bash setup_exercises.sh
   ```
2. **Hugging Face Integration**
   - Set your `HF_TOKEN`
   - Configure cache directory
   - Install required packages:
     - `pruna` (core package)
     - `pruna_pro` (advanced features)

### Hardware Requirements

- **Minimum**: Modest GPU (1080, 2080)
- **Recommended**: High-end GPU (V100, A100)
- **Note**: Exercises are optimized for accessibility

## Community

Connect with us across platforms:

[![Website](https://img.shields.io/badge/Pruna.ai-purple?style=flat-square)](https://pruna.ai)
[![X/Twitter](https://img.shields.io/twitter/url?url=https%3A%2F%2Fx.com%2FPrunaAI)](https://x.com/PrunaAI)
[![Dev.to](https://img.shields.io/badge/dev-to-black?style=flat-square)](https://dev.to/prunaai)
[![Reddit](https://img.shields.io/badge/Follow-r%2FPrunaAI-orange?style=social)](https://reddit.com/r/PrunaAI)
[![Discord](https://img.shields.io/badge/Discord-join_us-purple?style=flat-square)](https://discord.gg/prunaai)
[![Hugging Face](https://img.shields.io/badge/Huggingface-models-yellow?style=flat-square)](https://huggingface.co/prunaai)
[![Replicate](https://img.shields.io/badge/replicate-black?style=flat-square)](https://replicate.com/prunaai)

⭐ **Support the Project**: If you find these resources valuable, please star this repository and the [Awesome AI efficiency](https://github.com/PrunaAI/awesome-ai-efficiency) collection!
