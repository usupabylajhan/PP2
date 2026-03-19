import sys
import importlib

def solve():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    
    try:
        n_queries = int(input_data[0])
        for i in range(1, n_queries + 1):
            line = input_data[i].strip().split()
            if not line:
                continue
            
            module_path = line[0]
            attr_name = line[1]
            
            try:
                mod = importlib.import_module(module_path)
                if hasattr(mod, attr_name):
                    attr = getattr(mod, attr_name)
                    if callable(attr):
                        sys.stdout.write("CALLABLE\n")
                    else:
                        sys.stdout.write("VALUE\n")
                else:
                    sys.stdout.write("ATTRIBUTE_NOT_FOUND\n")
            except ImportError:
                sys.stdout.write("MODULE_NOT_FOUND\n")
            except Exception:
                sys.stdout.write("ATTRIBUTE_NOT_FOUND\n")
                
    except (ValueError, IndexError):
        pass

if __name__ == "__main__":
    solve()