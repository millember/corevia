from typing import Protocol

from corevia.domain.entities import Task, TaskGroup, TaskRun
from corevia.domain.enum import RunSource, RunStatus


class TaskRepositoryPort(Protocol):
    @staticmethod
    def create(task: Task) -> Task: ...

    @staticmethod
    def get_by_id(task_id: int) -> Task: ...

    @staticmethod
    def list_all(group_id: int | None = None) -> list[Task]: ...

    @staticmethod
    def list_enabled() -> list[Task]: ...

    @staticmethod
    def update(task: Task) -> Task: ...

    @staticmethod
    def delete(task_id: int) -> None: ...

    @staticmethod
    def set_enabled(task_id: int, enabled: bool) -> None: ...

    @staticmethod
    def set_group_enabled(group_id: int, enabled: bool) -> None: ...


class GroupRepositoryPort(Protocol):
    @staticmethod
    def create(name: str) -> TaskGroup: ...

    @staticmethod
    def get_by_id(group_id: int) -> TaskGroup: ...

    @staticmethod
    def list_all() -> list[TaskGroup]: ...

    @staticmethod
    def update(group_id: int, name: str) -> TaskGroup: ...

    @staticmethod
    def delete(group_id: int) -> None: ...


class RunRepositoryPort(Protocol):
    @staticmethod
    def create_running(task_id: int, source: RunSource) -> TaskRun: ...

    @staticmethod
    def finish(
        run_id: int,
        status: RunStatus,
        exit_code: int,
        stdout: str,
        stderr: str,
    ) -> TaskRun: ...

    @staticmethod
    def list_recent(limit: int = 200) -> list[TaskRun]: ...


class SettingsRepositoryPort(Protocol):
    @staticmethod
    def get(key: str, default: str | None = None) -> str | None: ...

    @staticmethod
    def set(key: str, value: str) -> None: ...
