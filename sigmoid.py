import math
from client_Zp import add_with_gate, open, mul_with_gate, mul_with_constant, add_with_constant, share
from client_fixed import fixed2Zp, Zp2fixed, reload_fixed
import client_Zp
from typing import Dict


# coefficient of Taylor series of sigmoid:
# 1/2 + (1/4) * x - (1/48) * x**3 + (1/480) * x**5 - (17/80640) * x**7 + (4369/92897280) * x**9
coef_mp: Dict[int, float] = {
    0: 1/2,
    1: 1/4,
    3: -1/48,
    5: 1/480,
    7: -17/80640,
    9: 4369/92897280
}


def sigmoid_by_taylor(x: float) -> float:
    ans: float = coef_mp[0] + x*coef_mp[1]
    x_to_2: float = x**2
    for i in range(3, 10, 2):
        x *= x_to_2
        ans += coef_mp[i]*x
    return ans


def sigmoid_real(x: float) -> float:
    return 1/(1 + math.e**(-x))


def sigmoid(var_name: str, des_name: str) -> None:
    # compute coef_mp on shares
    mul_with_constant(var_name, des_name, fixed2Zp(coef_mp[1]))  # ans = x*1/4
    reload_fixed(des_name)
    add_with_constant(des_name, des_name, fixed2Zp(coef_mp[0]))  # ans += 0.5
    mul_with_gate(var_name, var_name, "s_x^2")
    reload_fixed("s_x^2")
    add_with_constant(var_name, "s_x^1", 0)  # x^1 := x

    # compute: x^3, x^5, x^7, x^9
    for i in range(3, 10, 2):
        mul_with_gate(f"s_x^{i-2}", "s_x^2", f"s_x^{i}")  # compute x^i
        reload_fixed(f"s_x^{i}")
        mul_with_constant(f"s_x^{i}", f"s_x^{i}_with_conf", fixed2Zp(coef_mp[i]))  # conf_mp[i]*x^i
        reload_fixed(f"s_x^{i}_with_conf")
        add_with_gate(f"s_x^{i}_with_conf", des_name, des_name)  # ans += conf_mp[i]*x^i
    return


def test_sigmoid(x: float) -> None:
    client_Zp.total_mp["xyz"] = fixed2Zp(x)
    share("xyz")
    sigmoid("xyz", "answer")
    ans: float = Zp2fixed(open('answer'), scale=1)
    print(
        f"test_add_int: {ans}\n sigmiod_by_taylor: {sigmoid_by_taylor(x)}\n sigmoid_real: {sigmoid_real(x)}")
    return


if __name__ == "__main__":
    test_sigmoid(5)
