import sys
import json
import re

def resolve_query(data, query):
    # Regex to split path by dots or brackets: e.g., "a.b[0].c" -> ["a", "b", "[0]", "c"]
    parts = re.findall(r'[^.\[\]]+|\[\d+\]', query)
    current = data
    
    try:
        for part in parts:
            if part.startswith('[') and part.endswith(']'):
                # Array index access
                index = int(part[1:-1])
                if isinstance(current, list) and 0 <= index < len(current):
                    current = current[index]
                else:
                    return "NOT_FOUND"
            else:
                # Object key access
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    return "NOT_FOUND"
        
        return json.dumps(current, separators=(',', ':'))
    except (IndexError, KeyError, TypeError, ValueError):
        return "NOT_FOUND"

def main():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    
    try:
        json_obj = json.loads(input_data[0])
        num_queries = int(input_data[1])
        
        for i in range(2, 2 + num_queries):
            query = input_data[i].strip()
            if not query:
                continue
            result = resolve_query(json_obj, query)
            sys.stdout.write(result + "\n")
            
    except (ValueError, IndexError):
        pass

if __name__ == "__main__":
    main()