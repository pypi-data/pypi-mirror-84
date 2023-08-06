import random as __random__
import datetime as __time__

from functools import partial as __partial__

__open_number__ = set()


def __get_debug_id__(operation_name: str) -> str:
    global __open_number__

    random_number = __random__.randint(0, 1000)
    while random_number in __open_number__:
        __random__.seed(random_number)
        random_number = __random__.randint(0, 100000)

    return f"{operation_name}_{random_number}"


def __debug_message__(_id: str, message: str) -> None:
    current_time = str(__time__.datetime.now().time())
    print(f"{current_time}::{_id}::{message}")


def __get_local_debug_logger__(operation_type: str):
    _id = __get_debug_id__(operation_type)
    return __partial__(__debug_message__, _id)
