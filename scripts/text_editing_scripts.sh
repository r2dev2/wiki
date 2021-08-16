# Insert new line
pbpaste | python3 -c "import sys; [*map(print, sys.stdin)]" | pbcopy

# Convert json dict to readable list
pbpaste | python3 -c "import json, sys; print(*json.load(sys.stdin).values(), sep='\n')" | pbcopy

# Attach weights to json
