# GitHub公開準備 - 変更点まとめ

**作成日**: 2025-11-30

## 📁 ディレクトリ構成の変更

### 新規作成されたディレクトリ

- `src/` - ソースコードを格納
  - `main.py` (移動)
  - `beginview_window.py` (移動)
  - `i18n.py` (移動)
- `dist/` - PyInstaller出力用（.gitignore対象）
- `build/` - PyInstallerビルド生成物用（.gitignore対象）
- `assets/` - アイコンなど（将来使用）
- `release_notes/` - リリースノート
  - `v0.3.md` (新規作成)

## 📄 新規作成されたファイル

### 1. `README.md` (ユーザー向け)
- 日本語/英語のバイリンガルREADME
- ダウンロード方法、使い方、操作説明
- GitHub Releasesへのリンク
- 免責事項、技術情報

### 2. `pyinstaller.spec`
- PyInstaller設定ファイル
- onefileモード、コンソール非表示
- i18n.pyの明示的な含め込み
- アイコン設定（コメントアウト）

### 3. `BUILD.md`
- ビルド手順の詳細ドキュメント
- PyInstallerのインストール方法
- ビルドオプションの説明
- トラブルシューティング

### 4. `release_notes/v0.3.md`
- v0.3のリリースノートテンプレート
- 新機能、既知の問題、改善予定
- ダウンロードリンク例

### 5. `GITHUB_SETUP.md`
- GitHub公開手順ガイド
- リポジトリ作成からReleases公開まで
- 今後のリリース手順

### 6. `CHANGES.md` (このファイル)
- 変更点のまとめ

## 🔧 変更されたファイル

### 1. `src/i18n.py`
- Aboutダイアログ用の翻訳キーを追加
  - `menu_about`
  - `about_title`
  - `about_version`
  - `about_copyright`
  - `about_built_with`
  - `about_language`

### 2. `src/beginview_window.py`
- Helpメニューを追加
- Aboutダイアログ機能を実装（`_show_about`メソッド）
- `_update_ui_texts`メソッドにHelpメニューの更新処理を追加

### 3. `src/main.py`
- PyInstaller対応のパス解決コードを追加
- `sys._MEIPASS`のチェック

### 4. `.gitignore`
- `*.spec`のコメントアウト（specファイルはGitに含める）

## ✨ 新機能

### Aboutダイアログ
- `Help > About BeginView` からアクセス可能
- バージョン情報、著作権表示
- 技術情報（Python + PySide6）
- 多言語対応（日本語/英語）

## 📋 次のステップ

1. **GitHubリポジトリの作成**
   - リポジトリ名を決定
   - Publicリポジトリとして作成

2. **初回コミットとプッシュ**
   ```bash
   git init
   git remote add origin https://github.com/your-username/beginview.git
   git add .
   git commit -m "Initial commit: BeginView v0.3"
   git branch -M main
   git push -u origin main
   ```

3. **exeファイルのビルド**
   ```bash
   pyinstaller --noconfirm --clean pyinstaller.spec
   ```

4. **GitHub Releasesの作成**
   - `dist/BeginView.exe`をアップロード
   - `release_notes/v0.3.md`の内容をコピー

5. **README.mdの更新**
   - GitHubのユーザー名/リポジトリ名に合わせてURLを更新

## ⚠️ 注意事項

- `src/`ディレクトリに移動したため、実行時は`python src/main.py`ではなく、`python -m src.main`または`cd src && python main.py`で実行する必要があります
- PyInstallerでビルドする場合は、`pyinstaller.spec`を使用してください（パスが正しく設定されています）
- GitHubのユーザー名に合わせて、README.mdとrelease_notes内のURLを更新してください

