# Workshop Guide: Generative AI, Agentic AI, and Prompt Engineering

## What is Generative AI?

Generative AI refers to models that create new artifacts (text, images,
audio, code, video) from learned patterns in data. Instead of only
classifying or extracting, generative models *synthesize* --- e.g., they
can write an article, produce an image, or generate code snippets.
Common forms today: autoregressive language models (GPT-style),
diffusion/image generators, and music/audio generators.

## What is Agentic AI?

Agentic AI (or "agentic systems") are systems built *on top of*
generative models that plan, act, and use external tools to achieve
goals autonomously. Rather than returning a single answer when prompted,
agentic systems can (for example) break a high-level goal into
sub-tasks, call web APIs, update memory/state, iterate based on results,
and continue until the objective is met.

## Difference between Generative AI and Agentic AI

  ------------------------------------------------------------------------
  Aspect           Generative AI                  Agentic AI
  ---------------- ------------------------------ ------------------------
  Purpose          Produce content                Pursue goals across time
                   (text/images/code) in response (planning + acting).
                   to input.                      

  Interaction      Single-turn/few-turn           Multi-turn, autonomous
                   responses.                     workflows with tools &
                                                  memory.

  Examples         Creative writing,              Auto-GPT, workflow
                   summarization, code            automation, research
                   completion.                    agents.
  ------------------------------------------------------------------------

## Current Progress

-   Transformers became the backbone of modern LLMs.
-   Large multimodal models (e.g., GPT-4) combine text & vision.
-   Instruction tuning + RLHF improved alignment with users.
-   Retrieval-Augmented Generation (RAG) reduces hallucinations.
-   Agentic frameworks (LangChain, Auto-GPT) are emerging rapidly.

## Transformer Architecture Review

1.  Self-attention: tokens attend to all tokens via queries, keys,
    values.
2.  Multi-head attention: parallel heads capture different relations.
3.  Positional encoding: adds sequence order info.
4.  Encoder-decoder vs decoder-only architectures.
5.  Scaling laws: more data + compute → emergent in-context learning.

## Challenges in Generative AI

-   Hallucinations (fabricated facts).
-   Bias and fairness issues.
-   Safety and misuse (prompt injection, disinformation).
-   Data & copyright challenges.
-   Huge compute/energy cost.
-   Evaluation difficulties.

## What It Takes to Create an LLM

1.  Data pipeline & cleaning.
2.  Tokenization (BPE/Unigram).
3.  Transformer architecture design.
4.  Pretraining (next-token prediction).
5.  Instruction tuning & RLHF.
6.  Retrieval + memory (RAG).
7.  Evaluation & safety testing.
8.  Efficient deployment & monitoring.

## Designing a Prompt --- Workflow

1.  Define the goal clearly.
2.  Assign the model a role/persona.
3.  Provide context (docs, examples).
4.  Specify output format (JSON, bullet list, etc.).
5.  Add examples for few-shot learning.
6.  Add safety constraints.
7.  Iterate and evaluate outputs.

### Example Prompt (Summarization)

    System: You are a concise technical summarizer. Provide a 3-sentence TL;DR and 5 bullet points. Say "Insufficient info" if unsure.
    User: Article: <paste here>. Return JSON format.

## Defining Personas and Roles

-   Example:
    `You are an experienced legal analyst writing for executives.`
-   Multi-agent roles: Researcher, Verifier, Writer.

## Avoiding Prompt Injection

-   Use delimiters (\<`<USER_CONTENT>`{=html}\> ...
    \<`<END_USER_CONTENT>`{=html}\>).
-   Sanitize/strip instructions from user data.
-   Restrict model access to safe tools.
-   Add verification agents & monitoring.

## Zero-shot vs Few-shot Learning

-   **Zero-shot**: Instruction only, no examples.
-   **Few-shot**: Include input-output examples in the prompt.
-   Few-shot is better when format/nuance matters.

## Decoding Parameters

-   **Temperature**: randomness. Low = deterministic, high = creative.
-   **Top-p (nucleus sampling)**: picks from tokens with cumulative prob
    ≥ p.
-   **Max tokens**: output length cap.
-   **Frequency/Presence penalty**: reduces repetition.

## Controlling Hallucinations

-   Retrieval-Augmented Generation (RAG).
-   Instruction tuning + RLHF.
-   Constrain output format.
-   Verifier models/human review.
-   Conservative decoding (low temperature).

## Popular Prompt Patterns

1.  System + Role + Format.
2.  Chain-of-thought reasoning.
3.  Extract → Summarize (two-stage).
4.  RAG with citation IDs.
5.  Tool/function-calling with schemas.

### Example (Summarization)

    System: You are a summarizer. Use only provided docs. Output: TL;DR, 5 bullets, source doc IDs.

## Case Study: Summarization

**Pipeline:** 1. Split doc into chunks. 2. Embed & store in vector DB.
3. Retrieve top-k relevant chunks. 4. Summarize with citations.

**Evaluation:** - Automatic: ROUGE scores. - Human: factuality,
readability, citation accuracy.

**Workshop Exercise:** - Zero-shot summarizer vs RAG + few-shot
summarizer. - Compare outputs for hallucinations and factuality.

## Workshop Flow (3--4 hrs)

1.  Intro (GenAI vs Agentic AI) --- 15m.
2.  Transformer & LLM review --- 30m.
3.  Prompt engineering patterns --- 45m.
4.  Hands-on summarization --- 45m.
5.  Agentic AI demo & safety --- 30m.
6.  Q&A --- 15m.
