import pytest

from corevia.domain.entities import Task
from corevia.domain.enum import ScheduleType, TaskType
from corevia.domain.errors import InvalidTaskError
from corevia.domain.policies import TaskPolicy


def make_task(
    *,
    name: str = "Test",
    command: str = "print('ok')",
) -> Task:
    return Task(
        id=None,
        name=name,
        group_id=None,
        task_type=TaskType.PYTHON,
        command=command,
        enabled=True,
        schedule_type=ScheduleType.MANUAL,
        schedule_config={},
    )


def test_valid_manual_task() -> None:
    TaskPolicy.validate(make_task())


def test_empty_name_is_rejected() -> None:
    with pytest.raises(InvalidTaskError):
        TaskPolicy.validate(make_task(name="   "))
