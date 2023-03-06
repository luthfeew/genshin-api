import genshin
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
)


cookies = {"ltuid": 119480035, "ltoken": "cnF7TiZqHAAvYqgCBoSPx5EjwezOh1ZHoqSHf7dT"}
client = genshin.Client(cookies)

uncensor_dict = {
    "A": "А",
    "a": "а",
    "E": "Е",
    "e": "е",
    "O": "О",
    "o": "о",
    "I": "І",
    "i": "і",
}
uncensor_dict_ext = {
    "B": "В",
    "K": "К",
    "M": "М",
    "H": "Н",
    "P": "Р",
    "p": "р",
    "C": "С",
    "c": "с",
    "T": "Т",
    "y": "у",
    "X": "Х",
    "x": "х",
    "V": "Ѵ",
    "v": "ѵ",
    "u": "υ",
    " ": "ﾠ",
}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/uncensor/{text}")
def uncensor(text: str, ext: bool = False):
    if ext:
        uncensor_dict.update(uncensor_dict_ext)
    for key, value in uncensor_dict.items():
        text = text.replace(key, value)
    return {"text": text}


@app.get("/full/{uid}")
async def read_item(uid: int):
    try:
        data = await client.get_full_genshin_user(uid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"uid": uid, "data": data}


@app.get("/partial/{uid}")
async def read_item(uid: int):
    try:
        data = await client.get_partial_genshin_user(uid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"uid": uid, "data": data}


@app.get("/abyss/{uid}")
async def read_item(uid: int):
    try:
        data = await client.get_full_genshin_user(uid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    abyss = data.abyss.current if data.abyss.current.floors else data.abyss.previous
    return {"uid": uid, "data": abyss}
