import json
from datetime import UTC, datetime

from sqlalchemy import delete, select, update

from corevia.domain.entities import Task
from corevia.domain.errors import TaskNotFoundError
from corevia.infrastructure.common.database import SessionFactory
from corevia.infrastructure.common.mapper.mappers import TaskMapper
from corevia.infrastructure.common.orm.models import TaskORM


class SQLAlchemyTaskRepository:
    @staticmethod
    def create(task: Task) -> Task:
        model = TaskMapper.to_orm(task)

        with SessionFactory() as session:
            session.add(model)
            session.commit()
            session.refresh(model)
            return TaskMapper.to_domain(model)

    @staticmethod
    def get_by_id(task_id: int) -> Task:
        with SessionFactory() as session:
            model = session.get(TaskORM, task_id)

            if model is None:
                raise TaskNotFoundError(f"Task {task_id} not found.")

            return TaskMapper.to_domain(model)

    @staticmethod
    def list_all(group_id: int | None = None) -> list[Task]:
        statement = select(TaskORM)

        if group_id is not None:
            statement = statement.where(TaskORM.group_id == group_id)
        statement = statement.order_by(TaskORM.id.desc())

        with SessionFactory() as session:
            models = session.scalars(statement).all()
            return [TaskMapper.to_domain(model) for model in models]

    @staticmethod
    def list_enabled() -> list[Task]:
        statement = (
            select(TaskORM).where(TaskORM.enabled.is_(True)).order_by(TaskORM.id)
        )
        with SessionFactory() as session:
            models = session.scalars(statement).all()
            return [TaskMapper.to_domain(model) for model in models]

    @staticmethod
    def update(task: Task) -> Task:
        if task.id is None:
            raise ValueError("Task id is required.")

        with SessionFactory() as session:
            model = session.get(TaskORM, task.id)

            if model is None:
                raise TaskNotFoundError(f"Task {task.id} not found.")

            model.name = task.name
            model.group_id = task.group_id
            model.task_type = task.task_type.value
            model.command = task.command
            model.enabled = task.enabled
            model.schedule_type = task.schedule_type.value
            model.schedule_config = json.dumps(
                task.schedule_config,
                ensure_ascii=False,
            )
            model.updated_at = datetime.now(UTC)

            session.commit()
            session.refresh(model)

            return TaskMapper.to_domain(model)

    @staticmethod
    def delete(task_id: int) -> None:
        statement = delete(TaskORM).where(TaskORM.id == task_id)

        with SessionFactory() as session:
            session.execute(statement)
            session.commit()

    @staticmethod
    def set_enabled(task_id: int, enabled: bool) -> None:
        statement = (
            update(TaskORM)
            .where(TaskORM.id == task_id)
            .values(
                enabled=enabled,
                updated_at=datetime.now(UTC),
            )
        )

        with SessionFactory() as session:
            session.execute(statement)
            session.commit()

    @staticmethod
    def set_group_enabled(group_id: int, enabled: bool) -> None:
        statement = (
            update(TaskORM)
            .where(TaskORM.group_id == group_id)
            .values(
                enabled=enabled,
                updated_at=datetime.now(UTC),
            )
        )

        with SessionFactory() as session:
            session.execute(statement)
            session.commit()
