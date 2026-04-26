from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from datetime import date

app = FastAPI(
    title="DevJourney API" \
    "",
    description="API simples para registrar projetos e acompanhar a evolução como desenvolvedor.",
    version="1.0.0"
)

class ProjectRequest(BaseModel):
    title: str = Field(..., min_length=3, example="DevJourney API")
    description: str = Field(..., min_length=10, example="API para registrar minha evolução como desenvolvedor.")
    technology: str = Field(..., example="Python, FastAPI")
    status: str = Field(..., example="Concluído")

class Project(ProjectRequest):
    id: int
    created_at: date

projects: List[Project] = []
next_id = 1

@app.get("/")
def home():
    return {
        "message": "DevJourney API está online!",
        "docs": "/docs"
    }

@app.post("/projects", response_model=Project, status_code=201)
def create_project(request: ProjectRequest):
    global next_id

    project = Project(
        id=next_id,
        title=request.title,
        description=request.description,
        technology=request.technology,
        status=request.status,
        created_at=date.today()
    )

    projects.append(project)
    next_id += 1

    return project

@app.get("/projects", response_model=List[Project])
def list_projects():
    return projects

@app.get("/projects/{project_id}", response_model=Project)
def get_project(project_id: int):
    for project in projects:
        if project.id == project_id:
            return project

    raise HTTPException(status_code=404, detail="Projeto não encontrado")

@app.delete("/projects/{project_id}")
def delete_project(project_id: int):
    for index, project in enumerate(projects):
        if project.id == project_id:
            projects.pop(index)
            return {"message": "Projeto removido com sucesso"}

    raise HTTPException(status_code=404, detail="Projeto não encontrado")

@app.get("/summary")
def get_summary():
    total_projects = len(projects)

    technologies = [project.technology for project in projects]

    return {
        "total_projects": total_projects,
        "technologies_used": technologies,
        "message": "Você está construindo uma base sólida como desenvolvedor backend."
    }