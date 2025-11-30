"""
BeginView - 簡易な多言語対応モジュール
日本語/英語の文字列辞書を提供
"""

from typing import Dict

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "ja": {
        "app_title": "BeginView",
        "menu_file": "ファイル(&F)",
        "menu_open_folder": "フォルダを開く(&O)...",
        "menu_exit": "終了(&X)",
        "menu_language": "言語(&L)",
        "menu_lang_ja": "日本語(&J)",
        "menu_lang_en": "English(&E)",
        "msg_no_images_title": "画像なし",
        "msg_no_images_body": "このフォルダには画像ファイルがありません。",
        "msg_error_loading_title": "エラー",
        "msg_error_loading_body": "画像の読み込み中にエラーが発生しました: {filename}",
        "menu_settings": "設定(&S)",
        "menu_interval": "スライドショー間隔(&I)",
        "menu_interval_1s": "1秒",
        "menu_interval_2s": "2秒",
        "menu_interval_3s": "3秒（デフォルト）",
        "menu_interval_5s": "5秒",
        "menu_interval_10s": "10秒",
        "menu_include_subfolders": "サブフォルダを含める(&R)",
        "menu_interval_custom": "カスタム間隔(&C)...",
        "dialog_interval_title": "スライドショー間隔",
        "dialog_interval_label": "間隔（秒）:",
        "dialog_interval_invalid": "無効な値です。1以上の数値を入力してください。",
        "menu_view": "表示(&V)",
        "menu_zoom_fit": "ウィンドウに合わせる(&F)",
        "menu_zoom_100": "100%表示(&1)",
        "menu_zoom_in": "拡大(&+)",
        "menu_zoom_out": "縮小(&-)",
        "menu_show_info": "画像情報を表示(&I)",
        "info_title": "画像情報",
        "info_filename": "ファイル名:",
        "info_size": "サイズ:",
        "info_dimensions": "解像度:",
        "info_current": "現在:",
        "info_total": "合計:",
        "menu_about": "BeginViewについて(&A)",
        "about_title": "BeginView について",
        "about_version": "バージョン",
        "about_copyright": "© 2025 tensarestudio",
        "about_built_with": "Built with Python + PySide6",
        "about_language": "日本語/英語対応",
    },
    "en": {
        "app_title": "BeginView",
        "menu_file": "File(&F)",
        "menu_open_folder": "Open Folder(&O)...",
        "menu_exit": "Exit(&X)",
        "menu_language": "Language(&L)",
        "menu_lang_ja": "Japanese(&J)",
        "menu_lang_en": "English(&E)",
        "msg_no_images_title": "No Images",
        "msg_no_images_body": "No image files were found in this folder.",
        "msg_error_loading_title": "Error",
        "msg_error_loading_body": "An error occurred while loading the image: {filename}",
        "menu_settings": "Settings(&S)",
        "menu_interval": "Slide Show Interval(&I)",
        "menu_interval_1s": "1 second",
        "menu_interval_2s": "2 seconds",
        "menu_interval_3s": "3 seconds (default)",
        "menu_interval_5s": "5 seconds",
        "menu_interval_10s": "10 seconds",
        "menu_include_subfolders": "Include Subfolders(&R)",
        "menu_interval_custom": "Custom Interval(&C)...",
        "dialog_interval_title": "Slide Show Interval",
        "dialog_interval_label": "Interval (seconds):",
        "dialog_interval_invalid": "Invalid value. Please enter a number greater than or equal to 1.",
        "menu_view": "View(&V)",
        "menu_zoom_fit": "Fit to Window(&F)",
        "menu_zoom_100": "100%(&1)",
        "menu_zoom_in": "Zoom In(&+)",
        "menu_zoom_out": "Zoom Out(&-)",
        "menu_show_info": "Show Image Info(&I)",
        "info_title": "Image Information",
        "info_filename": "Filename:",
        "info_size": "Size:",
        "info_dimensions": "Dimensions:",
        "info_current": "Current:",
        "info_total": "Total:",
        "menu_about": "About BeginView(&A)",
        "about_title": "About BeginView",
        "about_version": "Version",
        "about_copyright": "© 2025 tensarestudio",
        "about_built_with": "Built with Python + PySide6",
        "about_language": "Japanese/English support",
    },
}


def get_text(lang_code: str, key: str) -> str:
    """
    指定された言語コードとキーから翻訳テキストを取得
    
    Args:
        lang_code: 言語コード ("ja" または "en")
        key: 翻訳キー
    
    Returns:
        翻訳されたテキスト。キーが見つからない場合はキー自体を返す
    """
    return TRANSLATIONS.get(lang_code, TRANSLATIONS["en"]).get(key, key)

