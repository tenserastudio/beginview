"""
BeginView - シンプルな画像スライドショービューア
エントリポイント
"""

import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication

# 同じディレクトリからのインポート
from beginview_window import BeginViewWindow

# PyInstallerでビルドされた場合のパス解決
if getattr(sys, 'frozen', False):
    # PyInstallerでビルドされた場合
    base_path = Path(sys._MEIPASS)
else:
    # 通常のPython実行の場合
    base_path = Path(__file__).parent


def main() -> None:
    """アプリケーションのメインエントリポイント"""
    app = QApplication(sys.argv)
    
    # メインウィンドウを作成して表示
    window = BeginViewWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

