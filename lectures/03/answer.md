# Lecture 03 Answers

## Exercises

### Plain LLM versus agent

In Lecture 1, the plain LLM could not identify the course's
three homework levels because it lacked course-specific information.

The Lecture 3 agent searched the glossary and answered:
Basic, Implementation, and Advanced. It also referenced Lecture 01.

### Observed glossary trace

- Tool: search_glossary
- Arguments: {"query": "homework levels"}
- Model requests: 2
- Tool calls: 1
- Input tokens: 737
- Output tokens: 143

The model requested a search, received its result, and then
generated an answer.

### Added tool: make_quiz

I added make_quiz(lecture: int), which filters glossary entries
by lecture number, randomly selects a term, and returns a
question, its answer, and the lecture number as JSON.
It handles lectures with no available terms without crashing.

Its docstring explains that it should be used when the learner
requests a quiz or review question.

I registered it with agent.tool_plain and added an instruction
telling the agent when to use it.

### Verification

The tool list displayed three tools after adding make_quiz.
All 11 existing tests passed in 3.67 seconds.

For "Give me one review question from Lecture 02", the trace
showed make_quiz({"lecture": 2}). The agent produced a question
about Supervised Fine-Tuning with a hint and a Lecture 02 reference.

This run used 2 model requests, 1 tool call, 885 input tokens,
and 90 output tokens.

## Homework

### Level attempted

Implementation.

### What I implemented

I added save_learning_log(topic: str, notes: str) to app/tools.py.
It writes a JSON record containing the topic, notes, and UTC
timestamp into learning_log/.

Generated filenames combine a timestamp and UUID. Exclusive
file creation avoids overwriting an existing record.
Empty topics or notes are rejected.

In app/agent.py, I registered the tool with requires_approval=True
and added DeferredToolRequests to the agent's output types.

The CLI displays the proposed content and asks for approval.
Only y or yes approves the operation. Other responses deny it.
The decision is passed back through DeferredToolResults, together
with the message history, so the agent can continue.

### Results

The tool list displayed all four tools.

Rejection test:
- Topic: Rejected test
- I entered N at the approval prompt.
- The program printed Denied.
- The trace reported that the tool call was denied.

Approval test:
- Topic: Agent tools
- Notes: An agent combines a model, a loop and tools.
- I entered y at the approval prompt.
- The program printed Approved.
- The tool returned status: saved.
- I inspected the resulting JSON file and verified its topic,
  notes, and timestamp.

The final folder inspection showed one JSON file containing
the approved note and no file containing the rejected note.

### Difficulties and observations

An indentation error in main() initially prevented imports and
test collection. I corrected the function's indentation and
successfully ran the tool list and both interactive save tests.

A tool description alone does not enforce approval. The framework's
requires_approval setting pauses execution, and the CLI supplies
the user's explicit decision before the write occurs.

The printed usage after resuming describes that resumed run;
it should not be treated as the total usage across both phases.

### AI assistance
### SUMMARY

After implementing the approval flow and fixing indentation,
all 11 existing tests passed in 3.94 seconds.
Approval and rejection were also verified through manual CLI tests.
I used ChatGPT to help implement the tools, resolve the indentation
error. I ran the commands myself and inspected
the approval prompts, tool results, and saved JSON content.