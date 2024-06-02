from functools import lru_cache
import os
from typing_extensions import Annotated
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from SearchAgent.search_agent.api_client import APIClient
from SearchAgent.search_agent.main import SearchAgent

import config

app = FastAPI()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


@lru_cache
def get_settings():
    return config.Settings()


class ChatRequest(BaseModel):
    query: str


@app.post("/api/chat/")
def chat(
    request: ChatRequest, settings: Annotated[config.Settings, Depends(get_settings)]
):

    api_base_url = f"http://localhost:{settings.api_port}/api"

    client = APIClient(api_base_url)

    lab_csv = "labs_data.csv"
    club_csv = "clubs_data.csv"

    lab_data = client.get_data("labs")
    client.save_to_csv(lab_data, lab_csv)

    club_data = client.get_data("clubs")
    client.save_to_csv(club_data, club_csv)

    # SearchAgent 실행
    search_agent = SearchAgent(lab_csv, club_csv)
    response, responseJson = search_agent.run(request.query)

    return response
