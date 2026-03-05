from pydantic import BaseModel


class TimeDTO(BaseModel):
    days: int
    hours: int
    minutes: int
    seconds: int


class HumanizeTimeDTO(BaseModel):
    days: str
    hours: str
    minutes: str
    seconds: str

    def show(self) -> str:
        return f"{self.days} {self.hours} {self.minutes} {self.seconds}"
