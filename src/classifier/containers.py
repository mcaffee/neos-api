from pydantic.main import BaseModel


class ModelTrainingStatus(BaseModel):
    status: str


class ModelTrainingData(BaseModel):
    data: str
