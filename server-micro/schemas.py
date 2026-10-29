from pydantic import BaseModel, Field

class HardwareItem(BaseModel):
    hardwareId: str = Field(min_length=1)
    hardwareName: str = Field(min_length=1)
    capacity: int = Field(gt=0)


class ProjectCreate(BaseModel):
    projectId: str = Field(min_length=1)
    projectName: str = Field(min_length=1)
    projectDesc: str = ""
    projectCreatorId: str = Field(min_length=1)
    budget: int = Field(ge=0)
    hardwareList: list[HardwareItem] = Field(default_factory=list)

class ProjectAction(BaseModel):
    projectId: str = Field(min_length=1)
    projectCreatorId: str = Field(min_length=1)
    userId: str = Field(min_length=1)

class ProjectSearch(BaseModel):
    projectId: str | None = None
    projectCreatorId: str | None = None