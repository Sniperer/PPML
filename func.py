from config import K
import random
from typing import Dict


def compute_shares(total_mp: Dict[str, int], k=K):
    share_mp_0 = {}
    share_mp_1 = {}
    for it in total_mp:
        r = random.randint(1, (1 << k) - 1)
        share_mp_0[it] = r
        share_mp_1[it] = (total_mp[it] - r) % (1 << k)

    return share_mp_0, share_mp_1


def test_compute_shares():
    total_mp = {"aa": 3, "bb": 4, "cc": 100}
    print(compute_shares(total_mp))


if __name__ == "__main__":
    test_compute_shares()
