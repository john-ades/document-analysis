from pydantic import BaseModel


class AutoTuneTrainData(BaseModel):
    prompt: str
    completion: str
