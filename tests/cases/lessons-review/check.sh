grep -Eqi 'factory|fabryk|construction|budowani|tworzeni' "$1" || { echo "construction/factory idea not named"; exit 1; }
grep -Eqi 'leak|przeciek|ciekn|own (result|type)|its own|własn|encapsulat|enkapsul|abstraction|abstrakc|boundar|granic' "$1" || { echo "leaky module idea not named"; exit 1; }
grep -Eqi 'session.jsonl.*(nie istnieje|does not exist|not found|missing)' "$1" && { echo "did not find the session file"; exit 1; }
exit 0
