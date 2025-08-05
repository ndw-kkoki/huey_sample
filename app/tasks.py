#  tasks.py - Hueyタスクを定義するモジュール
from huey import SqliteHuey, crontab
from time import sleep
from datetime import datetime
import pytz

huey = SqliteHuey(filename='huey.db')

from app.utils import run_python_script


@huey.task()
def task_a(x):
    print(f"Running task_a with {x}")
    # sample_function()         # 関数を呼び出し
    # subprocess_function()     # サブプロセスを利用した関数を呼び出し
    run_python_script()       # サブプロセスでPythonファイルを実行
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


# ===== Periodic Tasks (定期実行タスク) =====

# 3分ごとに実行される定期タスク
# @huey.periodic_task(crontab(minute='*/3'))  # 3分ごと実行
# def periodic_task_every_3_minutes():
#     """3分ごとに実行される定期タスク（他のタスクを呼び出し）"""
#     print(f"[{datetime.now()}] 3分ごとの定期タスク - 他のタスクを実行します")

#     # タスクaとタスクbを非同期で実行
#     a = task_a(1)
#     b = task_b(2)

#     # タスクaとタスクbの完了を待つ
#     a_result = a.get(blocking=True)
#     b_result = b.get(blocking=True)

#     # タスクcを実行し、結果を表示
#     c = task_c([a_result, b_result])
#     print(f"タスク実行完了: {c.get(blocking=True)}")

#     return "periodic_3min_done"


# JST 15:00に実行される定期タスク
str_jst_time = "15:00"
jst_datetime = datetime.strptime(str_jst_time, '%H:%M')
jst_now_datetime = datetime.now(pytz.timezone('Asia/Tokyo')).replace(hour=jst_datetime.hour, minute=jst_datetime.minute, second=0, microsecond=0)
utc_datetime = jst_now_datetime.astimezone(pytz.UTC)
print(f"JST {str_jst_time} -> UTC {utc_datetime.strftime('%H:%M')}")

@huey.periodic_task(crontab(hour=utc_datetime.hour, minute=utc_datetime.minute))
def my_task():
    """定期タスク"""
    print(f"[{datetime.now()}] 定期タスクが実行されました")

    # タスクaとタスクbを非同期で実行
    a = task_a(1)
    b = task_b(2)

    # タスクaとタスクbの完了を待つ
    a_result = a.get(blocking=True)
    b_result = b.get(blocking=True)

    # タスクcを実行し、結果を表示
    c = task_c([a_result, b_result])
    print(f"タスク実行完了: {c.get(blocking=True)}")

    # タスクの処理
    return "my_task_done"

