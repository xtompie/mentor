---
name: mentor
description: Turn a Claude Code session into one-line rules for the model, or short lessons for the user. Reads the session, finds what the user had to explain or correct, proposes rules or lessons with evidence, and writes nothing until the user approves each one.
argument-hint: "[session id or path] [rules|lessons|both]"
disable-model-invocation: true
---

Talk in the user's language. Ask one question at a time.

## 1. Read the session

Find the session file, then convert it. Run each command on its own, never chained with `;` or `&&`.

- The argument ends with `.jsonl`: it is a file path, relative to the current folder. Use it as it is.
- The argument is an id (letters, digits, dashes): `ls ~/.claude/projects/*/<id>.jsonl`.
- No argument: this session. Its id is `${CLAUDE_SESSION_ID}`; find its file the same way.

Convert: `perl ${CLAUDE_SKILL_DIR}/scripts/session-text.pl <file>`. Read the output, not the JSONL. Cite evidence by turn number, like `[12]`. Never analyse a different session than the one asked for; if the file is missing, say so and stop.

## 2. Ask the goal

If the arguments do not say `rules`, `lessons` or `both`, ask exactly one question:

> Improve the model next time (rules), learn something yourself (lessons), or both?

## 3. Find candidates

Read the whole conversation. Look for moments where the user had to give the model something it did not have. Strongest first:

1. The model said it was done, and the user came back with a failure.
2. The user explained the same thing over several turns until it worked.
3. The user interrupted (`USER INTERRUPTED`) and redirected.
4. A tool call was rejected (`! ... rejected`).
5. A correction right after a reply: "no", "not there", "I told you", "actually".
6. An edit that undid an earlier edit.
7. Anything the user explained that the model could not have known from the code or the instructions.

Not a candidate: creative iteration ("shorter", "redo the header", "another color"), a one-off request, taste that changes per task. Read `${CLAUDE_SKILL_DIR}/references/signals.md` when unsure.

## 4. Rules (for the model)

Read `${CLAUDE_SKILL_DIR}/references/rules.md`, then for each candidate:

- One imperative sentence. Specific: names, paths, commands. Keep the contrast "X, not Y" when there was one. No history, no "the user said".
- Evidence: the turn numbers and a short quote.
- When it applies: the kind of task or file.
- Keep it only if both hold: given at the start, it would have saved the back-and-forth; and it will apply to the next task of this kind.
- Before proposing, search for an existing rule on the same thing: `CLAUDE.md` and `AGENTS.md` from the project root up to the home folder, `~/.claude/CLAUDE.md`, the skill that was running, and project docs. If a rule exists and the model broke it anyway, propose strengthening that rule, never a second one.
- Propose where it goes (table in `references/rules.md`).

Advice for the user (how to ask, what to say upfront) is never a rule for the model. Put it under lessons or say it in the summary.

Zero rules is a valid result. Say so plainly.

## 5. Lessons (for the user)

Read `${CLAUDE_SKILL_DIR}/references/lessons.md`, then for each idea the user taught or learned in this session:

- Its name, the common term if there is one.
- Two or three sentences: what it is and why it matters.
- The example from this session: file, class, or turn.
- Optionally one line the user can give the model next time.

Offer to explain any of them in more depth. Do not write long essays unasked.

## 6. Approve, then write

Show one numbered list. For each item: the rule or lesson, the evidence, and the proposed place. Ask the user to answer per item: apply, edit, or skip.

- Apply only approved items. Add or change one line in the target file; never rewrite a whole file. Show the diff.
- Lessons go where the user says (a notes file, a doc). If the user names no place, show them and write nothing.
- If Droid is installed (`.ai/droids/droids.md`) and a droid owns the topic, offer `/droid-queue <droid> "<rule>"` instead of editing its wiki.
- Nothing is written before the user approves.

End with one short line: what was written where.
