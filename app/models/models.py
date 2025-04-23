from pydantic import BaseModel
from typing import List, Optional


class WrapperRequest(BaseModel):
    # recebe uma lista de dicionários, ex:
    # { "conditions": [ {"ano": "2025} ] }
        
    conditions: list
