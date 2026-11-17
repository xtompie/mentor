# Installing mentor: instructions for an AI agent

You are an AI coding agent. The user asked you to install mentor. Ask one question at a time and wait for the answer. Talk in the user's language.

## 1. Get the files

```bash
git clone --depth 1 https://github.com/xtompie/mentor.git /tmp/mentor-install
```

## 2. Ask

**For your user or for this project?** Recommend user.

- User (recommended): the skill goes to `~/.claude/skills/mentor/`. It works on any session in any project.
- Project: the skill goes to `<project>/.claude/skills/mentor/`. Anyone who clones the repo gets it. User skills win over project skills with the same name.

## 3. Copy

Let `<skills-dir>` be the chosen folder.

```bash
cp -R /tmp/mentor-install/skills/mentor <skills-dir>/mentor
cp /tmp/mentor-install/VERSION <skills-dir>/mentor/VERSION
```

If `<skills-dir>/mentor` already exists, stop and ask, or follow "Upgrading" below.

## 4. Check

```bash
perl <skills-dir>/mentor/scripts/session-text.pl /tmp/mentor-install/tests/fixtures/converter.jsonl
```

It should print a short conversation that starts with `# session`. Remove `/tmp/mentor-install`.

## 5. Explain

Tell the user briefly:

- At the end of a session, type `/mentor`. It asks whether you want rules for the model, lessons for yourself, or both.
- For an older session: `/mentor <session id>` or `/mentor <path>.jsonl`.
- It writes nothing until you approve each item.

If it was installed in a project, ask whether to commit it. Never push without being asked.

## Upgrading

When mentor is already installed (`<skills-dir>/mentor/SKILL.md` exists):

1. Read the installed version from `<skills-dir>/mentor/VERSION`. No such file: do every "Upgrade" step in the changelog; they are safe to repeat.
2. Get the files (step 1) and read `CHANGELOG.md`. Take every version newer than the installed one.
3. Replace `<skills-dir>/mentor` with the new `skills/mentor`, and copy `VERSION` into it again.
4. Do the "Upgrade" steps of each newer version, oldest first.
5. Tell the user what changed, in a few lines, from the changelog.
