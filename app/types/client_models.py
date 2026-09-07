from typing import List

from pydantic import BaseModel

from app.constants.transcript import COMPANY_STATUS


class ClientContext(BaseModel):
    name: str
    status: COMPANY_STATUS
    previous_meetings: List[str] = []