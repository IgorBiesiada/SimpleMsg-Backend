from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test/{test_id}")
async def test_route(test_id : int):
    return {"test": test_id}