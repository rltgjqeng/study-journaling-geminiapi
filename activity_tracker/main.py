# activity_tracker/main.py
import threading
import time
import json

from input_capture import start_input_capture
from tracking.event_tracker import track_user_inactivity
from db.manager import init_db

def load_config():
    try:
        with open("config.json") as f:
            config = json.load(f)
            return config.get("inactivity_threshold", 10)
    except Exception as e:
        print(f"[설정 불러오기 실패] 기본값 사용: {e}")
        return 10

if __name__ == "__main__":
    init_db()
    threshold = load_config()

    t_input = threading.Thread(target=start_input_capture, daemon=True)
    t_event = threading.Thread(target=lambda: track_user_inactivity(threshold), daemon=True)

    t_input.start()
    t_event.start()

    print("🚀 실시간 시스템 작동 중 (Ctrl+C로 종료)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 시스템 종료됨")