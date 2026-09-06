import json

from corevia.domain.entities import Task, TaskGroup, TaskRun
from corevia.domain.enum import RunSource, RunStatus, ScheduleType, TaskType
from corevia.infrastructure.common.orm.models import (
    TaskGroupORM,
    TaskORM,
    TaskRunORM,
)


class TaskMapper:
    @staticmethod
    def to_domain(model: TaskORM) -> Task:
        return Task(
            id=model.id,
            name=model.name,
            group_id=model.group_id,
            task_type=TaskType(model.task_type),
            command=model.command,
            enabled=model.enabled,
            schedule_type=ScheduleType(model.schedule_type),
            schedule_config=json.loads(model.schedule_config or "{}"),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_orm(task: Task) -> TaskORM:
        return TaskORM(
            name=task.name,
            group_id=task.group_id,
            task_type=task.task_type.value,
            command=task.command,
            enabled=task.enabled,
            schedule_type=task.schedule_type.value,
            schedule_config=json.dumps(task.schedule_config, ensure_ascii=False),
        )


class GroupMapper:
    @staticmethod
    def to_domain(model: TaskGroupORM) -> TaskGroup:
        return TaskGroup(
            id=model.id,
            name=model.name,
            created_at=model.created_at,
        )


class RunMapper:
    @staticmethod
    def to_domain(model: TaskRunORM) -> TaskRun:
        return TaskRun(
            id=model.id,
            task_id=model.task_id,
            started_at=model.started_at,
            finished_at=model.finished_at,
            status=RunStatus(model.status),
            exit_code=model.exit_code,
            stdout=model.stdout,
            stderr=model.stderr,
            source=RunSource(model.source),
        )
