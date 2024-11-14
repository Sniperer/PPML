from client_Zp import add_with_gate, open, mul_with_gate, mul_with_constant, add_with_constant, share
from client_fixed import fixed2Zp, Zp2fixed, reload_fixed
import client_Zp


def sigmoid(var_name: str, des_name: str) -> None:
    # Taylor = 0.5 + (1/4) * x - (1/48) * x**3 + (1/480) * x**5 - (17/80640) * x**7 + (4369/92897280) * x**9
    mul_with_constant(var_name, "s_ans_1", fixed2Zp(1/4))
    reload_fixed("s_ans_1")
    add_with_constant("s_ans_1", "s_ans_2", fixed2Zp(0.5))  # 2
    mul_with_gate(var_name, var_name, "s_x_2")
    reload_fixed("s_x_2")
    mul_with_gate("s_x_2", var_name, "s_x_3")
    reload_fixed("s_x_3")
    mul_with_constant("s_x_3", "s_ans_3", fixed2Zp(- 1/48))
    reload_fixed("s_ans_3")
    add_with_gate("s_ans_3", "s_ans_2", "s_ans_4")  # 3
    mul_with_gate("s_x_2", "s_x_3", "s_x_5")
    reload_fixed("s_x_5")
    mul_with_constant("s_x_5", "s_ans_5", fixed2Zp(1/480))
    reload_fixed("s_ans_5")
    add_with_gate("s_ans_5", "s_ans_4", "s_ans_6")  # 4
    mul_with_gate("s_x_5", "s_x_2", "s_x_7")
    reload_fixed("s_x_7")
    mul_with_constant("s_x_7", "s_ans_7", fixed2Zp(-17/80640))
    reload_fixed("s_ans_7")
    add_with_gate("s_ans_7", "s_ans_6", "s_ans_8")  # 5
    mul_with_gate("s_x_7", "s_x_2", "s_x_9")
    reload_fixed("s_x_9")
    mul_with_constant("s_x_9", "s_ans_9", fixed2Zp(4369/92897280))
    reload_fixed("s_ans_9")
    add_with_gate("s_ans_8", "s_ans_9", des_name)  # 6
    return


def test_sigmoid(x: float) -> None:
    Taylor = 0.5 + (1/4) * x - (1/48) * x**3 + (1/480) * x**5 - \
        (17/80640) * x**7 + (4369/92897280) * x**9
    client_Zp.total_mp["xyz"] = fixed2Zp(x)
    share("xyz")
    sigmoid("xyz", "answer")
    ans: float = Zp2fixed(open('answer'), scale=1)
    print(f"test_add_int: {ans} == {Taylor}")
    return


if __name__ == "__main__":
    print("123")
    test_sigmoid(1)
