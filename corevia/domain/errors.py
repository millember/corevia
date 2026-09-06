class CoreviaError(Exception):
    pass


class TaskNotFoundError(CoreviaError):
    pass


class GroupNotFoundError(CoreviaError):
    pass


class InvalidTaskError(CoreviaError):
    pass


class InvalidScheduleError(CoreviaError):
    pass
