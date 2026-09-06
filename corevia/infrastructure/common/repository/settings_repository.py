from corevia.infrastructure.common.database import SessionFactory
from corevia.infrastructure.common.orm.models import AppSettingORM


class SQLAlchemySettingsRepository:
    @staticmethod
    def get(key: str, default: str | None = None) -> str | None:
        with SessionFactory() as session:
            model = session.get(AppSettingORM, key)
            return default if model is None else model.value

    @staticmethod
    def set(key: str, value: str) -> None:
        with SessionFactory() as session:
            model = session.get(AppSettingORM, key)

            if model is None:
                session.add(AppSettingORM(key=key, value=value))
            else:
                model.value = value

            session.commit()
