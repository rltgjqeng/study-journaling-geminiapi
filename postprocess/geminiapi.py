import os
import json
import time
import PIL.Image
from utils.id_utils import generate_uuid
from db import manager
import google.generativeai as genai

# ==== 설정 ====
STATE_PATH = os.path.join("postprocess", "state.json")
DEFAULT_EVENT_ID = "00000000_000000"

# ==== Gemini 초기화 ====
genai.configure(api_key=os.getenv("GOOGLE_AI_KEY", ""))
model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat(history=[])

# ==== 프롬프트 정의 ====
prompt = (
    "Given the image, extract up to 3 questions a user might ask about it. "
    "Only return the questions, each on its own line. No extra explanation."
)

# ==== 상태 불러오기 / 저장 ====
def load_last_event_id():
    if not os.path.exists(STATE_PATH):
        return DEFAULT_EVENT_ID
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        state = json.load(f)
    return state.get("last_event_processed", DEFAULT_EVENT_ID)

def save_last_event_id(event_id):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump({"last_event_processed": event_id}, f, indent=2)

# ==== 이벤트 처리 ====
def process_event(event):
    try:
        img = PIL.Image.open(event["screenshot_path"])
    except Exception as e:
        print(f"[ERROR] Cannot open image: {event['screenshot_path']} ({e})")
        return []

    try:
        response = chat.send_message(
            content=[prompt, img],
            generation_config=genai.GenerationConfig(max_output_tokens=256, temperature=0.4)
        )
        text = response.text.strip()
        questions = [q.strip("-• ") for q in text.splitlines() if len(q.strip()) > 5]
    except Exception as e:
        print(f"[ERROR] Gemini API failed on event {event['event_id']}: {e}")
        return []

    if questions:
        full_text = "\n".join(questions)
        return [{
            "id": generate_uuid(),
            "event_id": event["event_id"],
            "timestamp": event["timestamp"],
            "source": event["source"],
            "question_text": full_text,
            "confirmed": 0
        }]
    else:
        return []

# ==== 실행 진입점 ====
def run_process():
    last_event_id = load_last_event_id()
    print(f"[INFO] Last processed event_id: {last_event_id}")

    all_events = manager.load_candidate_events_after("1970-01-01T00:00:00")  # timestamp 기준 정렬됨
    events = []
    seen = False if last_event_id != DEFAULT_EVENT_ID else True

    for ev in all_events:
        if seen:
            events.append(ev)
        elif ev["event_id"] == last_event_id:
            seen = True

    print(f"[INFO] Found {len(events)} new events to process")

    for event in events:
        print(f"[PROCESSING] {event['event_id']}")
        candidates = process_event(event)
        if candidates:
            manager.save_question_candidates(candidates)
            print(f"[SAVED] {len(candidates)} question(s) saved")
        else:
            print("[SKIPPED] No questions extracted")
        save_last_event_id(event["event_id"])
        time.sleep(0.5)  # 약간의 딜레이 (API 과부하 방지)

if __name__ == "__main__":
    run_process()
