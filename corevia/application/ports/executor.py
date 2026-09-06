from dataclasses import dataclass
from typing import Protocol

from corevia.domain.entities import Task


@dataclass(frozen=True)
class ExecutionResult:
    exit_code: int
    stdout: str
    stderr: str


class TaskExecutorPort(Protocol):
    @staticmethod
    def execute(task: Task) -> ExecutionResult: ...
