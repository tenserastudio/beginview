# GitHub公開準備ガイド

このドキュメントでは、BeginViewをGitHubで公開するための手順を説明します。

## 1. ディレクトリ構成

```
beginview/
├── src/                    # ソースコード
│   ├── main.py
│   ├── beginview_window.py
│   └── i18n.py
├── dist/                   # PyInstaller出力（.gitignore対象）
├── build/                  # PyInstallerビルド生成物（.gitignore対象）
├── assets/                 # アイコンなど（必要に応じて）
├── release_notes/          # リリースノート
│   └── v0.3.md
├── README.md              # ユーザー向けREADME
├── BUILD.md               # ビルド手順（開発者向け）
├── IMPLEMENTATION_STATUS.md # 実装状況ドキュメント
├── pyinstaller.spec      # PyInstaller設定ファイル
├── requirements.txt       # 依存関係
└── .gitignore            # Git除外設定
```

## 2. GitHubリポジトリの作成

1. GitHubにログイン
2. 新しいリポジトリを作成
   - リポジトリ名: `beginview`（または任意の名前）
   - 公開設定: **Public**（ソース非公開でもPublicでOK）
   - README、.gitignore、ライセンス: 追加しない（既に存在するため）

## 3. 初回コミットとプッシュ

```bash
# Gitリポジトリを初期化（まだの場合）
git init

# リモートリポジトリを追加
git remote add origin https://github.com/your-username/beginview.git

# ファイルをステージング
git add .

# 初回コミット
git commit -m "Initial commit: BeginView v0.3"

# メインブランチにプッシュ
git branch -M main
git push -u origin main
```

## 4. GitHub Releasesの作成

### 4.1 exeファイルのビルド

```bash
# 仮想環境をアクティベート
.\venv\Scripts\Activate.ps1

# PyInstallerでビルド
pyinstaller --noconfirm --clean pyinstaller.spec
```

### 4.2 リリースの作成

1. GitHubリポジトリのページに移動
2. "Releases" をクリック
3. "Draft a new release" をクリック
4. 以下を入力：
   - **Tag**: `v0.3`（例）
   - **Release title**: `BeginView v0.3`
   - **Description**: `release_notes/v0.3.md` の内容をコピー
5. `dist/BeginView.exe` をドラッグ&ドロップでアップロード
6. "Publish release" をクリック

## 5. README.mdの更新

GitHubのユーザー名に合わせて、README.md内の以下の部分を更新してください：

- `https://github.com/your-username/beginview` → 実際のリポジトリURL
- `your-username` → 実際のGitHubユーザー名

## 6. 今後のリリース手順

1. コードを更新
2. `release_notes/vX.X.md` を作成
3. exeをビルド
4. GitHub Releasesで新しいリリースを作成
5. exeファイルをアップロード

## 注意事項

- **ソースコードは公開されます**（Publicリポジトリの場合）
- ソース非公開にしたい場合は、Privateリポジトリにして、Releasesのみ公開する方法を検討してください
- exeファイルは `dist/` に生成されますが、`.gitignore` で除外されているため、Gitには含まれません
- Releasesにアップロードするexeファイルは、手動でアップロードする必要があります

