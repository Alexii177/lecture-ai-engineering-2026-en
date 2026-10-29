# Lecture 02 Answers

## Exercise: Original Course FAQ


Model: Qwen/Qwen3.5-0.8B.


Training used 14 examples, with 7 validation examples and
21 evaluation questions. The run completed 20 epochs and
40 steps in 198 seconds. Trainable parameters: 6,389,760
(0.8421% of all parameters). The final logged training loss
was 0.014778.

| Metric | Before | After |
|---|---:|---:|
| Format rate | 95.24% | 100% |
| Content rate | 38.10% | 85.71% |
| Both rate | 38.10% | 85.71% |
| Evaluation time | 52.4 s | 42.2 s |

No previously passing questions failed afterward.

Three content failures remained: the model unnecessarily
requested review for PDF-format and late-submission questions,
and answered an appointment-requirement question using
office-hour information that did not establish whether an
appointment was required.

In the additional knowledge checks, the model requested review
for the instructor's name and next lecture's topic. However,
it incorrectly treated the general assignment deadline as the
final-assignment deadline. These classifications were unchanged
by training. The supported general-deadline control remained
correct.

Training improved formatting and the main evaluation score,
but did not guarantee recognition of unsupported questions.

## Homework

### Level attempted

Implementation.

### Custom topic and changes

I replaced FAQ, GROUNDED, UNGROUNDED, and the additional
evaluation questions with an English RotorTutor teaching
scenario about rotor balancing.

The five FAQ items describe:
- The topic taught by RotorTutor.
- Eight holes for positioning a correction mass.
- A measurement duration of 20 seconds.
- Correction mass in grams and hole-number inputs.
- Comparison of RMS vibration and peak amplitude.

I preserved the JSON fields answer and needs_review,
the dataset split structure, and the original training settings.
The exact configuration is saved in result.json.

### Dataset design

The dataset contained 14 training examples, 7 validation
examples, and 21 test questions. Training, validation, and
test questions used distinct wording.

I prepared unsupported questions by identifying engineering
details absent from the five-item FAQ, including maximum speed,
tightening torque, numerical vibration limits, maximum
correction mass, sensor calibration intervals, and bearing
spacing. Their expected response was a request for confirmation,
with needs_review set to true.

The FAQ was included in each example's input. This experiment
therefore evaluates response behaviour with supplied context;
it does not demonstrate reliable memorisation of engineering
knowledge without the FAQ.

### Training and results

I ran the custom training myself. Training completed 20 epochs
and 40 steps in 171 seconds. The final logged training loss was
0.018149. There were 6,389,760 trainable parameters (0.8421%).

| Metric | Before | After |
|---|---:|---:|
| Format rate | 100% | 100% |
| Content rate | 23.81% (5/21) | 95.24% (20/21) |
| Both rate | 23.81% | 95.24% |
| Evaluation time | 22.4 s | 36.6 s |

The notebook reported no overall pass-to-fail regressions.

### Remaining failure

The question asking for a numerical RMS vibration limit
remained incorrect. After training, the model repeated the
available vibration metrics and set needs_review to false,
although the FAQ supplied no numerical threshold.

Before training, this response included an unsupported value
of 1000 while requesting review. Thus, neither answer was
acceptable, and the review flag itself worsened after training.

### Evaluation limitations

The evaluator requires particular keywords as well as the
correct review flag. Before training, an answer of "8" failed
because it omitted "holes". Several reasonable statements that
information was unavailable failed because they omitted
"Confirmation".

The score improvement therefore reflects both better review
decisions on supported questions and closer matching of
expected wording. It should not be interpreted as a general
95.24% factual-accuracy claim.

For the six unsupported main-test questions, review flags were
correct in 6/6 cases before training and 5/6 afterward.
A correct review flag alone also does not guarantee a sound
answer, as the invented RMS value demonstrates.

### Additional diagnostic checks

After inspecting the main results, I added three new unsupported
questions about motor warm-up time, correction-hole radius,
and vibration sampling frequency, plus a supported control
about measurement duration.

All four classifications were correct before and after training.
The control correctly identified 20 seconds. Training made the
wording more complete and consistent.

These were additional diagnostic checks created after the main
evaluation, not a pre-registered independent benchmark.

### Discussion

Fine-tuning helped produce consistent answers and review
messages for this small task. However, low training loss did not
eliminate unsupported answers, and correct JSON did not imply
correct reasoning about the FAQ.

For changing technical specifications, a system that retrieves
current documentation would make updates easier. Fine-tuning
could support consistent output behaviour, while retrieval
provides relevant evidence. Both approaches still require
evaluation of unsupported questions.

The recorded evaluation times are single-run observations.
They are insufficient to establish a general speed benefit or
penalty from LoRA.

### AI assistance and personal verification

I used ChatGPT to help adapt the dataset.
I ran the notebook myself, reviewed the before/after outputs,
checked the remaining failure and scoring limitations, and
saved the experiment evidence.