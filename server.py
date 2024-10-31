from fastapi import FastAPI
from typing import Dict
from config import K
from func import compute_shares

app = FastAPI()

share_mp: Dict[str, int] = {}
total_mp: Dict[str, int] = {"bb": 111}


@app.get("/open/{var_name}/{var_share}")
def open(var_name: str, var_share: str) -> str:
    var_share: int = int(var_share)
    myshare: int = share_mp[var_name]
    total_mp[var_name] = (myshare + var_share) % (1 << K)
    return str(total_mp[var_name])


@app.get("/register_share/{var_name}/{var_share}")
def register(var_name: str, var_share: str) -> str:
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
    share_mp[des_name] = (share_mp[var_name]*const) % (1 << K)
    return


@app.get("/add_with_gate/{var_name_a}/{var_name_b}/{des_name}")
def add_with_gate(var_name_a: str, var_name_b: str, des_name: str) -> None:
    share_mp[des_name] = (share_mp[var_name_a] +
                          share_mp[var_name_b]) % (1 << K)
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
