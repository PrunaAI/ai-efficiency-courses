# 🗂️ Final Challenge

Now that you have learned about the different aspects of building with efficiency in mind, we propose you to pick a final challenge where you can apply all the knowledge you have gained during the course.

In this section, we will present you four different projects with a central theme. Guess it? Efficiency, of course, in a real-world case.

Before you start, check the following pointers:

- The challenges are **unsupervised**. So, we are not providing you with an official solution. You are free to experiment, explore and be as creative as you want. There is no right or wrong way to complete the challenge.

- We recommend you to **select a challenge you are genuinely interested in**. If you are unsure where to begin, check the provided tools and resources. You can start with the easiest level first and then develop the more advanced features.

- Reach out to the **[Discord community](https://discord.com/invite/Tun8YgzxZ9)**. If you are stuck, we will be happy to discuss your ideas and help you get started. If you have completed the challenge, we would be excited to see and share your project.

- Publish your project **open-source and share** it with the community. We will be happy to reshare on socials!

## Pick your challenge

> 💡 Use Pruna for any compression task
>
> Smash your model using Pruna and integrate it in your project.
> Don't hesitate to check the [Pruna documentation](https://docs.pruna.ai/en/stable/index.html) to get the most out of it.

### 1. **Build your Own Efficient Chatbot**

> 🎯 Goal
>
> Hack an LLM-powered chatbot that delivers lightning-fast answers — smarter, sharper, cooler.

#### Description

Build a chatbot that can go beyond basic question answering and respond faster to make it faster for better user experience or smaller to run locally.

- Use an optimized LLM, to which you have applied at least one compression technique.
- Integrate a database to retrieve and store relevant information, and remember past iteractions.
- Include a basic UI or API endpoint for interaction
- **Advanced:** Implement multi-turn interactions with context awareness or multi-modality.

#### Tools and Resources

- Models: [Hugging Face Transformers](https://huggingface.co/models?pipeline_tag=text-generation&library=transformers&sort=trending)
- Frameworks: [LangChain](https://python.langchain.com/docs/tutorials/chatbot/), [LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/putting_it_all_together/chatbots/building_a_chatbot/), [Haystack](https://haystack.deepset.ai/tutorials/40_building_chat_application_with_function_calling)
- UI Frameworks: [Gradio](https://www.gradio.app/guides/creating-a-chatbot-fast), [Streamlit](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps)

#### Example Use Cases

Think beyond simple Q&A and your bot can make things more interesting. Here are some fun ways to use it:

- Customer support bot for a fictional company
- Study buddy that answers questions from lecture notes
- Travel assistant that remembers user preferences

### 2. **Build a Synthetic Data Pipeline**

> 🎯 Goal
>
> Supercharge AI projects with a pipeline that delivers high-quality synthetic data in record time.

#### Description

Synthetic data generation is a powerful tool to overcome the challenges of scarce, sensitive, or costly data collection, while being able to control the quality and diversity of the data.
By simulating real-world data, you can accelerate model development, protect privacy, and unlock edge cases that are hard to capture in reality.
In this case, your task will be to build an automated synthetic data pipeline with optimized and fast inference that can be useful to tackle the data scarcity problem in a specific domain.

- Choose an optimized model, to which you have applied at least one compression technique.
- Include seed data input and hyperparameter tuning to control data diversity and quality.
- Enable saving and exporting the generated datasets to HF for reuse and evaluation.
- **Advanced:** Add a data validation step to ensure the quality of the generated data, or fine-tune your own model with the generated data and publish it on Replicate.

#### Tools and Resources

- Models: [HF Transformers](https://huggingface.co/models?library=transformers&sort=trending), [HF Diffusers](https://huggingface.co/models?library=diffusers&sort=trending)
- Frameworks: [Outlines](https://dottxt-ai.github.io/outlines/latest/examples/qa-with-citations/), [LangChain](https://python.langchain.com/api_reference/experimental/tabular_synthetic_data/langchain_experimental.tabular_synthetic_data.base.SyntheticDataGenerator.html), [Haystack](https://haystack.deepset.ai/tutorials/28_structured_output_with_loop)
-Data validation: [Ultrafeedback](https://github.com/OpenBMB/UltraFeedback/blob/main/src/comparison_data_generation/main.py), [PrometheusEval](hhttps://github.com/prometheus-eval/prometheus-eval/blob/main/scripts/example_absolute.py)

#### Example Use Cases

Why stay stuck in data scarcity when you can generate exactly what you need? Take control and see what you can achieve:

- Generate data for low-resource languages or niche domains lacking data.
- Create images of objects under various conditions and from multipleangles for object detection.
- Generate news articles for a fake news detection model.

### 3. **Deploy an AI Model on a Consumer GPU**

> 🎯 Goal
>
> Democratize AI by making model inference lightning-fast on consumer GPUs.

#### Description

Build a deployment of an optimized AI model that runs efficiently on local, affordable consumer hardware with minimal latency and manageable memory usage. Instead of relying only on ready-made inference engines like llamacpp or vllm, explore creating a custom deployment pipeline to apply custom compression or quaantization methods or integrate with other inference engines.

- Select an optimized model, to which you have applied at least one compression technique.
- Provide a user-friendly way for running the deployment locally.
- Optimize the build so others can replicate it on their own hardware.
- **Advanced:** Build cross-platform support for running the deployment on different operating systems.

#### Tools and Resources

- Models: [HF Transformers](https://huggingface.co/models?library=transformers&sort=trending), [HF Diffusers](https://huggingface.co/models?library=diffusers&sort=trending)
- Deployment: [Docker](https://docs.docker.com/get-started/), [FastAPI](https://fastapi.tiangolo.com/)
- Consumer GPUs: RTX 3060/3070/3080/4060

#### Example Use Cases

Unlocks creative, private, and low-latency applications without relying on expensive cloud services. Some possibilities include:

- Offline transcription of speech to text.
- Local video summarization.
- Code assistant that can run code locally.
- Image generation and editing.

### 4. **Generate Video and Audio in Real-time**

> 🎯 Goal
>
> Bring generative AI to life: real-time video and audio with high quality and low latency.

#### Description

Develop a real-time video and audio generation pipeline that can be used to create videos and audio in real-time.

- Pick an optimized model, to which you have applied at least one compression technique
- Benchmark the performance of the model before and after the optimizations.
- Deploy the model in the cloud.
- **Advanced:** Add a live UI to interact with the model.

#### Tools and Resources

- Models: [HF Transformers](https://huggingface.co/models?library=transformers&sort=trending), [HF Diffusers](https://huggingface.co/models?library=diffusers&sort=trending)
- Deployment: [Gradio](https://www.gradio.app), [HF Spaces](https://huggingface.co/spaces), [LitServe](https://lightning.ai/docs/litserve/home/get-started), [BentoML](https://docs.bentoml.com/en/latest/get-started/cloud-deployment.html)

#### Example Use Cases

Open the door to interactive and more immersive experiences. Some possibilities include:

- Real-time voice synthesis for accessibility tools.
- An avatar that can speak and interact with the user for education or entertainment.