from config import K, DEALER_PREFIX
import random
import requests
from typing import Dict, List


def compute_shares(total_mp: Dict[str, int], k=K):
    share_mp_0 = {}
    share_mp_1 = {}
    for it in total_mp:
        r = random.randint(1, (1 << k) - 1)
        share_mp_0[it] = r
        share_mp_1[it] = (total_mp[it] - r) % (1 << k)

    return share_mp_0, share_mp_1

def generate_random() -> List[int]:
    r = requests.get(
        f"{DEALER_PREFIX}/generate_random")
    r = r.json()
    return r

def test_compute_shares():
    total_mp = {"aa": 3, "bb": 4, "cc": 100}
    print(compute_shares(total_mp))


if __name__ == "__main__":
    test_compute_shares()
