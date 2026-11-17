grep -q 'model/' "$1" || { echo "no rule about model/"; exit 1; }
grep -Eqi 'src/Entity' "$1" || { echo "rule lacks the X, not Y contrast"; exit 1; }
grep -Eqi 'session.jsonl.*(nie istnieje|does not exist|not found|missing)' "$1" && { echo "did not find the session file"; exit 1; }
exit 0
