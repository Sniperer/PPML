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


def share(var_name: str) -> None:
    r = random.randint(1, (1 << K) - 1)
    share_mp[var_name] = (total_mp[var_name] - r) % (1 << K)
    # print(r)
    requests.get(f"{URL_PREFIX}/register_share/{var_name}/{r}")


def open(var_name: str) -> int:
    r = requests.get(
        f"{URL_PREFIX}/open/{var_name}/{share_mp[var_name]}")
    r = r.json()
    return int(r)


def add_with_constant(var_name: str, des_name: str, const: int) -> None:
    # target: mp[des_name] = mp[var_name]+const
    share_mp[des_name] = (share_mp[var_name] + const) % (1 << K)
    r = requests.get(
        f"{URL_PREFIX}/add_with_constant/{var_name}/{des_name}")
    return


def mul_with_constant(var_name: str, des_name: str, const: int) -> None:
    # target: mp[des_name] = mp[var_name]*const
    share_mp[des_name] = (share_mp[var_name] * const) % (1 << K)
    requests.get(
        f"{URL_PREFIX}/mul_with_constant/{var_name}/{des_name}/{const}")
    return


def add_with_gate(var_name_a: str, var_name_b: str, des_name: str) -> None:
    share_mp[des_name] = (share_mp[var_name_a] +
                          share_mp[var_name_b]) % (1 << K)
    requests.get(
        f"{URL_PREFIX}/add_with_gate/{var_name_a}/{var_name_b}/{des_name}")
    return


def test_open():
    total_mp["xyz"] = 123
    share("xyz", 7)
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


if __name__ == "__main__":
    # test_open()
    # test_init_all_shares()
    # test_add_with_constant()
    # test_mul_with_constant()
    test_add_with_gate()
