#!/bin/sh
# Plain test of the transcript converter, no LLM. Usage: tests/converter.sh
ROOT=$(cd "$(dirname "$0")/.." && pwd)
out=$(perl "$ROOT/skills/mentor/scripts/session-text.pl" "$ROOT/tests/fixtures/converter.jsonl") || { echo "converter failed"; exit 1; }
fail() { echo "converter: $1"; exit 1; }
echo "$out" | grep -q '^\[1\] USER COMMAND: /model haiku$' || fail "slash command not shown"
echo "$out" | grep -q 'USER: Deploy with token=\[REDACTED\] to ~/shop please.$' || fail "user text, redaction or reminder stripping wrong"
echo "$out" | grep -q 'secret reminder' && fail "system reminder leaked"
echo "$out" | grep -q 'hidden thoughts' && fail "thinking leaked"
echo "$out" | grep -q 'local-command-caveat\|Caveat' && fail "meta line leaked"
echo "$out" | grep -q '^    tool Bash: rm -rf build$' || fail "tool call line missing"
echo "$out" | grep -q '^    ! Bash call rejected by the user$' || fail "rejection not marked"
echo "$out" | grep -q '^\[4\] USER INTERRUPTED$' || fail "interrupt not marked"
echo "$out" | grep -q '^# end completed$' || fail "end not detected"
echo "converter pass"
