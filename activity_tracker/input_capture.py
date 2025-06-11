# activity_tracker/input_capture.py

from pynput import keyboard
from collections import deque
import pyperclip
import easygui
import pyautogui
import time

from utils.time_utils import get_timestamp
from utils.window_utils import get_active_window_title
from db.manager import save_question

recent_keys = deque(maxlen=10)

def is_clipboard_changed():
    before_clip = pyperclip.paste()
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.2)
    after_clip = pyperclip.paste()
    if after_clip.strip() == before_clip.strip():
        print("[경고] 클립보드 내용 변경 안 됨 → 복사 실패 또는 중복")
        return False
    return True

def handle_ctrl_q_triggered():
    print("[Ctrl+Q] 감지됨 - 자동 복사 시도 중...")
    recent_keys.clear()

    try:
        if not is_clipboard_changed():
            return
        highlight = pyperclip.paste().strip()
    except Exception as e:
        print(f"[에러] 클립보드 복사 실패 (보안 앱 등): {e}")
        return

    if not highlight:
        print("[무시됨] 드래그된 텍스트 없음 → 입력 중단")
        return

    memo = easygui.enterbox("메모를 입력하세요:")
    ts = get_timestamp()

    entry = {
        "id": ts,
        "timestamp": ts,
        "highlight": highlight,
        "memo": memo or "",
        "source": get_active_window_title()
    }

    save_question(entry)
    print(f"✅ 질문 저장됨: {entry['id']}")

def on_key_press(key):
    try:
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            recent_keys.append('ctrl')
        elif isinstance(key, keyboard.KeyCode):
            char = key.char
            if char == '\x11':
                recent_keys.append('q')
            else:
                recent_keys.append(char.lower())
    except Exception as e:
        print(f"[오류] 키 처리 실패: {e}")

def on_ctrl_trigger():
    print('🔑 Ctrl+Q 조합 감지됨')
    handle_ctrl_q_triggered()

def start_input_capture():
    print("🟢 입력 감지 시작됨 (Ctrl+Q 대기 중)")
    keyboard.Listener(on_press=on_key_press).start()
    keyboard.GlobalHotKeys({
        '<ctrl>+q': on_ctrl_trigger
    }).start()