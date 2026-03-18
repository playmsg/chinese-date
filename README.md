## 大枣无损视频合并器

一个基于 `Python + PySide6 + ffmpeg` 的桌面工具，用于把同一视频的分段文件无损合并为一个文件（`-c copy`，不二次编码）。

## 环境与依赖（uv）

本项目使用 [uv](https://github.com/astral-sh/uv) 管理 Python 环境与依赖。

### 前置条件

- 已安装 `uv`
- 已安装 `ffmpeg` 并加入系统 `PATH`

### 安装依赖

```powershell
uv sync
```

### 运行

```powershell
uv run python main.py
```

## 打包为独立 exe（Windows）

```powershell
uv run pyinstaller --noconfirm --clean --windowed --onefile --name chinese-date main.py
```

输出文件在 `dist/chinese-date.exe`。

## 合并策略说明

- 采用 ffmpeg concat demuxer：`-f concat -safe 0 -i <jobfile> -c copy`
- 任务文件统一使用 `UTF-8` 和 `\n` 换行，避免旧版本里 `\r` 导致的解析异常
- 对 `mp4/m4v/mov` 输出自动追加 `-movflags +faststart`，提升播放器兼容性

> 注意：输入分段应保持编码参数一致（编码器、分辨率、帧率、音频参数等），否则 `-c copy` 可能失败或合并后异常。
