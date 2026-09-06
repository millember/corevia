from sqlalchemy import delete, select, update

from corevia.domain.entities import TaskGroup
from corevia.domain.errors import GroupNotFoundError
from corevia.infrastructure.common.database import SessionFactory
from corevia.infrastructure.common.mapper.mappers import GroupMapper
from corevia.infrastructure.common.orm.models import TaskGroupORM


class SQLAlchemyGroupRepository:
    @staticmethod
    def create(name: str) -> TaskGroup:
        model = TaskGroupORM(name=name.strip())

        with SessionFactory() as session:
            session.add(model)
            session.commit()
            session.refresh(model)
            return GroupMapper.to_domain(model)

    @staticmethod
    def get_by_id(group_id: int) -> TaskGroup:
        with SessionFactory() as session:
            model = session.get(TaskGroupORM, group_id)

            if model is None:
                raise GroupNotFoundError(f"Group {group_id} not found.")

            return GroupMapper.to_domain(model)

    @staticmethod
    def list_all() -> list[TaskGroup]:
        statement = select(TaskGroupORM).order_by(TaskGroupORM.name)

        with SessionFactory() as session:
            models = session.scalars(statement).all()
            return [GroupMapper.to_domain(model) for model in models]

    @staticmethod
    def update(group_id: int, name: str) -> TaskGroup:
        statement = (
            update(TaskGroupORM)
            .where(TaskGroupORM.id == group_id)
            .values(name=name.strip())
        )

        with SessionFactory() as session:
            session.execute(statement)
            session.commit()

        return SQLAlchemyGroupRepository.get_by_id(group_id)

    @staticmethod
    def delete(group_id: int) -> None:
        statement = delete(TaskGroupORM).where(TaskGroupORM.id == group_id)

        with SessionFactory() as session:
            session.execute(statement)
            session.commit()
