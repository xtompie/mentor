grep -Eqi 'no rules?|zero|nothing to (add|propose|write)|none|0 rules|brak regu|żadn[a-ząęśćżźńół]* regu|nie ma (żadnych )?regu|0 regu' "$1" || { echo "did not say there are no rules"; exit 1; }
grep -Eqi 'session.jsonl.*(nie istnieje|does not exist|not found|missing)' "$1" && { echo "did not find the session file"; exit 1; }
exit 0
