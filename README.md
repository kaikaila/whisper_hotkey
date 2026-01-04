Whisper Hotkey Readme

# Whisper Hotkey

A macOS productivity tool that enables voice-to-text transcription with a global hotkey, automatically copying the transcribed text to your clipboard.

## Features

- 🎤 **Global Hotkey**: Press `Cmd + Shift + R` to start/stop recording
- 🌍 **Multi-language Support**: Automatic language detection
- 🔄 **Mixed Language Input**: Handles Chinese-English mixed speech
- 🧹 **Auto Cleanup**: Automatically removes temporary audio files
- 🎯 **High Accuracy**: Uses OpenAI's Whisper large model
- ⚡ **Fast**: Built with Python + ffmpeg + whisper.cpp

## Demo

Press `Cmd + Shift + R` → Speak → Press again → Text appears in clipboard!

## Prerequisites

### 1. Install ffmpeg
```bash
brew install ffmpeg
```

### 2. Build whisper.cpp
```bash
git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp
WHISPER_METAL=1 make
```

### 3. Download Whisper Model

For better accuracy, use the large-v3 model:
```bash
cd models
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3.bin
```

### 4. Install Python Dependencies
```bash
pip install pynput pyperclip
```

## macOS Permissions Setup

⚠️ **Important**: macOS requires explicit permissions for keyboard monitoring and microphone access.

### Grant Accessibility Access (for hotkey monitoring)

1. Open `System Settings` → `Privacy & Security` → `Accessibility`
2. Click the lock icon 🔒 to unlock
3. Click `+` to add an application
4. Press `Command + Shift + G` and paste your Python path:
```bash
   python3 -c "import sys; print(sys.executable)"
```
5. Ensure Python is checked

### Grant Microphone Access

1. Open `System Settings` → `Privacy & Security` → `Microphone`
2. Add `python3` and ensure it's checked

## Usage

### 1. Update Configuration

Edit `whisper_hotkey.py` and set the correct path to your `whisper-cli`:
```python
WHISPER_CLI = "/path/to/whisper.cpp/build/bin/whisper-cli"
```

### 2. Run the Script
```bash
python whisper_hotkey.py
```

You should see:
```
🔥 Press Cmd + Shift + R to start recording, press again to stop
```

### 3. Record and Transcribe

1. Press `Cmd + Shift + R` to start recording
2. Speak your message
3. Press `Cmd + Shift + R` again to stop
4. Transcribed text is automatically copied to clipboard

### Example Output
```
📋 Copied to clipboard: Hello, this is a test of Whisper-Hotkey!
🗑️ Recording file automatically deleted
```

## How It Works

1. **Hotkey Detection**: Uses `pynput` to monitor global keyboard shortcuts
2. **Audio Recording**: Captures audio via `ffmpeg` with WAV format (16kHz mono)
3. **Transcription**: Processes audio through Whisper large-v3 model using `whisper.cpp`
4. **Clipboard Integration**: Copies result using `pyperclip`
5. **Cleanup**: Removes temporary audio files automatically

## Troubleshooting

### "This process is not trusted!" Error

**Cause**: Python doesn't have Accessibility permissions.

**Solution**: Add `python3` in `System Settings` → `Privacy & Security` → `Accessibility`

### ffmpeg Cannot Record Audio

**Cause**: Python doesn't have Microphone permissions.

**Solution**: Add `python3` in `System Settings` → `Privacy & Security` → `Microphone`

### "whisper-cli not found"

**Cause**: Incorrect path to whisper.cpp CLI.

**Solution**: Find the correct path:
```bash
find ~/whisper.cpp -name "whisper-cli"
```
Update `WHISPER_CLI` in the script with the correct path.

## Technical Stack

- **Python 3.x**: Core application logic
- **ffmpeg**: Audio recording and processing
- **whisper.cpp**: Fast CPU/GPU inference for Whisper models
- **pynput**: Global hotkey monitoring
- **pyperclip**: Cross-platform clipboard operations

