from typing import List

from pydantic import BaseModel


class DumpRequest(BaseModel):
    feeds: List[str]
