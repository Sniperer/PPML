"""
compute this model on bedoza:
model = models.Sequential([
    layers.Dense(64, activation='sigmoid', input_shape=(28 * 28,)),
    layers.Dense(1, activation='sigmoid')
])
"""
import keras
from config import NN_MODEL_FILE, test_data_point
from client_Zp import init_all_shares, add_with_gate, total_mp, open, mul_with_gate, share
from client_fixed import fixed2Zp, Zp2fixed, reload_fixed
from time import time
from sigmoid import sigmoid


def load_weights(model_path: str = NN_MODEL_FILE) -> list:
    model = keras.models.load_model(model_path)
    weights = model.get_weights()
    for i, weight in enumerate(weights):
        print(f"Layer {i} weights shape: {weight.shape}")
    return weights


def init_weight_input_to_total_mp(data_point: list, weights: list) -> None:
    # input data point
    for i in range(len(data_point)):
        total_mp[f"X_{i}"] = fixed2Zp(data_point[i])
    # layer 1, W
    for i in range(784):  # len(weights[0]) == 784 == 28*28
        for j in range(64):  # len(weights[0][i]) == 64
            total_mp[f"Layer_1_W_{i}_{j}"] = fixed2Zp(weights[0][i][j])
    # layer 1, B
    for i in range(64):  # 64 == len(weights[1])
        total_mp[f"Layer_1_B_{i}"] = fixed2Zp(weights[1][i])
    # layer 2, W
    for i in range(64):  # 64 == len(weights[2])
        for j in range(1):  # 1 == len(weights[2][i])
            total_mp[f"Layer_2_W_{i}_{j}"] = fixed2Zp(weights[2][i][j])
    # layer 2, B
    for i in range(1):  # 1 == len(weights[3])
        total_mp[f"Layer_2_B_{i}"] = fixed2Zp(weights[3][i])

    init_all_shares()
    return


def compute() -> None:
    # layer 1
    for j in range(64):
        total_mp[f"layer_1_ans_{j}"] = fixed2Zp(0.0)
        share(f"layer_1_ans_{j}")
        for i in range(28 * 28):
            # z[i][j] = W[i][j]*X[i]
            mul_with_gate(f"Layer_1_W_{i}_{j}", f"X_{i}", f"Z_{i}_{j}")
            reload_fixed(f"Z_{i}_{j}")
            # layer_1_ans[j] += Z[i][j]
            add_with_gate(f"Z_{i}_{j}", f"layer_1_ans_{j}", f"layer_1_ans_{j}")
        # layer_1_ans[j] += B[j]
        add_with_gate(f"Layer_1_B_{j}", f"layer_1_ans_{j}", f"layer_1_ans_{j}")

        ans = Zp2fixed(open(f"layer_1_ans_{j}"))
        sigmoid(f"layer_1_ans_{j}", f"layer_2_X_{j}")
        ans_2 = Zp2fixed(open(f"layer_2_X_{j}"))
        print(f"j = {j}, ans = {ans}, ans2 = {ans_2}")
        # a1.append(1 / (1 + np.exp(-z1))  )

    # layer 2
    total_mp["layer_2_ans"] = fixed2Zp(0.0)
    share("layer_2_ans")
    j = 0
    for i in range(64):
        # Z2[i][j] = layer_2_X[i]*W2[i][j]
        mul_with_gate(f"Layer_2_W_{i}_{j}", f"layer_2_X_{i}", f"Z2_{i}_{j}")
        reload_fixed(f"Z2_{i}_{j}")
        # layer_2_ans += Z2[i][j]
        add_with_gate(f"Z2_{i}_{j}", "layer_2_ans", "layer_2_ans")
    # layer_2_ans += B2
    add_with_gate(f"Layer_2_B_{0}", "layer_2_ans", "layer_2_ans")
    ans = Zp2fixed(open("layer_2_ans"))
    sigmoid("layer_2_ans", "NN_output")
    ans_2 = Zp2fixed(open("NN_output"))
    print(f"Layer 2, ans = {ans}, ans2 = {ans_2}")
    return


def NN_compution(data_point: list, weights: list) -> float:
    start_time = time()
    init_weight_input_to_total_mp(data_point, weights)
    end_time_1 = time()
    print(f"load_weights() takes {end_time_1 - start_time} s")
    compute()
    end_time_2 = time()
    print(f"compute() takes {end_time_2 - end_time_1} s")
    ans = Zp2fixed(open("NN_output"))
    return ans


def test_NN():
    weights = load_weights()
    data_point = test_data_point
    ans = NN_compution(data_point, weights)

    return


if __name__ == "__main__":
    test_NN()
