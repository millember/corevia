import pytest

from corevia.domain.entities import Task
from corevia.domain.enum import ScheduleType, TaskType
from corevia.domain.errors import InvalidScheduleError, InvalidTaskError
from corevia.domain.policies import TaskPolicy


def make_task(
    *,
    name: str = "Test",
    command: str = "print('ok')",
    schedule_type: ScheduleType = ScheduleType.MANUAL,
    schedule_config: dict | None = None,
) -> Task:
    return Task(
        id=None,
        name=name,
        group_id=None,
        task_type=TaskType.PYTHON,
        command=command,
        enabled=True,
        schedule_type=schedule_type,
        schedule_config=({} if schedule_config is None else schedule_config),
    )


def test_valid_manual_task() -> None:
    TaskPolicy.validate(make_task())


def test_empty_name_is_rejected() -> None:
    with pytest.raises(InvalidTaskError):
        TaskPolicy.validate(make_task(name="   "))


def test_empty_command_is_rejected() -> None:
    with pytest.raises(InvalidTaskError):
        TaskPolicy.validate(make_task(command="   "))


@pytest.mark.parametrize(
    ("schedule_type", "schedule_config"),
    [
        (ScheduleType.STARTUP, {}),
        (
            ScheduleType.DAILY,
            {"hour": 12, "minute": 30},
        ),
        (
            ScheduleType.WEEKLY,
            {
                "hour": 12,
                "minute": 30,
                "day_of_week": "mon",
            },
        ),
        (
            ScheduleType.INTERVAL,
            {"minutes": 10},
        ),
        (
            ScheduleType.ONE_TIME,
            {"run_date": "2026-09-10T12:00:00"},
        ),
    ],
)
def test_valid_schedules(
    schedule_type: ScheduleType,
    schedule_config: dict,
) -> None:
    TaskPolicy.validate(
        make_task(
            schedule_type=schedule_type,
            schedule_config=schedule_config,
        )
    )


@pytest.mark.parametrize(
    "schedule_config",
    [
        {"hour": -1, "minute": 30},
        {"hour": 24, "minute": 30},
        {"hour": 12, "minute": -1},
        {"hour": 12, "minute": 60},
    ],
)
def test_invalid_time_is_rejected(
    schedule_config: dict,
) -> None:
    with pytest.raises(InvalidScheduleError):
        TaskPolicy.validate(
            make_task(
                schedule_type=ScheduleType.DAILY,
                schedule_config=schedule_config,
            )
        )


def test_invalid_weekday_is_rejected() -> None:
    with pytest.raises(InvalidScheduleError):
        TaskPolicy.validate(
            make_task(
                schedule_type=ScheduleType.WEEKLY,
                schedule_config={
                    "hour": 12,
                    "minute": 30,
                    "day_of_week": "wrong",
                },
            )
        )


@pytest.mark.parametrize("minutes", [0, -1])
def test_invalid_interval_is_rejected(minutes: int) -> None:
    with pytest.raises(InvalidScheduleError):
        TaskPolicy.validate(
            make_task(
                schedule_type=ScheduleType.INTERVAL,
                schedule_config={"minutes": minutes},
            )
        )


def test_one_time_without_run_date_is_rejected() -> None:
    with pytest.raises(InvalidScheduleError):
        TaskPolicy.validate(
            make_task(
                schedule_type=ScheduleType.ONE_TIME,
                schedule_config={},
            )
        )
