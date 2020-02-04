import os

import headless
import opml

from fastapi import FastAPI
from model import DumpRequest
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware


# TODO: flags


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return RedirectResponse("static/index.html")


@app.get("/api/rsshub_addr")
def rsshub_addr():
    # Gets address of RSSHub instance.
    return os.environ.get("my_rsshub_addr", "https://rsshub.app")


@app.get("/api/search_user/{search_term}")
async def read_results(search_term):
    result = await headless.search_users(search_term)
    return result


@app.post("/api/dump")
async def dump_opml(data: DumpRequest):
    print(data)
    await opml.dump(data.feeds)
    return "Success"
