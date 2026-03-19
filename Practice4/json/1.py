import json

with open("sample-data.json") as f:
    data = json.load(f)

print("Interface Status")
print("="*80)
print(f"{'DN':50} {'Description':20} {'Speed':6} {'MTU':6}")
print("-"*50 + " " + "-"*20 + " " + "-"*6 + " " + "-"*6)

for intf in data.get('imdata', []):
    attrs = intf.get('l1PhysIf', {}).get('attributes', {})
    dn = attrs.get('dn', '')
    desc = attrs.get('descr', '')
    speed = attrs.get('speed', 'inherit')
    mtu = attrs.get('mtu', '')
    
    print(f"{dn:50} {desc:20} {speed:6} {mtu:6}")