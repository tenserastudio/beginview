# BeginView

**シンプルな画像スライドショービューア for Windows**

[English](#english) | [日本語](#日本語)

---

## 日本語

### 概要

BeginView は、指定したフォルダ内の画像を自動的にスライドショー表示するシンプルなビューアアプリです。  
インストール不要のポータブルアプリケーションで、軽量で使いやすい設計になっています。

### 主な機能

- 📁 **フォルダ選択による画像読み込み**
  - JPEG (.jpg, .jpeg) と PNG (.png) に対応
  - サブフォルダを含めた再帰的な読み込みも可能

- 🎬 **自動スライドショー**
  - デフォルト3秒間隔で自動切り替え
  - 1秒～10秒、またはカスタム間隔（0.1秒～3600秒）を設定可能

- ⌨️ **豊富なキーボード操作**
  - `Space`: 再生/一時停止
  - `←` `→`: 前/次の画像へ移動
  - `F11`: フルスクリーン表示
  - `+` `-`: ズームイン/アウト
  - `0`: 100%表示（等倍）
  - `F`: ウィンドウにフィット
  - `I`: 画像情報を表示

- 🖱️ **マウス操作**
  - クリック: 再生/一時停止をトグル
  - ダブルクリック: フルスクリーンをトグル
  - ホイール: ズームイン/アウト

- 🌐 **多言語対応**
  - 日本語 / 英語の切り替えが可能

### 対応OS

- **Windows 10 / 11** (64bit)

### ダウンロード

GitHub Releases から最新版の `BeginView.exe` をダウンロードしてください。

👉 **[GitHub Releases](https://github.com/your-username/beginview/releases)**

### インストール方法

**インストール不要です！**  
ダウンロードした `BeginView.exe` を任意のフォルダに配置し、ダブルクリックで起動できます。

### 使い方

1. `BeginView.exe` を起動
2. メニューバーから `File > Open Folder...` を選択して画像フォルダを指定
3. 自動的にスライドショーが開始されます

#### 基本操作

| 操作 | キー/操作 |
|------|----------|
| 再生/一時停止 | `Space` または 画像をクリック |
| 次の画像 | `→` |
| 前の画像 | `←` |
| フルスクリーン | `F11` または 画像をダブルクリック |
| ズームイン | `+` または マウスホイール上 |
| ズームアウト | `-` または マウスホイール下 |
| 100%表示 | `0` |
| ウィンドウにフィット | `F` |
| 画像情報表示 | `I` |

#### 設定

- **スライドショー間隔**: `Settings > Slide Show Interval` から選択
- **サブフォルダを含める**: `Settings > Include Subfolders` をチェック
- **言語切り替え**: `Language > 日本語 / English` を選択

### 不具合報告

不具合を発見した場合や、機能要望がある場合は、GitHub の Issues から報告してください。

👉 **[GitHub Issues](https://github.com/your-username/beginview/issues)**

### 免責事項

本アプリは個人開発・実験目的で作成されたアプリケーションです。  
使用により生じた損害について、開発者は一切の責任を負いません。

### 技術情報

本アプリは **Python + PySide6** で開発されています。  
PySide6 は LGPL ライセンスの下で提供されています。

---

## English

### Overview

BeginView is a simple image slideshow viewer application that automatically displays images from a selected folder.  
It's a portable application that requires no installation, designed to be lightweight and easy to use.

### Key Features

- 📁 **Image Loading from Folder**
  - Supports JPEG (.jpg, .jpeg) and PNG (.png)
  - Optional recursive loading including subfolders

- 🎬 **Automatic Slideshow**
  - Auto-advance with default 3-second interval
  - Configurable from 1 to 10 seconds, or custom interval (0.1 to 3600 seconds)

- ⌨️ **Rich Keyboard Controls**
  - `Space`: Play/Pause
  - `←` `→`: Previous/Next image
  - `F11`: Fullscreen display
  - `+` `-`: Zoom in/out
  - `0`: 100% view (actual size)
  - `F`: Fit to window
  - `I`: Show image information

- 🖱️ **Mouse Controls**
  - Click: Toggle play/pause
  - Double-click: Toggle fullscreen
  - Wheel: Zoom in/out

- 🌐 **Multi-language Support**
  - Switch between Japanese and English

### System Requirements

- **Windows 10 / 11** (64bit)

### Download

Download the latest `BeginView.exe` from GitHub Releases.

👉 **[GitHub Releases](https://github.com/your-username/beginview/releases)**

### Installation

**No installation required!**  
Simply place the downloaded `BeginView.exe` in any folder and double-click to launch.

### Usage

1. Launch `BeginView.exe`
2. Select `File > Open Folder...` from the menu bar and specify an image folder
3. The slideshow will start automatically

#### Basic Controls

| Action | Key/Operation |
|--------|--------------|
| Play/Pause | `Space` or Click image |
| Next image | `→` |
| Previous image | `←` |
| Fullscreen | `F11` or Double-click image |
| Zoom in | `+` or Mouse wheel up |
| Zoom out | `-` or Mouse wheel down |
| 100% view | `0` |
| Fit to window | `F` |
| Show image info | `I` |

#### Settings

- **Slideshow Interval**: Select from `Settings > Slide Show Interval`
- **Include Subfolders**: Check `Settings > Include Subfolders`
- **Language**: Select `Language > Japanese / English`

### Bug Reports

If you find a bug or have a feature request, please report it via GitHub Issues.

👉 **[GitHub Issues](https://github.com/your-username/beginview/issues)**

### Disclaimer

This application is developed for personal and experimental purposes.  
The developer assumes no responsibility for any damages caused by the use of this application.

### Technical Information

This application is developed with **Python + PySide6**.  
PySide6 is provided under the LGPL license.

---

**© 2025 tensarestudio**
