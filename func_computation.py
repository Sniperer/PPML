import requests
from config import k, URL_PREFIX
from client_Zp import init_all_shares, add_with_gate, total_mp, open, mul_with_gate, share
from client_int import int2Zp, Zp2int
from client_fixed import eps, fixed2Zp, Zp2fixed, reload_fixed
from time import time
import random
from typing import List

def is_valid(x:float) -> bool:
    if abs(x) <= eps:
        return True
    else:
        return False

def mul_layer(W_name:List[str], X_name:List[str], layer:int) -> int:
    for i in range(len(W_name)):
        mul_with_gate(W_name[i], X_name[i], f"Z_{layer}_{i}")
        reload_fixed(f"Z_{layer}_{i}")
    return len(W_name)

def add_layer(layer:int, width:int) -> int:
    for i in range(0,width,2):
        if i == width-1:
            add_with_gate(f"Z_{layer-1}_{width-1}", "NULL", f"Z_{layer}_{width//2}")
            return (width+1)//2        
        add_with_gate(f"Z_{layer-1}_{i}", f"Z_{layer-1}_{i+1}", f"Z_{layer}_{i//2}")
    return width//2

        
def func_computation(W:List[float], X:List[float], offset:float):
    for w in W:
        assert is_valid(w), "Input is out of range"
    for x in X:
        assert is_valid(x), "Input is out of range"
    assert is_valid(offset), "Input is out of range"
    W_name = [f"w{i}" for i in range(len(W))]
    X_name = [f"x{i}" for i in range(len(X))]
    for i in range(len(W)):
        total_mp[W_name[i]] = fixed2Zp(W[i])
    for i in range(len(X)):
        total_mp[X_name[i]] = fixed2Zp(X[i])
    total_mp["offset"] = fixed2Zp(offset)
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
    ans = Zp2fixed(open("pre_result"), scale = 1)
    return ans
        
def test():
    start_time = time()
    size = 1000
    W = [random.random()*2 for _ in range(size)]
    X = [random.random()*2 for _ in range(size)]
    offset = 10.0
    Z = [W[i]*X[i] for i in range(size)]
    ans = offset
    for i in Z:
        ans += i
    end_time = time()
    print(f"{func_computation(W,X,offset)} == {ans} using {(end_time - start_time)*1000}")
    

if __name__ == "__main__":
    test()
    
