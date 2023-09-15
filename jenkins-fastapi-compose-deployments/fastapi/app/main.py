from fastapi import FastAPI, HTTPException
import random


def percentile_true(percentile):
    return random.random() < percentile / 100.0


app = FastAPI()


@app.get("/")
def hello_world():
    should_fail_500 = percentile_true(10)
    if should_fail_500:
        raise HTTPException(status_code=500, detail="[500] Internal Server Error")
    should_fail_400 = percentile_true(10)
    if should_fail_400:
        raise HTTPException(status_code=400, detail="[400] Bad Request")
    should_fail_404 = percentile_true(10)
    if should_fail_404:
        raise HTTPException(status_code=404, detail="[404] Not Found")
    return {"message": "[200] OK"}
