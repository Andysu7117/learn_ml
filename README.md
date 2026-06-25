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

## AI Agents

#### Security Risks
- Data leakage and privacy exposure
- Prompt injection and manipulation attacks
- Unauthorized access and privilege escalation
- Data poisoning
- Supply Chain vulnerabilities
- Over-reliance on autonomous actions
- Inadequate auditability and logging
- Model Inversion and output leakage

#### Mitigation Strategies
- Enforcing role-based access controls (RBAC) and least privilege permissions
- Adding prompt filtering and validation layers to prevent injection attacks
- Sandboxing or gating sensitive operations behind human-in-the-loop approvals
- Maintaining comprehensive logging and traceability for all agent actions
- Auditing third-party dependencies and integrations regularly
- Continuously retraining and validating models to detect data drift or poisoning attempts

#### Agent types on Microsoft Foundry
- Declarrative Agents: agents defined through configuration rather than code
    - Prompt-based agents: a single agent configured with a model, instructions, tools, and prompts. Most common type of agent
    - Workflow agents: multi-agent orchestrations defined in YAML, enabling complex scenarios where multiple agents collaborate to complete tasks
- Hosted Agents: ontainerized agents that are created and deployed in code, then hosted by the foundry platform. Hosted agents give you full control over agent logic and execution while the platform manages infrastructure.

#### Features of Microsoft Foundry Agent Service
- Automatic tool calling - The service handles the entire tool-calling lifecycle, including running the model, invoking tools, and returning results. This eliminates complex integration code.

- Securely managed data - Conversation states are securely managed through the Responses API, removing the need for manual state management.

- Extensive tool catalog - A rich set of built-in and community tools extends agent capabilities beyond text generation, including code execution, file search, web search, and integrations with Azure services and external APIs.

- Model selection - Choose from various AI models to match your performance and cost requirements.

- Enterprise-grade security - The service ensures data privacy and compliance with secure data handling, keyless authentication, and built-in content safety filters.

- Customizable storage solutions - Use platform-managed storage or bring your own Azure Blob storage for full visibility and control.

- Observability and tracing - Built-in monitoring capabilities help you track agent behavior, debug issues, and optimize performance in production.

#### When to use the Foundry Portal
- Quick prototyping - Rapidly test agent concepts and configurations without setting up development environments
- Visual configuration - Configure agents through intuitive forms and dropdowns rather than code
- Centralized management - View and manage all agents across projects in one place
- Team collaboration - Share agent configurations with stakeholders who prefer visual interfaces
- Resource oversight - Monitor token usage, latency, and evaluation outcomes through dashboards

#### When to use Visual Studio Code Extention
- Developer-centric workflows - Build agents alongside your application code in a single environment
- Version control integration - Track agent configurations in Git alongside your codebase
- Rapid iteration - Make quick changes and test immediately without switching tools
- Code-first development - Edit YAML configurations directly for precise control
- Local development - Work on agent designs offline before deploying to Azure

#### Typical Development Workflow
1. Connect to your Microsoft Foundry project
2. Create an AI agent in the Foundry portal with a descriptive name and purpose
3. Configure agent instructions defining its behavior and capabilities (in the portal or VS Code)
4. Add tools to extend what the agent can do
5. Test the agent using integrated playgrounds
5. Iterate on the design based on test results
6. Deploy the agent to production
7. Integrate the agent into your applications

#### Testing Strategies
- Happy path testing - Verify the agent handles common, expected requests correctly.
- Edge case testing - Try ambiguous inputs, incomplete information, and unusual requests to reveal how agents handle uncertainty.
- Boundary testing - Confirm the agent respects boundaries defined in its instructions by testing out-of-scope requests.
- Multi-turn conversation testing - Verify the agent maintains context across multiple exchanges and builds on previous responses.
- Tool invocation testing - Verify agents call the right tools at the right times and incorporate results correctly.

## Rag

#### What to test?
- Straightforward Factual
    - example questions - what is our vacation policy?, where can I find the security guidelines
    - Expected behaviour - direct retrieval with citations
- Questions requiring synthesis
    - example questions - what are the differences between our leave types?, how do I request time off?
    - expected behaviour - multiple document retrieval, synthesized answer with multiple citations
- Questions outside knowledge base
    - example questions - what's the weather like today?, tell me about machine learning
    - expected behaviour - gracefull fallback ("I don't have that information")
- Ambiguous questions
    - example questions - what about benefits?, tell me more about that
    - expected behaviour - clarifying questions or focused search on most relevant topic

#### Moving from testing to production
Patterns that need to be traced
- Citation frequency - Are agents consistently citing sources?
- Fallback frequency - How often do agents say "I don't know"?
- Query types - What categories of questions appear most often?
- Retrieval accuracy - Do retrieved documents actually contain answers?

## Terminology
- Training set: data used to train model
- Feature: the input variable, x the input variable, y the output variable, m the number of training examples

