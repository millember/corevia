from datetime import UTC, datetime

from sqlalchemy import select

from corevia.domain.entities import TaskRun
from corevia.domain.enum import RunSource, RunStatus
from corevia.infrastructure.common.database import SessionFactory
from corevia.infrastructure.common.mapper.mappers import RunMapper
from corevia.infrastructure.common.orm.models import TaskRunORM


class SQLAlchemyRunRepository:
    @staticmethod
    def create_running(task_id: int, source: RunSource) -> TaskRun:
        model = TaskRunORM(
            task_id=task_id,
            started_at=datetime.now(UTC),
            finished_at=None,
            status=RunStatus.RUNNING.value,
            exit_code=None,
            stdout="",
            stderr="",
            source=source.value,
        )
        with SessionFactory() as session:
            session.add(model)
            session.commit()
            session.refresh(model)
            return RunMapper.to_domain(model)

    @staticmethod
    def finish(
        run_id: int,
        status: RunStatus,
        exit_code: int,
        stdout: str,
        stderr: str,
    ) -> TaskRun:
        with SessionFactory() as session:
            model = session.get(TaskRunORM, run_id)

            if model is None:
                raise ValueError(f"Run {run_id} not found.")

            model.finished_at = datetime.now(UTC)
            model.status = status.value
            model.exit_code = exit_code
            model.stdout = stdout
            model.stderr = stderr

            session.commit()
            session.refresh(model)

            return RunMapper.to_domain(model)

    @staticmethod
    def list_recent(limit: int = 200) -> list[TaskRun]:
        statement = select(TaskRunORM).order_by(TaskRunORM.id.desc()).limit(limit)

        with SessionFactory() as session:
            models = session.scalars(statement).all()
            return [RunMapper.to_domain(model) for model in models]