## Why This Project?

I built this tool to improve my productivity during my graduate studies at UC Berkeley. As someone who frequently needs to transcribe ideas, meeting notes, and multilingual content, I wanted a seamless voice-to-text solution that:
- Works offline (privacy)
- Supports multiple languages
- Integrates smoothly into my workflow
- Requires minimal interaction

## Future Improvements

- [ ] Custom hotkey configuration
- [ ] Support for other operating systems (Linux, Windows)
- [ ] GUI for easier setup
- [ ] Multiple Whisper model options
- [ ] Audio quality settings

## License

MIT License - feel free to use and modify!

## Contributing

Issues and pull requests are welcome! This was my first attempt at building a system-level productivity tool, and I'm always learning.

---

**Built with ❤️ for productivity**


Whisper-Hotkey: 语音输入到剪贴板

# 项目简介
Whisper-Hotkey 是一个 macOS 终端工具，允许你使用 全局快捷键 (Cmd + Shift + R) 进行录音，并自动调用 Whisper 进行语音转录，最终将文本复制到剪贴板。

- ✅ 支持多语言（自动检测）
- ✅ 支持中英文混合输入
- ✅ 自动删除临时音频文件
- ✅ 使用 Whisper 大模型提升准确率
- ✅ 基于 Python + ffmpeg + whisper.cpp

# 依赖安装
## 1️⃣ 安装 ffmpeg
Whisper 需要 ffmpeg 录制和处理音频，安装方式如下：

brew install ffmpeg
## 2️⃣ 安装 whisper.cpp
Whisper 是 OpenAI 的语音转文本模型，我们使用的是 whisper.cpp 版本。

git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp
然后编译它（启用 Metal 加速）：

WHISPER_METAL=1 make
## 3️⃣ 下载 Whisper 大模型（提高识别准确率）
默认 base 模型精度较低，我们使用 large-v3 模型：

cd models
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3.bin
## 4️⃣ 安装 Python 依赖
本项目依赖 pynput（监听快捷键）、pyperclip（复制到剪贴板）：

pip install pynput pyperclip
## ⚠️ macOS 额外权限配置
由于 macOS 限制应用对 键盘监听 和 麦克风录音，需要手动授权：

## 1️⃣ 允许 Python 访问“辅助功能”（用于监听快捷键）
打开 系统设置 > 隐私与安全性 > 辅助功能

解锁（左下角🔒），点击 +

输入 Command + Shift + G，粘贴 Python 路径

python3 -c "import sys; print(sys.executable)"
确保 python3 是勾选状态

## 2️⃣ 允许 Python 访问麦克风
打开 系统设置 > 隐私与安全性 > 麦克风

添加 python3，确保勾选

# 使用方法
## 1️⃣ 启动脚本
python whisper_hotkey.py
然后你会看到：

🔥 按 Cmd + Shift + R 开始录音，再按一次停止
## 2️⃣ 开始 & 停止录音
按 Cmd + Shift + R 开始录音

再按 Cmd + Shift + R 停止并转录

文本会自动复制到剪贴板

## 3️⃣ 示例输出
录音后，终端会显示：

📋 已复制到剪贴板：Hello, this is a test of Whisper-Hotkey!
🗑️ 录音文件已自动删除
# 常见问题（FAQ）
## ❓ 1. 运行时 This process is not trusted! 错误
- 原因：Python 没有辅助功能权限。 
- 解决方案：在 系统设置 > 隐私与安全性 > 辅助功能 中添加 python3。

## ❓ 2. ffmpeg 无法录音
- 原因：macOS 没有授权 python3 访问麦克风。 
- 解决方案：在 系统设置 > 隐私与安全性 > 麦克风 中添加 python3。

## ❓ 3. whisper-cli 找不到
- 原因：whisper.cpp 的 CLI 在 build/bin/ 里，而不是 bin/。 
- 解决方案：使用 find 查找并确保路径正确



