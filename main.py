from fastapi import FastAPI
from typing import Dict
from config import K
from func import compute_shares

app = FastAPI()

share_mp: Dict[str, int] = {}
total_mp: Dict[str, int] = {"qq": 99}


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
