# BeginView ビルド手順

このドキュメントでは、BeginView を PyInstaller で exe 化する手順を説明します。

## 前提条件

- Python 3.11 以上
- PySide6 がインストールされていること
- PyInstaller がインストールされていること

## PyInstaller のインストール

```bash
pip install pyinstaller
```

## ビルド手順

### 1. 基本的なビルド（onefile）

```bash
pyinstaller --noconfirm --clean --onefile --name BeginView src/main.py
```

### 2. spec ファイルを使用したビルド（推奨）

```bash
pyinstaller --noconfirm --clean pyinstaller.spec
```

### 3. アイコンを指定する場合

アイコンファイル（`.ico`）を `assets/icon.ico` に配置し、`pyinstaller.spec` の以下の行のコメントを外してください：

```python
icon='assets/icon.ico',
```

その後、以下のコマンドでビルド：

```bash
pyinstaller --noconfirm --clean pyinstaller.spec
```

## ビルドオプションの説明

### 基本オプション

- `--noconfirm`: 既存の出力ディレクトリを上書きする（確認なし）
- `--clean`: ビルド前にキャッシュと一時ファイルを削除
- `--onefile`: 単一の実行可能ファイルとして出力
- `--name BeginView`: 出力ファイル名を指定

### PySide6 用の追加オプション（必要に応じて）

```bash
pyinstaller \
  --noconfirm \
  --clean \
  --onefile \
  --name BeginView \
  --hidden-import PySide6.QtCore \
  --hidden-import PySide6.QtGui \
  --hidden-import PySide6.QtWidgets \
  --collect-all PySide6 \
  src/main.py
```

## 出力ファイル

ビルドが成功すると、以下の場所にファイルが生成されます：

- **実行ファイル**: `dist/BeginView.exe`
- **ビルド一時ファイル**: `build/` ディレクトリ（削除しても問題なし）

## 初回ビルド時の注意点

### 1. パスの問題

- `src/main.py` からの相対パスで `i18n.py` をインポートしている場合、PyInstaller が正しく検出できない可能性があります
- `pyinstaller.spec` の `datas` セクションで `i18n.py` を明示的に含めています

### 2. 相対パスの解決

実行時に相対パスを解決する必要がある場合、以下のようなコードを追加してください：

```python
import sys
import os

if getattr(sys, 'frozen', False):
    # PyInstallerでビルドされた場合
    base_path = sys._MEIPASS
else:
    # 通常のPython実行の場合
    base_path = os.path.dirname(os.path.abspath(__file__))
```

### 3. 動作確認

ビルド後は、以下の点を確認してください：

- ✅ exe ファイルが正常に起動するか
- ✅ 画像フォルダを開けるか
- ✅ スライドショーが動作するか
- ✅ 多言語切り替えが動作するか
- ✅ すべての機能が正常に動作するか

## トラブルシューティング

### エラー: "ModuleNotFoundError: No module named 'i18n'"

`pyinstaller.spec` の `datas` セクションを確認し、`i18n.py` が正しく含まれているか確認してください。

### エラー: PySide6 のモジュールが見つからない

`hiddenimports` に必要なモジュールを追加してください。

### exe ファイルが大きすぎる

PySide6 を含むため、exe ファイルは約 100-200MB になります。これは正常です。

## GitHub Releases へのアップロード

ビルドが成功したら、以下の手順で GitHub Releases にアップロードします：

1. `dist/BeginView.exe` を確認
2. GitHub の Releases ページに移動
3. "Draft a new release" をクリック
4. タグとリリースノートを入力
5. `BeginView.exe` をアップロード
6. "Publish release" をクリック

## 参考リンク

- [PyInstaller 公式ドキュメント](https://pyinstaller.org/)
- [PySide6 公式ドキュメント](https://doc.qt.io/qtforpython/)

