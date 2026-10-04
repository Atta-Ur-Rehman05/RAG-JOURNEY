<div align="center">

# 🧠 LLM Fundamentals

### How Large Language Models Work — From Tokens to Generated Responses

**RAG Learning Journey · Day 2**

[![AI](https://img.shields.io/badge/AI-LLM-blue)](https://github.com/)
[![RAG](https://img.shields.io/badge/Learning-RAG-green)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-Learning-yellow)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Learning-orange)](https://github.com/)

> A structured guide to understanding how modern Large Language Models process text, predict tokens, generate responses, and manage context.

</div>

---

# 📖 Overview

Large Language Models are the foundation behind modern AI applications such as:

* 💬 Chatbots
* 🔎 AI Search
* 📚 RAG systems
* 🤖 AI Agents
* 💻 Code assistants
* 📝 Content generation
* 📊 Information extraction
* 🧠 Reasoning systems

At their core, language models perform a deceptively simple task:

> **Predict the next token based on the tokens that came before it.**

That process is repeated thousands of times to generate an entire response.

This README builds the mental model from the ground up:

```text
Text
 ↓
Tokens
 ↓
Token IDs
 ↓
Embeddings
 ↓
Transformer
 ↓
Logits
 ↓
Probabilities
 ↓
Sampling
 ↓
Next Token
 ↓
Repeat
 ↓
Response
```

---

# 🎯 Learning Objectives

By completing this material, you should understand:

* What an LLM actually does
* How text is converted into tokens
* What token IDs are
* What embeddings represent
* Why positional information matters
* How Transformers process context
* What self-attention does
* What feed-forward networks do
* What logits are
* How logits become probabilities
* How the next token is selected
* What autoregressive generation means
* What prefill and decode mean
* Why KV caching matters
* How LLMs are trained at a high level
* How temperature changes sampling
* What `top_p` does
* What `top_k` does
* What context windows are
* How input and output tokens affect usage
* Why large context does not automatically mean better results
* Why these concepts matter when building RAG applications

---

# 🗂️ Table of Contents

* [1. What Is an LLM?](#1-what-is-an-llm)
* [2. LLM Generation Pipeline](#2-llm-generation-pipeline)
* [3. Input](#3-input)
* [4. Tokens](#4-tokens)
* [5. Token IDs](#5-token-ids)
* [6. Embeddings](#6-embeddings)
* [7. Positional Information](#7-positional-information)
* [8. Transformer](#8-transformer)

  * [Self-Attention](#81-self-attention)
  * [Feed-Forward Network](#82-feed-forward-network)
* [9. Logits and Probabilities](#9-logits-and-probabilities)
* [10. Token Selection](#10-token-selection)
* [11. Autoregressive Generation](#11-autoregressive-generation)
* [12. Prefill and Decode](#12-prefill-and-decode)
* [13. KV Cache](#13-kv-cache)
* [14. How LLMs Learn](#14-how-llms-learn)
* [15. Temperature](#15-temperature)
* [16. Top-P](#16-top-p)
* [17. Top-K](#17-top-k)
* [18. Sampling](#18-sampling)
* [19. Context Window](#19-context-window)
* [20. Input vs Output Tokens](#20-input-vs-output-tokens)
* [21. Token Budget](#21-token-budget)
* [22. Why Bigger Context Isn't Always Better](#22-why-bigger-context-isnt-always-better)
* [23. LLMs and RAG](#23-llms-and-rag)
* [24. Mental Model](#24-mental-model)
* [25. Final Checklist](#25-final-checklist)

---

# 1. What Is an LLM?

A **Large Language Model (LLM)** is a neural network trained to model language by predicting tokens.

The fundamental operation can be represented as:

```text
Previous Tokens
      ↓
LLM
      ↓
Probability Distribution
      ↓
Next Token
```

For example:

```text
Input:

"The sky is"

Possible next tokens:

blue    → 70%
clear   → 15%
gray    → 10%
green   →  5%
```

The model selects a token and continues.

```text
"The sky is blue"
```

Then it predicts the next token again.

---

# 2. LLM Generation Pipeline

A simplified LLM generation pipeline looks like this:

```text
┌─────────────────────┐
│     User Input      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│     Tokenization    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│     Token IDs       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│     Embeddings      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Transformer Layers  │
│                     │
│ Self-Attention      │
│ Feed Forward        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│       Logits        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│   Probabilities     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│      Sampling       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│    Next Token       │
└──────────┬──────────┘
           ↓
        Repeat
```

The model keeps repeating this process until:

* an end-of-sequence condition occurs, or
* the output limit is reached.

---

# 3. Input

The model's input is not necessarily just the latest user message.

A modern AI application may provide:

```text
System Instructions
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
```

All of this contributes to the model's input context.

### Why This Matters

This is especially important for RAG.

A RAG application may construct:

```text
System Prompt
      +
Retrieved Chunks
      +
Conversation History
      +
User Question
      ↓
LLM Input
```

The model then generates an answer based on this complete context.

---

# 4. Tokens

LLMs do not directly process human concepts such as "words".

They process **tokens**.

A token can represent:

* a complete word
* part of a word
* punctuation
* numbers
* spaces or word pieces
* code fragments

For example:

```text
"Write a sentence about AI."
```

may conceptually become:

```text
Write
a
sentence
about
AI
.
```

The exact tokenization depends on the model's tokenizer.

### Important Principle

> **Token count—not word count—is what matters for model context and token usage.**

Different types of text can have different token efficiency:

| Content          | Token Behavior                   |
| ---------------- | -------------------------------- |
| Common English   | Usually efficient                |
| Rare words       | May require more tokens          |
| Code             | Can require many tokens          |
| Numbers          | Can tokenize inefficiently       |
| Non-English text | Token count varies significantly |

---

# 5. Token IDs

After tokenization, each token is mapped to an integer.

```text
"hello"
   ↓
Token
   ↓
Token ID
   ↓
15339
```

Conceptually:

```text
Text
 ↓
Tokenizer
 ↓
["hello", "world"]
 ↓
[15339, 1917]
```

The model works with these numerical representations rather than raw text.

---

# 6. Embeddings

Token IDs themselves do not contain rich semantic information.

They are mapped into vectors through an embedding table.

```text
Token
  ↓
Token ID
  ↓
Embedding Lookup
  ↓
Vector
```

Example:

```text
"sky"
   ↓
[0.12, -0.48, 0.91, 0.07, ...]
```

These vectors form the numerical representation that the Transformer can process.

### Semantic Relationships

During training, representations learn useful relationships between tokens.

Conceptually:

```text
king
queen
man
woman
```

can develop meaningful relationships in representation space.

---

# 7. Positional Information

A Transformer needs information about **where tokens occur**.

Consider:

```text
The dog chased the cat.
```

versus:

```text
The cat chased the dog.
```

The same words appear, but their order changes the meaning.

Therefore, the model needs positional information.

```text
Token Embeddings
       +
Position Information
       ↓
Transformer Input
```

---

# 8. Transformer

The Transformer is the central architecture behind modern LLMs.

A simplified Transformer layer:

```text
Input Representations
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
```

This process occurs across many Transformer layers.

---

## 8.1 Self-Attention

Self-attention allows tokens to consider relationships with other tokens in the sequence.

For example:

```text
"The animal didn't cross the road because it was tired."
```

The model needs to understand what:

```text
"it"
```

refers to.

Attention helps the model establish relationships between tokens.

Conceptually:

```text
Token A ─────┐
Token B ─────┤
Token C ─────┼──→ Attention
Token D ─────┤
Token E ─────┘
```

Different attention heads can learn to focus on different patterns such as:

* grammatical relationships
* references
* topics
* nearby relationships
* long-range dependencies

---

## 8.2 Feed-Forward Network

After attention, representations pass through feed-forward transformations.

```text
Attention Output
       ↓
Feed-Forward Network
       ↓
Updated Representation
```

The repeated combination of attention and feed-forward processing allows the model to build increasingly rich representations.

---

# 9. Logits and Probabilities

Eventually, the model produces scores for possible next tokens.

These raw scores are called **logits**.

```text
Final Representation
        ↓
      Logits
        ↓
      Softmax
        ↓
 Probabilities
```

Example:

| Candidate | Probability |
| --------- | ----------: |
| `blue`    |         60% |
| `clear`   |         25% |
| `gray`    |         10% |
| `green`   |          5% |

The probabilities form a distribution over possible next tokens.

---

# 10. Token Selection

The model now needs to select one token.

Given:

```text
blue    → 60%
clear   → 25%
gray    → 10%
green   → 5%
```

The highest-probability token is:

```text
blue
```

A deterministic strategy may choose it directly.

A sampling strategy may choose among several candidates according to their probabilities.

---

# 11. Autoregressive Generation

LLMs generate responses **autoregressively**.

That means the newly generated token becomes part of the context for the next prediction.

Example:

```text
Prompt
  ↓
"The"
  ↓
"The sky"
  ↓
"The sky is"
  ↓
"The sky is blue"
  ↓
"The sky is blue."
```

The model does not generate the entire answer simultaneously.

Instead:

```text
Predict
  ↓
Append
  ↓
Predict
  ↓
Append
  ↓
Predict
  ↓
...
```

This is one of the most important mental models for understanding LLMs.

---

# 12. Prefill and Decode

LLM serving can be understood as two major phases.

## Prefill

The model processes the existing input.

```text
System Prompt
+
History
+
Documents
+
Question
       ↓
    Prefill
```

## Decode

The model generates output tokens one at a time.

```text
Token 1
 ↓
Token 2
 ↓
Token 3
 ↓
Token 4
 ↓
...
```

### Why It Matters

Long prompts can increase processing requirements before generation even begins.

This is particularly relevant to RAG systems containing large retrieved contexts.

---

# 13. KV Cache

During autoregressive generation, the model repeatedly attends to previously processed tokens.

Recomputing everything from scratch would be inefficient.

A **KV cache** stores previously computed attention information.

Conceptually:

```text
Previous Tokens
      ↓
Key / Value States
      ↓
     Cache
      ↓
Reuse during decoding
```

Instead of repeatedly recomputing previous attention states, the model can reuse cached information.

This improves generation efficiency.

---

# 14. How LLMs Learn

Modern LLM development can involve multiple stages.

| Stage                      | Purpose                                           |
| -------------------------- | ------------------------------------------------- |
| **Pre-training**           | Learn broad language patterns and knowledge       |
| **Supervised Fine-Tuning** | Improve instruction following                     |
| **Preference Tuning**      | Improve helpfulness, safety, and response quality |
| **Reasoning Training**     | Improve behavior on reasoning/checkable tasks     |

### Simplified Pipeline

```text
Large Corpus
     ↓
Pre-training
     ↓
Base Model
     ↓
Instruction Training
     ↓
Preference / Alignment Training
     ↓
More Capable Assistant
```

---

# 15. Temperature

Temperature controls the shape of the probability distribution during sampling.

Conceptually:

```text
softmax(logits / T)
```

### Low Temperature

```text
T < 1
```

Produces a more concentrated distribution.

```text
High probability
      ↓
Dominates
```

Useful for:

* classification
* extraction
* deterministic workflows
* structured tasks

### High Temperature

```text
T > 1
```

Produces a flatter distribution.

Useful for:

* brainstorming
* creative writing
* diverse generation

### Mental Model

```text
LOW
Temperature
    ↓
Focused
Predictable
Consistent


HIGH
Temperature
    ↓
Diverse
Creative
Variable
```

---

# 16. Top-P

`top_p` is also known as **nucleus sampling**.

Instead of selecting a fixed number of tokens, it keeps the smallest group whose cumulative probability reaches the selected threshold.

Example:

```text
blue    60%
clear   25%
gray    10%
green    5%
```

With:

```text
top_p = 0.90
```

We accumulate:

```text
blue
60%

blue + clear
85%

blue + clear + gray
95%
```

Therefore:

```text
blue
clear
gray
```

remain candidates.

---

# 17. Top-K

`top_k` keeps a fixed number of highest-probability candidates.

Example:

```text
blue    60%
clear   25%
gray    10%
green    5%
```

With:

```text
top_k = 2
```

Only:

```text
blue
clear
```

remain.

### Top-K vs Top-P

| Property             | Top-K        | Top-P                 |
| -------------------- | ------------ | --------------------- |
| Selection            | Fixed number | Probability threshold |
| Candidate count      | Fixed        | Variable              |
| Adapts to confidence | ❌            | ✅                     |
| Example              | `k = 20`     | `p = 0.9`             |

---

# 18. Sampling

After filtering, probabilities are renormalized.

Then a weighted random selection can occur.

```text
Logits
  ↓
Temperature
  ↓
Softmax
  ↓
Top-K / Top-P
  ↓
Renormalization
  ↓
Weighted Sampling
  ↓
Next Token
```

This explains why identical prompts can sometimes produce different responses.

---

# 19. Context Window

The **context window** is the maximum amount of tokenized information the model can process for a request.

Think of it as the model's working context.

```text
┌──────────────────────────────┐
│       CONTEXT WINDOW         │
│                              │
│ System Instructions          │
│ Few-Shot Examples            │
│ Chat History                 │
│ Retrieved Documents          │
│ Tool Information             │
│ User Question                │
│                              │
│ Generated Output             │
└──────────────────────────────┘
```

### Critical Principle

> **Input and output consume context capacity.**

---

# 20. Input vs Output Tokens

## Input Tokens

May include:

* system instructions
* user message
* chat history
* retrieved documents
* examples
* tool definitions
* tool results

## Output Tokens

Represent what the model generates.

Depending on the model/API, reasoning or thinking tokens can also contribute to output usage.

### Simplified

```text
Total Context
=
Input Tokens
+
Output Tokens
```

---

# 21. Token Budget

Suppose:

```text
Context Window = 128,000
Maximum Output = 8,192
```

Input:

| Component           |     Tokens |
| ------------------- | ---------: |
| System prompt       |      1,200 |
| Examples            |      2,500 |
| Retrieved documents |      5,000 |
| Chat history        |      1,000 |
| User message        |        300 |
| **Total**           | **10,000** |

Suppose output contains:

| Component      |    Tokens |
| -------------- | --------: |
| Reasoning      |     3,000 |
| Visible answer |       800 |
| **Total**      | **3,800** |

Total:

```text
10,000 + 3,800
= 13,800 tokens
```

The important lesson is that your prompt architecture directly affects:

* cost
* latency
* available output space
* model performance

---

# 22. Why Bigger Context Isn't Always Better

A larger context window is useful, but blindly adding more information can hurt.

### 1. 💰 Cost

More tokens generally mean more computation and potentially higher cost.

### 2. ⏱️ Latency

Large prompts require more processing.

### 3. 🧩 Lost in the Middle

Important information buried in a huge context may receive less effective attention.

### 4. 🌪️ Context Noise

Irrelevant or contradictory information can make the task harder.

---

## RAG Principle

> **Retrieve fewer, better chunks rather than everything.**

Instead of:

```text
20 mediocre chunks
```

prefer:

```text
5 highly relevant chunks
```

when those five contain the required evidence.

---

# 23. LLMs and RAG

This is where LLM fundamentals become directly useful for your RAG journey.

A basic RAG system looks like:

```text
              ┌──────────────────┐
              │   User Question  │
              └────────┬─────────┘
                       ↓
              ┌──────────────────┐
              │     Retrieval    │
              └────────┬─────────┘
                       ↓
              ┌──────────────────┐
              │ Relevant Chunks  │
              └────────┬─────────┘
                       ↓
              ┌──────────────────┐
              │ Prompt + Context │
              └────────┬─────────┘
                       ↓
              ┌──────────────────┐
              │       LLM        │
              └────────┬─────────┘
                       ↓
              ┌──────────────────┐
              │     Response     │
              └──────────────────┘
```

The LLM does **not** magically know your private documents.

RAG gives the model additional information by putting retrieved content into its context.

```text
Knowledge Base
     ↓
Retriever
     ↓
Relevant Context
     ↓
Prompt
     ↓
LLM
     ↓
Grounded Answer
```

---

# 24. Mental Model

If you remember only one pipeline, remember this:

```text
              USER INPUT
                   │
                   ▼
             TOKENIZATION
                   │
                   ▼
               TOKEN IDs
                   │
                   ▼
              EMBEDDINGS
                   │
                   ▼
             TRANSFORMER
             ┌─────┴─────┐
             │           │
       Attention     Feed Forward
             │           │
             └─────┬─────┘
                   │
                   ▼
                 LOGITS
                   │
                   ▼
             PROBABILITIES
                   │
                   ▼
              SAMPLING
                   │
                   ▼
              NEXT TOKEN
                   │
                   ▼
                REPEAT
                   │
                   ▼
              FINAL TEXT
```

---

# 25. Final Checklist

Before moving forward, make sure you can explain:

### Fundamentals

* [ ] What an LLM is
* [ ] What next-token prediction means
* [ ] What tokens are
* [ ] What token IDs are
* [ ] What embeddings are
* [ ] Why positional information is needed
* [ ] What a Transformer does
* [ ] What self-attention does
* [ ] What feed-forward networks do
* [ ] What logits are
* [ ] How logits become probabilities

### Generation

* [ ] Autoregressive generation
* [ ] Greedy decoding
* [ ] Sampling
* [ ] Temperature
* [ ] Top-P
* [ ] Top-K
* [ ] Prefill
* [ ] Decode
* [ ] KV cache

### Context

* [ ] Context window
* [ ] Input tokens
* [ ] Output tokens
* [ ] Token budget
* [ ] Context limitations
* [ ] Context noise

### RAG

* [ ] Why retrieved documents enter the prompt
* [ ] Why token count matters in RAG
* [ ] Why retrieval quality matters
* [ ] Why more context isn't always better

---

# 🧠 Final Takeaway

An LLM can be mentally reduced to:

```text
Understand Context
       ↓
Predict Next Token
       ↓
Select Token
       ↓
Add Token to Context
       ↓
Predict Again
       ↓
Repeat
```

The sophistication comes from the enormous neural network, Transformer architecture, learned representations, attention mechanisms, training process, and sampling strategies behind that loop.

Understanding this pipeline is essential before moving deeper into:

```text
Prompt Engineering
        ↓
Embeddings
        ↓
Vector Search
        ↓
RAG
        ↓
Agents
        ↓
LLM Applications
```

<div align="center">

### 🚀 LLM Fundamentals Complete

**Next → Prompt Engineering**

</div>
