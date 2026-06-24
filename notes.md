# Notes

## Supervised and Unsupervised Learning

### Supervised Learning
- Algorithms that learn input to output maps
- learns from being given "right answers" x -> y

#### Regression
- Logistical Regression -> result is a percentage between 0-1
- Linear Regression -> result is a numerical value

#### Classification
- Binary Classification -> outputs 0 or 1 (true or false)
- Multiclass Classification -> predicts based on a set of multiple classes

### Unsupervised Learning
Finding relationships with the learning -> find something interesting in unlabeled data -> there is no answer/y for features

#### Clustering
- groups similarities between observations based on features into discrete clusters

#### Anomaly Detection
- Find unusual datapoints

#### Dimensionality Reduction
- Compress data using fewer numbers

## Optimisation

#### When to use Prompt Engineering
- Guide the model's tone, format, and behavior.
- Provide specific instructions for a task.
- Quickly iterate on results without infrastructure changes.
- Keep costs low, as no additional training or data storage is required.

#### When to use RAG
- The model needs domain-specific knowledge: Your organization has private data that the model wasn't trained on, like a product catalog, policy documents, or internal knowledge base.
- Information changes frequently: Your data is updated regularly, such as inventory, pricing, or news. RAG retrieves current data at query time without retraining.
- Factual accuracy is critical: You need responses grounded in real data rather than the model's general knowledge.
- The base model's training data has a cutoff: Events or information that occurred after the model's training cutoff date need to be accessible.

#### Fine-tuning
Fine tuning techniques:
- Supervised fine-tuning (SFT): Train the model on a labeled dataset of prompt-and-response pairs. The model learns to produce outputs that match the patterns in your training data. This technique works best when there are clear, well-defined ways to approach a task.
- Reinforcement fine-tuning (RFT): Optimize the model's behavior through iterative feedback, using a grader to reward better responses incrementally. RFT works well for complex or dynamic tasks where there are many possible solutions and you want to improve the model's reasoning quality.
- Direct Preference Optimization (DPO): Align the model based on human preferences by providing preferred and non-preferred response pairs. DPO is computationally lighter than traditional reinforcement learning approaches while being equally effective at alignment.

#### Fine-tuning costs and challenges
- Training costs: Fine-tuning has upfront costs for training and ongoing hourly costs for hosting the custom model.
- Data quality requirements: Poor-quality or unrepresentative training data leads to overfitting, underfitting, or bias.
- Maintenance: Fine-tuned models may need to be retrained when data changes or when updated base models are released.
- Experimentation: Finding the right combination of hyperparameters (epochs, batch size, learning rate) requires testing and iteration.
- Model drift: Specializing too narrowly can make the model less effective at general language tasks outside the fine-tuned domain.

#### When to Fine-tune
- Consistent style and tone: Your organization has a specific brand voice, and the model needs to follow it reliably across all interactions. For example, the travel agency wants every response to use a warm, encouraging tone with short paragraphs.
- Specific output formats: You need the model to reliably produce structured output, like JSON responses following a defined schema, and few-shot examples alone aren't sufficient.
- Reducing prompt length: Long system messages with many examples consume tokens and increase latency. Fine-tuning embeds those patterns into the model, reducing the prompt size needed for each request.
- Distillation: You want to transfer the capabilities of a large, expensive model to a smaller, more efficient one. For example, you can collect outputs from a high-performing model and use them to fine-tune a smaller model that achieves similar quality at lower cost and latency.
- Enhancing tool usage: When your application uses tool calling, fine-tuning with tool examples can improve the accuracy of tool selection and parameter generation.

#### Strategy Comparison
Strategy : Time to implement : Complexity : Cost : Best for
Prompt Engineering : Low : Low : Low (per-token only) : Guiding tone, format, and behavior; quick iteration; providing instructions and examples

RAG : Medium : Medium : Medium (search infrastructure + storage + per-token) : Factual accuracy, domain-specific knowledge, dynamic or frequently changing data

Fine-tuning : High : High : High (training compute + model hosting + per-token) : Behavioral consistency, style enforcement, reducing prompt length, model distillation

#### Trade offs
Prompt Engineering: Prompt engineering is the quickest and least expensive optimization strategy. You can start immediately without any infrastructure changes. However, longer prompts consume more tokens per request, and the model might not always follow complex instructions consistently. Prompt engineering also can't give the model access to information it wasn't trained on.

RAG: RAG provides the model with up-to-date, relevant data at query time, which significantly improves factual accuracy. However, it requires setting up a search service, creating and maintaining an index, and processing embeddings. The quality of RAG responses depends on the quality of your search index and how well your data is chunked and indexed.

Fine-tuning: Fine-tuning produces the most consistent model behavior because the desired patterns are embedded in the model's weights. It can also reduce per-request costs by shortening prompts. However, fine-tuning has the highest upfront investment: you need to prepare training data, pay for training compute, and host the custom model. The fine-tuned model may also need to be retrained when the base model is updated or when your requirements change.

#### Decision Framework
1. Start with prompt engineering: Test system messages, few-shot examples, and parameter tuning. Evaluate whether the results meet your requirements.
2. Add RAG if accuracy matters: If the model needs access to specific, current, or private data to answer correctly, implement RAG with Azure AI Search.
3. Add fine-tuning if consistency matters: If the model doesn't reliably maintain the desired style, tone, or format despite detailed prompts, fine-tune the model with representative examples.
4. Combine as needed: Layer strategies based on your application's specific requirements. Not every application needs all three.

## Terminology
- Training set: data used to train model
- Feature: the input variable, x the input variable, y the output variable, m the number of training examples

