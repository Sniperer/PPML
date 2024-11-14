from client_Zp import init_all_shares, add_with_gate, total_mp, open, mul_with_gate
from client_fixed import eps, fixed2Zp, Zp2fixed, reload_fixed
from typing import List
import joblib
from sigmoid import sigmoid, sigmoid_by_taylor
from sklearn.linear_model import LogisticRegression
from config import test_x


def is_valid(x: float) -> bool:
    if abs(x) <= eps:
        return True
    else:
        return False


def mul_layer(W_name: List[str], X_name: List[str], layer: int) -> int:
    print("mul_layer start-> ")
    for i in range(len(W_name)):
        if i % 100 == 0:
            print(f"i = {i}")
        mul_with_gate(W_name[i], X_name[i], f"Z_{layer}_{i}")
        reload_fixed(f"Z_{layer}_{i}")
    return len(W_name)


def add_layer(layer: int, width: int) -> int:
    print(f"add_layer {layer} start-> ")
    for i in range(0, width, 2):
        if i == width-1:
            add_with_gate(f"Z_{layer-1}_{width-1}", "NULL", f"Z_{layer}_{width//2}")
            return (width+1)//2
        add_with_gate(f"Z_{layer-1}_{i}", f"Z_{layer-1}_{i+1}", f"Z_{layer}_{i//2}")
    return width//2


def func_computation_client(W: List[float], X: List[float]) -> float:
    for x in X:
        assert is_valid(x), "Input is out of range"
    W_name = [f"w{i}" for i in range(len(X))]
    X_name = [f"x{i}" for i in range(len(X))]

    for i in range(len(X)):
        total_mp[X_name[i]] = fixed2Zp(X[i])

    init_all_shares()
    # check whether all shares are initialized
    width = mul_layer(W_name, X_name, 0)
    layer = 1
    while True:
        width = add_layer(layer, width)
        layer += 1
        if width == 1:
            break
    add_with_gate(f"Z_{layer - 1}_{0}", "offset", "pre_result")
    sigmoid("pre_result", "result")
    ans: float = Zp2fixed(open("result"), scale=1)
    return ans


def test(X) -> None:
    size = 1024
    model = joblib.load("./model.joblib")
    W: List[float] = model.coef_.tolist()[0]
    offset: float = model.intercept_.tolist()[0]
    Z: List[float] = [W[i]*X[i] for i in range(size)]
    ans: float = offset
    for i in Z:
        ans += i
    prob: float = model.predict_proba([X])[0][1]
    print(f"{func_computation_client(W,X)} == {sigmoid_by_taylor(ans)} == {prob}")
    return


if __name__ == "__main__":
    X = test_x
    test(X)
