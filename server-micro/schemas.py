from pydantic import BaseModel, Field

class ProjectCreate(BaseModel):
    projectId: str = Field(min_length=1)
    projectName: str = Field(min_length=1)
    projectDesc: str = ""
    projectCreatorId: str = Field(min_length=1)

class ProjectAction(BaseModel):
    projectId: str = Field(min_length=1)
    projectCreatorId: str = Field(min_length=1)
    userId: str = Field(min_length=1)