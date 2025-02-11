import os
import pyperclip
import subprocess
import threading
from pynput import keyboard

WHISPER_PATH = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本目录
AUDIO_FILE = os.path.join(WHISPER_PATH, "input.wav")  # 录音文件
FIXED_AUDIO_FILE = os.path.join(WHISPER_PATH, "input_fixed.wav")  # 16kHz 版本

recording_process = None  # 录音进程
is_recording = False  # 录音状态


def start_recording():
    """ 开始录音 """
    global recording_process, is_recording
    if is_recording:
        print("⚠️ 录音已经在进行中，忽略重复触发")
        return  # 避免重复触发

    is_recording = True
    print("🎙 开始录音... 按 Cmd + Shift + R 停止")
    try:
        recording_process = subprocess.Popen(
            ["ffmpeg", "-f", "avfoundation", "-i", ":0", AUDIO_FILE],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        print("✅ `ffmpeg` 录音进程已启动")
    except Exception as e:
        print(f"❌ 录音启动失败: {e}")


def stop_recording():
    """ 停止录音，转换格式，进行语音识别 """
    global recording_process, is_recording
    if not is_recording:
        print("⚠️ 录音未进行，忽略停止请求")
        return  # 避免错误触发

    is_recording = False
    print("⏹ 录音停止中...")

    if recording_process:
        print("🔍 检查 `ffmpeg` 是否还在运行...")
        if recording_process.poll() is None:
            print("⚠️ `ffmpeg` 仍在运行，尝试强制终止")
            recording_process.kill()  # 直接 kill 进程
            recording_process.wait()
            print("✅ `ffmpeg` 录音进程已强制终止")
        else:
            print("✅ `ffmpeg` 进程已经自动退出")

        recording_process = None
    else:
        print("⚠️ 未找到录音进程，跳过终止步骤")

    print("🔄 正在调用 `process_audio()`...")
    process_audio()


def process_audio():
    """ 转换音频格式并运行 Whisper 识别 """
    print("🔄 进入 `process_audio()` 方法")

    if not os.path.exists(AUDIO_FILE):
        print(f"❌ 错误: 找不到录音文件 `{AUDIO_FILE}`")
        return

    print("🔄 转换音频格式（16kHz）...")
    subprocess.run(
        ["ffmpeg", "-i", AUDIO_FILE, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", FIXED_AUDIO_FILE],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    if not os.path.exists(FIXED_AUDIO_FILE):
        print(f"❌ 错误: 16kHz 转换失败，`{FIXED_AUDIO_FILE}` 文件不存在")
        return

    # **自动查找 `whisper-cli` 的路径**
    possible_paths = [
        os.path.join(WHISPER_PATH, "bin/whisper-cli"),
        os.path.join(WHISPER_PATH, "build/bin/whisper-cli"),
    ]
    whisper_cli_path = next((p for p in possible_paths if os.path.exists(p)), None)

    if not whisper_cli_path:
        print(f"❌ 错误: 无法找到 `whisper-cli`，请检查 `bin/` 或 `build/bin/` 目录")
        return

    print(f"🚀 运行 Whisper 语音识别中（使用 {whisper_cli_path}）...")
    result = subprocess.run(
        [whisper_cli_path, "-m", f"{WHISPER_PATH}/models/ggml-large-v3.bin",
         "-f", FIXED_AUDIO_FILE, "--threads", "8", "-l", "auto", "--output-txt"],
        capture_output=True, text=True
    )

    transcript = result.stdout.strip()
    if transcript:
        pyperclip.copy(transcript)
        print(f"📋 已复制到剪贴板：{transcript}")
    else:
        print("⚠️ Whisper 识别结果为空，请检查录音内容")

    # **自动删除音频**
    try:
        os.remove(AUDIO_FILE)
        os.remove(FIXED_AUDIO_FILE)
        print("🗑️ 录音文件已自动删除")
    except Exception as e:
        print(f"⚠️ 删除文件时出错: {e}")


def on_press(key):
    """ 监听快捷键 Cmd + Shift + R """
    if key == keyboard.KeyCode.from_char('r'):
        threading.Thread(target=start_recording if not is_recording else stop_recording).start()


def start_hotkey_listener():
    """ 监听快捷键 """
    print("🔥 按 Cmd + Shift + R 开始录音，再按一次停止")

    try:
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    except KeyboardInterrupt:
        print("\n⏹️ 进程已手动退出")


if __name__ == "__main__":
    start_hotkey_listener()