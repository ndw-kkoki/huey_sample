# run_worker.py - Hueyワーカーを起動するスクリプト

import sys

from app.tasks import huey

def run_worker():
    """Hueyワーカーを起動する"""
    print("Starting Huey worker...")
    print("Press Ctrl+C to stop")
    
    # コンシューマーを起動
    from huey.consumer import Consumer
    
    consumer = Consumer(huey)
    consumer.run()

if __name__ == "__main__":
    try:
        run_worker()
    except KeyboardInterrupt:
        print("\nWorker stopped by user")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
