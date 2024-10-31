import random
from typing import Dict
import requests
from config import K, URL_PREFIX

share_mp: Dict[str, int] = {}
total_mp: Dict[str, int] = {}


def init_all_shares() -> None:
    # share all value of Bob, and requests all value from Alice (via share_shares())
    # should always and only run at begining.
    global share_mp, total_mp
    for it in total_mp:
        share(it)
    r = requests.get(f"{URL_PREFIX}/share_shares")
    part_share_mp = r.json()
    share_mp = {**share_mp, **part_share_mp}
    return 


def share(var_name: str, k: int = K) -> None:
    r = random.randint(1, (1 << k) - 1)
    share_mp[var_name] = (total_mp[var_name] - r) % (1 << k)
    # print(r)
    requests.get(f"{URL_PREFIX}/register_share/{var_name}/{r}")


def register():
    return


def open(var_name: str) -> int:
    r = requests.get(
        f"{URL_PREFIX}/open/{var_name}/{share_mp[var_name]}")
    r = r.json()
    return int(r)


def add_with_constant_A(x):
    return


def test_open():
    total_mp["xyz"] = 123
    share("xyz", 7)
    print(f"test_open: {total_mp['xyz']} == {open('xyz')}")

def test_init_all_shares():
    global total_mp
    total_mp = {"aa":1, "bb":2, "cc":100}
    init_all_shares()
    print(share_mp)

if __name__ == "__main__":
    #test_open()
    test_init_all_shares()