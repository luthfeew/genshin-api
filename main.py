import genshin
from fastapi import FastAPI

app = FastAPI()

cookies = {"ltuid": 119480035, "ltoken": "cnF7TiZqHAAvYqgCBoSPx5EjwezOh1ZHoqSHf7dT"}
client = genshin.Client(cookies)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/full/{uid}")
async def read_item(uid: int):
    data = await client.get_full_genshin_user(uid)
    return {"uid": uid, "data": data}


@app.get("/partial/{uid}")
async def read_item(uid: int):
    data = await client.get_partial_genshin_user(uid)
    return {"uid": uid, "data": data}


@app.get("/abyss/{uid}")
async def read_item(uid: int):
    data = await client.get_full_genshin_user(uid)
    abyss = data.abyss.current if data.abyss.current.floors else data.abyss.previous
    return {"uid": uid, "data": abyss}
