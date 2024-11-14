import random
from typing import Dict, List
import requests
from config import k, URL_PREFIX
from func import generate_random

share_mp: Dict[str, int] = {"NULL": 0}
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


def share(var_name: str) -> None:
    r: int = random.randint(1, k - 1)
    share_mp[var_name] = (total_mp[var_name] - r) % k
    # print(r)
    requests.get(f"{URL_PREFIX}/register_share/{var_name}/{r}")


def open(var_name: str) -> int:
    r = requests.get(f"{URL_PREFIX}/open/{var_name}/{share_mp[var_name]}")
    r = r.json()
    return int(r)


def open_in_mul(var_name_a: str, var_name_b: str, des_name: str, d: int, e: int) -> List[int]:
    r = requests.get(f"{URL_PREFIX}/open_in_mul/{var_name_a}/{var_name_b}/{des_name}/{d}/{e}")
    r: List[int] = r.json()
    return r


def add_with_constant(var_name: str, des_name: str, const: int) -> None:
    # target: mp[des_name] = mp[var_name]+const
    share_mp[des_name] = (share_mp[var_name] + const) % k
    r = requests.get(f"{URL_PREFIX}/add_with_constant/{var_name}/{des_name}")
    return


def mul_with_constant(var_name: str, des_name: str, const: int) -> None:
    # target: mp[des_name] = mp[var_name]*const
    share_mp[des_name] = (share_mp[var_name] * const) % k
    requests.get(f"{URL_PREFIX}/mul_with_constant/{var_name}/{des_name}/{const}")
    return


def add_with_gate(var_name_a: str, var_name_b: str, des_name: str) -> None:
    share_mp[des_name] = (share_mp[var_name_a] + share_mp[var_name_b]) % k
    requests.get(f"{URL_PREFIX}/add_with_gate/{var_name_a}/{var_name_b}/{des_name}")
    return


def mul_with_gate(var_name_a: str, var_name_b: str, des_name: str) -> None:
    u, v, w = generate_random()
    # print(u, v, w)
    d = (share_mp[var_name_a] + u) % k
    e = (share_mp[var_name_b] + v) % k
    tmp = open_in_mul(var_name_a, var_name_b, des_name, d, e)
    d = tmp[0]
    e = tmp[1]
    share_mp[des_name] = (w + (e * share_mp[var_name_a]) %
                          k + (d * share_mp[var_name_b]) % k - (d * e) % k) % k
    return


def test_open():
    total_mp["xyz"] = 123
    share("xyz")
    print(f"test_open: {total_mp['xyz']} == {open('xyz')}")


def test_init_all_shares():
    global total_mp
    total_mp = {"aa": 1, "bb": 2, "cc": 100}
    init_all_shares()
    print("test_init_all_shares", share_mp)


def test_add_with_constant():
    global total_mp
    total_mp = {"aa": 11}
    init_all_shares()
    add_with_constant("aa", "sum_a", 3)
    print(f"test_add_with_constant: 14 == {open('sum_a')}")


def test_mul_with_constant():
    global total_mp
    total_mp = {"aa": 111}
    init_all_shares()
    mul_with_constant("aa", "mul_a", 11)
    print(f"test_mul_with_constant: 69 == {open('mul_a')}")


def test_add_with_gate():
    # Remember setting another's value before test this one
    global total_mp
    total_mp = {"aa": 13}
    init_all_shares()
    add_with_gate("aa", "bb", "cc")
    # print(share_mp)
    print(f"test_mul_with_gate: 124 == {open('cc')}")
    return


def test_mul_with_gate():
    global total_mp
    total_mp = {"aa": 13}
    init_all_shares()
    mul_with_gate("aa", "bb", "cc")
    print(f"test_mul_with_gate: {(111 * 13)%k} == {open('cc')}")
    return


def test_all():
    test_open()
    test_init_all_shares()
    test_add_with_constant()
    test_mul_with_constant()
    test_add_with_gate()
    test_mul_with_gate()


if __name__ == "__main__":
    test_all()
