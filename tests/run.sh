#!/bin/sh
# Live tests: each case runs a real Claude Code session (claude -p) in a fresh temp project,
# with the skill installed as /mt so it does not clash with an installed /mentor.
# The fixture session is copied into the project; the case checks the answer and that no file changed.
# Usage: tests/run.sh [case-id] [--runs N] [--model haiku|sonnet]
set -u

ROOT=$(cd "$(dirname "$0")/.." && pwd)
CASES="$ROOT/tests/cases"
RUNS=1
MODEL=haiku
ONLY=""
TIMEOUT=600
TOOLS='Read Glob Grep Bash(perl:*) Bash(ls:*) Bash(grep:*) Bash(cat:*) Bash(git status:*)'

while [ $# -gt 0 ]; do
    case "$1" in
        --runs) RUNS=$2; shift 2 ;;
        --model) MODEL=$2; shift 2 ;;
        -h|--help) sed -n '2,5p' "$0"; exit 0 ;;
        *) ONLY=$1; shift ;;
    esac
done

command -v claude >/dev/null 2>&1 || { echo "claude not found"; exit 2; }
sh "$ROOT/tests/converter.sh" || exit 1

install() { # project dir
    mkdir -p "$1/.claude/skills"
    cp -R "$ROOT/skills/mentor" "$1/.claude/skills/mt"
    sed -i.bak 's/^name: mentor$/name: mt/' "$1/.claude/skills/mt/SKILL.md" && rm "$1/.claude/skills/mt/SKILL.md.bak"
}

total_fail=0
for dir in "$CASES"/*/; do
    id=$(basename "$dir")
    [ -n "$ONLY" ] && [ "$id" != "$ONLY" ] && continue
    pass=0
    i=1
    while [ "$i" -le "$RUNS" ]; do
        p=$(mktemp -d "${TMPDIR:-/tmp}/mentor-test.XXXXXX")
        install "$p"
        cp "$ROOT/tests/fixtures/$(cat "$dir/fixture")" "$p/session.jsonl"
        (cd "$p" && git init -q && git add -A && git -c user.name=t -c user.email=t@t commit -qm init)
        stream="$p.stream"
        (cd "$p" && env -u CLAUDE_CODE_MESSAGING_SOCKET -u CLAUDE_CODE_SESSION_ID -u CLAUDE_PID \
            perl -e 'alarm shift; exec @ARGV' "$TIMEOUT" \
            claude -p "$(cat "$dir/prompt.md")" --model "$MODEL" --permission-mode default \
            --output-format stream-json --verbose --allowedTools $TOOLS < /dev/null) > "$stream" 2>&1
        out="$p.out"
        perl -CS -MJSON::PP -ne 'my $j = eval { decode_json($_) } or next; print $j->{result} if ($j->{type} // "") eq "result"' "$stream" > "$out"
        if ! grep -q '"mt"' "$stream"; then
            reason="skill /mt not loaded"; ok=1
        elif [ -n "$(cd "$p" && git status --porcelain)" ]; then
            reason="files changed without approval: $(cd "$p" && git status --porcelain | tr '\n' ' ')"; ok=1
        else
            reason=$(sh "$dir/check.sh" "$out" 2>&1); ok=$?
        fi
        if [ "$ok" -eq 0 ]; then
            pass=$((pass + 1)); echo "$id #$i pass"
        else
            echo "$id #$i fail $reason (answer: $out, log: $stream)"; stream=""; out=""
        fi
        rm -rf "$p" ${stream:+"$stream"} ${out:+"$out"}
        i=$((i + 1))
    done
    need=$(( (2 * RUNS + 2) / 3 ))
    echo "$id $pass/$RUNS"
    [ "$pass" -lt "$need" ] && total_fail=1
done
exit $total_fail
