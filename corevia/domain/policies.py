from corevia.domain.entities import Task
from corevia.domain.enum import ScheduleType
from corevia.domain.errors import InvalidScheduleError, InvalidTaskError


class TaskPolicy:
    @staticmethod
    def validate(task: Task) -> None:
        if not task.name.strip():
            raise InvalidTaskError("Task name must not be empty.")

        if not task.command.strip():
            raise InvalidTaskError("Task command must not be empty.")

        config = task.schedule_config

        match task.schedule_type:
            case ScheduleType.MANUAL | ScheduleType.STARTUP:
                return
            case ScheduleType.DAILY:
                TaskPolicy._validate_time(config)
            case ScheduleType.WEEKLY:
                TaskPolicy._validate_time(config)
                if config.get("day_of_week") not in {
                    "mon",
                    "tue",
                    "wed",
                    "thu",
                    "fri",
                    "sat",
                    "sun",
                }:
                    raise InvalidScheduleError("Invalid day_of_week.")
            case ScheduleType.INTERVAL:
                if int(config.get("minutes", 0)) < 1:
                    raise InvalidScheduleError("Interval must be >= 1 minute.")
            case ScheduleType.ONE_TIME:
                if not config.get("run_date"):
                    raise InvalidScheduleError("run_date is required.")

    @staticmethod
    def _validate_time(config: dict) -> None:
        hour = int(config.get("hour", -1))
        minute = int(config.get("minute", -1))

        if not 0 <= hour <= 23:
            raise InvalidScheduleError("Invalid hour.")

        if not 0 <= minute <= 59:
            raise InvalidScheduleError("Invalid minute.")
