# here we can compute over integer. Includes neg int.
from config import k
from client_Zp import init_all_shares, add_with_gate, total_mp, open, mul_with_gate


def Zp2int(x: int, k=k) -> int:
    # input x is a element in Zp. x in [0, p-1]
    # this function means to decode the x into a integer, range in [-p/2, p/2 - 1]
    if x >= k/2:
        return x-k
    else:
        return x


def int2Zp(x: int, k=k) -> int:
    # input is a a integer, range in [-p/2, p/2 - 1]
    # decode x into a element in Zp.
    if x < 0:
        return k + x
    else:
        return x


def test_add_int(a: int = -3, b: int = 2) -> None:
    # compute c=a+b, and a, b, c in [-k/2, k/2 - 1]
    # retest the function needs to restart the sever API
    total_mp["aa"] = int2Zp(a)
    total_mp["qq"] = int2Zp(b)
    init_all_shares()
    add_with_gate("aa", "qq", "cc")
    ans: int = Zp2int(open('cc'))
    print(f"test_add_int: {ans} == {a + b}")
    return


def test_mul_int(a: int, b: int) -> None:
    # compute c=a*b, and a, b, c in [-k/2, k/2 - 1]
    total_mp["aa"] = int2Zp(a)
    total_mp["qq"] = int2Zp(b)
    init_all_shares()
    mul_with_gate("aa", "qq", "cc")
    ans: int = Zp2int(open('cc'))
    print(f"test_add_int: {ans} == {a * b}")


if __name__ == "__main__":
    # test_add_int(-1, -11)
    test_mul_int(11, 11)
