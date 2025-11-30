"""
BeginView - メインウィンドウクラス
画像スライドショー表示機能を提供
"""

import os
from pathlib import Path
from typing import List, Optional

from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QMenuBar,
    QFileDialog,
    QMessageBox,
    QVBoxLayout,
    QWidget,
    QInputDialog,
)
from PySide6.QtCore import Qt, QTimer, QSize, QPoint
from PySide6.QtGui import QPixmap, QKeyEvent, QImage, QMouseEvent, QWheelEvent

from i18n import get_text


class BeginViewWindow(QMainWindow):
    """BeginView のメインウィンドウクラス"""

    # サポートする画像拡張子
    SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

    def __init__(self) -> None:
        """ウィンドウを初期化"""
        super().__init__()

        # 状態管理
        self.current_language: str = "ja"  # デフォルトは日本語
        self.image_files: List[Path] = []
        self.current_index: int = 0
        self.is_playing: bool = False
        self.slide_timer: Optional[QTimer] = None
        self.slide_interval: int = 3000  # デフォルト3秒（ミリ秒）
        self.include_subfolders: bool = False  # サブフォルダを含めるかどうか
        
        # ズーム機能用の状態
        self.original_pixmap: Optional[QPixmap] = None  # 元の画像
        self.zoom_factor: float = 1.0  # ズーム倍率（1.0 = 100%）
        self.zoom_mode: str = "fit"  # "fit", "100", "custom"

        # UI初期化
        self._init_ui()
        self._init_timer()
        self._update_ui_texts()

    def _init_ui(self) -> None:
        """UIコンポーネントを初期化"""
        # 中央ウィジェットとレイアウト
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # 画像表示用のラベル
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: black;")
        self.image_label.setText("フォルダを選択してください")
        # マウスイベントを有効化
        self.image_label.setMouseTracking(False)
        self.image_label.mousePressEvent = self._on_image_label_clicked
        self.image_label.mouseDoubleClickEvent = self._on_image_label_double_clicked
        self.image_label.wheelEvent = self._on_image_label_wheel
        layout.addWidget(self.image_label)

        # メニューバーを作成
        self._create_menu_bar()

        # ウィンドウ設定
        self.setMinimumSize(800, 600)
        self.resize(1200, 800)

    def _create_menu_bar(self) -> None:
        """メニューバーを作成"""
        menubar = self.menuBar()

        # File メニュー
        file_menu = menubar.addMenu("")  # テキストは _update_ui_texts() で設定
        self.file_menu = file_menu

        self.open_folder_action = file_menu.addAction("")
        self.open_folder_action.triggered.connect(self._on_open_folder)

        file_menu.addSeparator()

        self.exit_action = file_menu.addAction("")
        self.exit_action.triggered.connect(self.close)

        # Help メニュー（About用）
        help_menu = menubar.addMenu("")
        self.help_menu = help_menu

        self.about_action = help_menu.addAction("")
        self.about_action.triggered.connect(self._show_about)

        # Language メニュー
        lang_menu = menubar.addMenu("")
        self.lang_menu = lang_menu

        self.lang_ja_action = lang_menu.addAction("")
        self.lang_ja_action.triggered.connect(lambda: self._set_language("ja"))

        self.lang_en_action = lang_menu.addAction("")
        self.lang_en_action.triggered.connect(lambda: self._set_language("en"))

        # Settings メニュー
        settings_menu = menubar.addMenu("")
        self.settings_menu = settings_menu

        # スライドショー間隔サブメニュー
        interval_menu = settings_menu.addMenu("")
        self.interval_menu = interval_menu

        self.interval_1s_action = interval_menu.addAction("")
        self.interval_1s_action.setCheckable(True)
        self.interval_1s_action.triggered.connect(lambda: self._set_interval(1000))

        self.interval_2s_action = interval_menu.addAction("")
        self.interval_2s_action.setCheckable(True)
        self.interval_2s_action.triggered.connect(lambda: self._set_interval(2000))

        self.interval_3s_action = interval_menu.addAction("")
        self.interval_3s_action.setCheckable(True)
        self.interval_3s_action.triggered.connect(lambda: self._set_interval(3000))

        self.interval_5s_action = interval_menu.addAction("")
        self.interval_5s_action.setCheckable(True)
        self.interval_5s_action.triggered.connect(lambda: self._set_interval(5000))

        self.interval_10s_action = interval_menu.addAction("")
        self.interval_10s_action.setCheckable(True)
        self.interval_10s_action.triggered.connect(lambda: self._set_interval(10000))
        
        # デフォルトで3秒をチェック
        self.interval_3s_action.setChecked(True)

        settings_menu.addSeparator()
        
        self.interval_custom_action = interval_menu.addAction("")
        self.interval_custom_action.triggered.connect(self._set_custom_interval)

        settings_menu.addSeparator()

        self.include_subfolders_action = settings_menu.addAction("")
        self.include_subfolders_action.setCheckable(True)
        self.include_subfolders_action.triggered.connect(self._toggle_include_subfolders)
        
        # View メニュー
        view_menu = menubar.addMenu("")
        self.view_menu = view_menu
        
        self.zoom_fit_action = view_menu.addAction("")
        self.zoom_fit_action.triggered.connect(self._zoom_fit)
        
        self.zoom_100_action = view_menu.addAction("")
        self.zoom_100_action.triggered.connect(self._zoom_100)
        
        view_menu.addSeparator()
        
        self.zoom_in_action = view_menu.addAction("")
        self.zoom_in_action.triggered.connect(self._zoom_in)
        
        self.zoom_out_action = view_menu.addAction("")
        self.zoom_out_action.triggered.connect(self._zoom_out)
        
        view_menu.addSeparator()
        
        self.show_info_action = view_menu.addAction("")
        self.show_info_action.triggered.connect(self._show_image_info)

    def _init_timer(self) -> None:
        """スライドショー用タイマーを初期化"""
        self.slide_timer = QTimer(self)
        self.slide_timer.timeout.connect(self._on_timer_tick)
        self.slide_timer.setInterval(self.slide_interval)

    def _update_ui_texts(self) -> None:
        """現在の言語設定に基づいてUIテキストを更新"""
        # ウィンドウタイトル
        self.setWindowTitle(get_text(self.current_language, "app_title"))

        # メニュー
        self.file_menu.setTitle(get_text(self.current_language, "menu_file"))
        self.open_folder_action.setText(
            get_text(self.current_language, "menu_open_folder")
        )
        self.exit_action.setText(get_text(self.current_language, "menu_exit"))

        self.lang_menu.setTitle(get_text(self.current_language, "menu_language"))
        self.lang_ja_action.setText(
            get_text(self.current_language, "menu_lang_ja")
        )
        self.lang_en_action.setText(
            get_text(self.current_language, "menu_lang_en")
        )

        # Settings メニュー
        self.settings_menu.setTitle(get_text(self.current_language, "menu_settings"))
        self.interval_menu.setTitle(get_text(self.current_language, "menu_interval"))
        self.interval_1s_action.setText(
            get_text(self.current_language, "menu_interval_1s")
        )
        self.interval_2s_action.setText(
            get_text(self.current_language, "menu_interval_2s")
        )
        self.interval_3s_action.setText(
            get_text(self.current_language, "menu_interval_3s")
        )
        self.interval_5s_action.setText(
            get_text(self.current_language, "menu_interval_5s")
        )
        self.interval_10s_action.setText(
            get_text(self.current_language, "menu_interval_10s")
        )
        self.interval_custom_action.setText(
            get_text(self.current_language, "menu_interval_custom")
        )
        self.include_subfolders_action.setText(
            get_text(self.current_language, "menu_include_subfolders")
        )
        self.include_subfolders_action.setChecked(self.include_subfolders)
        
        # View メニュー
        self.view_menu.setTitle(get_text(self.current_language, "menu_view"))
        self.zoom_fit_action.setText(
            get_text(self.current_language, "menu_zoom_fit")
        )
        self.zoom_100_action.setText(
            get_text(self.current_language, "menu_zoom_100")
        )
        self.zoom_in_action.setText(
            get_text(self.current_language, "menu_zoom_in")
        )
        self.zoom_out_action.setText(
            get_text(self.current_language, "menu_zoom_out")
        )
        self.show_info_action.setText(
            get_text(self.current_language, "menu_show_info")
        )

        # Help メニュー
        if self.current_language == "ja":
            self.help_menu.setTitle("ヘルプ(&H)")
        else:
            self.help_menu.setTitle("Help(&H)")
        self.about_action.setText(
            get_text(self.current_language, "menu_about")
        )

        # 画像が無い場合のラベルテキスト
        if not self.image_files:
            if self.current_language == "ja":
                self.image_label.setText("フォルダを選択してください")
            else:
                self.image_label.setText("Please select a folder")

    def _set_language(self, lang_code: str) -> None:
        """言語を切り替え"""
        self.current_language = lang_code
        self._update_ui_texts()

    def _on_open_folder(self) -> None:
        """フォルダ選択ダイアログを表示して画像ファイルを読み込む"""
        folder_path = QFileDialog.getExistingDirectory(
            self, get_text(self.current_language, "menu_open_folder")
        )

        if not folder_path:
            return  # キャンセルされた場合

        # 画像ファイルを取得
        folder = Path(folder_path)
        
        if self.include_subfolders:
            # サブフォルダも含めて再帰的に検索
            image_files = [
                f
                for f in folder.rglob("*")
                if f.is_file() and f.suffix.lower() in self.SUPPORTED_EXTENSIONS
            ]
        else:
            # 現在のフォルダのみ
            image_files = [
                f
                for f in folder.iterdir()
                if f.is_file() and f.suffix.lower() in self.SUPPORTED_EXTENSIONS
            ]

        # ファイル名でソート
        image_files.sort(key=lambda x: x.name.lower())

        if not image_files:
            # 画像が無い場合のメッセージ
            QMessageBox.information(
                self,
                get_text(self.current_language, "msg_no_images_title"),
                get_text(self.current_language, "msg_no_images_body"),
            )
            return

        # 画像リストを更新
        self.image_files = image_files
        self.current_index = 0
        self.is_playing = True

        # タイマーを開始
        self.slide_timer.start()

        # 最初の画像を表示
        self._show_image(self.current_index)

    def _show_image(self, index: int) -> None:
        """
        指定されたインデックスの画像を表示
        
        Args:
            index: 表示する画像のインデックス
        """
        if not self.image_files or index < 0 or index >= len(self.image_files):
            return

        try:
            image_path = self.image_files[index]
            pixmap = QPixmap(str(image_path))

            if pixmap.isNull():
                raise ValueError(f"Failed to load image: {image_path}")

            # 元の画像を保存
            self.original_pixmap = pixmap
            
            # ズームモードに応じて表示
            if self.zoom_mode == "fit":
                self.zoom_factor = 1.0
                scaled_pixmap = self._scale_pixmap(pixmap)
            elif self.zoom_mode == "100":
                self.zoom_factor = 1.0
                scaled_pixmap = pixmap
            else:  # custom
                scaled_pixmap = self._apply_zoom(pixmap)
            
            self.image_label.setPixmap(scaled_pixmap)

            self.current_index = index

        except Exception as e:
            # エラーログをコンソールに出力（本番ではロガーを使う）
            print(
                get_text(self.current_language, "msg_error_loading_body").format(
                    filename=str(self.image_files[index])
                )
            )
            print(f"Error details: {e}")

            # 次の画像へ進む（最後の画像の場合は先頭へ）
            if index < len(self.image_files) - 1:
                self._show_image(index + 1)
            elif len(self.image_files) > 0:
                self._show_image(0)

    def _scale_pixmap(self, pixmap: QPixmap) -> QPixmap:
        """
        ウィンドウサイズに合わせてPixmapをスケーリング
        
        Args:
            pixmap: スケーリングするQPixmap
        
        Returns:
            スケーリングされたQPixmap
        """
        label_size = self.image_label.size()
        if label_size.width() <= 0 or label_size.height() <= 0:
            return pixmap

        scaled = pixmap.scaled(
            label_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        return scaled

    def resizeEvent(self, event) -> None:
        """ウィンドウサイズ変更時に画像を再スケーリング"""
        super().resizeEvent(event)
        if self.image_files and 0 <= self.current_index < len(self.image_files):
            # ズームモードがfitの場合は再スケーリング
            if self.zoom_mode == "fit" and self.original_pixmap:
                scaled_pixmap = self._scale_pixmap(self.original_pixmap)
                self.image_label.setPixmap(scaled_pixmap)
            elif self.zoom_mode in ["100", "custom"] and self.original_pixmap:
                # カスタムズームの場合は再適用
                scaled_pixmap = self._apply_zoom(self.original_pixmap)
                self.image_label.setPixmap(scaled_pixmap)

    def _on_timer_tick(self) -> None:
        """タイマーのtick時に次の画像へ進む"""
        if not self.image_files:
            return

        self.current_index = (self.current_index + 1) % len(self.image_files)
        self._show_image(self.current_index)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """キーボード操作を処理"""
        key = event.key()

        # Space: 再生/一時停止をトグル
        if key == Qt.Key.Key_Space:
            self._toggle_play_pause()

        # Right Arrow: 次の画像
        elif key == Qt.Key.Key_Right:
            self._next_image()

        # Left Arrow: 前の画像
        elif key == Qt.Key.Key_Left:
            self._previous_image()

        # F11: フルスクリーントグル
        elif key == Qt.Key.Key_F11:
            self._toggle_fullscreen()

        # Esc: フルスクリーンから戻る
        elif key == Qt.Key.Key_Escape:
            if self.isFullScreen():
                self.showNormal()
            elif self.zoom_mode != "fit":
                # ズームモードをfitに戻す
                self._zoom_fit()

        # Plus/Equal: ズームイン
        elif key in (Qt.Key.Key_Plus, Qt.Key.Key_Equal):
            self._zoom_in()

        # Minus: ズームアウト
        elif key == Qt.Key.Key_Minus:
            self._zoom_out()

        # 0: 100%表示
        elif key == Qt.Key.Key_0:
            self._zoom_100()

        # F: フィット表示
        elif key == Qt.Key.Key_F:
            self._zoom_fit()

        # I: 画像情報表示
        elif key == Qt.Key.Key_I:
            self._show_image_info()

        else:
            super().keyPressEvent(event)

    def _toggle_play_pause(self) -> None:
        """再生/一時停止をトグル"""
        if not self.image_files:
            return

        self.is_playing = not self.is_playing
        if self.is_playing:
            self.slide_timer.start()
        else:
            self.slide_timer.stop()

    def _next_image(self) -> None:
        """次の画像へ進む"""
        if not self.image_files:
            return

        self.current_index = (self.current_index + 1) % len(self.image_files)
        self._show_image(self.current_index)

    def _previous_image(self) -> None:
        """前の画像へ戻る"""
        if not self.image_files:
            return

        self.current_index = (self.current_index - 1) % len(self.image_files)
        self._show_image(self.current_index)

    def _toggle_fullscreen(self) -> None:
        """フルスクリーンと通常ウィンドウをトグル"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def _on_image_label_clicked(self, event: QMouseEvent) -> None:
        """画像ラベルのシングルクリックイベント（再生/一時停止をトグル）"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._toggle_play_pause()

    def _on_image_label_double_clicked(self, event: QMouseEvent) -> None:
        """画像ラベルのダブルクリックイベント（フルスクリーンをトグル）"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._toggle_fullscreen()

    def _set_interval(self, interval_ms: int) -> None:
        """
        スライドショー間隔を設定
        
        Args:
            interval_ms: 間隔（ミリ秒）
        """
        self.slide_interval = interval_ms
        self.slide_timer.setInterval(interval_ms)
        
        # メニューのチェック状態を更新
        self.interval_1s_action.setChecked(interval_ms == 1000)
        self.interval_2s_action.setChecked(interval_ms == 2000)
        self.interval_3s_action.setChecked(interval_ms == 3000)
        self.interval_5s_action.setChecked(interval_ms == 5000)
        self.interval_10s_action.setChecked(interval_ms == 10000)

    def _toggle_include_subfolders(self) -> None:
        """サブフォルダを含める設定をトグル"""
        self.include_subfolders = self.include_subfolders_action.isChecked()

    def _set_custom_interval(self) -> None:
        """カスタム間隔を設定するダイアログを表示"""
        current_seconds = self.slide_interval / 1000.0
        value, ok = QInputDialog.getDouble(
            self,
            get_text(self.current_language, "dialog_interval_title"),
            get_text(self.current_language, "dialog_interval_label"),
            current_seconds,
            0.1,
            3600.0,
            1,
        )
        
        if ok and value >= 0.1:
            interval_ms = int(value * 1000)
            self._set_interval(interval_ms)
            # カスタム間隔の場合は、すべてのチェックを外す
            self.interval_1s_action.setChecked(False)
            self.interval_2s_action.setChecked(False)
            self.interval_3s_action.setChecked(False)
            self.interval_5s_action.setChecked(False)
            self.interval_10s_action.setChecked(False)
        elif ok:
            QMessageBox.warning(
                self,
                get_text(self.current_language, "msg_error_loading_title"),
                get_text(self.current_language, "dialog_interval_invalid"),
            )

    def _apply_zoom(self, pixmap: QPixmap) -> QPixmap:
        """
        ズーム倍率を適用してPixmapをスケーリング
        
        Args:
            pixmap: 元のQPixmap
        
        Returns:
            ズーム適用後のQPixmap
        """
        if not pixmap or pixmap.isNull():
            return pixmap
        
        original_size = pixmap.size()
        new_size = QSize(
            int(original_size.width() * self.zoom_factor),
            int(original_size.height() * self.zoom_factor),
        )
        
        scaled = pixmap.scaled(
            new_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        return scaled

    def _zoom_fit(self) -> None:
        """ウィンドウに合わせて表示"""
        self.zoom_mode = "fit"
        self.zoom_factor = 1.0
        if self.original_pixmap:
            scaled_pixmap = self._scale_pixmap(self.original_pixmap)
            self.image_label.setPixmap(scaled_pixmap)

    def _zoom_100(self) -> None:
        """100%表示（等倍）"""
        self.zoom_mode = "100"
        self.zoom_factor = 1.0
        if self.original_pixmap:
            self.image_label.setPixmap(self.original_pixmap)

    def _zoom_in(self) -> None:
        """ズームイン（拡大）"""
        if not self.original_pixmap:
            return
        
        self.zoom_mode = "custom"
        self.zoom_factor = min(self.zoom_factor * 1.2, 10.0)  # 最大10倍
        
        scaled_pixmap = self._apply_zoom(self.original_pixmap)
        self.image_label.setPixmap(scaled_pixmap)

    def _zoom_out(self) -> None:
        """ズームアウト（縮小）"""
        if not self.original_pixmap:
            return
        
        self.zoom_mode = "custom"
        self.zoom_factor = max(self.zoom_factor / 1.2, 0.1)  # 最小0.1倍
        
        scaled_pixmap = self._apply_zoom(self.original_pixmap)
        self.image_label.setPixmap(scaled_pixmap)

    def _on_image_label_wheel(self, event: QWheelEvent) -> None:
        """マウスホイールイベント（ズーム）"""
        if not self.original_pixmap:
            return
        
        # ホイールの回転量を取得
        delta = event.angleDelta().y()
        
        if delta > 0:
            # 上に回転 = ズームイン
            self._zoom_in()
        else:
            # 下に回転 = ズームアウト
            self._zoom_out()

    def _show_image_info(self) -> None:
        """画像情報を表示"""
        if not self.image_files or self.current_index < 0 or self.current_index >= len(self.image_files):
            return
        
        image_path = self.image_files[self.current_index]
        
        # ファイル情報を取得
        file_size = image_path.stat().st_size
        file_size_mb = file_size / (1024 * 1024)
        
        # 画像サイズを取得
        if self.original_pixmap:
            width = self.original_pixmap.width()
            height = self.original_pixmap.height()
        else:
            width = height = 0
        
        # メッセージを作成
        info_text = f"{get_text(self.current_language, 'info_filename')} {image_path.name}\n"
        info_text += f"{get_text(self.current_language, 'info_size')} {file_size_mb:.2f} MB ({file_size:,} bytes)\n"
        if width > 0 and height > 0:
            info_text += f"{get_text(self.current_language, 'info_dimensions')} {width} × {height} px\n"
        info_text += f"\n{get_text(self.current_language, 'info_current')} {self.current_index + 1} / {len(self.image_files)}"
        
        QMessageBox.information(
            self,
            get_text(self.current_language, "info_title"),
            info_text,
        )

    def _show_about(self) -> None:
        """Aboutダイアログを表示"""
        about_text = f"{get_text(self.current_language, 'about_title')}\n\n"
        about_text += f"{get_text(self.current_language, 'about_version')} 0.3\n\n"
        about_text += f"{get_text(self.current_language, 'about_copyright')}\n\n"
        about_text += f"{get_text(self.current_language, 'about_built_with')}\n"
        about_text += f"{get_text(self.current_language, 'about_language')}"
        
        QMessageBox.about(
            self,
            get_text(self.current_language, "about_title"),
            about_text,
        )

