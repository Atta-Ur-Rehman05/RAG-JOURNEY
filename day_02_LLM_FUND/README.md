🧠 RAG — Day 2
How Large Language Models Work & Prompt Engineering

RAG Learning Journey · Day 2
Understanding how LLMs generate text, how sampling controls their behavior, how context windows work, and how to design reliable prompts.

📚 What You'll Learn

This day focuses on two major foundations of modern AI applications:

🧠 How Large Language Models work
✍️ How to engineer effective prompts

By the end of this day, you should understand:

How text becomes tokens
How tokens become embeddings
How Transformers process context
How next-token prediction generates responses
How probabilities and sampling work
What temperature, top_p, and top_k do
How context windows and token budgets work
The difference between input and output tokens
Zero-shot, one-shot, and many-shot prompting
Persona-based prompting
Chain-of-thought prompting
Structured outputs
How to combine multiple prompting techniques
How prompting decisions affect RAG systems
🗂️ Table of Contents
How an LLM Works
Input
Tokens
Embeddings
Transformer
Probabilities
Pick a Token
Repeat
How the Model Learned
Temperature, top_p and top_k
Temperature
top_p / Nucleus Sampling
top_k
Weighted Random Draw
Choosing Values
Context Window and Tokens
Input Tokens
Output Tokens
Token Budget
Why Bigger Context Isn't Always Better
Prompt Types
Shared Setup
Zero-Shot
One-Shot
Many-Shot
Persona-Based
Chain of Thought
Structured Output
Combining Prompt Types
Persona + Structured Output
CoT + Structured Output
Many-Shot + Structured Output
CoT + Many-Shot + Structured
All Four Combined
Quick Reference
Prompt Design Checklist
Key Takeaways
1. How an LLM Works

A Large Language Model (LLM) is a neural network trained to predict the next token based on the tokens that came before it.

This simple operation is repeated again and again to produce:

Answers
Code
Summaries
Conversations
Reasoning
Structured data
🔄 Simplified Generation Pipeline
User Input
    ↓
Tokenization
    ↓
Token IDs
    ↓
Embeddings
    ↓
Transformer Layers
    ↓
Logits / Scores
    ↓
Probabilities
    ↓
Sampling
    ↓
Next Token
    ↓
Append Token
    ↓
Repeat
    ↓
Final Response

The model continues generating tokens until:

It produces an end-of-sequence token, or
The maximum output limit is reached.
Example
Prompt:
"Write one short sentence about the sky."

Generated response:
"The sky is blue."

The model does not generate the entire sentence at once.

It approximately performs:

The
   ↓
The sky
   ↓
The sky is
   ↓
The sky is blue
   ↓
The sky is blue.

Each newly generated token becomes part of the context for the next prediction.

1.1 Input

The model's input is everything provided for that request, not merely the user's latest message.

A typical request may contain:

System Prompt
+
Conversation History
+
Retrieved Documents
+
Tool Definitions
+
Tool Results
+
User Message

The model ultimately processes these as one token sequence.

Simplified representation
<system>
You are a helpful assistant.

<user>
Write one short sentence about the sky.

<model>
The model starts generating here...

This is particularly important for RAG because retrieved documents become part of the model's input context.

1.2 Tokens

LLMs do not directly process words or characters.

They process tokens.

A token can be:

A complete word
Part of a word
Punctuation
A space-prefixed word piece
Numbers
Code fragments

Example:

"Write one short sentence about the sky."

May be split conceptually into:

Write
one
short
sentence
about
the
sky
.

Each token maps to an integer ID from the model's vocabulary.

Important

Token count—not word count—drives model cost and context-window usage.

The exact tokenization depends on the model.

Generally:

Common English text → fewer tokens
Rare words → potentially more tokens
Code → potentially more tokens
Numbers → potentially more tokens
Non-English languages → potentially more tokens

This is one reason token awareness is important when building RAG systems.

1.3 Embeddings

After tokenization, token IDs are converted into vectors using an embedding table learned during training.

Conceptually:

Token
  ↓
Token ID
  ↓
Embedding Lookup
  ↓
Vector

Example:

"sky"
   ↓
[0.12, -0.48, 0.91, 0.07, ...]

These vectors contain learned representations that allow the network to process relationships between tokens.

Tokens with related meanings can develop similar representations.

For example:

sky
cloud
weather

may have representations that capture meaningful relationships.

Positional Information

A Transformer also needs information about token position.

For example:

"The dog chased the cat."

is different from:

"The cat chased the dog."

Therefore, positional information is incorporated so the model can distinguish token order.

1.4 Transformer

