from fastapi import FastAPI
from typing import Dict

app = FastAPI()

share_mp:Dict[str, int] = {}
total_mp:Dict[str, int] = {}
k = 7

@app.get("/open/{var_name}/{var_share}")
def open(var_name:str, var_share:str) -> str:
    var_share:int = int(var_share)
    myshare:int = share_mp[var_name]
    total_mp[var_name]:int = (myshare + var_share)%(1 << k);
    return total_mp[var_name]

@app.get("/register_share/{var_name}/{var_share}")
def register(var_name:str, var_share:str) -> str:
    var_share:int = int(var_share)
    share_mp[var_name] = var_share
    return ""

@app.get("/share_shares")
def share_shares() -> Dict[str, int]:
    d = init_shares()
    return d 

@app.get("/")
async def root():
    return {"message": "Hello World"}
