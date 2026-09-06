from dataclasses import dataclass
from datetime import datetime

from corevia.domain.enum import (
    RunSource,
    RunStatus,
    ScheduleType,
    TaskType,
)


@dataclass(frozen=True)
class TaskGroup:
    id: int | None
    name: str
    created_at: datetime | None = None


@dataclass(frozen=True)
class Task:
    id: int | None
    name: str
    group_id: int | None
    task_type: TaskType
    command: str
    enabled: bool
    schedule_type: ScheduleType
    schedule_config: dict
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass(frozen=True)
class TaskRun:
    id: int | None
    task_id: int | None
    started_at: datetime
    finished_at: datetime | None
    status: RunStatus
    exit_code: int | None
    stdout: str
    stderr: str
    source: RunSource
