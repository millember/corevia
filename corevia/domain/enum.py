from enum import StrEnum


class Language(StrEnum):
    EN = "en"
    RU = "ru"


class TaskType(StrEnum):
    PYTHON = "python"
    BASH = "bash"
    SHELL = "shell"


class ScheduleType(StrEnum):
    MANUAL = "manual"
    DAILY = "daily"
    WEEKLY = "weekly"
    STARTUP = "startup"
    ONE_TIME = "one_time"
    INTERVAL = "interval"


class RunStatus(StrEnum):
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class RunSource(StrEnum):
    MANUAL = "manual"
    SCHEDULER = "scheduler"
    GROUP = "group"
