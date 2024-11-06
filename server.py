from fastapi import FastAPI
import uvicorn
from typing import Dict, List
from config import k, HOST, API_PORT
from func import compute_shares, generate_random

app = FastAPI()

share_mp: Dict[str, int] = {}
total_mp: Dict[str, int] = {"bb": 111}


@app.get("/open/{var_name}/{var_share}")
def open(var_name: str, var_share: str) -> str:
    var_share: int = int(var_share)
    myshare: int = share_mp[var_name]
    total_mp[var_name] = (myshare + var_share) % k
    return str(total_mp[var_name])


@app.get("/open_in_mul/{var_name_a}/{var_name_b}/{des_name}/{d}/{e}")
def open_in_mul(var_name_a: str, var_name_b: str, des_name: str, d: int, e: int) -> List[int]:
    tmp = generate_random()
    u = tmp[0]
    v = tmp[1]
    w = tmp[2]
    print(u, v, w)
    another_d = (share_mp[var_name_a] + u) % k
    another_e = (share_mp[var_name_b] + v) % k
    d += another_d
    e += another_e
    share_mp[des_name] = (w + (e * share_mp[var_name_a]) % k + (d * share_mp[var_name_b]) % k) % k
    return [d, e]


@app.get("/register_share/{var_name}/{var_share}")
def register(var_name: str, var_share: str) -> None:
    var_share: int = int(var_share)
    print(f"var_name: {var_name}, var_share:{var_share}")
    share_mp[var_name] = var_share
    return ""


@app.get("/add_with_constant/{var_name}/{des_name}")
def add_with_constant(var_name: str, des_name: str) -> None:
    share_mp[des_name] = share_mp[var_name]
    return


@app.get("/mul_with_constant/{var_name}/{des_name}/{const}")
def mul_with_constant(var_name: str, des_name: str, const: int) -> None:
    share_mp[des_name] = (share_mp[var_name]*const) % k
    return


@app.get("/add_with_gate/{var_name_a}/{var_name_b}/{des_name}")
def add_with_gate(var_name_a: str, var_name_b: str, des_name: str) -> None:
    share_mp[des_name] = (share_mp[var_name_a] + share_mp[var_name_b]) % k
    return


@app.get("/share_shares")
def share_shares() -> Dict[str, int]:
    global share_mp
    part_share_mp, another_share_mp = compute_shares(total_mp)
    share_mp = {**share_mp, **part_share_mp}
    print(share_mp)
    return another_share_mp


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=API_PORT)
