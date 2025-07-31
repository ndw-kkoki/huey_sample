# main.py - メインプロセスを起動するスクリプト

from app.tasks import task_a, task_b, task_c

def main():
    """メイン関数"""
    print("Starting main process...")

    # タスクaとタスクbを非同期で実行
    a = task_a(1)
    b = task_b(2)

    # タスクaとタスクbの完了を待つ
    a_result = a.get(blocking=True)
    b_result = b.get(blocking=True)

    # タスクcを実行し、結果を表示
    c = task_c([a_result, b_result])
    print("Final result:", c.get(blocking=True))

if __name__ == "__main__":
    main()