The vectors are passed through multiple Transformer layers.

The two major components emphasized in the PDF are:

1. Self-Attention

Self-attention allows tokens to consider other tokens when building their representations.

Conceptually:

Token A ─────┐
Token B ─────┼──→ Attention
Token C ─────┤
Token D ─────┘

Different attention heads can focus on different relationships such as:

Grammar
References
Topics
Relationships between words
2. Feed-Forward Network

After attention, the token representations are processed further through a feed-forward network.

Simplified Transformer layer:

Token Embeddings + Positions
            ↓
      Self-Attention
            ↓
      Add & Normalize
            ↓
   Feed-Forward Network
            ↓
      Add & Normalize
            ↓
       Next Layer

This happens across a stack of Transformer layers.

Eventually, the final representation is converted into scores for possible next tokens.

1.5 Probabilities

The model produces a raw score, called a logit, for every token in its vocabulary.

Conceptually:

Final Vector
     ↓
Logits
     ↓
Softmax
     ↓
Probabilities

Example:

Candidate	Probability
blue	60%
clear	25%
gray	10%
green	5%

The probabilities sum to approximately:

100%

The model can then use these probabilities to decide which token to generate next.

1.6 Pick a Token

The model selects one token from the probability distribution.

For example:

blue   → 60%
clear  → 25%
gray   → 10%
green  → 5%

A weighted random draw might select:

blue

But it could also select:

clear

even though blue has the highest probability.

Greedy Decoding

At temperature 0, the process is treated as greedy decoding:

Always choose the highest-probability token.

This favors deterministic behavior.

1.7 Repeat

After selecting a token, the model appends it to the sequence and runs the generation process again.

Prompt
  ↓
Predict token
  ↓
Append token
  ↓
Predict next token
  ↓
Append token
  ↓
Repeat...

This is called autoregressive generation.

Every generated token becomes part of the context used to generate the next token.

Generation stops when:

An end-of-sequence token is produced, or
The maximum output length is reached.
Prefill and Decode

Serving can be viewed as two phases:

Prefill

The model processes the input prompt.

Decode

The model generates output tokens one at a time.

A KV cache stores earlier attention results so they do not need to be recomputed from scratch during every decoding step.

This is also why long prompts can increase latency.

1.8 How the Model Learned

The PDF describes several stages involved in training modern language models.

Stage	What Happens	Result
Pre-training	Predict next tokens over a huge corpus	Language ability + broad knowledge
Supervised Fine-Tuning	Train on instruction/response pairs	Better instruction following
Preference Tuning	Humans/models rank responses	More helpful, safer, better-formatted outputs
Reasoning Training	Reinforcement learning on checkable tasks	Models capable of additional reasoning behavior
Why This Matters for RAG

LLMs can produce fluent but false information.

They also have a knowledge cutoff determined by their training.

RAG helps address these limitations by retrieving relevant information and placing it into the model's input context.

User Question
      ↓
Retrieve Relevant Documents
      ↓
Add Documents to Context
      ↓
LLM
      ↓
Grounded Response
2. Temperature, top_p and top_k

Three important controls affect the token selection/sampling stage:

temperature
top_p
top_k

A simplified sampling pipeline:

Logits
  ↓
Temperature
  ↓
Softmax
  ↓
top_k
  ↓
top_p
  ↓
Renormalize
  ↓
Weighted Random Draw
  ↓
Selected Token

The exact behavior can vary by model/provider, so always check the documentation for the model being used.

2.1 Temperature

Temperature controls how concentrated or spread out the probability distribution becomes.

Conceptually:

probabilities = softmax(logits / T)
Low Temperature
T < 1

Makes the distribution sharper.

The highest-probability token becomes more dominant.

Useful for:

Classification
Extraction
Rule-based decisions
Consistent outputs
Temperature = 1
T = 1

Preserves the model's natural probability distribution.

High Temperature
T > 1

Flattens the distribution.

Lower-probability tokens have more opportunity to be selected.

Useful for:

Brainstorming
Creative writing
Diverse generation
Simplified intuition
Low temperature
→ Focused
→ Predictable
→ Less variation

High temperature
→ Diverse
→ More variation
→ More surprising outputs
2.2 top_p — Nucleus Sampling

top_p keeps the smallest set of tokens whose cumulative probability reaches p.

Example:

blue   60%
clear  25%
gray   10%
green   5%

With:

top_p = 0.90

We accumulate:

blue                → 60%
blue + clear        → 85%
blue + clear + gray → 95%

Therefore:

blue
clear
gray

are retained, while:

green

is removed.

The remaining probabilities are then renormalized.

