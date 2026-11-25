# Lecture 05 Answers

## Exercises

- Answering model: gemini-3.5-flash-lite.
- Comparison question: In Lecture 2, what does LoRA freeze and what does it train? What does QLoRA add?
- Materials: the supplied course corpus. Vector, Tree and Graph used the selected Lecture 01–03 main materials; full context used a broader collection. Therefore, scope was not identical across all four methods.

### Results by method

Costs below are estimated generation API costs, excluding embeddings and index construction.

| Method | Answer and cited evidence | Time (s) | Input tokens | Output tokens | Model responses | Cost (USD) |
|---|---|---:|---:|---:|---:|---:|
| Full context | Correct core explanation; translated Lecture 2 PDF p.75 | 6.28 | 95,823 | 136 | 1 | 0.029087 |
| Vector | Correct core explanation; Lecture 2 pp.51–52 | 4.47 | 2,757 | 180 | 2 | 0.001277 |
| Tree | Correct core explanation with additional explanation; Lecture 2 p.52 | 8.82 | 9,437 | 329 | 5 | 0.003654 |
| Graph | Correct core explanation; Lecture 2 pp.51–52 | 3.58 | 5,186 | 254 | 2 | 0.002191 |

All four explained that LoRA freezes the original weights and trains small low-rank matrices, while QLoRA additionally quantizes the base weights.

The page metadata maps original Lecture 2 slide 52 to translated PDF page 75. These are different numbering systems for corresponding material.

### Tool traces

- Vector: one search_materials call with query "LoRA freeze train QLoRA add".
- Full context: no retrieval tool calls.
- Tree: four browse_tree calls, following root → lec02-main → lec02-main-s045 → lec02-main-p052.
- Graph: one search_graph call with query "LoRA freeze train QLoRA add Lecture 2".

The model generated its own search arguments; the user question remained fixed.

### Retrieval inspection

A later search-only audit using the recorded vector query returned:
lec02-main-p047, p051, p052, p060 and p061.

The answer relied on the PEFT and LoRA/QLoRA explanation on pages 51–52. Other retrieved pages, including exercise instructions and the discussion of RAG versus fine-tuning, were not needed for this narrow question.

The audit was run separately after generation. It documents retrieval with the same query, rather than a complete capture of the earlier generation-time tool response.

### Method choice and limitations

For this narrow factual question, I would start with vector retrieval. It produced the required explanation with the lowest observed generation cost. Tree exposed a useful navigation path but required more model responses. Graph included related evidence. Full context was much more expensive and included a broader material scope.

These were single successful runs, not repeated benchmarks. The results do not establish a general speed or accuracy ranking. Citation numbering also needs care: original slide numbers should not be presented as translated PDF page numbers without checking the metadata.

## Homework

### Level attempted

Implementation.

### Changes

I added search_with_neighbors in app/retrieval.py and connected search_materials in app/tools.py to it.

The function:
- Keeps the original vector hits first.
- Looks up pages immediately before and after each hit.
- Restricts neighbors to the same document_id.
- Avoids duplicate page IDs.
- Preserves page content and citation metadata.

I retained the original search function for other retrieval paths. I did not change the material text or embeddings, so no index rebuild was required.

### Comparison conditions

I used the same answering model, user questions, selected materials and vector-search settings before and after the change. The search_materials description remained unchanged.

Question 1:
In Lecture 2, what does LoRA freeze and what does it train? What does QLoRA add?

Question 2:
How does compaction differ from cross-session memory? Do all daily notes automatically become long-term memory?

For each question, the trace showed one search_materials call and two model responses both before and after. The recorded search query was unchanged within each pair.

### Before and after results

| Question | Retrieval | Time (s) | Input tokens | Output tokens | Model responses | Cost (USD) |
|---|---|---:|---:|---:|---:|---:|
| LoRA / QLoRA | Original | 4.47 | 2,757 | 180 | 2 | 0.001277 |
| LoRA / QLoRA | With neighbors | 3.29 | 4,672 | 180 | 2 | 0.001852 |
| Compaction / memory | Original | 6.70 | 2,285 | 260 | 2 | 0.001336 |
| Compaction / memory | With neighbors | 3.90 | 4,060 | 336 | 2 | 0.002058 |

Generation cost increased by approximately 45% for LoRA and 54% for memory. Lower observed elapsed times do not demonstrate a speed improvement because each condition was measured only once.

### Evidence added and unnecessary context

Both search-only audits expanded from five original hits to eleven unique pages.

For LoRA, the added pages were p053, p050, p046, p048, p059 and p062. They discussed fine-tuning decisions, behavior versus knowledge, continued pre-training, a lecture summary and the next lecture. These provide broader context but were unnecessary for identifying frozen weights, trainable matrices and quantization. The answer's core facts remained unchanged.

For memory, the original hits were lec03-main-p013, p038, p039, p040 and p065. The added pages were p064, p066, p037, p041, p012 and p014. These covered long-task capability, configuration standards, a section heading, Skills, the tool loop and the harness.

The added Skills page provides a related distinction between storing what happened and storing how to perform a task. However, the main evidence about compaction, persistence and filtering daily notes was already in the original hits.

### Improvements and remaining limitations

The memory answer became more direct after expansion: it explicitly contrasted within-session compaction with persistent cross-session storage and explained that daily notes are selectively promoted rather than automatically retained.

However, this does not demonstrate that newly retrieved pages supplied previously missing evidence. The relevant memory pages were already present. Generation variability may also explain the wording change.

Neither question demonstrated a clear factual-coverage improvement from neighbor expansion. Both demonstrated increased input size and generation cost. Automatically adding neighbors can retrieve unrelated sections or heading-only pages.

The memory answer also described cited pages as translated PDF pages. I have not independently verified every such page mapping, so citation numbering remains a limitation.

For this use case, I would keep ordinary vector retrieval as the default and investigate selective neighbor expansion when a retrieved page is incomplete or depends on surrounding slides.

### Verification and execution

I ran the commands and inspected the outputs myself, with AI assistance for implementation, debugging and report preparation.

The agent integration test was updated to mock the new retrieval entry point. Additional offline tests checked same-document expansion, deduplication, preservation of content and citation fields, and empty search results.

Final test result: 23 passed.
git diff --check reported no whitespace errors.

The environment encountered sqlite-vec download timeouts and intermittent model 503 errors. After installing the wheel locally, I used .venv/bin/python directly. Failed or interrupted generation attempts were retried; the table reports completed runs.

### Saved evidence

The results directory contains:
- Full-context, vector, Tree and Graph execution logs.
- Before/after logs for both comparison questions.
- lora_retrieval_evidence.json.
- memory_retrieval_evidence.json.
