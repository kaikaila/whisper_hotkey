Whisper Hotkey Readme

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



