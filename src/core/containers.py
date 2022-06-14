from typing import Optional, Dict, Union

from pydantic.main import BaseModel

from core.enums import StatusEnum


class OperationStatus(BaseModel):
    status: StatusEnum
    detail: Optional[Union[str, Dict]] = None
