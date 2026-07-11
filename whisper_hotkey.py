import os
import signal
import pyperclip
import subprocess
import threading
from pynput import keyboard

# 获取当前脚本所在目录
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

# Whisper CLI 的路径（相对于 `whisper-hotkey/`）
WHISPER_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "../whisper.cpp/build/bin"))

# Whisper CLI 可执行文件
WHISPER_CLI = os.path.join(WHISPER_PATH, "whisper-cli")
AUDIO_FILE = os.path.join(SCRIPT_DIR, "input.wav")

recording_process = None
is_recording = False

LANG = os.environ.get("WHISPER_HOTKEY_LANG", "zh")
MSG = {
    "zh": {
        "ready": "🔥 按 Cmd + Shift + R 开始录音，再按一次停止",
        "already_recording": "⚠️ 录音已经在进行中，忽略重复触发",
        "start": "🎙 开始录音... 按 Cmd + Shift + R 停止",
        "ffmpeg_started": "✅ ffmpeg 录音进程已启动",
        "audio_path": "🛠️ 录音文件路径: {}",
        "start_failed": "❌ 录音启动失败: {}",
        "not_recording": "⚠️ 录音未进行，忽略停止请求",
        "stopping": "⏹ 录音停止中...",
        "sending_signal": "⚠️ ffmpeg 仍在运行，发送停止信号...",
        "stopped": "✅ ffmpeg 录音进程已停止",
        "already_exited": "✅ ffmpeg 进程已经自动退出",
        "no_process": "⚠️ 未找到录音进程，跳过终止步骤",
        "no_audio": "❌ 错误: 找不到录音文件 `{}`",
        "no_cli": "❌ 错误: 无法找到 whisper-cli，路径: {}",
        "transcribing": "🚀 运行 Whisper 语音识别中...",
        "no_output": "❌ Whisper 未生成转录文件",
        "copied": "📋 已复制到剪贴板：{}",
        "exit": "\n⏹️ 进程已手动退出",
    },
    "en": {
        "ready": "🔥 Press Cmd + Shift + R to start recording, press again to stop",
        "already_recording": "⚠️ Already recording, ignoring",
        "start": "🎙 Recording... Press Cmd + Shift + R to stop",
        "ffmpeg_started": "✅ ffmpeg recording started",
        "audio_path": "🛠️ Audio file: {}",
        "start_failed": "❌ Failed to start recording: {}",
        "not_recording": "⚠️ Not recording, ignoring stop request",
        "stopping": "⏹ Stopping recording...",
        "sending_signal": "⚠️ ffmpeg still running, sending stop signal...",
        "stopped": "✅ ffmpeg recording stopped",
        "already_exited": "✅ ffmpeg already exited",
        "no_process": "⚠️ No recording process found, skipping",
        "no_audio": "❌ Audio file not found: `{}`",
        "no_cli": "❌ whisper-cli not found at: {}",
        "transcribing": "🚀 Running Whisper transcription...",
        "no_output": "❌ Whisper did not produce a transcript",
        "copied": "📋 Copied to clipboard: {}",
        "exit": "\n⏹️ Exited",
    },
}[LANG]


def start_recording():
    global recording_process, is_recording
    if is_recording:
        print(MSG["already_recording"])
        return

    is_recording = True
    print(MSG["start"])
    try:
        recording_process = subprocess.Popen(
            ["ffmpeg", "-y", "-f", "avfoundation", "-i", ":0",
             "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", AUDIO_FILE],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        print(MSG["ffmpeg_started"])
        print(MSG["audio_path"].format(AUDIO_FILE))
    except Exception as e:
        print(MSG["start_failed"].format(e))


def stop_recording():
    global recording_process, is_recording
    if not is_recording:
        print(MSG["not_recording"])
        return

    is_recording = False
    print(MSG["stopping"])

    if recording_process:
        if recording_process.poll() is None:
            print(MSG["sending_signal"])
            recording_process.send_signal(signal.SIGINT)
            try:
                recording_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                recording_process.kill()
                recording_process.wait()
            print(MSG["stopped"])
        else:
            print(MSG["already_exited"])

        recording_process = None
    else:
        print(MSG["no_process"])

    process_audio()


def process_audio():
    if not os.path.exists(AUDIO_FILE):
        print(MSG["no_audio"].format(AUDIO_FILE))
        return

    if not os.path.exists(WHISPER_CLI):
        print(MSG["no_cli"].format(WHISPER_CLI))
        return

    model_path = os.path.join(SCRIPT_DIR, "../whisper.cpp/models/ggml-large-v3.bin")
    print(MSG["transcribing"])
    result = subprocess.run(
        [WHISPER_CLI, "-m", os.path.abspath(model_path),
         "-f", AUDIO_FILE, "--threads", "8", "-l", "auto", "--output-txt"],
        capture_output=True, text=True
    )

    txt_file = AUDIO_FILE + ".txt"
    if not os.path.exists(txt_file):
        print(MSG["no_output"])
        print(f"stderr: {result.stderr[-500:]}" if result.stderr else "")
        return

    with open(txt_file, "r") as f:
        transcript = f.read().strip()

    pyperclip.copy(transcript)
    print(MSG["copied"].format(transcript))

    try:
        os.remove(txt_file)
    except OSError:
        pass


def toggle_recording():
    threading.Thread(target=start_recording if not is_recording else stop_recording).start()


def start_hotkey_listener():
    print(MSG["ready"])

    try:
        with keyboard.GlobalHotKeys({'<cmd>+<shift>+r': toggle_recording}) as h:
            h.join()
    except KeyboardInterrupt:
        print(MSG["exit"])


if __name__ == "__main__":
    start_hotkey_listener()