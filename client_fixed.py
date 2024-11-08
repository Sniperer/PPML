# here we can compute over fixed point. Includes neg number.
import requests
from config import k, URL_PREFIX
from client_Zp import init_all_shares, add_with_gate, total_mp, open, mul_with_gate, share
from client_int import int2Zp, Zp2int
import client_Zp
from time import time

eps = int(k**(1/3)/2 - 5)
# eps is: the range of fixed point. More detail on the doc


def fixed2Zp(x: float) -> int:
    x: int = int(x*eps)
    return int2Zp(x)


def Zp2fixed(x: int, scale=1) -> float:
    # scale can be 1 or 2.
    # for adding or general transfer, scale = 1
    # for mul, scale = 2
    x: int = Zp2int(x)
    x: float = x/(eps**scale)
    return x


def reload_fixed(var_name: str) -> None:
    # only used after mul 2 fixed numbers
    # TODO: some bug here, fix it later
    # bacause for reload,we can not only divide by eps, we also need to care about sign
    ans: float = Zp2fixed(open(var_name), scale=2)
    client_Zp.total_mp[var_name] = fixed2Zp(ans)
    share(var_name)
    return


def test_fixed2Zp(x: float = 3.14):
    zp: int = fixed2Zp(x)
    print(f"test_fixed2Zp:{x} == {Zp2fixed(zp)}")
    return


def test_add_fixed(a: float = -3.14, b: float = 2.718) -> None:
    # compute c=a+b, and a, b, c in [-k/2, k/2 - 1]
    # retest the function needs to restart the sever API
    total_mp["aa"] = fixed2Zp(a)
    total_mp["qq"] = fixed2Zp(b)
    init_all_shares()
    add_with_gate("aa", "qq", "cc")
    ans: float = Zp2fixed(open('cc'))
    print(f"test_add_int: {ans} == {a + b}")
    return


def test_mul_fixed(a: float = 3.14, b: float = -2.718) -> None:
    # compute c=a+b, and a, b, c in [-k/2, k/2 - 1]
    # retest the function needs to restart the sever API
    total_mp["aa"] = fixed2Zp(a)
    total_mp["qq"] = fixed2Zp(b)
    init_all_shares()
    mul_with_gate("aa", "qq", "cc")
    reload_fixed("cc")
    # if we want to do futher compution, we need to reload "cc", because now the scale=2.
    ans: float = Zp2fixed(open('cc'), scale=1)
    print(f"test_add_int: {ans} == {a * b}")
    return


def test_compute_1(w0: float, w1: float, w2: float, x1: float, x2: float) -> None:
    start_time = time()
    # compute w0*w1*w2+x1+x2
    total_mp["w0"] = fixed2Zp(w0)
    total_mp["w1"] = fixed2Zp(w1)
    total_mp["w2"] = fixed2Zp(w2)
    total_mp["x1"] = fixed2Zp(x1)
    total_mp["x2"] = fixed2Zp(x2)
    init_all_shares()
    mul_with_gate("w0", "w1", "ans_1")  # ans1 = w0 * w1
    reload_fixed("ans_1")
    mul_with_gate("ans_1", "w2", "ans_2")  # ans2 = ans1 * w2
    reload_fixed("ans_2")
    add_with_gate("ans_2", "x1", "ans_3")  # ans3 = ans2 + x1
    add_with_gate("ans_3", "x2", "ans_4")  # ans4 = ans3 + x2

    ans: float = Zp2fixed(open('ans_4'), scale=1)
    end_time = time()
    print(f"test_add_int in {(end_time-start_time)*1000} ms: {ans} == {w0 * w1 * w2 + x1 + x2}")


if __name__ == "__main__":
    # test_fixed2Zp()
    # test_add_fixed()
    # test_mul_fixed()
    test_compute_1(-11.1, 22.2, -3.33, 44.4, -55.5)
