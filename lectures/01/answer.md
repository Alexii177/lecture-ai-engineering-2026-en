# Lecture 01 Answers

## Exercises

- Model used: gemini-3.5 flash.
- Model's answer to the course specific question:
  The model stated that it did not have access to the AIE2026
  syllabus and could not identify the three homework levels.
- Comparison with the glossary:
  The actual levels were Basic, Implementation and Advanced.
  The model acknowledged its lack of course specific knowledge
  instead of inventing an answer which is hallucination. General knowledge alone does
  not guarantee knowledge of this course.
- Token counts displayed:
  For "What is LoRA?", the API reported 6 input tokens and
  731 output tokens.

## Homework

- Level attempted: Implementation.

### What I did

Modified app/ask.py to support an interactive conversation using
the Gemini SDK... Added --chat to start a conversation,
/reset to clear its history and /exit to end it. Preserved the
original single question mode and added input/output token reporting.

### Results

All 11 existing tests passed in 3.96 seconds.

I also manually tested conversation history:

| Step | Input | Observed result | Input tokens | Output tokens |

 1  it remembered that my project is called RotorTutor and teaches rotor balancing. | The model acknowledged the project details. | 19 | 51 |
 2  What is my project called, and what does it teach? | Correctly recalled RotorTutor and rotor balancing. | 84 | 17 |
 3  /reset | The application cleared the conversation history. | N/A | N/A |
 4  What is my project called, and what does it teach? | The model no longer knew the project details and asked for context. | 13 | 82 |

### Observations and questions

The chat returned information across follow up questions within
the same session. After /reset, the earlier project details were
no longer available it was not remembering anything...

The follow up request used 84 input tokens, compared with 13 for
the same question after resetting. This shows how conversation
history increases the input sent to the model and can increase
token usage and consumption of token...

This memory is conversation context, not model training or
permanent storage. Starting a new chat session clears that context.

The existing automated tests passed; the new conversation-history
and reset behavior i verified them manually.