from fastapi import FastAPI
from config import k
import random
app = FastAPI()

cnt = 0

s1 = [0, 0, 0]
s2 = [0, 0, 0]

@app.get("/generate_random")
def generate_random():
    global cnt
    if (cnt%2) == 0:
        u = random.randint(0, k-1)
        v = random.randint(0, k-1)
        w = (u*v)%k

        s1[0] = random.randint(0, k-1)
        s1[1] = random.randint(0, k-1)
        s1[2] = random.randint(0, k-1)

        s2[0] = (u - s1[0])%k
        s2[1] = (v - s1[1])%k
        s2[2] = (w - s1[2])%k

        print(f"{(s1[0] + s2[0])%k * (s1[1] + s2[1])%k} == {(s1[2] + s2[2])%k}")
        cnt += 1
        return s1
    else:
        cnt += 1
        return s2

            
