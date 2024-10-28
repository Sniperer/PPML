import random
from typing import Dict
import requests

share_mp:Dict[str, int] = {}
total_mp:Dict[str, int] = {}

def share(var_name:str, k:int) -> None:
    r = random.randint(1, (1 << k) - 1)
    share_mp[var_name] = (total_mp[var_name] - r)%(1 << k)
    print(r)
    requests.get(f"http://localhost:8000/register_share/{var_name}/{r}")

def register():
    return
    
def open(var_name:str) -> int:
    r = requests.get(f"http://localhost:8000/open/{var_name}/{share_mp[var_name]}")
    r = r.json()
    return int(r)

def add_with_constant_A(x):
    return

def test():
    total_mp["xyz"] = 123
    share("xyz", 7)
    print(open("xyz") + )

if __name__ == "__main__":
    test()
