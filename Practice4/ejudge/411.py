import sys
import json

def apply_patch(source, patch):
    if not isinstance(patch, dict):
        return patch
    
    if not isinstance(source, dict):
        source = {}

    for key, value in patch.items():
        if value is None:
            if key in source:
                del source[key]
        elif isinstance(value, dict) and key in source and isinstance(source[key], dict):
            apply_patch(source[key], value)
        else:
            source[key] = value
    return source

def main():
    lines = sys.stdin.read().splitlines()
    if len(lines) < 2:
        return
    
    try:
        source = json.loads(lines[0])
        patch = json.loads(lines[1])
        
        result = apply_patch(source, patch)
        
        # Compact JSON with sorted keys
        output = json.dumps(result, sort_keys=True, separators=(',', ':'))
        sys.stdout.write(output + "\n")
    except (ValueError, IndexError):
        pass

if __name__ == "__main__":
    main()