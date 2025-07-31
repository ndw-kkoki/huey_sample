#  tasks.py - Hueyタスクを定義するモジュール
from huey import SqliteHuey, crontab
from time import sleep
from datetime import datetime

huey = SqliteHuey(filename='huey.db')


@huey.task()
def task_a(x):
    print(f"Running task_a with {x}")
    sleep(2)
    return f"A{x}"


@huey.task()
def task_b(x):
    print(f"Running task_b with {x}")
    sleep(3)
    return f"B{x}"


@huey.task()
def task_c(results):
    print("task_c waiting for task_a and task_b to finish...")
    a_result, b_result = results
    print(f"Received: {a_result}, {b_result}")
    return f"Combined: {a_result} + {b_result}"
