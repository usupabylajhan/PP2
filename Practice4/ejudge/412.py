import sys
import json

def get_diff(obj1, obj2, path=""):
    diffs = {}
    
    # Ensure both are treated as dictionaries for key collection
    keys1 = set(obj1.keys()) if isinstance(obj1, dict) else set()
    keys2 = set(obj2.keys()) if isinstance(obj2, dict) else set()
    all_keys = keys1 | keys2
    
    for key in all_keys:
        current_path = f"{path}.{key}" if path else key
        
        # Check existence
        in_1 = isinstance(obj1, dict) and key in obj1
        in_2 = isinstance(obj2, dict) and key in obj2
        
        val1 = obj1[key] if in_1 else "<missing>"
        val2 = obj2[key] if in_2 else "<missing>"
        
        if val1 == val2:
            continue
            
        # Recurse only if both are dicts and both exist
        if isinstance(val1, dict) and isinstance(val2, dict):
            diffs.update(get_diff(val1, val2, current_path))
        else:
            # Format values
            v1_str = json.dumps(val1, separators=(',', ':')) if in_1 else "<missing>"
            v2_str = json.dumps(val2, separators=(',', ':')) if in_2 else "<missing>"
            diffs[current_path] = f"{current_path} : {v1_str} -> {v2_str}"
            
    return diffs

def main():
    # Use read().splitlines() or read().strip().split('\n') to handle varied line endings
    input_data = sys.stdin.read().strip().split('\n')
    if len(input_data) < 2:
        return
        
    try:
        obj1 = json.loads(input_data[0])
        obj2 = json.loads(input_data[1])
        
        differences = get_diff(obj1, obj2)
        
        if not differences:
            sys.stdout.write("No differences\n")
        else:
            for p in sorted(differences.keys()):
                sys.stdout.write(differences[p] + "\n")
    except (ValueError, IndexError):
        pass

if __name__ == "__main__":
    main()