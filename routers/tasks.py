from fastapi import APIRouter, HTTPException
from schemas import Task, TaskCreate

router = APIRouter(prefix="/tasks", tags=["tasks"])

tasks: list[Task] = []
next_id = 1

@router.get("")
def list_tasks():
    return tasks


@router.get("/{task_id}")
def get_task(task_id:int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@router.post("", status_code=201)
def create_task(payload: TaskCreate):
    global next_id
    task = Task(id=next_id, **payload.model_dump())
    next_id += 1
    tasks.append(task)
    return task