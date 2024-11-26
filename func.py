from config import k, DEALER_PREFIX
import random
import requests
from typing import Dict, List

# use only this one session to avoid use too many ports and then shut down
session = requests.Session()


def compute_shares(total_mp: Dict[str, int], k=k):
    share_mp_0 = {}
    share_mp_1 = {}
    for it in total_mp:
        r = random.randint(1, k - 1)
        share_mp_0[it] = r
        share_mp_1[it] = (total_mp[it] - r) % k

    return share_mp_0, share_mp_1


def generate_random() -> List[int]:
    r = requests.get(f"{DEALER_PREFIX}/generate_random")
    r = r.json()
    return r


def test_compute_shares():
    total_mp = {"aa": 3, "bb": 4, "cc": 100}
    print(compute_shares(total_mp))


if __name__ == "__main__":
    test_compute_shares()
