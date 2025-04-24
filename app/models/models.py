from pydantic import BaseModel
from typing import List, Optional,Union


class WrapperRequest(BaseModel):
    # recebe uma lista de dicionários, ex:
    # { "conditions": [ {"ano": "2025} ] }

    conditions: Optional[list] = None
    