Important

top_p represents a cumulative probability threshold, not the probability of one individual token.

2.3 top_k

top_k keeps a fixed number of the most likely tokens.

Example:

blue   60%
clear  25%
gray   10%
green   5%

With:

top_k = 2

Only:

blue
clear

survive.

Their probabilities are then renormalized.

top_k vs top_p

	top_k	top_p
Selection	Fixed number	Cumulative probability
Menu size	Always k	Changes with confidence
Adapts to confidence	❌	✅
Typical values	20–64	0.8–0.95

When both are used, they act as stacked filters.

2.4 Weighted Random Draw

After filtering and renormalization, the remaining probabilities form a probability distribution.

Imagine a number line:

0 ------------------------------------------- 1
|-------------|-----------|------------------|
     blue          clear          gray
     63.2%         26.3%         10.5%

A random number is generated.

The token whose probability region contains that number is selected.

This explains why the same prompt can sometimes produce different outputs.

Seed

A seed can make the random process more repeatable on a best-effort basis, depending on the provider/model.

2.5 Choosing Values

The PDF provides these practical starting points:

Task	Temperature	top_p	Goal
Classification / extraction / triage	0–0.2	Default	Consistency
Rule-based decisions	0–0.2	Default	Fewer slips
Chat persona	0.4–0.7	0.9–0.95	Natural variation
Brainstorming / creative writing	0.8–1.2	0.95	Diversity
Important Rule

Tune one randomness control at a time.

Also, sampling parameters are not universal across providers.

For example:

temperature → commonly available
top_p → commonly available
top_k → provider/model dependent

Always check the exact API documentation for your selected model.

3. Context Window and Tokens

The context window is the maximum number of tokens a model can process in a single request.

Think of it as the model's working memory.

┌──────────────────────────────────────┐
│          CONTEXT WINDOW              │
│                                      │
│ System Prompt                        │
│ Few-Shot Examples                    │
│ Chat History                         │
│ Retrieved Documents                  │
│ User Message                         │
│                                      │
│ Thinking / Output                    │
│ Visible Answer                       │
└──────────────────────────────────────┘
Critical Principle

Input and output share the same context window.

3.1 Input Tokens

Input tokens can include:

System prompt
Few-shot examples
Conversation history
Retrieved documents
Tool definitions
Tool results
Current user message

In a stateless API, a chat application generally resends the relevant conversation history with each request.

Therefore:

More conversation
       ↓
More input tokens
       ↓
More cost + latency

For RAG:

User Question
      +
Retrieved Chunks
      +
System Prompt
      +
Chat History
      ↓
Input Context
3.2 Output Tokens

Output tokens represent what the model generates.

For reasoning models, output may include:

Thinking Tokens
+
Visible Answer

Both can count toward output limits.

The maximum output setting may cap:

Thinking + Visible Answer

If thinking consumes too much of the output budget, the visible response may be shortened or even cut off.

Reasoning Effort

Depending on the model/API, reasoning effort or thinking budget can influence:

Cost
Latency
Output-token usage
Available reasoning budget
3.3 Worked Token Budget

Example from the PDF:

Context window = 128,000 tokens
Maximum output = 8,192 tokens

Input:

Component	Tokens
System prompt	1,200
Few-shot examples	2,500
Retrieved documents	5,000
Chat history	1,000
User message	300
Total input	10,000

Output:

Component	Tokens
Thinking	3,000
Visible answer	800
Total output	3,800

Total window usage:

10,000 + 3,800
= 13,800 tokens

That is approximately:

11% of a 128,000-token context window
Important

If thinking consumed 7,600 tokens out of an 8,192-token output cap, only:

592 tokens

would remain for the visible answer.

Therefore:

Leave sufficient output headroom when using thinking/reasoning models.

3.4 Bigger Is Not Always Better

A larger context window does not automatically mean better answers.

1. Cost

More input tokens generally mean higher cost.

2. Latency

Longer inputs can increase processing time.

3. Lost in the Middle

Models may attend less effectively to information buried in the middle of very long prompts.

4. Context Rot

Irrelevant or conflicting information can reduce response quality as context grows.

RAG Principle

Fewer, better chunks usually beat more chunks.

Instead of retrieving everything:

20 mediocre chunks

prefer:

5 highly relevant chunks

when they provide the information needed to answer the question.

Prompt Organization

A useful strategy:

Start
  ↓
Important instructions
  ↓
Relevant context
  ↓
User/task details
  ↓
Critical constraints repeated near the end

For long conversations:

Summarize old turns
Remove irrelevant history
Trim unnecessary context