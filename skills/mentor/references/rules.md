# Rules

## Shape

- One imperative sentence, at most about 20 words.
- Specific beats general: "Put models in `src/<Module>/Model/`, not in `src/Entity/`" beats "Keep files organized".
- Keep the contrast "X, not Y" when the session had one. It stops the old habit.
- No history ("we decided", "the user said"), no reasons longer than a few words.
- A rule a script can check (file size, naming, forbidden call) is better as a check than as a sentence. Say so.

## Tests before proposing

1. Upfront: given at the start of the session, would it have avoided the corrections?
2. Next time: will it apply to the next task of the same kind?
3. New: is it not already written somewhere? If it is and was broken, strengthen that one.

All three must hold.

## Where it goes

| The rule is about | Put it in |
|---|---|
| one module or folder | that folder's `AGENTS.md` or `CLAUDE.md` |
| the whole project | the project's `AGENTS.md` or `CLAUDE.md` |
| how a skill does its job | that skill's `SKILL.md` |
| what review should catch | the project's review skill or checklist |
| the user's taste in every project | `~/.claude/CLAUDE.md` |
| the user, not the model | the user's notes; never model instructions |
| a topic a droid owns | `/droid-queue <droid> "<rule>"` |

Pick the narrowest place that covers it. Read the target file first and match its style and language.
