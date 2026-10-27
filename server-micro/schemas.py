from pydantic import BaseModel, Field

class ProjectCreate(BaseModel):
    projectId: str = Field(min_length=1)
    projectName: str = Field(min_length=1)
    projectDesc: str = ""
    projectCreatorId: str = Field(min_length=1)
    budget: int = Field(ge=0)

class ProjectAction(BaseModel):
    projectId: str = Field(min_length=1)
    projectCreatorId: str = Field(min_length=1)
    userId: str = Field(min_length=1)

class ProjectSearch(BaseModel):
    projectId: str | None = None
    projectCreatorId: str | None = None