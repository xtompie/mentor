# Signals

How to tell a correction from normal work.

## A correction

- The user names something the model got wrong and says what is right: "models go in `model/`, not `src/`".
- The same point comes back in two or more user turns.
- The model claimed success and the user reports a failure.
- An interrupt followed by a different instruction.
- A rejected tool call followed by a different approach.
- The model edits a file back to how it was before.

## Not a correction

- Creative iteration on content: shorter, longer, other wording, other color, another try.
- New requirements the user had not decided before.
- A one-off choice for this task only.
- The model asked a fair question and the user answered it.

## What the model could not have known

- Where things live in this project, when the code does not make it obvious.
- Names the user uses for things, when they differ from the code.
- Decisions made outside the session: in a meeting, in another repo.
- The user's taste, when it is stable across tasks (code style, tone).
