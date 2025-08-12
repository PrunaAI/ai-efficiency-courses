# 🗂️ Final Challenge

Now that you have learned about the different aspects of building with efficiency in mind, we propose you to pick a final challenge where you can apply all the knowledge you have gained during the course.

In this section, we will present you four different projects with a central theme. Guess it? Efficiency, of course, in a real-world case.

Before you start, check the following pointers:

- The challenges are **unsupervised**. So, we are not providing you with an official solution. You are free to experiment, explore and be as creative as you want. The is no right or wrong way to complete the challenge.

- We recommend you to **select a challenge you are genuinely interested in**. If you are unsure where to begin, check the provided tools and resources. You can start with the easiest level first and then develop the more advanced features.

- Reach out to the **[Discord community](https://discord.com/invite/Tun8YgzxZ9)**. If you are stuck, we will be happy to discuss your ideas and help you get started. If you have completed the challenge, we would be excited to see and share your project.


## Pick your challenge

> 💡 Pro Tip
>
> Smash your model using Pruna and integrate it in your project.
> Don't hesitate to check the [Pruna documentation](https://docs.pruna.ai/en/stable/index.html) to get the most out of it.

### 1. **Build your Own Efficient Chatbot**

> 🎯 Goal
>
> Design an optimized chatbot powered by an LLM that can answer questions.

#### Description

Build a chatbot that can go beyond basic question answering and respond faster.

- Use an optimized LLM, to which you have applied at least one compression technique.
- Integrate a database to retrieve and store relevant information.
- Include a basic UI or API endpoint for interaction
- **Advanced:** Implement multi-turn interactions with context awareness or multi-modality.

#### Tools and Resources

- Models: [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)
- Frameworks: [LangChain](https://python.langchain.com/docs/tutorials/chatbot/), [LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/putting_it_all_together/chatbots/building_a_chatbot/), Haystack
- Databases: [Weaviate](https://docs.weaviate.io/weaviate/recipes/multi-vector-colipali-rag), FAISS, Chroma, Qdrant
- UI Frameworks: [Gradio](https://www.gradio.app/guides/creating-a-chatbot-fast), Streamlit

#### Example Use Cases

- Customer support bot for a fictional company
- Study buddy that answers questions from lecture notes
- Travel assistant that remembers user preferences

### 2. **Build a Synthetic Data Pipeline**

> 🎯 Goal
>
> Design and implement an efficient pipeline to generate high-quality synthetic data.

#### Description

Build an automated synthetic data pipeline with optimized and fast inference that can be useful to tackle the data scarcity problem in a specific domain.

- Choose an optimized LLM, to which you have applied at least one compression technique.
- Include seed data input and hyperparameter tuning to control data diversity and quality.
- Enable saving and exporting the generated datasets for reuse and evaluation.
- **Advanced:** Add a data validation step to ensure the quality of the generated data, or fine-tune your own model with the generated data.

#### Tools and Resources

- Models: [HF Transformers](https://huggingface.co/docs/transformers/index), [HF Diffusers](https://huggingface.co/docs/diffusers/index)
- Frameworks: [Outlines](https://dottxt-ai.github.io/outlines/latest/examples/qa-with-citations/), LangChain, Haystack
-Data validation: [Ultrafeedback](https://arxiv.org/abs/2310.01377), [PrometheusEval](https://arxiv.org/abs/2405.01535), [LLM-as-a-judge](https://arxiv.org/abs/2411.15594)

#### Example Use Cases

- Generate data for low-resource languages or niche domains lacking data.
- Create healthcare patient anonymized records for training a model to detect medical conditions.
- Generate images for a fake news detection model.

### 3. **Make a Consumer GPUs Deployment**

> 🎯 Goal
>
> Design and make an efficient deployment to run your model on a consumer GPU for inference.

#### Description

Create a deployment of an optimized model that allows to run local, affordable consumer hardware with minimal latency and reasonable memory usage.

- Select an optimized LLM, to which you have applied at least one compression technique.
- Provide a user-friendly way for running the deployment locally.
- Optimize the build so others can replicate it on their own hardware.
- **Advanced:** Build cross-platform support for running the deployment on different operating systems.

#### Tools and Resources

- Models: [HF Transformers](https://huggingface.co/docs/transformers/index), [HF Diffusers](https://huggingface.co/docs/diffusers/index)
- Deployment: [Docker](https://docs.docker.com/get-started/), [FastAPI](https://fastapi.tiangolo.com/)
- Consumer GPUs: RTX 3060/3070/3080/4060, M1/M2/M3

#### Example Use Cases

- Real-time object detection system for a webcam.
- Offline transcription of speech to text.
- Local video summarization.

### 4. **Maximize Inference Throughtput**

> 🎯 Goal
>
> Deploy an optimized model to maximize the number of inferences at the lowest possible cost, while maintainig the output quality.

#### Description

Optimize a model to serve more inferences per dollar without compromising quality.

- Pick an optimized LLM, to which you have applied at least one compression technique
- Benchmark the performance of the model before and after the optimizations.
- Deploy the model in the cloud.
- **Advanced:** Set a threshold to achive based on the current market prices.

#### Tools and Resources

- Models: [HF Transformers](https://huggingface.co/docs/transformers/index), [HF Diffusers](https://huggingface.co/docs/diffusers/index)
- Deployment: [Gradio](https://www.gradio.app), [HF Spaces](https://huggingface.co/spaces), [LitServe](https://lightning.ai/docs/litserve/home/get-started), [BentoML](https://docs.bentoml.com/en/latest/get-started/cloud-deployment.html)

#### Example Use Cases

- A text-generation API with thousands of concurrent users.
- An image editing service.