import sys
import random
sys.path.append('..')
from client_Zp import init_all_shares, add_with_gate, total_mp, open, mul_with_gate
from client_fixed import eps, fixed2Zp, Zp2fixed, reload_fixed, test_mul_fixed
import config

def generate_data(n = 100, pre = "aaa"):
    return [pre + str(i) for i in range(n)],[random.uniform(-255, 255) for _ in range(n)]

def generate_data_ab(n = 100, sum = 100):
    na = [str(sum) + "left" + str(i) for i in range(n)]
    va = [random.uniform(-sum, sum) for _ in range(n)]
    nb = [str(sum) + "right" + str(i) for i in range(n)]
    vb = [sum - va[i] for i in range(n)]
    return na, va, nb, vb
            
## empty transfer
def test_empty(n = 100):
    name, value = generate_data(n)
    for i in range(n):
        total_mp[name[i]] = fixed2Zp(value[i])
    errors = 0
    relative_err = 0
    err_max = -1
    for i in range(n):
        expected = value[i]
        final = Zp2fixed(total_mp[name[i]])
        err = abs(expected - final)
        err_max = max(err, err_max)
        assert err < 1/eps, "out of bound"
        errors = errors +  err
        relative_err =relative_err + (err/abs(expected))
    print(f"avg errors:{errors/n},avg relative errors:{relative_err/n},err_max:{err_max}")

## addition
def test_addition(n = 100):
    name_left, value_left = generate_data(n, "left")
    name_right, value_right = generate_data(n, "right")
    for i in range(n):
        total_mp[name_left[i]] = fixed2Zp(value_left[i])
        total_mp[name_right[i]] = fixed2Zp(value_right[i])
    init_all_shares()
    name_res = ["res" + str(i) for i in range(n)]
    value_res = [0 for _ in range(n)]
    for i in range(n):
        add_with_gate(name_left[i], name_right[i], name_res[i])
        value_res[i] = Zp2fixed(open(name_res[i]))

    errors = 0
    relative_err = 0
    err_max = -1
    for i in range(n):
        expected = value_left[i] + value_right[i]
        final = value_res[i]
        err = abs(expected - final)
        err_max = max(err, err_max)
        assert err < 2/eps, "out of bound"
        errors = errors +  err
        relative_err =relative_err + (err/abs(expected))
    print(f"avg errors:{errors/n},avg relative errors:{relative_err/n},err_max:{err_max}")
    return
    
## multiplication
def test_multiplication(s = 100):
    n = 100
    name_left, value_left, name_right, value_right = generate_data_ab(n = n, sum = s)
    for i in range(n):
        total_mp[name_left[i]] = fixed2Zp(value_left[i])
        total_mp[name_right[i]] = fixed2Zp(value_right[i])
    init_all_shares()
    name_res = [str(s) + "res" + str(i) for i in range(n)]
    value_res = [0 for _ in range(n)]
    for i in range(n):
        mul_with_gate(name_left[i], name_right[i], name_res[i])
        reload_fixed(name_res[i])
        value_res[i] = Zp2fixed(open(name_res[i]))

    #print(f"{value_left[0]}   {value_right[0]} {value_left[0] * value_right[0]}  {value_res[0]}")
    errors = 0
    relative_err = 0
    err_max = -1
    for i in range(n):
        expected = value_left[i] * value_right[i]
        final = value_res[i]
        err = abs(expected - final)
        if errors < max(errors, err):
            print(f"Using float: {value_left[i]}*{value_right[i]} = {expected}")
            print(f"Using bedoza: {total_mp[name_left[i]]} * {total_mp[name_right[i]]} = {value_res[i]}")
        errors = max(errors, err)
        relative_err = max(relative_err, err/abs(expected))
    print(f"avg errors:{errors},avg relative errors:{relative_err}")
    return
    
if __name__ == "__main__":
    #n = 100
    #print(f"Zp: {config.k} upper bound should be: {2/eps}")
    #print(f"times:{n}")
    test_multiplication(100)
    #test_mul_fixed()
